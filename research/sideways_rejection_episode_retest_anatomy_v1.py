#!/usr/bin/env python3
"""Descriptive sideways rejection episode/retest anatomy V1; not a trading backtest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
MINUTE_MS = 60_000
CONFIRMATION_DELAY_MS = 15 * MINUTE_MS
HORIZONS = {"15m": 15, "1h": 60, "4h": 240, "24h": 1440}
EVENT_KEY = ["asset", "definition", "direction", "snapshot_index", "segment_id", "test_rank", "test_start_ts_ms"]
EVENT_REQUIRED = EVENT_KEY + ["test_end_ts_ms", "first_strong_rejection_ts_ms", "snapshot_available_at_ts_ms", "snapshot_next_available_at_ts_ms", "rejection_open", "rejection_high", "rejection_low", "rejection_close"]
OHLC = ["open", "high", "low", "close"]
FEATURE_REQUIRED = ["available_at_ts_ms", "upper", "lower"]


def candle_anatomy(open_: float, high: float, low: float, close: float, upper: float, lower: float, direction: str) -> dict:
    vals = np.asarray([open_, high, low, close, upper, lower], dtype=float)
    if not np.isfinite(vals).all() or upper <= lower:
        raise ValueError("Non-finite candle or invalid channel bounds")
    if min(open_, high, low, close) <= 0:
        raise ValueError("Non-positive rejection candle OHLC")
    if direction not in {"upper", "lower"}:
        raise ValueError("Unknown boundary direction")
    if high < max(open_, close, low) or low > min(open_, close, high):
        raise ValueError("Invalid rejection candle OHLC")
    width = upper - lower
    rng = high - low
    body = abs(close - open_)
    uw = high - max(open_, close)
    lw = min(open_, close) - low
    denom = rng if rng > 0 else np.nan
    return {
        "channel_width": width, "rejection_range": rng, "rejection_body": body,
        "rejection_upper_wick": uw, "rejection_lower_wick": lw,
        "body_range_ratio": body / denom, "upper_wick_range_ratio": uw / denom,
        "lower_wick_range_ratio": lw / denom,
        "close_location_in_range": (close - low) / denom,
        "range_channel_width": rng / width, "body_channel_width": body / width,
        "upper_wick_channel_width": uw / width, "lower_wick_channel_width": lw / width,
        "signed_close_boundary_distance_width": ((upper - close) if direction == "upper" else (close - lower)) / width,
        "zero_range_candle": bool(rng == 0),
    }


def first_touch(ts: np.ndarray, highs: np.ndarray, lows: np.ndarray, level: float, direction: str, inclusive: bool = True):
    if direction not in {"upper", "lower"}:
        raise ValueError("Unknown boundary direction")
    mask = highs >= level if direction == "upper" else lows <= level
    ix = np.flatnonzero(mask)
    return int(ix[0]) if len(ix) else None


def first_level_revisit(highs: np.ndarray, lows: np.ndarray, level: float):
    ix = np.flatnonzero((lows <= level) & (highs >= level))
    return int(ix[0]) if len(ix) else None


def validate_event_ledger(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(set(EVENT_REQUIRED) - set(df.columns))
    if missing:
        raise ValueError(f"Event ledger missing columns: {missing}")
    df = df[df["first_strong_rejection_ts_ms"].notna()].copy()
    for col in ["snapshot_index", "segment_id", "test_rank", "test_start_ts_ms", "test_end_ts_ms", "first_strong_rejection_ts_ms", "snapshot_available_at_ts_ms", "snapshot_next_available_at_ts_ms"]:
        x = pd.to_numeric(df[col], errors="coerce")
        if x.isna().any() or (x % 1 != 0).any():
            raise ValueError(f"Invalid integer event field: {col}")
        df[col] = x.astype("int64")
    for col in ["rejection_open", "rejection_high", "rejection_low", "rejection_close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if not np.isfinite(df[col].to_numpy(dtype=float)).all():
            raise ValueError(f"Invalid rejection OHLC: {col}")
    if not set(df.asset).issubset(ASSETS) or not set(df.definition).issubset({"broad", "strict"}) or not set(df.direction).issubset({"upper", "lower"}):
        raise ValueError("Unknown asset, cohort, or direction in event ledger")
    if df.duplicated(EVENT_KEY).any():
        raise ValueError("Duplicate event identity")
    counts = df.groupby("definition").size().to_dict()
    expected = {"broad": 1154, "strict": 838}
    if counts != expected:
        raise ValueError(f"Rejection cohort count mismatch: expected {expected}, got {counts}")
    df["event_id"] = df[EVENT_KEY].astype(str).agg("|".join, axis=1)
    df["confirmation_ts_ms"] = df.first_strong_rejection_ts_ms + CONFIRMATION_DELAY_MS
    if (df.first_strong_rejection_ts_ms % (15 * MINUTE_MS) != 0).any():
        raise ValueError("Rejection candle open is not 15-minute aligned")
    if (df.confirmation_ts_ms % MINUTE_MS != 0).any():
        raise ValueError("Confirmation timestamp is not minute aligned")
    if (df.snapshot_index < 0).any() or (df.segment_id < 1).any() or (df.test_rank < 1).any():
        raise ValueError("Invalid snapshot, segment, or test-rank index")
    if (df.first_strong_rejection_ts_ms < df.test_start_ts_ms).any() or (df.first_strong_rejection_ts_ms > df.test_end_ts_ms).any():
        raise ValueError("Strong rejection timestamp falls outside its boundary-test interval")
    broad_keys = set(map(tuple, df.loc[df.definition == "broad", [c for c in EVENT_KEY if c != "definition"]].to_numpy()))
    strict_keys = set(map(tuple, df.loc[df.definition == "strict", [c for c in EVENT_KEY if c != "definition"]].to_numpy()))
    if not strict_keys.issubset(broad_keys):
        raise ValueError("Strict rejection events are not a subset of broad events")
    return df.sort_values(["asset", "definition", "confirmation_ts_ms", "event_id"]).reset_index(drop=True)


def load_features(path: Path, asset: str) -> pd.DataFrame:
    f = pd.read_csv(path)
    missing = sorted(set(FEATURE_REQUIRED) - set(f.columns))
    if missing:
        raise ValueError(f"{asset}: feature file missing {missing}")
    f["available_at_ts_ms"] = pd.to_numeric(f.available_at_ts_ms, errors="coerce")
    f[["upper", "lower"]] = f[["upper", "lower"]].apply(pd.to_numeric, errors="coerce")
    if not np.isfinite(f[FEATURE_REQUIRED].to_numpy(dtype=float)).all():
        raise ValueError(f"{asset}: non-finite feature values")
    if (f.available_at_ts_ms % 1 != 0).any() or f.available_at_ts_ms.duplicated().any() or not f.available_at_ts_ms.is_monotonic_increasing:
        raise ValueError(f"{asset}: invalid feature availability sequence")
    if (f.upper <= f.lower).any():
        raise ValueError(f"{asset}: invalid frozen channel bounds")
    return f.reset_index(drop=True)


def load_minutes(path: Path, asset: str) -> pd.DataFrame:
    m = pd.read_csv(path, usecols=["ts", *OHLC])
    m["ts"] = pd.to_numeric(m.ts, errors="coerce")
    m[OHLC] = m[OHLC].apply(pd.to_numeric, errors="coerce")
    if not np.isfinite(m[["ts", *OHLC]].to_numpy(dtype=float)).all():
        raise ValueError(f"{asset}: non-finite minute data")
    if (m.ts % MINUTE_MS != 0).any() or m.ts.duplicated().any() or not m.ts.is_monotonic_increasing:
        raise ValueError(f"{asset}: invalid minute timestamps")
    if (m[OHLC] <= 0).any().any() or (m.high < m[["open", "close", "low"]].max(axis=1)).any() or (m.low > m[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError(f"{asset}: invalid OHLC")
    m["ts"] = m.ts.astype("int64")
    return m.reset_index(drop=True)


def event_measurements(event, feature: pd.Series, minutes: pd.DataFrame) -> tuple[dict, dict]:
    upper, lower = float(feature.upper), float(feature.lower)
    width = upper - lower
    if not np.isfinite(width) or width <= 0:
        raise ValueError("Invalid channel width")
    direction = event.direction
    ro, rh, rl, rc = map(float, [event.rejection_open, event.rejection_high, event.rejection_low, event.rejection_close])
    anatomy = candle_anatomy(ro, rh, rl, rc, upper, lower, direction)
    confirmation = int(event.confirmation_ts_ms)
    ts_all = minutes.ts.to_numpy(dtype=np.int64)
    start = int(np.searchsorted(ts_all, confirmation, side="left"))
    if start >= len(ts_all) or int(ts_all[start]) != confirmation:
        raise ValueError(f"Missing exact confirmation minute for {event.event_id}")
    base_record = {
        "event_id": event.event_id, "asset": event.asset, "definition": event.definition,
        "direction": direction, "snapshot_index": int(event.snapshot_index),
        "segment_id": int(event.segment_id), "test_rank": int(event.test_rank),
        "test_start_ts_ms": int(event.test_start_ts_ms),
        "test_end_ts_ms": int(event.test_end_ts_ms),
        "closure_reason": event.closure_reason,
        "first_strong_rejection_ts_ms": int(event.first_strong_rejection_ts_ms),
        "confirmation_ts_ms": confirmation, "upper": upper, "lower": lower,
        "rejection_open": ro, "rejection_high": rh, "rejection_low": rl, "rejection_close": rc,
        "snapshot_available_at_ts_ms": int(event.snapshot_available_at_ts_ms),
        "snapshot_next_available_at_ts_ms": int(event.snapshot_next_available_at_ts_ms),
        **anatomy,
    }
    rows = []
    for horizon, count in HORIZONS.items():
        stop = start + count
        expected = confirmation + np.arange(count, dtype=np.int64) * MINUTE_MS
        observed_ts = ts_all[start:min(stop, len(ts_all))]
        status, censor = "complete", ""
        if len(observed_ts) != count:
            status, censor = "incomplete", "insufficient_future_data"
        elif not np.array_equal(observed_ts, expected):
            status, censor = "incomplete", "missing_or_irregular_minute"
        row = {
            "event_id": event.event_id, "asset": event.asset, "definition": event.definition,
            "direction": direction, "snapshot_index": int(event.snapshot_index),
            "segment_id": int(event.segment_id), "test_rank": int(event.test_rank),
            "test_start_ts_ms": int(event.test_start_ts_ms),
            "test_end_ts_ms": int(event.test_end_ts_ms),
            "first_strong_rejection_ts_ms": int(event.first_strong_rejection_ts_ms),
            "confirmation_ts_ms": confirmation, "upper": upper, "lower": lower,
            "channel_width": width, "horizon": horizon,
            "expected_bars": count, "observed_bars": len(observed_ts),
            "horizon_end_ts_ms": int(confirmation + (count - 1) * MINUTE_MS),
            "confirmation_minute_open": float(minutes.iloc[start].open),
            "status": status, "censor_reason": censor,
        }
        if status == "complete":
            w = minutes.iloc[start:stop]
            ts = w.ts.to_numpy(dtype=np.int64)
            op, hi, lo, cl = (w[c].to_numpy(dtype=float) for c in OHLC)
            zone_line = upper - 0.10 * width if direction == "upper" else lower + 0.10 * width
            separation_line = upper - 0.20 * width if direction == "upper" else lower + 0.20 * width
            zone_ix = first_touch(ts, hi, lo, zone_line, direction)
            sep_mask = cl <= separation_line if direction == "upper" else cl >= separation_line
            sep_ixs = np.flatnonzero(sep_mask)
            sep_ix = int(sep_ixs[0]) if len(sep_ixs) else None
            pen_mask = hi > upper if direction == "upper" else lo < lower
            pen_ixs = np.flatnonzero(pen_mask)
            pen_ix = int(pen_ixs[0]) if len(pen_ixs) else None
            level_ix = {name: first_level_revisit(hi, lo, level) for name, level in {
                "high": rh, "low": rl, "open": ro, "close": rc}.items()}
            def stamp(ix):
                return int(ts[ix]) if ix is not None else np.nan
            def elapsed(ix):
                return float((ts[ix] - confirmation) / MINUTE_MS) if ix is not None else np.nan
            outward = max(0.0, (np.max(hi) - upper) / width) if direction == "upper" else max(0.0, (lower - np.min(lo)) / width)
            inward = max(0.0, (upper - np.min(lo)) / width) if direction == "upper" else max(0.0, (np.max(hi) - lower) / width)
            row.update({
                "first_boundary_retest_ts_ms": stamp(zone_ix), "first_boundary_retest_elapsed_min": elapsed(zone_ix),
                "first_boundary_retest_open": float(op[zone_ix]) if zone_ix is not None else np.nan,
                "first_boundary_retest_high": float(hi[zone_ix]) if zone_ix is not None else np.nan,
                "first_boundary_retest_low": float(lo[zone_ix]) if zone_ix is not None else np.nan,
                "first_boundary_retest_close": float(cl[zone_ix]) if zone_ix is not None else np.nan,
                "retest_close_inward": bool(cl[zone_ix] < upper if direction == "upper" else cl[zone_ix] > lower) if zone_ix is not None else False,
                "first_inward_separation_ts_ms": stamp(sep_ix), "first_inward_separation_elapsed_min": elapsed(sep_ix),
                "first_inward_separation_open": float(op[sep_ix]) if sep_ix is not None else np.nan,
                "first_inward_separation_high": float(hi[sep_ix]) if sep_ix is not None else np.nan,
                "first_inward_separation_low": float(lo[sep_ix]) if sep_ix is not None else np.nan,
                "first_inward_separation_close": float(cl[sep_ix]) if sep_ix is not None else np.nan,
                "first_penetration_ts_ms": stamp(pen_ix), "first_penetration_elapsed_min": elapsed(pen_ix),
                "first_penetration_depth_width": float(((hi[pen_ix]-upper) if direction == "upper" else (lower-lo[pen_ix])) / width) if pen_ix is not None else np.nan,
                "first_penetration_open": float(op[pen_ix]) if pen_ix is not None else np.nan,
                "first_penetration_high": float(hi[pen_ix]) if pen_ix is not None else np.nan,
                "first_penetration_low": float(lo[pen_ix]) if pen_ix is not None else np.nan,
                "first_penetration_close": float(cl[pen_ix]) if pen_ix is not None else np.nan,
                "max_high": float(np.max(hi)), "min_low": float(np.min(lo)),
                "max_inward_excursion_width": float(inward), "max_outward_penetration_width": float(outward),
                "horizon_close": float(cl[-1]), "horizon_close_from_upper_width": float((cl[-1]-upper)/width),
                "horizon_close_from_lower_width": float((cl[-1]-lower)/width),
                "horizon_close_from_midpoint_width": float((cl[-1]-(upper+lower)/2)/width),
                "same_bar_retest_separation_ambiguous": bool(zone_ix is not None and sep_ix is not None and zone_ix == sep_ix),
                "retest_vs_separation_order": ("same_bar_ambiguous" if zone_ix is not None and sep_ix is not None and zone_ix == sep_ix else "retest_first" if zone_ix is not None and (sep_ix is None or zone_ix < sep_ix) else "separation_first" if sep_ix is not None else "neither"),
            })
            for name, ix in level_ix.items():
                row[f"rejection_{name}_revisit_ts_ms"] = stamp(ix)
                row[f"rejection_{name}_revisit_elapsed_min"] = elapsed(ix)
                for field, values in [("open", op), ("high", hi), ("low", lo), ("close", cl)]:
                    row[f"rejection_{name}_revisit_{field}"] = float(values[ix]) if ix is not None else np.nan
        else:
            for col in ["first_boundary_retest_ts_ms","first_boundary_retest_elapsed_min","first_boundary_retest_open","first_boundary_retest_high","first_boundary_retest_low","first_boundary_retest_close","first_inward_separation_ts_ms","first_inward_separation_elapsed_min","first_inward_separation_open","first_inward_separation_high","first_inward_separation_low","first_inward_separation_close","first_penetration_ts_ms","first_penetration_elapsed_min","first_penetration_depth_width","first_penetration_open","first_penetration_high","first_penetration_low","first_penetration_close","max_high","min_low","max_inward_excursion_width","max_outward_penetration_width","horizon_close","horizon_close_from_upper_width","horizon_close_from_lower_width","horizon_close_from_midpoint_width","rejection_high_revisit_ts_ms","rejection_low_revisit_ts_ms","rejection_open_revisit_ts_ms","rejection_close_revisit_ts_ms"] + [f"rejection_{name}_revisit_{field}" for name in ["high","low","open","close"] for field in ["open","high","low","close"]]:
                row[col] = np.nan
            row["retest_close_inward"] = False
            row["same_bar_retest_separation_ambiguous"] = False
            row["retest_vs_separation_order"] = "censored"
        rows.append(row)
    return base_record, {"rows": rows, "confirmation_minute_exists": True}


def build_summaries(paths: pd.DataFrame) -> pd.DataFrame:
    work = paths.copy()
    work["asset_group"] = work["asset"]
    work["direction_group"] = work["direction"]
    work["test_rank_group"] = work["test_rank"].map(lambda n: str(int(n)) if int(n) <= 3 else "4+")
    work["chronological_period"] = pd.to_datetime(work["confirmation_ts_ms"], unit="ms", utc=True).dt.strftime("%Y-%m")
    dimensions = [
        ("ALL", []), ("asset", ["asset_group"]), ("direction", ["direction_group"]),
        ("rank", ["test_rank_group"]), ("month", ["chronological_period"]),
        ("asset_direction", ["asset_group", "direction_group"]),
        ("asset_rank", ["asset_group", "test_rank_group"]),
        ("direction_rank", ["direction_group", "test_rank_group"]),
    ]
    metrics = [
        "first_boundary_retest_elapsed_min", "first_inward_separation_elapsed_min",
        "first_penetration_elapsed_min", "max_inward_excursion_width",
        "max_outward_penetration_width", "horizon_close_from_midpoint_width",
    ]
    rows = []
    for definition in ["broad", "strict"]:
        for horizon in HORIZONS:
            base = work[(work.definition == definition) & (work.horizon == horizon)]
            for dimension_name, cols in dimensions:
                groups = [((), base)] if not cols else base.groupby(cols, dropna=False)
                for keys, group in groups:
                    if not isinstance(keys, tuple):
                        keys = (keys,)
                    row = {
                        "definition": definition, "horizon": horizon,
                        "group_dimension": dimension_name, "events": len(group),
                        "complete": int((group.status == "complete").sum()),
                        "censored": int((group.status != "complete").sum()),
                    }
                    for col, key in zip(cols, keys):
                        row[col] = key
                    complete = group[group.status == "complete"]
                    for col in ["first_boundary_retest_elapsed_min", "first_inward_separation_elapsed_min", "first_penetration_elapsed_min"]:
                        values = complete[col].dropna()
                        row[f"{col}_observed_n"] = len(values)
                        row[f"{col}_not_observed_n"] = len(complete) - len(values)
                        row[f"{col}_observed_denominator"] = len(complete)
                        row[f"{col}_observed_fraction"] = len(values) / len(complete) if len(complete) else np.nan
                    for flag in ["retest_close_inward", "same_bar_retest_separation_ambiguous"]:
                        if flag == "retest_close_inward":
                            eligible = complete[complete.first_boundary_retest_ts_ms.notna()]
                        else:
                            eligible = complete
                        numerator = int(eligible[flag].fillna(False).astype(bool).sum())
                        row[f"{flag}_numerator"] = numerator
                        row[f"{flag}_denominator"] = len(eligible)
                        row[f"{flag}_fraction"] = numerator / len(eligible) if len(eligible) else np.nan
                    for name in ["high", "low", "open", "close"]:
                        col = f"rejection_{name}_revisit_ts_ms"
                        numerator = int(complete[col].notna().sum())
                        row[f"rejection_{name}_revisit_numerator"] = numerator
                        row[f"rejection_{name}_revisit_denominator"] = len(complete)
                        row[f"rejection_{name}_revisit_fraction"] = numerator / len(complete) if len(complete) else np.nan
                    row["censored_n"] = int((group.status != "complete").sum())
                    row["censored_denominator"] = len(group)
                    for col in metrics:
                        values = complete[col].dropna()
                        for stat, val in [
                            ("median", values.median()), ("p10", values.quantile(.1)),
                            ("p25", values.quantile(.25)), ("p75", values.quantile(.75)),
                            ("p90", values.quantile(.9)),
                        ]:
                            row[f"{col}_{stat}"] = float(val) if pd.notna(val) else np.nan
                    rows.append(row)
    return pd.DataFrame(rows)


def run(events_path: Path, feature_dir: Path, minute_dir: Path, output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output_dir}")
    events = validate_event_ledger(events_path)
    anatomy, path_rows, audits = [], [], []
    for asset in ASSETS:
        ae = events[events.asset == asset]
        if ae.empty:
            raise ValueError(f"No source events for {asset}")
        features = load_features(feature_dir / f"{asset}_features_original_v1.csv", asset)
        minutes = load_minutes(minute_dir / f"{asset}_USDT_USDT_1m.csv", asset)
        for e in ae.itertuples(index=False):
            ix = int(e.snapshot_index)
            if ix < 0 or ix >= len(features):
                raise ValueError(f"{asset}: snapshot index outside feature file")
            f = features.iloc[ix]
            next_available = int(features.iloc[ix+1].available_at_ts_ms) if ix+1 < len(features) else int(f.available_at_ts_ms) + 4*60*60*1000
            if int(f.available_at_ts_ms) != int(e.snapshot_available_at_ts_ms) or next_available != int(e.snapshot_next_available_at_ts_ms):
                raise ValueError(f"{e.event_id}: event-to-feature snapshot availability mismatch")
            if int(e.first_strong_rejection_ts_ms) < int(f.available_at_ts_ms) or int(e.first_strong_rejection_ts_ms) >= next_available:
                raise ValueError(f"{e.event_id}: rejection outside its frozen snapshot interval")
            a, result = event_measurements(e, f, minutes)
            anatomy.append(a)
            path_rows.extend(result["rows"])
        asset_rows = ae
        audits.append({
            "asset": asset, "minute_rows": len(minutes), "feature_rows": len(features),
            "broad_events": int((asset_rows.definition == "broad").sum()),
            "strict_events": int((asset_rows.definition == "strict").sum()),
            "non_60s_minute_gaps": int((np.diff(minutes.ts.to_numpy(dtype=np.int64)) != MINUTE_MS).sum()),
            "exact_confirmation_minutes": len(asset_rows),
            "snapshot_join_mismatches": 0,
            "zero_range_rejection_candles": int(sum(bool(x["zero_range_candle"]) for x in anatomy if x["asset"] == asset)),
        })
    a_df, p_df = pd.DataFrame(anatomy), pd.DataFrame(path_rows)
    if len(a_df) != 1992 or len(p_df) != 1992 * len(HORIZONS):
        raise ValueError("Event/horizon row reconciliation failed")
    if a_df.event_id.duplicated().any() or p_df.duplicated(["event_id", "horizon"]).any():
        raise ValueError("Duplicate event output identity")
    for horizon in HORIZONS:
        subset = p_df[p_df.horizon == horizon]
        if len(subset) != len(a_df) or subset.event_id.nunique() != len(a_df):
            raise ValueError(f"{horizon}: event/horizon population reconciliation failed")
        if int((subset.status == "complete").sum() + (subset.status != "complete").sum()) != len(a_df):
            raise ValueError(f"{horizon}: complete/censored reconciliation failed")
    for audit in audits:
        asset = audit["asset"]
        for horizon in HORIZONS:
            subset = p_df[(p_df.asset == asset) & (p_df.horizon == horizon)]
            audit[f"{horizon}_complete_events"] = int((subset.status == "complete").sum())
            audit[f"{horizon}_censored_events"] = int((subset.status != "complete").sum())
    output_dir.mkdir(parents=True, exist_ok=True)
    a_df.to_csv(output_dir / "event_anatomy_v1.csv", index=False)
    p_df.to_csv(output_dir / "event_path_outcomes_v1.csv", index=False)
    build_summaries(p_df).to_csv(output_dir / "group_summary_v1.csv", index=False)
    pd.DataFrame(audits).to_csv(output_dir / "data_validation_v1.csv", index=False)
    import hashlib
    from datetime import datetime, timezone
    implementation_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    metadata = {
        "study": "Sideways Rejection Episode and Retest Anatomy V1",
        "execution_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "implementation_sha256": implementation_sha256,
        "source_event_ledger_rows": int(sum(1 for _ in open(events_path, encoding="utf-8")) - 1),
        "eligible_rejection_events": len(a_df), "horizon_rows": len(p_df),
        "cohort_counts": {k: int((a_df.definition == k).sum()) for k in ["broad", "strict"]},
        "horizons_minutes": HORIZONS, "confirmation_delay_ms": CONFIRMATION_DELAY_MS,
        "boundary_touch_band_fraction": .10, "inward_separation_fraction": .20,
        "source_events": str(events_path), "feature_directory": str(feature_dir),
        "minute_directory": str(minute_dir),
        "limitations": ["Descriptive selected-event cohort only", "OHLC cannot establish intrabar order or executable fills", "Strict cohort is nested within broad", "Overlapping events are not independent", "Incomplete horizons are censored, never gap-bridged"],
    }
    (output_dir / "run_metadata_v1.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {len(a_df)} events and {len(p_df)} event-horizon rows; outputs: {output_dir}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--events", type=Path, default=Path("reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv"))
    p.add_argument("--feature-dir", type=Path, default=Path("reports/sideways_detector_original_v1"))
    p.add_argument("--minute-dir", type=Path, default=Path("data/market_1m"))
    p.add_argument("--output", type=Path, default=Path("reports/sideways_rejection_episode_retest_anatomy_v1"))
    args = p.parse_args()
    run(args.events, args.feature_dir, args.minute_dir, args.output)


if __name__ == "__main__":
    main()
