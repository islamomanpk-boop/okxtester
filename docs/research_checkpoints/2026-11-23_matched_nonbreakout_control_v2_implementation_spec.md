# Matched Non-Breakout Control Study — V2 Implementation Specification

**Status:** Proposed implementation specification; not yet executed.  
**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Purpose:** Freeze the V2 implementation choices before writing or running the matched-control calculation.

## 1. Research question and interpretation

Within the same 48-hour sideways-channel context, compare confirmed upper/lower 15-minute channel breakouts with comparable 15-minute observations approaching the same channel boundary without closing outside it.

This is a conditional, descriptive, matched comparison. It is not a causal estimate, a profitability test, or a trading-strategy simulation.

## 2. Immutable source and reproduction gate

- Use the recovered original source as the event-definition reference:
  `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`.
- Do not edit or overwrite that file.
- Preserve matched-control V1 unchanged:
  `research/matched_controls/matched_control_event_gate_v1.py`.
- V2 must independently reproduce all 20 historical event counts and the P25/P40 thresholds from the recovered original source before any controls or matched outcomes are accepted.
- If any threshold or event count differs, stop. Do not proceed to matching or outcomes.
- Use the same five assets, common 1-minute intersection, complete 15-minute/4-hour candles, resampling labels, shifted 12-bar channel, efficiency, overlap, quantile population, sideways gates, snapshot logic, and signal timing as the recovered original.
- Preserve the original event rules: no previous-sideways gate, no previous-selected gate, and no cooldown/de-clustering.
- 15-minute signal close label maps to the final 1-minute candle at signal label minus one minute. Follow-up begins at the next 1-minute candle open.

## 3. Candidate strata and control eligibility

Exact matching strata are:
1. Asset.
2. Channel-width definition: strict P25 or broad P40.
3. Direction: upper or lower.

A control candidate must:
- Be in the same valid sideways state and frozen channel snapshot as defined by the original event engine.
- Not be the first 15-minute candle after a new 4-hour snapshot (`same_snapshot` must be true).
- Close inside the frozen channel and within 0.10% of the relevant boundary:
  - Upper: `upper * (1 - 0.10/100) <= close <= upper`.
  - Lower: `lower <= close <= lower * (1 + 0.10/100)`.
- Have a valid next-1-minute-open follow-up start.
- Have complete, uninterrupted 1-minute follow-up data for all four horizons (15m, 1h, 4h, 12h).
- Not share the exact signal timestamp of a breakout event in the same stratum.

Do not exclude a control because it later breaks out. Report its same-direction breakout incidence separately by horizon. Do not bridge missing 1-minute intervals.

The breakout event reproduction gate is evaluated on the full original event set before complete-follow-up exclusions. The matched primary sample then includes only breakout events and controls with complete uninterrupted follow-up for all four horizons. Report all exclusions and counts explicitly.

## 4. Pre-start matching covariates

Calculate all covariates using only information available by the candidate signal close; no future values may enter matching.

1. **Signed normalized boundary distance (percent):**
   - Upper: `(upper - close) / upper * 100`.
   - Lower: `(close - lower) / lower * 100`.
   - Positive values are inside the channel; negative values are beyond the boundary.
2. **15-minute range percentile:** percentile rank of the candidate's 15-minute high-low range among valid eligible sideways 15-minute observations for the same asset and same strict/broad definition. Use the same eligible sideways population for breakout and control candidates.
3. **Frozen 4-hour channel width:** the original channel-width percentage from the candidate's frozen snapshot.
4. **Frozen 4-hour directional efficiency:** the original efficiency value from that same frozen snapshot.
5. **Recent 1-hour realized absolute movement (percent):** sum of absolute close-to-close percentage returns over the 60 completed 1-minute intervals ending at the final 1-minute candle before the candidate's 15-minute signal label. No return may use a candle after the signal close.

A candidate with a missing or non-finite required covariate is ineligible for matching and must be counted and reported, not silently imputed.

## 5. Standardization and distance — explicit V2 convention

The study plan requires standardized distances and a maximum overall distance of 2.0 but does not specify the aggregation formula. V2 will use this explicit convention:

- Standardize each of the five covariates separately within each exact stratum.
- The reference population for each stratum is the pooled set of otherwise eligible breakout and control candidates in the primary complete-follow-up sample, before matching.
- For each covariate, calculate the pooled arithmetic mean and population standard deviation (`ddof=0`) across that pooled candidate population.
- Convert each candidate value to a z-score using those fixed stratum-specific parameters.
- If a required covariate has zero or numerically unusable standard deviation in a stratum, mark that covariate unusable and stop matching in that stratum. Do not silently drop it, substitute a scale, or match on fewer dimensions.
- For a breakout-control pair, calculate the Euclidean distance across the five standardized covariate differences:
  `distance = sqrt(sum((z_breakout - z_control)^2))`.
