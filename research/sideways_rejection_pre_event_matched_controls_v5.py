#!/usr/bin/env python3
"""Outcome-blind V5 caliper sensitivity for Phase 3 pre-event matching."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sideways_rejection_pre_event_matched_controls_v4 import (
    COVARIATES, CLASSES, build_covariates, robust_scale, smd
)

TARGET = "signed_close_boundary_distance_width"
CALIPERS = (0.25, 0.50, 0.75, 1.00)


def match_with_target_caliper(frame: pd.DataFrame, target_caliper: float,
                              max_distance: float = 2.0,
                              max_component: float = 1.5,
                              max_time_gap_days: float = 30.0) -> pd.DataFrame:
    if target_caliper <= 0 or max_distance <= 0 or max_component <= 0 or max_time_gap_days < 0:
        raise ValueError("calipers must be positive and time gap non-negative")
    required = {"event_id", "sequence_class", "asset", "direction", "confirmation_ts_ms", *COVARIATES}
    if not required.issubset(frame.columns):
        raise ValueError("matching frame is missing required columns")
    data = frame[frame.sequence_class.isin(CLASSES)].copy().reset_index(drop=True)
    if data.event_id.duplicated().any():
        raise ValueError("event_id must be unique")
    med, scale = robust_scale(data)
    z = (data[list(COVARIATES)].to_numpy(dtype=float)-med)/scale
    if not np.isfinite(z).all():
        raise ValueError("non-finite matching covariates")
    target_ix = list(COVARIATES).index(TARGET)
    data["_row"] = np.arange(len(data))
    ts = data.confirmation_ts_ms.to_numpy(dtype=np.int64)
    pairs=[]
    for _, group in data.groupby(["asset","direction"], sort=True, dropna=False):
        a=group[group.sequence_class==CLASSES[0]]
        b=group[group.sequence_class==CLASSES[1]]
        if a.empty or b.empty:
            continue
        ai,bi=a["_row"].to_numpy(),b["_row"].to_numpy()
        dist=np.sqrt(np.mean((z[ai,None,:]-z[None,bi,:])**2,axis=2))
        edges=[]
        for i,ia in enumerate(ai):
            for j,ib in enumerate(bi):
                gap=abs(int(ts[ia])-int(ts[ib]))/86400000.0
                delta=np.abs(z[ia]-z[ib])
                if (dist[i,j] <= max_distance and delta.max() <= max_component
                    and delta[target_ix] <= target_caliper and gap <= max_time_gap_days):
                    edges.append((float(dist[i,j]),gap,int(ia),int(ib),float(delta[target_ix])))
        edges.sort(key=lambda x:(x[0],x[1],x[2],x[3]))
        used_a,used_b=set(),set()
        for d,gap,ia,ib,target_delta in edges:
            if ia in used_a or ib in used_b: continue
            used_a.add(ia); used_b.add(ib)
            ra,rb=data.iloc[ia],data.iloc[ib]
            pairs.append({"pair_id":f"P{len(pairs)+1:06d}",
                "separation_event_id":ra.event_id,"retest_event_id":rb.event_id,
                "asset":ra.asset,"direction":ra.direction,
                "separation_confirmation_month":ra.confirmation_month if "confirmation_month" in ra else "",
                "retest_confirmation_month":rb.confirmation_month if "confirmation_month" in rb else "",
                "match_time_gap_days":gap,"match_distance_rms_robust_sd":d,
                "target_abs_difference_robust_sd":target_delta})
    return pd.DataFrame(pairs,columns=["pair_id","separation_event_id","retest_event_id",
        "asset","direction","separation_confirmation_month","retest_confirmation_month",
        "match_time_gap_days","match_distance_rms_robust_sd","target_abs_difference_robust_sd"])


def evaluate_caliper(frame: pd.DataFrame, caliper: float) -> tuple[pd.DataFrame,pd.DataFrame]:
    pairs=match_with_target_caliper(frame,caliper)
    a=frame[frame.sequence_class==CLASSES[0]].set_index("event_id")
    b=frame[frame.sequence_class==CLASSES[1]].set_index("event_id")
    rows=[]
    for c in COVARIATES:
        before=smd(frame.loc[frame.sequence_class==CLASSES[0],c],
                   frame.loc[frame.sequence_class==CLASSES[1],c])
        after=smd(a.loc[pairs.separation_event_id,c],b.loc[pairs.retest_event_id,c]) if len(pairs)>1 else np.nan
        rows.append({"target_caliper_robust_sd":caliper,"covariate":c,
                     "smd_before":before,"smd_after":after,
                     "abs_smd_after":abs(after) if pd.notna(after) else np.nan})
    return pairs,pd.DataFrame(rows)


def run(anatomy:Path,sequence:Path,feature_dir:Path,minute_dir:Path,output:Path):
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output}")
    cov=build_covariates(anatomy,sequence,feature_dir,minute_dir)
    pair_frames=[]; balance_frames=[]; summaries=[]
    for definition in ("broad","strict"):
        cohort=cov[cov.definition==definition].copy()
        for caliper in CALIPERS:
            pairs,balance=evaluate_caliper(cohort,caliper)
            pairs.insert(0,"definition",definition)
            pairs.insert(1,"target_caliper_robust_sd",caliper)
            balance.insert(0,"definition",definition)
            pair_frames.append(pairs); balance_frames.append(balance)
            summaries.append({"definition":definition,"target_caliper_robust_sd":caliper,
                "eligible_separation_first":int((cohort.sequence_class==CLASSES[0]).sum()),
                "eligible_retest_first":int((cohort.sequence_class==CLASSES[1]).sum()),
                "matched_pairs":len(pairs),
                "unmatched_separation_first":int((cohort.sequence_class==CLASSES[0]).sum())-len(pairs),
                "unmatched_retest_first":int((cohort.sequence_class==CLASSES[1]).sum())-len(pairs),
                "max_abs_smd_after":float(balance.abs_smd_after.max()) if balance.abs_smd_after.notna().any() else np.nan,
                "target_abs_smd_after":float(balance.loc[balance.covariate==TARGET,"abs_smd_after"].iloc[0])})
    output.mkdir(parents=True,exist_ok=True)
    pd.concat(pair_frames,ignore_index=True).to_csv(output/"matched_pairs_caliper_grid_v5.csv",index=False)
    pd.concat(balance_frames,ignore_index=True).to_csv(output/"covariate_balance_caliper_grid_v5.csv",index=False)
    pd.DataFrame(summaries).to_csv(output/"caliper_grid_summary_v5.csv",index=False)
    meta={"study":"Phase 3 outcome-blind pre-event matching caliper sensitivity V5",
      "input_builder":"V4 frozen pre-event covariate construction",
      "matching":"1:1 greedy nearest-edge without replacement; exact asset/direction; max 30-day gap",
      "target_covariate":TARGET,"target_calipers_robust_sd":list(CALIPERS),
      "other_constraints":{"overall_rms_robust_sd":2.0,"maximum_component_robust_sd":1.5},
      "outcome_blind":True,"outcome_note":"no outcome columns are loaded or used",
      "month_matching":"not enforced; month labels are retained only for audit",
      "covariates":list(COVARIATES),
      "selection_rule":"compare retained pair counts and absolute standardized mean differences; do not select by outcome",
      "limitations":["greedy matching is not globally optimal","standardized differences are diagnostics, not proof of exchangeability",
        "residual and unmeasured confounding may remain","broad and strict cohorts are nested",
        "sensitivity grid comparisons are descriptive"]}
    (output/"run_metadata_v5.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(pd.DataFrame(summaries).to_string(index=False))
    return pd.DataFrame(summaries)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("anatomy","sequence","feature-dir","minute-dir","output"):
        p.add_argument("--"+arg,type=Path,required=True)
    a=p.parse_args()
    run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.output)


if __name__=="__main__": main()
