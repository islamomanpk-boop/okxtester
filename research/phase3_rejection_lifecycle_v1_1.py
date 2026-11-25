#!/usr/bin/env python3
"""Descriptive Phase 3 rejection lifecycle V1.1 with overlap clusters; no trade simulation or PnL."""
from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import math
import statistics
from array import array
from collections import defaultdict
from pathlib import Path

ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
HORIZONS = (("15m", 15), ("1h", 60), ("4h", 240), ("24h", 1440))
MINUTE_MS = 60_000
CONFIRMATION_DELAY_MS = 900_000
TOUCH_BAND = 0.10
SEPARATION_BAND = 0.20
EXPECTED_LEDGER_ROWS = 2452
EXPECTED_ANATOMY_ROWS = 1992
EXPECTED_COHORTS = {"broad": 1154, "strict": 838}

# Git blob object IDs pin the exact accepted inputs reviewed before implementation.
EXPECTED_BLOBS = {
    "reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv": "2af6f85cd60194019f903a17f16216841ae61f8c",
    "reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv": "c58de65ec1936607790c2ee40b828897e6f726dc",
    "reports/sideways_detector_original_v1/BTC_features_original_v1.csv": "e422073b993cf5d9d11050216509165277339710",
    "reports/sideways_detector_original_v1/ETH_features_original_v1.csv": "c38641d3846931afd6e44a7f39318251fe3c5653",
    "reports/sideways_detector_original_v1/SOL_features_original_v1.csv": "5ba90a99a33924f3de6bcbe9cd1d76aa0a9dd207",
    "reports/sideways_detector_original_v1/DOGE_features_original_v1.csv": "5fb8cb621628e069b1e2500f8047eb908b031909",
    "reports/sideways_detector_original_v1/AVAX_features_original_v1.csv": "06b6f7ee947ef5e62b8cf2b9cc64fb7caaa523e5",
    "data/market_1m/BTC_USDT_USDT_1m.csv": "639f7b8a6d54747dd3eb3370dc133d53f6382bfd",
    "data/market_1m/ETH_USDT_USDT_1m.csv": "3017d870fe1cb764e1acb8fdec04138592749d69",
    "data/market_1m/SOL_USDT_USDT_1m.csv": "a850c2dc4a2c14b34b59737ccfbb2e4c59d97bf3",
    "data/market_1m/DOGE_USDT_USDT_1m.csv": "2162df0f277bef6c04bd191b459a35d735c68f2d",
    "data/market_1m/AVAX_USDT_USDT_1m.csv": "6e0cb0c55aa2aafb4118d62522826bcf1a2aeb62",
}


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def verify_blob(root: Path, relative: str, expected: str) -> str:
    path = root / relative
    if not path.is_file():
        raise FileNotFoundError(f"Required source is missing: {relative}")
    actual = git_blob_sha1(path)
    if actual != expected:
        raise ValueError(
            f"Source Git blob mismatch for {relative}: expected {expected}, got {actual}"
        )
    return actual


def to_int_ms(value, label: str) -> int:
    number = float(value)
    if not math.isfinite(number) or not number.is_integer():
        raise ValueError(f"{label} must be an exact finite millisecond timestamp")
    return int(number)


def optional_finite_float(value):
    if value is None or str(value).strip() == "":
        return ""
    number = float(value)
    return number if math.isfinite(number) else ""


def read_dict_rows(path: Path):
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        return list(reader)


def load_features(root: Path, asset: str):
    relative = f"reports/sideways_detector_original_v1/{asset}_features_original_v1.csv"
    rows = read_dict_rows(root / relative)
    if len(rows) != 2358:
        raise ValueError(f"{asset}: expected 2,358 frozen feature rows, got {len(rows)}")
    for index, row in enumerate(rows):
        if row.get("asset") != asset:
            raise ValueError(f"{asset}: feature asset mismatch at row {index}")
    return rows


