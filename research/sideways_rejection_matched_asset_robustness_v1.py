#!/usr/bin/env python3
"""Asset-level and leave-one-asset-out robustness for Phase 3 matched pairs V1."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

HORIZONS = ("1h", "4h", "24h")
METRICS = ("final_close_direction_adjusted_midpoint_width",
           "max_inward_excursion_width", "max_outward_penetration_width")
ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")


def paired_block_bootstrap(frame: pd.DataFrame, *, block_days: int,
                           replicates: int, rng: np.random.Generator) -> dict:
    if len(frame) < 5:
        return {"ci_2_5": np.nan, "ci_97_5": np.nan,
                "valid_replicates": 0, "bootstrap_status": "too_few_pairs"}
    d = frame.copy()
    d["day"] = pd.to_datetime(d.pair_confirmation_ts_ms, unit="ms", utc=True).dt.floor("D")
    first, last = d.day.min(), d.day.max()
    n_days = int((last-first)/pd.Timedelta(days=1))+1
    day_ix = ((d.day-first)/pd.Timedelta(days=1)).to_numpy(dtype=np.int64)
    sums, counts = np.zeros(n_days), np.zeros(n_days)
    np.add.at(sums, day_ix, d.difference.to_numpy(dtype=float))
    np.add.at(counts, day_ix, 1)
    block_days = min(block_days, n_days)
    starts = np.arange(n_days-block_days+1)
    offsets = np.arange(block_days)
    nblocks = int(np.ceil(n_days/block_days))
    boot = []
    for _ in range(replicates):
        ix = (rng.choice(starts, size=nblocks, replace=True)[:, None]+offsets).ravel()
        mult = np.bincount(ix, minlength=n_days).astype(float)
        denom = float(np.dot(counts, mult))
        if denom:
            boot.append(float(np.dot(sums, mult)/denom))
    ci = np.quantile(boot, [.025, .975]) if boot else [np.nan, np.nan]
    return {"ci_2_5": float(ci[0]), "ci_97_5": float(ci[1]),
            "valid_replicates": len(boot), "bootstrap_status": "complete"}


def run(pairs_path: Path, outcomes_path: Path, output_dir: Path,
        replicates: int = 10000, seed: int = 20261124, blocks=(3, 7, 14)) -> pd.DataFrame:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output_dir}")
    pairs = pd.read_csv(pairs_path)
    outcomes = pd.read_csv(outcomes_path)
    required_pairs = {"pair_id", "definition", "asset", "pair_confirmation_ts_ms",
                      "separation_event_id", "retest_event_id"}
    if not required_pairs.issubset(pairs.columns):
        raise ValueError("matched pair file missing required columns")
    if pairs.duplicated(["definition", "pair_id"]).any():
        raise ValueError("duplicate matched pair identity")
    rng = np.random.default_rng(seed)
    rows, counts_rows = [], []
    for definition in ("broad", "strict"):
        p = pairs[pairs.definition == definition].copy()
        for asset in ASSETS:
            counts_rows.append({"definition": definition, "asset": asset,
                                "matched_pairs": int((p.asset == asset).sum())})
        for horizon in HORIZONS:
            h = outcomes[(outcomes.definition == definition) &
                         (outcomes.horizon == horizon) &
                         (outcomes.status == "complete")].set_index("event_id")
            for metric in METRICS:
                diffs = []
                for pair in p.itertuples(index=False):
                    if pair.separation_event_id not in h.index or pair.retest_event_id not in h.index:
                        continue
                    a = h.at[pair.separation_event_id, metric]
                    b = h.at[pair.retest_event_id, metric]
                    if pd.notna(a) and pd.notna(b):
                        diffs.append({"pair_id": pair.pair_id, "asset": pair.asset,
                                      "pair_confirmation_ts_ms": pair.pair_confirmation_ts_ms,
                                      "difference": float(a-b)})
                base = pd.DataFrame(diffs, columns=["pair_id", "asset", "pair_confirmation_ts_ms", "difference"])
                scopes = [("ALL_ASSETS", base)]
                for asset in ASSETS:
                    scopes.append((f"ASSET_{asset}", base[base.asset == asset]))
                    scopes.append((f"EXCLUDING_{asset}", base[base.asset != asset]))
                for scope, sample in scopes:
                    for block in blocks:
                        boot = paired_block_bootstrap(sample, block_days=block,
                            replicates=replicates, rng=rng)
                        rows.append({"definition": definition, "horizon": horizon,
                            "metric": metric, "scope": scope, "block_days": block,
                            "pairs": len(sample),
                            "mean_difference": float(sample.difference.mean()) if len(sample) else np.nan,
                            "median_difference": float(sample.difference.median()) if len(sample) else np.nan,
                            "replicates": replicates, **boot})
    output_dir.mkdir(parents=True, exist_ok=True)
    result = pd.DataFrame(rows)
    result.to_csv(output_dir/"asset_robustness_contrasts_v1.csv", index=False)
    pd.DataFrame(counts_rows).to_csv(output_dir/"asset_pair_counts_v1.csv", index=False)
    metadata = {"study":"Phase 3 Matched-Pair Asset Heterogeneity and Leave-One-Asset-Out V1",
        "input_matching":"V4 exact-asset/direction 1:1 matched pairs with 30-day time-gap limit",
        "contrast":"paired outcome difference: SEPARATION_FIRST minus RETEST_FIRST",
        "scopes":"all assets, each asset alone, and leave-one-asset-out",
        "bootstrap":"paired differences resampled in UTC calendar-day moving blocks",
        "block_lengths_days":list(blocks),"replicates_per_scope_contrast":replicates,"seed":seed,
        "minimum_pairs_for_bootstrap":5,
        "limitations":["small asset-specific samples may have no bootstrap interval",
            "leave-one-asset-out estimates remain observational and are not independent",
            "broad and strict cohorts are nested",
            "many asset/scope/horizon/metric comparisons are exploratory; no multiple-testing correction",
            "does not remove residual covariate imbalance or unmeasured confounding"]}
    (output_dir/"run_metadata_v1.json").write_text(json.dumps(metadata,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {len(result)} asset robustness contrasts")
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pairs",type=Path,required=True)
    p.add_argument("--outcomes",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--replicates",type=int,default=10000)
    p.add_argument("--seed",type=int,default=20261124)
    a=p.parse_args()
    run(a.pairs,a.outcomes,a.output,a.replicates,a.seed)


if __name__=="__main__":
    main()
