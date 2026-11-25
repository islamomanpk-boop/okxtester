# Phase 3 Causal Breakout Reconstruction — Implementation Architecture Audit V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Branch at audit:** `price-action-v1`  
**Status:** SOURCE AUDIT COMPLETE — IMPLEMENTATION NOT YET RUN; NO CAUSAL RESULTS OR CANDIDATES

## 1. Scope

This audit checks the frozen causal reconstruction preflight against the recovered original Python source, the accepted historical metadata, the current Module B lifecycle implementation, and the detector feature ledger. It does not modify raw data or run a new event reconstruction.

## 2. Verified source facts

1. The recovered original Python source is `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`, Git blob SHA `95d2975947c449f3813d80ee7b12008db14f071f`.
2. It constructs complete 15M and 4H bars with right-edge labels and left-closed intervals; it uses the intersection of the five canonical 1M timestamp indices.
3. Its 4H context uses the prior 12 completed 4H bars, with rolling high/low extrema shifted by one row. The exact efficiency and overlap expressions are present in the recovered source and must be copied unchanged into the new implementation.
4. Historical P25/P40 are calculated from the non-null **joined 15M channel-width series** using pandas' default linear quantile interpolation. They are retrospective references only.
5. The original crossing mask requires two consecutive 15M rows assigned to the same context snapshot, a previous close at/inside the relevant boundary, and a current close outside it. The new full-universe scan must preserve this crossing definition while separating raw crossing discovery from causal regime eligibility.
6. The historical runtime metadata confirms the canonical source SHA-256 values and the common five-asset timeline of 569,125 timestamps with zero gaps. Per-asset source row counts are BTC 569,125; ETH 569,125; SOL 569,126; DOGE 569,126; AVAX 569,127.
7. The accepted historical reconstruction audit reports 37,941 complete 15M bars and joined 15M rows per asset, 2,370 complete 4H bars, and 2,369 snapshot changes. These are historical audit values to re-verify from the pinned inputs, not hard-coded replacements for runtime checks.
8. The detector feature ledger has 2,358 rows per asset. The expected context relationship remains the documented one-4H offset: breakout context snapshot T corresponds to detector feature availability T minus 4 hours. Exact boundary and width comparisons are required; no nearest-time fuzzy join is permitted.

## 3. Existing Module B is not the causal scanner

`research/phase3_breakout_lifecycle_v1_1.py` verifies and analyzes the already selected historical classifications and their prior-test links. It starts from the retrospective classification CSV, filters the primary 10% zone, and requires the existing 1,592-row selected population. It therefore cannot be repurposed as the full-universe causal scanner: doing so would preserve the retrospective selection bias that the new preflight explicitly forbids.

The existing workflow also has `contents: write` permission and commits reports back to the research branch. It must not be dispatched or reused for this reconstruction.

## 4. Implementation architecture to follow

The new implementation should be a separate, read-only module with these isolated stages:

1. **Immutable input gate:** verify all five source SHA-256 hashes before parsing; validate required OHLCV columns, source rows, unique ordered timestamps, finite/valid OHLCV, and the exact 569,125-row common index.
2. **Bar/context builder:** reproduce the original complete-bar aggregation and context formulas exactly; keep source 1M data immutable.
3. **Availability audit:** backward as-of join 15M close labels to the latest context available at that close; assert no future context, finite geometry, and exact context-to-15M coverage. A context T owns the right-labelled 15M rows with labels T, T+15m, ..., T+3h45m; the next context T+4h takes effect at that close.
4. **Cross-pipeline reconciliation:** compare context timestamp, upper, lower and width to the detector feature ledger using the exact four-hour offset and a predeclared numeric tolerance.
5. **Historical compatibility gate:** compute full-sample joined-15M P25/P40 and reproduce the accepted 20 asset/definition/direction counts exactly before allowing any causal population output. Stop on the first mismatch; do not tune formulas.
6. **Full raw crossing universe:** enumerate unique crossings without first applying historical P25/P40 or the old selected-event ledger. Preserve the original same-snapshot and close-crossing semantics.
7. **Six causal sensitivity variants:** calculate each context's P25/P40 from strictly prior contexts only, on the shared 4H clock, for both unique-4H and joined-15M weighting, and for fixed-180, expanding-prior, and rolling-180 policies. Apply efficiency <= 0.30 and overlap >= 0.70 without changing their source formulas.
8. **Historical reconciliation:** map the old 932 unique selected signal identities to the new event identities and report unchanged, newly eligible, no-longer eligible, and raw-source mismatch separately for every variant, definition, asset and direction.
9. **Descriptive-only outputs:** emit input/context audits, baseline reproduction, thresholds, unique raw crossing ledger with six eligibility pairs, reconciliation, summary counts and run metadata/output hashes. Do not emit candidate IDs, orders, fills, controls, outcomes, inference or PnL.

## 5. Required tests before any full run

Synthetic tests must cover: right-labelled bar boundaries; incomplete 15M/4H exclusion; context snapshot availability at equal timestamps; no future as-of assignment; current-context rows excluded from thresholds; identical prior-context timestamp sets for both populations; 16 complete 15M close labels per full context; all three policy windows and common warm-up; strict nested within broad; one unique event row with six pairs of flags; and historical event identity deduplication independent of strict/broad labels.

## 6. Disposition

This audit is an implementation design checkpoint only. No new source scan or causal threshold calculation was run. It does not select a threshold policy, close G0-04/G0-05, authorize candidate generation or strategy backtesting, or change Gate 0's CONDITIONAL HOLD status.
