# G0-05 Threshold Policy and Calibration Population Decision — V1

**Date:** 2026-11-26  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Dependency:** G0-04 accepted by delegated project-owner disposition; see `2026-11-26_g0_04_acceptance_decision_v1.md`.  
**Status:** G0-05 design decision; no canonical candidate generation has been run.  
**Evidence artifact:** G0-04 run 45756061179, artifact 15087542445, ZIP SHA-256 `ef6204b546b49880675514bf76b4f6cb86e2821ba2b0d1d5412549927388f0a1`.

## 1. Decision

For the primary G0-05 causal candidate-availability contract, use:

- **Threshold policy:** `EXPANDING_PRIOR`
- **Calibration population:** `UNIQUE_4H_FEATURE_ROWS`
- **Warm-up:** minimum 180 prior completed 4-hour contexts; the current context is never included in its own calibration.
- **Definitions:** preserve both `STRICT_P25` and `BROAD_P40` as separately labelled nested eligibility cohorts. Do not collapse them into one label.
- **Sensitivity evidence:** retain `FIXED_180`, `ROLLING_180`, and `JOINED_15M_ROWS` results as explicit alternatives. Do not erase or rewrite G0-04 outputs.

This is a methodological choice for descriptive candidate availability, not a claim of superior trading performance. No PnL, execution or outcome data were used to select it.

## 2. Why this is the primary contract

1. The signal's regime state is represented by a completed 4-hour context. Giving each completed 4-hour feature row one calibration observation makes the statistical unit match the state being classified.
2. `JOINED_15M_ROWS` is a different population: the 15-minute channel width can vary within a 4-hour context, so it can weight a context multiple times and produce materially different expanding-prior quantiles. It is preserved as sensitivity evidence rather than treated as interchangeable with unique 4-hour rows.
3. `EXPANDING_PRIOR` uses all available prior completed contexts after the fixed 180-context warm-up. It avoids freezing the calibration forever at the first 180 contexts (`FIXED_180`) and avoids the abrupt sample turnover of a rolling 180-context window (`ROLLING_180`). Its slower adaptation is a known trade-off; rolling remains a mandatory sensitivity comparison.
4. The historical full-sample P25/P40 reconstruction remains a separate descriptive baseline. It is not the causal threshold used for candidate availability.

## 3. Recomputed sensitivity summary

The figures below were recalculated from the frozen G0-04 artifact's unique raw crossing event ledger. Total raw crossing identities: **2,861**; historical selected identities: **932**.

| Policy | Population | Strict eligible | Broad eligible | Broad-only increment |
|---|---|---:|---:|---:|
| FIXED_180 | UNIQUE_4H_FEATURE_ROWS | 1,081 | 1,156 | 75 |
| FIXED_180 | JOINED_15M_ROWS | 1,081 | 1,156 | 75 |
| EXPANDING_PRIOR | UNIQUE_4H_FEATURE_ROWS | 794 | 1,038 | 244 |
| EXPANDING_PRIOR | JOINED_15M_ROWS | 794 | 1,039 | 245 |
| ROLLING_180 | UNIQUE_4H_FEATURE_ROWS | 704 | 960 | 256 |
| ROLLING_180 | JOINED_15M_ROWS | 704 | 960 | 256 |

All counts are descriptive eligibility counts, not trades or performance outcomes. Strict eligibility is nested within broad eligibility in every variant.

### Policy agreement (unique 4-hour population)

| Comparison | Strict Jaccard | Broad Jaccard | Strict identities differing | Broad identities differing |
|---|---:|---:|---:|---:|
| FIXED_180 vs EXPANDING_PRIOR | 0.733 | 0.893 | 289 | 124 |
| FIXED_180 vs ROLLING_180 | 0.638 | 0.813 | 395 | 218 |
| EXPANDING_PRIOR vs ROLLING_180 | 0.756 | 0.871 | 208 | 138 |

The variants are not interchangeable. This is why the chosen primary policy and all sensitivity variants must remain explicitly versioned.

### Population sensitivity

- FIXED_180: no event-eligibility differences between the two populations.
- EXPANDING_PRIOR: strict eligibility is identical; broad eligibility differs for one raw event (joined-15M marks one additional event eligible).
- ROLLING_180: no event-eligibility differences; a maximum P40 numerical difference of approximately 8e-14 is present in the threshold table and does not change event flags.
- For EXPANDING_PRIOR, unique-4H versus joined-15M P25 values differ in 3,083 of 10,885 asset/snapshot rows (maximum absolute difference approximately 0.1164); P40 differs in 4,405 rows (maximum approximately 0.1032). This confirms the populations are not equivalent when the 15-minute width varies within a 4-hour context.

## 4. Limitations and controls

- This choice is based on unit-of-analysis coherence and transparent causal timing, not on realized outcome quality.
- Expanding-prior calibration can adapt slowly after a structural change. The rolling-180 alternative must therefore remain visible in all sensitivity reports.
- The first 180 completed prior contexts remain warm-up and ineligible. G0-04 recorded 262 raw crossing events without threshold rows; these remain ineligible under all variants.
- Two SOL events with undefined efficiency/overlap remain explicitly ineligible. Twelve legacy ratio-efficiency values above 1 remain valid under the preserved legacy formula and must not be confused with the detector's difference-based efficiency measure.
- Both strict and broad cohorts must be emitted separately; do not choose between them based on candidate counts.
- This decision does not define rejection-family confirmation, de-clustering, invalidation or expiry; those remain separate G0-05 contract decisions.
- No order, fill, synthetic execution price, stop, target, PnL, profitability statistic, strategy backtest or OOS claim is authorized.

## 5. Next G0-05 work

Before any canonical candidate generator is run, freeze and test:
1. Exact snapshot refresh/validity interval and inclusive/exclusive endpoint semantics.
2. Support/resistance rejection source mapping and completed-15-minute confirmation time.
3. Rejection repeated-test/de-clustering, invalidation and expiry rules.
4. Breakout continuation repeated-cross and episode/de-clustering rules.
5. Failed-breakout reversal confirmation and linkage to an eligible source breakout.
6. Input manifests, schemas, blob IDs, hashes and all family-level reconciliation rules.
7. The complete synthetic edge-case matrix and deterministic rerun requirements.

**Current status:** primary threshold policy/population selected for the G0-05 contract. Candidate generation remains blocked until all remaining family-specific and snapshot decisions are frozen and the complete synthetic contract passes.