def load_market_bars(root: Path, asset: str):
    relative = f"data/market_1m/{asset}_USDT_USDT_1m.csv"
    timestamps = array("q")
    opens, highs, lows, closes = (array("d") for _ in range(4))
    gaps = 0
    previous = None
    with (root / relative).open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"ts", "open", "high", "low", "close"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{asset}: 1M source missing required OHLC columns")
        for row_number, row in enumerate(reader, start=2):
            ts = to_int_ms(row["ts"], f"{asset} row {row_number} ts")
            o, h, low, close = (float(row[k]) for k in ("open", "high", "low", "close"))
            if not all(math.isfinite(v) and v > 0 for v in (o, h, low, close)):
                raise ValueError(f"{asset}: invalid OHLC at row {row_number}")
            if low > min(o, close) or h < max(o, close) or low > h:
                raise ValueError(f"{asset}: inconsistent OHLC at row {row_number}")
            if previous is not None:
                if ts <= previous:
                    raise ValueError(f"{asset}: duplicate or unordered timestamps")
                if ts - previous != MINUTE_MS:
                    gaps += 1
            timestamps.append(ts)
            opens.append(o)
            highs.append(h)
            lows.append(low)
            closes.append(close)
            previous = ts
    if not timestamps:
        raise ValueError(f"{asset}: empty 1M source")
    return {
        "ts": timestamps, "open": opens, "high": highs,
        "low": lows, "close": closes, "gap_count": gaps,
    }


def make_event_id(row: dict) -> str:
    return "|".join((
        row["asset"],
        row["definition"].lower(),
        row["direction"].lower(),
        str(int(row["snapshot_index"])),
        str(int(row["segment_id"])),
        str(int(row["test_rank"])),
        str(to_int_ms(row["test_start_ts_ms"], "test_start_ts_ms")),
    ))


