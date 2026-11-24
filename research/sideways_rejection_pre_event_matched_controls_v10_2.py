#!/usr/bin/env python3
"""Outcome-blind V10.2 covariate redundancy and matched-balance attribution."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates

def audit(eligible: pd.DataFrame, pairs: pd.DataFrame, correlations: pd.DataFrame):
    required={"event_id","definition","sequence_class","asset","direction",*COVARIATES}
    if not required.issubset(eligible.columns): raise ValueError("eligible covariate inputs incomplete")
    if eligible.event_id.duplicated().any(): raise ValueError("eligible event_id values must be unique")
    pair_required={"definition","target_caliper_robust_sd","separation_event_id","retest_event_id","asset","direction"}
    if not pair_required.issubset(pairs.columns): raise ValueError("V6 pair input incomplete")
    corr_required={"definition","asset","direction","sequence_class","scope","covariate_a","covariate_b","correlation","abs_correlation"}
    if not corr_required.issubset(correlations.columns): raise ValueError("V10.1 correlation input incomplete")
    valid_ids=set(eligible.event_id)
    if not set(pairs.separation_event_id).issubset(valid_ids) or not set(pairs.retest_event_id).issubset(valid_ids):
        raise ValueError("V6 pair references events outside frozen eligible cohort")
    ev=eligible.set_index("event_id",drop=False)
    # Correlation redundancy is summarized within sequence class and exact asset/direction.
    within=correlations[correlations.scope=="within_sequence_class"].copy()
    within["abs_correlation"]=pd.to_numeric(within.abs_correlation,errors="raise")
    within_summary=(within.groupby(["definition","covariate_a","covariate_b"],as_index=False)
      .agg(group_observations=("abs_correlation","count"),
           median_abs_correlation=("abs_correlation","median"),
           max_abs_correlation=("abs_correlation","max"),
           groups_ge_0_80=("abs_correlation",lambda x:int((x>=.80).sum())),
           groups_ge_0_90=("abs_correlation",lambda x:int((x>=.90).sum()))))
    # Balance uses V8's eligible pooled class SD within definition x asset x direction.
    rows=[]
    for (definition,caliper),cohort in pairs.groupby(["definition","target_caliper_robust_sd"],sort=True):
        for (asset,direction),g in cohort.groupby(["asset","direction"],sort=True):
            ref=eligible[(eligible.definition==definition)&(eligible.asset==asset)&(eligible.direction==direction)]
            a_ref=ref[ref.sequence_class==CLASSES[0]]
            b_ref=ref[ref.sequence_class==CLASSES[1]]
            if a_ref.empty or b_ref.empty: raise ValueError("matched stratum lacks one eligible class")
            a=ev.loc[g.separation_event_id]; b=ev.loc[g.retest_event_id]
            for cov in COVARIATES:
                av=pd.to_numeric(a[cov],errors="raise").to_numpy(float)
                bv=pd.to_numeric(b[cov],errors="raise").to_numpy(float)
                ar=pd.to_numeric(a_ref[cov],errors="raise").to_numpy(float)
                br=pd.to_numeric(b_ref[cov],errors="raise").to_numpy(float)
                ref_sd=float(np.sqrt((np.var(ar,ddof=1)+np.var(br,ddof=1))/2))
                diff=float(np.mean(av)-np.mean(bv))
                smd=diff/ref_sd if np.isfinite(ref_sd) and ref_sd>0 else np.nan
                rows.append({"definition":definition,"target_caliper_robust_sd":float(caliper),
                  "asset":asset,"direction":direction,"covariate":cov,"matched_pairs":len(g),
                  "eligible_reference_sd":ref_sd,"matched_mean_difference":diff,
                  "smd":smd,"abs_smd":abs(smd) if np.isfinite(smd) else np.nan})
    balance=pd.DataFrame(rows)
    attribution=(balance.groupby(["definition","target_caliper_robust_sd","covariate"],as_index=False)
      .agg(strata_count=("abs_smd","count"),median_abs_smd=("abs_smd","median"),
           mean_abs_smd=("abs_smd","mean"),max_abs_smd=("abs_smd","max"),
           strata_abs_smd_gt_0_10=("abs_smd",lambda x:int((x>.10).sum())),
           strata_abs_smd_gt_0_20=("abs_smd",lambda x:int((x>.20).sum()))))
    # Cross-reference high-correlation pairs against balance, without dropping either variable.
    high=within_summary[(within_summary.groups_ge_0_80>0)].copy()
    return within_summary,balance,attribution,high

def run(anatomy,sequence,feature_dir,minute_dir,pairs_path,correlations_path,output):
    if output.exists() and any(output.iterdir()): raise FileExistsError(f"Refusing non-empty output directory: {output}")
    eligible=build_covariates(anatomy,sequence,feature_dir,minute_dir)
    pairs=pd.read_csv(pairs_path); correlations=pd.read_csv(correlations_path)
    red,balance,attr,high=audit(eligible,pairs,correlations)
    output.mkdir(parents=True,exist_ok=True)
    red.to_csv(output/"within_group_redundancy_summary_v10_2.csv",index=False)
    balance.to_csv(output/"matched_balance_by_stratum_v10_2.csv",index=False)
    attr.to_csv(output/"covariate_imbalance_attribution_v10_2.csv",index=False)
    high.to_csv(output/"high_correlation_pairs_for_review_v10_2.csv",index=False)
    meta={"study":"Phase 3 V10.2 covariate redundancy and matched-balance attribution",
      "inputs":"Frozen eligible pre-event covariates, archived V6 matched pairs, archived V10.1 within-sequence correlation pairs",
      "balance_reference":"Eligible class-specific sample SD pooled within exact definition x asset x direction, consistent with V8 reference convention",
      "redundancy":"Summarizes repeated within-sequence absolute Pearson correlations >=0.80 and >=0.90; no variable is removed",
      "interpretation":"Outcome-blind descriptive audit only; no matching rules changed, no cohort approved, no outcomes loaded or compared",
      "limitations":["correlation does not establish redundancy or causal irrelevance","small groups produce unstable correlation and SMD estimates",
        "pairwise correlation summaries may overlap across definitions","SMDs are descriptive and do not prove exchangeability",
        "broad and strict definitions are nested","unmeasured confounding remains possible"]}
    (output/"run_metadata_v10_2.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print("Top imbalance covariates:")
    print(attr.sort_values("mean_abs_smd",ascending=False).groupby(["definition","target_caliper_robust_sd"]).head(5).to_string(index=False))
    print("Repeated high-correlation pairs:")
    print(red.sort_values(["groups_ge_0_90","max_abs_correlation"],ascending=False).head(15).to_string(index=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for x in ("anatomy","sequence","feature-dir","minute-dir","pairs","correlations","output"):
        p.add_argument("--"+x,type=Path,required=True)
    a=p.parse_args()
    run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.pairs,a.correlations,a.output)
if __name__=="__main__": main()
