#!/usr/bin/env python3
"""V10.9: outcome-blind empirical distribution overlap audit for Phase 3 matched cohorts."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, wasserstein_distance
try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates

KEYS=("definition","target_caliper_robust_sd")

def _finite(values):
    x=pd.to_numeric(pd.Series(values),errors="raise").to_numpy(dtype=float)
    if not np.isfinite(x).all():
        raise ValueError("Non-finite covariate values in frozen eligible cohort")
    return x

def audit_distributional_overlap(pairs:pd.DataFrame, eligible:pd.DataFrame):
    rp={"definition","target_caliper_robust_sd","pair_id","separation_event_id","retest_event_id","asset","direction"}
    re={"event_id","definition","sequence_class","asset","direction",*COVARIATES}
    if not rp.issubset(pairs.columns) or not re.issubset(eligible.columns):
        raise ValueError("V6 pairs or rebuilt eligible covariates missing required columns")
    if eligible.event_id.duplicated().any() or pairs.pair_id.isna().any():
        raise ValueError("Eligible event IDs must be unique and pair IDs non-null")
    ev=eligible.set_index("event_id",drop=False)
    rows=[]
    for (definition,caliper),cohort in pairs.groupby(list(KEYS),sort=True):
        if cohort.pair_id.duplicated().any() or cohort.separation_event_id.duplicated().any() or cohort.retest_event_id.duplicated().any():
            raise ValueError("Pair IDs and matched endpoints must be unique within cohort")
        ids=set(cohort.separation_event_id)|set(cohort.retest_event_id)
        if not ids.issubset(set(ev.index)):
            raise ValueError("Matched endpoint absent from rebuilt eligible cohort")
        sep=ev.loc[cohort.separation_event_id]
        ret=ev.loc[cohort.retest_event_id]
        if not ((sep.asset.to_numpy()==ret.asset.to_numpy()).all() and (sep.direction.to_numpy()==ret.direction.to_numpy()).all()):
            raise ValueError("Matched endpoint asset/direction mismatch")
        if not ((sep.definition.to_numpy()==definition).all() and (ret.definition.to_numpy()==definition).all()):
            raise ValueError("Matched endpoint definition mismatch")
        for (asset,direction),g in cohort.groupby(["asset","direction"],sort=True):
            ref=eligible[(eligible.definition==definition)&(eligible.asset==asset)&(eligible.direction==direction)]
            xref=ref[ref.sequence_class==CLASSES[0]]
            yref=ref[ref.sequence_class==CLASSES[1]]
            if xref.empty or yref.empty:
                raise ValueError("Both eligible sequence classes are required in every represented stratum")
            a=ev.loc[g.separation_event_id]; b=ev.loc[g.retest_event_id]
            for cov in COVARIATES:
                x=_finite(xref[cov]); y=_finite(yref[cov])
                ax=_finite(a[cov]); by=_finite(b[cov])
                pooled_sd=float(np.sqrt((np.var(x,ddof=1)+np.var(y,ddof=1))/2)) if len(x)>1 and len(y)>1 else np.nan
                qx=np.quantile(x,[.05,.95]); qy=np.quantile(y,[.05,.95])
                lo,hi=max(qx[0],qy[0]),min(qx[1],qy[1])
                union_lo,union_hi=min(qx[0],qy[0]),max(qx[1],qy[1])
                overlap=max(0.0,hi-lo)/(union_hi-union_lo) if union_hi>union_lo else np.nan
                inside=float((np.sum((ax>=lo)&(ax<=hi))+np.sum((by>=lo)&(by<=hi)))/(2*len(g))) if hi>=lo else 0.0
                med_gap=float(np.median(x)-np.median(y))
                rows.append({
                  "definition":definition,"target_caliper_robust_sd":caliper,"asset":asset,"direction":direction,
                  "covariate":cov,"eligible_separation_n":len(x),"eligible_retest_n":len(y),"matched_pairs":len(g),
                  "ks_statistic":float(ks_2samp(x,y,method="auto").statistic),
                  "wasserstein_distance":float(wasserstein_distance(x,y)),
                  "wasserstein_distance_pooled_sd":float(wasserstein_distance(x,y)/pooled_sd) if np.isfinite(pooled_sd) and pooled_sd>0 else np.nan,
                  "median_difference":med_gap,
                  "median_difference_pooled_sd":float(med_gap/pooled_sd) if np.isfinite(pooled_sd) and pooled_sd>0 else np.nan,
                  "separation_p05":float(qx[0]),"separation_p95":float(qx[1]),
                  "retest_p05":float(qy[0]),"retest_p95":float(qy[1]),
                  "central90_range_overlap_ratio":float(overlap) if np.isfinite(overlap) else np.nan,
                  "matched_endpoints_inside_shared_central90_fraction":inside,
                  "interpretation":"Descriptive distribution diagnostics; KS statistic is not an inferential test here"
                })
    detail=pd.DataFrame(rows)
    if detail.empty: raise ValueError("No matched strata were available for V10.9")
    summary=(detail.groupby(list(KEYS),as_index=False).agg(
      represented_asset_direction_strata=("asset","count"),
      covariate_stratum_cells=("covariate","count"),
      median_ks_statistic=("ks_statistic","median"),
      median_wasserstein_pooled_sd=("wasserstein_distance_pooled_sd","median"),
      median_abs_median_gap_pooled_sd=("median_difference_pooled_sd",lambda s:float(s.abs().median())),
      median_central90_range_overlap=("central90_range_overlap_ratio","median"),
      median_matched_endpoint_inside_shared_range=("matched_endpoints_inside_shared_central90_fraction","median"),
      cells_ks_at_least_0_25=("ks_statistic",lambda s:int((s>=.25).sum())),
      cells_wasserstein_over_0_20_sd=("wasserstein_distance_pooled_sd",lambda s:int((s>.20).sum())),
      cells_endpoint_inside_fraction_below_0_80=("matched_endpoints_inside_shared_central90_fraction",lambda s:int((s<.80).sum()))
    ))
    summary["acceptance_status"]="NOT_ACCEPTED_FOR_OUTCOME_COMPARISON"
    return detail.sort_values(list(KEYS)+["asset","direction","covariate"]),summary

def run(anatomy_path,sequence_path,feature_dir,minute_dir,pairs_path,output):
    anatomy_path=Path(anatomy_path); sequence_path=Path(sequence_path)
    feature_dir=Path(feature_dir); minute_dir=Path(minute_dir)
    pairs_path=Path(pairs_path); output=Path(output)
    eligible=build_covariates(anatomy_path,sequence_path,feature_dir,minute_dir)
    pairs=pd.read_csv(pairs_path)
    detail,summary=audit_distributional_overlap(pairs,eligible)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output}")
    output.mkdir(parents=True,exist_ok=True)
    detail.to_csv(output/"distributional_overlap_detail_v10_9.csv",index=False)
    summary.to_csv(output/"distributional_overlap_summary_v10_9.csv",index=False)
    meta={
      "study":"Phase 3 V10.9 empirical distributional overlap audit",
      "inputs":"Archived outcome-blind V6 pairs and independently rebuilt frozen eligible pre-event covariates",
      "reference":"Full eligible separation and retest classes within definition x asset x direction, before matching",
      "diagnostics":["two-sample empirical KS distance (statistic only; no inferential p-values)","1D Wasserstein distance normalized by pooled class SD","median difference normalized by pooled class SD","intersection of central 5th-95th percentile ranges","fraction of matched endpoints inside shared central range"],
      "thresholds":{"ks_0_25":"descriptive flag only","wasserstein_over_0_20_pooled_sd":"descriptive flag only","matched_endpoint_inside_below_0_80":"descriptive flag only"},
      "limitations":["univariate diagnostics do not establish multivariate common support","KS statistic is not used as an inferential hypothesis test","matched endpoints are selected observations; support diagnostics are descriptive","broad and strict cohorts are nested","no outcomes are loaded or compared; no trading inference is made"],
      "outcome_data_loaded":False,"acceptance_status":"No cohort accepted for outcome comparison"
    }
    (output/"run_metadata_v10_9.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(summary.to_string(index=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("anatomy","sequence","feature-dir","minute-dir","pairs","output"):
        p.add_argument("--"+arg,required=True)
    a=p.parse_args()
    run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.pairs,a.output)
if __name__=="__main__": main()

# V10.9 execution trigger: workflow and test files are committed on price-action-v1.

# Re-run after correcting CLI path normalization for GitHub Actions.
