#!/usr/bin/env python3
"""Read-only full-window OKX mark-price coverage at audited funding timestamps.

Funding timestamps are reconstructed from the already-audited, committed
funding coverage manifest (all five schedules have exact recorded coverage and
cadence). The script retrieves public 4H mark-price candles and a bounded 1m
mark-candle sample, then compares them with available canonical 1m trade bars.

No credentials are used. No source CSV, funding file, database, or VPS state is
modified. Only a small JSON summary is written to the requested output path.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
DEFAULT_FUNDING_MANIFEST = Path(
    "reports/sideways_phase3_research_archive_v1/funding_coverage_audit_v1/funding_coverage_manifest.json"
)
MARK_BASE = "https://www.okx.com/api/v5/market/history-mark-price-candles"


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


def build_funding_timestamps(asset_record: dict) -> list[int]:
    if asset_record.get("issues") or asset_record.get("gaps") or asset_record.get("irregular_intervals"):
        raise ValueError("Funding manifest asset record contains issues, gaps, or irregular intervals")
    rows = int(asset_record["rows"])
    first_ts = int(asset_record["first_timestamp_ms"])
    last_ts = int(asset_record["last_timestamp_ms"])
    interval_ms = int(asset_record["expected_interval_ms"])
    if rows < 2 or interval_ms <= 0:
        raise ValueError("Funding manifest row count or interval is invalid")
    timestamps = [first_ts + i * interval_ms for i in range(rows)]
    if timestamps[-1] != last_ts:
        raise ValueError("Funding manifest bounds do not agree with its row count and interval")
    return timestamps


def load_funding_manifest(path: Path) -> tuple[dict[str, list[int]], dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != "PASS":
        raise ValueError(f"Funding coverage manifest is not PASS: {payload.get('status')}")
    events = {}
    meta = {}
    for asset in ASSETS:
        records = [x for x in payload.get("assets", []) if x.get("asset") == asset]
        if len(records) != 1:
            raise ValueError(f"Funding manifest must contain exactly one record for {asset}")
        record = records[0]
        timestamps = build_funding_timestamps(record)
        events[asset] = timestamps
        meta[asset] = {
            "source": "committed funding coverage manifest",
            "instrument_name": record.get("instrument_name"),
            "rows": len(timestamps),
            "first_timestamp_ms": timestamps[0],
            "last_timestamp_ms": timestamps[-1],
            "first_timestamp_utc": datetime.fromtimestamp(timestamps[0] / 1000, timezone.utc).isoformat(),
            "last_timestamp_utc": datetime.fromtimestamp(timestamps[-1] / 1000, timezone.utc).isoformat(),
            "expected_interval_ms": int(record["expected_interval_ms"]),
            "expected_interval_minutes": int(record["expected_interval_ms"]) // 60000,
            "funding_csv_sha256_from_manifest": record.get("sha256"),
            "missing_settlement_count": record.get("missing_settlement_count"),
        }
    reference = set(events[ASSETS[0]])
    if any(set(events[a]) != reference for a in ASSETS[1:]):
        raise ValueError("Funding manifest timestamp sets differ across assets")
    manifest_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    return events, {"path": str(path), "sha256": manifest_hash, "status": payload.get("status"), "assets": meta}


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


def fetch_mark_candles(asset: str, start_ms: int, end_ms: int, bar: str = "4H") -> tuple[dict[int, dict], dict]:
    instrument = f"{asset}-USDT-SWAP"
    cursor = end_ms + 1
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
            if start_ms <= ts <= end_ms:
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
        if page_min <= start_ms:
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


def run_audit(trade_dir: Path, funding_manifest: Path, samples_per_asset: int = 12) -> dict:
    events_by_asset, funding_meta = load_funding_manifest(funding_manifest)
    all_timestamps = {asset: set(events_by_asset[asset]) for asset in ASSETS}
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
        events = events_by_asset[asset]
        start_ms, end_ms = events[0], events[-1]
        print(f"[{asset}] funding events from audited manifest: {len(events)}", flush=True)
        print(f"[{asset}] Fetching full-window 4H mark-price candles...", flush=True)
        mark_4h, mark_meta = fetch_mark_candles(asset, start_ms, end_ms, "4H")
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
                "mark_1m_confirm": mark_1m_row["confirm"],
                "mark_1m_open_vs_4h_open_bps": open_diff,
                "mark_1m_close_vs_4h_open_bps": close_diff,
                "trade_1m_close_available": trade is not None,
            })

        pooled["sample_1m_open_vs_4h_open_bps"].extend(sample_diffs_open)
        pooled["sample_1m_close_vs_4h_open_bps"].extend(sample_diffs_close)

        asset_results[asset] = {
            "funding": funding_meta["assets"][asset],
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
                "examples": sample_results,
            },
        }
        print(
            f"[{asset}] mark4h_exact={len(event_mark_rows)}/{len(events)} "
            f"missing_mark={len(missing_mark)} trade_matches={len(trade_rows)} "
            f"1m_sample={len(sample_diffs_open)}/{len(sample_timestamps)}",
            flush=True,
        )

    reference = all_timestamps[ASSETS[0]]
    cross_asset_equal = all(all_timestamps[a] == reference for a in ASSETS[1:])
    first_ts = events_by_asset[ASSETS[0]][0]
    last_ts = events_by_asset[ASSETS[0]][-1]
    return {
        "status": "COMPLETE",
        "inspection": "public mark-candle coverage against the previously audited funding manifest; canonical trade CSVs read-only; no credentials or source data writes",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "funding_manifest": {
            "path": funding_meta["path"],
            "sha256": funding_meta["sha256"],
            "status": funding_meta["status"],
        },
        "funding_window": {
            "start_ms": first_ts,
            "end_ms": last_ts,
            "start_utc": utc_string(first_ts),
            "end_utc": utc_string(last_ts),
            "events_per_asset": len(events_by_asset[ASSETS[0]]),
            "cross_asset_timestamp_sets_identical": cross_asset_equal,
        },
        "mark_price_proxy_definition": "4H mark-price candle open at the exact fundingTime; this is a candle-derived proxy, not independently proven exact settlement mark",
        "official_endpoint": "GET /api/v5/market/history-mark-price-candles",
        "assets": asset_results,
        "pooled_proxy_difference_distributions_bps": {
            key: distribution(values) for key, values in pooled.items()
        },
        "interpretation_limits": [
            "A matching 4H candle timestamp and open does not prove that the exchange funding assessment used that exact mark snapshot.",
            "The OKX funding mechanism may assess positions over a short window after the nominal settlement timestamp.",
            "Account-bill px for real production funding events remains the strongest candidate for independent settlement reconciliation; no production account bills were accessed.",
            "Canonical 1m trade files do not cover every funding event at the start/end boundaries; those events remain in mark-price coverage but are excluded from trade-proxy comparisons.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trade-dir", type=Path, default=Path("data/market_1m"))
    parser.add_argument("--funding-manifest", type=Path, default=DEFAULT_FUNDING_MANIFEST)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--samples-per-asset", type=int, default=12)
    args = parser.parse_args()
    if args.samples_per_asset < 1 or args.samples_per_asset > 50:
        raise SystemExit("--samples-per-asset must be between 1 and 50")
    result = run_audit(args.trade_dir, args.funding_manifest, args.samples_per_asset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Summary written to {args.output}", flush=True)


if __name__ == "__main__":
    main()
