"""Reconstruct the OKX module-4 400-level BTC L2 archive for 2025-10-20.

The 6.8m-row stream is processed sequentially on a GitHub-hosted runner.
The raw archive is temporary; only compact metrics are retained.
"""
import hashlib
import heapq
import json
import statistics
import tarfile
import tempfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://www.okx.com"
API_PATH = "/api/v5/public/market-data-history"
SAMPLE_DAY = "2025-10-20"
FAMILY = "BTC-USDT"
INST_ID = "BTC-USDT-SWAP"
MODULE = "4"
METRIC_SAMPLE_EVERY_RECORDS = 10000


def parse_levels(levels, side, require_sorted=False):
    if not isinstance(levels, list):
        raise ValueError(f"{side} must be an array")
    result = {}
    previous = None
    for level in levels:
        if not isinstance(level, list) or len(level) != 3:
            raise ValueError(f"{side} level must contain price, size and order count")
        try:
            price, size, count = Decimal(str(level[0])), Decimal(str(level[1])), int(str(level[2]))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(f"{side} level contains invalid values") from exc
        if not price.is_finite() or not size.is_finite() or price <= 0 or size < 0 or count < 0:
            raise ValueError(f"{side} level contains out-of-range values")
        if require_sorted and previous is not None:
            if side == "bids" and price > previous:
                raise ValueError("Snapshot bids are not sorted descending")
            if side == "asks" and price < previous:
                raise ValueError("Snapshot asks are not sorted ascending")
        previous = price
        result[price] = (size, count)
    return result


def apply_updates(book, levels, side):
    if not isinstance(levels, list):
        raise ValueError(f"{side} update must be an array")
    for level in levels:
        if not isinstance(level, list) or len(level) != 3:
            raise ValueError(f"{side} update level must contain price, size and order count")
        try:
            price, size, count = Decimal(str(level[0])), Decimal(str(level[1])), int(str(level[2]))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(f"{side} update contains invalid values") from exc
        if not price.is_finite() or not size.is_finite() or price <= 0 or size < 0 or count < 0:
            raise ValueError(f"{side} update contains out-of-range values")
        if size == 0:
            book.pop(price, None)
        else:
            book[price] = (size, count)


def percentiles(values):
    if not values:
        return {"min": None, "p50": None, "p95": None, "max": None}
    ordered = sorted(values)
    idx = min(len(ordered) - 1, int((len(ordered) - 1) * 0.95 + 0.999999))
    return {"min": round(ordered[0], 8), "p50": round(statistics.median(ordered), 8),
            "p95": round(ordered[idx], 8), "max": round(ordered[-1], 8)}