def prepare_events(root: Path, features_by_asset, anatomy_by_id):
    ledger_path = root / "reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv"
    rows = read_dict_rows(ledger_path)
    if len(rows) != EXPECTED_LEDGER_ROWS:
        raise ValueError(f"Expected {EXPECTED_LEDGER_ROWS} source-ledger rows, got {len(rows)}")

    eligible = []
    counts = defaultdict(int)
    seen = set()
    for row in rows:
        rejection_ts_raw = (row.get("first_strong_rejection_ts_ms") or "").strip()
        if not rejection_ts_raw:
            continue
        asset = row["asset"]
        if asset not in ASSETS:
            raise ValueError(f"Unexpected asset in rejection ledger: {asset}")
        definition = row["definition"].lower()
        direction = row["direction"].lower()
        if definition not in EXPECTED_COHORTS or direction not in ("upper", "lower"):
            raise ValueError(f"Invalid event definition/direction: {definition}/{direction}")
        snapshot_index = int(row["snapshot_index"])
        feature_rows = features_by_asset[asset]
        if snapshot_index < 0 or snapshot_index + 1 >= len(feature_rows):
            raise ValueError(f"{asset}: snapshot index lacks current/next feature row")
        feature = feature_rows[snapshot_index]
        next_feature = feature_rows[snapshot_index + 1]
        snapshot_available = to_int_ms(row["snapshot_available_at_ts_ms"], "snapshot_available_at_ts_ms")
        snapshot_next = to_int_ms(row["snapshot_next_available_at_ts_ms"], "snapshot_next_available_at_ts_ms")
        if to_int_ms(feature["available_at_ts_ms"], "feature available_at") != snapshot_available:
            raise ValueError(f"{asset}: snapshot availability mismatch at index {snapshot_index}")
        if to_int_ms(next_feature["available_at_ts_ms"], "next feature availability") != snapshot_next:
            raise ValueError(f"{asset}: next snapshot availability mismatch at index {snapshot_index}")
        upper, lower = float(feature["upper"]), float(feature["lower"])
        width = upper - lower
        if not all(math.isfinite(v) for v in (upper, lower, width)) or width <= 0:
            raise ValueError(f"{asset}: invalid frozen channel geometry at snapshot {snapshot_index}")

        event_id = make_event_id(row)
        if event_id in seen:
            raise ValueError(f"Duplicate immutable event identity: {event_id}")
        seen.add(event_id)
        anatomy = anatomy_by_id.get(event_id)
        if anatomy is None:
            raise ValueError(f"Accepted anatomy row missing for source event: {event_id}")
        rejection_ts = to_int_ms(rejection_ts_raw, "first_strong_rejection_ts_ms")
        confirmation_ts = rejection_ts + CONFIRMATION_DELAY_MS
        if to_int_ms(anatomy["confirmation_ts_ms"], "anatomy confirmation_ts_ms") != confirmation_ts:
            raise ValueError(f"{event_id}: anatomy confirmation timestamp mismatch")
        if float(anatomy["upper"]) != upper or float(anatomy["lower"]) != lower:
            raise ValueError(f"{event_id}: anatomy frozen boundaries mismatch")

        counts[definition] += 1
        eligible.append({
            "event_id": event_id,
            "asset": asset,
            "definition": definition,
            "direction": direction,
            "snapshot_index": snapshot_index,
            "segment_id": int(row["segment_id"]),
            "test_rank": int(row["test_rank"]),
            "test_rank_group": "4+" if int(row["test_rank"]) >= 4 else str(int(row["test_rank"])),
            "test_start_ts_ms": to_int_ms(row["test_start_ts_ms"], "test_start_ts_ms"),
            "test_end_ts_ms": to_int_ms(row["test_end_ts_ms"], "test_end_ts_ms"),
            "rejection_ts_ms": rejection_ts,
            "confirmation_ts_ms": confirmation_ts,
            "snapshot_available_at_ts_ms": snapshot_available,
            "snapshot_next_available_at_ts_ms": snapshot_next,
            "upper": upper,
            "lower": lower,
            "channel_width": width,
            "rejection_open": float(anatomy["rejection_open"]),
            "rejection_high": float(anatomy["rejection_high"]),
            "rejection_low": float(anatomy["rejection_low"]),
            "rejection_close": float(anatomy["rejection_close"]),
            "rejection_range": float(anatomy["rejection_range"]),
            "rejection_body": float(anatomy["rejection_body"]),
            "rejection_upper_wick": float(anatomy["rejection_upper_wick"]),
            "rejection_lower_wick": float(anatomy["rejection_lower_wick"]),
            "body_range_ratio": optional_finite_float(anatomy["body_range_ratio"]),
            "upper_wick_range_ratio": optional_finite_float(anatomy["upper_wick_range_ratio"]),
            "lower_wick_range_ratio": optional_finite_float(anatomy["lower_wick_range_ratio"]),
            "close_location_in_range": optional_finite_float(anatomy["close_location_in_range"]),
            "range_channel_width": float(anatomy["range_channel_width"]),
            "body_channel_width": float(anatomy["body_channel_width"]),
            "upper_wick_channel_width": float(anatomy["upper_wick_channel_width"]),
            "lower_wick_channel_width": float(anatomy["lower_wick_channel_width"]),
            "zero_range_candle": anatomy["zero_range_candle"].strip().lower() == "true",
        })
    if counts != EXPECTED_COHORTS:
        raise ValueError(f"Eligible cohort counts differ: expected {EXPECTED_COHORTS}, got {dict(counts)}")
    if len(eligible) != EXPECTED_ANATOMY_ROWS or len(anatomy_by_id) != EXPECTED_ANATOMY_ROWS:
        raise ValueError("Accepted rejection cohort/anatomy row count mismatch")
    if set(seen) != set(anatomy_by_id):
        raise ValueError("Source-ledger eligible IDs and accepted anatomy IDs differ")
    return eligible


