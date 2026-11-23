#!/usr/bin/env python3
"""Causal descriptive forward outcomes for reconstructed sideways-boundary rejections V1.

This is an event study, not an execution simulator or profitability backtest.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
MINUTE_MS = 60_000
FIFTEEN_MIN_MS = 15 * MINUTE_MS
HORIZONS = {
    "15m": 15 * MINUTE_MS,
    "1h": 60 * MINUTE_MS,
    "4h": 4 * 60 * MINUTE_MS,
    "24h": 24 * 60 * MINUTE_MS,
}
EVENT_COLUMNS = [
    "asset", "definition", "direction", "snapshot_index", "segment_id",
    "test_rank", "test_start_ts_ms", "test_end_ts_ms",
    "first_strong_rejection_ts_ms", "closure_reason",
]
MINUTE_COLUMNS = ["ts", "open", "high", "low", "close"]
EXPECTED_REJECTIONS = {"broad": 1154, "strict": 838}


def validate_events(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Missing event ledger: {path}")
    df = pd.read_csv(path)
    missing = [c for c in EVENT_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Event ledger missing columns: {missing}")
    df = df[df["first_strong_rejection_ts_ms"].notna()].copy()
    if df.empty:
        raise ValueError("No events with a first strong rejection")
    for col in [
        "snapshot_index", "segment_id", "test_rank", "test_start_ts_ms",
        "test_end_ts_ms", "first_strong_rejection_ts_ms",
    ]:
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any() or (values % 1 != 0).any():
            raise ValueError(f"Invalid integer event field: {col}")
        df[col] = values.astype("int64")
    if not set(df["asset"]).issubset(ASSETS):
        raise ValueError("Event ledger contains an unknown asset")
    if not set(df["definition"]).issubset({"broad", "strict"}):
        raise ValueError("Event ledger contains an unknown definition")
    if not set(df["direction"]).issubset({"upper", "lower"}):
        raise ValueError("Event ledger contains an unknown direction")
    key = [
        "asset", "definition", "direction", "snapshot_index",
        "segment_id", "test_rank", "test_start_ts_ms",
    ]
    if df.duplicated(key).any():
        raise ValueError("Duplicate event identity keys")
    rejection = df["first_strong_rejection_ts_ms"]
    if ((rejection < df["test_start_ts_ms"]) | (rejection > df["test_end_ts_ms"])).any():
        raise ValueError("A rejection timestamp lies outside its test boundaries")
    if (rejection % FIFTEEN_MIN_MS != 0).any():
        raise ValueError("A rejection timestamp is not on the 15M epoch grid")
    df["rejection_confirmed_at_ts_ms"] = rejection + FIFTEEN_MIN_MS
    if (df["rejection_confirmed_at_ts_ms"] % MINUTE_MS != 0).any():
        raise ValueError("A confirmation timestamp is not on the 1M epoch grid")
    counts = df.groupby("definition").size().to_dict()
    for definition, expected in EXPECTED_REJECTIONS.items():
        actual = int(counts.get(definition, 0))
        if actual != expected:
            raise ValueError(
                f"{definition} rejection count mismatch: expected {expected}, got {actual}"
            )
    df["event_id"] = df[key].astype(str).agg("|".join, axis=1)
    return df.sort_values(["asset", "definition", "first_strong_rejection_ts_ms", "event_id"]).reset_index(drop=True)


def load_minutes(path: Path, asset: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: missing 1M file: {path}")
    df = pd.read_csv(path, usecols=MINUTE_COLUMNS)
    ts = pd.to_numeric(df["ts"], errors="coerce")
    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{asset}: invalid 1M timestamps")
    df["ts"] = ts.astype("int64")
    for col in MINUTE_COLUMNS[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    values = df[MINUTE_COLUMNS[1:]].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError(f"{asset}: non-finite 1M OHLC")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{asset}: non-positive 1M price")
    bad = (
        (df["high"] < df[["open", "close", "low"]].max(axis=1))
        | (df["low"] > df[["open", "close", "high"]].min(axis=1))
    )
    if bad.any():
        raise ValueError(f"{asset}: {int(bad.sum())} invalid 1M OHLC rows")
    if (df["ts"] % MINUTE_MS != 0).any():
        raise ValueError(f"{asset}: 1M timestamps are not epoch-grid aligned")
    if df["ts"].duplicated().any():
        raise ValueError(f"{asset}: duplicate 1M timestamps")
    if not df["ts"].is_monotonic_increasing:
        raise ValueError(f"{asset}: 1M timestamps are not ordered")
    gaps = np.diff(df["ts"].to_numpy(dtype=np.int64))
    unusual = int(np.count_nonzero(gaps != MINUTE_MS))
    if unusual:
        raise ValueError(f"{asset}: found {unusual} non-60-second timestamp gaps")
    return df.reset_index(drop=True)


def direction_adjusted_return(raw_return: float, direction: str) -> float:
    if direction == "upper":
        return -float(raw_return)
    if direction == "lower":
        return float(raw_return)
    raise ValueError(f"Unknown direction: {direction}")


def calculate_horizon(
    ts: np.ndarray,
    opens: np.ndarray,
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    confirmation_ts_ms: int,
    direction: str,
    horizon_ms: int,
) -> dict:
    """Calculate one horizon using only exact 1M bars at/after confirmation."""
    expected_count = horizon_ms // MINUTE_MS
    start = int(np.searchsorted(ts, confirmation_ts_ms, side="left"))
    base = {
        "status": "incomplete",
        "censor_reason": "",
        "expected_bars": int(expected_count),
        "observed_bars": 0,
        "horizon_end_ts_ms": int(confirmation_ts_ms + horizon_ms),
        "reference_entry_price": np.nan,
        "horizon_close": np.nan,
        "max_high": np.nan,
        "min_low": np.nan,
        "raw_return": np.nan,
        "direction_adjusted_return": np.nan,
        "favorable_excursion": np.nan,
        "adverse_excursion": np.nan,
    }
    if start >= len(ts) or int(ts[start]) != int(confirmation_ts_ms):
        base["censor_reason"] = "missing_confirmation_minute"
        return base
    stop = start + expected_count
    available_stop = min(stop, len(ts))
    actual_ts = ts[start:available_stop]
    base["observed_bars"] = int(len(actual_ts))
    expected_ts = confirmation_ts_ms + np.arange(expected_count, dtype=np.int64) * MINUTE_MS
    if len(actual_ts) != expected_count:
        base["censor_reason"] = "insufficient_future_data"
        return base
    if not np.array_equal(actual_ts, expected_ts):
        base["censor_reason"] = "missing_or_irregular_minute"
        return base
    if int(actual_ts[0]) < int(confirmation_ts_ms):
        raise AssertionError("Look-ahead: outcome interval starts before confirmation")
    entry = float(opens[start])
    exit_close = float(closes[stop - 1])
    max_high = float(np.max(highs[start:stop]))
    min_low = float(np.min(lows[start:stop]))
    raw = exit_close / entry - 1.0
    adjusted = direction_adjusted_return(raw, direction)
    if direction == "upper":
        favorable = (entry - min_low) / entry
        adverse = (max_high - entry) / entry
    elif direction == "lower":
        favorable = (max_high - entry) / entry
        adverse = (entry - min_low) / entry
    else:
        raise ValueError(f"Unknown direction: {direction}")
    base.update({
        "status": "complete",
        "censor_reason": "",
        "reference_entry_price": entry,
        "horizon_close": exit_close,
        "max_high": max_high,
        "min_low": min_low,
        "raw_return": raw,
        "direction_adjusted_return": adjusted,
        "favorable_excursion": favorable,
        "adverse_excursion": adverse,
    })
    return base


def build_event_outcomes(events: pd.DataFrame, minute_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    outcomes = []
    audits = []
    for asset in ASSETS:
        asset_events = events[events["asset"] == asset]
        if asset_events.empty:
            raise ValueError(f"No rejection events found for {asset}")
        minutes = load_minutes(minute_dir / f"{asset}_USDT_USDT_1m.csv", asset)
        ts = minutes["ts"].to_numpy(dtype=np.int64)
        opens = minutes["open"].to_numpy(dtype=float)
        highs = minutes["high"].to_numpy(dtype=float)
        lows = minutes["low"].to_numpy(dtype=float)
        closes = minutes["close"].to_numpy(dtype=float)
        exact_entries = 0
        for event in asset_events.itertuples(index=False):
            confirmation = int(event.rejection_confirmed_at_ts_ms)
            p = int(np.searchsorted(ts, confirmation, side="left"))
            entry_exists = p < len(ts) and int(ts[p]) == confirmation
            exact_entries += int(entry_exists)
            record = {
                "event_id": event.event_id,
                "asset": event.asset,
                "definition": event.definition,
                "direction": event.direction,
                "snapshot_index": int(event.snapshot_index),
                "segment_id": int(event.segment_id),
                "test_rank": int(event.test_rank),
                "test_start_ts_ms": int(event.test_start_ts_ms),
                "test_end_ts_ms": int(event.test_end_ts_ms),
                "first_strong_rejection_ts_ms": int(event.first_strong_rejection_ts_ms),
                "rejection_confirmed_at_ts_ms": confirmation,
                "closure_reason": event.closure_reason,
                "entry_minute_exists": bool(entry_exists),
            }
            for label, horizon_ms in HORIZONS.items():
                result = calculate_horizon(
                    ts, opens, highs, lows, closes,
                    confirmation, event.direction, horizon_ms,
                )
                for key, value in result.items():
                    record[f"{label}_{key}"] = value
            outcomes.append(record)
        gaps = np.diff(ts)
        audits.append({
            "asset": asset,
            "source_1m_rows": len(minutes),
            "first_1m_ts_ms": int(ts[0]),
            "last_1m_ts_ms": int(ts[-1]),
            "non_60s_gaps": int(np.count_nonzero(gaps != MINUTE_MS)),
            "broad_events": int((asset_events["definition"] == "broad").sum()),
            "strict_events": int((asset_events["definition"] == "strict").sum()),
            "exact_confirmation_minutes": exact_entries,
            "confirmation_minutes_missing": int(len(asset_events) - exact_entries),
        })
    return pd.DataFrame(outcomes), pd.DataFrame(audits)


def build_aggregate(outcomes: pd.DataFrame) -> pd.DataFrame:
    rows = []
    group_specs = [
        ("ALL", "ALL", outcomes),
    ]
    for asset in ASSETS:
        subset = outcomes[outcomes["asset"] == asset]
        group_specs.append((asset, "ALL", subset))
    for direction in ("upper", "lower"):
        subset = outcomes[outcomes["direction"] == direction]
        group_specs.append(("ALL", direction, subset))
    for asset in ASSETS:
        for direction in ("upper", "lower"):
            subset = outcomes[
                (outcomes["asset"] == asset) & (outcomes["direction"] == direction)
            ]
            group_specs.append((asset, direction, subset))

    for definition in ("broad", "strict"):
        cohort = outcomes[outcomes["definition"] == definition]
        for asset_label, direction_label, _ in group_specs:
            subset = cohort
            if asset_label != "ALL":
                subset = subset[subset["asset"] == asset_label]
            if direction_label != "ALL":
                subset = subset[subset["direction"] == direction_label]
            for horizon in HORIZONS:
                status = subset[f"{horizon}_status"]
                complete = subset[status == "complete"]
                adjusted = complete[f"{horizon}_direction_adjusted_return"].astype(float)
                mfe = complete[f"{horizon}_favorable_excursion"].astype(float)
                mae = complete[f"{horizon}_adverse_excursion"].astype(float)
                n = len(subset)
                n_complete = len(complete)
                row = {
                    "definition": definition,
                    "asset_group": asset_label,
                    "direction_group": direction_label,
                    "horizon": horizon,
                    "events": n,
                    "complete": n_complete,
                    "censored": int(n - n_complete),
                    "positive_direction_adjusted_count": int((adjusted > 0).sum()),
                    "positive_direction_adjusted_frequency": float((adjusted > 0).mean()) if n_complete else np.nan,
                }
                for metric, values in [
                    ("direction_adjusted_return", adjusted),
                    ("favorable_excursion", mfe),
                    ("adverse_excursion", mae),
                ]:
                    for stat, value in [
                        ("mean", values.mean()),
                        ("median", values.median()),
                        ("p10", values.quantile(0.10)),
                        ("p25", values.quantile(0.25)),
                        ("p75", values.quantile(0.75)),
                        ("p90", values.quantile(0.90)),
                    ]:
                        row[f"{metric}_{stat}"] = float(value) if pd.notna(value) else np.nan
                rows.append(row)
    return pd.DataFrame(rows)


def run(event_path: Path, minute_dir: Path, output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to write into non-empty output directory: {output_dir}")
    events = validate_events(event_path)
    outcomes, audits = build_event_outcomes(events, minute_dir)
    if len(outcomes) != 1992:
        raise ValueError(f"Expected 1,992 broad+strict event rows, got {len(outcomes)}")
    if not outcomes["entry_minute_exists"].all():
        missing = int((~outcomes["entry_minute_exists"]).sum())
        raise ValueError(f"{missing} events lack the exact confirmation minute")
    aggregates = build_aggregate(outcomes)
    output_dir.mkdir(parents=True, exist_ok=True)
    outcomes.to_csv(output_dir / "event_level_outcomes.csv", index=False)
    aggregates.to_csv(output_dir / "aggregate_summary.csv", index=False)
    audits.to_csv(output_dir / "data_validation.csv", index=False)
    print("===== FORWARD OUTCOME STUDY V1 =====")
    print("Events:", len(outcomes))
    print("Broad:", int((outcomes["definition"] == "broad").sum()))
    print("Strict:", int((outcomes["definition"] == "strict").sum()))
    print("Output:", output_dir)
    print("\n===== HORIZON COMPLETENESS =====")
    for definition in ("broad", "strict"):
        subset = outcomes[outcomes["definition"] == definition]
        for horizon in HORIZONS:
            complete = int((subset[f"{horizon}_status"] == "complete").sum())
            print(f"{definition} {horizon}: complete={complete}, censored={len(subset)-complete}")
    print("\n===== DATA VALIDATION =====")
    print(audits.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--events",
        type=Path,
        default=Path("reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv"),
    )
    parser.add_argument(
        "--minute-dir", type=Path, default=Path.home() / "okx_scalping_data"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/sideways_rejection_forward_outcomes_v1"),
    )
    args = parser.parse_args()
    run(args.events, args.minute_dir, args.output)


if __name__ == "__main__":
    main()
