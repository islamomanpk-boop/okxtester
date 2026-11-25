#!/usr/bin/env python3
"""Read-only full-window funding/mark-candle coverage and proxy comparison.

Downloads public OKX monthly funding archives and realizedRate API records into
memory, retrieves 4H historical mark-price candles, and compares their opens
with funding timestamps and available canonical 1m trade candles. A bounded
1m mark-candle sample checks cross-resolution open-price consistency.

No credentials are used. No source CSV, archive, database, or VPS state is
modified. Only a small JSON summary is written to the requested output path.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
START_MS = 1760918400000  # 2025-10-20 00:00:00 UTC
END_MS = 1795104000000    # 2026-11-19 16:00:00 UTC
EXPECTED_ROWS = 1188
EXPECTED_INTERVAL_MS = 28_800_000
ARCHIVE_FIELDS = ["instrument_name", "funding_rate", "funding_time"]
MARK_BASE = "https://www.okx.com/api/v5/market/history-mark-price-candles"
FUNDING_API_BASE = "https://www.okx.com/api/v5/public/funding-rate-history"
ARCHIVE_BASE = "https://static.okx.com/cdn/okex/traderecords/swaprates/monthly"


def month_range(start: str = "2025-10", end: str = "2026-11") -> list[str]:
    sy, sm = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    result = []
    year, month = sy, sm
    while (year, month) <= (ey, em):
        result.append(f"{year:04d}-{month:02d}")
        month += 1
        if month == 13:
            year += 1
            month = 1
    return result


def as_decimal(value: object) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid decimal value: {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"Non-finite decimal value: {value!r}")
    return result


def bps_difference(reference: Decimal, comparison: Decimal) -> float:
    if comparison == 0:
        raise ValueError("Cannot calculate basis points against zero")
    return float((reference / comparison - Decimal(1)) * Decimal(10000))


def percentile(values: Iterable[float], q: float) -> float | None:
    ordered = sorted(values)
    if not ordered:
        return None
    if q <= 0:
        return ordered[0]
    if q >= 1:
        return ordered[-1]
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def distribution(values: Iterable[float]) -> dict:
    vals = list(values)
    if not vals:
        return {"count": 0}
    return {
        "count": len(vals),
        "min": min(vals),
        "p05": percentile(vals, 0.05),
        "median": statistics.median(vals),
        "p95": percentile(vals, 0.95),
        "p99": percentile(vals, 0.99),
        "max": max(vals),
        "mean_absolute": statistics.fmean(abs(x) for x in vals),
    }


def http_json(url: str, *, timeout: int = 45, retries: int = 4, pause: float = 0.12) -> dict:
    last_error = None
    for attempt in range(retries):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "OKX-Price-Action-Research/1.0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if payload.get("code") != "0":
                raise RuntimeError(f"OKX API {payload.get('code')}: {payload.get('msg')}")
            time.sleep(pause)
            return payload
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
            last_error = exc
            if attempt + 1 >= retries:
                break
            time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"Request failed after {retries} attempts: {last_error}") from last_error


def fetch_archive_month(asset: str, month: str) -> dict[int, Decimal]:
    instrument = f"{asset}-USDT-SWAP"
    year, mon = month.split("-")
    filename = f"{instrument}-fundingrates-{month}.zip"
    url = f"{ARCHIVE_BASE}/{year}{mon}/{filename}?v=1001"
    request = urllib.request.Request(url, headers={"User-Agent": "OKX-Price-Action-Research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read()

    if not zipfile.is_zipfile(io.BytesIO(content)):
        raise ValueError(f"{asset} {month}: invalid ZIP archive")
    records: dict[int, Decimal] = {}
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
        if len(names) != 1:
            raise ValueError(f"{asset} {month}: expected one CSV member, found {len(names)}")
        with archive.open(names[0]) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(text)
            if reader.fieldnames != ARCHIVE_FIELDS:
                raise ValueError(f"{asset} {month}: unexpected archive header {reader.fieldnames}")
            for row in reader:
                if row["instrument_name"] != instrument:
                    raise ValueError(f"{asset} {month}: wrong instrument {row['instrument_name']}")
                ts = int(row["funding_time"])
                rate = as_decimal(row["funding_rate"])
                if START_MS <= ts <= END_MS:
                    if ts in records and records[ts] != rate:
                        raise ValueError(f"{asset} {month}: conflicting duplicate timestamp {ts}")
                    records[ts] = rate
    return records


def fetch_funding_api(asset: str) -> dict[int, Decimal]:
    instrument = f"{asset}-USDT-SWAP"
    params = urllib.parse.urlencode({"instId": instrument, "limit": "400"})
    payload = http_json(f"{FUNDING_API_BASE}?{params}", pause=0.15)
    records: dict[int, Decimal] = {}
    for row in payload.get("data", []):
        if row.get("instId") != instrument:
            raise ValueError(f"{asset}: funding API returned another instrument")
        if row.get("realizedRate") in (None, ""):
            raise ValueError(f"{asset}: API row missing realizedRate")
        ts = int(row["fundingTime"])
        rate = as_decimal(row["realizedRate"])
        if START_MS <= ts <= END_MS:
            if ts in records and records[ts] != rate:
                raise ValueError(f"{asset}: conflicting API duplicate {ts}")
            records[ts] = rate
    return records


def load_funding_events(asset: str, months: list[str]) -> tuple[list[int], dict]:
    archive: dict[int, Decimal] = {}
    archive_months_ok = 0
    for month in months:
        month_rows = fetch_archive_month(asset, month)
        archive_months_ok += 1
        for ts, rate in month_rows.items():
            if ts in archive and archive[ts] != rate:
                raise ValueError(f"{asset}: conflicting archive duplicate {ts}")
            archive[ts] = rate
        time.sleep(0.15)

    api = fetch_funding_api(asset)
    overlap = set(archive) & set(api)
    mismatches = [
        ts for ts in overlap
        if abs(archive[ts] - api[ts]) > Decimal("0.000000000001")
    ]
    if mismatches:
        raise ValueError(f"{asset}: {len(mismatches)} archive/API realized-rate conflicts")

    combined = dict(archive)
    combined.update(api)
    events = sorted(combined)
    if len(events) != EXPECTED_ROWS:
        raise ValueError(f"{asset}: expected {EXPECTED_ROWS} funding events, found {len(events)}")
    if events[0] != START_MS or events[-1] != END_MS:
        raise ValueError(f"{asset}: unexpected funding bounds {events[0]}..{events[-1]}")
    intervals = Counter(b - a for a, b in zip(events, events[1:]))
    if intervals != Counter({EXPECTED_INTERVAL_MS: EXPECTED_ROWS - 1}):
        raise ValueError(f"{asset}: unexpected settlement intervals {dict(intervals)}")

    return events, {
        "archive_months_downloaded": archive_months_ok,
        "archive_rows": len(archive),
        "api_rows_in_window": len(api),
        "archive_api_overlap": len(overlap),
        "rate_conflicts": len(mismatches),
        "merged_rows": len(events),
        "first_timestamp_ms": events[0],
        "last_timestamp_ms": events[-1],
        "intervals_minutes": {str(k // 60000): v for k, v in intervals.items()},
    }


def fetch_mark_candles(asset: str, bar: str = "4H") -> tuple[dict[int, dict], dict]:
    instrument = f"{asset}-USDT-SWAP"
    cursor = END_MS + 1
    candles: dict[int, dict] = {}
    pages = 0
    duplicate_rows = 0
    max_pages = 200

    while pages < max_pages:
        params = urllib.parse.urlencode({
            "instId": instrument,
            "bar": bar,
            "limit": "100",
            "after": str(cursor),
        })
        payload = http_json(f"{MARK_BASE}?{params}", pause=0.12)
        rows = payload.get("data", [])
        if not rows:
            break
        pages += 1
        page_timestamps = []
        for row in rows:
            if len(row) < 6:
                raise ValueError(f"{asset}: malformed {bar} mark candle")
            ts = int(row[0])
            page_timestamps.append(ts)
            if START_MS <= ts <= END_MS:
                candle = {
                    "open": as_decimal(row[1]),
                    "high": as_decimal(row[2]),
                    "low": as_decimal(row[3]),
                    "close": as_decimal(row[4]),
                    "confirm": int(row[5]),
                }
                if ts in candles:
                    duplicate_rows += 1
                    if candles[ts] != candle:
                        raise ValueError(f"{asset}: conflicting duplicate {bar} mark candle at {ts}")
                else:
                    candles[ts] = candle

        page_min = min(page_timestamps)
        if page_min >= cursor:
            raise RuntimeError(f"{asset}: {bar} pagination did not move backwards")
        if page_min <= START_MS:
            break
        cursor = page_min
    else:
        raise RuntimeError(f"{asset}: exceeded {max_pages} {bar} mark-candle pages")

    ordered = sorted(candles)
    gaps = []
    interval_ms = 4 * 60 * 60 * 1000 if bar == "4H" else 60 * 60 * 1000
    for prev, nxt in zip(ordered, ordered[1:]):
        if nxt - prev != interval_ms:
            gaps.append({
                "previous_timestamp_ms": prev,
                "next_timestamp_ms": nxt,
                "delta_ms": nxt - prev,
            })

    return candles, {
        "bar": bar,
        "pages": pages,
        "candles_in_window": len(candles),
        "duplicate_rows": duplicate_rows,
        "confirmed_candles": sum(1 for c in candles.values() if c["confirm"] == 1),
        "unconfirmed_candles": sum(1 for c in candles.values() if c["confirm"] != 1),
        "first_timestamp_ms": ordered[0] if ordered else None,
        "last_timestamp_ms": ordered[-1] if ordered else None,
        "gap_intervals": len(gaps),
        "gap_examples": gaps[:5],
    }


def load_trade_rows(trade_dir: Path, asset: str, timestamps: set[int]) -> dict[int, dict]:
    matches = sorted(trade_dir.glob(f"{asset}*_1m.csv"))
    if len(matches) != 1:
        raise FileNotFoundError(f"{asset}: expected one canonical 1m CSV, found {len(matches)}")
    result = {}
    with matches[0].open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"ts", "open", "high", "low", "close", "vol"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"{asset}: unexpected trade CSV header {reader.fieldnames}")
        for row in reader:
            ts = int(row["ts"])
            if ts in timestamps:
                if ts in result:
                    raise ValueError(f"{asset}: duplicate trade candle at {ts}")
                result[ts] = {
                    "open": as_decimal(row["open"]),
                    "close": as_decimal(row["close"]),
                }
    return result


def evenly_spaced(values: list[int], count: int) -> list[int]:
    if not values or count <= 0:
        return []
    if len(values) <= count:
        return values[:]
    if count == 1:
        return [values[len(values) // 2]]
    indices = [round(i * (len(values) - 1) / (count - 1)) for i in range(count)]
    return [values[i] for i in indices]


def fetch_one_mark_1m(asset: str, timestamp: int) -> dict | None:
    instrument = f"{asset}-USDT-SWAP"
    params = urllib.parse.urlencode({
        "instId": instrument,
        "bar": "1m",
        "limit": "100",
        "after": str(timestamp + 60000),
    })
    payload = http_json(f"{MARK_BASE}?{params}", pause=0.12)
    for row in payload.get("data", []):
        if len(row) >= 6 and int(row[0]) == timestamp:
            return {
                "open": as_decimal(row[1]),
                "high": as_decimal(row[2]),
                "low": as_decimal(row[3]),
                "close": as_decimal(row[4]),
                "confirm": int(row[5]),
            }
    return None


def utc_string(ts: int | None) -> str | None:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts / 1000, timezone.utc).isoformat()


def run_audit(trade_dir: Path, samples_per_asset: int = 12) -> dict:
    months = month_range()
    all_timestamps = {}
    asset_results = {}
    pooled = {
        "mark_4h_open_vs_trade_1m_close_bps": [],
        "mark_4h_close_vs_trade_1m_close_bps": [],
        "mark_4h_open_vs_trade_1m_open_bps": [],
        "mark_4h_range_bps": [],
        "sample_1m_open_vs_4h_open_bps": [],
        "sample_1m_close_vs_4h_open_bps": [],
    }

    for asset in ASSETS:
        print(f"[{asset}] Downloading and reconciling public funding history...", flush=True)
        events, funding_meta = load_funding_events(asset, months)
        all_timestamps[asset] = set(events)

        print(f"[{asset}] Fetching full-window 4H mark-price candles...", flush=True)
        mark_4h, mark_meta = fetch_mark_candles(asset, "4H")
        event_mark_rows = {ts: mark_4h[ts] for ts in events if ts in mark_4h}
        missing_mark = [ts for ts in events if ts not in mark_4h]
        incomplete_mark = [ts for ts, candle in event_mark_rows.items() if candle["confirm"] != 1]

        trade_rows = load_trade_rows(trade_dir, asset, set(events))
        missing_trade = [ts for ts in events if ts not in trade_rows]

        differences = {
            "mark_4h_open_vs_trade_1m_close_bps": [],
            "mark_4h_close_vs_trade_1m_close_bps": [],
            "mark_4h_open_vs_trade_1m_open_bps": [],
            "mark_4h_range_bps": [],
        }
        for ts in events:
            mark = event_mark_rows.get(ts)
            trade = trade_rows.get(ts)
            if mark is None or trade is None:
                continue
            differences["mark_4h_open_vs_trade_1m_close_bps"].append(
                bps_difference(mark["open"], trade["close"])
            )
            differences["mark_4h_close_vs_trade_1m_close_bps"].append(
                bps_difference(mark["close"], trade["close"])
            )
            differences["mark_4h_open_vs_trade_1m_open_bps"].append(
                bps_difference(mark["open"], trade["open"])
            )
            differences["mark_4h_range_bps"].append(
                float((mark["high"] - mark["low"]) / mark["open"] * Decimal(10000))
            )
        for key, values in differences.items():
            pooled[key].extend(values)

        sample_timestamps = evenly_spaced(events, samples_per_asset)
        sample_results = []
        sample_diffs_open = []
        sample_diffs_close = []
        sample_open_matches = 0
        sample_missing = 0
        sample_unconfirmed = 0
        for ts in sample_timestamps:
            mark_4h_row = mark_4h.get(ts)
            mark_1m_row = fetch_one_mark_1m(asset, ts)
            trade = trade_rows.get(ts)
            if mark_1m_row is None or mark_4h_row is None:
                sample_missing += 1
                sample_results.append({"timestamp_ms": ts, "status": "MISSING_MARK_CANDLE"})
                continue
            if mark_1m_row["confirm"] != 1:
                sample_unconfirmed += 1
            open_diff = bps_difference(mark_1m_row["open"], mark_4h_row["open"])
            close_diff = bps_difference(mark_1m_row["close"], mark_4h_row["open"])
            sample_diffs_open.append(open_diff)
            sample_diffs_close.append(close_diff)
            if mark_1m_row["open"] == mark_4h_row["open"]:
                sample_open_matches += 1
            sample_results.append({
                "timestamp_ms": ts,
                "timestamp_utc": utc_string(ts),
                "mark_4h_open": str(mark_4h_row["open"]),
                "mark_1m_open": str(mark_1m_row["open"]),
                "mark_1m_close": str(mark_1m_row["close"]),
                "mark_1m_confirm": mark_1m_row["confirm"],
                "mark_1m_open_vs_4h_open_bps": open_diff,
                "mark_1m_close_vs_4h_open_bps": close_diff,
                "trade_1m_close": str(trade["close"]) if trade else None,
            })

        pooled["sample_1m_open_vs_4h_open_bps"].extend(sample_diffs_open)
        pooled["sample_1m_close_vs_4h_open_bps"].extend(sample_diffs_close)

        asset_results[asset] = {
            "funding": funding_meta,
            "mark_4h": {
                **mark_meta,
                "exact_funding_timestamp_matches": len(event_mark_rows),
                "missing_funding_timestamp_candles": len(missing_mark),
                "missing_funding_timestamp_examples": missing_mark[:10],
                "incomplete_funding_timestamp_candles": len(incomplete_mark),
                "incomplete_funding_timestamp_examples": incomplete_mark[:10],
            },
            "trade_1m": {
                "matched_funding_timestamps": len(trade_rows),
                "missing_funding_timestamps": len(missing_trade),
                "missing_funding_timestamp_examples": missing_trade[:10],
            },
            "proxy_difference_distributions_bps": {
                key: distribution(values) for key, values in differences.items()
            },
            "one_minute_cross_resolution_sample": {
                "requested": len(sample_timestamps),
                "exact_mark_rows_found": len(sample_diffs_open),
                "missing_mark_rows": sample_missing,
                "unconfirmed_mark_rows": sample_unconfirmed,
                "mark_1m_open_equals_mark_4h_open": sample_open_matches,
                "mark_1m_open_vs_4h_open_bps": distribution(sample_diffs_open),
                "mark_1m_close_vs_4h_open_bps": distribution(sample_diffs_close),
                "examples": sample_results[:12],
            },
        }
        print(
            f"[{asset}] funding={len(events)} mark4h_exact={len(event_mark_rows)} "
            f"missing_mark={len(missing_mark)} trade_matches={len(trade_rows)} "
            f"1m_sample={len(sample_diffs_open)}/{len(sample_timestamps)}",
            flush=True,
        )

    reference = all_timestamps[ASSETS[0]]
    cross_asset_equal = all(all_timestamps[a] == reference for a in ASSETS[1:])
    result = {
        "status": "COMPLETE",
        "inspection": "public funding archive/API reconstruction plus public mark-candle coverage; canonical trade CSVs read-only; no credentials or source data writes",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "funding_window": {
            "start_ms": START_MS,
            "end_ms": END_MS,
            "start_utc": utc_string(START_MS),
            "end_utc": utc_string(END_MS),
            "expected_events_per_asset": EXPECTED_ROWS,
        },
        "mark_price_proxy_definition": "4H mark-price candle open at the exact public fundingTime; this is a candle-derived proxy, not independently proven exact settlement mark",
        "official_endpoint": "GET /api/v5/market/history-mark-price-candles",
        "cross_asset_funding_timestamp_sets_identical": cross_asset_equal,
        "assets": asset_results,
        "pooled_proxy_difference_distributions_bps": {
            key: distribution(values) for key, values in pooled.items()
        },
        "interpretation_limits": [
            "A matching 4H candle timestamp and open does not prove that the exchange's funding assessment used that exact mark snapshot.",
            "The OKX funding mechanism may assess positions over a short window after the nominal settlement timestamp.",
            "Account-bill px for real production funding events remains the strongest candidate for independent settlement reconciliation, but no production account bills were accessed.",
            "Canonical 1m trade files do not cover every funding event at the start/end boundaries; those events remain in the mark-price coverage audit but are excluded from trade-proxy comparisons.",
        ],
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trade-dir", type=Path, default=Path("data/market_1m"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--samples-per-asset", type=int, default=12)
    args = parser.parse_args()
    if args.samples_per_asset < 1 or args.samples_per_asset > 50:
        raise SystemExit("--samples-per-asset must be between 1 and 50")
    result = run_audit(args.trade_dir, args.samples_per_asset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Summary written to {args.output}", flush=True)


if __name__ == "__main__":
    main()
