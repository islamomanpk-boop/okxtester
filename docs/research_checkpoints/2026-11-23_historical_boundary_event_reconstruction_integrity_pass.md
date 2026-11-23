# Historical Boundary Event Reconstruction V1 — Integrity Validation Pass

Date: 2026-11-23  
Branch: `price-action-v1`  
Research script: `research/sideways_boundary_events_historical_v1.py`  
Output directory (local Termux): `reports/sideways_boundary_events_historical_v1/`

## Status

**PASS — reconstruction integrity checks passed (6/6).** This validates the generated event ledger and summary reconciliation under the documented historical protocol. It does not validate predictive power or profitability.

## Cohort totals

| Cohort | Test rows | First strong rejections | Incidence |
|---|---:|---:|---:|
| Strict (P25 width) | 1,031 | 838 | 81.28% |
| Broad (P40 width) | 1,421 | 1,154 | 81.21% |

Incidence is first-strong-rejection events divided by reconstructed tests within that cohort.

**Overlapping cohort warning:** The strict cohort is fully contained in the broad cohort. The integrity check confirmed every strict event exists identically in the broad cohort. Therefore, the 2,452 rows (1,031 strict + 1,421 broad) and 1,992 rejection rows are sums across two overlapping labels, not unique independent events. The broad cohort is the inclusive population of 1,421 tests; strict is its 1,031-test subset. Do not pool the two cohort rows as if independent.

## Integrity checks — all passed

1. Test identifiers are unique within the specified asset/definition/direction/snapshot/segment/rank key.
2. Every recorded first-rejection timestamp lies within its test start/end boundaries.
3. No test begins before the first eligible 15-minute candle after snapshot availability.
4. Every test end timestamp is greater than or equal to its start timestamp.
5. Every strict event is present identically in the broad cohort.
6. Snapshot test-count distributions reconcile to qualifying snapshot totals.

## Source and reconstruction audit

The reconstruction audit reported, for each of five assets and both definitions:
- 37,941 source 15-minute rows.
- 2,358 detector feature rows.
- Zero global 15-minute timestamp gaps.
- Every qualifying snapshot had its first observed 15-minute bar suppressed as specified.
- Zero 15-minute gaps inside processed snapshot intervals.

Snapshot distribution includes zero-test snapshots and reconciles to the qualifying snapshot count for each asset, definition, and direction.

## Interpretation and limitations

- The 81.28% strict and 81.21% broad figures are **historical descriptive incidence rates**: the proportion of reconstructed boundary tests that recorded a first strong rejection under the fixed event definitions.
- They are not trade win rates, probabilities of profitable trades, evidence of a tradable edge, or forward-return results.
- Many tests terminate at snapshot end; test-rank and repeat-test statistics must be interpreted with that censoring/termination mechanism in mind.
- Strict and broad cohorts overlap; upper/lower direction cohorts can also overlap. Do not add cohort counts to infer independent events.
- Width P25/P40 thresholds are full-sample historical quantiles and remain retrospective/exploratory, not live-safe thresholds.
- No 1-minute execution outcomes, forward returns, fills, fees, slippage, funding, or portfolio performance were tested in this reconstruction.
- Earlier 2,095-event outcome work remains unreconciled and must not be reused as accepted results.

## Local artifacts

The run generated:
- `boundary_tests_historical_v1.csv`
- `rejection_incidence_by_rank_v1.csv`
- `snapshot_test_count_distribution_v1.csv`
- `reconstruction_audit_v1.csv`

These are in the local Termux output directory listed above. This checkpoint records the validated findings; it does not claim that those CSV files have been committed to GitHub.

## Next research step

Before studying forward outcomes, perform a focused review of the reconstruction implementation and output semantics (especially snapshot-end termination and eligible-bar cutoff behavior). Then design a separate, causally aligned 1-minute outcome study using only the accepted reconstructed event ledger, with explicit outcome definitions and realistic costs. Keep descriptive event incidence separate from trade performance.
