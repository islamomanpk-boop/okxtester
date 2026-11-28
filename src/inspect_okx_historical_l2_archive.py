"""Inspect one public OKX historical L2 archive and validate its JSONL stream.

Downloads only BTC-USDT-SWAP module 5 for 2025-11-01, streams the complete
archive member for structural/timestamp checks, then deletes the temporary
archive. No credentials are used and no market data is retained.
"""
import argparse
import csv
import hashlib
import json
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
SAMPLE_FAMILY = "BTC-USDT"
SAMPLE_MODULE = "5"


def _validate_levels(levels, side):
    if not isinstance(levels, list):
        raise ValueError(f"{side} must be an array")
    parsed = []
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
        parsed.append((price, size, count))
    return parsed


def inspect_jsonl_member(handle, expected_inst_id):
    rows = 0
    actions = Counter()
    delta_counts = Counter()
    duplicate_timestamps = 0
    non_monotonic_timestamps = 0
    sequence_fields_seen = 0
    sequence_chain_mismatches = 0
    previous_ts = None
    previous_seq = None
    snapshot_bid_levels = None
    snapshot_ask_levels = None
    top_bid = None
    top_ask = None
    first_ts = None
    last_ts = None
    first_keys = None

    for raw_line in handle:
        if not raw_line.strip():
            continue
        try:
            row = json.loads(raw_line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Archive member contains a malformed JSON line") from exc
        if not isinstance(row, dict):
            raise ValueError("Archive JSONL record must be an object")
        if row.get("instId") != expected_inst_id:
            raise ValueError("Archive record instrument ID does not match requested instrument")
        action = row.get("action")
        if action not in ("snapshot", "update"):
            raise ValueError("Archive action must be snapshot or update")
        try:
            ts = int(row["ts"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Archive record timestamp is missing or invalid") from exc
        bids = _validate_levels(row.get("bids"), "bids")
        asks = _validate_levels(row.get("asks"), "asks")

        if rows == 0:
            if action != "snapshot":
                raise ValueError("First archive record must be a snapshot")
            first_ts = ts
            first_keys = sorted(row.keys())
            snapshot_bid_levels = len(bids)
            snapshot_ask_levels = len(asks)
            top_bid = [str(x) for x in bids[0]] if bids else None
            top_ask = [str(x) for x in asks[0]] if asks else None
            if bids and any(bids[i][0] < bids[i + 1][0] for i in range(len(bids) - 1)):
                raise ValueError("Snapshot bids are not sorted descending")
            if asks and any(asks[i][0] > asks[i + 1][0] for i in range(len(asks) - 1)):
                raise ValueError("Snapshot asks are not sorted ascending")
        if previous_ts is not None:
            delta = ts - previous_ts
            delta_counts[str(delta)] += 1
            if delta == 0:
                duplicate_timestamps += 1
            elif delta < 0:
                non_monotonic_timestamps += 1
        previous_ts = ts
        last_ts = ts

        if "seqId" in row and "prevSeqId" in row:
            sequence_fields_seen += 1
            if previous_seq is not None and str(row["prevSeqId"]) != str(previous_seq):
                sequence_chain_mismatches += 1
            previous_seq = row["seqId"]
        actions[action] += 1
        rows += 1

    if rows == 0:
        raise ValueError("Archive member contains no JSONL records")
    return {
        "record_count": rows,
        "first_timestamp_ms": str(first_ts),
        "last_timestamp_ms": str(last_ts),
        "elapsed_seconds": (last_ts - first_ts) / 1000,
        "action_counts": dict(actions),
        "timestamp_delta_counts_ms_top10": dict(delta_counts.most_common(10)),
        "duplicate_timestamps": duplicate_timestamps,
        "non_monotonic_timestamps": non_monotonic_timestamps,
        "sequence_fields_seen": sequence_fields_seen,
        "sequence_chain_mismatches": sequence_chain_mismatches,
        "first_record_keys": first_keys,
        "snapshot_bid_level_count": snapshot_bid_levels,
        "snapshot_ask_level_count": snapshot_ask_levels,
        "snapshot_best_bid": top_bid,
        "snapshot_best_ask": top_ask,
    }


def fetch_archive_url():
    stamp = str(int(datetime.strptime(SAMPLE_DAY, "%Y-%m-%d")
                   .replace(tzinfo=timezone.utc).timestamp() * 1000))
    params = {
        "module": SAMPLE_MODULE,
        "instType": "SWAP",
        "instFamilyList": SAMPLE_FAMILY,
        "dateAggrType": "daily",
        "begin": stamp,
        "end": stamp,
    }
    url = BASE_URL + API_PATH + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": "okxtester-g0-07-l2-archive-inspector/1.0"})
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if str(payload.get("code")) != "0":
        raise ValueError("OKX historical-data API returned a nonzero code")
    for block in payload.get("data", []):
        for detail in block.get("details", []):
            if detail.get("instFamily") != SAMPLE_FAMILY:
                continue
            for item in detail.get("groupDetails", []):
                if SAMPLE_DAY in item.get("filename", "") and item.get("url", "").startswith("https://"):
                    return item["url"], item
    raise ValueError("Expected BTC 5000-level archive is not available")


def inspect_download(url, metadata):
    digest = hashlib.sha256()
    downloaded_size = 0
    with tempfile.NamedTemporaryFile(prefix="okx_l2_probe_", suffix=".tar.gz") as tmp:
        request = Request(url, headers={"User-Agent": "okxtester-g0-07-l2-archive-inspector/1.0"})
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
                raise ValueError("Expected exactly one regular data member in archive")
            member = members[0]
            handle = archive.extractfile(member)
            if handle is None:
                raise ValueError("Unable to read archive member")
            stream_stats = inspect_jsonl_member(handle, "BTC-USDT-SWAP")
    return {
        "filename": metadata["filename"],
        "advertised_size_mb": metadata.get("sizeMB"),
        "downloaded_size_bytes": downloaded_size,
        "downloaded_sha256": digest.hexdigest(),
        "archive_format": "tar.gz",
        "member_count": 1,
        "first_member_name": member.name,
        "first_member_uncompressed_size_bytes": member.size,
        **stream_stats,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("reports/g0_07_historical_l2_archive_format_v1.json"))
    args = parser.parse_args(argv)
    url, metadata = fetch_archive_url()
    result = inspect_download(url, metadata)
    report = {
        "audit_id": "G0-07_OKX_HISTORICAL_L2_ARCHIVE_FORMAT_V1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "instrument_family": SAMPLE_FAMILY,
        "date_utc": SAMPLE_DAY,
        "module": SAMPLE_MODULE,
        "module_description": "5000-level orderbook",
        "downloaded_archive_retained": False,
        "result": result,
        "limitations": [
            "One BTC instrument/day archive only; not evidence of full-period or all-asset integrity.",
            "Stream structure and timestamps are checked, but no full order-book reconstruction is attempted.",
            "L2 depth does not establish queue priority, hidden liquidity, latency or guaranteed executable fills.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("G0-07 HISTORICAL L2 ARCHIVE STREAM VALIDATION")
    print(f"Archive: {result['filename']}")
    print(f"Downloaded: {result['downloaded_size_bytes']} bytes")
    print(f"SHA-256: {result['downloaded_sha256']}")
    print(f"Records: {result['record_count']}")
    print(f"Actions: {json.dumps(result['action_counts'], sort_keys=True)}")
    print(f"Timestamp deltas ms: {json.dumps(result['timestamp_delta_counts_ms_top10'], sort_keys=True)}")
    print(f"Snapshot depth bids/asks: {result['snapshot_bid_level_count']}/{result['snapshot_ask_level_count']}")
    print(f"Sequence fields: {result['sequence_fields_seen']}; chain mismatches: {result['sequence_chain_mismatches']}")
    print("Archive retained: no")
    print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
