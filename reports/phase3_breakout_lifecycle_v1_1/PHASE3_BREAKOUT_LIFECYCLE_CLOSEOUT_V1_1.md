# Phase 3 Breakout / Failed-Breakout Lifecycle V1.1 — Formal Closeout

**Decision date:** 2026-11-25  
**Project:** OKX Price Action Strategy V1 — Phase 3 Sideways / Range  
**Gate:** Gate 1 — Complete descriptive lifecycle  
**Module:** B — Breakout continuation, failure, reclaim and reversal lifecycle  
**Decision:** **ACCEPTED — descriptive lifecycle evidence, with explicit benchmark limitations**  
**Strategy authorization:** None. This closeout does not authorize Gate 2 or any strategy PnL backtest.

## 1. Decision and scope

Module B V1.1 is accepted as a completed descriptive lifecycle study for the frozen primary population and definitions in the parent protocol and V1.1 amendment. The study provides event-level breakout continuation, 1-minute return-inside, completed-15-minute failure confirmation, reclaim, outside retest, inside retest, reversal path and overlap-cluster measurements.

Acceptance is limited to the five archived assets (BTC, ETH, SOL, DOGE, AVAX), the primary 10%-of-channel prior-test classification zone, BROAD_P40 and nested STRICT_P25 definitions, UPPER and LOWER directions, and the fixed 15M/1H/4H/12H horizons. The post-breakout retest band is the amended ±0.10% of frozen boundary price—not 10% of channel width.

Five lifecycle retest fields are not present in the frozen forward-outcome archive and therefore have no independent historical benchmark in that archive. They are accepted only as descriptive measurements produced from the frozen 1M source under the amended definitions, supported by code review, synthetic edge-case tests, output reconciliation and deterministic rerun. They must not be described as independently cross-validated against the forward archive.

## 2. Frozen protocol and implementation identity

Controlling documents:
- `docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md`
- `docs/research_checkpoints/2026-11-25_phase3_breakout_lifecycle_v1_1_amendment.md`

Immutable recovered original source:
- `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`
- Git blob SHA: `95d2975947c449f3813d80ee7b12008db14f071f`

Implemented analysis at the reproducibility run:
- `research/phase3_breakout_lifecycle_v1_1.py`
- Git blob SHA: `f272b90344320c884f84b5c13752377f74a5eb99`

Synthetic tests:
- `tests/test_phase3_breakout_lifecycle_v1_1.py`
- Git blob SHA: `5235732f90c76cde7ee3195a5a2798020ca7099c`
- 23 test methods; all 23 passed in both reproducibility runs.

## 3. Source population and provenance checks

The historical run reproduced:
- 1,592 unique primary event keys: 932 BROAD_P40 and 660 STRICT_P25 (strict is nested, not an independent cohort).
- Direction counts: 823 UPPER and 769 LOWER.
- Asset counts: BTC 349, ETH 266, SOL 361, DOGE 276, AVAX 340.
- All 20 original event-count reproduction rows and all 10 original quantile reproduction rows.
- 1,537 prior-touch-test links; 160 events correctly have zero prior touch tests; zero prior-link-count mismatches.
- 5 reconstruction-audit rows.
- 6,368 event/horizon rows and 6,368 forward-archive comparison rows; all 6,368 matched across the 18 fields available in the frozen forward archive.

The five 1M source files are pinned by Git blob and SHA-256 in `run_metadata_v1_1.json`. Source row counts were BTC 569,125; ETH 569,125; SOL 569,126; DOGE 569,126; AVAX 569,127. The five sources share 569,125 common minute timestamps, with zero gaps in the common aligned timeline.

The 1,592 event identities, source joins, prior-link counts, frozen boundaries, signal-to-first-1M mapping, source hashes and forward archive comparisons passed the recorded reproduction gates. No event population was silently expanded or deduplicated; strict remains a nested sensitivity cohort.

## 4. Lifecycle output and censoring

The 6,368 horizon rows comprise 1,592 rows at each of 15M, 1H, 4H and 12H. All 6,368 horizons are marked COMPLETE. No horizon rows were censored in the accepted primary output.

Event-level first-passage totals:
- 1,363 events have a 1-minute return-inside timestamp.
- 1,289 events have a completed-15-minute return-inside confirmation.
- 1,029 events have a subsequent breakout-side reclaim timestamp.
- 14 events have the first post-signal entry open already through the frozen boundary.

Outside-retest state counts:
- 921 before the first 1-minute return-inside.
- 107 in the same 1-minute bar as the return-inside (ordering ambiguous).
- 275 after the first 1-minute return-inside.
- 197 with no outside retest within 12 hours.
- 92 with no 1-minute return-inside within 12 hours.

Outside-retest hold status:
- 947 HELD_OUTSIDE.
- 448 CLOSED_BACK_INSIDE.
- 197 blank because no outside retest was recorded.

