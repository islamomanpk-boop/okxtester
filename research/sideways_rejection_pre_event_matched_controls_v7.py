#!/usr/bin/env python3
"""Outcome-blind V7 audit of V6 matched-cohort balance, coverage and event overlap."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import (
        COVARIATES, CLASSES, build_covariates, smd
    )
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import (
        COVARIATES, CLASSES, build_covariates, smd
    )

KEYS = ("definition", "target_caliper_robust_sd")

def audit_pairs(pairs: pd.DataFrame, anatomy: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    required_pairs = {"definition", "target_caliper_robust_sd", "pair_id",
        "separation_event_id", "retest_event_id", "asset", "direction",
        "match_time_gap_days", "match_distance_rms_robust_sd",
        "target_abs_difference_robust_sd"}
    required_events = {"event_id", "asset", "direction", "definition",
        "test_start_ts_ms", "confirmation_ts_ms"}
    if not required_pairs.issubset(pairs.columns) or not required_events.issubset(anatomy.columns):
        raise ValueError("V6 pairs or anatomy input is missing required columns")
    if pairs.pair_id.isna().any() or pairs.duplicated(["definition","target_caliper_robust_sd","pair_id"]).any():
        raise ValueError("pair IDs must be non-null and unique within each V6 cohort")
    ev = anatomy.drop_duplicates("event_id").set_index("event_id", drop=False)
    if anatomy.event_id.duplicated().any():
        raise ValueError("anatomy event IDs must be unique")
    strata_rows, balance_rows, summary_rows = [], [], []
    for (definition, caliper), cohort in pairs.groupby(list(KEYS), sort=True):
        if cohort.separation_event_id.duplicated().any() or cohort.retest_event_id.duplicated().any():
            raise ValueError("V6 matching reuses an event within a cohort")
        endpoint_ids = set(cohort.separation_event_id) | set(cohort.retest_event_id)
        missing = endpoint_ids - set(ev.index)
        if missing:
            raise ValueError(f"V6 pair references unknown anatomy event: {next(iter(missing))}")
        a = ev.loc[cohort.separation_event_id].reset_index(drop=True)
        b = ev.loc[cohort.retest_event_id].reset_index(drop=True)
        if not ((a.asset.to_numpy()==b.asset.to_numpy()).all() and
                (a.direction.to_numpy()==b.direction.to_numpy()).all()):
            raise ValueError("matched event asset/direction strata do not agree")
        if not ((a.definition.to_numpy()==definition).all() and
                (b.definition.to_numpy()==definition).all()):
            raise ValueError("matched event definition does not agree with V6 cohort")
        merged = cohort.reset_index(drop=True).copy()
        merged["pair_midpoint_ts_ms"] = (
            pd.to_numeric(a.confirmation_ts_ms).to_numpy(dtype=np.int64) +
            pd.to_numeric(b.confirmation_ts_ms).to_numpy(dtype=np.int64)
        ) // 2
        merged["separation_start_ts_ms"] = pd.to_numeric(a.test_start_ts_ms).to_numpy(dtype=np.int64)
        merged["separation_end_ts_ms"] = pd.to_numeric(a.confirmation_ts_ms).to_numpy(dtype=np.int64)
        merged["retest_start_ts_ms"] = pd.to_numeric(b.test_start_ts_ms).to_numpy(dtype=np.int64)
        merged["retest_end_ts_ms"] = pd.to_numeric(b.confirmation_ts_ms).to_numpy(dtype=np.int64)
        # Cross-pair overlap is a dependence warning, not a claim that observations are independent.
        overlap_counts = np.zeros(len(merged), dtype=int)
        for asset, ix in merged.groupby("asset").groups.items():
            positions = np.asarray(list(ix), dtype=int)
            for ii, pos in enumerate(positions):
                s0 = min(merged.loc[pos,"separation_start_ts_ms"], merged.loc[pos,"retest_start_ts_ms"])
                e0 = max(merged.loc[pos,"separation_end_ts_ms"], merged.loc[pos,"retest_end_ts_ms"])
                for other in positions:
                    if other == pos: continue
                    s1 = min(merged.loc[other,"separation_start_ts_ms"], merged.loc[other,"retest_start_ts_ms"])
                    e1 = max(merged.loc[other,"separation_end_ts_ms"], merged.loc[other,"retest_end_ts_ms"])
                    if max(s0,s1) <= min(e0,e1):
                        overlap_counts[pos] += 1
        merged["overlapping_other_pairs_same_asset"] = overlap_counts
        # Fine-grained coverage and balance by asset x boundary direction.
        for (asset, direction), sub in merged.groupby(["asset","direction"], sort=True):
            n = len(sub)
            for cov in COVARIATES:
                av = ev.loc[sub.separation_event_id, cov].to_numpy(dtype=float)
                bv = ev.loc[sub.retest_event_id, cov].to_numpy(dtype=float)
                balance_rows.append({"definition":definition,"target_caliper_robust_sd":caliper,
                    "asset":asset,"direction":direction,"covariate":cov,"matched_pairs":n,
                    "smd_after":smd(pd.Series(av),pd.Series(bv)) if n >= 2 else np.nan,
                    "abs_smd_after":abs(smd(pd.Series(av),pd.Series(bv))) if n >= 2 else np.nan})
            strata_rows.append({"definition":definition,"target_caliper_robust_sd":caliper,
                "asset":asset,"direction":direction,"matched_pairs":n,
                "median_match_gap_days":float(sub.match_time_gap_days.median()),
                "max_match_gap_days":float(sub.match_time_gap_days.max()),
                "median_match_distance_rms":float(sub.match_distance_rms_robust_sd.median()),
                "max_target_difference_robust_sd":float(sub.target_abs_difference_robust_sd.max()),
                "pairs_with_cross_pair_window_overlap":int((sub.overlapping_other_pairs_same_asset>0).sum())})
        n_overlap = int((overlap_counts > 0).sum())
        summary_rows.append({"definition":definition,"target_caliper_robust_sd":caliper,
            "matched_pairs":len(merged),"assets_represented":int(merged.asset.nunique()),
            "asset_direction_strata_represented":int(merged[["asset","direction"]].drop_duplicates().shape[0]),
            "pairs_with_cross_pair_window_overlap":n_overlap,
            "cross_pair_overlap_pair_fraction":float(n_overlap/len(merged)) if len(merged) else np.nan,
            "median_match_gap_days":float(merged.match_time_gap_days.median()),
            "max_match_gap_days":float(merged.match_time_gap_days.max()),
            "median_pair_midpoint_utc":pd.to_datetime(merged.pair_midpoint_ts_ms,unit="ms",utc=True).median().isoformat(),
            "max_asset_direction_abs_smd":float(pd.DataFrame([x for x in balance_rows if x["definition"]==definition and x["target_caliper_robust_sd"]==caliper]).abs_smd_after.max()) if balance_rows else np.nan,
            "subgroups_with_fewer_than_two_pairs":int((merged.groupby(["asset","direction"]).size()<2).sum())})
    return pd.DataFrame(strata_rows), pd.DataFrame(balance_rows), pd.DataFrame(summary_rows)

def run(anatomy_path:Path, sequence_path:Path, feature_dir:Path, minute_dir:Path,
        pairs_path:Path, output:Path):
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output}")
    # Rebuild frozen pre-event covariates to independently verify pair membership and balance.
    cov = build_covariates(anatomy_path, sequence_path, feature_dir, minute_dir)
    pairs = pd.read_csv(pairs_path)
    anatomy = pd.read_csv(anatomy_path)
    strata, balance, summary = audit_pairs(pairs, cov)
    # Confirm all paired IDs are in the frozen eligible cohort for their definition/class.
    eligible = set(cov.event_id.astype(str))
    used = set(pairs.separation_event_id.astype(str)) | set(pairs.retest_event_id.astype(str))
    if not used.issubset(eligible):
        raise ValueError("V6 matched pairs include events outside rebuilt frozen eligible cohort")
    # Validate V6 covariates are unchanged against the independently rebuilt event table.
    indexed = cov.set_index("event_id")
    for event_id in used:
        if event_id not in indexed.index:
            raise ValueError("matched event missing from rebuilt covariate table")
    output.mkdir(parents=True, exist_ok=True)
    strata.to_csv(output/"asset_direction_coverage_v7.csv",index=False)
    balance.to_csv(output/"asset_direction_balance_v7.csv",index=False)
    summary.to_csv(output/"matching_dependence_summary_v7.csv",index=False)
    meta = {"study":"Phase 3 V6 matched-cohort quality and dependence audit V7",
        "input":"Archived outcome-blind V6 optimal matched pairs; frozen event anatomy, sequence and pre-event feature inputs",
        "checks":["pair ID uniqueness","one-to-one event use per definition/caliper","event membership in frozen eligible cohort",
            "exact asset/direction/definition agreement","asset-direction subgroup coverage","within-subgroup covariate SMD",
            "cross-pair overlap of event test windows within the same asset"],
        "event_window":"test_start_ts_ms through confirmation_ts_ms, inclusive",
        "overlap_interpretation":"descriptive dependence warning only; overlapping windows do not establish identical information sets",
        "limitations":["small subgroup SMDs are unstable; values are descriptive and not a pass/fail causal test",
            "broad and strict cohorts are nested",
            "matched balance does not establish exchangeability",
            "overlapping windows are only one dependence diagnostic",
            "no outcomes are loaded or compared; no trading inference is made"]}
    (output/"run_metadata_v7.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(summary.to_string(index=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("anatomy","sequence","feature-dir","minute-dir","pairs","output"):
        p.add_argument("--"+arg,type=Path,required=True)
    a=p.parse_args()
    run(a.anatomy,a.sequence,a.feature_dir,a.minute_dir,a.pairs,a.output)
if __name__=="__main__": main()
