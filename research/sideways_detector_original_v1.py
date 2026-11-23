#!/usr/bin/env python3
"""Historical-formula 48H sideways detector reproduction V1.

This is separate from research/sideways_detector_v1.py. It reproduces the
formulas and 2,358-row alignment documented in the historical research files.
Full-sample width quantiles are retrospective/exploratory, not live-safe.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
REQUIRED = ["ts", "open", "high", "low", "close", "vol"]
FOUR_HOURS_MS = 4 * 60 * 60 * 1000
CHANNEL_BARS = 12
ER_CHANGES = 12
WIDTH_QUANTILES = (0.25, 0.40, 0.50)
ER_LIMITS = (0.20, 0.30, 0.40)
OVERLAP_FLOORS = (0.50, 0.60, 0.70)


def channel_width_pct(highs: np.ndarray, lows: np.ndarray) -> float:
    """Historical width: (rolling maximum high / minimum low - 1) * 100."""
    highs = np.asarray(highs, dtype=float)
    lows = np.asarray(lows, dtype=float)
    if highs.shape != (CHANNEL_BARS,) or lows.shape != (CHANNEL_BARS,):
        raise ValueError("channel_width_pct requires 12 highs and 12 lows")
    if not np.isfinite(highs).all() or not np.isfinite(lows).all():
        raise ValueError("Non-finite channel values")
    upper = float(highs.max())
    lower = float(lows.min())
    if lower <= 0.0 or upper < lower:
        raise ValueError("Invalid channel bounds")
    return float((upper / lower - 1.0) * 100.0)


def directional_efficiency(closes: np.ndarray) -> float:
    """Historical ER: 12 close changes, hence exactly 13 finite closes."""
    values = np.asarray(closes, dtype=float)
    if values.shape != (ER_CHANGES + 1,) or not np.isfinite(values).all():
        raise ValueError("directional_efficiency requires 13 finite closes")
    path = float(np.abs(np.diff(values)).sum())
    if path == 0.0:
        # Defensive convention; the historical documents do not specify this edge.
        return 0.0
    return float(abs(values[-1] - values[0]) / path)


def pair_overlap_smaller_range(
    high_a: float, low_a: float, high_b: float, low_b: float
) -> float:
    """Historical overlap: intersection / smaller candle range.

    A zero-width smaller candle is missing (NaN), matching the historical
    feature-distribution document.
    """
    values = np.asarray([high_a, low_a, high_b, low_b], dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Overlap inputs must be finite")
    if high_a < low_a or high_b < low_b:
        raise ValueError("Invalid candle range")
    intersection = max(0.0, min(high_a, high_b) - max(low_a, low_b))
    denominator = min(high_a - low_a, high_b - low_b)
    if denominator == 0.0:
        return float("nan")
    return float(np.clip(intersection / denominator, 0.0, 1.0))


def mean_adjacent_overlap(highs: np.ndarray, lows: np.ndarray) -> float:
    """Mean of non-missing overlap ratios over 11 adjacent pairs."""
    highs = np.asarray(highs, dtype=float)
    lows = np.asarray(lows, dtype=float)
    if highs.shape != (CHANNEL_BARS,) or lows.shape != (CHANNEL_BARS,):
        raise ValueError("mean_adjacent_overlap requires 12 highs and lows")
    if not np.isfinite(highs).all() or not np.isfinite(lows).all():
        raise ValueError("Non-finite high/low values")
    if (highs < lows).any():
        raise ValueError("High below low")
    ratios = np.asarray([
        pair_overlap_smaller_range(highs[i - 1], lows[i - 1], highs[i], lows[i])
        for i in range(1, CHANNEL_BARS)
    ], dtype=float)
    valid = ratios[np.isfinite(ratios)]
    if len(valid) == 0:
        return float("nan")
    return float(valid.mean())


def linear_quantile(values: np.ndarray, q: float) -> float:
    """Linear interpolation; historical interpolation method is not preserved."""
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        raise ValueError("Cannot calculate quantile from no finite values")
    try:
        return float(np.quantile(arr, q, method="linear"))
    except TypeError:  # NumPy compatibility
        return float(np.quantile(arr, q, interpolation="linear"))


def build_features(df: pd.DataFrame, asset: str) -> pd.DataFrame:
    """Build 2,358-style rows: 12-bar channel plus 12-change ER."""
    rows: list[dict] = []
    # Index i needs i-12 for the 13-close ER and i-11..i for channel/overlap.
    for i in range(ER_CHANGES, len(df)):
        channel = df.iloc[i - CHANNEL_BARS + 1:i + 1]
        er_closes = df.iloc[i - ER_CHANGES:i + 1]["close"].to_numpy(dtype=float)
        highs = channel["high"].to_numpy(dtype=float)
        lows = channel["low"].to_numpy(dtype=float)

        upper = float(highs.max())
        lower = float(lows.min())
        width = channel_width_pct(highs, lows)
        efficiency = directional_efficiency(er_closes)
        overlap = mean_adjacent_overlap(highs, lows)

        start_ts = int(channel.iloc[0]["ts"])
        end_ts = int(channel.iloc[-1]["ts"])
        rows.append({
            "asset": asset,
            "channel_start_ts_ms": start_ts,
            "channel_end_candle_ts_ms": end_ts,
            "available_at_ts_ms": end_ts + FOUR_HOURS_MS,
            "channel_start_utc": pd.to_datetime(start_ts, unit="ms", utc=True),
            "channel_end_candle_start_utc": pd.to_datetime(end_ts, unit="ms", utc=True),
            "available_at_utc": pd.to_datetime(end_ts + FOUR_HOURS_MS, unit="ms", utc=True),
            "channel_window_candles": CHANNEL_BARS,
            "er_close_observations": ER_CHANGES + 1,
            "er_close_changes": ER_CHANGES,
            "upper": upper,
            "lower": lower,
            "channel_width_pct": width,
            "directional_efficiency": efficiency,
            "mean_overlap": overlap,
            "overlap_valid_pairs": int(sum(
                np.isfinite(pair_overlap_smaller_range(
                    highs[j - 1], lows[j - 1], highs[j], lows[j]
                ))
                for j in range(1, CHANNEL_BARS)
            )),
            "er_lookback_start_close_ts_ms": int(df.iloc[i - ER_CHANGES]["ts"]),
        })
    return pd.DataFrame(rows)


def classify_asset(features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    if features.empty:
        raise ValueError("No valid historical feature rows")
    widths = features["channel_width_pct"].to_numpy(dtype=float)
    thresholds = {q: linear_quantile(widths, q) for q in WIDTH_QUANTILES}

    result = features.copy()
    for q, threshold in thresholds.items():
        result[f"width_p{int(q * 100)}_pct"] = threshold

    result["passes_efficiency_020"] = result["directional_efficiency"] <= 0.20
    result["passes_efficiency_030"] = result["directional_efficiency"] <= 0.30
    result["passes_efficiency_040"] = result["directional_efficiency"] <= 0.40
    for q, threshold in thresholds.items():
        p = int(q * 100)
        result[f"passes_width_p{p}"] = result["channel_width_pct"] <= threshold

    for floor in OVERLAP_FLOORS:
        result[f"passes_overlap_{int(floor * 100)}"] = (
            result["mean_overlap"] >= floor
        )

    candidate_rows = []
    for q, width_threshold in thresholds.items():
        p = int(q * 100)
        for er_limit in ER_LIMITS:
            for overlap_floor in OVERLAP_FLOORS:
                mask = (
                    (result["channel_width_pct"] <= width_threshold)
                    & (result["directional_efficiency"] <= er_limit)
                    & (result["mean_overlap"] >= overlap_floor)
                )
                candidate_rows.append({
                    "asset": str(result["asset"].iloc[0]),
                    "width_percentile": p,
                    "width_threshold_pct": width_threshold,
                    "er_max": er_limit,
                    "overlap_min": overlap_floor,
                    "qualifying_windows": int(mask.sum()),
                    "valid_windows": int(len(result)),
                    "qualifying_pct": float(mask.mean() * 100.0),
                })

    strict = (
        result["passes_width_p25"]
        & result["passes_efficiency_030"]
        & result["passes_overlap_70"]
    )
    broad = (
        result["passes_width_p40"]
        & result["passes_efficiency_030"]
        & result["passes_overlap_70"]
    )
    summary = {
        "asset": str(result["asset"].iloc[0]),
        "valid_windows": int(len(result)),
        "p25_width_pct": thresholds[0.25],
        "p40_width_pct": thresholds[0.40],
        "p50_width_pct": thresholds[0.50],
        "strict_p25_de030_ov70_count": int(strict.sum()),
        "strict_p25_de030_ov70_pct": float(strict.mean() * 100.0),
        "broad_p40_de030_ov70_count": int(broad.sum()),
        "broad_p40_de030_ov70_pct": float(broad.mean() * 100.0),
        "overlap_missing_windows": int(result["mean_overlap"].isna().sum()),
    }
    return result, pd.DataFrame(candidate_rows), summary


def load_4h(path: Path, asset: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: missing 4H file: {path}")
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"{asset}: missing columns {missing}")
    df = df[REQUIRED].copy()
    ts = pd.to_numeric(df["ts"], errors="coerce")
    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{asset}: invalid/non-integer timestamps")
    df["ts"] = ts.astype("int64")
    for c in ["open", "high", "low", "close", "vol"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    numeric = df[["open", "high", "low", "close", "vol"]].to_numpy(float)
    if not np.isfinite(numeric).all():
        raise ValueError(f"{asset}: non-finite OHLCV values")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{asset}: non-positive price")
    if (df["vol"] < 0).any():
        raise ValueError(f"{asset}: negative volume")
    invalid = (
        (df["high"] < df[["open", "close", "low"]].max(axis=1))
        | (df["low"] > df[["open", "close", "high"]].min(axis=1))
    )
    if invalid.any():
        raise ValueError(f"{asset}: {int(invalid.sum())} invalid OHLC rows")
    if (df["ts"] % FOUR_HOURS_MS != 0).any():
        raise ValueError(f"{asset}: timestamps not epoch-aligned to 4H")
    if df["ts"].duplicated().any():
        raise ValueError(f"{asset}: duplicate timestamps")
    delta = df["ts"].diff().dropna()
    if (delta != FOUR_HOURS_MS).any():
        raise ValueError(f"{asset}: missing/irregular 4H intervals; refusing to bridge")
    return df.reset_index(drop=True)


def self_test() -> None:
    highs = np.full(12, 110.0)
    lows = np.full(12, 100.0)
    assert abs(channel_width_pct(highs, lows) - 10.0) < 1e-12
    assert directional_efficiency(np.arange(13, dtype=float)) == 1.0
    assert directional_efficiency(np.full(13, 5.0)) == 0.0
    assert np.isnan(pair_overlap_smaller_range(10, 10, 12, 8))
    assert pair_overlap_smaller_range(10, 0, 20, 10) == 0.0
    assert pair_overlap_smaller_range(10, 0, 15, 5) == 1.0
    assert pair_overlap_smaller_range(15, 5, 10, 0) == 1.0
    assert mean_adjacent_overlap(np.full(12, 10.0), np.zeros(12)) == 1.0
    assert np.isnan(mean_adjacent_overlap(np.ones(12), np.ones(12)))
    assert abs(linear_quantile(np.array([0.0, 10.0, 20.0, 30.0]), 0.25) - 7.5) < 1e-12

    # 13 source bars create one row: channel bars 1..12, ER closes 0..12.
    rows = []
    for i in range(13):
        rows.append({
            "ts": i * FOUR_HOURS_MS, "open": 100.0 + i,
            "high": 102.0 + i, "low": 99.0 + i,
            "close": 101.0 + i, "vol": 1.0,
        })
    feature = build_features(pd.DataFrame(rows), "TST")
    assert len(feature) == 1
    assert feature.iloc[0]["channel_start_ts_ms"] == FOUR_HOURS_MS
    assert feature.iloc[0]["channel_end_candle_ts_ms"] == 12 * FOUR_HOURS_MS
    assert feature.iloc[0]["er_lookback_start_close_ts_ms"] == 0

    # Historical count alignment: N bars -> N - 12 rows.
    longer = pd.concat([pd.DataFrame(rows)] * 2, ignore_index=True)
    longer["ts"] = np.arange(len(longer), dtype=np.int64) * FOUR_HOURS_MS
    assert len(build_features(longer, "TST")) == len(longer) - 12
    print("PASS: historical detector formula/alignment self-tests (11 checks)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path,
        default=Path.home() / "okx_adaptive_bot" / "data",
        help="Directory containing ASSET_USDT_4h.csv files",
    )
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path.home() / "okxtester" / "reports" / "sideways_detector_original_v1",
        help="Separate output directory; reconstructed V1 is not modified",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        if len(__import__("sys").argv) == 2:
            return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    all_candidates = []
    print("===== HISTORICAL SIDEWAYS DETECTOR REPRODUCTION V1 =====")
    print("12-bar channel + 12 close changes (13 closes); retrospective quantiles.")
    for asset in ASSETS:
        source_path = args.data_dir / f"{asset}_USDT_4h.csv"
        source = load_4h(source_path, asset)
        features = build_features(source, asset)
        classified, candidates, summary = classify_asset(features)
        if len(source) == 2370 and len(features) != 2358:
            raise AssertionError(f"{asset}: expected 2,358 rows, got {len(features)}")
        classified.to_csv(args.output_dir / f"{asset}_features_original_v1.csv", index=False)
        candidates.to_csv(args.output_dir / f"{asset}_candidate_grid_original_v1.csv", index=False)
        summaries.append(summary)
        all_candidates.append(candidates)
        print(
            f"{asset}: source={len(source):,}, windows={len(features):,}, "
            f"P25={summary['p25_width_pct']:.6f}, "
            f"P40={summary['p40_width_pct']:.6f}, "
            f"strict={summary['strict_p25_de030_ov70_count']}, "
            f"broad={summary['broad_p40_de030_ov70_count']}"
        )

    summary_df = pd.DataFrame(summaries)
    candidates_df = pd.concat(all_candidates, ignore_index=True)
    summary_df.to_csv(args.output_dir / "detector_summary_original_v1.csv", index=False)
    candidates_df.to_csv(args.output_dir / "all_candidate_grid_original_v1.csv", index=False)

    quantile_rows = []
    for asset in ASSETS:
        f = pd.read_csv(args.output_dir / f"{asset}_features_original_v1.csv")
        for feature_name in ["channel_width_pct", "directional_efficiency", "mean_overlap"]:
            for q in [0.10, 0.25, 0.40, 0.50, 0.60, 0.75, 0.90]:
                quantile_rows.append({
                    "asset": asset, "feature": feature_name, "quantile": q,
                    "value": linear_quantile(f[feature_name].to_numpy(float), q),
                })
    pd.DataFrame(quantile_rows).to_csv(
        args.output_dir / "feature_distributions_original_v1.csv", index=False
    )

    print("\n===== REFERENCE COMPARISON TARGETS =====")
    references = {
        "BTC": (3.242, 3.948, 401, 601),
        "ETH": (4.245, 5.475, 415, 620),
        "SOL": (5.067, 6.115, 409, 607),
        "DOGE": (5.166, 6.264, 407, 606),
        "AVAX": (5.705, 6.916, 430, 624),
    }
    for row in summaries:
        ref = references[row["asset"]]
        print(
            f"{row['asset']}: P25 ref={ref[0]:.3f}, got={row['p25_width_pct']:.3f}; "
            f"P40 ref={ref[1]:.3f}, got={row['p40_width_pct']:.3f}; "
            f"strict ref={ref[2]}, got={row['strict_p25_de030_ov70_count']}; "
            f"broad ref={ref[3]}, got={row['broad_p40_de030_ov70_count']}"
        )
    print(f"\nReports saved in: {args.output_dir}")
    print("No source market-data files were modified.")
    print("IMPORTANT: compare all results with historical references before acceptance.")


if __name__ == "__main__":
    main()
