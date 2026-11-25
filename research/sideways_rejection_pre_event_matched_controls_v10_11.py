#!/usr/bin/env python3
"""V10.11 outcome-blind percentile sensitivity for frozen V10.10 joint support."""
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
RANGES={"central_98":(.01,.99),"central_95":(.025,.975),"central_90":(.05,.95),"central_80":(.10,.90)}

def percentile_sensitivity(pairs,eligible):
 rp={"definition","target_caliper_robust_sd","pair_id","separation_event_id","retest_event_id","asset","direction"}
 re={"event_id","definition","sequence_class","asset","direction",*COVARIATES}
 if not rp.issubset(pairs.columns) or not re.issubset(eligible.columns): raise ValueError("Frozen V6 pairs or eligible covariates missing required columns")
 if eligible.event_id.duplicated().any() or pairs.pair_id.isna().any(): raise ValueError("Eligible event IDs must be unique and pair IDs non-null")
 ev=eligible.set_index("event_id",drop=False); details=[]
 for (definition,caliper),cohort in pairs.groupby(list(KEYS),sort=True):
  if cohort.pair_id.duplicated().any() or cohort.separation_event_id.duplicated().any() or cohort.retest_event_id.duplicated().any(): raise ValueError("Pair IDs and endpoints must be unique within each cohort")
  ids=set(cohort.separation_event_id)|set(cohort.retest_event_id)
  if not ids.issubset(set(ev.index)): raise ValueError("Matched endpoint absent from frozen eligible cohort")
  sep=ev.loc[cohort.separation_event_id]; ret=ev.loc[cohort.retest_event_id]
  if not (sep.sequence_class.eq(CLASSES[0]).all() and ret.sequence_class.eq(CLASSES[1]).all()): raise ValueError("Matched endpoints must belong to their designated event classes")
  if not ((sep.asset.to_numpy()==ret.asset.to_numpy()).all() and (sep.direction.to_numpy()==ret.direction.to_numpy()).all()): raise ValueError("Matched endpoint asset/direction mismatch")
  if not ((sep.definition.to_numpy()==definition).all() and (ret.definition.to_numpy()==definition).all()): raise ValueError("Matched endpoint definition mismatch")
  for (asset,direction),g in cohort.groupby(["asset","direction"],sort=True):
   ref=eligible[(eligible.definition==definition)&(eligible.asset==asset)&(eligible.direction==direction)]
   x=ref[ref.sequence_class==CLASSES[0]]; y=ref[ref.sequence_class==CLASSES[1]]
   if x.empty or y.empty: raise ValueError("Both eligible classes required")
   a=ev.loc[g.separation_event_id]; b=ev.loc[g.retest_event_id]
   for label,(qlo,qhi) in RANGES.items():
    used=[]; constants=[]; no_overlap=[]; bounds={}
    for cov in COVARIATES:
     xv=pd.to_numeric(x[cov],errors="raise").to_numpy(float); yv=pd.to_numeric(y[cov],errors="raise").to_numpy(float)
     if not np.isfinite(xv).all() or not np.isfinite(yv).all(): raise ValueError(f"Non-finite values in {cov}")
     if len(xv)<2 or len(yv)<2 or np.var(xv,ddof=1)<=0 or np.var(yv,ddof=1)<=0: constants.append(cov); continue
     qx=np.quantile(xv,[qlo,qhi]); qy=np.quantile(yv,[qlo,qhi]); lo=float(max(qx[0],qy[0])); hi=float(min(qx[1],qy[1]))
     if hi<lo: no_overlap.append(cov)
     else: used.append(cov); bounds[cov]=(lo,hi)
    if no_overlap:
     xm=np.zeros(len(x),bool); ym=np.zeros(len(y),bool); am=np.zeros(len(g),bool); bm=np.zeros(len(g),bool)
    else:
     xm=np.ones(len(x),bool); ym=np.ones(len(y),bool); am=np.ones(len(g),bool); bm=np.ones(len(g),bool)
     for cov,(lo,hi) in bounds.items():
      xm &= x[cov].to_numpy(float).__ge__(lo)&x[cov].to_numpy(float).__le__(hi)
      ym &= y[cov].to_numpy(float).__ge__(lo)&y[cov].to_numpy(float).__le__(hi)
      am &= a[cov].to_numpy(float).__ge__(lo)&a[cov].to_numpy(float).__le__(hi)
      bm &= b[cov].to_numpy(float).__ge__(lo)&b[cov].to_numpy(float).__le__(hi)
    both=am&bm
    details.append({"range":label,"lower_quantile":qlo,"upper_quantile":qhi,"definition":definition,"target_caliper_robust_sd":caliper,"asset":asset,"direction":direction,
     "eligible_separation_n":len(x),"eligible_retest_n":len(y),"joint_support_dimensions":len(used),"constant_dimensions_excluded":len(constants),"nonoverlap_dimensions":len(no_overlap),"nonoverlap_covariates":";".join(no_overlap),
     "joint_support_separation_n":int(xm.sum()),"joint_support_retest_n":int(ym.sum()),"separation_retention_fraction":float(xm.mean()),"retest_retention_fraction":float(ym.mean()),
     "matched_pairs":len(g),"pairs_both_endpoints_in_joint_support":int(both.sum()),"matched_pair_retention_fraction":float(both.mean()),"acceptance_status":"NOT_ACCEPTED_FOR_OUTCOME_COMPARISON"})
 detail=pd.DataFrame(details)
 if detail.empty: raise ValueError("No matched strata available")
 keys=["range",*KEYS]
 summary=detail.groupby(keys,as_index=False).agg(represented_strata=("asset","count"),median_joint_dimensions=("joint_support_dimensions","median"),strata_with_any_nonoverlap_dimension=("nonoverlap_dimensions",lambda s:int((s>0).sum())),eligible_separation_events=("eligible_separation_n","sum"),eligible_retest_events=("eligible_retest_n","sum"),joint_support_separation_events=("joint_support_separation_n","sum"),joint_support_retest_events=("joint_support_retest_n","sum"),matched_pairs=("matched_pairs","sum"),pairs_both_endpoints_in_joint_support=("pairs_both_endpoints_in_joint_support","sum"),median_stratum_pair_retention=("matched_pair_retention_fraction","median"))
 summary["separation_joint_retention"]=summary.joint_support_separation_events/summary.eligible_separation_events
 summary["retest_joint_retention"]=summary.joint_support_retest_events/summary.eligible_retest_events
 summary["matched_pair_joint_retention"]=summary.pairs_both_endpoints_in_joint_support/summary.matched_pairs
 summary["acceptance_status"]="NOT_ACCEPTED_FOR_OUTCOME_COMPARISON"
 return detail.sort_values(keys+["asset","direction"]),summary.sort_values(keys)

