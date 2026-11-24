#!/usr/bin/env python3
"""V10.1 repair: robust outcome-blind correlation and effective-rank diagnostics."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates

GROUP=("definition","asset","direction")
def correlation_diagnostics(frame: pd.DataFrame, group_cols, scope: str):
    rows=[]; pairs=[]
    for keys,g in frame.groupby(list(group_cols),sort=True,dropna=False):
        if not isinstance(keys,tuple): keys=(keys,)
        x=g[list(COVARIATES)].apply(pd.to_numeric,errors="coerce")
        variable=[c for c in COVARIATES if x[c].notna().sum()>=3 and x[c].nunique(dropna=True)>1]
        constant=[c for c in COVARIATES if c not in variable]
        corr=x[variable].corr(min_periods=3) if variable else pd.DataFrame()
        vals=corr.to_numpy(float) if len(variable)>1 else np.empty((0,0))
        tri=vals[np.triu_indices(len(variable),1)] if len(variable)>1 else np.array([])
        finite=tri[np.isfinite(tri)]
        rank=np.nan; condition=np.nan
        if len(variable)>=2 and len(g)>=3 and np.isfinite(vals).all():
            eig=np.linalg.eigvalsh((vals+vals.T)/2)
            eig=np.clip(eig,0,None)
            denom=float(np.square(eig).sum())
            rank=float(eig.sum()**2/denom) if denom>0 else np.nan
            positive=eig[eig>1e-10]
            condition=float(positive.max()/positive.min()) if len(positive) else np.nan
        rec=dict(zip(group_cols,keys))
        rows.append({**rec,"scope":scope,"n_rows":len(g),"covariate_count":len(COVARIATES),
          "variable_covariate_count":len(variable),"constant_or_insufficient_covariate_count":len(constant),
          "constant_or_insufficient_covariates":";".join(constant),
          "finite_pairwise_correlation_count":int(len(finite)),
          "median_abs_pairwise_correlation":float(np.median(np.abs(finite))) if len(finite) else np.nan,
          "max_abs_pairwise_correlation":float(np.max(np.abs(finite))) if len(finite) else np.nan,
          "pairs_abs_ge_0_80":int((np.abs(finite)>=.80).sum()),"pairs_abs_ge_0_90":int((np.abs(finite)>=.90).sum()),
          "correlation_effective_rank_nonconstant":rank,"correlation_condition_number_nonconstant":condition})
        for i,a in enumerate(variable):
            for b in variable[i+1:]:
                value=float(corr.loc[a,b])
                if np.isfinite(value):
                    pairs.append({**rec,"scope":scope,"covariate_a":a,"covariate_b":b,
                      "correlation":value,"abs_correlation":abs(value),
                      "high_correlation_ge_0_80":bool(abs(value)>=.80),
                      "very_high_correlation_ge_0_90":bool(abs(value)>=.90)})
    return pd.DataFrame(rows),pd.DataFrame(pairs)

def run(anatomy,sequence,feature_dir,minute_dir,output):
    if output.exists() and any(output.iterdir()): raise FileExistsError(f"Refusing non-empty output directory: {output}")
    eligible=build_covariates(anatomy,sequence,feature_dir,minute_dir)
    required={"definition","asset","direction","sequence_class",*COVARIATES}
    if not required.issubset(eligible.columns): raise ValueError("eligible covariate frame missing required columns")
    all_summary=[]; all_pairs=[]
    specs=[(GROUP+("sequence_class",),"within_sequence_class"),
           (GROUP,"pooled_classes_within_asset_direction"),
           (("definition","sequence_class"),"pooled_assets_within_class"),
           (("definition",),"pooled_all_assets_and_classes")]
    for cols,scope in specs:
        s,p=correlation_diagnostics(eligible,cols,scope)
        all_summary.append(s); all_pairs.append(p)
    summary=pd.concat(all_summary,ignore_index=True)
    pair_table=pd.concat(all_pairs,ignore_index=True)
    output.mkdir(parents=True,exist_ok=True)
    summary.to_csv(output/"correlation_group_diagnostics_v10_1.csv",index=False)
    pair_table.to_csv(output/"covariate_correlation_pairs_v10_1.csv",index=False)
    # Explicitly report variable coverage and high-correlation pair frequency by scope.
    coverage=(summary.groupby("scope",as_index=False).agg(groups=("n_rows","count"),
      groups_with_constant_variables=("constant_or_insufficient_covariate_count",lambda x:int((x>0).sum())),
      median_effective_rank=("correlation_effective_rank_nonconstant","median"),
      median_variable_covariates=("variable_covariate_count","median"),
      groups_with_any_abs_corr_ge_0_90=("pairs_abs_ge_0_90",lambda x:int((x>0).sum()))))
    coverage.to_csv(output/"correlation_scope_coverage_v10_1.csv",index=False)
    meta={"study":"Phase 3 V10.1 robust covariate correlation diagnostic repair",
      "input":"Frozen eligible pre-event covariates rebuilt from original Phase 3 inputs",
      "scopes":["within sequence class by definition x asset x direction","pooled classes within definition x asset x direction",
        "pooled assets within definition x sequence class","pooled all assets and classes by definition"],
      "method":"Pearson correlations using pairwise available observations with minimum 3; constant or insufficient variables explicitly counted and excluded from matrix eigenanalysis",
      "effective_rank":"Participation-ratio effective rank of the symmetric nonnegative-clipped correlation eigenvalues for nonconstant variables only; NA where fewer than two variable covariates or matrix invalid",
      "thresholds":"Absolute pairwise correlation >=0.80 and >=0.90 are descriptive flags, not automatic variable-removal rules",
      "interpretation":"Outcome-blind descriptive diagnostics only; no covariates removed, no matching rules changed, no outcomes loaded or compared",
      "limitations":["correlation is not proof of redundancy or causal irrelevance","pooled correlations may reflect between-group structure; compare with within-group results",
        "pairwise deletion can produce non-positive-semidefinite matrices with missingness","small groups yield unstable estimates",
        "effective rank is a summary, not a causal or predictive measure"]}
    (output/"run_metadata_v10_1.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print("\nScope coverage:\n",coverage.to_string(index=False))
    print("\nMost frequently highly correlated pairs by scope:\n",
      pair_table[pair_table.abs_correlation>=.90].groupby(["scope","covariate_a","covariate_b"],as_index=False).size()
      .sort_values(["scope","size"],ascending=[True,False]).groupby("scope").head(10).to_string(index=False))
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("anatomy","sequence","feature-dir","minute-dir","output"): p.add_argument("--"+arg,type=Path,required=True)
    a=p.parse_args(); run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.output)
if __name__=="__main__": main()
