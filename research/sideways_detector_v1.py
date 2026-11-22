#!/usr/bin/env python3
"""Reconstructed 4H sideways detector v1.

Research-only. Reads validated 4H OHLCV CSVs and writes raw rolling
snapshot metrics plus asset-specific full-sample P25/P40 classifications.
It does not reconstruct 15M tests or post-rejection outcomes.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
REQUIRED = ["ts", "open", "high", "low", "close", "vol"]
FOUR_HOURS_MS = 4 * 60 * 60 * 1000
WINDOW = 12


def directional_efficiency(closes: np.ndarray) -> float:
    """ER over exactly 12 closes / 11 adjacent close-to-close changes."""
    values = np.asarray(closes, dtype=float)
    if values.shape != (WINDOW,) or not np.isfinite(values).all():
        raise ValueError("directional_efficiency requires 12 finite closes")
    path = float(np.abs(np.diff(values)).sum())
    if path == 0.0:
        return 0.0
    return float(abs(values[-1] - values[0]) / path)


def pair_overlap(high_a: float, low_a: float,
                 high_b: float, low_b: float) -> float:
    """Intersection / union of two high-low ranges."""
    intersection = max(0.0, min(high_a, high_b) - max(low_a, low_b))
    union = max(high_a, high_b) - min(low_a, low_b)
    if union < 0:
        raise ValueError("Invalid negative range union")
    if union == 0.0:
        return 1.0
    return float(intersection / union)


def mean_adjacent_overlap(highs: np.ndarray, lows: np.ndarray) -> float:
    highs = np.asarray(highs, dtype=float)
    lows = np.asarray(lows, dtype=float)
    if highs.shape != (WINDOW,) or lows.shape != (WINDOW,):
        raise ValueError("mean_adjacent_overlap requires 12 highs and lows")
    if not np.isfinite(highs).all() or not np.isfinite(lows).all():
        raise ValueError("Non-finite high/low values")
    if (highs < lows).any():
        raise ValueError("High below low")
    ratios = [
        pair_overlap(highs[i - 1], lows[i - 1], highs[i], lows[i])
        for i in range(1, WINDOW)
    ]
    return float(np.mean(ratios))


def linear_quantile(values: np.ndarray, q: float) -> float:
    """NumPy linear quantile, with compatibility for older NumPy."""
    try:
        return float(np.quantile(values, q, method="linear"))
    except TypeError:
        return float(np.quantile(values, q, interpolation="linear"))


def load_4h(path: Path, asset: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: missing 4H file: {path}")
    df = pd.read_csv(path)
    missing = [column for column in REQUIRED if column not in df.columns]
    if missing:
        raise ValueError(f"{asset}: missing columns {missing}")

    df = df[REQUIRED].copy()
    ts = pd.to_numeric(df["ts"], errors="coerce")
    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{asset}: invalid/non-integer timestamps")
    df["ts"] = ts.astype("int64")

    for column in ["open", "high", "low", "close", "vol"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    numeric = df[["open", "high", "low", "close", "vol"]].to_numpy(float)
    if not np.isfinite(numeric).all():
        raise ValueError(f"{asset}: non-finite OHLCV values")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{asset}: non-positive price")
    if (df["vol"] < 0).any():
        raise ValueError(f"{asset}: negative volume")
    invalid_ohlc = (
        (df["high"] < df[["open", "close", "low"]].max(axis=1))
        | (df["low"] > df[["open", "close", "high"]].min(axis=1))
    )
    if invalid_ohlc.any():
        raise ValueError(f"{asset}: {int(invalid_ohlc.sum())} invalid OHLC rows")
    if (df["ts"] % FOUR_HOURS_MS != 0).any():
        raise ValueError(f"{asset}: timestamps are not epoch-aligned to 4H")

    delta = df["ts"].diff().dropna()
    if (delta != FOUR_HOURS_MS).any():
        bad = int((delta != FOUR_HOURS_MS).sum())
        raise ValueError(
            f"{asset}: {bad} 4H timestamp gaps/interval errors; "
            "stop rather than silently bridge missing candles"
        )
    if df["ts"].duplicated().any():
        raise ValueError(f"{asset}: duplicate 4H timestamps")
    return df.reset_index(drop=True)


def build_snapshots(df: pd.DataFrame, asset: str) -> pd.DataFrame:
    rows = []
    for end in range(WINDOW - 1, len(df)):
        window = df.iloc[end - WINDOW + 1:end + 1]
        highs = window["high"].to_numpy(dtype=float)
        lows = window["low"].to_numpy(dtype=float)
        closes = window["close"].to_numpy(dtype=float)

        upper = float(highs.max())
        lower = float(lows.min())
        midpoint = (upper + lower) / 2.0
        if midpoint <= 0.0:
            raise ValueError(f"{asset}: non-positive channel midpoint")

        width_pct = (upper - lower) / midpoint * 100.0
        efficiency = directional_efficiency(closes)
        overlap = mean_adjacent_overlap(highs, lows)

        snapshot_start = int(window.iloc[0]["ts"])
        snapshot_end = int(window.iloc[-1]["ts"])
        available_at = snapshot_end + FOUR_HOURS_MS

        rows.append({
            "asset": asset,
            "snapshot_start_ts_ms": snapshot_start,
            "snapshot_end_candle_ts_ms": snapshot_end,
            "available_at_ts_ms": available_at,
            "snapshot_start_utc": pd.to_datetime(snapshot_start, unit="ms", utc=True),
            "snapshot_end_candle_start_utc": pd.to_datetime(snapshot_end, unit="ms", utc=True),
            "available_at_utc": pd.to_datetime(available_at, unit="ms", utc=True),
            "window_candles": WINDOW,
            "upper": upper,
            "lower": lower,
            "midpoint": midpoint,
            "channel_width_pct": width_pct,
            "directional_efficiency": efficiency,
            "mean_overlap": overlap,
        })
    return pd.DataFrame(rows)


def classify_asset(snapshots: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    if snapshots.empty:
        raise ValueError("No complete 12-candle snapshots to classify")
    widths = snapshots["channel_width_pct"].to_numpy(dtype=float)
    p25 = linear_quantile(widths, 0.25)
    p40 = linear_quantile(widths, 0.40)

    result = snapshots.copy()
    result["asset_p25_width_pct"] = p25
    result["asset_p40_width_pct"] = p40
    result["passes_efficiency"] = result["directional_efficiency"] <= 0.30
    result["passes_overlap"] = result["mean_overlap"] >= 0.70
    result["passes_strict_width"] = result["channel_width_pct"] <= p25
    result["passes_broad_width"] = result["channel_width_pct"] <= p40
    result["strict_sideways"] = (
        result["passes_strict_width"]
        & result["passes_efficiency"]
        & result["passes_overlap"]
    )
    result["broad_sideways"] = (
        result["passes_broad_width"]
        & result["passes_efficiency"]
        & result["passes_overlap"]
    )

    summary = {
        "asset": str(result["asset"].iloc[0]),
        "valid_snapshots": int(len(result)),
        "p25_width_pct": p25,
        "p40_width_pct": p40,
        "strict_width_pass": int(result["passes_strict_width"].sum()),
        "broad_width_pass": int(result["passes_broad_width"].sum()),
        "efficiency_pass": int(result["passes_efficiency"].sum()),
        "overlap_pass": int(result["passes_overlap"].sum()),
        "strict_sideways_snapshots": int(result["strict_sideways"].sum()),
        "broad_sideways_snapshots": int(result["broad_sideways"].sum()),
        "strict_and_broad_overlap": int(
            (result["strict_sideways"] & result["broad_sideways"]).sum()
        ),
    }
    return result, summary


def self_test() -> None:
    linear = np.arange(100.0, 112.0)
    assert abs(directional_efficiency(linear) - 1.0) < 1e-12
    assert directional_efficiency(np.full(12, 100.0)) == 0.0
    assert pair_overlap(10, 0, 10, 0) == 1.0
    assert pair_overlap(10, 0, 20, 10) == 0.0
    assert abs(pair_overlap(10, 0, 15, 5) - (5.0 / 15.0)) < 1e-12
    assert mean_adjacent_overlap(np.ones(12), np.zeros(12)) == 1.0
    assert abs(linear_quantile(np.array([0.0, 10.0, 20.0, 30.0]), 0.25) - 7.5) < 1e-12
    print("PASS: detector formula self-tests (7 assertions)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path.home() / "okx_adaptive_bot" / "data",
        help="Directory containing ASSET_USDT_4h.csv files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.home() / "okxtester" / "reports" / "sideways_detector_v1",
        help="Output directory for snapshot CSVs and summary",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        if len(sys.argv) == 2:
            return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    print("===== RECONSTRUCTED SIDEWAYS DETECTOR V1 =====")
    print("Research-only; full-sample P25/P40 are retrospective.")

    for asset in ASSETS:
        path = args.data_dir / f"{asset}_USDT_4h.csv"
        print(f"\nLoading {asset}: {path}")
        source = load_4h(path, asset)
        raw = build_snapshots(source, asset)
        classified, summary = classify_asset(raw)

        output = args.output_dir / f"{asset}_sideways_snapshots_v1.csv"
        classified.to_csv(output, index=False)
        summaries.append(summary)

        print(f"4H source candles: {len(source):,}")
        print(f"Valid rolling snapshots: {summary['valid_snapshots']:,}")
        print(f"P25 width: {summary['p25_width_pct']:.8f}%")
        print(f"P40 width: {summary['p40_width_pct']:.8f}%")
        print(f"Strict sideways: {summary['strict_sideways_snapshots']:,}")
        print(f"Broad sideways: {summary['broad_sideways_snapshots']:,}")
        print(f"Saved: {output}")

    summary_df = pd.DataFrame(summaries)
    summary_path = args.output_dir / "detector_summary_v1.csv"
    summary_df.to_csv(summary_path, index=False)

    report = [
        "# Reconstructed Sideways Detector v1 — Run Summary",
        "",
        "**Status:** calculation run completed; independent formula/data audit still required.",
        "",
        "Research-only. Full-sample asset-specific P25/P40 thresholds are retrospective.",
        "",
        "| Asset | Valid snapshots | P25 width % | P40 width % | Strict sideways | Broad sideways |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in summaries:
        report.append(
            f"| {item['asset']} | {item['valid_snapshots']} | "
            f"{item['p25_width_pct']:.8f} | {item['p40_width_pct']:.8f} | "
            f"{item['strict_sideways_snapshots']} | {item['broad_sideways_snapshots']} |"
        )
    report += [
        "",
        "## Required interpretation limits",
        "",
        "- This output contains 4H detector snapshots only; no 15M tests/rejections or outcomes.",
        "- Each snapshot becomes available at the close of its final 4H candle.",
        "- The first 15M candle at the availability timestamp must be excluded downstream.",
        "- P25/P40 use all valid snapshots in the supplied history and therefore are not live-safe.",
        "- Independent recomputation and timestamp mapping must pass before downstream reconstruction.",
    ]
    report_path = args.output_dir / "detector_summary_v1.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n===== COMPLETE =====")
    print(f"Summary CSV: {summary_path}")
    print(f"Summary report: {report_path}")
    print("No source market-data files were modified.")


if __name__ == "__main__":
    main()
