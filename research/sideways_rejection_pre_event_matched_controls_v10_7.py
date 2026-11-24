#!/usr/bin/env python3
"""V10.7: outcome-blind sensitivity to minimum matched-pair subgroup size."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

MINIMUMS = (3, 5, 8, 10)
THRESHOLD = 0.10
REQUIRED = {"design","definition","target_caliper_robust_sd","asset_direction",
            "matched_pairs","covariate","abs_smd_after"}

def analyze(frame: pd.DataFrame):
    missing=REQUIRED-set(frame.columns)
    if missing: raise ValueError(f"Missing V10.5 columns: {sorted(missing)}")
    x=frame.copy()
    x["matched_pairs"]=pd.to_numeric(x["matched_pairs"],errors="raise")
    x["abs_smd_after"]=pd.to_numeric(x["abs_smd_after"],errors="coerce")
    keys=["design","definition","target_caliper_robust_sd"]
    detail=[]
    for minimum in MINIMUMS:
        x["eligible_stratum"]=x["matched_pairs"]>=minimum
        for key,g in x.groupby(keys+["covariate"],sort=True):
            eligible=g[g["eligible_stratum"] & g["abs_smd_after"].notna()]
            detail.append(dict(zip(["minimum_pairs"]+keys+["covariate"],[minimum]+list(key))) | {
                "strata_with_pairs":int(len(g)),
                "eligible_strata":int(len(eligible)),
                "eligible_strata_abs_smd_over_0_10":int((eligible["abs_smd_after"]>THRESHOLD).sum()),
                "median_eligible_abs_smd":float(eligible["abs_smd_after"].median()) if len(eligible) else None
            })
    d=pd.DataFrame(detail)
    summary=(d.groupby(["minimum_pairs"]+keys,as_index=False)
        .agg(covariates=("covariate","count"),
             covariates_with_eligible_strata=("eligible_strata",lambda s:int((s>0).sum())),
             median_eligible_strata_per_covariate=("eligible_strata","median"),
             covariates_median_abs_smd_over_0_10=("median_eligible_abs_smd",lambda s:int((s>THRESHOLD).sum())),
             imbalanced_cells=("eligible_strata_abs_smd_over_0_10","sum"),
             eligible_cells=("eligible_strata","sum")))
    summary["imbalance_rate"]=summary.apply(lambda r:r.imbalanced_cells/r.eligible_cells if r.eligible_cells else None,axis=1)
    summary["acceptance_status"]="NOT_ACCEPTED_FOR_OUTCOME_COMPARISON"
    return d,summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True); p.add_argument("--output",required=True)
    a=p.parse_args(); source=Path(a.input)
    if not source.is_file(): raise FileNotFoundError(source)
    d,s=analyze(pd.read_csv(source)); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    d.to_csv(out/"minimum_sample_sensitivity_detail_v10_7.csv",index=False)
    s.to_csv(out/"minimum_sample_sensitivity_summary_v10_7.csv",index=False)
    (out/"run_metadata_v10_7.json").write_text(json.dumps({
      "study":"Phase 3 V10.7 minimum subgroup-size sensitivity",
      "input":"asset_direction_covariate_balance_v10_5.csv",
      "minimum_pair_thresholds":list(MINIMUMS),"imbalance_threshold_abs_smd":THRESHOLD,
      "design_rows":int(len(s)),"detail_rows":int(len(d)),"outcome_data_loaded":False,
      "interpretation":"Outcome-blind diagnostic only; no cohort accepted for outcome comparison."
    },indent=2)+"\\n")
if __name__=="__main__": main()
