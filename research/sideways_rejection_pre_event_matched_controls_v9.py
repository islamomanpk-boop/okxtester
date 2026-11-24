#!/usr/bin/env python3
"""Outcome-blind V9 audit of V6 matching feasibility and constraint bottlenecks."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching
try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates, robust_scale
    from research.sideways_rejection_pre_event_matched_controls_v5 import CALIPERS
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates, robust_scale
    from sideways_rejection_pre_event_matched_controls_v5 import CALIPERS

MAX_DISTANCE = 2.0
MAX_COMPONENT = 1.5
MAX_TIME_GAP_DAYS = 30.0

def audit_feasibility(frame: pd.DataFrame, archived_pairs: pd.DataFrame):
    required = {"event_id","sequence_class","asset","direction","confirmation_ts_ms",*COVARIATES}
    if not required.issubset(frame.columns):
        raise ValueError("eligible frame missing V6 matching inputs")
    if frame.event_id.duplicated().any():
        raise ValueError("eligible event IDs must be unique")
    if not {"definition","target_caliper_robust_sd","asset","direction","separation_event_id","retest_event_id"}.issubset(archived_pairs.columns):
        raise ValueError("archived V6 pairs missing required fields")
    strata_rows, summaries = [], []
    for definition in ("broad","strict"):
        data=frame[(frame.definition==definition)&frame.sequence_class.isin(CLASSES)].copy().reset_index(drop=True)
        if data.empty: continue
        med,scale=robust_scale(data)
        z=(data[list(COVARIATES)].to_numpy(dtype=float)-med)/scale
        if not np.isfinite(z).all(): raise ValueError("non-finite robust-scaled covariates")
        ts=pd.to_numeric(data.confirmation_ts_ms,errors="raise").to_numpy(dtype=np.int64)
        target_ix=list(COVARIATES).index("range_channel_width")
        for caliper in CALIPERS:
            archived=archived_pairs[(archived_pairs.definition==definition)&
                np.isclose(pd.to_numeric(archived_pairs.target_caliper_robust_sd),caliper)]
            archived_count=len(archived)
            independent_total=0
            for (asset,direction),g in data.groupby(["asset","direction"],sort=True):
                a=g[g.sequence_class==CLASSES[0]]
                b=g[g.sequence_class==CLASSES[1]]
                ai=a.index.to_numpy(); bi=b.index.to_numpy()
                if not len(ai) or not len(bi):
                    strata_rows.append({"definition":definition,"target_caliper_robust_sd":caliper,
                        "asset":asset,"direction":direction,"separation_n":len(ai),"retest_n":len(bi),
                        "candidate_edges":0,"max_feasible_pairs":0,"archived_v6_pairs":0,
                        "isolated_separation":len(ai),"isolated_retest":len(bi),
                        "edges_if_overall_distance_removed":0,"edges_if_component_limit_removed":0,
                        "edges_if_target_caliper_removed":0,"edges_if_time_gap_removed":0})
                    continue
                delta=np.abs(z[ai,None,:]-z[None,bi,:])
                rms=np.sqrt(np.mean(delta**2,axis=2))
                component=delta.max(axis=2)
                gap=np.abs(ts[ai,None]-ts[None,bi])/86400000.0
                c_dist=rms<=MAX_DISTANCE
                c_comp=component<=MAX_COMPONENT
                c_target=delta[:,:,target_ix]<=caliper
                c_time=gap<=MAX_TIME_GAP_DAYS
                valid=c_dist&c_comp&c_target&c_time
                edge_i,edge_j=np.where(valid)
                graph=csr_matrix((np.ones(len(edge_i),dtype=np.int8),(edge_i,edge_j)),shape=(len(ai),len(bi)))
                match=maximum_bipartite_matching(graph,perm_type="column")
                max_pairs=int(np.count_nonzero(match>=0))
                independent_total+=max_pairs
                deg_a=valid.sum(axis=1); deg_b=valid.sum(axis=0)
                sub_arch=archived[(archived.asset==asset)&(archived.direction==direction)]
                relaxed={
                    "edges_if_overall_distance_removed":int((c_comp&c_target&c_time).sum()),
                    "edges_if_component_limit_removed":int((c_dist&c_target&c_time).sum()),
                    "edges_if_target_caliper_removed":int((c_dist&c_comp&c_time).sum()),
                    "edges_if_time_gap_removed":int((c_dist&c_comp&c_target).sum())}
                strata_rows.append({"definition":definition,"target_caliper_robust_sd":caliper,
                    "asset":asset,"direction":direction,"separation_n":len(ai),"retest_n":len(bi),
                    "candidate_edges":int(valid.sum()),"max_feasible_pairs":max_pairs,
                    "archived_v6_pairs":len(sub_arch),"isolated_separation":int((deg_a==0).sum()),
                    "isolated_retest":int((deg_b==0).sum()),**relaxed})
            strata=pd.DataFrame([r for r in strata_rows if r["definition"]==definition and r["target_caliper_robust_sd"]==caliper])
            feasible=int(strata.max_feasible_pairs.sum())
            archived_in_scope=int(archived_count)
            summaries.append({"definition":definition,"target_caliper_robust_sd":caliper,
                "eligible_separation_n":int((data.sequence_class==CLASSES[0]).sum()),
                "eligible_retest_n":int((data.sequence_class==CLASSES[1]).sum()),
                "archived_v6_pairs":archived_in_scope,"independent_maximum_feasible_pairs":feasible,
                "archived_minus_independent_maximum":archived_in_scope-feasible,
                "candidate_edges_total":int(strata.candidate_edges.sum()),
                "isolated_separation_total":int(strata.isolated_separation.sum()),
                "isolated_retest_total":int(strata.isolated_retest.sum()),
                "strata_with_zero_candidate_edges":int((strata.candidate_edges==0).sum()),
                "strata_with_archived_count_below_feasible":int((strata.archived_v6_pairs<strata.max_feasible_pairs).sum())})
    return pd.DataFrame(strata_rows),pd.DataFrame(summaries)

def run(anatomy,sequence,feature_dir,minute_dir,pairs_path,output):
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output}")
    eligible=build_covariates(anatomy,sequence,feature_dir,minute_dir)
    pairs=pd.read_csv(pairs_path)
    strata,summary=audit_feasibility(eligible,pairs)
    output.mkdir(parents=True,exist_ok=True)
    strata.to_csv(output/"matching_feasibility_by_stratum_v9.csv",index=False)
    summary.to_csv(output/"matching_feasibility_summary_v9.csv",index=False)
    metadata={"study":"Phase 3 V6 matching feasibility and constraint bottleneck audit V9",
      "method":"Independent sparse bipartite maximum-cardinality matching within exact asset x direction strata",
      "frozen_constraints":{"overall_rms_robust_sd_max":MAX_DISTANCE,"maximum_single_covariate_robust_sd":MAX_COMPONENT,
        "target_covariate":"range_channel_width","target_calipers_robust_sd":list(CALIPERS),
        "maximum_confirmation_time_gap_days":MAX_TIME_GAP_DAYS},
      "constraint_diagnostics":"Each edge count removes one constraint at a time while retaining the other three; these counts are diagnostic and not additive.",
      "limitations":["feasibility is conditional on V6 eligible events, covariates, scaling, and constraints",
        "maximum pair count does not imply good covariate balance or exchangeability",
        "relaxed-edge counts do not recommend changing constraints",
        "broad and strict cohorts are nested","no outcomes are loaded or compared; no trading inference is made"]}
    (output/"run_metadata_v9.json").write_text(json.dumps(metadata,indent=2)+"\n",encoding="utf-8")
    print(summary.to_string(index=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for x in ("anatomy","sequence","feature-dir","minute-dir","pairs","output"):
        p.add_argument("--"+x,type=Path,required=True)
    a=p.parse_args()
    run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.pairs,a.output)
if __name__=="__main__": main()
