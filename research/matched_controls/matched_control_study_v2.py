#!/usr/bin/env python3
"""Matched breakout versus near-boundary non-breakout controls, V2.

Rebuilds the accepted breakout events from the recovered original source
methodology, gates on all 20 counts and 10 thresholds, then performs the
frozen V2 matching and descriptive outcome analysis.

Read-only with respect to market data. Prints results to stdout; writes no files.
"""

from __future__ import annotations

from pathlib import Path
import math
import sys

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
BASE = Path.home() / "okx_scalping_data"
HORIZONS = {"15M": 15, "1H": 60, "4H": 240, "12H": 720}
EFFICIENCY_MAX = 0.30
OVERLAP_MIN = 0.70
CONTROL_BAND_PCT = 0.10
MAX_DISTANCE = 2.0
BOOTSTRAP_REPS = 2000
BOOTSTRAP_SEED = 20261123
BLOCK_DAYS = 7
FEATURES = [
    "boundary_distance_pct",
    "range_percentile",
    "channel_width_pct",
    "efficiency",
    "realized_abs_move_1h_pct",
]
ALL_FEATURES = FEATURES + ["calendar_time_days"]
EXPECTED = {
    ("BTC", "STRICT_P25", "LOWER"): 62,
    ("BTC", "STRICT_P25", "UPPER"): 81,
    ("BTC", "BROAD_P40", "LOWER"): 91,
    ("BTC", "BROAD_P40", "UPPER"): 115,
    ("ETH", "STRICT_P25", "LOWER"): 51,
    ("ETH", "STRICT_P25", "UPPER"): 51,
    ("ETH", "BROAD_P40", "LOWER"): 87,
    ("ETH", "BROAD_P40", "UPPER"): 77,
    ("SOL", "STRICT_P25", "LOWER"): 77,
    ("SOL", "STRICT_P25", "UPPER"): 71,
    ("SOL", "BROAD_P40", "LOWER"): 117,
    ("SOL", "BROAD_P40", "UPPER"): 96,
    ("DOGE", "STRICT_P25", "LOWER"): 55,
    ("DOGE", "STRICT_P25", "UPPER"): 65,
    ("DOGE", "BROAD_P40", "LOWER"): 81,
    ("DOGE", "BROAD_P40", "UPPER"): 75,
    ("AVAX", "STRICT_P25", "LOWER"): 64,
    ("AVAX", "STRICT_P25", "UPPER"): 83,
    ("AVAX", "BROAD_P40", "LOWER"): 84,
    ("AVAX", "BROAD_P40", "UPPER"): 109,
}
EXPECTED_THRESHOLDS = {
    "BTC": (3.242203, 3.948630),
    "ETH": (4.242326, 5.481886),
    "SOL": (5.067043, 6.114542),
    "DOGE": (5.165724, 6.264058),
    "AVAX": (5.703625, 6.916216),
}


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


def load_market_data() -> tuple[dict[str, pd.DataFrame], pd.DatetimeIndex]:
    data: dict[str, pd.DataFrame] = {}
    for asset in ASSETS:
        path = BASE / f"{asset}_USDT_USDT_1m.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        df = pd.read_csv(path)
        required = {"ts", "open", "high", "low", "close", "vol"}
        if not required.issubset(df.columns):
            raise ValueError(f"{asset}: missing required columns {sorted(required - set(df.columns))}")
        df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        df = df.set_index("ts").sort_index()
        if df.index.has_duplicates:
            raise ValueError(f"{asset}: duplicate minute timestamps")
        data[asset] = df[["open", "high", "low", "close", "vol"]].astype(float)

    common = data[ASSETS[0]].index
    for asset in ASSETS[1:]:
        common = common.intersection(data[asset].index)
    common = common.sort_values()
    if len(common) < 10000:
        raise ValueError(f"Common minute intersection unexpectedly small: {len(common)}")
    expected_step = pd.Timedelta(minutes=1)
    # Pandas 3 may retain a millisecond-resolution DatetimeIndex after unit="ms".
    # Normalize integer timestamps to nanoseconds before comparing with Timedelta.value.
    common_ns = common.as_unit("ns").asi8
    gaps = np.flatnonzero(np.diff(common_ns) != expected_step.value)
    if len(gaps):
        raise ValueError(
            f"Common minute index has {len(gaps)} gaps; first gap "
            f"{common[gaps[0]]} -> {common[gaps[0] + 1]}. Refusing to bridge gaps."
        )
    for asset in ASSETS:
        data[asset] = data[asset].reindex(common)
    return data, common


