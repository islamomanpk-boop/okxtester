#!/usr/bin/env python3
"""Download and validate OKX historical USDT perpetual funding archives."""

import argparse
import csv
import io
import time
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
START_MONTH = "2025-10"
END_MONTH = "2026-11"

BASE = Path.home() / "okx_scalping_data" / "funding_rates"
RAW = BASE / "raw_archive"
PROCESSED = BASE / "processed"
REPORT = Path("reports/funding_data_audit.md")

FIELDS = ["instrument_name", "funding_rate", "funding_time"]


def month_range(start, end):
    sy, sm = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    result = []
    y, m = sy, sm
    while (y, m) <= (ey, em):
        result.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y += 1
            m = 1
    return result


def parse_archive(content, instrument):
    if not zipfile.is_zipfile(io.BytesIO(content)):
        raise ValueError("Downloaded content is not a valid ZIP")

    records = []
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        names = [n for n in archive.namelist() if not n.endswith("/")]
        if len(names) != 1:
            raise ValueError(f"Expected one CSV file, found {len(names)}")

        with archive.open(names[0]) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(text)

            if reader.fieldnames != FIELDS:
                raise ValueError(f"Unexpected CSV columns: {reader.fieldnames}")

            for line_no, row in enumerate(reader, start=2):
                if row["instrument_name"] != instrument:
                    raise ValueError(
                        f"Wrong instrument on CSV line {line_no}: "
                        f"{row['instrument_name']}"
                    )
                try:
                    rate = float(row["funding_rate"])
                    ts = int(row["funding_time"])
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid rate/timestamp on line {line_no}")

                if not (-1 < rate < 1):
                    raise ValueError(f"Implausible funding rate on line {line_no}")
                if ts <= 0:
                    raise ValueError(f"Invalid funding timestamp on line {line_no}")

                records.append({
                    "instrument_name": instrument,
                    "funding_rate": format(rate, ".16g"),
                    "funding_time": str(ts),
                })

    if not records:
        raise ValueError("Archive contains no funding records")
    return records


def download_one(asset, month):
    instrument = f"{asset}-USDT-SWAP"
    year, mon = month.split("-")
    filename = f"{instrument}-fundingrates-{month}.zip"
    url = (
        "https://static.okx.com/cdn/okex/traderecords/swaprates/"
        f"monthly/{year}{mon}/{filename}?v=1001"
    )

    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / filename

    if path.exists():
        content = path.read_bytes()
        parse_archive(content, instrument)
        return path, parse_archive(content, instrument), "cached"

    request = urllib.request.Request(
        url, headers={"User-Agent": "OKX-Price-Action-Research/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read()

    records = parse_archive(content, instrument)
    temporary = path.with_suffix(".zip.tmp")
    temporary.write_bytes(content)
    temporary.replace(path)
    return path, records, "downloaded"


def write_asset_csv(asset, records, start_ms, end_ms):
    instrument = f"{asset}-USDT-SWAP"
    unique = {}

    for row in records:
        ts = int(row["funding_time"])
        if not start_ms <= ts <= end_ms:
            continue
        if ts in unique and unique[ts]["funding_rate"] != row["funding_rate"]:
            raise ValueError(f"{instrument}: conflicting duplicate at {ts}")
        unique[ts] = row

    ordered = [unique[k] for k in sorted(unique)]
    if not ordered:
        raise ValueError(f"{instrument}: no records in requested date range")

    PROCESSED.mkdir(parents=True, exist_ok=True)
    path = PROCESSED / f"{asset}_USDT_SWAP_funding_rates.csv"

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(ordered)

    return path, ordered


def utc_string(ts):
    return datetime.fromtimestamp(ts / 1000, timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2025-10-20T00:00:00Z")
    parser.add_argument("--end", default="2026-11-19T23:59:59Z")
    args = parser.parse_args()

    start_dt = datetime.fromisoformat(args.start.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(args.end.replace("Z", "+00:00"))
    if start_dt.tzinfo is None or end_dt.tzinfo is None or start_dt >= end_dt:
        raise SystemExit("Start/end must be valid timezone-aware ISO timestamps.")

    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)
    months = month_range(START_MONTH, END_MONTH)

    print("===== OKX FUNDING ARCHIVE DOWNLOAD =====")
    print("Assets:", ", ".join(ASSETS))
    print("Archive months:", months[0], "through", months[-1])
    print("Requested UTC:", start_dt.isoformat(), "to", end_dt.isoformat())
    print("Archives expected:", len(ASSETS) * len(months))

    report = [
        "# OKX Historical Funding Data Audit",
        "",
        f"- Requested range: {start_dt.isoformat()} to {end_dt.isoformat()}",
        f"- Archive months: {months[0]} through {months[-1]}",
        "- Instruments: " + ", ".join(f"{a}-USDT-SWAP" for a in ASSETS),
        "- Source: OKX public historical funding-rate monthly ZIP archives",
        "",
        "## Download results",
        "",
        "| Asset | Archive files | Rows in range | First UTC | Last UTC |",
        "|---|---:|---:|---|---|",
    ]

    failures = []
    total_rows = 0

    for asset in ASSETS:
        all_records = []
        downloaded = 0
        print(f"\n===== {asset} =====")

        for month in months:
            try:
                path, records, status = download_one(asset, month)
                downloaded += 1
                all_records.extend(records)
                print(f"{month}: {status}, {len(records)} rows, {path.stat().st_size} bytes")
            except Exception as exc:
                message = f"{asset} {month}: {type(exc).__name__}: {exc}"
                failures.append(message)
                print("ERROR:", message)
            time.sleep(0.15)

        try:
            output, ordered = write_asset_csv(asset, all_records, start_ms, end_ms)
            first = utc_string(int(ordered[0]["funding_time"]))
            last = utc_string(int(ordered[-1]["funding_time"]))
            report.append(
                f"| {asset} | {downloaded}/{len(months)} | {len(ordered)} "
                f"| {first} | {last} |"
            )
            total_rows += len(ordered)
            print(f"{asset} consolidated rows: {len(ordered)}")
            print("Saved:", output)
        except Exception as exc:
            failures.append(f"{asset} consolidation: {type(exc).__name__}: {exc}")

    report.extend([
        "",
        "## Summary",
        "",
        f"- Total consolidated records: {total_rows}",
        f"- Expected archive files: {len(ASSETS) * len(months)}",
        f"- Failed downloads or validations: {len(failures)}",
        "",
        "## Funding interval note",
        "",
        "Funding settlement intervals can change. This audit does not assume "
        "a fixed eight-hour interval. Missing or unusual intervals require "
        "separate investigation before backtesting.",
        "",
        "## Errors",
        "",
    ])
    report.extend([f"- {x}" for x in failures] or ["- None"])

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n===== DOWNLOAD SUMMARY =====")
    print("Total consolidated records:", total_rows)
    print("Failures:", len(failures))
    print("Report:", REPORT)

    if failures or total_rows == 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