def run(anatomy,sequence,feature_dir,minute_dir,pairs_path,output):
 eligible=build_covariates(Path(anatomy),Path(sequence),Path(feature_dir),Path(minute_dir)); pairs=pd.read_csv(pairs_path)
 detail,summary=percentile_sensitivity(pairs,eligible); out=Path(output)
 if out.exists() and any(out.iterdir()): raise FileExistsError(f"Refusing non-empty output: {out}")
 out.mkdir(parents=True,exist_ok=True)
 detail.to_csv(out/"joint_support_percentile_detail_v10_11.csv",index=False); summary.to_csv(out/"joint_support_percentile_summary_v10_11.csv",index=False)
 meta={"study":"Phase 3 V10.11 joint common-support percentile sensitivity","frozen_pair_source":"V6 optimal_matched_pairs_v6.csv; no rematching or cohort changes","ranges":{k:{"lower_quantile":v[0],"upper_quantile":v[1]} for k,v in RANGES.items()},"method":"Within definition x asset x direction, intersect class-specific central percentile intervals across all nonconstant covariates; any disjoint dimension empties joint support for that stratum","constant_dimensions":"Excluded and counted, exactly as V10.10","baseline":"central_90 reproduces V10.10's 5th-95th percentile definition","outcome_data_loaded":False,"outcomes_compared":False,"limitations":["conservative intersection of marginal intervals, not a multivariate density estimator","percentile sensitivity is diagnostic and does not authorize selecting a favorable range","no rematching; original V6 pairs remain frozen","no cohort accepted for outcome comparison"]}
 (out/"run_metadata_v10_11.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
 print(summary.to_string(index=False))
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for a in ("anatomy","sequence","feature-dir","minute-dir","pairs","output"):p.add_argument("--"+a,required=True)
 run(**vars(p.parse_args()).keys()) if False else None
 a=p.parse_args();run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.pairs,a.output)
if __name__=="__main__":main()

# Trigger the committed V10.11 percentile-sensitivity workflow on the research branch.