def _boundary_flags(event, bar):
    upper, lower, width = event["upper"], event["lower"], event["channel_width"]
    if event["direction"] == "upper":
        retest = bar["high"] >= upper - TOUCH_BAND * width
        separation = bar["close"] <= upper - SEPARATION_BAND * width
        close_through = bar["close"] > upper
        wick_penetration = bar["high"] > upper
        inward = max(0.0, (upper - bar["low"]) / width)
        outward = max(0.0, (bar["high"] - upper) / width)
        signed_retest_distance = (upper - bar["high"]) / width
        penetration = max(0.0, (bar["high"] - upper) / width)
        close_inward = (upper - bar["close"]) / width
        inside_to_outside = None
        outside_to_inside = None
    else:
        retest = bar["low"] <= lower + TOUCH_BAND * width
        separation = bar["close"] >= lower + SEPARATION_BAND * width
        close_through = bar["close"] < lower
        wick_penetration = bar["low"] < lower
        inward = max(0.0, (bar["high"] - lower) / width)
        outward = max(0.0, (lower - bar["low"]) / width)
        signed_retest_distance = (bar["low"] - lower) / width
        penetration = max(0.0, (lower - bar["low"]) / width)
        close_inward = (bar["close"] - lower) / width
        inside_to_outside = None
        outside_to_inside = None
    return {
        "retest": retest, "separation": separation,
        "close_through": close_through, "wick_penetration": wick_penetration,
        "inward": inward, "outward": outward,
        "signed_retest_distance": signed_retest_distance,
        "penetration": penetration, "close_inward": close_inward,
    }