def reconstruct_jsonl(handle, expected_inst_id=INST_ID, sample_every=METRIC_SAMPLE_EVERY_RECORDS):
    bids, asks = {}, {}
    actions, deltas, snapshot_intervals = Counter(), Counter(), Counter()
    spread, bid_depth, ask_depth = [], [], []
    previous_ts = previous_snapshot_ts = None
    first_ts = last_ts = None
    duplicate_ts = backwards_ts = seq_fields = crossed = empty = 0
    snapshot_bid_counts, snapshot_ask_counts = [], []
    max_bid = max_ask = rows = metric_points = 0
    first_keys = None

    def sample():
        nonlocal crossed, empty, metric_points
        if not bids or not asks:
            empty += 1
            return
        best_bid, best_ask = max(bids), min(asks)
        if best_bid >= best_ask:
            crossed += 1
        mid = (best_bid + best_ask) / Decimal(2)
        spread.append(float((best_ask - best_bid) / mid * Decimal(10000)))
        bp = heapq.nlargest(10, bids)
        ap = heapq.nsmallest(10, asks)
        bid_depth.append(float(sum(bids[p][0] for p in bp)))
        ask_depth.append(float(sum(asks[p][0] for p in ap)))
        metric_points += 1

    for raw in handle:
        if not raw.strip():
            continue
        try:
            row = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Malformed JSONL record") from exc
        if not isinstance(row, dict) or row.get("instId") != expected_inst_id:
            raise ValueError("Instrument ID mismatch")
        action = row.get("action")
        if action not in ("snapshot", "update"):
            raise ValueError("Unknown action")
        try:
            ts = int(row["ts"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Invalid timestamp") from exc
        if first_ts is None:
            first_ts, first_keys = ts, sorted(row.keys())
        if previous_ts is not None:
            delta = ts - previous_ts
            deltas[str(delta)] += 1
            duplicate_ts += int(delta == 0)
            backwards_ts += int(delta < 0)
        previous_ts, last_ts = ts, ts
        seq_fields += int("seqId" in row or "prevSeqId" in row)

        if action == "snapshot":
            bids = parse_levels(row.get("bids"), "bids", True)
            asks = parse_levels(row.get("asks"), "asks", True)
            snapshot_bid_counts.append(len(bids))
            snapshot_ask_counts.append(len(asks))
            if previous_snapshot_ts is not None:
                snapshot_intervals[str(ts - previous_snapshot_ts)] += 1
            previous_snapshot_ts = ts
        else:
            if not snapshot_bid_counts:
                raise ValueError("Update arrived before initial snapshot")
            apply_updates(bids, row.get("bids"), "bids")
            apply_updates(asks, row.get("asks"), "asks")

        actions[action] += 1
        rows += 1
        max_bid, max_ask = max(max_bid, len(bids)), max(max_ask, len(asks))
        if rows == 1 or rows % sample_every == 0:
            sample()
    if rows and (rows - 1) % sample_every:
        sample()
    if not rows or not snapshot_bid_counts:
        raise ValueError("No usable snapshot/update stream")
    return {
        "record_count": rows, "action_counts": dict(actions),
        "snapshot_count": len(snapshot_bid_counts),
        "snapshot_intervals_ms": dict(snapshot_intervals),
        "snapshot_bid_level_count_min": min(snapshot_bid_counts),
        "snapshot_bid_level_count_max": max(snapshot_bid_counts),
        "snapshot_ask_level_count_min": min(snapshot_ask_counts),
        "snapshot_ask_level_count_max": max(snapshot_ask_counts),
        "timestamp_delta_counts_ms": dict(sorted(deltas.items(), key=lambda kv: int(kv[0]))),
        "duplicate_timestamps": duplicate_ts, "non_monotonic_timestamps": backwards_ts,
        "first_timestamp_ms": str(first_ts), "last_timestamp_ms": str(last_ts),
        "elapsed_seconds": (last_ts - first_ts) / 1000,
        "sequence_fields_seen": seq_fields, "first_record_keys": first_keys,
        "metric_sample_every_records": sample_every, "metric_sample_count": metric_points,
        "crossed_book_observations_sampled": crossed, "empty_book_observations_sampled": empty,
        "max_bid_levels_observed": max_bid, "max_ask_levels_observed": max_ask,
        "spread_bps": percentiles(spread),
        "top10_bid_depth_contracts": percentiles(bid_depth),
        "top10_ask_depth_contracts": percentiles(ask_depth),
        "depth_unit": "contracts (linear SWAP order-book size)",
        "reconstruction_policy": "snapshot replaces both sides; updates replace price levels; zero size removes price level; periodic snapshots reset book",
    }


def fetch_archive():
    begin = str(int(datetime.strptime(SAMPLE_DAY, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000))
    params = {"module": MODULE, "instType": "SWAP", "instFamilyList": FAMILY,
              "dateAggrType": "daily", "begin": begin, "end": begin}
    url = BASE_URL + API_PATH + "?" + urlencode(params)
    req = Request(url, headers={"User-Agent": "okxtester-g0-07-module4-reconstruction/1.0"})
    with urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode())
    if str(payload.get("code")) != "0":
        raise ValueError("OKX historical data API returned nonzero code")
    for block in payload.get("data", []):
        for detail in block.get("details", []):
            if detail.get("instFamily") == FAMILY:
                for item in detail.get("groupDetails", []):
                    if SAMPLE_DAY in item.get("filename", "") and item.get("url", "").startswith("https://"):
                        return item["url"], item
    raise ValueError("Expected module-4 archive not available")


def inspect_download(url, metadata):
    digest, size = hashlib.sha256(), 0
    with tempfile.NamedTemporaryFile(prefix="okx_module4_recon_", suffix=".tar.gz") as tmp:
        req = Request(url, headers={"User-Agent": "okxtester-g0-07-module4-reconstruction/1.0"})
        with urlopen(req, timeout=300) as response:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                tmp.write(chunk)
                digest.update(chunk)
                size += len(chunk)
        tmp.flush()
        with tarfile.open(tmp.name, "r:gz") as archive:
            members = [m for m in archive.getmembers() if m.isfile()]
            if len(members) != 1:
                raise ValueError("Expected one regular archive member")
            member = members[0]
            handle = archive.extractfile(member)
            if handle is None:
                raise ValueError("Unable to stream archive member")
            stats = reconstruct_jsonl(handle)
    return {"filename": metadata["filename"], "advertised_size_mb": metadata.get("sizeMB"),
            "downloaded_size_bytes": size, "downloaded_sha256": digest.hexdigest(),
            "member_name": member.name, "member_uncompressed_size_bytes": member.size, **stats}


def main():
    url, metadata = fetch_archive()
    result = inspect_download(url, metadata)
    report = {"audit_id": "G0-07_OKX_MODULE4_HISTORICAL_L2_BOOK_RECONSTRUCTION_V1",
              "captured_at_utc": datetime.now(timezone.utc).isoformat(),
              "date_utc": SAMPLE_DAY, "module": MODULE, "module_description": "400-level orderbook",
              "instrument_family": FAMILY, "downloaded_archive_retained": False,
              "result": result,
              "limitations": [
                  "One BTC instrument/day only; not full-period or cross-asset validation.",
                  "No seqId/prevSeqId means timestamp ordering cannot prove lossless update continuity.",
                  "Visible depth does not prove queue position, hidden liquidity, latency, market impact or fills.",
                  "Top-10 depth is contracts; historical effective contract-value metadata remains unresolved.",
                  "Metrics are sampled every 10,000 records and do not capture every transient book state.",
              ]}
    out = Path("reports/g0_07_module4_btc_l2_book_reconstruction_v1.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    json.loads(out.read_text(encoding="utf-8"))
    print("G0-07 MODULE-4 BTC BOOK RECONSTRUCTION PASS")
    print(f"Records={result['record_count']} snapshots={result['snapshot_count']} updates={result['action_counts'].get('update', 0)}")
    print(f"Spread bps={json.dumps(result['spread_bps'], sort_keys=True)}")
    print(f"Top10 depth contracts bid={json.dumps(result['top10_bid_depth_contracts'], sort_keys=True)} ask={json.dumps(result['top10_ask_depth_contracts'], sort_keys=True)}")
    print(f"Crossed sampled={result['crossed_book_observations_sampled']} empty sampled={result['empty_book_observations_sampled']}")
    print(f"Report={out}; raw archive retained=no")


if __name__ == "__main__":
    main()
