#!/usr/bin/env python3
"""V10.4 outcome-blind sensitivity of V6 matching to predeclared edge-constraint relaxations."""
from pathlib import Path
import argparse,json
import pandas as pd
try:
 from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES,CLASSES,build_covariates,smd
 from research.sideways_rejection_pre_event_matched_controls_v6 import optimal_match
 from research.sideways_rejection_pre_event_matched_controls_v5 import CALIPERS
except ModuleNotFoundError:
 from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES,CLASSES,build_covariates,smd
 from sideways_rejection_pre_event_matched_controls_v6 import optimal_match
 from sideways_rejection_pre_event_matched_controls_v5 import CALIPERS

DESIGNS=[
 ("v6_frozen",1.5,30.0),
 ("component_2_0",2.0,30.0),
 ("component_2_5",2.5,30.0),
 ("time_gap_60d",1.5,60.0),
 ("time_gap_90d",1.5,90.0),
 ("component_2_0_time_60d",2.0,60.0),
]
def run(anatomy,sequence,feature_dir,minute_dir,out):
 if out.exists() and any(out.iterdir()): raise FileExistsError(f"Refusing non-empty output directory: {out}")
 cov=build_covariates(anatomy,sequence,feature_dir,minute_dir)
 pairs=[]; balances=[]; summary=[]
 for definition in ("broad","strict"):
  cohort=cov[cov.definition==definition].copy()
  for caliper in CALIPERS:
   for design,component,timegap in DESIGNS:
    m=optimal_match(cohort,caliper,max_distance=2.0,max_component=component,max_time_gap_days=timegap)
    if not m.empty:
     m.insert(0,"design",design);m.insert(1,"definition",definition);m.insert(2,"target_caliper_robust_sd",caliper);pairs.append(m)
    left=cohort[cohort.sequence_class==CLASSES[0]].set_index("event_id")
    right=cohort[cohort.sequence_class==CLASSES[1]].set_index("event_id")
    vals=[]
    for c in COVARIATES:
     x=smd(left.loc[m.separation_event_id,c],right.loc[m.retest_event_id,c]) if len(m)>1 else float("nan")
     vals.append(abs(x) if pd.notna(x) else float("nan"))
     balances.append({"design":design,"definition":definition,"target_caliper_robust_sd":caliper,
       "covariate":c,"matched_pairs":len(m),"smd":x,"abs_smd":abs(x) if pd.notna(x) else float("nan")})
    finite=[x for x in vals if pd.notna(x)]
    summary.append({"design":design,"definition":definition,"target_caliper_robust_sd":caliper,
      "max_component_robust_sd":component,"max_time_gap_days":timegap,"matched_pairs":len(m),
      "mean_abs_smd":sum(finite)/len(finite) if finite else float("nan"),
      "max_abs_smd":max(finite) if finite else float("nan")})
 out.mkdir(parents=True,exist_ok=True)
 pd.concat(pairs,ignore_index=True).to_csv(out/"alternative_design_pairs_v10_4.csv",index=False)
 pd.DataFrame(balances).to_csv(out/"alternative_design_balance_v10_4.csv",index=False)
 pd.DataFrame(summary).to_csv(out/"alternative_design_summary_v10_4.csv",index=False)
 (out/"run_metadata_v10_4.json").write_text(json.dumps({
  "study":"Phase 3 V10.4 alternative matching constraint sensitivity",
  "baseline":"V6 frozen max RMS distance 2.0, max component 1.5, max time gap 30 days; exact asset-direction strata; target calipers unchanged",
  "alternatives":"One-at-a-time and combined relaxations of maximum component distance and maximum confirmation-time gap",
  "method":"Same V6 maximum-cardinality bipartite assignment and minimum total RMS distance objective for each candidate-edge design",
  "interpretation":"Outcome-blind design sensitivity only; larger pair counts do not establish balance, exchangeability, or preferred design",
  "limitations":["relaxing edge constraints changes the eligible match graph","SMDs are descriptive, not causal guarantees",
  "no outcomes loaded or compared","no strategy or profitability conclusions"]},indent=2)+"\n")
 print(pd.DataFrame(summary).to_string(index=False))
def main():
 p=argparse.ArgumentParser()
 for x in ("anatomy","sequence","feature-dir","minute-dir","output"):p.add_argument("--"+x,type=Path,required=True)
 a=p.parse_args();run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.output)
if __name__=="__main__":main()