def analyze_event_path(event: dict, bars: list[dict], gap_after: bool = False):
    """Pure event-path analyzer used by the real-data runner and synthetic tests."""
    direction = event["direction"]
    upper, lower, width = event["upper"], event["lower"], event["channel_width"]
    if direction not in ("upper", "lower") or width <= 0:
        raise ValueError("Invalid event direction or channel width")
    if not bars:
        raise ValueError("At least the exact confirmation-minute candle is required")
    confirmation = event["confirmation_ts_ms"]
    if bars[0]["ts"] != confirmation:
        raise ValueError("First post-confirmation bar must open exactly at confirmation")
    for previous, current in zip(bars, bars[1:]):
        if current["ts"] - previous["ts"] != MINUTE_MS:
            raise ValueError("Event bars must be consecutive; truncate before a gap")

    max_bars = min(len(bars), 1440)
    window = bars[:max_bars]
    first_retest = first_separation = first_close_through = None
    first_wick_penetration = first_reclaim = None
    inside_to_outside = outside_to_inside = 0
    max_inward = max_outward = 0.0
    episodes = []
    active = None
    close_through_seen = False
    previous_close = event["rejection_close"]

    for index, bar in enumerate(window):
        flags = _boundary_flags(event, bar)
        max_inward = max(max_inward, flags["inward"])
        max_outward = max(max_outward, flags["outward"])

        if direction == "upper":
            crossed_out = previous_close <= upper and bar["close"] > upper
            crossed_in = previous_close > upper and bar["close"] <= upper
        else:
            crossed_out = previous_close >= lower and bar["close"] < lower
            crossed_in = previous_close < lower and bar["close"] >= lower
        if crossed_out:
            inside_to_outside += 1
        if crossed_in:
            outside_to_inside += 1

        if first_wick_penetration is None and flags["wick_penetration"]:
            first_wick_penetration = bar["ts"]
        if first_separation is None and not close_through_seen and flags["separation"]:
            first_separation = bar["ts"]
        if first_close_through is None and flags["close_through"]:
            first_close_through = bar["ts"]
        had_close_through_before = close_through_seen
        if close_through_seen and first_reclaim is None and crossed_in:
            first_reclaim = bar["ts"]

        if active is not None:
            active["bar_count"] += 1
            if direction == "upper":
                if bar["high"] > active["deepest_extreme"]:
                    active["deepest_extreme"] = bar["high"]
                    active["deepest_ts_ms"] = bar["ts"]
                    active["deepest_open"] = bar["open"]
                    active["deepest_high"] = bar["high"]
                    active["deepest_low"] = bar["low"]
                    active["deepest_close"] = bar["close"]
            else:
                if bar["low"] < active["deepest_extreme"]:
                    active["deepest_extreme"] = bar["low"]
                    active["deepest_ts_ms"] = bar["ts"]
                    active["deepest_open"] = bar["open"]
                    active["deepest_high"] = bar["high"]
                    active["deepest_low"] = bar["low"]
                    active["deepest_close"] = bar["close"]
            if flags["close_through"]:
                active["resolution"] = "CLOSE_THROUGH_BOUNDARY"
                active["resolution_ts_ms"] = bar["ts"]
                active["same_bar_ambiguous"] = True
            elif flags["separation"]:
                active["resolution"] = "INWARD_SEPARATION"
                active["resolution_ts_ms"] = bar["ts"]
            if active["resolution"]:
                active["same_bar_ambiguous"] = bool(flags["retest"] and (flags["separation"] or flags["close_through"]))
                episodes.append(_finish_episode(event, active))
                active = None
        elif not had_close_through_before and flags["retest"]:
            if first_retest is None:
                first_retest = bar["ts"]
            active = {
                "episode_index": len(episodes) + 1,
                "start_ts_ms": bar["ts"],
                "start_open": bar["open"], "start_high": bar["high"],
                "start_low": bar["low"], "start_close": bar["close"],
                "deepest_ts_ms": bar["ts"],
                "deepest_extreme": bar["high"] if direction == "upper" else bar["low"],
                "deepest_open": bar["open"], "deepest_high": bar["high"],
                "deepest_low": bar["low"], "deepest_close": bar["close"],
                "bar_count": 1,
                "resolution": "",
                "resolution_ts_ms": None,
                "same_bar_ambiguous": False,
            }
            if flags["close_through"]:
                active["resolution"] = "CLOSE_THROUGH_BOUNDARY"
                active["resolution_ts_ms"] = bar["ts"]
                active["same_bar_ambiguous"] = True
            elif flags["separation"]:
                active["resolution"] = "INWARD_SEPARATION"
                active["resolution_ts_ms"] = bar["ts"]
                active["same_bar_ambiguous"] = True
            if active["resolution"]:
                episodes.append(_finish_episode(event, active))
                active = None

        if flags["close_through"]:
            close_through_seen = True
        previous_close = bar["close"]

    if active is not None:
        active["resolution"] = "HORIZON_CENSORED"
        active["resolution_ts_ms"] = window[-1]["ts"]
        active["same_bar_ambiguous"] = False
        episodes.append(_finish_episode(event, active))

    event_result = dict(event)
    event_result.update({
        "status": "COMPLETE_24H" if len(window) == 1440 else (
            "CENSORED_GAP" if gap_after else "CENSORED_SOURCE_END"
        ),
        "observed_bars_24h": len(window),
        "complete_24h": len(window) == 1440,
        "first_retest_ts_ms": first_retest,
        "first_inward_separation_ts_ms": first_separation,
        "first_wick_penetration_ts_ms": first_wick_penetration,
        "first_close_through_ts_ms": first_close_through,
        "first_reclaim_ts_ms": first_reclaim,
        "retest_episode_count": len(episodes),
        "inside_to_outside_close_cross_count": inside_to_outside,
        "outside_to_inside_close_cross_count": outside_to_inside,
        "max_inward_excursion_width": max_inward,
        "max_outward_penetration_width": max_outward,
        "terminal_close_inward_distance_width": _close_inward(event, window[-1]["close"]),
        "censor_reason": "" if len(window) == 1440 else ("GAP" if gap_after else "SOURCE_END"),
    })

    horizon_rows = []
    for horizon_name, expected in HORIZONS:
        observed = min(expected, len(window))
        sample = window[:observed]
        complete = observed == expected
        horizon_rows.append({
            "event_id": event["event_id"],
            "asset": event["asset"],
            "definition": event["definition"],
            "direction": direction,
            "test_rank_group": event["test_rank_group"],
            "horizon": horizon_name,
            "expected_bars": expected,
            "observed_bars": observed,
            "complete": complete,
            "censor_reason": "" if complete else event_result["censor_reason"],
            "max_inward_excursion_width": max(
                (_boundary_flags(event, bar)["inward"] for bar in sample), default=0.0
            ),
            "max_outward_penetration_width": max(
                (_boundary_flags(event, bar)["outward"] for bar in sample), default=0.0
            ),
            "terminal_close_inward_distance_width": _close_inward(event, sample[-1]["close"]) if sample else "",
            "first_retest_ts_ms": _first_condition_ts(event, sample, "retest"),
            "first_inward_separation_ts_ms": _first_condition_ts(event, sample, "separation"),
            "first_close_through_ts_ms": _first_condition_ts(event, sample, "close_through"),
        })
    return event_result, episodes, horizon_rows


