# Sideways Boundary Interaction and Penetration Taxonomy V1
## Historical Results and Reporting Audit

Date: 2026-11-24
Project: OKX Price Action V1
Phase: Phase 3 — Sideways / Range
Status: HISTORICAL RUN COMPLETED — REPORT AUDITS PASSED
Specification: Frozen V1 specification dated 2026-11-24
Implementation: sideways_boundary_interaction_taxonomy_v1.py

---

## 1. Research scope

This study measures candle-level price interaction with frozen upper
and lower boundaries from historically available 4H sideways snapshots.

Assets:
- BTC
- ETH
- SOL
- DOGE
- AVAX

Range definitions:
- STRICT_P25
- BROAD_P40

Approach bands:
- 5% of channel width
- 10% of channel width (primary)
- 15% of channel width

The study is descriptive. It does not test a trading strategy.

## 2. Run outcome and observation counts

The corrected historical run completed successfully.

- Candle-side observation rows: 153,540
- Underlying unique candle observations: 76,770
- Assets: 5
- Range definitions: 2
- Boundary sides: UPPER and LOWER
- Snapshot audit rows: 23,580
- Chronological summary rows: 1,617
- Final truncated 4H snapshot: excluded from primary observations
- Source hash verification: enabled; corrected SOL manifest hash used
- Timestamp policy: strict continuous 15-minute cadence; no gaps bridged

Each eligible underlying candle contributes one upper-side and one
lower-side observation.

## 3. Primary 10% interaction class distributions

Counts and proportions below are aggregated across assets and both
boundary sides within each range definition. Denominators are therefore
side-observation totals, not independent episode counts.

### STRICT_P25

| Interaction class | Count | Denominator | Proportion |
|---|---:|---:|---:|
| APPROACH_ONLY | 2,831 | 61,860 | 4.58% |
| BOUNDARY_TOUCH | 32 | 61,860 | 0.05% |
| CLOSE_OUTSIDE | 2,544 | 61,860 | 4.11% |
| NO_APPROACH | 55,562 | 61,860 | 89.82% |
| REENTRY_INSIDE | 311 | 61,860 | 0.50% |
| WICK_PENETRATION | 580 | 61,860 | 0.94% |

### BROAD_P40

| Interaction class | Count | Denominator | Proportion |
|---|---:|---:|---:|
| APPROACH_ONLY | 4,021 | 91,680 | 4.39% |
| BOUNDARY_TOUCH | 42 | 91,680 | 0.05% |
| CLOSE_OUTSIDE | 3,461 | 91,680 | 3.78% |
| NO_APPROACH | 82,944 | 91,680 | 90.47% |
| REENTRY_INSIDE | 421 | 91,680 | 0.46% |
| WICK_PENETRATION | 791 | 91,680 | 0.86% |

NO_APPROACH is the dominant class in both definitions.
Exact boundary contact is rare under the exact-equality rule.

## 4. Dual-boundary interactions

The dual-boundary flag is defined as both sides having a non-NO_APPROACH
classification under the widest 15% approach band. Each underlying
candle is counted once.

All ten asset/definition groups reported zero dual-boundary candles.

The independent report audit recomputed this flag from both side
classifications for 76,770 unique candles and found no mismatches.

## 5. Penetration findings

Penetration means movement strictly beyond the exact frozen boundary.
It is not approach-band entry.

Across the asset/definition/side groups, penetration rates ranged
approximately from 4.54% to 6.54% of side observations.

Examples:
- SOL BROAD_P40 LOWER: 6.41%
- SOL STRICT_P25 LOWER: 6.54%
- BTC BROAD_P40 LOWER: 5.16%
- ETH BROAD_P40 LOWER: 5.27%
- AVAX BROAD_P40 UPPER: 4.54%

Positive penetration-depth distributions were calculated using only
strictly positive depths. Zero-depth observations were counted
separately.

The largest reported 90th-percentile positive penetration depth among
the displayed groups was approximately 1.168 channel widths
(ETH STRICT_P25 LOWER). This is a normalized descriptive measurement,
not a forecast or stop-distance recommendation.

Full asset/definition/side statistics are preserved in:
penetration_depth_summary_v1.csv

