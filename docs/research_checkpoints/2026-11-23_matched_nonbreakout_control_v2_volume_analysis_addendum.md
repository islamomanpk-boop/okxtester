# Matched Non-Breakout Control Study — V2 Volume Analysis Addendum

**Status:** Approved scope addition following user agreement.  
**Date:** 2026-11-23  
**Applies to:** `docs/research_checkpoints/2026-11-23_matched_nonbreakout_control_v2_implementation_spec.md`  
**Important:** This addendum supplements the V2 specification. It does not change the primary matching dimensions or the original breakout event definition.

## 1. Purpose

Measure whether breakout and non-breakout control observations differ in trading activity, and whether breakout outcomes vary descriptively with relative volume.

Volume is an additional analysis dimension. It is not added to the primary matching distance in V2. This avoids forcing breakout and control observations to have similar volume and potentially concealing a volume/outcome relationship.

## 2. Volume measurements

For every eligible breakout and control candidate, calculate the following using only completed 15-minute candles available at that candidate's signal close:

1. **Current signal-candle volume:** volume of the candidate's completed 15-minute candle.
2. **Previous 1-hour average 15-minute volume:** arithmetic mean of volume over the four completed 15-minute candles immediately before the signal candle.
3. **Previous 1-hour total volume:** sum of volume over those same four completed 15-minute candles.
4. **Relative volume (RVOL):** current signal-candle volume divided by the arithmetic mean volume of the 16 completed 15-minute candles immediately before the signal candle. This compares the signal candle with the preceding four hours' average 15-minute volume.
5. **Previous 24-hour maximum 15-minute volume:** maximum volume among the 96 completed 15-minute candles immediately before the signal candle.

The current signal candle is excluded from all prior-period baselines and the prior-24-hour maximum.

Use the volume field and units present in the validated source data. Do not silently convert units or mix quote-volume and base-volume fields. Inspect and document the source schema before implementation. If the volume field's meaning cannot be established, stop and report the ambiguity rather than guessing.

If any required lookback is incomplete, contains a gap, or has missing/non-finite volume, mark the relevant measurement unavailable and report the count. Do not fill missing values or bridge gaps. If the prior-16-bar mean is zero or unusable, RVOL is unavailable; do not divide by zero.

## 3. Analysis and reporting

Report the five volume measurements separately for breakout and control candidates:
- Sample counts and unavailable counts.
- Mean, median, P75, P90, and maximum where meaningful.
- Breakout-versus-control descriptive differences within exact strata and overall, with sample sizes clearly shown.
- RVOL distributions and proportions in transparent bins: below 0.5, 0.5 to below 1.0, 1.0 to below 1.5, 1.5 to below 2.0, and 2.0 or higher.
- For breakout observations, report forward outcomes by RVOL bin, with counts for every horizon. Do not imply that bins with small samples are reliable.
- Report the corresponding control RVOL distributions and outcomes as descriptive context.

Volume analysis is secondary and descriptive. It does not change eligibility, matching, pair selection, the 2.0 matching-distance threshold, or the primary matched outcome sample. Do not claim volume causes better or worse breakout outcomes.

## 4. Timing and look-ahead safeguards

- Signal-candle volume is available only after that 15-minute candle has completed; the study's signal timestamp is the candle's closing label.
- All prior-period calculations use candles strictly before the signal candle.
- No volume from the follow-up period may enter candidate features or volume baselines.
- Keep volume measurements out of the primary six-dimensional matching distance.
- Preserve all primary study results and report volume findings as a separate section.

## 5. Implementation and preservation

Implement these calculations only in the new V2 script. Do not edit the recovered original breakout script or matched-control V1. Do not overwrite prior checkpoints or failed experiments. Validate volume timestamps, lookback counts, gaps, field units, and zero-denominator handling before accepting volume results.
