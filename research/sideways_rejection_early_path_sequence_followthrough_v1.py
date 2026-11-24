#!/usr/bin/env python3
"""Descriptive early-path sequence and strictly post-landmark follow-through V1."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from .sideways_rejection_episode_retest_anatomy_v1 import (
        ASSETS, MINUTE_MS, validate_event_ledger, load_features, load_minutes,
        resolve_feature_snapshot, first_touch,
    )
except ImportError:
    from sideways_rejection_episode_retest_anatomy_v1 import (
        ASSETS, MINUTE_MS, validate_event_ledger, load_features, load_minutes,
        resolve_feature_snapshot, first_touch,
    )

HORIZONS = {"1h": 60, "4h": 240, "24h": 1440}
CLASS_BARS = 15
BAND = 0.10
SEPARATION = 0.20


def classify_sequence(ts, op, hi, lo, cl, upper, lower, direction):
    """Classify exactly one 15-bar window; return class and first-passage indexes."""
    if len(ts) != CLASS_BARS:
        raise ValueError("classification window must contain exactly 15 bars")
    width = upper - lower
    if not np.isfinite(width) or width <= 0:
        raise ValueError("invalid channel width")
    zone = upper - BAND * width if direction == "upper" else lower + BAND * width
    sep = upper - SEPARATION * width if direction == "upper" else lower + SEPARATION * width
    retest_ix = first_touch(ts, hi, lo, zone, direction)
    mask = cl <= sep if direction == "upper" else cl >= sep
    ix = np.flatnonzero(mask)
    sep_ix = int(ix[0]) if len(ix) else None
    if retest_ix is not None and sep_ix is not None and retest_ix == sep_ix:
        label = "SAME_BAR_AMBIGUOUS"
    elif retest_ix is not None and (sep_ix is None or retest_ix < sep_ix):
        label = "RETEST_FIRST"
    elif sep_ix is not None:
        label = "SEPARATION_FIRST"
    else:
        label = "NEITHER_WITHIN_15M"
    return label, retest_ix, sep_ix


def analyze_event(event, feature, minutes):
    upper, lower = float(feature.upper), float(feature.lower)
    width = upper - lower
    if not np.isfinite(width) or width <= 0:
        raise ValueError(f"{event.event_id}: invalid frozen channel width")
    direction = event.direction
    confirmation = int(event.confirmation_ts_ms)
    all_ts = minutes.ts.to_numpy(dtype=np.int64)
    start = int(np.searchsorted(all_ts, confirmation, side="left"))
    if start >= len(all_ts) or int(all_ts[start]) != confirmation:
        raise ValueError(f"{event.event_id}: exact confirmation minute missing")
    class_expected = confirmation + np.arange(CLASS_BARS, dtype=np.int64) * MINUTE_MS
    class_ts = all_ts[start:start + CLASS_BARS]
    seq = {
        "event_id": event.event_id, "asset": event.asset, "definition": event.definition,
        "direction": direction, "snapshot_index": int(event.snapshot_index),
        "segment_id": int(event.segment_id), "test_rank": int(event.test_rank),
        "test_start_ts_ms": int(event.test_start_ts_ms),
        "first_strong_rejection_ts_ms": int(event.first_strong_rejection_ts_ms),
        "confirmation_ts_ms": confirmation, "landmark_ts_ms": confirmation + CLASS_BARS * MINUTE_MS,
        "upper": upper, "lower": lower, "channel_width": width,
        "classification_expected_bars": CLASS_BARS, "classification_observed_bars": len(class_ts),
        "classification_status": "complete", "classification_censor_reason": "",
        "sequence_class": "INCOMPLETE_CLASSIFICATION",
        "first_retest_index": np.nan, "first_retest_ts_ms": np.nan,
        "first_retest_elapsed_min": np.nan, "first_retest_close_inward": False,
        "first_separation_index": np.nan, "first_separation_ts_ms": np.nan,
        "first_separation_elapsed_min": np.nan,
    }
    if len(class_ts) != CLASS_BARS or not np.array_equal(class_ts, class_expected):
        seq["classification_status"] = "incomplete"
        seq["classification_censor_reason"] = "missing_or_irregular_classification_minute"
    else:
        w = minutes.iloc[start:start + CLASS_BARS]
        op, hi, lo, cl = (w[c].to_numpy(dtype=float) for c in ["open", "high", "low", "close"])
        label, retest_ix, sep_ix = classify_sequence(class_ts, op, hi, lo, cl, upper, lower, direction)
        seq["sequence_class"] = label
        if retest_ix is not None:
            seq.update({"first_retest_index": retest_ix,
                        "first_retest_ts_ms": int(class_ts[retest_ix]),
                        "first_retest_elapsed_min": float(retest_ix),
                        "first_retest_close_inward": bool(cl[retest_ix] < upper if direction == "upper" else cl[retest_ix] > lower)})
        if sep_ix is not None:
            seq.update({"first_separation_index": sep_ix,
                        "first_separation_ts_ms": int(class_ts[sep_ix]),
                        "first_separation_elapsed_min": float(sep_ix)})

    outcomes = []
    landmark = confirmation + CLASS_BARS * MINUTE_MS
    future_start = int(np.searchsorted(all_ts, landmark, side="left"))
    for horizon, count in HORIZONS.items():
        expected = landmark + np.arange(count, dtype=np.int64) * MINUTE_MS
        observed = all_ts[future_start:future_start + count]
        row = {"event_id": event.event_id, "asset": event.asset, "definition": event.definition,
               "direction": direction, "test_rank": int(event.test_rank),
               "confirmation_ts_ms": confirmation, "landmark_ts_ms": landmark,
               "sequence_class": seq["sequence_class"], "horizon": horizon,
               "expected_bars": count, "observed_bars": len(observed),
               "status": "complete", "censor_reason": "",
               "max_high": np.nan, "min_low": np.nan, "final_close": np.nan,
               "max_inward_excursion_width": np.nan, "max_outward_penetration_width": np.nan,
               "final_close_inward_distance_width": np.nan,
               "final_close_direction_adjusted_midpoint_width": np.nan,
               "first_future_retest_ts_ms": np.nan, "first_future_retest_elapsed_min": np.nan,
               "first_future_penetration_ts_ms": np.nan, "first_future_penetration_elapsed_min": np.nan}
        if seq["classification_status"] != "complete":
            row.update(status="not_classified", censor_reason="incomplete_classification_window")
        elif len(observed) != count:
            row.update(status="incomplete", censor_reason="insufficient_future_data")
        elif not np.array_equal(observed, expected):
            row.update(status="incomplete", censor_reason="missing_or_irregular_future_minute")
        else:
            f = minutes.iloc[future_start:future_start + count]
            op, hi, lo, cl = (f[c].to_numpy(dtype=float) for c in ["open", "high", "low", "close"])
            zone = upper - BAND * width if direction == "upper" else lower + BAND * width
            touch_ix = first_touch(observed, hi, lo, zone, direction)
            pen_mask = hi > upper if direction == "upper" else lo < lower
            pen_ixs = np.flatnonzero(pen_mask)
            pen_ix = int(pen_ixs[0]) if len(pen_ixs) else None
            max_hi, min_lo, final_close = float(hi.max()), float(lo.min()), float(cl[-1])
            midpoint = (upper + lower) / 2
            if direction == "upper":
                inward = max(0.0, (upper - min_lo) / width)
                outward = max(0.0, (max_hi - upper) / width)
                close_inward = (upper - final_close) / width
                close_mid = (midpoint - final_close) / width
            else:
                inward = max(0.0, (max_hi - lower) / width)
                outward = max(0.0, (lower - min_lo) / width)
                close_inward = (final_close - lower) / width
                close_mid = (final_close - midpoint) / width
            row.update({"max_high": max_hi, "min_low": min_lo, "final_close": final_close,
                        "max_inward_excursion_width": inward,
                        "max_outward_penetration_width": outward,
                        "final_close_inward_distance_width": close_inward,
                        "final_close_direction_adjusted_midpoint_width": close_mid,
                        "first_future_retest_ts_ms": int(observed[touch_ix]) if touch_ix is not None else np.nan,
                        "first_future_retest_elapsed_min": float(touch_ix) if touch_ix is not None else np.nan,
                        "first_future_penetration_ts_ms": int(observed[pen_ix]) if pen_ix is not None else np.nan,
                        "first_future_penetration_elapsed_min": float(pen_ix) if pen_ix is not None else np.nan})
        outcomes.append(row)
    return seq, outcomes


def build_summary(paths):
    rows = []
    dims = [("ALL", []), ("sequence_class", ["sequence_class"]),
            ("asset_sequence", ["asset", "sequence_class"]),
            ("direction_sequence", ["direction", "sequence_class"]),
            ("rank_sequence", ["test_rank_group", "sequence_class"]),
            ("month_sequence", ["confirmation_month", "sequence_class"])]
    for definition in ["broad", "strict"]:
        for horizon in HORIZONS:
            base_all = paths[(paths.definition == definition) & (paths.horizon == horizon)].copy()
            base_all["test_rank_group"] = base_all.test_rank.map(lambda n: str(int(n)) if int(n) <= 3 else "4+")
            base_all["confirmation_month"] = pd.to_datetime(base_all.confirmation_ts_ms, unit="ms", utc=True).dt.strftime("%Y-%m")
            for name, cols in dims:
                groups = [((), base_all)] if not cols else base_all.groupby(cols, dropna=False)
                for keys, g in groups:
                    if not isinstance(keys, tuple): keys = (keys,)
                    complete = g[g.status == "complete"]
                    r = {"definition": definition, "horizon": horizon, "group_dimension": name,
                         "events": len(g), "complete": len(complete),
                         "censored_or_unclassified": int((g.status != "complete").sum())}
                    for c, k in zip(cols, keys): r[c] = k
                    if name != "ALL" and "sequence_class" in cols:
                        denom_cols = [c for c in cols if c != "sequence_class"]
                        denom = len(base_all)
                        if denom_cols:
                            mask = np.ones(len(base_all), dtype=bool)
                            non_sequence_keys = [k for c, k in zip(cols, keys) if c != "sequence_class"]
                            for dc, dk in zip(denom_cols, non_sequence_keys):
                                mask &= base_all[dc].astype(str).to_numpy() == str(dk)
                            denom = int(mask.sum())
                        r["class_fraction_of_group"] = len(g) / denom if denom else np.nan
                    for metric in ["max_inward_excursion_width", "max_outward_penetration_width",
                                   "final_close_inward_distance_width", "final_close_direction_adjusted_midpoint_width"]:
                        vals = complete[metric].dropna()
                        r[f"{metric}_median"] = float(vals.median()) if len(vals) else np.nan
                        r[f"{metric}_p25"] = float(vals.quantile(.25)) if len(vals) else np.nan
                        r[f"{metric}_p75"] = float(vals.quantile(.75)) if len(vals) else np.nan
                    for metric in ["first_future_retest_elapsed_min", "first_future_penetration_elapsed_min"]:
                        vals = complete[metric].dropna()
                        r[f"{metric}_observed_n"] = len(vals)
                        r[f"{metric}_observed_fraction"] = len(vals) / len(complete) if len(complete) else np.nan
                        r[f"{metric}_median"] = float(vals.median()) if len(vals) else np.nan
                        r[f"{metric}_p25"] = float(vals.quantile(.25)) if len(vals) else np.nan
                        r[f"{metric}_p75"] = float(vals.quantile(.75)) if len(vals) else np.nan
                    rows.append(r)
    return pd.DataFrame(rows)


def run(events_path, feature_dir, minute_dir, output_dir):
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output_dir}")
    events = validate_event_ledger(events_path)
    seq_rows, path_rows, audits = [], [], []
    for asset in ASSETS:
        ae = events[events.asset == asset]
        features = load_features(feature_dir / f"{asset}_features_original_v1.csv", asset)
        minutes = load_minutes(minute_dir / f"{asset}_USDT_USDT_1m.csv", asset)
        before = len(seq_rows)
        for e in ae.itertuples(index=False):
            feature = resolve_feature_snapshot(e, features)
            s, p = analyze_event(e, feature, minutes)
            seq_rows.append(s); path_rows.extend(p)
        asset_seq = seq_rows[before:]
        audits.append({"asset": asset, "minute_rows": len(minutes), "feature_rows": len(features),
                       "source_events": len(ae), "classification_complete": sum(x["classification_status"] == "complete" for x in asset_seq),
                       "classification_incomplete": sum(x["classification_status"] != "complete" for x in asset_seq),
                       "non_60s_minute_gaps": int((np.diff(minutes.ts.to_numpy(dtype=np.int64)) != MINUTE_MS).sum()),
                       **{f"{h}_complete": int(sum(x["asset"] == asset and x["horizon"] == h and x["status"] == "complete" for x in path_rows)) for h in HORIZONS},
                       **{f"{h}_incomplete_or_unclassified": int(sum(x["asset"] == asset and x["horizon"] == h and x["status"] != "complete" for x in path_rows)) for h in HORIZONS}})
    s_df, p_df = pd.DataFrame(seq_rows), pd.DataFrame(path_rows)
    if len(s_df) != 1992 or len(p_df) != 1992 * len(HORIZONS):
        raise ValueError("Event/horizon row reconciliation failed")
    if s_df.event_id.duplicated().any() or p_df.duplicated(["event_id", "horizon"]).any():
        raise ValueError("Duplicate event output identity")
    if not (p_df.landmark_ts_ms >= p_df.confirmation_ts_ms + CLASS_BARS * MINUTE_MS).all():
        raise ValueError("Outcome landmark overlaps classification window")
    output_dir.mkdir(parents=True, exist_ok=True)
    s_df.to_csv(output_dir / "event_sequence_v1.csv", index=False)
    p_df.to_csv(output_dir / "event_followthrough_v1.csv", index=False)
    build_summary(p_df).to_csv(output_dir / "group_summary_v1.csv", index=False)
    pd.DataFrame(audits).to_csv(output_dir / "data_validation_v1.csv", index=False)
    meta = {"study": "Sideways Rejection Early-Path Sequence and Conditional Follow-Through V1",
            "execution_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "eligible_events": len(s_df), "event_horizon_rows": len(p_df),
            "cohort_counts": {k: int((s_df.definition == k).sum()) for k in ["broad", "strict"]},
            "classification_bars": CLASS_BARS, "classification_window_minutes": 15,
            "outcome_landmark_delay_minutes": 15, "boundary_touch_band_fraction": BAND,
            "inward_separation_fraction": SEPARATION, "horizons_minutes": HORIZONS,
            "limitations": ["descriptive selected-event cohort", "strict nested within broad",
                            "overlapping events are not independent", "minute OHLC cannot establish intrabar order or fills",
                            "sequence class is post-confirmation state, not randomized treatment",
                            "future outcomes begin strictly after the classification window"]}
    (output_dir / "run_metadata_v1.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {len(s_df)} events and {len(p_df)} event-horizon rows; outputs: {output_dir}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--events", type=Path, default=Path("reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv"))
    p.add_argument("--feature-dir", type=Path, default=Path("reports/sideways_detector_original_v1"))
    p.add_argument("--minute-dir", type=Path, default=Path("data/market_1m"))
    p.add_argument("--output", type=Path, default=Path("reports/sideways_rejection_early_path_sequence_followthrough_v1"))
    a = p.parse_args(); run(a.events, a.feature_dir, a.minute_dir, a.output)

if __name__ == "__main__": main()
