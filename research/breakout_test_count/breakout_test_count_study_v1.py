#!/usr/bin/env python3
"""Causal prior boundary-test classification for original breakout events V1.

Rebuilds the recovered original breakout detector on common 1M data, audits
its historical event counts/quantiles, then classifies only prior same-snapshot
15M touch/rejection tests. Read-only inputs; versioned outputs only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
OHLCV = ["open", "high", "low", "close", "vol"]
EXPECTED_COUNTS = {
    ("BTC", "BROAD_P40", "LOWER"): 91, ("BTC", "BROAD_P40", "UPPER"): 115,
    ("BTC", "STRICT_P25", "LOWER"): 62, ("BTC", "STRICT_P25", "UPPER"): 81,
    ("ETH", "BROAD_P40", "LOWER"): 87, ("ETH", "BROAD_P40", "UPPER"): 77,
    ("ETH", "STRICT_P25", "LOWER"): 51, ("ETH", "STRICT_P25", "UPPER"): 51,
    ("SOL", "BROAD_P40", "LOWER"): 117, ("SOL", "BROAD_P40", "UPPER"): 96,
    ("SOL", "STRICT_P25", "LOWER"): 77, ("SOL", "STRICT_P25", "UPPER"): 71,
    ("DOGE", "BROAD_P40", "LOWER"): 81, ("DOGE", "BROAD_P40", "UPPER"): 75,
    ("DOGE", "STRICT_P25", "LOWER"): 55, ("DOGE", "STRICT_P25", "UPPER"): 65,
    ("AVAX", "BROAD_P40", "LOWER"): 84, ("AVAX", "BROAD_P40", "UPPER"): 109,
    ("AVAX", "STRICT_P25", "LOWER"): 64, ("AVAX", "STRICT_P25", "UPPER"): 83,
}
EXPECTED_QUANTILES = {
    "BTC": (3.242203, 3.948630), "ETH": (4.242326, 5.481886),
    "SOL": (5.067043, 6.114542), "DOGE": (5.165724, 6.264058),
    "AVAX": (5.703625, 6.916216),
}
ZONE_FRACS = (0.05, 0.10, 0.15)
SEPARATION_FRAC = 0.20
EFFICIENCY_MAX = 0.30
OVERLAP_MIN = 0.70
FIFTEEN_MIN = pd.Timedelta(minutes=15)
SOURCE_REL = "research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py"
SOURCE_BLOB_SHA = "95d2975947c449f3813d80ee7b12008db14f071f"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def complete_bars(df: pd.DataFrame, rule: str, expected: int) -> pd.DataFrame:
    grouped = df.resample(rule, label="right", closed="left")
    bars = grouped.agg({
        "open": "first", "high": "max", "low": "min",
        "close": "last", "vol": "sum",
    })
    counts = grouped["close"].count()
    return bars.loc[counts == expected].dropna()


def overlap_ratio(high: pd.Series, low: pd.Series) -> pd.Series:
    previous_high = high.shift(1)
    previous_low = low.shift(1)
    intersection = (
        np.minimum(high, previous_high) -
        np.maximum(low, previous_low)
    ).clip(lower=0)
    smaller = np.minimum(high - low, previous_high - previous_low)
    return (intersection / smaller.replace(0, np.nan)).clip(0, 1)


def build_context(bars4: pd.DataFrame) -> pd.DataFrame:
    x = bars4.copy()
    x["upper"] = x["high"].rolling(12).max().shift(1)
    x["lower"] = x["low"].rolling(12).min().shift(1)
    x["channel_width"] = (x["upper"] / x["lower"] - 1) * 100
    net = (x["close"].shift(1) / x["close"].shift(13) - 1).abs()
    path = x["close"].pct_change().abs().rolling(12).sum().shift(1)
    x["efficiency"] = net / path.replace(0, np.nan)
    x["overlap"] = overlap_ratio(x["high"], x["low"]).rolling(12).mean().shift(1)
    return x


def load_common_data(data_dir: Path):
    data = {}
    source_hashes = {}
    source_rows = {}
    for asset in ASSETS:
        path = data_dir / f"{asset}_USDT_USDT_1m.csv"
        if not path.is_file():
            raise FileNotFoundError(path)
        df = pd.read_csv(path)
        required = {"ts", *OHLCV}
        if not required.issubset(df.columns):
            raise ValueError(f"{asset}: missing columns {sorted(required - set(df.columns))}")
        df = df[["ts", *OHLCV]].copy()
        raw_ts = pd.to_numeric(df["ts"], errors="coerce")
        if raw_ts.isna().any() or (raw_ts % 1 != 0).any():
            raise ValueError(f"{asset}: invalid millisecond timestamps")
        df["ts"] = pd.to_datetime(raw_ts.astype("int64"), unit="ms", utc=True)
        for col in OHLCV:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        if not np.isfinite(df[OHLCV].to_numpy(dtype=float)).all():
            raise ValueError(f"{asset}: non-finite OHLCV")
        if df["ts"].duplicated().any():
            raise ValueError(f"{asset}: duplicate timestamps")
        df = df.set_index("ts").sort_index()
        if not df.index.is_monotonic_increasing:
            raise ValueError(f"{asset}: timestamps not ordered")
        data[asset] = df[OHLCV]
        source_hashes[asset] = sha256_file(path)
        source_rows[asset] = len(df)

    common = data[ASSETS[0]].index
    for asset in ASSETS[1:]:
        common = common.intersection(data[asset].index)
    common = common.sort_values()
    if len(common) < 10000:
        raise ValueError(f"Common timeline unexpectedly small: {len(common)}")
    for asset in ASSETS:
        data[asset] = data[asset].reindex(common)
    return data, common, source_hashes, source_rows


def build_joined(minute: pd.DataFrame) -> pd.DataFrame:
    bars15 = complete_bars(minute, "15min", 15)
    bars4 = complete_bars(minute, "4h", 240)
    context = build_context(bars4)
    left = bars15.reset_index().rename(columns={"ts": "time", "index": "time"})
    right = context.reset_index().rename(columns={"ts": "snapshot", "index": "snapshot"})
    left = left.sort_values("time")
    right = right.sort_values("snapshot")
    joined = pd.merge_asof(
        left,
        right[["snapshot", "upper", "lower", "channel_width", "efficiency", "overlap"]],
        left_on="time", right_on="snapshot", direction="backward",
    ).set_index("time")
    return joined, bars15, bars4


def original_events(asset: str, joined: pd.DataFrame, minute: pd.DataFrame):
    widths = joined["channel_width"].dropna()
    p25 = float(widths.quantile(0.25))
    p40 = float(widths.quantile(0.40))
    definitions = {"STRICT_P25": p25, "BROAD_P40": p40}
    minute_positions = pd.Series(np.arange(len(minute)), index=minute.index)
    events = []
    counts = {}
    for definition, width_limit in definitions.items():
        sideways = (
            (joined["channel_width"] <= width_limit)
            & (joined["efficiency"] <= EFFICIENCY_MAX)
            & (joined["overlap"] >= OVERLAP_MIN)
        )
        same_snapshot = joined["snapshot"].eq(joined["snapshot"].shift(1))
        previous_close = joined["close"].shift(1)
        current_close = joined["close"]
        masks = {
            "UPPER": sideways & same_snapshot
                     & (previous_close <= joined["upper"])
                     & (current_close > joined["upper"]),
            "LOWER": sideways & same_snapshot
                     & (previous_close >= joined["lower"])
                     & (current_close < joined["lower"]),
        }
        for direction, mask in masks.items():
            signal_times = joined.index[mask.fillna(False)]
            accepted = []
            for signal_time in signal_times:
                row = joined.loc[signal_time]
                final_minute = signal_time - pd.Timedelta(minutes=1)
                pos = minute_positions.get(final_minute)
                if pd.isna(pos):
                    continue
                pos = int(pos)
                start = pos + 1
                if start + 15 > len(minute):
                    continue
                boundary = float(row["upper"] if direction == "UPPER" else row["lower"])
                if not np.isfinite(boundary) or boundary <= 0:
                    continue
                event = {
                    "asset": asset, "definition": definition,
                    "direction": direction, "signal_time": signal_time,
                    "snapshot": row["snapshot"], "boundary": boundary,
                    "upper": float(row["upper"]), "lower": float(row["lower"]),
                    "channel_width_price": float(row["upper"] - row["lower"]),
                    "channel_width_pct": float(row["channel_width"]),
                    "efficiency": float(row["efficiency"]),
                    "overlap": float(row["overlap"]),
                    "minute_signal_pos": pos,
                }
                events.append(event)
                accepted.append(event)
            counts[(asset, definition, direction)] = len(accepted)
    return events, {"P25": p25, "P40": p40}, counts


def _test_record(asset, definition, direction, zone_frac, snapshot, segment_id,
                 start_time, upper, lower, width):
    return {
        "asset": asset, "definition": definition, "direction": direction,
        "zone_pct_of_channel": zone_frac * 100,
        "snapshot": snapshot, "segment_id": segment_id,
        "test_start_time": start_time, "test_end_time": pd.NaT,
        "first_rejection_time": pd.NaT, "closure_reason": "active_at_end",
        "upper": upper, "lower": lower, "channel_width_price": width,
        "zone_width_price": zone_frac * width,
        "separation_width_price": SEPARATION_FRAC * width,
        "test_start_high": np.nan, "test_start_low": np.nan,
        "test_start_close": np.nan, "rejection_close": np.nan,
    }


def classify_events(joined: pd.DataFrame, events: list[dict], asset: str,
                    definition: str, zone_frac: float):
    """Causal event-time state machine; signal candle is classified before processing."""
    event_by_time = {}
    for event in events:
        if event["definition"] == definition:
            event_by_time.setdefault(event["signal_time"], []).append(event)

    records = {"UPPER": [], "LOWER": []}
    links = []
    event_rows = []
    active_snapshot = None
    previous_time = None
    segment_id = -1
    states = {
        d: {"active": None, "tests": []}
        for d in ("UPPER", "LOWER")
    }

    for i, (time, row) in enumerate(joined.iterrows()):
        # A breakout is classified using state accumulated strictly before this bar.
        for event in event_by_time.get(time, []):
            d = event["direction"]
            tests = states[d]["tests"]
            prior = [dict(t) for t in tests if t["test_start_time"] < time]
            rejection_tests = [
                t for t in prior
                if pd.notna(t["first_rejection_time"])
                and t["first_rejection_time"] < time
            ]
            contact_tests = [t for t in prior if t not in rejection_tests]
            n_rej = len(rejection_tests)
            group = "3+" if n_rej >= 3 else str(n_rej)
            event_row = {
                **event,
                "zone_pct_of_channel": zone_frac * 100,
                "prior_touch_test_count": len(prior),
                "prior_confirmed_rejection_count": n_rej,
                "prior_contact_only_test_count": len(contact_tests),
                "prior_rejection_group": group,
            }
            event_rows.append(event_row)
            for test in prior:
                links.append({
                    "asset": asset, "definition": definition,
                    "direction": d, "signal_time": time,
                    "zone_pct_of_channel": zone_frac * 100,
                    "test_start_time": test["test_start_time"],
                    "first_rejection_time": test["first_rejection_time"],
                    "test_end_time": test["test_end_time"],
                    "closure_reason": test["closure_reason"],
                    "test_status_at_breakout": (
                        "confirmed_rejection" if pd.notna(test["first_rejection_time"])
                        and test["first_rejection_time"] < time else "contact_only"
                    ),
                    "upper": test["upper"], "lower": test["lower"],
                    "channel_width_price": test["channel_width_price"],
                    "zone_width_price": test["zone_width_price"],
                    "separation_width_price": test["separation_width_price"],
                })

        snapshot = row["snapshot"]
        valid_context = (
            pd.notna(snapshot) and np.isfinite(row["upper"])
            and np.isfinite(row["lower"]) and row["upper"] > row["lower"]
            and bool(
                (row["channel_width"] <= (
                    EXPECTED_QUANTILES[asset][0] if definition == "STRICT_P25"
                    else EXPECTED_QUANTILES[asset][1]
                ))
                and (row["efficiency"] <= EFFICIENCY_MAX)
                and (row["overlap"] >= OVERLAP_MIN)
            )
        )
        gap = previous_time is not None and time - previous_time != FIFTEEN_MIN
        snapshot_change = active_snapshot is not None and snapshot != active_snapshot
        if gap or snapshot_change or not valid_context:
            for d in states:
                states[d] = {"active": None, "tests": []}
            if valid_context:
                segment_id += 1
        elif valid_context and (active_snapshot is None or previous_time is None):
            segment_id += 1

        if not valid_context:
            active_snapshot = None
            previous_time = time
            continue

        upper = float(row["upper"])
        lower = float(row["lower"])
        width = upper - lower
        if not np.isfinite(width) or width <= 0:
            for d in states:
                states[d] = {"active": None, "tests": []}
            active_snapshot = None
            previous_time = time
            continue

        for direction in ("UPPER", "LOWER"):
            state = states[direction]
            active = state["active"]
            if direction == "UPPER":
                touch = float(row["high"]) >= upper - zone_frac * width
                rejection = touch and float(row["close"]) < upper - zone_frac * width and float(row["close"]) > lower
                separated = (not touch) and float(row["close"]) <= upper - SEPARATION_FRAC * width
            else:
                touch = float(row["low"]) <= lower + zone_frac * width
                rejection = touch and float(row["close"]) > lower + zone_frac * width and float(row["close"]) < upper
                separated = (not touch) and float(row["close"]) >= lower + SEPARATION_FRAC * width

            if active is None:
                if touch:
                    active = _test_record(
                        asset, definition, direction, zone_frac, snapshot,
                        segment_id, time, upper, lower, width
                    )
                    active["test_start_high"] = float(row["high"])
                    active["test_start_low"] = float(row["low"])
                    active["test_start_close"] = float(row["close"])
                    state["tests"].append(active)
                    state["active"] = active
            else:
                if rejection and pd.isna(active["first_rejection_time"]):
                    active["first_rejection_time"] = time
                    active["rejection_close"] = float(row["close"])
                if separated:
                    active["test_end_time"] = time
                    active["closure_reason"] = "separated"
                    state["active"] = None

        active_snapshot = snapshot
        previous_time = time

    return pd.DataFrame(event_rows), pd.DataFrame(links)


def group_summary(classifications: pd.DataFrame) -> pd.DataFrame:
    cols = ["asset", "definition", "direction", "zone_pct_of_channel", "prior_rejection_group"]
    if classifications.empty:
        return pd.DataFrame(columns=cols + ["event_count", "share_within_stratum_pct"])
    grouped = classifications.groupby(cols, dropna=False).size().rename("event_count").reset_index()
    totals = classifications.groupby(
        ["asset", "definition", "direction", "zone_pct_of_channel"]
    ).size().rename("stratum_event_count").reset_index()
    grouped = grouped.merge(totals, on=cols[:-1], how="left")
    grouped["share_within_stratum_pct"] = (
        grouped["event_count"] / grouped["stratum_event_count"] * 100
    )
    return grouped.sort_values(cols).reset_index(drop=True)


def run(data_dir: Path, output_dir: Path):
    if output_dir.exists():
        if not output_dir.is_dir() or any(output_dir.iterdir()):
            raise FileExistsError(f"Refusing non-empty/existing output path: {output_dir}")
        raise FileExistsError(f"Refusing pre-existing output directory: {output_dir}")
    data, common, source_hashes, source_rows = load_common_data(data_dir)
    joined_by_asset = {}
    bars_audit = {}
    all_events = []
    all_quantiles = {}
    reproduced_counts = {}
    for asset in ASSETS:
        joined, bars15, bars4 = build_joined(data[asset])
        joined_by_asset[asset] = joined
        bars_audit[asset] = {
            "complete_15m_bars": len(bars15), "complete_4h_bars": len(bars4),
            "joined_15m_rows": len(joined),
            "joined_15m_gaps": int((joined.index.to_series().diff().dropna() != FIFTEEN_MIN).sum()),
        }
        events, quantiles, counts = original_events(asset, joined, data[asset])
        all_events.extend(events)
        all_quantiles[asset] = quantiles
        reproduced_counts.update(counts)

    count_mismatches = []
    for key, expected in EXPECTED_COUNTS.items():
        actual = reproduced_counts.get(key, 0)
        if actual != expected:
            count_mismatches.append({"key": "|".join(key), "expected": expected, "actual": actual})
    quantile_mismatches = []
    for asset, (p25, p40) in EXPECTED_QUANTILES.items():
        actual = all_quantiles[asset]
        for name, expected in (("P25", p25), ("P40", p40)):
            value = actual[name]
            if not np.isclose(value, expected, rtol=0, atol=0.0000005):
                quantile_mismatches.append({
                    "asset": asset, "quantile": name, "expected": expected, "actual": value
                })
    if count_mismatches or quantile_mismatches:
        raise RuntimeError(
            "Original breakout reproduction gate FAILED. "
            f"Count mismatches={count_mismatches}; quantile mismatches={quantile_mismatches}"
        )

    # Strict must be a subset of broad for each asset/direction/signal close.
    strict_keys = {
        (e["asset"], e["direction"], e["signal_time"])
        for e in all_events if e["definition"] == "STRICT_P25"
    }
    broad_keys = {
        (e["asset"], e["direction"], e["signal_time"])
        for e in all_events if e["definition"] == "BROAD_P40"
    }
    if not strict_keys.issubset(broad_keys):
        raise RuntimeError("Strict event set is not a subset of broad event set.")

    classifications = []
    link_frames = []
    for asset in ASSETS:
        joined = joined_by_asset[asset]
        asset_events = [e for e in all_events if e["asset"] == asset]
        for definition in ("STRICT_P25", "BROAD_P40"):
            for zone in ZONE_FRACS:
                c, l = classify_events(joined, asset_events, asset, definition, zone)
                if not c.empty:
                    classifications.append(c)
                if not l.empty:
                    link_frames.append(l)

    class_df = pd.concat(classifications, ignore_index=True) if classifications else pd.DataFrame()
    links_df = pd.concat(link_frames, ignore_index=True) if link_frames else pd.DataFrame()
    summary_df = group_summary(class_df)

    # Event-time causality and linkage reconciliation.
    if not class_df.empty:
        if not (class_df["prior_confirmed_rejection_count"] <= class_df["prior_touch_test_count"]).all():
            raise RuntimeError("Rejection count exceeds prior touch-test count.")
        if not (
            class_df["prior_touch_test_count"]
            == class_df["prior_confirmed_rejection_count"] + class_df["prior_contact_only_test_count"]
        ).all():
            raise RuntimeError("Per-event touch/rejection/contact-only counts do not reconcile.")
        if not (class_df["signal_time"] > class_df["snapshot"]).all():
            raise RuntimeError("Breakout signal timestamp is not after its snapshot availability.")
        if not links_df.empty and not (links_df["test_start_time"] < links_df["signal_time"]).all():
            raise RuntimeError("A prior test starts at/after breakout close.")
        if not links_df.empty:
            bad_rej = links_df["first_rejection_time"].notna() & (
                links_df["first_rejection_time"] >= links_df["signal_time"]
            )
            if bad_rej.any():
                raise RuntimeError("A rejection is not strictly prior to breakout close.")

    output_dir.mkdir(parents=True, exist_ok=False)
    class_df.to_csv(output_dir / "breakout_prior_test_classifications_v1.csv", index=False)
    links_df.to_csv(output_dir / "breakout_prior_test_links_v1.csv", index=False)
    summary_df.to_csv(output_dir / "breakout_prior_test_group_counts_v1.csv", index=False)

    audit_rows = []
    for asset in ASSETS:
        audit_rows.append({
            "asset": asset, "source_1m_rows": source_rows[asset],
            "common_1m_rows": len(common), **bars_audit[asset],
            "original_P25": all_quantiles[asset]["P25"],
            "original_P40": all_quantiles[asset]["P40"],
            "original_counts_reproduced": True,
            "strict_subset_broad": True,
            "source_sha256": source_hashes[asset],
        })
    pd.DataFrame(audit_rows).to_csv(output_dir / "reconstruction_audit_v1.csv", index=False)

    metadata = {
        "study": "breakout_prior_test_count_study_v1",
        "specification": "docs/research_checkpoints/2026-11-24_breakout_prior_test_count_study_spec_v1.md",
        "original_source": SOURCE_REL, "original_source_git_blob_sha": SOURCE_BLOB_SHA,
        "assets": ASSETS, "common_1m_timestamps": len(common),
        "timestamp_convention": "15M and 4H bars label=right, closed=left; labels are close times",
        "zones_pct_of_channel": [z * 100 for z in ZONE_FRACS],
        "separation_pct_of_channel": SEPARATION_FRAC * 100,
        "expected_counts_reproduced": 20, "expected_quantiles_reproduced": 10,
        "classification_rows": len(class_df), "prior_test_link_rows": len(links_df),
        "strict_events_are_subset_of_broad": True,
        "limitations": [
            "Descriptive classification only; no forward outcomes or strategy inference.",
            "Strict/broad and zone variants overlap and are not independent samples.",
            "Full-sample width quantiles are retrospective.",
            "Volume is excluded because source units are unverified.",
        ],
        "source_sha256": source_hashes,
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print("PASS: original breakout counts 20/20 and quantiles 10/10 reproduced.")
    print(f"Common 1M timestamps: {len(common):,}")
    print(f"Classification rows: {len(class_df):,}; prior-test links: {len(links_df):,}")
    print(f"Reports: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path.home() / "okx_scalping_data")
    parser.add_argument("--output-dir", type=Path, default=Path.home() / "okxtester" /
                        "reports" / "breakout_prior_test_count_v1")
    args = parser.parse_args()
    run(args.data_dir, args.output_dir)


if __name__ == "__main__":
    main()