def _close_inward(event, close):
    if event["direction"] == "upper":
        return (event["upper"] - close) / event["channel_width"]
    return (close - event["lower"]) / event["channel_width"]


def _first_condition_ts(event, bars, condition):
    failed = False
    for bar in bars:
        flags = _boundary_flags(event, bar)
        if condition == "retest" and not failed and flags["retest"]:
            return bar["ts"]
        if condition == "separation" and not failed and flags["separation"]:
            return bar["ts"]
        if condition == "close_through" and flags["close_through"]:
            return bar["ts"]
        if flags["close_through"]:
            failed = True
    return None


def _finish_episode(event, active):
    width = event["channel_width"]
    if event["direction"] == "upper":
        signed_distance = (event["upper"] - active["deepest_extreme"]) / width
        penetration = max(0.0, (active["deepest_extreme"] - event["upper"]) / width)
    else:
        signed_distance = (active["deepest_extreme"] - event["lower"]) / width
        penetration = max(0.0, (event["lower"] - active["deepest_extreme"]) / width)
    result = {
        "event_id": event["event_id"],
        "episode_id": f'{event["event_id"]}|retest|{active["episode_index"]}',
        "episode_index": active["episode_index"],
        "asset": event["asset"],
        "definition": event["definition"],
        "direction": event["direction"],
        "test_rank_group": event["test_rank_group"],
        "start_ts_ms": active["start_ts_ms"],
        "resolution_ts_ms": active["resolution_ts_ms"],
        "resolution": active["resolution"],
        "elapsed_minutes": (active["resolution_ts_ms"] - active["start_ts_ms"]) // MINUTE_MS,
        "bar_count": active["bar_count"],
        "start_open": active["start_open"], "start_high": active["start_high"],
        "start_low": active["start_low"], "start_close": active["start_close"],
        "deepest_ts_ms": active["deepest_ts_ms"],
        "deepest_open": active["deepest_open"], "deepest_high": active["deepest_high"],
        "deepest_low": active["deepest_low"], "deepest_close": active["deepest_close"],
        "signed_boundary_distance_width": signed_distance,
        "wick_penetration_width": penetration,
        "same_bar_ambiguous": active["same_bar_ambiguous"],
    }
    return result


def _quantile(values, q):
    if not values:
        return ""
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (position - lo)


def assign_overlap_clusters(event_results):
    """Assign deterministic interval-graph clusters by asset across all definitions/sides."""
    by_asset = defaultdict(list)
    for event in event_results:
        if int(event["observed_bars_24h"]) <= 0:
            raise ValueError(f'{event["event_id"]}: overlap window must contain at least one bar')
        by_asset[event["asset"]].append(event)

    mapping = {}
    largest_cluster = 0
    size_distribution = defaultdict(int)
    clusters_by_asset = {}
    for asset in ASSETS:
        ordered = sorted(
            by_asset.get(asset, []),
            key=lambda e: (int(e["confirmation_ts_ms"]), e["event_id"]),
        )
        cluster_number = 0
        active = []
        cluster_start = None
        cluster_end = None

        def finalize():
            nonlocal largest_cluster
            if not active:
                return
            size = len(active)
            largest_cluster = max(largest_cluster, size)
            size_distribution[str(size)] += 1
            cluster_id = f"{asset}|overlap|{cluster_number:04d}"
            for item in active:
                mapping[item["event_id"]] = {
                    "overlap_cluster_id": cluster_id,
                    "overlap_cluster_size": size,
                    "overlap_cluster_start_ts_ms": cluster_start,
                    "overlap_cluster_end_exclusive_ts_ms": cluster_end,
                }

        for event in ordered:
            start = int(event["confirmation_ts_ms"])
            end = start + int(event["observed_bars_24h"]) * MINUTE_MS
            if active and start >= cluster_end:
                finalize()
                active = []
                cluster_start = None
                cluster_end = None
            if not active:
                cluster_number += 1
                cluster_start = start
                cluster_end = end
            else:
                cluster_end = max(cluster_end, end)
            active.append(event)
        finalize()
        clusters_by_asset[asset] = cluster_number

    if len(mapping) != len(event_results):
        raise ValueError("Overlap clustering failed to assign every event exactly once")
    return mapping, {
        "total": sum(clusters_by_asset.values()),
        "by_asset": clusters_by_asset,
        "largest_cluster_size": largest_cluster,
        "size_distribution": dict(sorted(size_distribution.items(), key=lambda x: int(x[0]))),
    }


