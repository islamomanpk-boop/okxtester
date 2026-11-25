#!/usr/bin/env python3
"""Descriptive Phase 3 breakout / failed-breakout lifecycle V1.1."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
PRIMARY_ZONE = 10.0
RETEST_BAND_PCT = 0.10
RETEST_BAND_FRACTION = RETEST_BAND_PCT / 100.0
MINUTE_MS = 60_000
MINUTE_NS = 60_000_000_000
QUARTER_HOUR_MS = 900_000
HORIZONS = (("15M", 15), ("1H", 60), ("4H", 240), ("12H", 720))
EXPECTED_SOURCE_ROWS = {"BTC": 569125, "ETH": 569125, "SOL": 569126, "DOGE": 569126, "AVAX": 569127}
EXPECTED_CLASSIFICATION_ROWS = 4776
EXPECTED_LINK_ROWS = 4534
EXPECTED_PRIMARY_EVENTS = 1592
EXPECTED_PRIMARY_LINK_ROWS = 1537
EXPECTED_PRIMARY_ZERO_LINK_EVENTS = 160
EXPECTED_COMMON_MINUTES = 569125

EXPECTED_BLOBS = {
    "research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py": "95d2975947c449f3813d80ee7b12008db14f071f",
    "reports/breakout_prior_test_count_v1/breakout_prior_test_classifications_v1.csv": "b432bf5d399f5340f3ed985c45aa64791779ab5f",
    "reports/breakout_prior_test_count_v1/breakout_prior_test_links_v1.csv": "7e8119e0634f2fa73207f0a030e6140d2612a32e",
    "reports/breakout_prior_test_count_v1/run_metadata.json": "6a26e087108381ad10507971468bef4b785291ec",
    "reports/breakout_prior_test_count_v1/reconstruction_audit_v1.csv": "dddf558db7e5eaee28b579b2f585863991dd4707",
    "reports/breakout_forward_outcome_v1/run_metadata.json": "456ee605a2b2ba7c01b1e390a2880619e01c0660",
    "reports/breakout_forward_outcome_v1/breakout_forward_outcomes_v1.csv": "458fb8d65bb108b78c04c201ed6115c56ff8096e",
    "reports/breakout_forward_outcome_v1/original_event_reproduction_v1.csv": "7e697d7f861d54a9e14da1efb8bcf6c53b69b2e6",
    "reports/breakout_forward_outcome_v1/original_quantile_reproduction_v1.csv": "dea9d1cc7548d74da71f0de265bb10ef26089d03",
    "data/market_1m/BTC_USDT_USDT_1m.csv": "639f7b8a6d54747dd3eb3370dc133d53f6382bfd",
    "data/market_1m/ETH_USDT_USDT_1m.csv": "3017d870fe1cb764e1acb8fdec04138592749d69",
    "data/market_1m/SOL_USDT_USDT_1m.csv": "a850c2dc4a2c14b34b59737ccfbb2e4c59d97bf3",
    "data/market_1m/DOGE_USDT_USDT_1m.csv": "2162df0f277bef6c04bd191b459a35d735c68f2d",
    "data/market_1m/AVAX_USDT_USDT_1m.csv": "6e0cb0c55aa2aafb4118d62522826bcf1a2aeb62",
}
EXPECTED_MARKET_SHA256 = {
    "BTC": "3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633",
    "ETH": "8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2",
    "SOL": "8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3",
    "DOGE": "eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4",
    "AVAX": "44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5",
}


def git_blob_sha1(path: Path) -> str:
    size = path.stat().st_size
    digest = hashlib.sha1(f"blob {size}\0".encode("ascii"))
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_blob(root: Path, relative: str, expected: str) -> str:
    path = root / relative
    if not path.is_file():
        raise FileNotFoundError(f"Required source missing: {relative}")
    actual = git_blob_sha1(path)
    if actual != expected:
        raise ValueError(f"Git blob mismatch for {relative}: {actual} != {expected}")
    return actual


def timestamp_ms(value) -> int:
    stamp = pd.Timestamp(value)
    if stamp.tzinfo is None:
        stamp = stamp.tz_localize("UTC")
    else:
        stamp = stamp.tz_convert("UTC")
    return int(stamp.value // 1_000_000)


def ms_iso(value):
    if value is None or pd.isna(value) or value == "":
        return ""
    return pd.to_datetime(int(value), unit="ms", utc=True).strftime("%Y-%m-%d %H:%M:%S+00:00")


def event_key(row):
    return (
        str(row["asset"]),
        str(row["definition"]),
        str(row["direction"]),
        timestamp_ms(row["signal_time"]),
        float(row["zone_pct_of_channel"]),
    )


def event_id_from_key(key):
    asset, definition, direction, signal_ms, zone = key
    return f"{asset}|{definition.lower()}|{direction.lower()}|{signal_ms}|zone{zone:g}"


def load_market(root: Path, asset: str):
    relative = f"data/market_1m/{asset}_USDT_USDT_1m.csv"
    path = root / relative
    blob = git_blob_sha1(path)
    expected_blob = EXPECTED_BLOBS[relative]
    if blob != expected_blob:
        raise ValueError(f"{asset}: market Git blob mismatch")
    sha256 = file_sha256(path)
    if sha256 != EXPECTED_MARKET_SHA256[asset]:
        raise ValueError(f"{asset}: market SHA-256 differs from accepted breakout source")

    frame = pd.read_csv(path, usecols=["ts", "open", "high", "low", "close"])
    if len(frame) != EXPECTED_SOURCE_ROWS[asset]:
        raise ValueError(f"{asset}: unexpected 1M row count {len(frame)}")
    frame["ts"] = pd.to_datetime(frame["ts"], unit="ms", utc=True)
    frame = frame.set_index("ts").sort_index()
    if frame.index.has_duplicates or not frame.index.is_monotonic_increasing:
        raise ValueError(f"{asset}: duplicate or unordered 1M timestamps")
    if len(frame) > 1 and not np.all(np.diff(frame.index.asi8) == MINUTE_NS):
        raise ValueError(f"{asset}: 1M source has missing or irregular intervals")
    values = frame[["open", "high", "low", "close"]].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values <= 0).any():
        raise ValueError(f"{asset}: invalid or non-positive OHLC")
    o, h, low, close = (frame[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
    if ((low > np.minimum(o, close)) | (h < np.maximum(o, close)) | (low > h)).any():
        raise ValueError(f"{asset}: inconsistent OHLC")
    return frame, {"git_blob_sha1": blob, "sha256": sha256, "rows": len(frame)}


def build_complete_15m(frame: pd.DataFrame) -> pd.DataFrame:
    grouped = frame.resample("15min", label="right", closed="left")
    bars = grouped.agg({
        "open": "first", "high": "max", "low": "min", "close": "last",
    })
    counts = grouped["close"].count()
    bars = bars.loc[counts == 15].dropna()
    return bars


def find_outside_retest(direction, boundary, previous_close, bars):
    band_high = boundary * (1 + RETEST_BAND_FRACTION)
    band_low = boundary * (1 - RETEST_BAND_FRACTION)
    for offset, bar in enumerate(bars):
        if direction == "UPPER":
            approached = previous_close > band_high and bar["low"] <= band_high
            crossed = bar["low"] <= boundary
            depth = max(0.0, (boundary - bar["low"]) / boundary * 100.0)
        else:
            approached = previous_close < band_low and bar["high"] >= band_low
            crossed = bar["high"] >= boundary
            depth = max(0.0, (bar["high"] - boundary) / boundary * 100.0)
        if approached:
            return {
                "offset": offset,
                "bar_open_ts_ms": bar["ts_ms"],
                "elapsed_minutes": offset + 1,
                "depth_pct_of_boundary": depth,
                "boundary_crossed": bool(crossed),
                "bar_open": bar["open"], "bar_high": bar["high"],
                "bar_low": bar["low"], "bar_close": bar["close"],
            }
        previous_close = bar["close"]
    return None


def first_1m_return_inside(direction, boundary, bars):
    for offset, bar in enumerate(bars):
        returned = bar["close"] <= boundary if direction == "UPPER" else bar["close"] >= boundary
        if returned:
            return {"offset": offset, "bar_open_ts_ms": bar["ts_ms"],
                    "available_ts_ms": bar["ts_ms"] + MINUTE_MS, "close": bar["close"]}
    return None


def first_15m_failure_and_reclaim(direction, boundary, bars15):
    failure = None
    reclaim = None
    for close_ts, close in bars15:
        inside = close <= boundary if direction == "UPPER" else close >= boundary
        outside = close > boundary if direction == "UPPER" else close < boundary
        if failure is None and inside:
            failure = {"close_ts_ms": close_ts, "close": close}
        elif failure is not None and reclaim is None and outside:
            reclaim = {"close_ts_ms": close_ts, "close": close}
    return failure, reclaim


def find_inside_retest(direction, boundary, failure_close, bars):
    band_high = boundary * (1 + RETEST_BAND_FRACTION)
    band_low = boundary * (1 - RETEST_BAND_FRACTION)
    if direction == "UPPER":
        initially_in_band = band_low <= failure_close <= boundary
        away = failure_close < band_low
    else:
        initially_in_band = boundary <= failure_close <= band_high
        away = failure_close > band_high
    previous_close = failure_close
    for offset, bar in enumerate(bars):
        if not away:
            if direction == "UPPER" and bar["close"] < band_low:
                away = True
            elif direction == "LOWER" and bar["close"] > band_high:
                away = True
            previous_close = bar["close"]
            continue
        if direction == "UPPER":
            approached = previous_close < band_low and bar["high"] >= band_low
            crossed = bar["high"] >= boundary
            depth = max(0.0, (bar["high"] - band_low) / boundary * 100.0)
        else:
            approached = previous_close > band_high and bar["low"] <= band_high
            crossed = bar["low"] <= boundary
            depth = max(0.0, (band_high - bar["low"]) / boundary * 100.0)
        if approached:
            return {
                "status": "RETEST_AFTER_MOVING_AWAY",
                "initially_in_band": initially_in_band,
                "offset": offset, "bar_open_ts_ms": bar["ts_ms"],
                "depth_pct_of_boundary": depth,
                "boundary_crossed": bool(crossed),
                "bar_open": bar["open"], "bar_high": bar["high"],
                "bar_low": bar["low"], "bar_close": bar["close"],
            }
        previous_close = bar["close"]
    return {
        "status": "ALREADY_IN_BAND_AT_FAILURE_CONFIRMATION" if initially_in_band else "NO_INSIDE_RETEST_WITHIN_WINDOW",
        "initially_in_band": initially_in_band,
    }


def assign_overlap_clusters(event_rows):
    by_asset = defaultdict(list)
    for row in event_rows:
        observed = int(row["observed_bars_12h"])
        if observed <= 0:
            raise ValueError(f'{row["event_id"]}: no positive observed window for clustering')
        by_asset[row["asset"]].append(row)
    mapping = {}
    largest = 0
    size_distribution = defaultdict(int)
    by_asset_counts = {}
    for asset in ASSETS:
        ordered = sorted(by_asset.get(asset, []), key=lambda r: (int(r["signal_time_ms"]), r["event_id"]))
        cluster_number, active, cluster_start, cluster_end = 0, [], None, None

        def finalize():
            nonlocal largest
            if not active:
                return
            size = len(active)
            largest = max(largest, size)
            size_distribution[str(size)] += 1
            cluster_id = f"{asset}|overlap|{cluster_number:04d}"
            for event in active:
                mapping[event["event_id"]] = {
                    "overlap_cluster_id": cluster_id,
                    "overlap_cluster_size": size,
                    "overlap_cluster_start_ts_ms": cluster_start,
                    "overlap_cluster_end_exclusive_ts_ms": cluster_end,
                }

        for row in ordered:
            start = int(row["signal_time_ms"])
            end = start + int(row["observed_bars_12h"]) * MINUTE_MS
            if active and start >= cluster_end:
                finalize()
                active, cluster_start, cluster_end = [], None, None
            if not active:
                cluster_number += 1
                cluster_start, cluster_end = start, end
            else:
                cluster_end = max(cluster_end, end)
            active.append(row)
        finalize()
        by_asset_counts[asset] = cluster_number
    if len(mapping) != len(event_rows):
        raise ValueError("Overlap clustering did not assign every event exactly once")
    return mapping, {
        "total": sum(by_asset_counts.values()),
        "by_asset": by_asset_counts,
        "largest_cluster_size": largest,
        "size_distribution": dict(sorted(size_distribution.items(), key=lambda x: int(x[0]))),
    }


def _float_or_blank(value):
    if value is None or pd.isna(value):
        return ""
    return float(value)


def parse_bool(value):
    if value is None or pd.isna(value):
        return None
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes")
    return bool(value)


def _time_ms_or_blank(value):
    if value is None or pd.isna(value) or value == "":
        return ""
    return timestamp_ms(value)


def _first_15m_close_after(bars15: pd.DataFrame, minute_close_ts: pd.Timestamp):
    candidates = bars15.loc[bars15.index >= minute_close_ts]
    if candidates.empty:
        return None
    ts = candidates.index[0]
    return {"close_ts_ms": timestamp_ms(ts), "close": float(candidates.iloc[0]["close"])}


def analyze_event(event, minute: pd.DataFrame, bars15: pd.DataFrame):
    signal_time = event["signal_time"]
    start_pos = minute.index.get_indexer([signal_time])[0]
    if start_pos < 1:
        raise ValueError(f'{event["event_id"]}: missing exact signal-time minute or prior signal minute')
    if timestamp_ms(signal_time) % QUARTER_HOUR_MS != 0:
        raise ValueError(f'{event["event_id"]}: signal_time is not UTC quarter-hour aligned')
    if signal_time not in bars15.index:
        raise ValueError(f'{event["event_id"]}: original completed 15M signal bar is missing')

    window = minute.iloc[start_pos:start_pos + 720]
    if window.empty:
        raise ValueError(f'{event["event_id"]}: no post-signal 1M window')
    bars = []
    for ts, row in window.iterrows():
        bars.append({
            "ts_ms": timestamp_ms(ts), "open": float(row.open),
            "high": float(row.high), "low": float(row.low), "close": float(row.close),
        })
    previous_signal_close = float(minute.iloc[start_pos - 1]["close"])
    direction, boundary = event["direction"], event["boundary"]
    upper, lower, width = event["upper"], event["lower"], event["channel_width_price"]
    band_high = boundary * (1 + RETEST_BAND_FRACTION)
    band_low = boundary * (1 - RETEST_BAND_FRACTION)

    entry_open = bars[0]["open"]
    immediate_adverse = entry_open <= boundary if direction == "UPPER" else entry_open >= boundary
    first_1m_inside = first_1m_return_inside(direction, boundary, bars)

    post15 = bars15.loc[
        (bars15.index > signal_time) &
        (bars15.index <= signal_time + pd.Timedelta(hours=12))
    ]
    bars15_rows = [(timestamp_ms(ts), float(row.close)) for ts, row in post15.iterrows()]
    failure15, reclaim15 = first_15m_failure_and_reclaim(direction, boundary, bars15_rows)

    outside_retest = find_outside_retest(direction, boundary, previous_signal_close, bars)
    if outside_retest:
        retest_ts = pd.to_datetime(outside_retest["bar_open_ts_ms"], unit="ms", utc=True)
        retest_hold = _first_15m_close_after(bars15, retest_ts + pd.Timedelta(minutes=1))
        if retest_hold is None:
            outside_retest["hold_status"] = "CENSORED_NO_COMPLETE_15M_CLOSE"
            outside_retest["hold_close_ts_ms"] = ""
            outside_retest["hold_close"] = ""
        else:
            hold_outside = retest_hold["close"] > boundary if direction == "UPPER" else retest_hold["close"] < boundary
            outside_retest["hold_status"] = "HELD_OUTSIDE" if hold_outside else "CLOSED_BACK_INSIDE"
            outside_retest["hold_close_ts_ms"] = retest_hold["close_ts_ms"]
            outside_retest["hold_close"] = retest_hold["close"]
        if first_1m_inside is None:
            outside_retest["stage"] = "NO_1M_RETURN_INSIDE_WITHIN_12H"
            outside_retest["same_bar_as_1m_return_inside"] = False
        elif outside_retest["offset"] < first_1m_inside["offset"]:
            outside_retest["stage"] = "BEFORE_FIRST_1M_RETURN_INSIDE"
            outside_retest["same_bar_as_1m_return_inside"] = False
        elif outside_retest["offset"] == first_1m_inside["offset"]:
            outside_retest["stage"] = "SAME_1M_BAR_AS_RETURN_INSIDE"
            outside_retest["same_bar_as_1m_return_inside"] = True
        else:
            outside_retest["stage"] = "AFTER_FIRST_1M_RETURN_INSIDE"
            outside_retest["same_bar_as_1m_return_inside"] = False
        retest_offset = outside_retest["offset"]
        stop_offset = len(bars)
        if first_1m_inside and first_1m_inside["offset"] > retest_offset:
            stop_offset = first_1m_inside["offset"]
        continuation = bars[retest_offset + 1:stop_offset]
        if continuation:
            if direction == "UPPER":
                extreme = max(x["high"] for x in continuation)
                adverse = max(0.0, boundary - min(x["low"] for x in continuation))
                extreme_bar = next(x for x in continuation if x["high"] == extreme)
            else:
                extreme = min(x["low"] for x in continuation)
                adverse = max(0.0, max(x["high"] for x in continuation) - boundary)
                extreme_bar = next(x for x in continuation if x["low"] == extreme)
            continuation_price = max(0.0, extreme - boundary) if direction == "UPPER" else max(0.0, boundary - extreme)
            outside_retest.update({
                "post_retest_continuation_width_pct": continuation_price / width * 100.0,
                "post_retest_continuation_time_ts_ms": extreme_bar["ts_ms"],
                "post_retest_continuation_minutes": (extreme_bar["ts_ms"] - outside_retest["bar_open_ts_ms"]) // MINUTE_MS,
                "post_retest_adverse_width_pct": adverse / width * 100.0,
            })
        else:
            outside_retest.update({
                "post_retest_continuation_width_pct": "",
                "post_retest_continuation_time_ts_ms": "",
                "post_retest_continuation_minutes": "",
                "post_retest_adverse_width_pct": "",
            })

    inside_retest = None
    if failure15:
        failure_ts = pd.to_datetime(failure15["close_ts_ms"], unit="ms", utc=True)
        failure_idx = minute.index.get_indexer([failure_ts])[0]
        if failure_idx < 0:
            inside_retest = {"status": "NO_EXACT_1M_BAR_AT_FAILURE_CONFIRMATION"}
        else:
            failure_window = minute.iloc[failure_idx:start_pos + 720]
            failure_bars = [{
                "ts_ms": timestamp_ms(ts), "open": float(row.open),
                "high": float(row.high), "low": float(row.low), "close": float(row.close),
            } for ts, row in failure_window.iterrows()]
            inside_retest = find_inside_retest(direction, boundary, failure15["close"], failure_bars)
            if inside_retest.get("offset") is not None:
                retest_ts = pd.to_datetime(inside_retest["bar_open_ts_ms"], unit="ms", utc=True)
                hold = _first_15m_close_after(bars15, retest_ts + pd.Timedelta(minutes=1))
                if hold is None:
                    inside_retest["hold_status"] = "CENSORED_NO_COMPLETE_15M_CLOSE"
                    inside_retest["hold_close_ts_ms"] = ""
                else:
                    hold_inside = hold["close"] <= boundary if direction == "UPPER" else hold["close"] >= boundary
                    inside_retest["hold_status"] = "HELD_INSIDE" if hold_inside else "RECLAIMED_OUTSIDE"
                    inside_retest["hold_close_ts_ms"] = hold["close_ts_ms"]
                    inside_retest["hold_close"] = hold["close"]
                if reclaim15 is None:
                    inside_retest["stage"] = "NO_BREAKOUT_SIDE_RECLAIM_WITHIN_12H"
                elif inside_retest["bar_open_ts_ms"] + MINUTE_MS <= reclaim15["close_ts_ms"]:
                    inside_retest["stage"] = "BEFORE_OR_AT_BREAKOUT_SIDE_RECLAIM"
                else:
                    inside_retest["stage"] = "AFTER_BREAKOUT_SIDE_RECLAIM"

    reversal = {}
    if failure15:
        failure_ts = pd.to_datetime(failure15["close_ts_ms"], unit="ms", utc=True)
        failure_idx = minute.index.get_indexer([failure_ts])[0]
        if failure_idx >= 0:
            reversal_window = minute.iloc[failure_idx:start_pos + 720]
            if not reversal_window.empty:
                if direction == "UPPER":
                    favourable_idx = int(np.argmin(reversal_window["low"].to_numpy()))
                    adverse_idx = int(np.argmax(reversal_window["high"].to_numpy()))
                    favourable_price = float(reversal_window.iloc[favourable_idx]["low"])
                    adverse_price = float(reversal_window.iloc[adverse_idx]["high"])
                    favourable_move = max(0.0, failure15["close"] - favourable_price)
                    adverse_move = max(0.0, adverse_price - failure15["close"])
                else:
                    favourable_idx = int(np.argmax(reversal_window["high"].to_numpy()))
                    adverse_idx = int(np.argmin(reversal_window["low"].to_numpy()))
                    favourable_price = float(reversal_window.iloc[favourable_idx]["high"])
                    adverse_price = float(reversal_window.iloc[adverse_idx]["low"])
                    favourable_move = max(0.0, favourable_price - failure15["close"])
                    adverse_move = max(0.0, failure15["close"] - adverse_price)
                favourable_ts = timestamp_ms(reversal_window.index[favourable_idx])
                adverse_ts = timestamp_ms(reversal_window.index[adverse_idx])
                reversal = {
                    "reversal_favourable_price": favourable_price,
                    "reversal_favourable_ts_ms": favourable_ts,
                    "reversal_favourable_minutes": (favourable_ts - failure15["close_ts_ms"]) // MINUTE_MS,
                    "reversal_favourable_width_pct": favourable_move / width * 100.0,
                    "reversal_adverse_price": adverse_price,
                    "reversal_adverse_ts_ms": adverse_ts,
                    "reversal_adverse_minutes": (adverse_ts - failure15["close_ts_ms"]) // MINUTE_MS,
                    "reversal_adverse_width_pct": adverse_move / width * 100.0,
                }

    event_result = dict(event)
    event_result.update({
        "signal_time_ms": timestamp_ms(signal_time),
        "entry_time_ms": timestamp_ms(signal_time),
        "entry_open": entry_open,
        "entry_open_already_through_boundary": bool(immediate_adverse),
        "band_high": band_high, "band_low": band_low,
        "observed_bars_12h": len(bars),
        "complete_12h": len(bars) == 720,
        "first_1m_return_inside_bar_open_ts_ms": first_1m_inside["bar_open_ts_ms"] if first_1m_inside else "",
        "first_1m_return_inside_available_ts_ms": first_1m_inside["available_ts_ms"] if first_1m_inside else "",
        "first_15m_return_inside_close_ts_ms": failure15["close_ts_ms"] if failure15 else "",
        "breakout_side_reclaim_close_ts_ms": reclaim15["close_ts_ms"] if reclaim15 else "",
        "outside_retest_status": outside_retest["stage"] if outside_retest else "NO_OUTSIDE_RETEST_WITHIN_12H",
        "outside_retest_bar_open_ts_ms": outside_retest["bar_open_ts_ms"] if outside_retest else "",
        "outside_retest_elapsed_minutes": outside_retest["elapsed_minutes"] if outside_retest else "",
        "outside_retest_depth_pct_of_boundary": outside_retest["depth_pct_of_boundary"] if outside_retest else "",
        "outside_retest_boundary_crossed": outside_retest["boundary_crossed"] if outside_retest else "",
        "outside_retest_hold_status": outside_retest["hold_status"] if outside_retest else "",
        "outside_retest_hold_close_ts_ms": outside_retest.get("hold_close_ts_ms", "") if outside_retest else "",
        "outside_retest_same_bar_ambiguous": outside_retest["same_bar_as_1m_return_inside"] if outside_retest else False,
        "post_retest_continuation_width_pct": outside_retest.get("post_retest_continuation_width_pct", "") if outside_retest else "",
        "post_retest_continuation_time_ts_ms": outside_retest.get("post_retest_continuation_time_ts_ms", "") if outside_retest else "",
        "post_retest_continuation_minutes": outside_retest.get("post_retest_continuation_minutes", "") if outside_retest else "",
        "post_retest_adverse_width_pct": outside_retest.get("post_retest_adverse_width_pct", "") if outside_retest else "",
        "inside_retest_status": inside_retest["status"] if inside_retest else "NO_15M_FAILURE_CONFIRMATION",
        "inside_retest_bar_open_ts_ms": inside_retest.get("bar_open_ts_ms", "") if inside_retest else "",
        "inside_retest_depth_pct_of_boundary": inside_retest.get("depth_pct_of_boundary", "") if inside_retest else "",
        "inside_retest_boundary_crossed": inside_retest.get("boundary_crossed", "") if inside_retest else "",
        "inside_retest_hold_status": inside_retest.get("hold_status", "") if inside_retest else "",
        "inside_retest_hold_close_ts_ms": inside_retest.get("hold_close_ts_ms", "") if inside_retest else "",
        "inside_retest_stage": inside_retest.get("stage", "") if inside_retest else "",
        **reversal,
    })

    horizon_results = []
    for horizon_name, minutes in HORIZONS:
        complete = len(bars) >= minutes
        sample = bars[:minutes]
        if not sample:
            raise ValueError(f'{event["event_id"]}: empty horizon sample')
        highs = np.asarray([x["high"] for x in sample], dtype=float)
        lows = np.asarray([x["low"] for x in sample], dtype=float)
        closes = np.asarray([x["close"] for x in sample], dtype=float)
        opens = np.asarray([x["open"] for x in sample], dtype=float)
        if direction == "UPPER":
            favourable_idx = int(np.argmax(highs))
            adverse_idx = int(np.argmin(lows))
            favourable_price = float(highs[favourable_idx])
            adverse_price = float(lows[adverse_idx])
            favourable_move = favourable_price - entry_open
            adverse_move = entry_open - adverse_price
            boundary_failure_mask = closes <= boundary
            ended_inside = bool(closes[-1] <= boundary)
            extension = max(0.0, favourable_price - boundary)
        else:
            favourable_idx = int(np.argmin(lows))
            adverse_idx = int(np.argmax(highs))
            favourable_price = float(lows[favourable_idx])
            adverse_price = float(highs[adverse_idx])
            favourable_move = entry_open - favourable_price
            adverse_move = adverse_price - entry_open
            boundary_failure_mask = closes >= boundary
            ended_inside = bool(closes[-1] >= boundary)
            extension = max(0.0, boundary - favourable_price)
        failure_positions = np.flatnonzero(boundary_failure_mask)
        failure_offset = int(failure_positions[0]) if len(failure_positions) else None
        favourable_ts = sample[favourable_idx]["ts_ms"]
        adverse_ts = sample[adverse_idx]["ts_ms"]
        failure_ts = sample[failure_offset]["ts_ms"] if failure_offset is not None else ""
        horizon_end_ts = sample[-1]["ts_ms"] + MINUTE_MS
        retest_in_horizon = bool(outside_retest and outside_retest["offset"] < minutes)
        retest_hold_in_horizon = bool(
            retest_in_horizon and outside_retest.get("hold_close_ts_ms")
            and int(outside_retest["hold_close_ts_ms"]) <= horizon_end_ts
        )
        horizon_results.append({
            "event_id": event["event_id"], "asset": event["asset"],
            "definition": event["definition"], "direction": direction,
            "pre_breakout_group": event["pre_breakout_group"],
            "horizon": horizon_name, "horizon_minutes": minutes,
            "complete": complete, "horizon_status": "COMPLETE" if complete else "INCOMPLETE",
            "observed_bars": len(sample),
            "entry_time_ms": timestamp_ms(signal_time), "entry_open": entry_open,
            "directional_close_return_pct": (1.0 if direction == "UPPER" else -1.0) * (closes[-1] / entry_open - 1.0) * 100.0,
            "mfe_pct": favourable_move / entry_open * 100.0,
            "mae_pct": adverse_move / entry_open * 100.0,
            "mfe_channel_width_pct": favourable_move / width * 100.0,
            "mae_channel_width_pct": adverse_move / width * 100.0,
            "favourable_extreme_price": favourable_price,
            "favourable_extreme_time_ms": favourable_ts,
            "time_to_mfe_minutes": favourable_idx,
            "adverse_extreme_price": adverse_price,
            "adverse_extreme_time_ms": adverse_ts,
            "time_to_mae_minutes": adverse_idx,
            "extension_pct_of_boundary": extension / boundary * 100.0,
            "extension_pct_of_channel": extension / width * 100.0,
            "entry_open_already_through_boundary": bool(immediate_adverse),
            "boundary_failure": failure_offset is not None,
            "boundary_failure_time_ms": failure_ts,
            "minutes_to_boundary_failure": failure_offset if failure_offset is not None else "",
            "ended_inside": ended_inside,
            "outside_retest": retest_in_horizon,
            "outside_retest_boundary_crossed": bool(retest_in_horizon and outside_retest["boundary_crossed"]),
            "outside_retest_minutes": outside_retest["elapsed_minutes"] if retest_in_horizon else "",
            "outside_retest_depth_pct_of_boundary": outside_retest["depth_pct_of_boundary"] if retest_in_horizon else "",
            "outside_retest_hold": outside_retest["hold_status"] in ("HELD_OUTSIDE",) if retest_hold_in_horizon else "",
            "first_1m_return_inside_available_ts_ms": first_1m_inside["available_ts_ms"] if first_1m_inside and first_1m_inside["available_ts_ms"] <= horizon_end_ts else "",
            "first_15m_return_inside_close_ts_ms": failure15["close_ts_ms"] if failure15 and failure15["close_ts_ms"] <= horizon_end_ts else "",
            "breakout_side_reclaim_close_ts_ms": reclaim15["close_ts_ms"] if reclaim15 and reclaim15["close_ts_ms"] <= horizon_end_ts else "",
            "inside_retest": bool(inside_retest and inside_retest.get("offset") is not None and inside_retest["bar_open_ts_ms"] + MINUTE_MS <= horizon_end_ts),
            "inside_retest_hold": (
                inside_retest.get("hold_status") == "HELD_INSIDE"
                if inside_retest and inside_retest.get("hold_close_ts_ms")
                and int(inside_retest["hold_close_ts_ms"]) <= horizon_end_ts else ""
            ),
        })
    return event_result, horizon_results


def compare_with_forward_archive(horizon_rows, reference):
    ref_map = {}
    for _, row in reference.iterrows():
        key = (row.asset, row.definition, row.direction, timestamp_ms(row.signal_time), str(row.horizon))
        ref_map[key] = row
    output = []
    metric_pairs = (
        ("entry_time_ms", "entry_time"),
        ("directional_close_return_pct", "directional_close_return_pct"),
        ("mfe_pct", "mfe_pct"), ("mae_pct", "mae_pct"),
        ("mfe_channel_width_pct", "mfe_channel_width_pct"),
        ("mae_channel_width_pct", "mae_channel_width_pct"),
        ("favourable_extreme_price", "favourable_extreme_price"),
        ("adverse_extreme_price", "adverse_extreme_price"),
        ("time_to_mfe_minutes", "time_to_mfe_minutes"),
        ("time_to_mae_minutes", "time_to_mae_minutes"),
        ("entry_open", "entry_open"), ("entry_open_already_through_boundary", "entry_open_already_through_boundary"),
        ("horizon_status", "horizon_status"),
        ("favourable_extreme_time_ms", "favourable_extreme_time"),
        ("adverse_extreme_time_ms", "adverse_extreme_time"),
        ("boundary_failure_time_ms", "boundary_failure_time"),
        ("boundary_failure", "boundary_failure"), ("minutes_to_boundary_failure", "minutes_to_boundary_failure"),
        ("outside_retest", "band_approach"), ("outside_retest_boundary_crossed", "boundary_penetration"),
        ("outside_retest_minutes", "retest_minutes"), ("outside_retest_depth_pct_of_boundary", "penetration_depth_pct"),
    )
    mismatches = []
    for row in horizon_rows:
        key = (row["asset"], row["definition"], row["direction"], row["entry_time_ms"], row["horizon"])
        ref = ref_map.get(key)
        if ref is None:
            raise ValueError(f"Missing accepted forward-outcome reference row: {key}")
        checks = {}
        for ours, theirs in metric_pairs:
            a, b = row.get(ours), ref.get(theirs)
            if a == "" or a is None or pd.isna(a):
                checks[ours] = bool(pd.isna(b) or b == "")
            elif ours.endswith("_time_ms") and theirs.endswith("_time"):
                checks[ours] = bool(pd.notna(b) and timestamp_ms(b) == int(a))
            elif isinstance(a, (bool, np.bool_)):
                parsed_b = parse_bool(b)
                checks[ours] = parsed_b is not None and bool(a) == parsed_b
            elif isinstance(a, (int, float, np.integer, np.floating)):
                checks[ours] = bool(pd.notna(b) and math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-8))
            else:
                checks[ours] = str(a) == str(b)
        # Retest hold is only comparable when the first completed 15M close is within this horizon.
        ref_hold = parse_bool(ref.get("retest_hold"))
        if row["outside_retest_hold"] != "":
            checks["outside_retest_hold"] = ref_hold is not None and bool(row["outside_retest_hold"]) == ref_hold
        else:
            checks["outside_retest_hold"] = ref_hold is None
        all_pass = all(checks.values())
        if not all_pass:
            mismatches.append({"event_id": row["event_id"], "horizon": row["horizon"], "failed_fields": [k for k,v in checks.items() if not v]})
        output.append({
            "event_id": row["event_id"], "asset": row["asset"],
            "definition": row["definition"], "direction": row["direction"],
            "horizon": row["horizon"], "reference_match": all_pass,
            "failed_fields": ";".join(k for k,v in checks.items() if not v),
        })
    if mismatches:
        raise ValueError(f"Forward archive cross-validation failed on {len(mismatches)} rows; sample={mismatches[:5]}")
    return output


def build_group_summary(event_rows, horizon_rows):
    horizons = pd.DataFrame(horizon_rows)
    group_cols = ["asset", "definition", "direction", "pre_breakout_group", "horizon"]
    result = []
    for key, group in horizons.groupby(group_cols, dropna=False, sort=True):
        result.append({
            **dict(zip(group_cols, key)),
            "events": len(group),
            "overlap_clusters": group["overlap_cluster_id"].nunique(),
            "complete": int(group["complete"].sum()),
            "censored": int((~group["complete"]).sum()),
            "boundary_failures": int(group["boundary_failure"].sum()),
            "boundary_failure_rate": float(group["boundary_failure"].mean()),
            "outside_retests": int(group["outside_retest"].sum()),
            "outside_retest_rate": float(group["outside_retest"].mean()),
            "one_minute_return_inside": int(group["first_1m_return_inside_available_ts_ms"].apply(lambda x: x is not None and not pd.isna(x) and x != "").sum()),
            "fifteen_minute_failure_confirmations": int(group["first_15m_return_inside_close_ts_ms"].apply(lambda x: x is not None and not pd.isna(x) and x != "").sum()),
            "breakout_side_reclaims": int(group["breakout_side_reclaim_close_ts_ms"].apply(lambda x: x is not None and not pd.isna(x) and x != "").sum()),
            "inside_retests": int(group["inside_retest"].sum()),
            "mfe_median_pct": float(group["mfe_pct"].median()),
            "mae_median_pct": float(group["mae_pct"].median()),
            "mfe_channel_median_pct": float(group["mfe_channel_width_pct"].median()),
            "mae_channel_median_pct": float(group["mae_channel_width_pct"].median()),
        })
    return result


def run(root: Path, output_dir: Path):
    source_blob_ids = {
        relative: verify_blob(root, relative, expected)
        for relative, expected in EXPECTED_BLOBS.items()
    }
    prior_meta = json.loads((root / "reports/breakout_prior_test_count_v1/run_metadata.json").read_text())
    forward_meta = json.loads((root / "reports/breakout_forward_outcome_v1/run_metadata.json").read_text())
    if prior_meta["original_source_git_blob_sha"] != EXPECTED_BLOBS["research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py"]:
        raise ValueError("Prior-test metadata original source SHA mismatch")
    if prior_meta["expected_counts_reproduced"] != 20 or prior_meta["expected_quantiles_reproduced"] != 10:
        raise ValueError("Prior-test source reproduction gate was not fully passed")
    if forward_meta["expected_event_counts_reproduced"] != 20 or forward_meta["expected_quantiles_reproduced"] != 10:
        raise ValueError("Forward-outcome source reproduction gate was not fully passed")
    if prior_meta["common_1m_timestamps"] != EXPECTED_COMMON_MINUTES or prior_meta["common_1m_gaps"] != 0:
        raise ValueError("Accepted common 1M timeline metadata mismatch")

    market_frames, market_hashes = {}, {}
    for asset in ASSETS:
        market_frames[asset], market_hashes[asset] = load_market(root, asset)
    common = market_frames[ASSETS[0]].index
    for asset in ASSETS[1:]:
        common = common.intersection(market_frames[asset].index)
    common = common.sort_values()
    if len(common) != EXPECTED_COMMON_MINUTES:
        raise ValueError(f"Expected {EXPECTED_COMMON_MINUTES} common minutes, got {len(common)}")
    if len(common) > 1 and not np.all(np.diff(common.asi8) == MINUTE_NS):
        raise ValueError("Common five-asset 1M timeline has gaps or irregular intervals")
    market_frames = {asset: frame.reindex(common) for asset, frame in market_frames.items()}
    if any(frame[["open","high","low","close"]].isna().any().any() for frame in market_frames.values()):
        raise ValueError("Common 1M intersection has missing OHLC values")
    bars15_by_asset = {asset: build_complete_15m(frame) for asset, frame in market_frames.items()}

    classes = pd.read_csv(root / "reports/breakout_prior_test_count_v1/breakout_prior_test_classifications_v1.csv")
    links = pd.read_csv(root / "reports/breakout_prior_test_count_v1/breakout_prior_test_links_v1.csv")
    forward = pd.read_csv(root / "reports/breakout_forward_outcome_v1/breakout_forward_outcomes_v1.csv")
    classes["signal_time"] = pd.to_datetime(classes["signal_time"], utc=True)
    links["signal_time"] = pd.to_datetime(links["signal_time"], utc=True)
    forward["signal_time"] = pd.to_datetime(forward["signal_time"], utc=True)
    primary = classes.loc[np.isclose(classes["zone_pct_of_channel"], PRIMARY_ZONE)].copy()
    primary_links = links.loc[np.isclose(links["zone_pct_of_channel"], PRIMARY_ZONE)].copy()
    primary_forward = forward.loc[np.isclose(forward["zone_pct_of_channel"], PRIMARY_ZONE)].copy()
    if len(classes) != EXPECTED_CLASSIFICATION_ROWS or len(links) != EXPECTED_LINK_ROWS:
        raise ValueError("Archived prior-test classification/link row counts changed")
    if len(primary) != EXPECTED_PRIMARY_EVENTS or primary.duplicated(["asset","definition","direction","signal_time","zone_pct_of_channel"]).any():
        raise ValueError("Primary 10% breakout event population is not 1,592 unique rows")
    if len(primary_links) != EXPECTED_PRIMARY_LINK_ROWS:
        raise ValueError("Primary 10% prior-test link row count mismatch")
    if len(primary_forward) != EXPECTED_PRIMARY_EVENTS * 4:
        raise ValueError("Primary forward-outcome reference must have exactly four horizons per event")

    link_groups = defaultdict(list)
    for _, link in primary_links.iterrows():
        key = (link.asset, link.definition, link.direction, timestamp_ms(link.signal_time), float(link.zone_pct_of_channel))
        link_groups[key].append(link)
    event_rows, horizon_rows, link_output = [], [], []
    seen_event_ids = set()
    zero_link_events = 0
    for _, source in primary.iterrows():
        key = (source.asset, source.definition, source.direction, timestamp_ms(source.signal_time), float(source.zone_pct_of_channel))
        event_id = event_id_from_key(key)
        if event_id in seen_event_ids:
            raise ValueError(f"Duplicate primary breakout event ID: {event_id}")
        seen_event_ids.add(event_id)
        prior_links = link_groups.get(key, [])
        declared = int(source.prior_touch_test_count)
        if len(prior_links) != declared:
            raise ValueError(f"{event_id}: prior-test link count {len(prior_links)} != declared {declared}")
        if declared == 0:
            zero_link_events += 1
        upper, lower, width = float(source.upper), float(source.lower), float(source.channel_width_price)
        boundary = upper if source.direction == "UPPER" else lower
        if not all(math.isfinite(x) for x in (upper, lower, width, boundary)) or width <= 0:
            raise ValueError(f"{event_id}: invalid frozen boundary geometry")
        if abs((upper - lower) - width) > 1e-8:
            raise ValueError(f"{event_id}: channel width does not equal upper minus lower")
        if abs(float(source.boundary) - boundary) > 1e-8:
            raise ValueError(f"{event_id}: boundary column does not match direction")
        for link in prior_links:
            if abs(float(link.upper) - upper) > 1e-8 or abs(float(link.lower) - lower) > 1e-8 or abs(float(link.channel_width_price) - width) > 1e-8:
                raise ValueError(f"{event_id}: linked prior-test boundary mismatch")
            if not pd.to_datetime(link.test_start_time, utc=True) < source.signal_time:
                raise ValueError(f"{event_id}: prior test starts at/after breakout signal")
            if pd.notna(link.first_rejection_time) and not pd.to_datetime(link.first_rejection_time, utc=True) < source.signal_time:
                raise ValueError(f"{event_id}: prior rejection is not strictly before breakout")
            if pd.notna(link.test_end_time) and pd.to_datetime(link.test_end_time, utc=True) > source.signal_time:
                raise ValueError(f"{event_id}: prior test end is after breakout signal")
            link_dict = link.to_dict()
            link_dict["event_id"] = event_id
            link_dict["prior_test_link_id"] = f'{event_id}|prior_test|{timestamp_ms(link.test_start_time)}'
            link_output.append(link_dict)

        minute = market_frames[source.asset]
        signal_pos = minute.index.get_indexer([source.signal_time])[0]
        if signal_pos <= 0:
            raise ValueError(f"{event_id}: exact signal-time 1M bar or prior signal minute is missing")
        if source.signal_time not in bars15_by_asset[source.asset].index:
            raise ValueError(f"{event_id}: original 15M signal close is not reproduced")
        event = {
            "event_id": event_id, "asset": source.asset, "definition": source.definition,
            "direction": source.direction, "signal_time": source.signal_time,
            "signal_time_ms": key[3], "snapshot": source.snapshot,
            "boundary": boundary, "upper": upper, "lower": lower,
            "channel_width_price": width, "channel_width_pct": float(source.channel_width_pct),
            "zone_pct_of_channel": float(source.zone_pct_of_channel),
            "prior_touch_test_count": declared,
            "prior_confirmed_rejection_count": int(source.prior_confirmed_rejection_count),
            "prior_contact_only_test_count": int(source.prior_contact_only_test_count),
            "pre_breakout_group": source.pre_breakout_group,
            "prior_segment_id": int(source.prior_segment_id),
            "prior_test_link_count": len(prior_links),
        }
        event_result, horizons = analyze_event(event, minute, bars15_by_asset[source.asset])
        event_rows.append(event_result)
        horizon_rows.extend(horizons)

    if len(event_rows) != EXPECTED_PRIMARY_EVENTS or zero_link_events != EXPECTED_PRIMARY_ZERO_LINK_EVENTS:
        raise ValueError("Primary event / zero-prior-test population mismatch")

    # Validate each primary event has four complete forward-reference rows.
    reference_keys = set()
    for _, row in primary_forward.iterrows():
        reference_keys.add((row.asset, row.definition, row.direction, timestamp_ms(row.signal_time), str(row.horizon)))
    if len(reference_keys) != len(primary_forward):
        raise ValueError("Duplicate primary forward-outcome event/horizon keys")
    cross_validation = compare_with_forward_archive(horizon_rows, primary_forward)

    # Attach deterministic overlap clusters to event and derived rows.
    cluster_map, cluster_summary = assign_overlap_clusters(event_rows)
    for row in event_rows:
        row.update(cluster_map[row["event_id"]])
    for row in horizon_rows:
        row.update(cluster_map[row["event_id"]])
    summaries = build_group_summary(event_rows, horizon_rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(event_rows).to_csv(output_dir / "breakout_lifecycle_events_v1_1.csv", index=False)
    pd.DataFrame(horizon_rows).to_csv(output_dir / "breakout_lifecycle_horizons_v1_1.csv", index=False)
    pd.DataFrame(link_output).to_csv(output_dir / "breakout_lifecycle_prior_links_v1_1.csv", index=False)
    pd.DataFrame(cross_validation).to_csv(output_dir / "breakout_lifecycle_forward_crosscheck_v1_1.csv", index=False)
    pd.DataFrame(summaries).to_csv(output_dir / "breakout_lifecycle_group_summary_v1_1.csv", index=False)

    metadata = {
        "study": "Phase 3 Breakout / Failed-Breakout Lifecycle V1.1",
        "status": "DESCRIPTIVE_RUN_COMPLETE_PENDING_INDEPENDENT_CLOSEOUT",
        "protocol": "docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md",
        "protocol_amendment": "docs/research_checkpoints/2026-11-25_phase3_breakout_lifecycle_v1_1_amendment.md",
        "original_source_git_blob_sha": EXPECTED_BLOBS["research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py"],
        "primary_zone_pct_of_channel": PRIMARY_ZONE,
        "post_breakout_retest_band_pct_of_boundary": RETEST_BAND_PCT,
        "assets": list(ASSETS),
        "primary_events": len(event_rows),
        "primary_definitions": {"BROAD_P40": 932, "STRICT_P25": 660},
        "primary_directions": {"UPPER": 823, "LOWER": 769},
        "primary_links": len(link_output),
        "events_with_zero_prior_touch_tests": zero_link_events,
        "horizon_rows": len(horizon_rows),
        "forward_crosscheck_rows": len(cross_validation),
        "forward_crosscheck_passed": sum(1 for x in cross_validation if x["reference_match"]),
        "common_1m_timestamps": len(common),
        "common_1m_gaps": int(np.count_nonzero(np.diff(common.asi8) != MINUTE_NS)),
        "source_rows": {asset: market_hashes[asset]["rows"] for asset in ASSETS},
        "source_git_blob_ids": source_blob_ids,
        "source_sha256": {asset: market_hashes[asset]["sha256"] for asset in ASSETS},
        "overlap_clusters": cluster_summary,
        "reproduction_gates": {
            "original_event_counts_reproduced": prior_meta["expected_counts_reproduced"],
            "original_quantiles_reproduced": prior_meta["expected_quantiles_reproduced"],
            "primary_classification_rows": len(primary),
            "primary_prior_test_link_rows": len(primary_links),
            "prior_test_link_count_mismatches": 0,
            "primary_forward_reference_rows": len(primary_forward),
        },
        "output_sha256": {},
        "limitations": [
            "Descriptive lifecycle and price-path study only; no orders, fills, fees, funding, PnL or profitability inference.",
            "Strict breakout definition is nested within broad; never pool as independent samples.",
            "OHLC data cannot establish intraminute event order or executable fills.",
            "The 10% prior-test zone is 10% of channel width; the post-breakout retest band is separately 0.10% of boundary price.",
            "Overlapping event windows are dependent; clusters are reported and no independent-event standard errors are calculated.",
            "The original full-sample P25/P40 channel-width quantiles are retrospective and not live calibrated.",
        ],
    }
    for path in sorted(output_dir.glob("*.csv")):
        metadata["output_sha256"][path.name] = file_sha256(path)
    (output_dir / "run_metadata_v1_1.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    log = [
        "Phase 3 Breakout / Failed-Breakout Lifecycle V1.1",
        f"primary_events={len(event_rows)}",
        f"primary_prior_test_links={len(link_output)}",
        f"horizon_rows={len(horizon_rows)}",
        f"forward_crosscheck_passed={metadata['forward_crosscheck_passed']}/{len(cross_validation)}",
        f"overlap_clusters={cluster_summary}",
        "No strategy simulation, fills, or PnL were performed.",
    ]
    (output_dir / "run.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=None)
    parser.add_argument("--output-dir", default="reports/phase3_breakout_lifecycle_v1_1")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    result = run(root, (root / args.output_dir).resolve())
    print(json.dumps({
        "status": result["status"],
        "primary_events": result["primary_events"],
        "primary_links": result["primary_links"],
        "horizon_rows": result["horizon_rows"],
        "forward_crosscheck_passed": result["forward_crosscheck_passed"],
        "overlap_clusters": result["overlap_clusters"]["total"],
    }, indent=2))


if __name__ == "__main__":
    main()
