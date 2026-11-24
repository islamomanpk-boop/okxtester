#!/usr/bin/env python3
"""Outcome-blind descriptive balance-versus-retention frontier for Phase 3 V6 cohorts."""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path
import math
from statistics import median

def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def summarize(balance_rows, pair_rows, feasibility_rows):
    required={"definition","target_caliper_robust_sd","asset","direction","covariate","abs_smd"}
    if not balance_rows or not required.issubset(balance_rows[0]):
        raise ValueError("V10.2 balance input is empty or incomplete")
    if not pair_rows or not {"definition","target_caliper_robust_sd"}.issubset(pair_rows[0]):
        raise ValueError("V6 pair input is empty or incomplete")
    if not feasibility_rows or not {"definition","target_caliper_robust_sd","independent_maximum_feasible_pairs"}.issubset(feasibility_rows[0]):
        raise ValueError("V9 feasibility input is empty or incomplete")
    pair_counts=defaultdict(int)
    for r in pair_rows:
        pair_counts[(r["definition"],float(r["target_caliper_robust_sd"]))]+=1
    feasible={}
    for r in feasibility_rows:
        key=(r["definition"],float(r["target_caliper_robust_sd"]))
        feasible[key]=int(r["independent_maximum_feasible_pairs"])
    groups=defaultdict(list)
    covs=defaultdict(list)
    strata=defaultdict(lambda: defaultdict(list))
    for r in balance_rows:
        key=(r["definition"],float(r["target_caliper_robust_sd"]))
        try: x=float(r["abs_smd"])
        except (ValueError,TypeError): continue
        if not math.isfinite(x): continue
        groups[key].append(x)
        covs[key+(r["covariate"],)].append(x)
        strata[key+(r["asset"],r["direction"])][r["covariate"]].append(x)
    frontier=[]
    rankings=[]
    for key, vals in sorted(groups.items()):
        definition,caliper=key
        if key not in pair_counts or key not in feasible: raise ValueError(f"Missing pair/feasibility row for {key}")
        n=len(vals); mean=sum(vals)/n
        strata_keys=[k for k in strata if k[:2]==key]
        bad10=sum(any(x>.10 for values in strata[k].values() for x in values) for k in strata_keys)
        # Each stratum-covariate cell is one balance diagnostic; thresholds are descriptive only.
        frontier.append({
          "definition":definition,"target_caliper_robust_sd":caliper,
          "matched_pairs":pair_counts[key],"independent_maximum_feasible_pairs":feasible[key],
          "pair_retention_vs_feasible":pair_counts[key]/feasible[key] if feasible[key] else "",
          "asset_direction_strata":len(strata_keys),"covariate_stratum_cells":n,
          "mean_abs_smd":mean,"median_abs_smd":median(vals),
          "max_abs_smd":max(vals),"cells_abs_smd_gt_0_10":sum(x>.10 for x in vals),
          "cells_abs_smd_gt_0_20":sum(x>.20 for x in vals),
          "cells_abs_smd_le_0_10":sum(x<=.10 for x in vals),
          "strata_with_any_abs_smd_gt_0_10":bad10
        })
        ranked=sorted(((c, sum(v)/len(v),max(v),sum(x>.10 for x in v)) for (d,ca,c),v in covs.items() if (d,ca)==key),key=lambda z:(-z[1],z[0]))
        for rank,(cov,avg,mx,gt) in enumerate(ranked,1):
            rankings.append({"definition":definition,"target_caliper_robust_sd":caliper,
              "imbalance_rank":rank,"covariate":cov,"mean_abs_smd":avg,
              "max_abs_smd":mx,"cells_abs_smd_gt_0_10":gt})
    return frontier,rankings

def run(balance,pairs,feasibility,out):
    if out.exists() and any(out.iterdir()): raise FileExistsError(f"Refusing non-empty output directory: {out}")
    frontier,rankings=summarize(read_csv(balance),read_csv(pairs),read_csv(feasibility))
    out.mkdir(parents=True,exist_ok=True)
    for name,rows in [("cohort_balance_retention_frontier_v10_3.csv",frontier),
                      ("covariate_imbalance_rankings_v10_3.csv",rankings)]:
        with (out/name).open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    meta={"study":"Phase 3 V10.3 balance-versus-retention frontier",
      "inputs":"Archived V10.2 stratum-level SMDs, frozen V6 matched pairs, V9 independent maximum-cardinality feasibility summary",
      "purpose":"Describe the trade-off between retained matched pairs and observed covariate balance across existing frozen configurations",
      "thresholds":"Absolute SMD 0.10 and 0.20 are descriptive reporting thresholds, not automatic acceptance criteria",
      "interpretation":"No configuration selected or approved; no matching rules changed; no outcomes loaded or compared",
      "limitations":["SMD summaries are descriptive and do not prove exchangeability",
        "asset-direction strata and covariate cells are not independent observations",
        "small strata can yield unstable estimates","broad and strict definitions are nested",
        "unmeasured confounding remains possible"]}
    (out/"run_metadata_v10_3.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print("Balance-retention frontier")
    for r in frontier: print(r)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--balance",type=Path,required=True)
    p.add_argument("--pairs",type=Path,required=True)
    p.add_argument("--feasibility",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(); run(a.balance,a.pairs,a.feasibility,a.output)
if __name__=="__main__": main()
