#!/usr/bin/env python3
"""Causal historical sideways-boundary event reconstruction V1.

Consumes existing historical detector feature CSVs and 15M candles. It does
not rerun the detector, alter source data, or calculate forward outcomes.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
OHLCV = ["open", "high", "low", "close", "vol"]
REQUIRED = ["ts", *OHLCV]
FIFTEEN_MIN_MS = 15 * 60 * 1000
FOUR_HOURS_MS = 4 * 60 * 60 * 1000
FEATURE_REQUIRED = [
    "available_at_ts_ms", "channel_end_candle_ts_ms", "upper", "lower",
    "channel_width_pct", "directional_efficiency", "mean_overlap",
    "width_p25_pct", "width_p40_pct",
]


def load_15m(path: Path, asset: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: missing 15M file: {path}")
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"{asset}: 15M file missing columns {missing}")
    df = df[REQUIRED].copy()
    ts = pd.to_numeric(df["ts"], errors="coerce")
    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{asset}: invalid 15M timestamps")
    df["ts"] = ts.astype("int64")
    for col in OHLCV:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    values = df[OHLCV].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError(f"{asset}: non-finite 15M OHLCV")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{asset}: non-positive 15M price")
    if (df["vol"] < 0).any():
        raise ValueError(f"{asset}: negative 15M volume")
    bad = (
        (df["high"] < df[["open", "close", "low"]].max(axis=1))
        | (df["low"] > df[["open", "close", "high"]].min(axis=1))
    )
    if bad.any():
        raise ValueError(f"{asset}: {int(bad.sum())} invalid 15M OHLC rows")
    if (df["ts"] % FIFTEEN_MIN_MS != 0).any():
        raise ValueError(f"{asset}: 15M timestamps are not epoch-grid aligned")
    if df["ts"].duplicated().any():
        raise ValueError(f"{asset}: duplicate 15M timestamps")
    if not df["ts"].is_monotonic_increasing:
        raise ValueError(f"{asset}: 15M timestamps are not ordered")
    return df.reset_index(drop=True)


def load_features(path: Path, asset: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: missing feature file: {path}")
    df = pd.read_csv(path)
    missing = [c for c in FEATURE_REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"{asset}: feature file missing columns {missing}")
    df = df.copy()
    numeric = FEATURE_REQUIRED
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if not np.isfinite(df[numeric].to_numpy(dtype=float)).all():
        raise ValueError(f"{asset}: non-finite required feature values")
    for col in ["available_at_ts_ms", "channel_end_candle_ts_ms"]:
        if (df[col] % 1 != 0).any():
            raise ValueError(f"{asset}: non-integer feature timestamp: {col}")
        df[col] = df[col].astype("int64")
    if df["available_at_ts_ms"].duplicated().any():
        raise ValueError(f"{asset}: duplicate feature availability timestamps")
    if not df["available_at_ts_ms"].is_monotonic_increasing:
        raise ValueError(f"{asset}: feature rows are not ordered")
    if (df["available_at_ts_ms"] - df["channel_end_candle_ts_ms"] != FOUR_HOURS_MS).any():
        raise ValueError(f"{asset}: feature availability does not equal final 4H close")
    if (df["available_at_ts_ms"].diff().dropna() != FOUR_HOURS_MS).any():
        raise ValueError(f"{asset}: feature snapshots are not exactly 4H-spaced")
    if (df["upper"] <= df["lower"]).any():
        raise ValueError(f"{asset}: invalid channel bounds")
    return df.reset_index(drop=True)


def context_passes(row: pd.Series, definition: str) -> bool:
    width_limit = row["width_p25_pct"] if definition == "strict" else row["width_p40_pct"]
    return bool(
        row["channel_width_pct"] <= width_limit
        and row["directional_efficiency"] <= 0.30
        and row["mean_overlap"] >= 0.70
    )


def close_test(active: dict, end_ts: int, reason: str) -> dict:
    active["test_end_ts_ms"] = int(end_ts)
    active["closure_reason"] = reason
    return active


def process_snapshot(
    bars: pd.DataFrame,
    feature: pd.Series,
    asset: str,
    definition: str,
    snapshot_index: int,
    snapshot_next_ts: int,
    first_bar_suppressed: bool,
) -> tuple[list[dict], dict]:
    """Process one valid context snapshot; upper/lower state is independent."""
    upper = float(feature["upper"])
    lower = float(feature["lower"])
    width = upper - lower
    if not np.isfinite(width) or width <= 0:
        raise ValueError(f"{asset}: non-positive channel width")
    available = int(feature["available_at_ts_ms"])
    tests: list[dict] = []
    active = {"upper": None, "lower": None}
    rank = {"upper": 0, "lower": 0}
    segment = 1
    gap_count = 0
    processed = 0
    last_ts = None

    for row in bars.itertuples(index=False):
        ts = int(row.ts)
        if last_ts is not None and ts - last_ts != FIFTEEN_MIN_MS:
            gap_count += 1
            for direction in ("upper", "lower"):
                if active[direction] is not None:
                    tests.append(close_test(active[direction], last_ts, "15m_gap"))
                    active[direction] = None
                rank[direction] = 0
            segment += 1
        processed += 1
        high, low, close = float(row.high), float(row.low), float(row.close)

        for direction in ("upper", "lower"):
            if direction == "upper":
                touched = high >= upper - 0.10 * width
                rejection = touched and close < upper - 0.10 * width and close > lower
                separated = (not touched) and close <= upper - 0.20 * width
            else:
                touched = low <= lower + 0.10 * width
                rejection = touched and close > lower + 0.10 * width and close < upper
                separated = (not touched) and close >= lower + 0.20 * width

            current = active[direction]
            if current is None:
                if touched:
                    rank[direction] += 1
                    current = {
                        "asset": asset,
                        "definition": definition,
                        "direction": direction,
                        "snapshot_index": int(snapshot_index),
                        "snapshot_available_at_ts_ms": available,
                        "snapshot_next_available_at_ts_ms": int(snapshot_next_ts),
                        "segment_id": int(segment),
                        "test_rank": int(rank[direction]),
                        "test_start_ts_ms": ts,
                        "test_end_ts_ms": ts,
                        "test_start_open": float(row.open),
                        "test_start_high": high,
                        "test_start_low": low,
                        "test_start_close": close,
                        "first_strong_rejection_ts_ms": np.nan,
                        "rejection_open": np.nan,
                        "rejection_high": np.nan,
                        "rejection_low": np.nan,
                        "rejection_close": np.nan,
                        "closure_reason": "snapshot_end",
                    }
                    active[direction] = current
                    if rejection:
                        current["first_strong_rejection_ts_ms"] = ts
                        current["rejection_open"] = float(row.open)
                        current["rejection_high"] = high
                        current["rejection_low"] = low
                        current["rejection_close"] = close
            else:
                current["test_end_ts_ms"] = ts
                if pd.isna(current["first_strong_rejection_ts_ms"]) and rejection:
                    current["first_strong_rejection_ts_ms"] = ts
                    current["rejection_open"] = float(row.open)
                    current["rejection_high"] = high
                    current["rejection_low"] = low
                    current["rejection_close"] = close
                # A separation candle ends/arms but never starts the next test.
                if separated:
                    tests.append(close_test(current, ts, "separated"))
                    active[direction] = None
        last_ts = ts

    if last_ts is not None:
        for direction in ("upper", "lower"):
            if active[direction] is not None:
                tests.append(close_test(active[direction], last_ts, "snapshot_end"))

    return tests, {
        "processed_eligible_bars": int(processed),
        "15m_gaps_within_snapshot": int(gap_count),
        "continuity_segments": int(segment),
        "first_bar_suppressed": bool(first_bar_suppressed),
    }


def summarize(tests: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_rows = []
    snapshot_rows = []
    if tests.empty:
        return pd.DataFrame(), pd.DataFrame()
    work = tests.copy()
    work["has_rejection"] = work["first_strong_rejection_ts_ms"].notna()
    work["rank_bucket"] = work["test_rank"].map(
        lambda x: str(int(x)) if int(x) <= 3 else "4+"
    )
    groups = ["asset", "definition", "direction", "rank_bucket"]
    for keys, group in work.groupby(groups, dropna=False):
        n = len(group)
        rejected = int(group["has_rejection"].sum())
        summary_rows.append({
            "asset": keys[0], "definition": keys[1], "direction": keys[2],
            "test_rank": keys[3], "tests": n, "tests_with_rejection": rejected,
            "rejection_incidence": rejected / n if n else np.nan,
        })
    snap_groups = ["asset", "definition", "direction", "snapshot_available_at_ts_ms"]
    per_snapshot = work.groupby(snap_groups).size().rename("tests").reset_index()
    for keys, group in per_snapshot.groupby(["asset", "definition", "direction"]):
        for bucket, mask in [
            ("1", group["tests"] == 1), ("2", group["tests"] == 2),
            ("3", group["tests"] == 3), ("4+", group["tests"] >= 4),
            ("0", group["tests"] == 0),
        ]:
            snapshot_rows.append({
                "asset": keys[0], "definition": keys[1], "direction": keys[2],
                "snapshots_with_test_count": bucket, "snapshot_count": int(mask.sum()),
            })
    return pd.DataFrame(summary_rows), pd.DataFrame(snapshot_rows)


def run(data_dir: Path, feature_dir: Path, output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"Refusing to write into non-empty output directory: {output_dir}"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    all_tests = []
    audits = []
    for asset in ASSETS:
        bars = load_15m(data_dir / f"{asset}_USDT_15m.csv", asset)
        features = load_features(
            feature_dir / f"{asset}_features_original_v1.csv", asset
        )
        deltas = bars["ts"].diff().dropna()
        global_gaps = int((deltas != FIFTEEN_MIN_MS).sum())
        for definition in ("strict", "broad"):
            cohort_snapshots = 0
            suppressed = 0
            processed = 0
            gaps = 0
            for i, feature in features.iterrows():
                if not context_passes(feature, definition):
                    continue
                cohort_snapshots += 1
                available = int(feature["available_at_ts_ms"])
                next_available = (
                    int(features.iloc[i + 1]["available_at_ts_ms"])
                    if i + 1 < len(features) else available + FOUR_HOURS_MS
                )
                left = int(bars["ts"].searchsorted(available, side="left"))
                right = int(bars["ts"].searchsorted(next_available, side="left"))
                snapshot_bars = bars.iloc[left:right]
                has_first = len(snapshot_bars) > 0
                if has_first:
                    suppressed += 1
                    # Suppress exactly the first observed 15M candle at/after availability.
                    eligible = snapshot_bars.iloc[1:]
                else:
                    eligible = snapshot_bars
                snapshot_tests, audit = process_snapshot(
                    eligible, feature, asset, definition, i, next_available, has_first
                )
                all_tests.extend(snapshot_tests)
                processed += audit["processed_eligible_bars"]
                gaps += audit["15m_gaps_within_snapshot"]
            audits.append({
                "asset": asset, "definition": definition,
                "source_15m_rows": len(bars), "feature_rows": len(features),
                "global_15m_gaps": global_gaps,
                "qualifying_snapshots": cohort_snapshots,
                "snapshots_with_suppressed_first_bar": suppressed,
                "eligible_15m_bars_processed": processed,
                "15m_gaps_inside_processed_snapshots": gaps,
                "note": "Strict/broad cohorts overlap; descriptive counts only.",
            })

    tests = pd.DataFrame(all_tests)
    if tests.empty:
        tests = pd.DataFrame(columns=[
            "asset", "definition", "direction", "snapshot_index",
            "snapshot_available_at_ts_ms", "snapshot_next_available_at_ts_ms",
            "segment_id", "test_rank", "test_start_ts_ms", "test_end_ts_ms",
            "test_start_open", "test_start_high", "test_start_low",
            "test_start_close", "first_strong_rejection_ts_ms", "rejection_open",
            "rejection_high", "rejection_low", "rejection_close", "closure_reason",
        ])
    summary, snapshot_dist = summarize(tests)
    tests.to_csv(output_dir / "boundary_tests_historical_v1.csv", index=False)
    summary.to_csv(output_dir / "rejection_incidence_by_rank_v1.csv", index=False)
    snapshot_dist.to_csv(output_dir / "snapshot_test_count_distribution_v1.csv", index=False)
    pd.DataFrame(audits).to_csv(output_dir / "reconstruction_audit_v1.csv", index=False)
    print("===== HISTORICAL BOUNDARY EVENT RECONSTRUCTION V1 =====")
    print(f"Test rows: {len(tests):,}")
    print(f"Tests with first strong rejection: "
          f"{int(tests['first_strong_rejection_ts_ms'].notna().sum()):,}")
    print(f"Reports saved in: {output_dir}")
    print("No source candle, detector feature, or earlier report was modified.")
    print("Descriptive event counts only; no forward outcomes or profitability claims.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path,
                        default=Path.home() / "okx_adaptive_bot" / "data")
    parser.add_argument("--feature-dir", type=Path,
                        default=Path.home() / "okxtester" / "reports" /
                                "sideways_detector_original_v1")
    parser.add_argument("--output-dir", type=Path,
                        default=Path.home() / "okxtester" / "reports" /
                                "sideways_boundary_events_historical_v1")
    args = parser.parse_args()
    run(args.data_dir, args.feature_dir, args.output_dir)


if __name__ == "__main__":
    main()
