# Breakout Event Reproduction Conflict — HOLD

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** HOLD — accepted event-count reproduction is not independently reproduced  
**Scope:** Read-only rerun of the variant diagnostic after correcting its timestamp-resolution guard.

## Latest Termux result

- Corrected continuity audit: all five 1M source indexes have zero duplicates and zero non-one-minute intervals.
- Common five-asset index: 569,125 timestamps; zero non-one-minute intervals.
- Diagnostic ran successfully after commit `4db5840`.
- All four tested combinations produced **0/20 exact matches** against the accepted reference:
  - UNIQUE_4H quantiles + accepted mask
  - UNIQUE_4H quantiles + archived mask
  - JOINED_15M quantiles + accepted mask
  - JOINED_15M quantiles + archived mask
- For each asset/definition/direction, eligible 15M follow-up count equalled raw count.
- The archived-mask and accepted-mask counts were identical in all 20 rows for both quantile populations.

## Important source discrepancy

The recovered archived script `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh` computes quantiles from unique 4H feature rows and uses:
`selected & previous_selected & same_snapshot`.

The accepted reference checkpoint `2026-11-22_original_breakout_event_reproduction_pass.md` instead records joined-15M-observation quantiles and explicitly says no additional previous-sideways requirement was used.

The new diagnostic tests both quantile populations and both mask variants, but neither reproduces the accepted counts. Therefore neither the recovered archived script nor the current diagnostic has established the precise source/method that generated the accepted 20-count reference.

Some thresholds in the diagnostic agree with accepted thresholds (for example BTC P25 and several P40 values), but event counts still differ materially. Threshold agreement alone is not validation.

## Interpretation

The previous continuity failure was a diagnostic bug caused by assuming nanosecond timestamp storage. That issue is corrected and is not a data-gap finding.

The current event-count discrepancy is a separate unresolved research-method/source issue. Do not attribute it to timestamp continuity, and do not tune filters or thresholds to force a match.

The accepted 20-count PASS checkpoint is retained as a historical record of what was reported on 2026-11-22, but it is now under an independent-reproduction hold pending recovery of the exact producing source and inputs.

## Required next steps

1. Locate the exact script or command that generated the accepted 20 event counts and its contemporaneous output/log.
2. Verify the exact 15M/4H alignment, feature snapshot availability, quantile population, and event mask used by that run.
3. Reproduce the accepted 20 counts from that source without modifying definitions to force agreement.
4. If the exact source cannot be recovered, rebuild the event engine from the accepted written specification as a new, explicitly versioned implementation and report any differences transparently; do not claim reproduction of the historical run.
5. Keep matched-control construction, outcome calculations, and all inference on hold until the event-count gate is resolved.

## Research integrity

No matched controls, outcome calculations, or profitability analysis were performed by this diagnostic. This checkpoint records a discrepancy, not a strategy result.