Inside-retest state counts:
- 630 RETEST_AFTER_MOVING_AWAY.
- 551 SAME_BAR_AMBIGUOUS.
- 303 NO_15M_FAILURE_CONFIRMATION.
- 85 NO_INSIDE_RETEST_WITHIN_WINDOW.
- 23 ALREADY_IN_BAND_AT_FAILURE_CONFIRMATION.

Ambiguity totals are kept separate: 107 outside-retest same-bar ordering ambiguities and 551 inside-retest same-bar ordering ambiguities. The 630 confirmed inside retests after separation are distinct from the ambiguous cases. No intraminute OHLC ordering is inferred.

Overlap clustering produced 454 clusters across the five assets (BTC 99, ETH 86, SOL 98, DOGE 77, AVAX 94); the largest cluster contains 18 events. Strict/broad membership is preserved and not treated as independent observations.

## 5. Synthetic coverage and code-review corrections

The 23-test suite includes coverage for:
- strict-within-broad nesting and duplicate immutable event identity rejection;
- upper/lower outside retest symmetry, exact outer-band equality and 0.10%-of-boundary geometry;
- 1-minute return-inside equality and availability timestamp;
- completed-15-minute failure, strict-later close timing and reclaim;
- inside retest after moving away, already-in-band state and upper/lower same-bar ambiguity;
- complete 15-minute construction and missing-minute rejection;
- forward-archive cross-check field scope;
- separate ambiguity counts in group summaries;
- transitive, asset-scoped overlap clusters and half-open window boundaries;
- immediate adverse entry, incomplete-horizon censoring and completed-15-minute close availability.

Independent review corrections are retained in the commit history: strict-later 15-minute close timing, same-bar ambiguity classification, separate group-summary ambiguity counts, explicit horizon-censoring and 15-minute availability tests, strict/broad nesting guard, and duplicate source-event identity guard.

## 6. Reproducibility decision

Two successful workflow runs:
- [45644799449](https://github.com/islamomanpk-boop/okxtester/actions/runs/45644799449), commit `d791361a7fea4aa448907de3dfb5d3559c194d60`.
- [45645349572](https://github.com/islamomanpk-boop/okxtester/actions/runs/45645349572), commit `90d0d5417830fac50a712c4418b6cb65e86c7a1f`.

Both runs passed all 23 synthetic tests and completed frozen historical generation. The second run's commit comparison against the first contains only a workflow comment and documentation changes; the analysis script, test file, frozen input files and report schema are unchanged. The second workflow's report-commit step stated `No report changes to commit.` Therefore the regenerated research output files were byte-identical to the checked-in outputs from the first run. The two ZIP artifact digests differ at the packaging level; this does not contradict the identical file outputs. **The same-code, same-test, same-input, same-schema deterministic-output criterion is accepted.**

## 7. Forward archive limitations and unbenchmarked fields

The frozen forward-outcome archive does not contain these five Module B lifecycle fields:
1. `outside_retest`
2. `outside_retest_boundary_crossed`
3. `outside_retest_minutes`
4. `outside_retest_depth_pct_of_boundary`
5. `outside_retest_hold`

All other 18 archived fields per event/horizon row were compared and matched for all 6,368 rows. The five listed lifecycle fields were not independently benchmarked against that archive. Their inclusion is justified only as new descriptive measurements from the pinned 1M OHLC source, under the frozen amendment, with synthetic tests and explicit same-bar ambiguity handling. No claim is made that a separate historical implementation or independent data source validates those five fields.

Additional limitations:
- 1M OHLC cannot reveal the order of prices touched inside a minute; ambiguous states are retained.
- Overlapping event windows are dependent; clusters are reported, but no independent-event standard errors, p-values or causal claims are made.
- Original full-sample P25/P40 thresholds are retrospective and are not live-calibrated.
- This is not an execution study. A path extreme or boundary touch is not a fill.
- The study does not establish predictiveness, profitability, or suitability for live trading.

## 8. Explicit exclusions

No orders, fills, limit-order queue modelling, spread, slippage, fee, funding, position sizing, stop/target, PnL, return-on-capital, profitability, causal or live-readiness calculations were performed. No entry, exit, risk or strategy parameters were selected. Gate 2 execution-resolution research and Gate 6 strategy backtesting are not authorized by this module closeout.

## 9. Formal disposition

**Module B V1.1: ACCEPTED as descriptive lifecycle evidence, with the five unbenchmarked fields explicitly limited as described above.**

This closes the Module B research deliverable under Gate 1. Together with the previously accepted Module A rejection lifecycle, the descriptive lifecycle scope in Gate 1 is complete. The overall Phase 3 programme is not complete: **Gate 0 remains CONDITIONAL HOLD**, so Gate 2 remains closed. No strategy backtest or Phase 1 handoff is authorized.

Next permitted work is Gate 0 blocker resolution only: runtime source/event availability and provenance, three-family Phase 3 candidate generation, real-input funding integration and settlement mark policy, fee/instrument verification, and execution-engine acceptance.
