"""Reconstruct one historical OKX L2 book from snapshots and incremental updates.

Downloads only BTC-USDT-SWAP module 5 for 2025-11-01, reconstructs the book
in memory, writes compact statistics, then deletes the temporary archive.
Spread/depth metrics are sampled every ten records for efficiency.
No credentials are used and no historical raw data is retained.
"""
import argparse
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
SAMPLE_DAY = "2025-11-01"
SAMPLE_FAMILIES = ("BTC-USDT", "ETH-USDT", "SOL-USDT", "DOGE-USDT", "AVAX-USDT")
SAMPLE_MODULE = "5"
DEPTH_LIMIT = 5000
METRIC_SAMPLE_EVERY_RECORDS = 60


def _levels_to_map(levels, side):
    if not isinstance(levels, list):
        raise ValueError(f"{side} must be an array")
    result = {}
    previous = None
    for level in levels:
        if not isinstance(level, list) or len(level) != 3:
            raise ValueError(f"{side} level must contain price, size and order count")
        try:
            price = Decimal(str(level[0]))
            size = Decimal(str(level[1]))
            count = int(str(level[2]))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(f"{side} level contains invalid values") from exc
        if not price.is_finite() or not size.is_finite() or price <= 0 or size < 0 or count < 0:
            raise ValueError(f"{side} level contains out-of-range values")
        if previous is not None:
            if side == "bids" and price > previous:
                raise ValueError("Snapshot bids are not sorted descending")
            if side == "asks" and price < previous:
                raise ValueError("Snapshot asks are not sorted ascending")
        previous = price
        result[price] = (size, count)
    return result


def _apply_changes(book_side, levels, side):
    if not isinstance(levels, list):
        raise ValueError(f"{side} update must be an array")
    for level in levels:
        if not isinstance(level, list) or len(level) != 3:
            raise ValueError(f"{side} update level must contain price, size and order count")
        try:
            price = Decimal(str(level[0]))
            size = Decimal(str(level[1]))
            count = int(str(level[2]))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(f"{side} update contains invalid values") from exc
        if not price.is_finite() or not size.is_finite() or price <= 0 or size < 0 or count < 0:
            raise ValueError(f"{side} update contains out-of-range values")
        if size == 0:
            book_side.pop(price, None)
        else:
            book_side[price] = (size, count)



def _percentiles(values):
    if not values:
        return {"min": None, "p50": None, "p95": None, "max": None}
    ordered = sorted(values)
    p95_index = min(len(ordered) - 1, int((len(ordered) - 1) * 0.95 + 0.999999))
    return {
        "min": round(ordered[0], 8),
        "p50": round(statistics.median(ordered), 8),
        "p95": round(ordered[p95_index], 8),
        "max": round(ordered[-1], 8),
    }


