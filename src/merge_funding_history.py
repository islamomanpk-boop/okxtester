"""Merge OKX monthly funding archives with official realized-rate API history."""

import csv
import json
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
BASE = Path.home() / "okx_scalping_data/funding_rates"
PROCESSED = BASE / "processed"
START_MS = 1760918400000       # 2025-10-20 00:00 UTC
END_MS = 1795132799000         # 2026-11-19 23:59:59 UTC
MIN_API_OVERLAP = 20
RATE_TOLERANCE = Decimal("0.000000000001")


def read_archive(path, instrument):
    records = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"instrument_name", "funding_rate", "funding_time"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{path}: invalid columns")

        for row in reader:
            if row["instrument_name"] != instrument:
                raise ValueError(f"{path}: wrong instrument")
            ts = int(row["funding_time"])
            rate = Decimal(row["funding_rate"])
            if ts <= 0 or not rate.is_finite() or abs(rate) > 1:
                raise ValueError(f"{path}: invalid funding record")
            if START_MS <= ts <= END_MS:
                if ts in records and records[ts] != rate:
                    raise ValueError(f"{path}: conflicting duplicate {ts}")
                records[ts] = rate
    return records


def parse_api_records(payload, instrument):
    if payload.get("code") != "0":
        raise ValueError(f"OKX API error: {payload.get('code')} {payload.get('msg')}")

    records = {}
    for row in payload.get("data", []):
        if row.get("instId") != instrument:
            raise ValueError(f"API returned wrong instrument for {instrument}")
        if "realizedRate" not in row or row["realizedRate"] in (None, ""):
            raise ValueError(f"{instrument}: API record missing realizedRate")

        ts = int(row["fundingTime"])
        rate = Decimal(row["realizedRate"])
        if ts <= 0 or not rate.is_finite() or abs(rate) > 1:
            raise ValueError(f"{instrument}: invalid API record")

        if START_MS <= ts <= END_MS:
            if ts in records and records[ts] != rate:
                raise ValueError(f"{instrument}: conflicting API duplicate {ts}")
            records[ts] = rate

    return records


