#!/usr/bin/env python3
"""Dependence-aware calendar-block bootstrap for rejection forward outcomes V1."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
COHORTS = {"broad": 1154, "strict": 838}
HORIZONS = ["15m", "1h", "4h", "24h"]
BLOCK_LENGTHS = [3, 7, 14]
DEFAULT_REPLICATES = 10_000
DEFAULT_SEED = 20261123
REQUIRED = [
    "event_id", "asset", "definition", "direction",
    "rejection_confirmed_at_ts_ms",
] + [f"{h}_{suffix}" for h in HORIZONS for suffix in (
    "status", "direction_adjusted_return"
)]


def load_and_validate(path: Path) -> tuple[pd.DataFrame, pd.DatetimeIndex]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing forward-outcome input: {path}")
    df = pd.read_csv(path)
    missing = [column for column in REQUIRED if column not in df.columns]
    if missing:
        raise ValueError(f"Input missing required columns: {missing}")
    if not set(df["asset"]).issubset(ASSETS) or set(df["asset"]) != set(ASSETS):
        raise ValueError("Input must contain exactly the five expected assets")
    if not set(df["definition"]).issubset(COHORTS):
        raise ValueError("Unknown cohort definition")
    if not set(df["direction"]).issubset({"upper", "lower"}):
        raise ValueError("Unknown direction")
    counts = df["definition"].value_counts().to_dict()
    if counts != COHORTS:
        raise ValueError(f"Cohort counts mismatch: expected {COHORTS}, got {counts}")
    if df.duplicated(["definition", "event_id"]).any():
        raise ValueError("Duplicate (definition, event_id) identity")
    ts = pd.to_numeric(df["rejection_confirmed_at_ts_ms"], errors="coerce")
    if ts.isna().any() or not np.isfinite(ts.to_numpy(dtype=float)).all():
        raise ValueError("Invalid confirmation timestamps")
    if (ts % 60_000 != 0).any():
        raise ValueError("Confirmation timestamps must align to the 1-minute grid")
    df = df.copy()
    df["rejection_confirmed_at_ts_ms"] = ts.astype("int64")
    day = pd.to_datetime(df["rejection_confirmed_at_ts_ms"], unit="ms", utc=True).dt.floor("D")
    df["calendar_day"] = day
    calendar = pd.date_range(day.min(), day.max(), freq="D", tz="UTC")
    if len(calendar) == 0:
        raise ValueError("Empty calendar range")
    for horizon in HORIZONS:
        status_col = f"{horizon}_status"
        return_col = f"{horizon}_direction_adjusted_return"
        if not set(df[status_col].dropna()).issubset({"complete", "incomplete"}):
            raise ValueError(f"Unknown {horizon} status")
        values = pd.to_numeric(df[return_col], errors="coerce")
        complete = df[status_col].eq("complete")
        if values[complete].isna().any() or not np.isfinite(values[complete].to_numpy(dtype=float)).all():
            raise ValueError(f"{horizon}: complete rows must have finite adjusted returns")
        if values[~complete].notna().any():
            raise ValueError(f"{horizon}: incomplete rows must not contain adjusted returns")
        df[return_col] = values
    return df, calendar


def sample_day_multiplicities(
    n_days: int, block_length: int, rng: np.random.Generator
) -> np.ndarray:
    """Sample moving contiguous blocks and return multiplicity for every calendar day."""
    if n_days < 1 or block_length < 1 or block_length > n_days:
        raise ValueError("Invalid calendar or block length")
    n_blocks = int(np.ceil(n_days / block_length))
    starts = rng.integers(0, n_days - block_length + 1, size=n_blocks)
    sampled = np.concatenate([
        np.arange(start, start + block_length, dtype=np.int64) for start in starts
    ])[:n_days]
    return np.bincount(sampled, minlength=n_days).astype(np.int64)


def contrast_from_sufficient_stats(
    weights: np.ndarray,
    upper_sum: np.ndarray,
    upper_n: np.ndarray,
    lower_sum: np.ndarray,
    lower_n: np.ndarray,
) -> np.ndarray:
    """Vectorized mean(upper)-mean(lower); NaN where either side is absent."""
    u_sum = weights @ upper_sum
    u_n = weights @ upper_n
    l_sum = weights @ lower_sum
    l_n = weights @ lower_n
    result = np.full(np.asarray(u_sum).shape, np.nan, dtype=float)
    valid = (u_n > 0) & (l_n > 0)
    result[valid] = u_sum[valid] / u_n[valid] - l_sum[valid] / l_n[valid]
    return result


def daily_sufficient_stats(
    subset: pd.DataFrame, calendar: pd.DatetimeIndex, horizon: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return day-indexed sums/counts, retaining calendar days with no events."""
    complete = subset[subset[f"{horizon}_status"].eq("complete")].copy()
    complete = complete[np.isfinite(complete[f"{horizon}_direction_adjusted_return"])]
    day_index = pd.Series(np.arange(len(calendar), dtype=np.int64), index=calendar)
    positions = complete["calendar_day"].map(day_index)
    if positions.isna().any():
        raise ValueError("An event day is outside the full calendar index")
    complete["_day_position"] = positions.astype("int64")
    arrays = []
    for direction in ("upper", "lower"):
        side = complete[complete["direction"].eq(direction)]
        grouped = side.groupby("_day_position")[f"{horizon}_direction_adjusted_return"].agg(["sum", "count"])
        sums = np.zeros(len(calendar), dtype=float)
        counts = np.zeros(len(calendar), dtype=float)
        if not grouped.empty:
            ix = grouped.index.to_numpy(dtype=np.int64)
            sums[ix] = grouped["sum"].to_numpy(dtype=float)
            counts[ix] = grouped["count"].to_numpy(dtype=float)
        arrays.extend([sums, counts])
    return tuple(arrays)