## 6. STRICT_P25 versus BROAD_P40

The supplied primary-band comparison summary averaged the
BROAD_P40-minus-STRICT_P25 proportion difference across ten
asset/side comparisons per class.

| Interaction class | Mean difference |
|---|---:|
| APPROACH_ONLY | -0.18 percentage points |
| BOUNDARY_TOUCH | -0.01 percentage points |
| CLOSE_OUTSIDE | -0.34 percentage points |
| NO_APPROACH | +0.65 percentage points |
| REENTRY_INSIDE | -0.04 percentage points |
| WICK_PENETRATION | -0.07 percentage points |

The average differences are small, but individual asset/side
differences remain. STRICT_P25 and BROAD_P40 cohorts overlap and
must not be treated as independent samples.

## 7. Reporting and integrity audits

Completed checks include:

- Main observation row count: 153,540.
- Five expected assets present.
- Both range definitions and both boundary sides present.
- No duplicate side-observation keys.
- Upper/lower pairing reconciles to 76,770 underlying candles.
- OHLC geometry independently reproduced.
- 5%, 10%, and 15% class labels independently reproduced.
- All class labels valid.
- Class summary contains 360 rows.
- Class counts reconcile to their denominators.
- Class proportions sum to one within groups.
- All 360 class-count entries independently matched raw observations.
- Snapshot audit contains 23,580 rows with unique snapshot keys.
- First-bar suppression and eligible-bar accounting reconcile.
- Nonqualifying snapshots and the final truncated snapshot contribute
  no primary observations.
- Expected side rows from the snapshot audit equal 153,540.
- Dual-boundary summary reconciles.
- Dual-boundary flags match both-side 15% classifications across
  76,770 unique candles.
- Penetration counts, rates, and positive-depth statistics reconcile.
- Dual summary: 10 rows.
- Observation audit: 20 rows.
- Upper/lower comparison: 180 rows.
- Strict/broad comparison: 180 rows.
- Strong-rejection comparison: 185 rows.
- Chronological summary: 1,617 rows.
- Upper/lower, strict/broad, and strong-rejection comparison reports
  contain no null values.
- Strong-rejection proportions sum to one.

The final report-audit command passed 12/12 checks with zero failures.
Earlier independent audits and the 360-entry class reconciliation
also passed.

## 8. Interpretation limits

These are candle-level observations. Consecutive candles may belong
to the same underlying market episode and are not independent tests.

The results do not establish:
- independent episode frequencies;
- predictive value;
- causal effects;
- successful or failed breakout outcomes;
- profitable entries or exits;
- executable fills;
- net returns after fees, slippage, or funding;
- strategy robustness.

The strong-rejection flag is retained as a reference classification.
It does not turn the interaction classes into validated rejection
or breakout-failure outcomes.

No trading rule or strategy selection is authorized by these results.

## 9. Preserved report inventory

Directory:
reports/sideways_boundary_interaction_taxonomy_v1/

Expected files:
1. candle_level_interactions_v1.csv
2. chronological_subperiod_summary_v1.csv
3. class_counts_proportions_v1.csv
4. dual_boundary_summary_v1.csv
5. observation_audit_v1.csv
6. penetration_depth_summary_v1.csv
7. run_metadata_v1.json
8. snapshot_tail_audit_v1.csv
9. strict_broad_class_comparison_v1.csv
10. strong_rejection_reference_comparison_v1.csv
11. upper_lower_class_comparison_v1.csv

Corrected successful run log:
reports/sideways_boundary_interaction_taxonomy_v1_run_2026-11-24_corrected_hash.log

The earlier failed-run log is separate and remains preserved:
reports/sideways_boundary_interaction_taxonomy_v1_run_2026-11-24.log

## 10. Version-control status

The corrected implementation, regression test, frozen specification,
and SOL hash-correction checkpoint were previously committed and
verified on GitHub branch price-action-v1.

This results checkpoint, the 11 generated report files, and the
corrected successful run log must be committed separately.

Do not overwrite the original specification, implementation, tests,
provenance, or earlier failed-run evidence.

---

End of results checkpoint.
