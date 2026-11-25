#!/usr/bin/env python3
"""V10.10: outcome-blind joint common-support retention audit for Phase 3."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES,CLASSES,build_covariates
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES,CLASSES,build_covariates

KEYS=("definition","target_caliper_robust_sd")

def joint_support_audit(pairs:pd.DataFrame,eligible:pd.DataFrame):
    rp={"definition","target_caliper_robust_sd","pair_id","separation_event_id","retest_event_id","asset","direction"}
    re={"event_id","definition","sequence_class","asset","direction",*COVARIATES}
    if not rp.issubset(pairs.columns) or not re.issubset(eligible.columns):
        raise ValueError("V6 pairs or frozen eligible covariates missing required columns")
    if eligible.event_id.duplicated().any() or pairs.pair_id.isna().any():
        raise ValueError("Eligible event IDs must be unique and pair IDs non-null")
    ev=eligible.set_index("event_id",drop=False)
    details=[]
    for (definition,caliper),cohort in pairs.groupby(list(KEYS),sort=True):
        if cohort.pair_id.duplicated().any() or cohort.separation_event_id.duplicated().any() or cohort.retest_event_id.duplicated().any():
            raise ValueError("Pair IDs and endpoints must be unique within each cohort")
        ids=set(cohort.separation_event_id)|set(cohort.retest_event_id)
        if not ids.issubset(set(ev.index)):
            raise ValueError("Matched endpoint absent from frozen eligible cohort")
        sep=ev.loc[cohort.separation_event_id]; ret=ev.loc[cohort.retest_event_id]
        if not ((sep.asset.to_numpy()==ret.asset.to_numpy()).all() and (sep.direction.to_numpy()==ret.direction.to_numpy()).all()):
            raise ValueError("Matched endpoint asset/direction mismatch")
        if not ((sep.definition.to_numpy()==definition).all() and (ret.definition.to_numpy()==definition).all()):
            raise ValueError("Matched endpoint definition mismatch")
        for (asset,direction),g in cohort.groupby(["asset","direction"],sort=True):
            ref=eligible[(eligible.definition==definition)&(eligible.asset==asset)&(eligible.direction==direction)]
            x=ref[ref.sequence_class==CLASSES[0]]
            y=ref[ref.sequence_class==CLASSES[1]]
            if x.empty or y.empty: raise ValueError("Both eligible classes required for every matched stratum")
            used=[]; excluded_constant=[]; excluded_no_overlap=[]; bounds={}
            for cov in COVARIATES:
                xv=pd.to_numeric(x[cov],errors="raise").to_numpy(float)
                yv=pd.to_numeric(y[cov],errors="raise").to_numpy(float)
                if not np.isfinite(xv).all() or not np.isfinite(yv).all():
                    raise ValueError(f"Non-finite values in {cov}")
                if len(xv)<2 or len(yv)<2 or np.var(xv,ddof=1)<=0 or np.var(yv,ddof=1)<=0:
                    excluded_constant.append(cov); continue
                qx=np.quantile(xv,[.05,.95]); qy=np.quantile(yv,[.05,.95])
                lo=float(max(qx[0],qy[0])); hi=float(min(qx[1],qy[1]))
                if hi<lo:
                    excluded_no_overlap.append(cov); continue
                used.append(cov); bounds[cov]=(lo,hi)
            if excluded_no_overlap:
                xmask=np.zeros(len(x),dtype=bool); ymask=np.zeros(len(y),dtype=bool)
                amask=np.zeros(len(g),dtype=bool); bmask=np.zeros(len(g),dtype=bool)
            elif not used:
                xmask=np.ones(len(x),dtype=bool); ymask=np.ones(len(y),dtype=bool)
                amask=np.ones(len(g),dtype=bool); bmask=np.ones(len(g),dtype=bool)
            else:
                xmask=np.ones(len(x),dtype=bool); ymask=np.ones(len(y),dtype=bool)
                amask=np.ones(len(g),dtype=bool); bmask=np.ones(len(g),dtype=bool)
                a=ev.loc[g.separation_event_id]; b=ev.loc[g.retest_event_id]
                for cov,(lo,hi) in bounds.items():
                    xmask &= (pd.to_numeric(x[cov]).to_numpy(float)>=lo)&(pd.to_numeric(x[cov]).to_numpy(float)<=hi)
                    ymask &= (pd.to_numeric(y[cov]).to_numpy(float)>=lo)&(pd.to_numeric(y[cov]).to_numpy(float)<=hi)
                    amask &= (pd.to_numeric(a[cov]).to_numpy(float)>=lo)&(pd.to_numeric(a[cov]).to_numpy(float)<=hi)
                    bmask &= (pd.to_numeric(b[cov]).to_numpy(float)>=lo)&(pd.to_numeric(b[cov]).to_numpy(float)<=hi)
            both=amask&bmask
            details.append({
              "definition":definition,"target_caliper_robust_sd":caliper,"asset":asset,"direction":direction,
              "eligible_separation_n":len(x),"eligible_retest_n":len(y),
              "joint_support_dimensions":len(used),"constant_dimensions_excluded":len(excluded_constant),
              "nonoverlap_dimensions":len(excluded_no_overlap),
              "nonoverlap_covariates":";".join(excluded_no_overlap),
              "joint_support_separation_n":int(xmask.sum()),"joint_support_retest_n":int(ymask.sum()),
              "separation_retention_fraction":float(xmask.mean()),"retest_retention_fraction":float(ymask.mean()),
              "matched_pairs":len(g),"pairs_both_endpoints_in_joint_support":int(both.sum()),
              "matched_pair_retention_fraction":float(both.mean()),
              "acceptance_status":"NOT_ACCEPTED_FOR_OUTCOME_COMPARISON"
            })
    detail=pd.DataFrame(details)
    if detail.empty: raise ValueError("No matched strata available for joint support audit")
    summary=detail.groupby(list(KEYS),as_index=False).agg(
      represented_strata=("asset","count"),
      median_joint_dimensions=("joint_support_dimensions","median"),
      median_constant_dimensions_excluded=("constant_dimensions_excluded","median"),
      strata_with_any_nonoverlap_dimension=("nonoverlap_dimensions",lambda s:int((s>0).sum())),
      eligible_separation_events=("eligible_separation_n","sum"),
      eligible_retest_events=("eligible_retest_n","sum"),
      joint_support_separation_events=("joint_support_separation_n","sum"),
      joint_support_retest_events=("joint_support_retest_n","sum"),
      matched_pairs=("matched_pairs","sum"),
      pairs_both_endpoints_in_joint_support=("pairs_both_endpoints_in_joint_support","sum"),
      median_stratum_pair_retention=("matched_pair_retention_fraction","median"))
    summary["separation_joint_retention"]=summary.joint_support_separation_events/summary.eligible_separation_events
    summary["retest_joint_retention"]=summary.joint_support_retest_events/summary.eligible_retest_events
    summary["matched_pair_joint_retention"]=summary.pairs_both_endpoints_in_joint_support/summary.matched_pairs
    summary["acceptance_status"]="NOT_ACCEPTED_FOR_OUTCOME_COMPARISON"
    return detail.sort_values(list(KEYS)+["asset","direction"]),summary

def run(anatomy_path,sequence_path,feature_dir,minute_dir,pairs_path,output):
    anatomy_path=Path(anatomy_path);sequence_path=Path(sequence_path)
    feature_dir=Path(feature_dir);minute_dir=Path(minute_dir)
    pairs_path=Path(pairs_path);output=Path(output)
    eligible=build_covariates(anatomy_path,sequence_path,feature_dir,minute_dir)
    pairs=pd.read_csv(pairs_path)
    detail,summary=joint_support_audit(pairs,eligible)
    if output.exists() and any(output.iterdir()):raise FileExistsError(f"Refusing non-empty output directory: {output}")
    output.mkdir(parents=True,exist_ok=True)
    detail.to_csv(output/"joint_support_stratum_detail_v10_10.csv",index=False)
    summary.to_csv(output/"joint_support_summary_v10_10.csv",index=False)
    meta={
      "study":"Phase 3 V10.10 joint common-support retention audit",
      "reference":"Within definition x asset x direction, intersection of full eligible classes' central 5th-95th percentile intervals across all nonconstant covariates with overlapping intervals",
      "constant_dimensions":"Excluded from joint intersection and counted separately",
      "no_overlap_dimensions":"If any nonconstant covariate has disjoint central intervals, joint support is empty for that stratum",
      "matched_retention":"Fraction of original matched pairs for which both endpoints remain inside every joint-support interval",
      "limitations":["conservative univariate-interval intersection, not a multivariate density estimator","support restriction is diagnostic only; no pairs are rematched or outcomes compared","central 90% interval is descriptive, not an acceptance threshold","broad and strict cohorts are nested","no outcomes loaded; no trading inference"],
      "outcome_data_loaded":False,"acceptance_status":"No cohort accepted for outcome comparison"
    }
    (output/"run_metadata_v10_10.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(summary.to_string(index=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("anatomy","sequence","feature-dir","minute-dir","pairs","output"):p.add_argument("--"+arg,required=True)
    a=p.parse_args();run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.pairs,a.output)
if __name__=="__main__":main()
