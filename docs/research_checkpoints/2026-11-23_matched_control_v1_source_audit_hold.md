# Matched-control V1 source audit — do not use as validated event gate

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** HOLD — source audit found material divergence from the accepted original breakout script.  
**Scope:** Read-only source comparison of `research/matched_controls/matched_control_event_gate_v1.py`, the recovered accepted original breakout script, and the agreed matched-control study plan.

## Decision

Do not run V1 as the matched-control event gate and do not use its output to authorize matching. Preserve it unchanged as a historical diagnostic. A new implementation must be created under a new filename and must reproduce the accepted original event engine exactly before controls or outcomes are calculated.

## Files compared

- `research/matched_controls/matched_control_event_gate_v1.py`
- `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`
- `docs/research_checkpoints/2026-11-22_matched_nonbreakout_control_study_plan.md`

## Material differences found

1. **Resampling labels differ.** V1 calls `resample(..., label="left", closed="left")`; the accepted original calls `resample(..., label="right", closed="left")`. This changes the time labels used for higher-timeframe bars and their alignment.
2. **Channel construction differs.** V1 computes rolling 12-bar highs/lows without shifting them. The accepted original computes rolling 12-bar highs/lows and then applies `.shift(1)`. Therefore the frozen channel inputs are not the same.
3. **Directional-efficiency construction differs.** V1 uses an 11-period path sum and a close comparison shifted by 11, with no final one-bar shift of the resulting context. The accepted original uses the previous 12 completed 4H candles: net movement `close.shift(1) / close.shift(13) - 1`, and a 12-period absolute close-to-close path sum shifted by one.
4. **Adjacent-overlap construction differs.** V1 averages 11 overlap pairs without the accepted original's 12-pair rolling window and final `.shift(1)`. The accepted original uses `overlap_ratio(...).rolling(12).mean().shift(1)`.

These are not cosmetic differences. They alter the 4H context, frozen channel, sideways eligibility and potentially the event mask. V1 is therefore not an exact implementation of the validated original event engine.

## What remains valid

- The recovered original script's unchanged runtime reproduced all 20 accepted asset × definition × direction event counts on the current dataset; see `docs/research_checkpoints/2026-11-23_recovered_original_breakout_event_reproduction_runtime_pass.md`.
- The matched-control plan remains the agreed design.
- This audit does not invalidate the original runtime PASS. It identifies V1 as unsuitable for the next stage.

## Required next implementation

Create a new, separately named matched-control implementation. Preserve the original script's resampling labels, 4H context formulas, quantile population, as-of alignment, sideways conditions, `same_snapshot` rule, breakout masks, and timing correction exactly. First validate all 20 event counts against the accepted reference. Only after that gate passes may the implementation construct eligible controls, match within exact strata, report balance and calculate the predeclared forward outcomes.

The new implementation must also satisfy the complete control eligibility, covariate standardization, greedy one-to-one matching, distance cap, unmatched reporting, continuity checks, outcome definitions and safeguards in the agreed plan. Do not silently omit unusable features or relax the matching threshold.

## Preservation

V1 is intentionally not modified or deleted. No local data, original source, or research result was changed by this audit.