def run_bootstrap(
    df: pd.DataFrame,
    calendar: pd.DatetimeIndex,
    replicates: int = DEFAULT_REPLICATES,
    seed: int = DEFAULT_SEED,
    block_lengths: list[int] | None = None,
) -> pd.DataFrame:
    if replicates < 1:
        raise ValueError("replicates must be positive")
    block_lengths = block_lengths or BLOCK_LENGTHS
    if any(length < 1 or length > len(calendar) for length in block_lengths):
        raise ValueError("Block length must be between 1 and calendar length")
    rng = np.random.default_rng(seed)
    output = []
    n_days = len(calendar)

    for block_length in block_lengths:
        # One synchronous calendar resample per replicate is shared by every
        # cohort, horizon, asset, and direction.
        weight_matrix = np.empty((replicates, n_days), dtype=np.int16)
        for rep in range(replicates):
            weights = sample_day_multiplicities(n_days, block_length, rng)
            if int(weights.sum()) != n_days:
                raise AssertionError("Resampled calendar length changed")
            weight_matrix[rep] = weights

        for definition in ("broad", "strict"):
            cohort = df[df["definition"].eq(definition)]
            group_specs = [("ALL", cohort)] + [
                (asset, cohort[cohort["asset"].eq(asset)]) for asset in ASSETS
            ]
            for asset_group, subset in group_specs:
                for horizon in HORIZONS:
                    upper_sum, upper_n, lower_sum, lower_n = daily_sufficient_stats(
                        subset, calendar, horizon
                    )
                    point_u_n = int(upper_n.sum())
                    point_l_n = int(lower_n.sum())
                    if point_u_n == 0 or point_l_n == 0:
                        raise ValueError(f"No two-sided point estimate: {definition}/{asset_group}/{horizon}")
                    point_u = float(upper_sum.sum() / point_u_n)
                    point_l = float(lower_sum.sum() / point_l_n)
                    point = point_u - point_l
                    boot = contrast_from_sufficient_stats(
                        weight_matrix, upper_sum, upper_n, lower_sum, lower_n
                    )
                    valid = boot[np.isfinite(boot)]
                    lo, hi = (np.quantile(valid, [0.025, 0.975]) if len(valid) else (np.nan, np.nan))
                    output.append({
                        "definition": definition,
                        "asset_group": asset_group,
                        "horizon": horizon,
                        "block_length_days": block_length,
                        "events_total": int(len(subset)),
                        "complete_upper": point_u_n,
                        "complete_lower": point_l_n,
                        "censored_total": int(len(subset) - point_u_n - point_l_n),
                        "mean_upper": point_u,
                        "mean_lower": point_l,
                        "point_difference": point,
                        "ci_2_5": float(lo),
                        "ci_97_5": float(hi),
                        "valid_replicates": int(len(valid)),
                        "replicates_requested": int(replicates),
                        "seed": int(seed),
                    })
    return pd.DataFrame(output)


def run(
    input_path: Path,
    output_dir: Path,
    replicates: int = DEFAULT_REPLICATES,
    seed: int = DEFAULT_SEED,
) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to write into non-empty output directory: {output_dir}")
    df, calendar = load_and_validate(input_path)
    results = run_bootstrap(df, calendar, replicates=replicates, seed=seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_dir / "bootstrap_summary.csv", index=False)
    metadata = {
        "method": "synchronous moving UTC calendar-day block bootstrap",
        "input": str(input_path),
        "calendar_first_day": str(calendar.min()),
        "calendar_last_day": str(calendar.max()),
        "calendar_days_including_empty": int(len(calendar)),
        "days_with_events": int(df["calendar_day"].nunique()),
        "empty_calendar_days": int(len(calendar) - df["calendar_day"].nunique()),
        "cohort_counts": COHORTS,
        "block_lengths_days": BLOCK_LENGTHS,
        "replicates": int(replicates),
        "seed": int(seed),
        "primary_estimand": "broad / ALL assets / 24h / mean(upper)-mean(lower)",
        "units": "decimal return; multiply by 100 for percentage points",
        "strict_is_nested_sensitivity_not_independent_replication": True,
        "interpretation": "descriptive uncertainty only; not a trading-edge or profitability test",
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print("BOOTSTRAP COMPLETE")
    print(f"Rows: {len(results)}")
    print(f"Calendar days: {len(calendar)} (empty: {len(calendar) - df['calendar_day'].nunique()})")
    print(f"Replicates per block length: {replicates}")
    primary = results[
        results["definition"].eq("broad")
        & results["asset_group"].eq("ALL")
        & results["horizon"].eq("24h")
    ].sort_values("block_length_days")
    print("\nPRIMARY: BROAD ALL-ASSET 24H UPPER-LOWER MEAN DIFFERENCE")
    print(primary[[
        "block_length_days", "point_difference", "ci_2_5", "ci_97_5",
        "valid_replicates", "complete_upper", "complete_lower",
    ]].to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("reports/sideways_rejection_forward_outcomes_v1/event_level_outcomes.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/rejection_outcome_block_bootstrap_v1"),
    )
    parser.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()
    run(args.input, args.output, args.replicates, args.seed)


if __name__ == "__main__":
    main()
