# Breakout Previous-Selected Gate Diagnostic V5

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** Methodology checkpoint; runtime pending; event gate remains on HOLD.

## Why V5 is needed

The archived breakout/retest source `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh` explicitly computes:

```python
previous_selected = selected.shift(1).fillna(False).astype(bool)
valid_cross = selected & previous_selected & same_snapshot
```

V3 and V4 used the current selected state and same-snapshot condition but did not require the previous 15-minute row to be selected. That is a concrete event-eligibility difference.

Earlier diagnostics compared archived/current mask variants using the archived ER11 formula, but did not establish whether the previous-selected gate reconciles counts when paired with the exact historical ER12 absolute-price formula. V5 isolates that remaining combination.

## Controlled comparison

Script: `research/validation/breakout_event_previous_selected_gate_diagnostic_v5.py`

Fixed across variants:
- Common continuous 1-minute intersection: expected 569,125 timestamps.
- Epoch-aligned 4H and 15M resampling, left-labelled/left-closed; retain only complete 240-minute and 15-minute bars.
- Exact historical ER12 formula: `abs(close - close.shift(12)) / close.diff().abs().rolling(12).sum()`.
- 12-bar channel and 11 adjacent overlap pairs, available-valid-pair mean.
- Feature snapshot available at 4H bar-start plus four hours.
- Backward as-of mapping to 15M bar-start labels.
- Efficiency limit 0.30, overlap floor 0.70, same-snapshot requirement.
- Frozen upper/lower boundary crossing conditions.
- No previous-sideways condition in the current-only variant; no other event rules changed.

Varied dimensions:
1. Quantile population: unique 4H feature rows vs joined 15M rows.
2. Event gate:
   - `CURRENT_SELECTED_ONLY`: current selected state and same snapshot.
   - `ARCHIVED_PREVIOUS_SELECTED`: current selected state, immediately previous 15M row selected, and same snapshot.

All four combinations are compared against the 20 historically reported reference counts. No tuning is performed.

## Interpretation rules

- If the archived previous-selected gate materially changes counts, that establishes the gate as an important source of event-set differences, but not automatically the historical accepted producer or a 20/20 reproduction.
- Only an exact 20/20 match, together with confirmation of all other producer details and contemporaneous provenance, could support reopening the event gate.
- If no combination matches, retain HOLD and continue auditing timestamp availability/alignment, source script provenance, quantile filtering, and event mask semantics.
- Do not choose a variant based on closeness to the expected counts.

## Safety and scope

Read-only diagnostic. It writes no files and calculates no controls, forward outcomes, matching, inference, trades, or profitability. The expected counts are comparison targets, not a calibration objective.