def fetch_api_records(instrument):
    params = urllib.parse.urlencode({"instId": instrument, "limit": "400"})
    url = "https://www.okx.com/api/v5/public/funding-rate-history?" + params
    request = urllib.request.Request(
        url, headers={"User-Agent": "OKX-Price-Action-Research/1.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return parse_api_records(payload, instrument)


def merge_records(archive, api, instrument):
    overlap = set(archive) & set(api)
    if len(overlap) < MIN_API_OVERLAP:
        raise ValueError(
            f"{instrument}: only {len(overlap)} overlapping timestamps; "
            f"need at least {MIN_API_OVERLAP} to validate sources"
        )

    mismatches = []
    for ts in sorted(overlap):
        if abs(archive[ts] - api[ts]) > RATE_TOLERANCE:
            mismatches.append((ts, archive[ts], api[ts]))

    if mismatches:
        sample = mismatches[0]
        raise ValueError(
            f"{instrument}: {len(mismatches)} archive/API rate mismatches; "
            f"first timestamp={sample[0]}, archive={sample[1]}, API={sample[2]}"
        )

    combined = dict(archive)
    combined.update(api)

    if not combined:
        raise ValueError(f"{instrument}: no records after merge")

    latest = max(combined)
    latest_utc = datetime.fromtimestamp(latest / 1000, timezone.utc)
    if latest_utc < datetime(2026, 11, 19, 0, 0, tzinfo=timezone.utc):
        raise ValueError(f"{instrument}: API does not cover through Nov 19")

    return combined, len(overlap)


def write_csv(path, instrument, records):
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["instrument_name", "funding_rate", "funding_time"])
        for ts in sorted(records):
            writer.writerow([instrument, str(records[ts]), ts])
    temp.replace(path)


def main():
    results = []
    merged_by_asset = {}

    print("===== OKX FUNDING HISTORY MERGE =====")
    print("Range: 2025-10-20 through 2026-11-19 UTC")
    print("API field: realizedRate (actual settled funding rate)")
    print()

    # Validate and fetch all assets before replacing any processed CSV.
    for asset in ASSETS:
        instrument = f"{asset}-USDT-SWAP"
        path = PROCESSED / f"{asset}_USDT_SWAP_funding_rates.csv"

        if not path.is_file():
            raise FileNotFoundError(path)

        archive = read_archive(path, instrument)
        api = fetch_api_records(instrument)
        combined, overlap_count = merge_records(archive, api, instrument)

        times = sorted(combined)
        intervals = Counter(
            (b - a) // 60000 for a, b in zip(times, times[1:])
        )
        first = datetime.fromtimestamp(times[0] / 1000, timezone.utc)
        last = datetime.fromtimestamp(times[-1] / 1000, timezone.utc)

        merged_by_asset[asset] = combined
        results.append({
            "asset": asset,
            "archive": len(archive),
            "api": len(api),
            "overlap": overlap_count,
            "rows": len(combined),
            "first": first.isoformat(),
            "last": last.isoformat(),
            "intervals": intervals,
        })

        print(
            f"{asset}: archive={len(archive)}, API={len(api)}, "
            f"overlap={overlap_count}, merged={len(combined)}"
        )
        print(f"  First: {first} | Last: {last}")
        print(f"  Observed intervals (minutes): {dict(intervals)}")

    # Only write after all five assets pass validation.
    for asset, records in merged_by_asset.items():
        instrument = f"{asset}-USDT-SWAP"
        path = PROCESSED / f"{asset}_USDT_SWAP_funding_rates.csv"
        write_csv(path, instrument, records)

    report = [
        "# OKX Historical Funding Data — Reconciliation Audit",
        "",
        "- Requested range: 2025-10-20 00:00 UTC to 2026-11-19 23:59:59 UTC",
        "- Instruments: BTC, ETH, SOL, DOGE, AVAX USDT perpetual swaps",
        "- Archive source: OKX monthly historical funding ZIP files",
        "- API source: OKX public funding-rate-history endpoint",
        "- API field used: `realizedRate` (actual settled rate)",
        "- Overlapping archive/API timestamps were compared before merging.",
        f"- Rate comparison tolerance: {RATE_TOLERANCE}",
        "",
        "## Results",
        "",
        "| Asset | Archive rows | API rows in range | Overlap checked | Merged rows | First UTC | Last UTC |",
        "|---|---:|---:|---:|---:|---|---|",
    ]

    for r in results:
        report.append(
            f"| {r['asset']} | {r['archive']} | {r['api']} | "
            f"{r['overlap']} | {r['rows']} | {r['first']} | {r['last']} |"
        )

    report.extend([
        "",
        "## Observed settlement intervals",
        "",
        "Intervals are measured from the actual timestamps. No fixed eight-hour "
        "schedule is assumed.",
        "",
    ])

    for r in results:
        report.append(f"### {r['asset']}")
        report.append("")
        report.append(f"`{dict(r['intervals'])}` minutes")
        report.append("")

    report.extend([
        "## Validation",
        "",
        "- All five assets passed archive schema and instrument checks.",
        "- All API records used for merging contained `realizedRate`.",
        "- Archive/API overlap met the minimum comparison count.",
        "- No overlapping funding-rate conflicts were found.",
        "- Duplicate timestamp conflicts were rejected.",
        "- Output timestamps are sorted and unique.",
        "- Processed CSV files were replaced only after all five assets passed.",
        "",
        "## Storage",
        "",
        "Processed CSVs and raw ZIP archives remain outside normal Git history. "
        "Code, tests, documentation and this audit report belong in Git.",
        "",
    ])

    report_path = Path("reports/funding_data_audit.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report), encoding="utf-8")

    print("\n===== MERGE COMPLETE =====")
    print("Assets passed:", len(results))
    print("Report:", report_path)


if __name__ == "__main__":
    main()
