#!/usr/bin/env python3
"""Outcome-blind V10 covariate-structure and matching-bottleneck attribution audit."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates

KEYS=("definition","target_caliper_robust_sd")

def audit_structure(eligible: pd.DataFrame, pairs: pd.DataFrame, feasibility: pd.DataFrame):
    need={"event_id","definition","sequence_class","asset","direction",*COVARIATES}
    if not need.issubset(eligible.columns): raise ValueError("eligible frame missing required columns")
    if eligible.event_id.duplicated().any(): raise ValueError("eligible event IDs must be unique")
    if not {"definition","target_caliper_robust_sd","asset","direction","separation_event_id","retest_event_id"}.issubset(pairs.columns):
        raise ValueError("matched pairs missing required columns")
    if not {"definition","target_caliper_robust_sd","asset","direction","candidate_edges","edges_if_overall_distance_removed","edges_if_component_limit_removed","edges_if_target_caliper_removed","edges_if_time_gap_removed"}.issubset(feasibility.columns):
        raise ValueError("V9 feasibility diagnostics missing required columns")
    ev=eligible.set_index("event_id",drop=False)
    structure=[]
    for (definition,asset,direction,cls),g in eligible.groupby(["definition","asset","direction","sequence_class"],sort=True):
        x=g[list(COVARIATES)].apply(pd.to_numeric,errors="raise")
        corr=x.corr().to_numpy(float)
        tri=np.abs(corr[np.triu_indices(len(COVARIATES),1)])
        finite=tri[np.isfinite(tri)]
        eig=np.linalg.eigvalsh(np.corrcoef(x.to_numpy(float),rowvar=False)) if len(g)>len(COVARIATES) and np.isfinite(corr).all() else np.array([])
        eig=np.clip(eig,0,None)
        effective=float((eig.sum()**2)/(np.square(eig).sum())) if len(eig) and np.square(eig).sum()>0 else np.nan
        structure.append({"definition":definition,"asset":asset,"direction":direction,"sequence_class":cls,
          "n":len(g),"covariate_count":len(COVARIATES),"median_abs_pairwise_correlation":float(np.median(finite)) if len(finite) else np.nan,
          "max_abs_pairwise_correlation":float(np.max(finite)) if len(finite) else np.nan,
          "correlation_pairs_abs_ge_0_90":int((finite>=.90).sum()),"correlation_effective_rank":effective})
    structure_df=pd.DataFrame(structure)
    # Pair balance: within exact definition x asset x direction, use the full eligible
    # class-pooled SD as the reference scale, consistent with V8.
    rows=[]
    for (definition,caliper),cohort in pairs.groupby(list(KEYS),sort=True):
        for (asset,direction),g in cohort.groupby(["asset","direction"],sort=True):
            a=ev.loc[g.separation_event_id]; b=ev.loc[g.retest_event_id]
            ref=eligible[(eligible.definition==definition)&(eligible.asset==asset)&(eligible.direction==direction)]
            x=ref[ref.sequence_class==CLASSES[0]]; y=ref[ref.sequence_class==CLASSES[1]]
            for cov in COVARIATES:
                xv=pd.to_numeric(x[cov],errors="raise").to_numpy(float); yv=pd.to_numeric(y[cov],errors="raise").to_numpy(float)
                sd=float(np.sqrt((np.var(xv,ddof=1)+np.var(yv,ddof=1))/2)) if len(xv)>1 and len(yv)>1 else np.nan
                diff=float(pd.to_numeric(a[cov]).mean()-pd.to_numeric(b[cov]).mean())
                smd=diff/sd if np.isfinite(sd) and sd>0 else np.nan
                rows.append({"definition":definition,"target_caliper_robust_sd":caliper,"asset":asset,"direction":direction,
                  "covariate":cov,"matched_pairs":len(g),"eligible_reference_sd":sd,"matched_mean_difference":diff,
                  "smd":smd,"abs_smd":abs(smd) if np.isfinite(smd) else np.nan})
    balance=pd.DataFrame(rows)
    attribution=(balance.groupby(["definition","target_caliper_robust_sd","covariate"],as_index=False)
      .agg(strata_n=("abs_smd","count"),median_abs_smd=("abs_smd","median"),mean_abs_smd=("abs_smd","mean"),
           max_abs_smd=("abs_smd","max"),strata_abs_smd_gt_0_10=("abs_smd",lambda s:int((s>.10).sum())),
           strata_abs_smd_gt_0_20=("abs_smd",lambda s:int((s>.20).sum()))))
    # One-constraint-at-a-time edge expansion, summed across strata; these are
    # overlapping diagnostic counterfactuals, not additive contributions.
    f=feasibility.copy()
    for c in ["candidate_edges","edges_if_overall_distance_removed","edges_if_component_limit_removed","edges_if_target_caliper_removed","edges_if_time_gap_removed"]:
        f[c]=pd.to_numeric(f[c],errors="raise")
    cols=["edges_if_overall_distance_removed","edges_if_component_limit_removed","edges_if_target_caliper_removed","edges_if_time_gap_removed"]
    bottleneck=f.groupby(list(KEYS),as_index=False).agg(candidate_edges=("candidate_edges","sum"),**{c:(c,"sum") for c in cols})
    for c in cols: bottleneck[c.replace("edges_if_","additional_edges_if_")]=bottleneck[c]-bottleneck.candidate_edges
    return structure_df,balance,attribution,bottleneck

def run(anatomy,sequence,feature_dir,minute_dir,pairs_path,feasibility_path,output):
    if output.exists() and any(output.iterdir()): raise FileExistsError(f"Refusing non-empty output directory: {output}")
    eligible=build_covariates(anatomy,sequence,feature_dir,minute_dir)
    pairs=pd.read_csv(pairs_path); feasibility=pd.read_csv(feasibility_path)
    structure,balance,attribution,bottleneck=audit_structure(eligible,pairs,feasibility)
    output.mkdir(parents=True,exist_ok=True)
    structure.to_csv(output/"covariate_correlation_structure_v10.csv",index=False)
    balance.to_csv(output/"matched_balance_by_stratum_v10.csv",index=False)
    attribution.to_csv(output/"covariate_imbalance_attribution_v10.csv",index=False)
    bottleneck.to_csv(output/"constraint_bottleneck_attribution_v10.csv",index=False)
    meta={"study":"Phase 3 V6 matched cohort covariate structure and bottleneck attribution V10",
      "inputs":"Frozen eligible pre-event covariates, archived V6 matched pairs, archived V9 edge diagnostics",
      "correlation_scope":"Separate definition x asset x direction x sequence-class groups; no outcomes used",
      "imbalance_scale":"Within definition x asset x direction pooled sample SD of both full eligible classes, matching V8 reference convention",
      "constraint_analysis":"V9 one-constraint-at-a-time edge counts summed by definition and caliper; counterfactuals overlap and are not additive",
      "interpretation":"Descriptive diagnostics only; no covariates removed, no matching rules changed, no cohort accepted/rejected, no outcomes loaded or compared",
      "limitations":["correlation is not proof of redundancy or causal irrelevance","correlation summaries can be unstable in small strata",
        "small matched strata produce unstable SMDs","edge expansions do not equal additional maximum matched pairs",
        "maximum cardinality and balance are distinct properties","broad and strict cohorts are nested",
        "unmeasured confounding remains possible"]}
    (output/"run_metadata_v10.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print("\nTop imbalance diagnostics:\n",attribution.sort_values("mean_abs_smd",ascending=False).groupby(["definition","target_caliper_robust_sd"]).head(5).to_string(index=False))
    print("\nConstraint diagnostics:\n",bottleneck.to_string(index=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("anatomy","sequence","feature-dir","minute-dir","pairs","feasibility","output"): p.add_argument("--"+arg,type=Path,required=True)
    a=p.parse_args()
    run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.pairs,a.feasibility,a.output)
if __name__=="__main__": main()
