"""Read-only availability probe for OKX historical L2 order-book archives.

Queries only GET /api/v5/public/market-data-history. It records archive
metadata (filename, size and download URL) but does not download the archives.
"""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://www.okx.com"
ENDPOINT = "/api/v5/public/market-data-history"
FAMILIES = ("BTC-USDT", "ETH-USDT", "SOL-USDT", "DOGE-USDT", "AVAX-USDT")
SAMPLES = (
    ("2025-10-20", "4"),  # 400-level; project data start
    ("2025-11-01", "4"),  # 400-level
    ("2025-11-01", "5"),  # 5000-level availability start
    ("2026-06-01", "4"),
    ("2026-06-01", "5"),
    ("2026-11-19", "4"),  # latest full/partial project data date
    ("2026-11-19", "5"),
)


def parse_archive_metadata(payload, expected_families):
    if not isinstance(payload, dict) or str(payload.get("code")) != "0":
        raise ValueError("OKX historical-data response code is not 0")
    rows = []
    for block in payload.get("data", []):
        for detail in block.get("details", []):
            family = str(detail.get("instFamily", ""))
            if family not in expected_families:
                continue
            for item in detail.get("groupDetails", []):
                filename = str(item.get("filename", ""))
                url = str(item.get("url", ""))
                size = str(item.get("sizeMB", ""))
                if not filename or not url.startswith("https://") or not size:
                    raise ValueError("Historical archive metadata is incomplete")
                rows.append({
                    "inst_family": family,
                    "filename": filename,
                    "size_mb": size,
                    "url": url,
                    "data_timestamp_ms": str(item.get("dataTs", "")),
                })
    return rows


def query_sample(day, module, timeout=30):
    dt = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    stamp = str(int(dt.timestamp() * 1000))
    params = {
        "module": module,
        "instType": "SWAP",
        "instFamilyList": ",".join(FAMILIES),
        "dateAggrType": "daily",
        "begin": stamp,
        "end": stamp,
    }
    url = BASE_URL + ENDPOINT + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": "okxtester-g0-07-l2-availability/1.0"})
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    files = parse_archive_metadata(payload, set(FAMILIES))
    by_family = {family: [] for family in FAMILIES}
    for item in files:
        by_family[item["inst_family"]].append(item)
    return {
        "date_utc": day,
        "module": module,
        "module_description": "400-level orderbook" if module == "4" else "5000-level orderbook",
        "files": files,
        "missing_families": [family for family, found in by_family.items() if not found],
        "returned_file_count": len(files),
        "total_size_mb": str(sum(float(x["size_mb"]) for x in files)),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("reports/g0_07_historical_orderbook_availability_v1.json"))
    args = parser.parse_args(argv)

    samples, errors = [], []
    for index, (day, module) in enumerate(SAMPLES):
        try:
            samples.append(query_sample(day, module))
        except Exception as exc:
            errors.append({
                "date_utc": day,
                "module": module,
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
        if index < len(SAMPLES) - 1:
            time.sleep(0.45)

    expected = sum(len(FAMILIES) for _ in SAMPLES)
    found = sum(row["returned_file_count"] for row in samples)
    report = {
        "audit_id": "G0-07_OKX_HISTORICAL_L2_ORDERBOOK_AVAILABILITY_V1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": "GET /api/v5/public/market-data-history",
        "authentication": "public; no credentials",
        "downloaded_archives": False,
        "expected_archive_slots": expected,
        "returned_archive_count": found,
        "status": (
            "OKX_HISTORICAL_ORDERBOOK_AVAILABILITY_QUERY_ERROR"
            if errors else (
                "OKX_HISTORICAL_ORDERBOOK_AVAILABILITY_COMPLETE"
                if found == expected else
                "OKX_HISTORICAL_ORDERBOOK_AVAILABILITY_PARTIAL"
            )
        ),
        "families": list(FAMILIES),
        "samples": samples,
        "errors": errors,
        "limitations": [
            "This is a metadata availability probe, not an archive download or data-integrity audit.",
            "OKX states historical backfill is in progress and availability may vary by module, instrument and date.",
            "Archive presence does not establish complete intraday coverage, usable sampling frequency, or executable fills.",
            "Order-book data timestamps are interpreted in UTC according to the OKX API documentation.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("G0-07 HISTORICAL L2 ORDER-BOOK AVAILABILITY")
    print(f"Status: {report['status']}")
    print(f"Archive slots returned: {found}/{expected}")
    for sample in samples:
        print(
            f"{sample['date_utc']} module={sample['module']}: "
            f"{sample['returned_file_count']}/5 files; "
            f"missing={','.join(sample['missing_families']) or 'none'}; "
            f"size={sample['total_size_mb']} MB"
        )
    if errors:
        print("Query errors: " + json.dumps(errors, sort_keys=True))
    print(f"Local report: {args.output}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