- Accept a pair only when the overall distance is <= 2.0.
- No hidden feature weights, no feature omission, no scale recalculation after matching, and no threshold relaxation.

### Calendar proximity component

Calendar proximity is included transparently as a **separate sixth standardized distance component**, not buried in a feature or hidden weight:

- Within each exact stratum, express candidate signal timestamps as elapsed days from that stratum's earliest candidate timestamp.
- Standardize this elapsed-day value using the pooled candidate population's arithmetic mean and population standard deviation (`ddof=0`), using the same pooled primary-sample candidates as above.
- Include the standardized calendar-time difference as the sixth dimension in the Euclidean overall distance.
- Therefore the final distance is `sqrt(sum((z_breakout - z_control)^2) + (ztime_breakout - ztime_control)^2)`, with a maximum of 2.0.
- If the calendar-time scale is zero or numerically unusable, matching in that stratum stops.
- Report calendar-time pair differences in hours and days, their distribution, and their standardized contribution separately from the five market-feature contributions.

This gives all six standardized dimensions equal, explicit weight. The 2.0 limit applies to the six-dimensional Euclidean distance. This is a proposed operational interpretation of the plan's calendar-proximity requirement; it must be clearly identified in all reports.

## 6. Matching algorithm

- Perform matching independently within each exact stratum.
- Generate all eligible breakout-control pair distances.
- Sort all candidate pairs in ascending distance, with deterministic timestamp tie-breaks.
- Greedily accept the smallest available pair if neither event nor control has already been used.
- Match one-to-one without replacement.
- Reject pairs with distance > 2.0.
- This is greedy matching, not a globally optimal assignment.
- Do not reuse controls, relax the distance limit, or backfill with a different stratum.
- Report total breakout candidates, eligible controls, matched pairs, unmatched breakouts, unused controls, and reasons for exclusions per stratum.

## 7. Balance and audit outputs

Before and after matching, report for every covariate and calendar-time component:
- Candidate counts.
- Mean, standard deviation, median, and relevant quantiles by breakout/control group.
- Standardized mean difference (SMD).
- Pairwise absolute standardized differences and overall distance distribution after matching.

Also report:
- The full matching scale parameters for every stratum and dimension.
- Missing/non-finite and unusable-scale diagnostics.
- Calendar separation in hours and days.
- Deterministic tie-break behavior.
- A row-level matched-pair audit table in the report output.

Do not describe balance as adequate merely because matching completed. Show the values.

## 8. Forward outcomes

Start both breakout and control follow-up from the same timing convention: next eligible 1-minute candle open. Use the same calculation for both groups.

For 15m, 1h, 4h, and 12h, report:
- Directional maximum favourable excursion (MFE).
- Directional maximum adverse excursion (MAE), reported as a non-positive value.
- Mean, median, P75, and P90 for MFE and MAE.
- Net directional close-to-close movement at the horizon.
- Frequency reaching 0.25%, 0.50%, 1.00%, 1.50%, and 2.00% favourable movement.
- Time to each favourable threshold among those that reach it.
- Sample count for each metric/horizon.

Additionally:
- For breakout events, report return-inside-channel and ending-inside-channel frequencies.
- For controls, report same-direction breakout incidence by each horizon.
- Report paired breakout-minus-control differences for each outcome.
- Use time-block or event-cluster bootstrap intervals to respect temporal clustering; do not treat all events as independent. Label intervals approximate and document the resampling unit and settings.

No entries, stops, targets, fees, slippage, funding, fills, or strategy simulation.

## 9. Data handling and output safety

- Read-only with respect to source market data.
- Do not modify source data or the recovered original script.
- Preserve V1 and all prior failed diagnostics.
- New implementation must use a new filename, e.g. `research/matched_controls/matched_control_study_v2.py`.
- The calculation should not write or overwrite local result files. Initial run should print auditable summaries to stdout; any later report artifact must be deliberately created under a new, unique filename.
- Preserve failed runs and logs rather than overwriting them.
- Do not commit results until the event gate, matching audit, and output checks pass.

## 10. Interpretation limits

A successful run would establish only that the specified descriptive comparison was computed from the specified historical dataset and event rules. It would not establish causation, tradability, profitability, or live performance.

## 11. Pre-run review checkpoint

This document freezes the proposed distance convention, including equal-weight six-dimensional Euclidean distance and the 2.0 maximum. Before coding/running V2, review this convention against the study objective. If the convention is changed, revise this specification in a new version or clearly recorded amendment before calculation; do not silently alter it in code.
