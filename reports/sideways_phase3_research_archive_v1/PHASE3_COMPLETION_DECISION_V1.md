# Phase 3 (Sideways / Range) — Research Completion Decision V1

**Status:** Core descriptive research complete; V6 matched-controls branch formally closed as unsuitable for outcome comparison.  
**Decision date:** 2026-11-25  
**Research branch:** `price-action-v1`

## 1. Scope and decision

Phase 3 examined sideways/range market behaviour across BTC, ETH, SOL, DOGE, and AVAX. The completed work is descriptive and historical. It does not establish a profitable trading strategy, causal effect, or live-trading readiness.

The core descriptive work is sufficiently complete to move to Phase 1 (Uptrend / Bullish), while retaining all Phase 3 scripts, source data, reports, and negative findings. This is a research-sequence decision, not a claim that every conceivable sideways-market question has been answered.

## 2. Completed descriptive research

- Historical sideways-boundary event reconstruction and candle-level boundary-interaction / penetration taxonomy.
- Episode/retest anatomy, forward-path outcomes, and group summaries.
- Early-path sequence and follow-through study.
- Calendar moving-block bootstrap contrasts.
- Per-asset and leave-one-asset-out robustness analysis.
- Breakout prior-test count and descriptive forward-outcome studies.
- Five-asset source-data quality and timestamp-alignment checks.

The boundary-interaction taxonomy archive records 153,540 candle-level observations across five assets, two overlapping context definitions, upper/lower boundaries, and 5%, 10%, and 15% approach bands. It excludes the final truncated 4-hour snapshot interval, suppresses the first 15-minute candle after snapshot availability, and does not bridge timestamp gaps. Consecutive candle observations are not independent episodes.

Primary archives:
- `reports/sideways_boundary_interaction_taxonomy_v1/`
- `reports/breakout_prior_test_count_v1/`
- `reports/breakout_forward_outcome_v1/`
- `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/`
- `reports/sideways_phase3_research_archive_v1/early_path_followthrough_v1/`
- `reports/sideways_phase3_research_archive_v1/sequence_block_bootstrap_v1/`
- `reports/sideways_phase3_research_archive_v1/asset_robustness_v1/`

## 3. Matched-controls branch: final decision

The matched-controls investigation is retained as an audit trail, not accepted as a valid basis for comparing future outcomes. V6 achieved maximum feasible pair counts for its candidate graph, but balance and joint common support remained inadequate. V7–V10.10 examined cohort quality, support, balance, matching sensitivity, and distributional overlap. V10.11 then tested four predeclared percentile definitions without changing V6 pairs or matching rules.

### V10.11 frozen-cohort sensitivity

| Joint-support range | Broad pairs retained (calipers 0.25 / 0.50 / 0.75 / 1.00) | Strict pairs retained (same order) |
|---|---:|---:|
| Central 80% (10th–90th) | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Central 90% (5th–95th) | 2 / 2 / 2 / 2 | 0 / 0 / 0 / 0 |
| Central 95% (2.5th–97.5th) | 6 / 8 / 8 / 7 | 2 / 5 / 7 / 9 |
| Central 98% (1st–99th) | 9 / 14 / 14 / 16 | 3 / 6 / 9 / 11 |

At central 98%, pooled eligible-event retention was only 29.14% for broad separation events, 27.23% for broad retest events, 18.23% for strict separation events, and 20.36% for strict retest events. At the central-90% V10.10 baseline, the V10.11 aggregate exactly reproduces V10.10: 2 broad pairs and 0 strict pairs retained at both endpoints for every caliper.

No individual covariate had a completely disjoint central interval in the reported strata; nevertheless, intersecting support across all usable dimensions retained only a small fraction of events and pairs. The fact that some marginal overlap exists does not make the joint cohort adequate.

**Decision:** Stop the V6 matched-controls branch for this cohort. Do not widen percentiles further, alter matching constraints to force a larger sample, rematch, or compare future outcomes using these cohorts. Preserve all V1–V10.11 scripts and archives, including failed and rejected approaches, for reproducibility.

V10.11 archive:
`reports/sideways_phase3_research_archive_v1/joint_common_support_percentile_sensitivity_v10_11/`

Successful final workflow:
https://github.com/islamomanpk-boop/okxtester/actions/runs/45527535621

## 4. Interpretation safeguards

- The broad and strict cohorts overlap; they are not independent samples.
- Candle-level observations and repeated events can be dependent.
- Historical forward outcomes and bootstrap contrasts are exploratory observational associations, not causal estimates.
- Residual covariate imbalance in earlier matched cohorts remains a limitation; the later common-support audits do not erase it.
- No Phase 3 result establishes a tradable edge or justifies strategy selection, parameter optimization, or live deployment.

## 5. Research sequence handoff

Proceed in the agreed order:
1. **Phase 1 — Uptrend / Bullish**
2. Phase 2 — Downtrend / Bearish
3. Phase 4 — Choppy / High Volatility
4. Phase 5 — Transition / Expansion

Phase 1 begins as a separate descriptive research phase. First define and validate bullish/uptrend context and event labels, audit data availability and causal timestamps, then study event anatomy and forward behaviour. Do not reuse sideways-specific definitions without justification and do not begin strategy optimization.

## 6. Reproducibility

V10.11 used the frozen V6 pair file and the same eligible pre-event covariate source. The four percentile ranges were fixed before execution. No future-outcome data were loaded or compared, and no rematching occurred. The archived CSV and JSON outputs are the authoritative detailed record.
