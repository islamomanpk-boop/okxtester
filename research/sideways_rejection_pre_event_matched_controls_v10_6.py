#!/usr/bin/env python3
"""V10.6: outcome-blind synthesis of V10.5 asset-direction balance diagnostics."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

INPUT = "asset_direction_covariate_balance_v10_5.csv"
MIN_PAIRS = 5
THRESHOLD = 0.10

def summarize(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = {"design","definition","target_caliper_robust_sd","asset_direction",
                "matched_pairs","covariate","abs_smd_after","small_stratum_flag"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing V10.5 columns: {sorted(missing)}")
    x = frame.copy()
    x["matched_pairs"] = pd.to_numeric(x["matched_pairs"], errors="raise")
    x["abs_smd_after"] = pd.to_numeric(x["abs_smd_after"], errors="coerce")
    x["stable"] = x["matched_pairs"] >= MIN_PAIRS
    keys = ["design","definition","target_caliper_robust_sd","covariate"]
    rows = []
    for key, group in x.groupby(keys, sort=True):
        stable = group[group["stable"] & group["abs_smd_after"].notna()]
        all_valid = group[group["abs_smd_after"].notna()]
        rows.append(dict(zip(keys,key)) | {
            "asset_direction_strata_with_pairs": int(len(group)),
            "stable_strata_n": int(len(stable)),
            "stable_strata_abs_smd_over_0_10": int((stable["abs_smd_after"] > THRESHOLD).sum()),
            "stable_strata_abs_smd_over_0_20": int((stable["abs_smd_after"] > 0.20).sum()),
            "stable_median_abs_smd": float(stable["abs_smd_after"].median()) if len(stable) else None,
            "all_valid_median_abs_smd": float(all_valid["abs_smd_after"].median()) if len(all_valid) else None,
            "unstable_strata_n": int((~group["stable"]).sum()),
            "interpretation": "no_stable_strata" if len(stable)==0 else "descriptive_only"
        })
    detail = pd.DataFrame(rows)
    overall = (detail.groupby(["design","definition","target_caliper_robust_sd"], as_index=False)
        .agg(covariates=("covariate","count"),
             covariates_with_any_stable_strata=("stable_strata_n", lambda s: int((s>0).sum())),
             median_stable_strata_per_covariate=("stable_strata_n","median"),
             median_covariate_stable_median_abs_smd=("stable_median_abs_smd","median"),
             covariates_with_median_abs_smd_over_0_10=("stable_median_abs_smd",lambda s: int((s>THRESHOLD).sum())),
             total_stable_strata_imbalanced_cells=("stable_strata_abs_smd_over_0_10","sum"),
             total_stable_strata_cells=("stable_strata_n","sum"),
             total_unstable_strata_cells=("unstable_strata_n","sum")))
    overall["stable_cell_imbalance_rate"] = overall.apply(
        lambda r: r.total_stable_strata_imbalanced_cells/r.total_stable_strata_cells
        if r.total_stable_strata_cells else None, axis=1)
    overall["acceptance_status"] = "NOT_ACCEPTED_FOR_OUTCOME_COMPARISON"
    return detail, overall

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    source=Path(args.input)
    if not source.is_file(): raise FileNotFoundError(source)
    detail, overall=summarize(pd.read_csv(source))
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    detail.to_csv(out/"stable_stratum_balance_persistence_v10_6.csv",index=False)
    overall.to_csv(out/"design_level_balance_synthesis_v10_6.csv",index=False)
    import json
    (out/"run_metadata_v10_6.json").write_text(json.dumps({
      "study":"Phase 3 V10.6 stable-stratum balance persistence synthesis",
      "input":INPUT,"minimum_pairs_per_stratum":MIN_PAIRS,
      "imbalance_threshold_abs_smd":THRESHOLD,
      "designs":int(overall[["design","definition","target_caliper_robust_sd"]].drop_duplicates().shape[0]),
      "detail_rows":int(len(detail)),"outcome_data_loaded":False,
      "interpretation":"Descriptive balance audit only; no cohort accepted and no outcome comparison."
    },indent=2)+"\n")
if __name__=="__main__": main()