def build_summaries(horizon_rows):
    groups = defaultdict(list)
    for row in horizon_rows:
        key = (row["asset"], row["definition"], row["direction"], row["test_rank_group"], row["horizon"])
        groups[key].append(row)
    output = []
    for key, rows in sorted(groups.items()):
        complete = [r for r in rows if r["complete"]]
        inward = [float(r["max_inward_excursion_width"]) for r in complete]
        outward = [float(r["max_outward_penetration_width"]) for r in complete]
        terminal = [float(r["terminal_close_inward_distance_width"]) for r in complete]
        output.append({
            "asset": key[0], "definition": key[1], "direction": key[2],
            "test_rank_group": key[3], "horizon": key[4],
            "events": len(rows),
            "overlap_clusters": len({r["overlap_cluster_id"] for r in rows}),
            "complete": len(complete), "censored": len(rows) - len(complete),
            "inward_median": statistics.median(inward) if inward else "",
            "inward_p25": _quantile(inward, 0.25), "inward_p75": _quantile(inward, 0.75),
            "outward_median": statistics.median(outward) if outward else "",
            "outward_p25": _quantile(outward, 0.25), "outward_p75": _quantile(outward, 0.75),
            "terminal_close_inward_median": statistics.median(terminal) if terminal else "",
            "terminal_close_inward_p25": _quantile(terminal, 0.25),
            "terminal_close_inward_p75": _quantile(terminal, 0.75),
        })
    return output