def build_joined(minute: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    bars15 = complete_bars(minute, "15min", 15)
    bars4 = complete_bars(minute, "4h", 240)
    context = build_context(bars4)

    left = bars15.reset_index().rename(columns={"ts": "time", bars15.index.name or "index": "time"})
    if "time" not in left.columns:
        left = left.rename(columns={left.columns[0]: "time"})
    right = context.reset_index()
    right = right.rename(columns={right.columns[0]: "snapshot"})
    left = left.sort_values("time")
    right = right.sort_values("snapshot")
    joined = pd.merge_asof(
        left,
        right[["snapshot", "upper", "lower", "channel_width", "efficiency", "overlap"]],
        left_on="time", right_on="snapshot", direction="backward"
    ).set_index("time")

    widths = joined["channel_width"].dropna()
    p25 = float(widths.quantile(0.25))
    p40 = float(widths.quantile(0.40))
    return joined, p25, p40


def finite_features(values: list[float]) -> bool:
    return bool(np.all(np.isfinite(np.asarray(values, dtype=float))))


def candidate_outcomes(
    candidate: dict,
    minute: pd.DataFrame,
    opens: np.ndarray,
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    boundary: float,
) -> dict:
    start = candidate["start_pos"]
    entry = float(opens[start])
    direction = candidate["direction"]
    out: dict[str, float | bool] = {}
    for horizon, minutes in HORIZONS.items():
        w_hi = highs[start:start + minutes]
        w_lo = lows[start:start + minutes]
        w_cl = closes[start:start + minutes]
        if direction == "UPPER":
            mfe = (float(np.max(w_hi)) / entry - 1) * 100
            mae = (float(np.min(w_lo)) / entry - 1) * 100
            net = (float(w_cl[-1]) / entry - 1) * 100
            return_inside = bool(np.any(w_cl < boundary))
            ending_inside = bool(w_cl[-1] < boundary)
            same_direction_break = bool(np.any(w_cl > boundary))
            threshold_values = (w_hi / entry - 1) * 100
        else:
            mfe = (entry / float(np.min(w_lo)) - 1) * 100
            mae = (entry / float(np.max(w_hi)) - 1) * 100
            net = (entry / float(w_cl[-1]) - 1) * 100
            return_inside = bool(np.any(w_cl > boundary))
            ending_inside = bool(w_cl[-1] > boundary)
            same_direction_break = bool(np.any(w_cl < boundary))
            threshold_values = (entry / w_lo - 1) * 100

        out[f"{horizon}_mfe_pct"] = mfe
        out[f"{horizon}_mae_pct"] = mae
        out[f"{horizon}_net_pct"] = net
        out[f"{horizon}_return_inside"] = return_inside
        out[f"{horizon}_ending_inside"] = ending_inside
        out[f"{horizon}_same_direction_break"] = same_direction_break
        for threshold in (0.25, 0.5, 1.0, 1.5, 2.0):
            hit = np.flatnonzero(threshold_values >= threshold)
            out[f"{horizon}_hit_{threshold:g}pct"] = bool(len(hit))
            out[f"{horizon}_minutes_to_{threshold:g}pct"] = (
                int(hit[0] + 1) if len(hit) else np.nan
            )
    return out


def main() -> None:
    print("=" * 88)
    print("MATCHED BREAKOUT VS NEAR-BOUNDARY CONTROL STUDY V2")
    print("FIVE ASSETS | STRICT + BROAD | UPPER + LOWER | READ ONLY")
    print("=" * 88)
    print("Loading five 1-minute datasets and building their common intersection...")
    data, common = load_market_data()
    print(f"Common 1M timestamps: {len(common):,} | {common[0]} through {common[-1]}")
    print("VOLUME ANALYSIS NOT RUN: volume units not verified.")

    all_candidates: list[dict] = []
    gate_rows: list[dict] = []
    threshold_rows: list[dict] = []
    minute_arrays: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}

    # Stage A: reproduce original event engine and all accepted counts first.
    for asset in ASSETS:
        minute = data[asset]
        joined, p25, p40 = build_joined(minute)
        threshold_rows.append({
            "asset": asset,
            "p25_actual": p25,
            "p25_expected": EXPECTED_THRESHOLDS[asset][0],
            "p40_actual": p40,
            "p40_expected": EXPECTED_THRESHOLDS[asset][1],
        })
        definitions = {"STRICT_P25": p25, "BROAD_P40": p40}
        minute_index = minute.index
        minute_positions = pd.Series(np.arange(len(minute)), index=minute_index)
        opens = minute["open"].to_numpy(dtype=float)
        highs = minute["high"].to_numpy(dtype=float)
        lows = minute["low"].to_numpy(dtype=float)
        closes = minute["close"].to_numpy(dtype=float)
        minute_arrays[asset] = (opens, highs, lows, closes)

        for definition, width_limit in definitions.items():
            sideways = (
                (joined["channel_width"] <= width_limit) &
                (joined["efficiency"] <= EFFICIENCY_MAX) &
                (joined["overlap"] >= OVERLAP_MIN)
            )
            same_snapshot = joined["snapshot"].eq(joined["snapshot"].shift(1))
            previous_close = joined["close"].shift(1)
            current_close = joined["close"]
            masks = {
                "UPPER": (
                    sideways & same_snapshot &
                    (previous_close <= joined["upper"]) &
                    (current_close > joined["upper"])
                ),
                "LOWER": (
                    sideways & same_snapshot &
                    (previous_close >= joined["lower"]) &
                    (current_close < joined["lower"])
                ),
            }

            # Common eligible sideways population for range percentile.
            eligible_sideways = sideways & same_snapshot
            ranges = (
                (joined["high"] - joined["low"]) /
                joined["close"].shift(1).replace(0, np.nan) * 100
            )
            valid_ranges = ranges.loc[eligible_sideways].replace([np.inf, -np.inf], np.nan).dropna()
            if valid_ranges.empty:
                raise RuntimeError(f"{asset}/{definition}: no valid eligible sideways ranges")
            range_sorted = np.sort(valid_ranges.to_numpy(dtype=float))

            for direction in ("UPPER", "LOWER"):
                signal_times = joined.index[masks[direction].fillna(False)]
                gate_rows.append({
                    "asset": asset, "definition": definition,
                    "direction": direction, "count": int(len(signal_times)),
                    "expected": EXPECTED[(asset, definition, direction)],
                })

                # Candidate universe includes breakout signals and eligible controls.
                breakout_time_set = set(signal_times)
                control_mask = eligible_sideways.copy()
                if direction == "UPPER":
                    control_mask &= (
                        (joined["close"] <= joined["upper"]) &
                        (joined["close"] >= joined["upper"] * (1 - CONTROL_BAND_PCT / 100))
                    )
                else:
                    control_mask &= (
                        (joined["close"] >= joined["lower"]) &
                        (joined["close"] <= joined["lower"] * (1 + CONTROL_BAND_PCT / 100))
                    )
                control_times = joined.index[control_mask.fillna(False)]
                control_time_set = set(control_times) - breakout_time_set

                for role, times in (("BREAKOUT", signal_times), ("CONTROL", control_times)):
                    for signal_time in times:
                        row = joined.loc[signal_time]
                        boundary = float(row["upper"] if direction == "UPPER" else row["lower"])
                        if not np.isfinite(boundary) or boundary <= 0:
                            continue
                        last_signal_minute = signal_time - pd.Timedelta(minutes=1)
                        signal_pos = minute_positions.get(last_signal_minute)
                        if pd.isna(signal_pos):
                            continue
                        signal_pos = int(signal_pos)
                        start = signal_pos + 1
                        # Require all four uninterrupted forward horizons.
                        if start + max(HORIZONS.values()) > len(minute):
                            continue
                        if minute.index[start] != signal_time:
                            continue
                        # Recent 1H absolute close-to-close movement: 60 completed
                        # one-minute returns ending at the final pre-signal minute.
                        if signal_pos < 60:
                            continue
                        recent = closes[signal_pos - 59:signal_pos + 1]
                        previous = closes[signal_pos - 60:signal_pos]
                        returns = np.abs(recent / previous - 1) * 100
                        realized_1h = float(np.sum(returns))
                        if role == "BREAKOUT":
                            distance = (
                                (boundary - float(row["close"])) / boundary * 100
                                if direction == "UPPER"
                                else (float(row["close"]) - boundary) / boundary * 100
                            )
                        else:
                            distance = (
                                (boundary - float(row["close"])) / boundary * 100
                                if direction == "UPPER"
                                else (float(row["close"]) - boundary) / boundary * 100
                            )
                        candle_range = float(ranges.loc[signal_time])
                        percentile = float(np.searchsorted(
                            range_sorted, candle_range, side="right"
                        ) / len(range_sorted) * 100) if np.isfinite(candle_range) else np.nan
                        features = [
                            distance, percentile, float(row["channel_width"]),
                            float(row["efficiency"]), realized_1h,
                        ]
                        if not finite_features(features):
                            continue
                        # Breakout signal timestamp must not be used as a control
                        # in the same exact stratum.
                        if role == "CONTROL" and signal_time in breakout_time_set:
                            continue
                        all_candidates.append({
                            "asset": asset,
                            "definition": definition,
                            "direction": direction,
                            "role": role,
                            "time": signal_time,
                            "boundary": boundary,
                            "start_pos": start,
                            "features": np.asarray(features, dtype=float),
                        })

    gate = pd.DataFrame(gate_rows)
    thresholds = pd.DataFrame(threshold_rows)
    print("\n===== MANDATORY ORIGINAL EVENT-COUNT GATE =====")
    print(gate.to_string(index=False))
    print("\n===== ORIGINAL JOINED-15M WIDTH THRESHOLDS =====")
    print(thresholds.to_string(index=False, float_format=lambda x: f"{x:.9f}"))

    count_failures = gate[gate["count"] != gate["expected"]]
    threshold_failures = []
    for row in threshold_rows:
        if not math.isclose(row["p25_actual"], row["p25_expected"], rel_tol=0, abs_tol=0.0000005):
            threshold_failures.append((row["asset"], "P25", row["p25_actual"], row["p25_expected"]))
        if not math.isclose(row["p40_actual"], row["p40_expected"], rel_tol=0, abs_tol=0.0000005):
            threshold_failures.append((row["asset"], "P40", row["p40_actual"], row["p40_expected"]))
    if len(gate) != 20 or len(count_failures) or threshold_failures:
        print("\nSTOP: ORIGINAL EVENT REPRODUCTION GATE FAILED.")
        if len(count_failures):
            print("Count mismatches:")
            print(count_failures.to_string(index=False))
        if threshold_failures:
            print("Threshold mismatches:", threshold_failures)
        print("No matching or outcome analysis was performed.")
        raise SystemExit(2)

    print("\nPASS: all 20 original event counts and all 10 thresholds reproduced.")
    print("Proceeding to matched-control eligibility and matching.")

    # Stage B: pooled standardization and greedy matching per exact stratum.
    candidate_frame = pd.DataFrame(all_candidates)
    if candidate_frame.empty:
        raise RuntimeError("No eligible candidates after complete-follow-up/covariate checks.")
    matched_pairs: list[dict] = []
    stratum_audits: list[dict] = []
    pair_feature_rows: list[dict] = []

    for key, group in candidate_frame.groupby(["asset", "definition", "direction"], sort=True):
        breakouts = group[group["role"] == "BREAKOUT"].copy().sort_values("time")
        controls = group[group["role"] == "CONTROL"].copy().sort_values("time")
        if breakouts.empty or controls.empty:
            stratum_audits.append({
                "asset": key[0], "definition": key[1], "direction": key[2],
                "breakout_candidates": len(breakouts), "control_candidates": len(controls),
                "matched_pairs": 0, "unmatched_breakouts": len(breakouts),
                "unused_controls": len(controls), "status": "NO PAIRABLE CANDIDATES",
            })
            continue

        pooled = np.vstack([
            np.vstack(breakouts["features"].to_numpy()),
            np.vstack(controls["features"].to_numpy()),
        ])
        time_origin = min(breakouts["time"].min(), controls["time"].min())
        b_days = (breakouts["time"] - time_origin).dt.total_seconds().to_numpy() / 86400.0
        c_days = (controls["time"] - time_origin).dt.total_seconds().to_numpy() / 86400.0
        pooled_days = np.concatenate([b_days, c_days])
        means = np.concatenate([np.mean(pooled, axis=0), [float(np.mean(pooled_days))]])
        stds = np.concatenate([np.std(pooled, axis=0, ddof=0), [float(np.std(pooled_days, ddof=0))]])
        scale_ok = np.isfinite(stds) & (stds > np.finfo(float).eps * np.maximum(1.0, np.abs(means)))
        if not np.all(scale_ok):
            bad = [ALL_FEATURES[i] for i, ok in enumerate(scale_ok) if not ok]
            stratum_audits.append({
                "asset": key[0], "definition": key[1], "direction": key[2],
                "breakout_candidates": len(breakouts), "control_candidates": len(controls),
                "matched_pairs": 0, "unmatched_breakouts": len(breakouts),
                "unused_controls": len(controls), "status": "STOPPED: unusable scale " + ",".join(bad),
            })
            print(f"\nSTOP MATCHING STRATUM {key}: unusable scale for {bad}")
            continue

        b_raw = np.vstack(breakouts["features"].to_numpy())
        c_raw = np.vstack(controls["features"].to_numpy())
        b_z = (b_raw - means[:5]) / stds[:5]
        c_z = (c_raw - means[:5]) / stds[:5]
        b_time_z = (b_days - means[5]) / stds[5]
        c_time_z = (c_days - means[5]) / stds[5]

        # Full pairwise distance matrix; all candidate pairs are evaluated.
        delta = b_z[:, None, :] - c_z[None, :, :]
        distance_sq = np.sum(delta * delta, axis=2)
        time_delta = b_time_z[:, None] - c_time_z[None, :]
        distance = np.sqrt(distance_sq + time_delta * time_delta)
        bi, ci = np.indices(distance.shape)
        flat_d = distance.ravel()
        flat_b = bi.ravel()
        flat_c = ci.ravel()
        b_ns = breakouts["time"].astype("int64").to_numpy()
        c_ns = controls["time"].astype("int64").to_numpy()
        order = np.lexsort((c_ns[flat_c], b_ns[flat_b], flat_d))

        used_b: set[int] = set()
        used_c: set[int] = set()
        accepted = 0
        for ix in order:
            d = float(flat_d[ix])
            if d > MAX_DISTANCE:
                break
            ib = int(flat_b[ix])
            ic = int(flat_c[ix])
            if ib in used_b or ic in used_c:
                continue
            used_b.add(ib)
            used_c.add(ic)
            b_row = breakouts.iloc[ib]
            c_row = controls.iloc[ic]
            pair_id = f"{key[0]}|{key[1]}|{key[2]}|{accepted + 1:04d}"
            matched_pairs.append({
                "pair_id": pair_id, "asset": key[0], "definition": key[1],
                "direction": key[2], "breakout": b_row.to_dict(),
                "control": c_row.to_dict(), "distance": d,
                "calendar_gap_hours": abs((b_row["time"] - c_row["time"]).total_seconds()) / 3600,
                "calendar_gap_days": abs((b_row["time"] - c_row["time"]).total_seconds()) / 86400,
                "calendar_component": abs(float(b_time_z[ib] - c_time_z[ic])),
            })
            accepted += 1
        status = "PASS" if accepted else "NO PAIRS WITHIN CALIPER"
        stratum_audits.append({
            "asset": key[0], "definition": key[1], "direction": key[2],
            "breakout_candidates": len(breakouts), "control_candidates": len(controls),
            "matched_pairs": accepted, "unmatched_breakouts": len(breakouts) - len(used_b),
            "unused_controls": len(controls) - len(used_c), "status": status,
        })

        for j, feature in enumerate(FEATURES):
            pair_feature_rows.append({
                "asset": key[0], "definition": key[1], "direction": key[2],
                "feature": feature,
                "breakout_mean": float(np.mean(b_raw[:, j])),
                "control_mean": float(np.mean(c_raw[:, j])),
                "breakout_std": float(np.std(b_raw[:, j], ddof=0)),
                "control_std": float(np.std(c_raw[:, j], ddof=0)),
                "pooled_scale": float(stds[j]),
            })
        pair_feature_rows.append({
            "asset": key[0], "definition": key[1], "direction": key[2],
            "feature": "calendar_time_days",
            "breakout_mean": float(np.mean(b_days)), "control_mean": float(np.mean(c_days)),
            "breakout_std": float(np.std(b_days, ddof=0)),
            "control_std": float(np.std(c_days, ddof=0)), "pooled_scale": float(stds[5]),
        })

    audit_df = pd.DataFrame(stratum_audits)
    print("\n===== MATCHING COUNTS BY STRATUM =====")
    print(audit_df.to_string(index=False) if not audit_df.empty else "No strata.")
    if any(str(x).startswith("STOPPED") for x in audit_df.get("status", [])):
        print("\nWARNING: at least one stratum was stopped for an unusable scale; no dimension was dropped.")
    print("\n===== POOLED STANDARDIZATION PARAMETERS =====")
    print(pd.DataFrame(pair_feature_rows).to_string(index=False) if pair_feature_rows else "No usable strata.")

    if not matched_pairs:
        print("\nNo matched pairs. No outcome summaries can be produced.")
        raise SystemExit(0)

    # Stage C: outcomes, row-level pair audit, balance and paired differences.
    pair_audit_rows: list[dict] = []
    outcome_rows: list[dict] = []
    for pair in matched_pairs:
        asset = pair["asset"]
        opens, highs, lows, closes = minute_arrays[asset]
        b = pair["breakout"]
        c = pair["control"]
        b_out = candidate_outcomes(b, data[asset], opens, highs, lows, closes, b["boundary"])
        c_out = candidate_outcomes(c, data[asset], opens, highs, lows, closes, c["boundary"])
        pair_audit_rows.append({
            "pair_id": pair["pair_id"], "asset": asset,
            "definition": pair["definition"], "direction": pair["direction"],
            "breakout_time": b["time"], "control_time": c["time"],
            "breakout_boundary": b["boundary"], "control_boundary": c["boundary"],
            "distance": pair["distance"], "calendar_gap_hours": pair["calendar_gap_hours"],
            "calendar_gap_days": pair["calendar_gap_days"],
            "calendar_component": pair["calendar_component"],
            **{f"breakout_{FEATURES[i]}": float(b["features"][i]) for i in range(5)},
            **{f"control_{FEATURES[i]}": float(c["features"][i]) for i in range(5)},
        })
        for horizon in HORIZONS:
            record = {
                "pair_id": pair["pair_id"], "asset": asset,
                "definition": pair["definition"], "direction": pair["direction"],
                "horizon": horizon,
            }
            for metric in (
                "mfe_pct", "mae_pct", "net_pct", "return_inside",
                "ending_inside", "same_direction_break",
                "hit_0.25pct", "hit_0.5pct", "hit_1pct", "hit_1.5pct", "hit_2pct",
                "minutes_to_0.25pct", "minutes_to_0.5pct", "minutes_to_1pct",
                "minutes_to_1.5pct", "minutes_to_2pct",
            ):
                bv = b_out[f"{horizon}_{metric}"]
                cv = c_out[f"{horizon}_{metric}"]
                record[f"breakout_{metric}"] = bv
                record[f"control_{metric}"] = cv
                if metric in ("mfe_pct", "mae_pct", "net_pct"):
                    record[f"paired_difference_{metric}"] = float(bv) - float(cv)
            outcome_rows.append(record)

    pair_audit = pd.DataFrame(pair_audit_rows)
    outcomes = pd.DataFrame(outcome_rows)
    print("\n===== MATCHED PAIR ROW-LEVEL AUDIT =====")
    print(pair_audit.to_string(index=False, max_rows=250))
    print("\n===== MATCHED DISTANCE AND CALENDAR SEPARATION =====")
    print(pair_audit[["distance", "calendar_gap_hours", "calendar_gap_days", "calendar_component"]].describe(
        percentiles=[0.25, 0.5, 0.75, 0.9]
    ).to_string())

    # Standardized mean differences before/after matching for all six dimensions.
    balance_rows = []
    for key, group in candidate_frame.groupby(["asset", "definition", "direction"], sort=True):
        pair_subset = [p for p in matched_pairs if (p["asset"], p["definition"], p["direction"]) == key]
        if not pair_subset:
            continue
        b_all = group[group["role"] == "BREAKOUT"]
        c_all = group[group["role"] == "CONTROL"]
        b_match = np.vstack([p["breakout"]["features"] for p in pair_subset])
        c_match = np.vstack([p["control"]["features"] for p in pair_subset])
        t0 = min(group["time"])
        bdays_all = (b_all["time"] - t0).dt.total_seconds().to_numpy() / 86400
        cdays_all = (c_all["time"] - t0).dt.total_seconds().to_numpy() / 86400
        bdays_match = np.array([(p["breakout"]["time"] - t0).total_seconds() / 86400 for p in pair_subset])
        cdays_match = np.array([(p["control"]["time"] - t0).total_seconds() / 86400 for p in pair_subset])
        arrays = list(zip(
            list(b_all["features"].to_list()) and np.vstack(b_all["features"].to_numpy()).T or [],
            list(c_all["features"].to_list()) and np.vstack(c_all["features"].to_numpy()).T or [],
        )) if False else None
        for j, name in enumerate(FEATURES):
            before_b = np.vstack(b_all["features"].to_numpy())[:, j]
            before_c = np.vstack(c_all["features"].to_numpy())[:, j]
            after_b, after_c = b_match[:, j], c_match[:, j]
            for stage, vb, vc in (("BEFORE", before_b, before_c), ("AFTER", after_b, after_c)):
                pooled_sd = math.sqrt((float(np.var(vb, ddof=0)) + float(np.var(vc, ddof=0))) / 2)
                smd = (float(np.mean(vb)) - float(np.mean(vc))) / pooled_sd if pooled_sd > 0 else np.nan
                balance_rows.append({
                    "asset": key[0], "definition": key[1], "direction": key[2],
                    "stage": stage, "feature": name,
                    "breakout_mean": float(np.mean(vb)), "control_mean": float(np.mean(vc)),
                    "breakout_std": float(np.std(vb, ddof=0)),
                    "control_std": float(np.std(vc, ddof=0)), "SMD": smd,
                    "breakout_median": float(np.median(vb)), "control_median": float(np.median(vc)),
                    "breakout_p25": float(np.quantile(vb, .25)), "control_p25": float(np.quantile(vc, .25)),
                    "breakout_p75": float(np.quantile(vb, .75)), "control_p75": float(np.quantile(vc, .75)),
                })
        for stage, vb, vc in (("BEFORE", bdays_all, cdays_all), ("AFTER", bdays_match, cdays_match)):
            pooled_sd = math.sqrt((float(np.var(vb, ddof=0)) + float(np.var(vc, ddof=0))) / 2)
            smd = (float(np.mean(vb)) - float(np.mean(vc))) / pooled_sd if pooled_sd > 0 else np.nan
            balance_rows.append({
                "asset": key[0], "definition": key[1], "direction": key[2],
                "stage": stage, "feature": "calendar_time_days",
                "breakout_mean": float(np.mean(vb)), "control_mean": float(np.mean(vc)),
                "breakout_std": float(np.std(vb, ddof=0)),
                "control_std": float(np.std(vc, ddof=0)), "SMD": smd,
                "breakout_median": float(np.median(vb)), "control_median": float(np.median(vc)),
                "breakout_p25": float(np.quantile(vb, .25)), "control_p25": float(np.quantile(vc, .25)),
                "breakout_p75": float(np.quantile(vb, .75)), "control_p75": float(np.quantile(vc, .75)),
            })
    balance = pd.DataFrame(balance_rows)
    print("\n===== COVARIATE BALANCE BEFORE / AFTER MATCHING =====")
    print(balance.to_string(index=False, max_rows=300))

    # Descriptive outcome summaries by stratum and horizon.
    print("\n===== OUTCOME SUMMARIES =====")
    for key, group in outcomes.groupby(["asset", "definition", "direction", "horizon"], sort=True):
        print(f"\n{key} | matched pairs={len(group)}")
        cols = [
            "breakout_mfe_pct", "control_mfe_pct",
            "breakout_mae_pct", "control_mae_pct",
            "breakout_net_pct", "control_net_pct",
            "paired_difference_mfe_pct", "paired_difference_mae_pct",
            "paired_difference_net_pct",
        ]
        summary = group[cols].agg(["mean", "median", lambda s: float(s.quantile(.75)), lambda s: float(s.quantile(.90))])
        summary.index = ["mean", "median", "p75", "p90"]
        print(summary.round(5).to_string())
        bool_cols = ["breakout_return_inside", "control_same_direction_break"]
        print("Breakout return-inside rate:", round(float(group[bool_cols[0]].mean() * 100), 3), "%")
        print("Control same-direction breakout incidence:", round(float(group[bool_cols[1]].mean() * 100), 3), "%")
        print("Breakout ending-inside rate:", round(float(group["breakout_ending_inside"].mean() * 100), 3), "%")
        for threshold in ("0.25", "0.5", "1", "1.5", "2"):
            bcol = f"breakout_hit_{threshold}pct"
            ccol = f"control_hit_{threshold}pct"
            print(f"Reach {threshold}% favorable | breakout={group[bcol].mean()*100:.2f}% control={group[ccol].mean()*100:.2f}%")

    # Paired matched-pair bootstrap clustered in fixed 7-day calendar blocks.
    print("\n===== APPROXIMATE 95% CALENDAR-BLOCK BOOTSTRAP INTERVALS =====")
    print(f"Resampling: {BOOTSTRAP_REPS} replicates; {BLOCK_DAYS}-day calendar blocks; seed={BOOTSTRAP_SEED}.")
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    bootstrap_rows = []
    pair_meta = pair_audit.set_index("pair_id")
    for key, group in outcomes.groupby(["asset", "definition", "direction", "horizon"], sort=True):
        pair_ids = group["pair_id"].to_numpy()
        times = pd.to_datetime([pair_meta.loc[p, "breakout_time"] for p in pair_ids], utc=True)
        origin = times.min()
        block_ids = ((times - origin).total_seconds() // (BLOCK_DAYS * 86400)).astype(int)
        unique_blocks = np.unique(block_ids)
        if len(unique_blocks) < 2:
            print(f"{key}: insufficient distinct calendar blocks for interval; omitted.")
            continue
        diffs = group["paired_difference_net_pct"].to_numpy(dtype=float)
        boot_means = []
        for _ in range(BOOTSTRAP_REPS):
            sampled = rng.choice(unique_blocks, size=len(unique_blocks), replace=True)
            indices = np.concatenate([np.flatnonzero(block_ids == block) for block in sampled])
            if len(indices):
                boot_means.append(float(np.mean(diffs[indices])))
        lo, hi = np.quantile(boot_means, [0.025, 0.975])
        bootstrap_rows.append({
            "asset": key[0], "definition": key[1], "direction": key[2],
            "horizon": key[3], "pairs": len(group), "calendar_blocks": len(unique_blocks),
            "mean_paired_net_difference_pct": float(np.mean(diffs)),
            "ci95_low": float(lo), "ci95_high": float(hi),
        })
    print(pd.DataFrame(bootstrap_rows).to_string(index=False) if bootstrap_rows else "No intervals available.")

    print("\n===== INTERPRETATION AND LIMITATIONS =====")
    print("This is a matched, conditional descriptive comparison, not a causal estimate.")
    print("Greedy nearest-pair matching is without replacement, not globally optimal.")
    print(f"Maximum standardized Euclidean distance: {MAX_DISTANCE:.2f}; six equally weighted dimensions.")
    print("No relaxed calipers, replacement, or backfilling were used.")
    print("Matched sample requires complete uninterrupted follow-up through 12H.")
    print("Controls are not removed if they later break out; that incidence is reported.")
    print("No trading simulation, fees, slippage, funding, fills, or profitability inference.")
    print("Thresholds are full-sample retrospective quantiles, not live-calibrated.")
    print("Volume analysis not run because source volume units remain unverified.")
    print("Read-only: source CSVs and research scripts were not modified; no files written.")
    print("=" * 88)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nFATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
