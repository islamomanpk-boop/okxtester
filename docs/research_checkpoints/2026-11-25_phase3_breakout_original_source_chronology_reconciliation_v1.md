# Phase 3 Original Breakout Source Chronology Reconciliation V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Branch:** `price-action-v1`  
**Status:** Historical event-count source reproduction PASS; causal event-availability gate remains OPEN.

## Purpose

Resolve an apparent conflict between the 2026-11-23 breakout event-reproduction HOLD / V4 / V5 diagnostics and the separately recovered original timing-corrected Python source.

## Verified chronology

| Evidence | UTC timestamp | Finding |
|---|---:|---|
| `2026-11-23_breakout_event_reproduction_conflict_hold.md` | 2026-11-23 13:43:55 | HOLD recorded before the original Python source was archived |
| V4 quantile-population runtime diagnostic | 2026-11-23 15:20:39 | Tested the separate archived shell-script implementation |
| V5 previous-selected-gate runtime diagnostic | 2026-11-23 15:25:56 | Also tested the separate archived shell-script implementation |
| Original Python source archive commit `dd55b604bd248b6e4e75dbcc5bd400a6c2eab2c3` | 2026-11-23 16:17:32 | Archived `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py` |
| Original-source runtime PASS commit `daad3e016b4f6cf4d30974751c85aa8ab2c371ff` | 2026-11-23 16:32:35 | Recorded unchanged execution and exact 20/20 event-count reproduction |

## Source identity and reproduction

The recovered Python source is a distinct artifact from `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh`.

The Python source:
- calculates full-sample P25/P40 from the joined 15M channel-width observations;
- uses the same-snapshot breakout mask without a previous-selected gate;
- uses complete right-labelled 15M/4H bars and the prior 12 completed 4H context;
- preserves the corrected signal-minute and first-follow-up-minute timing.

The archived runtime PASS checkpoint states that this exact Python file was recovered from the original conversation, committed and read back from GitHub, then run unchanged by the user. It records **20/20 exact matches** to the accepted five-asset × two-definition × two-direction event-count table.

The separate shell script uses a different construction, including unique-4H quantiles and a previous-selected gate. The V4/V5 zero-match findings apply to that separate shell-script implementation and do not invalidate the later recovered Python-source reproduction.

## Disposition

1. The historical event-count reproduction requirement is **PASS for the recovered original Python source and recorded runtime**.
2. The earlier 2026-11-23 HOLD and V4/V5 diagnostics remain valid historical records of the earlier source-recovery state and the separate shell-script tests. They are superseded only for the narrow question of whether the original 20 historical event counts were reproduced by the recovered Python source.
3. This does **not** make the historical full-sample P25/P40 thresholds causal. They remain retrospective descriptive thresholds.
4. This does **not** close G0-04/G0-05. The full eligible 15M observation universe still requires a source-specific past-only threshold reconstruction; causal signal availability, three-family candidate contract, source provenance, and execution readiness remain open.
5. No candidates, matched controls, forward outcomes, inference, PnL, or strategy backtests are authorized by this reconciliation.

**Evidence files:**  
- `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`  
- `docs/research_checkpoints/2026-11-23_recovered_original_breakout_event_reproduction_runtime_pass.md`  
- `docs/research_checkpoints/2026-11-23_breakout_event_reproduction_conflict_hold.md`  
- `docs/research_checkpoints/2026-11-23_archived_breakout_script_v5_source_reconciliation.md`
