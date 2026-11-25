#!/usr/bin/env python3
"""V10.8: outcome-blind ranking of persistent covariate imbalance across V10.7 thresholds."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

REQUIRED={"minimum_pairs","design","definition","target_caliper_robust_sd","covariate",
          "strata_with_pairs","eligible_strata","eligible_strata_abs_smd_over_0_10",
          "median_eligible_abs_smd"}
THRESHOLD=0.10

def analyze(frame: pd.DataFrame):
    missing=REQUIRED-set(frame.columns)
    if missing: raise ValueError(f"Missing V10.7 detail columns: {sorted(missing)}")
    x=frame.copy()
    for c in ("minimum_pairs","strata_with_pairs","eligible_strata","eligible_strata_abs_smd_over_0_10"):
        x[c]=pd.to_numeric(x[c],errors="raise")
    x["median_eligible_abs_smd"]=pd.to_numeric(x["median_eligible_abs_smd"],errors="coerce")
    if (x["eligible_strata_abs_smd_over_0_10"]>x["eligible_strata"]).any():
        raise ValueError("Imbalanced strata cannot exceed eligible strata")
    if (x["eligible_strata"]>x["strata_with_pairs"]).any():
        raise ValueError("Eligible strata cannot exceed strata with pairs")
    keys=["minimum_pairs","covariate"]
    persistence=(x.groupby(keys,as_index=False).agg(
        design_cells=("design","count"),
        eligible_design_cells=("eligible_strata",lambda s:int((s>0).sum())),
        eligible_stratum_cells=("eligible_strata","sum"),
        imbalanced_stratum_cells=("eligible_strata_abs_smd_over_0_10","sum"),
        median_cell_abs_smd=("median_eligible_abs_smd","median"),
        covariate_designs=("design","nunique")))
    persistence["imbalance_rate"]=persistence.apply(
        lambda r:r.imbalanced_stratum_cells/r.eligible_stratum_cells if r.eligible_stratum_cells else None,axis=1)
    persistence["imbalance_rate_rank"]=persistence.groupby("minimum_pairs")["imbalance_rate"].rank(
        method="min",ascending=False).astype("Int64")
    persistence["interpretation"]="Repeated design cells are sensitivity diagnostics, not independent samples"
    design=x.groupby(["minimum_pairs","design","definition","target_caliper_robust_sd"],as_index=False).agg(
        covariates=("covariate","nunique"),
        eligible_stratum_cells=("eligible_strata","sum"),
        imbalanced_stratum_cells=("eligible_strata_abs_smd_over_0_10","sum"),
        covariates_with_median_abs_smd_over_0_10=("median_eligible_abs_smd",lambda s:int((s>THRESHOLD).sum())))
    design["imbalance_rate"]=design.apply(
        lambda r:r.imbalanced_stratum_cells/r.eligible_stratum_cells if r.eligible_stratum_cells else None,axis=1)
    design["acceptance_status"]="NOT_ACCEPTED_FOR_OUTCOME_COMPARISON"
    return persistence.sort_values(["minimum_pairs","imbalance_rate_rank","covariate"]),design

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",required=True); p.add_argument("--output",required=True)
    a=p.parse_args()
    source=Path(a.input)
    if not source.is_file(): raise FileNotFoundError(source)
    persistence,design=analyze(pd.read_csv(source))
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    persistence.to_csv(out/"covariate_imbalance_persistence_v10_8.csv",index=False)
    design.to_csv(out/"design_balance_persistence_v10_8.csv",index=False)
    (out/"run_metadata_v10_8.json").write_text(json.dumps({
      "study":"Phase 3 V10.8 covariate imbalance persistence",
      "input":"minimum_sample_sensitivity_detail_v10_7.csv",
      "minimum_pair_thresholds":sorted(pd.to_numeric(persistence.minimum_pairs).unique().tolist()),
      "imbalance_threshold_abs_smd":THRESHOLD,
      "covariate_rows":int(len(persistence)),"design_rows":int(len(design)),
      "outcome_data_loaded":False,
      "interpretation":"Outcome-blind descriptive ranking; repeated designs are not independent observations; no cohort accepted for outcome comparison."
    },indent=2)+"\\n")
if __name__=="__main__": main()
