"""Inspect a targeted OKX module-4 historical L2 archive (BTC, 2025-10-20).

The archive is streamed on a GitHub-hosted runner, structurally validated,
summarized, and deleted. No raw market data is committed or retained.
"""
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
SAMPLE_DAY = "2025-10-20"
SAMPLE_FAMILY = "BTC-USDT"
SAMPLE_MODULE = "4"
EXPECTED_INST_ID = "BTC-USDT-SWAP"


def validate_levels(levels, side):
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


def inspect_jsonl_member(handle, expected_inst_id=EXPECTED_INST_ID):
    rows = 0
    actions = Counter()
    timestamp_deltas = Counter()
    snapshot_bid_counts = []
    snapshot_ask_counts = []
    previous_ts = None
    first_ts = last_ts = None
    duplicate_timestamps = 0
    non_monotonic_timestamps = 0
    seq_fields_seen = 0
    first_record_keys = None
    first_snapshot_top = None

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

        bids = validate_levels(row.get("bids"), "bids")
        asks = validate_levels(row.get("asks"), "asks")
        if rows == 0:
            if action != "snapshot":
                raise ValueError("First archive record must be a snapshot")
            first_ts = ts
            first_record_keys = sorted(row.keys())
            if any(bids[i][0] < bids[i + 1][0] for i in range(len(bids) - 1)):
                raise ValueError("Snapshot bids are not sorted descending")
            if any(asks[i][0] > asks[i + 1][0] for i in range(len(asks) - 1)):
                raise ValueError("Snapshot asks are not sorted ascending")
            first_snapshot_top = {
                "best_bid": str(bids[0][0]) if bids else None,
                "best_ask": str(asks[0][0]) if asks else None,
            }
        if action == "snapshot":
            snapshot_bid_counts.append(len(bids))
            snapshot_ask_counts.append(len(asks))
        if previous_ts is not None:
            delta = ts - previous_ts
            timestamp_deltas[str(delta)] += 1
            duplicate_timestamps += int(delta == 0)
            non_monotonic_timestamps += int(delta < 0)
        previous_ts = ts
        last_ts = ts
        seq_fields_seen += int("seqId" in row or "prevSeqId" in row)
        actions[action] += 1
        rows += 1

    if rows == 0 or not snapshot_bid_counts:
        raise ValueError("Archive contains no usable snapshot/update stream")
    return {
        "record_count": rows,
        "action_counts": dict(actions),
        "snapshot_bid_level_count_min": min(snapshot_bid_counts),
        "snapshot_bid_level_count_max": max(snapshot_bid_counts),
        "snapshot_ask_level_count_min": min(snapshot_ask_counts),
        "snapshot_ask_level_count_max": max(snapshot_ask_counts),
        "first_record_keys": first_record_keys,
        "first_snapshot_top": first_snapshot_top,
        "first_timestamp_ms": str(first_ts),
        "last_timestamp_ms": str(last_ts),
        "elapsed_seconds": (last_ts - first_ts) / 1000,
        "timestamp_delta_counts_ms": dict(sorted(timestamp_deltas.items(), key=lambda item: int(item[0]))),
        "timestamp_delta_exactly_1000ms_count": timestamp_deltas.get("1000", 0),
        "timestamp_delta_non_1000ms_count": sum(v for k, v in timestamp_deltas.items() if k != "1000"),
        "duplicate_timestamps": duplicate_timestamps,
        "non_monotonic_timestamps": non_monotonic_timestamps,
        "sequence_fields_seen": seq_fields_seen,
        "snapshot_count": len(snapshot_bid_counts),
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
    request = Request(url, headers={"User-Agent": "okxtester-g0-07-module4-inspector/1.0"})
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
    raise ValueError("Expected BTC module-4 archive is not available")


def inspect_download(url, metadata):
    digest = hashlib.sha256()
    downloaded_bytes = 0
    with tempfile.NamedTemporaryFile(prefix="okx_module4_", suffix=".tar.gz") as tmp:
        request = Request(url, headers={"User-Agent": "okxtester-g0-07-module4-inspector/1.0"})
        with urlopen(request, timeout=300) as response:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                tmp.write(chunk)
                digest.update(chunk)
                downloaded_bytes += len(chunk)
        tmp.flush()
        with tarfile.open(tmp.name, mode="r:gz") as archive:
            members = [member for member in archive.getmembers() if member.isfile()]
            if len(members) != 1:
                raise ValueError("Expected exactly one regular data member")
            member = members[0]
            handle = archive.extractfile(member)
            if handle is None:
                raise ValueError("Unable to stream archive member")
            stats = inspect_jsonl_member(handle)
    return {
        "filename": metadata["filename"],
        "advertised_size_mb": metadata.get("sizeMB"),
        "downloaded_size_bytes": downloaded_bytes,
        "downloaded_sha256": digest.hexdigest(),
        "archive_format": "tar.gz",
        "member_name": member.name,
        "member_uncompressed_size_bytes": member.size,
        **stats,
    }


def main():
    url, metadata = fetch_archive_url()
    result = inspect_download(url, metadata)
    report = {
        "audit_id": "G0-07_OKX_MODULE4_HISTORICAL_L2_ARCHIVE_INSPECTION_V1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "date_utc": SAMPLE_DAY,
        "module": SAMPLE_MODULE,
        "module_description": "400-level orderbook",
        "instrument_family": SAMPLE_FAMILY,
        "downloaded_archive_retained": False,
        "result": result,
        "limitations": [
            "One BTC instrument/day sample only; not full-period or cross-asset validation.",
            "No seqId/prevSeqId means timestamp ordering cannot prove lossless update continuity.",
            "This is archive-format and stream validation, not a fill simulator or calibrated slippage study.",
        ],
    }
    output = Path("reports/g0_07_module4_historical_l2_archive_inspection_v1.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    json.loads(output.read_text(encoding="utf-8"))
    print("G0-07 MODULE-4 HISTORICAL L2 ARCHIVE INSPECTION")
    print(f"Archive: {result['filename']}")
    print(f"Downloaded bytes: {result['downloaded_size_bytes']}")
    print(f"Records: {result['record_count']}; actions: {json.dumps(result['action_counts'], sort_keys=True)}")
    print(f"Snapshot depth bid: {result['snapshot_bid_level_count_min']}-{result['snapshot_bid_level_count_max']}; ask: {result['snapshot_ask_level_count_min']}-{result['snapshot_ask_level_count_max']}")
    print(f"Timestamp deltas exactly 1000ms: {result['timestamp_delta_exactly_1000ms_count']}; non-1000ms: {result['timestamp_delta_non_1000ms_count']}")
    print(f"Sequence fields seen: {result['sequence_fields_seen']}; archive retained: no")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
