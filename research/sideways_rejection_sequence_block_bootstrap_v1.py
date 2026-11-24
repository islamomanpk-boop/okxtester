#!/usr/bin/env python3
"""Calendar moving-block bootstrap for descriptive sideways rejection sequence contrasts V1."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

CLASSES = ("SEPARATION_FIRST", "RETEST_FIRST")
HORIZONS = ("1h", "4h", "24h")
METRICS = (
    "final_close_direction_adjusted_midpoint_width",
    "max_inward_excursion_width",
    "max_outward_penetration_width",
)


def _day_index(ts_ms: pd.Series, first_day: pd.Timestamp) -> np.ndarray:
    dates = pd.to_datetime(ts_ms, unit="ms", utc=True).dt.floor("D")
    return ((dates - first_day) / pd.Timedelta(days=1)).to_numpy(dtype=np.int64)


def moving_block_contrast(values: pd.DataFrame, *, block_days: int, replicates: int,
                          rng: np.random.Generator) -> dict:
    """Bootstrap mean(class A)-mean(class B), resampling shared calendar blocks."""
    if block_days < 1 or replicates < 1:
        raise ValueError("block_days and replicates must be positive")
    data = values.copy()
    data["day"] = pd.to_datetime(data.confirmation_ts_ms, unit="ms", utc=True).dt.floor("D")
    first_day, last_day = data.day.min(), data.day.max()
    n_days = int((last_day - first_day) / pd.Timedelta(days=1)) + 1
    day_ix = ((data.day - first_day) / pd.Timedelta(days=1)).to_numpy(dtype=np.int64)
    block_days = min(block_days, n_days)
    starts = np.arange(n_days - block_days + 1, dtype=np.int64)
    daily = {}
    for label in CLASSES:
        subset = data[data.sequence_class == label]
        sums = np.zeros(n_days, dtype=float)
        counts = np.zeros(n_days, dtype=float)
        valid = subset.metric.notna().to_numpy()
        np.add.at(sums, day_ix[data.sequence_class.to_numpy() == label][valid],
                  subset.metric.to_numpy(dtype=float)[valid])
        np.add.at(counts, day_ix[data.sequence_class.to_numpy() == label][valid], 1)
        daily[label] = (sums, counts)
    observed_means = {}
    for label in CLASSES:
        s, c = daily[label]
        observed_means[label] = float(s.sum() / c.sum()) if c.sum() else np.nan
    observed = observed_means[CLASSES[0]] - observed_means[CLASSES[1]]
    if not np.isfinite(observed):
        return {"observed_difference": np.nan, "ci_2_5": np.nan, "ci_97_5": np.nan,
                "valid_replicates": 0, "replicates": replicates,
                "class_a_n": int((data.sequence_class == CLASSES[0]).sum()),
                "class_b_n": int((data.sequence_class == CLASSES[1]).sum())}
    blocks_per_draw = int(np.ceil(n_days / block_days))
    boot = []
    offsets = np.arange(block_days, dtype=np.int64)
    for _ in range(replicates):
        sampled = (rng.choice(starts, size=blocks_per_draw, replace=True)[:, None] + offsets).ravel()
        multiplicity = np.bincount(sampled, minlength=n_days).astype(float)
        means = []
        for label in CLASSES:
            sums, counts = daily[label]
            denom = float(np.dot(counts, multiplicity))
            means.append(float(np.dot(sums, multiplicity) / denom) if denom else np.nan)
        if np.isfinite(means).all():
            boot.append(means[0] - means[1])
    ci = np.quantile(boot, [0.025, 0.975]) if boot else [np.nan, np.nan]
    return {"observed_difference": float(observed), "ci_2_5": float(ci[0]),
            "ci_97_5": float(ci[1]), "valid_replicates": len(boot),
            "replicates": replicates,
            "class_a_n": int((data.sequence_class == CLASSES[0]).sum()),
            "class_b_n": int((data.sequence_class == CLASSES[1]).sum())}


def run(sequence_path: Path, outcomes_path: Path, output_dir: Path,
        replicates: int = 10000, seed: int = 20261124, blocks=(3, 7, 14)) -> pd.DataFrame:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output_dir}")
    seq = pd.read_csv(sequence_path)
    out = pd.read_csv(outcomes_path)
    required_seq = {"event_id", "definition", "sequence_class", "confirmation_ts_ms"}
    required_out = {"event_id", "definition", "horizon", "status", *METRICS}
    if not required_seq.issubset(seq.columns) or not required_out.issubset(out.columns):
        raise ValueError("Input files are missing required columns")
    if seq.event_id.duplicated().any() or out.duplicated(["event_id", "horizon"]).any():
        raise ValueError("Duplicate event or event-horizon identity")
    if not set(seq.sequence_class).issubset(set(CLASSES) | {"NEITHER_WITHIN_15M", "SAME_BAR_AMBIGUOUS", "INCOMPLETE_CLASSIFICATION"}):
        raise ValueError("Unknown sequence class")
    joined = out.merge(seq[["event_id", "definition", "sequence_class", "confirmation_ts_ms"]],
                       on=["event_id", "definition"], how="left", validate="many_to_one",
                       suffixes=("", "_sequence"))
    if joined.sequence_class.isna().any() or (joined.confirmation_ts_ms != joined.confirmation_ts_ms_sequence).any():
        raise ValueError("Outcome-to-sequence join mismatch")
    joined = joined[(joined.status == "complete") & joined.sequence_class.isin(CLASSES)].copy()
    rng = np.random.default_rng(seed)
    rows = []
    for definition in ("broad", "strict"):
        for horizon in HORIZONS:
            base = joined[(joined.definition == definition) & (joined.horizon == horizon)]
            for metric in METRICS:
                sample = base[["confirmation_ts_ms", "sequence_class", metric]].rename(columns={metric: "metric"})
                for block in blocks:
                    result = moving_block_contrast(sample, block_days=block, replicates=replicates, rng=rng)
                    rows.append({"definition": definition, "horizon": horizon, "metric": metric,
                                 "block_days": block, "class_a": CLASSES[0], "class_b": CLASSES[1],
                                 **result})
    result_df = pd.DataFrame(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(output_dir / "block_bootstrap_contrasts_v1.csv", index=False)
    metadata = {
        "study": "Sideways Rejection Sequence Calendar Moving-Block Bootstrap V1",
        "seed": seed, "replicates_per_contrast": replicates, "block_lengths_days": list(blocks),
        "contrast": "mean(SEPARATION_FIRST) minus mean(RETEST_FIRST)",
        "resampling_unit": "shared UTC calendar-day blocks across all five assets in each cohort",
        "cohorts": ["broad", "strict"], "strict_is_nested_within_broad": True,
        "horizons": list(HORIZONS), "metrics": list(METRICS),
        "inclusion": "complete follow-through rows for the two named sequence classes only",
        "limitations": ["descriptive observational contrast, not causal or a trading strategy",
                        "overlapping events may remain dependent within blocks",
                        "percentile intervals do not correct for multiple comparisons",
                        "broad and strict cohorts are nested, not independent",
                        "block bootstrap does not remove selection or regime confounding"]
    }
    (output_dir / "run_metadata_v1.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(result_df)} bootstrap contrasts to {output_dir}")
    return result_df


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sequence", type=Path, required=True)
    p.add_argument("--outcomes", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--replicates", type=int, default=10000)
    p.add_argument("--seed", type=int, default=20261124)
    a = p.parse_args()
    run(a.sequence, a.outcomes, a.output, a.replicates, a.seed)


if __name__ == "__main__":
    main()