def write_csv(path: Path, rows, fieldnames=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows and not fieldnames:
        raise ValueError(f"Field names are required for empty output: {path}")
    fields = list(rows[0].keys()) if rows else list(fieldnames)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run(root: Path, output_dir: Path):
    source_hashes = {}
    for relative, expected in EXPECTED_BLOBS.items():
        source_hashes[relative] = verify_blob(root, relative, expected)

    anatomy_path = root / "reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv"
    anatomy_rows = read_dict_rows(anatomy_path)
    anatomy_by_id = {row["event_id"]: row for row in anatomy_rows}
    if len(anatomy_by_id) != len(anatomy_rows):
        raise ValueError("Duplicate event IDs in accepted anatomy ledger")

    features_by_asset = {
        asset: load_features(root, asset) for asset in ASSETS
    }
    events = prepare_events(root, features_by_asset, anatomy_by_id)
    bars_by_asset = {
        asset: load_market_bars(root, asset) for asset in ASSETS
    }

    event_results, episode_results, horizon_results = [], [], []
    for event in events:
        bars = bars_by_asset[event["asset"]]
        timestamps = bars["ts"]
        index = bisect.bisect_left(timestamps, event["confirmation_ts_ms"])
        if index >= len(timestamps) or timestamps[index] != event["confirmation_ts_ms"]:
            raise ValueError(f'{event["event_id"]}: exact confirmation minute is missing')
        selected = []
        gap_after = False
        stop = min(index + 1440, len(timestamps))
        for i in range(index, stop):
            if i > index and timestamps[i] - timestamps[i - 1] != MINUTE_MS:
                gap_after = True
                break
            selected.append({
                "ts": timestamps[i], "open": bars["open"][i],
                "high": bars["high"][i], "low": bars["low"][i],
                "close": bars["close"][i],
            })
        event_result, episodes, horizons = analyze_event_path(event, selected, gap_after=gap_after)
        event_results.append(event_result)
        episode_results.extend(episodes)
        horizon_results.extend(horizons)

    cluster_map, cluster_summary = assign_overlap_clusters(event_results)
    for row in event_results:
        row.update(cluster_map[row["event_id"]])
    for row in episode_results:
        row.update(cluster_map[row["event_id"]])
    for row in horizon_results:
        row.update(cluster_map[row["event_id"]])

    summaries = build_summaries(horizon_results)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "rejection_lifecycle_events_v1.csv", event_results)
    write_csv(
        output_dir / "rejection_lifecycle_episodes_v1.csv",
        episode_results,
        fieldnames=[
            "event_id", "episode_id", "episode_index", "asset", "definition",
            "direction", "test_rank_group", "start_ts_ms", "resolution_ts_ms",
            "resolution", "elapsed_minutes", "bar_count", "start_open", "start_high",
            "start_low", "start_close", "deepest_ts_ms", "deepest_open", "deepest_high",
            "deepest_low", "deepest_close", "signed_boundary_distance_width",
            "wick_penetration_width", "same_bar_ambiguous",
        ],
    )
    write_csv(output_dir / "rejection_lifecycle_horizons_v1.csv", horizon_results)
    write_csv(output_dir / "rejection_lifecycle_group_summary_v1.csv", summaries)

    metadata = {
        "study": "Phase 3 Rejection Lifecycle V1",
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "protocol": "docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md",
        "protocol_amendment": "docs/research_checkpoints/2026-11-25_phase3_rejection_lifecycle_v1_1_overlap_cluster_amendment.md",
        "overlap_cluster_method": "Per-asset interval-graph connected components across all definitions and directions; half-open observed windows; strict start < running end means overlap.",
        "overlap_clusters": cluster_summary,
        "status": "DESCRIPTIVE_RUN_COMPLETE_PENDING_INDEPENDENT_CLOSEOUT",
        "assets": list(ASSETS),
        "eligible_events": len(events),
        "cohort_counts": dict(EXPECTED_COHORTS),
        "event_level_rows": len(event_results),
        "episode_rows": len(episode_results),
        "horizon_rows": len(horizon_results),
        "horizons_minutes": dict(HORIZONS),
        "confirmation_delay_ms": CONFIRMATION_DELAY_MS,
        "touch_band_fraction": TOUCH_BAND,
        "inward_separation_fraction": SEPARATION_BAND,
        "source_git_blob_ids": source_hashes,
        "market_source_rows": {
            asset: len(bars_by_asset[asset]["ts"]) for asset in ASSETS
        },
        "market_source_gap_counts": {
            asset: bars_by_asset[asset]["gap_count"] for asset in ASSETS
        },
        "output_sha256": {},
        "limitations": [
            "Descriptive event/path study only; no entries, fills, PnL or profitability inference.",
            "Strict cohort is nested within broad and is reported separately.",
            "Overlapping event windows are dependent and are not independent samples.",
            "Minute OHLC cannot establish intrabar ordering or executable fills.",
            "Incomplete horizons are censored; no gap bridging or synthetic candles.",
            "The 10% retest band and 20% separation line are inherited frozen definitions, not optimized thresholds.",
        ],
    }
    for path in sorted(output_dir.glob("*.csv")):
        metadata["output_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    (output_dir / "run_metadata_v1.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    log_lines = [
        "Phase 3 Rejection Lifecycle V1",
        f"eligible_events={len(events)}",
        f"episodes={len(episode_results)}",
        f"horizon_rows={len(horizon_results)}",
        f"overlap_clusters={cluster_summary}",
        f"market_gaps={metadata['market_source_gap_counts']}",
        "No strategy simulation or PnL was performed.",
    ]
    (output_dir / "run.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=None, help="Repository root (default: inferred from this file)")
    parser.add_argument("--output-dir", default="reports/phase3_rejection_lifecycle_v1_1")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    output_dir = (root / args.output_dir).resolve()
    metadata = run(root, output_dir)
    print(json.dumps({
        "status": metadata["status"],
        "eligible_events": metadata["eligible_events"],
        "episodes": metadata["episode_rows"],
        "horizon_rows": metadata["horizon_rows"],
        "output_dir": str(output_dir),
    }, indent=2))


if __name__ == "__main__":
    main()
