# Sideways Boundary Interaction Taxonomy V1 — Reporting and Audit Corrections

Date: 2026-11-24  
Branch: `price-action-v1`  
Applies to: `research/sideways_boundary_interaction_taxonomy/sideways_boundary_interaction_taxonomy_v1.py`  
Specification: `docs/research_checkpoints/2026-11-24_sideways_boundary_interaction_taxonomy_spec_v1.md`  
Data-source amendment: `docs/research_checkpoints/2026-11-24_sideways_boundary_interaction_taxonomy_spec_v1_data_source_amendment.md`

## 1. Purpose

A pre-run code review identified reporting and reconciliation gaps. This checkpoint records the corrections made before any historical taxonomy study run. The frozen interaction definitions, thresholds, cohort definitions, input files, source hashes, and final-tail exclusion policy were not changed.

## 2. Corrections implemented

1. **Penetration distributions:** distribution statistics now use strictly positive penetration depths only. Zero-penetration observations and the penetration rate are reported separately. If a group has no positive penetration, its positive-depth statistics are null/NaN rather than misleading zero quantiles.
2. **Upper-versus-lower comparison:** added `upper_lower_class_comparison_v1.csv`, with each side's count, denominator, proportion, and lower-minus-upper proportion difference for every asset, definition, band, and class.
3. **STRICT_P25-versus-BROAD_P40 comparison:** added `strict_broad_class_comparison_v1.csv`, with both cohort denominators and proportions. The cohorts overlap; this is descriptive and does not treat them as independent.
4. **Strong-rejection reference comparison:** added `strong_rejection_reference_comparison_v1.csv`, cross-tabulating the unchanged reference flag against the primary 10% interaction class, with denominators and proportions.
5. **Chronological subperiods:** added `chronological_subperiod_summary_v1.csv`, using UTC calendar quarters and retaining asset, definition, side, band, class, count, denominator, and proportion. Partial calendar quarters remain visible and are not annualized.
6. **Snapshot/exclusion accounting:** replaced the ambiguous `eligible_bars_before_tail_rule` label with explicit counts after first-bar suppression, counts excluded by nonqualifying context, counts excluded by the final-tail rule, included primary 15-minute bars, and expected side-row counts. Exclusion-reason counts can overlap when the final snapshot also fails the range cohort.
7. **Observation reconciliation:** the implementation now checks that produced upper/lower side rows equal twice the number of included primary 15-minute bars recorded by the snapshot audit.
8. **Dual-boundary counting:** dual-boundary interactions are now counted once per underlying candle, not twice because the candle has both an upper-side and lower-side row.
9. **Feature input row count:** the feature files are required to contain the 2,358 snapshots documented in the provenance amendment.

## 3. New or revised report files

The output directory remains:

`reports/sideways_boundary_interaction_taxonomy_v1/`

New outputs:
- `upper_lower_class_comparison_v1.csv`
- `strict_broad_class_comparison_v1.csv`
- `strong_rejection_reference_comparison_v1.csv`
- `chronological_subperiod_summary_v1.csv`

Revised outputs:
- `penetration_depth_summary_v1.csv`
- `dual_boundary_summary_v1.csv`
- `snapshot_tail_audit_v1.csv`
- `run_metadata_v1.json`

Existing candle-level and class-count outputs remain.

## 4. Validation status and execution gate

The original 16 classification tests passed in Termux on 2026-11-24. Four reporting-helper tests have now been added, covering positive-only penetration statistics, the no-penetration case, upper/lower comparison denominators, and strict/broad comparison selection.

The updated code and expanded test suite have been committed to GitHub, but the expanded tests have **not yet been run in the user's Termux environment**. No historical taxonomy data run has been performed by this corrected implementation.

Before historical execution:
1. synchronize the branch in Termux;
2. run Python syntax compilation and the full targeted unit-test file;
3. stop on any failure;
4. only after tests pass, execute the five-asset historical run with source-hash verification enabled;
5. inspect every output and audit before accepting results.

## 5. Interpretation limits

All new comparisons are descriptive. STRICT_P25 is contained within BROAD_P40 and the cohorts overlap. Consecutive 15-minute observations are not independent episodes. Calendar-quarter summaries describe sample composition and do not establish temporal stability, prediction, causality, or profitability.

The frozen specification and its data-source amendment remain unchanged. No original reconstruction script, test, report, or raw data file was modified.
