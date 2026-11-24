#!/usr/bin/env python3
"""V10.5 asset-direction-specific attribution of pre-event matched-cohort imbalance.

Outcome-blind: reuses the frozen V10.4 design grid and V6 assignment objective.
Reports each asset/direction stratum separately; small strata are explicitly flagged.
"""
from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd

try:
    from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates, smd
    from research.sideways_rejection_pre_event_matched_controls_v6 import optimal_match
    from research.sideways_rejection_pre_event_matched_controls_v5 import CALIPERS
    from research.sideways_rejection_pre_event_matched_controls_v10_4 import DESIGNS
except ModuleNotFoundError:
    from sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES, build_covariates, smd
    from sideways_rejection_pre_event_matched_controls_v6 import optimal_match
    from sideways_rejection_pre_event_matched_controls_v5 import CALIPERS
    from sideways_rejection_pre_event_matched_controls_v10_4 import DESIGNS

MIN_PAIRS_STABLE = 5

def run(anatomy, sequence, feature_dir, minute_dir, output):
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output}")
    cov = build_covariates(anatomy, sequence, feature_dir, minute_dir)
    cell_rows, ranking_rows, coverage_rows = [], [], []
    for definition in ("broad", "strict"):
        cohort = cov[cov.definition == definition].copy()
        for caliper in CALIPERS:
            for design, component, timegap in DESIGNS:
                pairs = optimal_match(cohort, caliper, max_distance=2.0,
                                      max_component=component,
                                      max_time_gap_days=timegap)
                if pairs.empty:
                    continue
                left = cohort[cohort.sequence_class == CLASSES[0]].set_index("event_id")
                right = cohort[cohort.sequence_class == CLASSES[1]].set_index("event_id")
                pairs = pairs.copy()
                pairs["stratum"] = pairs.asset.astype(str) + "|" + pairs.direction.astype(str)
                # Per-stratum balance and pre-match context.
                for stratum, pg in pairs.groupby("stratum", sort=True):
                    a_ids, b_ids = pg.separation_event_id.tolist(), pg.retest_event_id.tolist()
                    pre_a = cohort[(cohort.sequence_class == CLASSES[0]) &
                                   (cohort.asset.astype(str) + "|" + cohort.direction.astype(str) == stratum)]
                    pre_b = cohort[(cohort.sequence_class == CLASSES[1]) &
                                   (cohort.asset.astype(str) + "|" + cohort.direction.astype(str) == stratum)]
                    for c in COVARIATES:
                        before = smd(pre_a[c], pre_b[c]) if len(pre_a) > 1 and len(pre_b) > 1 else np.nan
                        after = smd(left.loc[a_ids, c], right.loc[b_ids, c]) if len(pg) > 1 else np.nan
                        cell_rows.append({
                            "design": design, "definition": definition,
                            "target_caliper_robust_sd": caliper,
                            "max_component_robust_sd": component,
                            "max_time_gap_days": timegap,
                            "asset_direction": stratum, "asset": pg.asset.iloc[0],
                            "direction": pg.direction.iloc[0],
                            "matched_pairs": len(pg),
                            "eligible_separation_events": len(pre_a),
                            "eligible_retest_events": len(pre_b),
                            "covariate": c, "smd_before": before,
                            "smd_after": after,
                            "abs_smd_after": abs(after) if pd.notna(after) else np.nan,
                            "small_stratum_flag": len(pg) < MIN_PAIRS_STABLE
                        })
                # Coverage: matched and eligible counts, isolated by asset-direction.
                for stratum, group in cohort.assign(
                    asset_direction=cohort.asset.astype(str) + "|" + cohort.direction.astype(str)
                ).groupby("asset_direction", sort=True):
                    cp = int((pairs.stratum == stratum).sum())
                    coverage_rows.append({
                        "design": design, "definition": definition,
                        "target_caliper_robust_sd": caliper,
                        "asset_direction": stratum,
                        "eligible_separation_events": int((group.sequence_class == CLASSES[0]).sum()),
                        "eligible_retest_events": int((group.sequence_class == CLASSES[1]).sum()),
                        "matched_pairs": cp,
                        "unmatched_separation_events": int((group.sequence_class == CLASSES[0]).sum()) - cp,
                        "unmatched_retest_events": int((group.sequence_class == CLASSES[1]).sum()) - cp,
                        "small_stratum_flag": cp < MIN_PAIRS_STABLE
                    })
    cells = pd.DataFrame(cell_rows)
    if cells.empty:
        raise RuntimeError("No matched subgroup diagnostics were produced")
    keys = ["design", "definition", "target_caliper_robust_sd", "covariate"]
    for key, g in cells.groupby(keys, sort=True):
        valid = g[g.abs_smd_after.notna()]
        ranking_rows.append({
            "design": key[0], "definition": key[1],
            "target_caliper_robust_sd": key[2], "covariate": key[3],
            "asset_direction_strata_with_pairs": len(g),
            "strata_with_at_least_5_pairs": int((g.matched_pairs >= MIN_PAIRS_STABLE).sum()),
            "strata_with_abs_smd_over_0_10": int((valid.abs_smd_after > 0.10).sum()),
            "strata_with_abs_smd_over_0_20": int((valid.abs_smd_after > 0.20).sum()),
            "worst_abs_smd": float(valid.abs_smd_after.max()) if len(valid) else np.nan,
            "median_abs_smd": float(valid.abs_smd_after.median()) if len(valid) else np.nan,
            "small_strata_only_warning": bool((g.matched_pairs < MIN_PAIRS_STABLE).all())
        })
    output.mkdir(parents=True, exist_ok=True)
    cells.to_csv(output / "asset_direction_covariate_balance_v10_5.csv", index=False)
    pd.DataFrame(ranking_rows).to_csv(output / "covariate_imbalance_by_stratum_v10_5.csv", index=False)
    pd.DataFrame(coverage_rows).to_csv(output / "asset_direction_match_coverage_v10_5.csv", index=False)
    metadata = {
        "study": "Phase 3 V10.5 asset-direction-specific balance attribution",
        "design_grid": "Exactly the six V10.4 designs and four V5 target calipers; no new tuning",
        "matching": "V6 maximum-cardinality 1:1 assignment, exact asset/direction, outcome-blind",
        "diagnostics": "Within each asset-direction stratum, compare matched class covariate means using the V4 SMD definition; also report pre-match SMD and match coverage",
        "small_stratum_threshold_pairs": MIN_PAIRS_STABLE,
        "interpretation": "SMDs in strata with fewer than five pairs are flagged as unstable descriptive diagnostics, not accepted evidence",
        "prohibited_inference": "No outcomes loaded or compared; no causal, strategy, or profitability conclusions",
        "limitations": ["small subgroup samples can make SMDs unstable",
                        "stratum-specific balance does not establish exchangeability",
                        "broad and strict cohorts are nested",
                        "no outcome comparison is performed"]
    }
    (output / "run_metadata_v10_5.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print("V10.5 rows:", len(cells), "subgroup rankings:", len(ranking_rows),
          "coverage rows:", len(coverage_rows))

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for x in ("anatomy", "sequence", "feature-dir", "minute-dir", "output"):
        p.add_argument("--" + x, type=Path, required=True)
    a = p.parse_args()
    run(a.anatomy, a.sequence, a.feature_dir, a.minute_dir, a.output)

if __name__ == "__main__":
    main()
