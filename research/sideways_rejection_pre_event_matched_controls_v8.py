#!/usr/bin/env python3
"""Outcome-blind V8 common-support and pre-match-reference balance audit."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates

KEYS = ("definition", "target_caliper_robust_sd")

def audit_common_support(pairs: pd.DataFrame, eligible: pd.DataFrame):
    required_pairs = {"definition", "target_caliper_robust_sd", "pair_id", "separation_event_id", "retest_event_id", "asset", "direction"}
    required_eligible = {"event_id", "definition", "sequence_class", "asset", "direction", *COVARIATES}
    if not required_pairs.issubset(pairs.columns) or not required_eligible.issubset(eligible.columns):
        raise ValueError("V6 pairs or frozen eligible covariates missing required columns")
    if eligible.event_id.duplicated().any() or pairs.pair_id.isna().any():
        raise ValueError("eligible event IDs must be unique and pair IDs non-null")
    ev = eligible.set_index("event_id", drop=False)
    coverage, diagnostics, summaries = [], [], []
    for (definition, caliper), cohort in pairs.groupby(list(KEYS), sort=True):
        if cohort.pair_id.duplicated().any() or cohort.separation_event_id.duplicated().any() or cohort.retest_event_id.duplicated().any():
            raise ValueError("pair IDs and matched event endpoints must be unique within cohort")
        ids = set(cohort.separation_event_id) | set(cohort.retest_event_id)
        if not ids.issubset(set(ev.index)):
            raise ValueError("matched endpoint absent from rebuilt eligible cohort")
        a = ev.loc[cohort.separation_event_id].reset_index(drop=True)
        b = ev.loc[cohort.retest_event_id].reset_index(drop=True)
        if not ((a.asset.to_numpy()==b.asset.to_numpy()).all() and (a.direction.to_numpy()==b.direction.to_numpy()).all()):
            raise ValueError("matched endpoint asset/direction mismatch")
        if not ((a.definition.to_numpy()==definition).all() and (b.definition.to_numpy()==definition).all()):
            raise ValueError("matched endpoint definition mismatch")
        sub_summaries = []
        for (asset, direction), g in cohort.groupby(["asset","direction"], sort=True):
            sep = ev.loc[g.separation_event_id]
            ret = ev.loc[g.retest_event_id]
            ref = eligible[(eligible.definition==definition) & (eligible.asset==asset) & (eligible.direction==direction)]
            x = ref[ref.sequence_class==CLASSES[0]]
            y = ref[ref.sequence_class==CLASSES[1]]
            for cov in COVARIATES:
                xv = pd.to_numeric(x[cov], errors="raise").to_numpy(float)
                yv = pd.to_numeric(y[cov], errors="raise").to_numpy(float)
                pooled_sd = float(np.sqrt((np.var(xv,ddof=1)+np.var(yv,ddof=1))/2)) if len(xv)>1 and len(yv)>1 else np.nan
                smd = float((sep[cov].mean()-ret[cov].mean())/pooled_sd) if np.isfinite(pooled_sd) and pooled_sd>0 else np.nan
                qx = np.quantile(xv,[.05,.95]) if len(xv) else [np.nan,np.nan]
                qy = np.quantile(yv,[.05,.95]) if len(yv) else [np.nan,np.nan]
                lo, hi = max(qx[0],qy[0]), min(qx[1],qy[1])
                union_lo, union_hi = min(qx[0],qy[0]), max(qx[1],qy[1])
                overlap = max(0.0,hi-lo)/(union_hi-union_lo) if np.isfinite(union_hi-union_lo) and union_hi>union_lo else np.nan
                inside = float((((sep[cov]>=lo)&(sep[cov]<=hi)).sum()+((ret[cov]>=lo)&(ret[cov]<=hi)).sum())/(2*len(g))) if hi>=lo and len(g) else 0.0
                row = {"definition":definition,"target_caliper_robust_sd":caliper,"asset":asset,"direction":direction,
                    "covariate":cov,"eligible_separation_n":len(x),"eligible_retest_n":len(y),"matched_pairs":len(g),
                    "eligible_reference_pooled_sd":pooled_sd,"matched_mean_difference":float(sep[cov].mean()-ret[cov].mean()),
                    "smd_using_eligible_reference_sd":smd,"abs_smd_using_eligible_reference_sd":abs(smd) if np.isfinite(smd) else np.nan,
                    "separation_p05":qx[0],"separation_p95":qx[1],"retest_p05":qy[0],"retest_p95":qy[1],
                    "central_90pct_range_overlap_ratio":overlap,"matched_endpoints_inside_shared_central_range_fraction":inside}
                diagnostics.append(row)
                sub_summaries.append(row)
            coverage.append({"definition":definition,"target_caliper_robust_sd":caliper,"asset":asset,"direction":direction,
                "eligible_separation_n":len(x),"eligible_retest_n":len(y),"matched_pairs":len(g),
                "matched_fraction_of_smaller_class":len(g)/min(len(x),len(y)) if min(len(x),len(y)) else np.nan})
        d = pd.DataFrame(sub_summaries)
        summaries.append({"definition":definition,"target_caliper_robust_sd":caliper,"matched_pairs":len(cohort),
            "assets_represented":int(cohort.asset.nunique()),"asset_direction_strata":int(cohort[["asset","direction"]].drop_duplicates().shape[0]),
            "covariate_strata_abs_smd_gt_0_10":int((d.abs_smd_using_eligible_reference_sd>.10).sum()),
            "covariate_strata_abs_smd_gt_0_20":int((d.abs_smd_using_eligible_reference_sd>.20).sum()),
            "median_central_range_overlap_ratio":float(d.central_90pct_range_overlap_ratio.median()),
            "median_matched_endpoints_inside_shared_central_range_fraction":float(d.matched_endpoints_inside_shared_central_range_fraction.median()),
            "strata_with_fewer_than_two_pairs":int((cohort.groupby(["asset","direction"]).size()<2).sum())})
    return pd.DataFrame(coverage), pd.DataFrame(diagnostics), pd.DataFrame(summaries)

def run(anatomy_path, sequence_path, feature_dir, minute_dir, pairs_path, output):
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output}")
    eligible = build_covariates(anatomy_path,sequence_path,feature_dir,minute_dir)
    pairs = pd.read_csv(pairs_path)
    coverage, diagnostics, summary = audit_common_support(pairs,eligible)
    output.mkdir(parents=True,exist_ok=True)
    coverage.to_csv(output/"asset_direction_support_v8.csv",index=False)
    diagnostics.to_csv(output/"covariate_common_support_balance_v8.csv",index=False)
    summary.to_csv(output/"common_support_summary_v8.csv",index=False)
    meta={"study":"Phase 3 V6 matched cohort common-support and reference-balance audit V8",
      "inputs":"Archived outcome-blind V6 pairs and independently rebuilt frozen eligible pre-event covariates",
      "reference_scale":"Within definition x asset x direction, pooled sample SD of the two full eligible sequence classes before matching",
      "distribution_support":"Intersection of each class's 5th-95th percentile interval divided by the union interval; descriptive range-overlap diagnostic, not a density-overlap estimator",
      "matched_support":"Fraction of matched endpoints inside the shared central 90% interval",
      "thresholds":{"abs_smd_0_10":"reported diagnostic only; not an automatic acceptance threshold","abs_smd_0_20":"reported diagnostic only; not an automatic rejection threshold"},
      "limitations":["central-range overlap is not full distributional equivalence","small asset-direction matched samples remain unstable",
        "reference SD standardizes differences but does not prove exchangeability","broad and strict cohorts are nested",
        "unmeasured confounding remains possible","no outcomes are loaded or compared; no trading inference is made"]}
    (output/"run_metadata_v8.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(summary.to_string(index=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("anatomy","sequence","feature-dir","minute-dir","pairs","output"):
        p.add_argument("--"+arg,type=Path,required=True)
    a=p.parse_args()
    run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.pairs,a.output)
if __name__=="__main__": main()