def reconstruct_jsonl_member(handle, expected_inst_id):
    bids, asks = {}, {}
    actions = Counter()
    timestamp_deltas = Counter()
    snapshot_intervals = Counter()
    spread_bps = []
    bid_top10_contracts = []
    ask_top10_contracts = []
    previous_ts = None
    previous_snapshot_ts = None
    first_ts = None
    last_ts = None
    duplicate_timestamps = 0
    non_monotonic_timestamps = 0
    crossed_books_sampled = 0
    empty_books_sampled = 0
    snapshots = 0
    updates = 0
    max_bid_levels = 0
    max_ask_levels = 0
    seqid_fields_seen = 0
    first_keys = None
    snapshot_bid_level_counts = []
    snapshot_ask_level_counts = []
    metric_sample_rows = 0
    last_metric_row = 0
    rows = 0

    def capture_metrics(row_number):
        nonlocal metric_sample_rows, last_metric_row
        nonlocal crossed_books_sampled, empty_books_sampled
        if not bids or not asks:
            empty_books_sampled += 1
            last_metric_row = row_number
            return
        best_bid = max(bids)
        best_ask = min(asks)
        if best_bid >= best_ask:
            crossed_books_sampled += 1
        mid = (best_bid + best_ask) / Decimal("2")
        spread_bps.append(float((best_ask - best_bid) / mid * Decimal("10000")))
        top_bids = heapq.nlargest(10, bids)
        top_asks = heapq.nsmallest(10, asks)
        bid_top10_contracts.append(float(sum(bids[p][0] for p in top_bids)))
        ask_top10_contracts.append(float(sum(asks[p][0] for p in top_asks)))
        metric_sample_rows += 1
        last_metric_row = row_number

    for raw_line in handle:
        if not raw_line.strip():
            continue
        try:
            row = json.loads(raw_line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Archive member contains malformed JSON") from exc
        if not isinstance(row, dict) or row.get("instId") != expected_inst_id:
            raise ValueError("Archive record instrument ID mismatch")
        action = row.get("action")
        if action not in ("snapshot", "update"):
            raise ValueError("Archive action must be snapshot or update")
        try:
            ts = int(row["ts"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Archive timestamp is missing or invalid") from exc
        if first_ts is None:
            first_ts = ts
            first_keys = sorted(row.keys())
        if previous_ts is not None:
            delta = ts - previous_ts
            timestamp_deltas[str(delta)] += 1
            duplicate_timestamps += int(delta == 0)
            non_monotonic_timestamps += int(delta < 0)
        previous_ts = ts
        last_ts = ts
        if "seqId" in row or "prevSeqId" in row:
            seqid_fields_seen += 1

        if action == "snapshot":
            bids = _levels_to_map(row.get("bids"), "bids")
            asks = _levels_to_map(row.get("asks"), "asks")
            snapshots += 1
            snapshot_bid_level_counts.append(len(bids))
            snapshot_ask_level_counts.append(len(asks))
            if previous_snapshot_ts is not None:
                snapshot_intervals[str(ts - previous_snapshot_ts)] += 1
            previous_snapshot_ts = ts
        else:
            if snapshots == 0:
                raise ValueError("Incremental update arrived before first snapshot")
            _apply_changes(bids, row.get("bids"), "bids")
            _apply_changes(asks, row.get("asks"), "asks")
            updates += 1

        actions[action] += 1
        rows += 1
        max_bid_levels = max(max_bid_levels, len(bids))
        max_ask_levels = max(max_ask_levels, len(asks))
        if rows == 1 or rows % METRIC_SAMPLE_EVERY_RECORDS == 0:
            capture_metrics(rows)

    if rows != last_metric_row:
        capture_metrics(rows)
    if snapshots == 0 or not actions:
        raise ValueError("Archive contains no usable snapshot/update records")

    return {
        "record_count": rows,
        "action_counts": dict(actions),
        "snapshot_intervals_ms": dict(snapshot_intervals),
        "snapshot_bid_level_count_min": min(snapshot_bid_level_counts),
        "snapshot_bid_level_count_max": max(snapshot_bid_level_counts),
        "snapshot_ask_level_count_min": min(snapshot_ask_level_counts),
        "snapshot_ask_level_count_max": max(snapshot_ask_level_counts),
        "timestamp_delta_counts_ms": dict(sorted(timestamp_deltas.items(), key=lambda x: int(x[0]))),
        "timestamp_delta_exactly_1000ms_count": timestamp_deltas.get("1000", 0),
        "timestamp_delta_non_1000ms_count": sum(v for k, v in timestamp_deltas.items() if k != "1000"),
        "duplicate_timestamps": duplicate_timestamps,
        "non_monotonic_timestamps": non_monotonic_timestamps,
        "first_timestamp_ms": str(first_ts),
        "last_timestamp_ms": str(last_ts),
        "elapsed_seconds": (last_ts - first_ts) / 1000,
        "sequence_fields_seen": seqid_fields_seen,
        "first_record_keys": first_keys,
        "crossed_book_observations_sampled": crossed_books_sampled,
        "empty_book_observations_sampled": empty_books_sampled,
        "metric_sample_interval_records": METRIC_SAMPLE_EVERY_RECORDS,
        "metric_sample_count": metric_sample_rows,
        "max_bid_levels_observed": max_bid_levels,
        "max_ask_levels_observed": max_ask_levels,
        "spread_bps": _percentiles(spread_bps),
        "top10_bid_depth_contracts": _percentiles(bid_top10_contracts),
        "top10_ask_depth_contracts": _percentiles(ask_top10_contracts),
        "depth_unit": "contracts (linear SWAP order-book size)",
        "reconstruction_policy": (
            "snapshot replaces both sides; updates replace a price level; "
            "zero quantity removes the level; periodic snapshots reset both sides; observed map size is not artificially truncated"
        ),
    }

def fetch_archive_url(family):
    stamp = str(int(datetime.strptime(SAMPLE_DAY, "%Y-%m-%d")
                   .replace(tzinfo=timezone.utc).timestamp() * 1000))
    params = {
        "module": SAMPLE_MODULE,
        "instType": "SWAP",
        "instFamilyList": family,
        "dateAggrType": "daily",
        "begin": stamp,
        "end": stamp,
    }
    url = BASE_URL + API_PATH + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": "okxtester-g0-07-l2-book-reconstruction/1.0"})
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if str(payload.get("code")) != "0":
        raise ValueError("OKX historical-data API returned a nonzero code")
    for block in payload.get("data", []):
        for detail in block.get("details", []):
            if detail.get("instFamily") != family:
                continue
            for item in detail.get("groupDetails", []):
                if SAMPLE_DAY in item.get("filename", "") and item.get("url", "").startswith("https://"):
                    return item["url"], item
    raise ValueError("Expected BTC 5000-level archive is not available")


def inspect_download(url, metadata, expected_inst_id):
    digest = hashlib.sha256()
    downloaded_size = 0
    with tempfile.NamedTemporaryFile(prefix="okx_l2_book_", suffix=".tar.gz") as tmp:
        request = Request(url, headers={"User-Agent": "okxtester-g0-07-l2-book-reconstruction/1.0"})
        with urlopen(request, timeout=180) as response:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                tmp.write(chunk)
                digest.update(chunk)
                downloaded_size += len(chunk)
        tmp.flush()
        with tarfile.open(tmp.name, mode="r:gz") as archive:
            members = [m for m in archive.getmembers() if m.isfile()]
            if len(members) != 1:
                raise ValueError("Expected exactly one regular data member")
            member = members[0]
            handle = archive.extractfile(member)
            if handle is None:
                raise ValueError("Unable to read archive member")
            stats = reconstruct_jsonl_member(handle, expected_inst_id)
    return {
        "filename": metadata["filename"],
        "advertised_size_mb": metadata.get("sizeMB"),
        "downloaded_size_bytes": downloaded_size,
        "downloaded_sha256": digest.hexdigest(),
        "member_name": member.name,
        "member_uncompressed_size_bytes": member.size,
        **stats,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("reports/g0_07_historical_l2_book_reconstruction_v1.json"))
    args = parser.parse_args(argv)

    results = []
    for family in SAMPLE_FAMILIES:
        url, metadata = fetch_archive_url(family)
        result = inspect_download(url, metadata, family + "-SWAP")
        results.append({"inst_family": family, **result})
        print(
            f"{family}: spread_bps={json.dumps(result['spread_bps'], sort_keys=True)} "
            f"top10_bid_contracts_p50={result['top10_bid_depth_contracts']['p50']} "
            f"top10_ask_contracts_p50={result['top10_ask_depth_contracts']['p50']} "
            f"crossed_sampled={result['crossed_book_observations_sampled']}"
        )

    report = {
        "audit_id": "G0-07_OKX_HISTORICAL_L2_BOOK_RECONSTRUCTION_V1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "date_utc": SAMPLE_DAY,
        "module": SAMPLE_MODULE,
        "module_description": "5000-level orderbook",
        "instrument_families": list(SAMPLE_FAMILIES),
        "downloaded_archives_retained": False,
        "results": results,
        "limitations": [
            "One date across five instrument families only; not full-period validation.",
            "Historical archives have no seqId/prevSeqId fields; timestamp ordering cannot prove lossless update continuity.",
            "Visible depth does not prove queue position, hidden liquidity, latency, market impact or guaranteed fills.",
            "Top-10 depth is reported in contracts, not USDT notional; historical effective contract-value metadata is not established.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    json.loads(args.output.read_text(encoding="utf-8"))
    print("G0-07 HISTORICAL L2 BOOK RECONSTRUCTION")
    print(f"Date: {SAMPLE_DAY}; assets reconstructed: {len(results)}")
    print("Archive retained: no")
    print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
