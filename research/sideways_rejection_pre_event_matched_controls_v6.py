#!/usr/bin/env python3
"""Outcome-blind V6: compare maximum-cardinality optimal matching with V5 greedy matching."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from research.sideways_rejection_pre_event_matched_controls_v4 import (
    COVARIATES, CLASSES, build_covariates, robust_scale, smd,
)
from research.sideways_rejection_pre_event_matched_controls_v5 import CALIPERS, TARGET

def optimal_match(frame: pd.DataFrame, target_caliper: float, max_distance: float=2.0,
                  max_component: float=1.5, max_time_gap_days: float=30.0) -> pd.DataFrame:
    if target_caliper <= 0 or max_distance <= 0 or max_component <= 0 or max_time_gap_days < 0:
        raise ValueError("calipers must be positive and time gap non-negative")
    required={"event_id","sequence_class","asset","direction","confirmation_ts_ms",*COVARIATES}
    if not required.issubset(frame.columns):
        raise ValueError("matching frame is missing required columns")
    data=frame[frame.sequence_class.isin(CLASSES)].copy().reset_index(drop=True)
    if data.event_id.duplicated().any():
        raise ValueError("event_id must be unique")
    med,scale=robust_scale(data)
    z=(data[list(COVARIATES)].to_numpy(dtype=float)-med)/scale
    if not np.isfinite(z).all():
        raise ValueError("non-finite matching covariates")
    target_ix=list(COVARIATES).index(TARGET)
    ts=data.confirmation_ts_ms.to_numpy(dtype=np.int64)
    rows=[]
    for _,g in data.groupby(["asset","direction"],sort=True,dropna=False):
        a=g[g.sequence_class==CLASSES[0]]
        b=g[g.sequence_class==CLASSES[1]]
        if a.empty or b.empty: continue
        ai,bi=a.index.to_numpy(),b.index.to_numpy()
        delta=np.abs(z[ai,None,:]-z[None,bi,:])
        dist=np.sqrt(np.mean(delta**2,axis=2))
        gap=np.abs(ts[ai,None]-ts[None,bi])/86400000.0
        valid=(dist<=max_distance)&(delta.max(axis=2)<=max_component)&(delta[:,:,target_ix]<=target_caliper)&(gap<=max_time_gap_days)
        # Dummy columns represent unmatched separation events. The penalty makes
        # cardinality primary; total robust distance is minimized among max-cardinality solutions.
        k=min(len(ai),len(bi))
        penalty=2.0*k+1.0
        invalid=penalty*(len(ai)+len(bi)+2)*10.0
        cost=np.full((len(ai),len(bi)+len(ai)),invalid,dtype=float)
        cost[:,:len(bi)]=np.where(valid,dist,invalid)
        cost[:,len(bi):]=penalty
        rr,cc=linear_sum_assignment(cost)
        for i,j in zip(rr,cc):
            if j>=len(bi) or not valid[i,j]: continue
            ia,ib=int(ai[i]),int(bi[j])
            ra,rb=data.iloc[ia],data.iloc[ib]
            rows.append({"pair_id":f"P{len(rows)+1:06d}","separation_event_id":ra.event_id,
                "retest_event_id":rb.event_id,"asset":ra.asset,"direction":ra.direction,
                "separation_confirmation_month":ra.confirmation_month if "confirmation_month" in ra else "",
                "retest_confirmation_month":rb.confirmation_month if "confirmation_month" in rb else "",
                "match_time_gap_days":float(gap[i,j]),"match_distance_rms_robust_sd":float(dist[i,j]),
                "target_abs_difference_robust_sd":float(delta[i,j,target_ix])})
    return pd.DataFrame(rows,columns=["pair_id","separation_event_id","retest_event_id","asset","direction",
        "separation_confirmation_month","retest_confirmation_month","match_time_gap_days",
        "match_distance_rms_robust_sd","target_abs_difference_robust_sd"])

def run(anatomy:Path,sequence:Path,feature_dir:Path,minute_dir:Path,output:Path):
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output}")
    cov=build_covariates(anatomy,sequence,feature_dir,minute_dir)
    all_pairs=[]; balances=[]; summaries=[]
    for definition in ("broad","strict"):
        cohort=cov[cov.definition==definition].copy()
        a=cohort[cohort.sequence_class==CLASSES[0]].set_index("event_id")
        b=cohort[cohort.sequence_class==CLASSES[1]].set_index("event_id")
        for caliper in CALIPERS:
            pairs=optimal_match(cohort,caliper)
            pairs.insert(0,"definition",definition); pairs.insert(1,"target_caliper_robust_sd",caliper)
            all_pairs.append(pairs)
            abs_smd=[]
            for c in COVARIATES:
                before=smd(cohort[cohort.sequence_class==CLASSES[0]][c],cohort[cohort.sequence_class==CLASSES[1]][c])
                after=smd(a.loc[pairs.separation_event_id,c],b.loc[pairs.retest_event_id,c]) if len(pairs)>1 else np.nan
                balances.append({"definition":definition,"target_caliper_robust_sd":caliper,
                    "covariate":c,"smd_before":before,"smd_after":after,
                    "abs_smd_after":abs(after) if pd.notna(after) else np.nan})
                if pd.notna(after): abs_smd.append(abs(after))
            target_smd=next((x["abs_smd_after"] for x in balances[::-1]
                if x["definition"]==definition and x["target_caliper_robust_sd"]==caliper
                and x["covariate"]==TARGET),np.nan)
            summaries.append({"definition":definition,"target_caliper_robust_sd":caliper,
                "eligible_separation_first":int((cohort.sequence_class==CLASSES[0]).sum()),
                "eligible_retest_first":int((cohort.sequence_class==CLASSES[1]).sum()),
                "matched_pairs":len(pairs),
                "max_abs_smd_after":max(abs_smd) if abs_smd else np.nan,
                "target_abs_smd_after":target_smd})
    output.mkdir(parents=True,exist_ok=True)
    pd.concat(all_pairs,ignore_index=True).to_csv(output/"optimal_matched_pairs_v6.csv",index=False)
    pd.DataFrame(balances).to_csv(output/"optimal_covariate_balance_v6.csv",index=False)
    pd.DataFrame(summaries).to_csv(output/"optimal_caliper_summary_v6.csv",index=False)
    meta={"study":"Phase 3 outcome-blind optimal matching sensitivity V6",
        "method":"maximum-cardinality 1:1 bipartite assignment, then minimum total robust RMS distance",
        "solver":"scipy.optimize.linear_sum_assignment with explicit unmatched dummy columns",
        "strata":"exact asset and direction; month labels audit-only, not a matching stratum",
        "target_covariate":TARGET,"target_calipers_robust_sd":list(CALIPERS),
        "other_constraints":{"overall_rms_robust_sd":2.0,"maximum_component_robust_sd":1.5,"maximum_time_gap_days":30.0},
        "outcome_blind":True,"outcomes_loaded":False,
        "limitations":["optimality applies only to the specified eligible edge set and objective",
          "standardized mean differences do not prove exchangeability",
          "unmeasured confounding and overlapping-event dependence remain",
          "broad and strict cohorts are nested","no outcome comparison or trading inference is made"]}
    (output/"run_metadata_v6.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(pd.DataFrame(summaries).to_string(index=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for x in ("anatomy","sequence","feature-dir","minute-dir","output"): p.add_argument("--"+x,type=Path,required=True)
    a=p.parse_args(); run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.output)
if __name__=="__main__": main()
