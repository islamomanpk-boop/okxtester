# Matched non-breakout controls for sideways-channel breakout research

**Project:** Price Action V1  
**Branch:** `price-action-v1`  
**Status:** agreed research design; read-only calculations only. No strategy backtest or local data modification.

## Research question

Within the same 48-hour sideways context, do confirmed upper/lower 15M channel breakouts show different subsequent price paths from comparable 15M observations that approach the same boundary but do not break out?

This is a conditional descriptive comparison, not a causal estimate and not a profitability test.

## Universe and inherited definitions

- Assets: BTC, ETH, SOL, DOGE, AVAX.
- Use the same common 1M timestamp intersection and complete 15M/4H candles.
- Preserve the previous 48H context: prior 12 completed 4H candles; DE <= 0.30; adjacent 4H overlap >= 0.70.
- Preserve STRICT_P25 and BROAD_P40 channel-width cutoffs from the prior study for comparability. Clearly label full-sample quantiles as retrospective exploratory thresholds. Recompute the quantiles using the same full-sample procedure as the accepted breakout study rather than substituting rounded display values.
- Preserve frozen upper/lower channel boundaries and the accepted timing correction: 15M close label maps to the final 1M candle at close label minus one minute; follow-up starts at the next 1M candle open.
- Preserve the exact accepted final breakout event masks:
  - `same_snapshot = snapshot.eq(snapshot.shift(1))`
  - Upper breakout: `sideways & same_snapshot & (previous_close <= upper) & (current_close > upper)`
  - Lower breakout: `sideways & same_snapshot & (previous_close >= lower) & (current_close < lower)`
- **Do not add a `previous_sideways` requirement.** That appeared in an earlier construction, not in the accepted final timing-corrected script.
- **Do not add event de-clustering or a cooldown.** The accepted final script counted each qualifying crossing and allowed overlapping follow-up windows. The previous plan's instruction to inherit de-clustering was incorrect and is superseded here.
- Suppress the first 15M candle after a new 4H context snapshot through the `same_snapshot` condition.
- The 1M follow-up must be exactly continuous. Reject an event/control horizon if any expected minute timestamp is missing; do not bridge gaps by taking the next available timestamp.

## Control definition

For each breakout event, construct a candidate control from a 15M candle that:

1. Is in the same asset, same strict/broad definition, and same upper/lower direction.
2. Has the same valid sideways-context conditions and a frozen channel snapshot; also require the observation not to be the first 15M candle after a new context snapshot.
3. Closes inside the channel (not a breakout) but is within the corresponding inner boundary band. Interpret the inherited 0.10 value as **0.10% of boundary price**, matching the original retest band calculation: upper close is at least `upper * (1 - 0.10/100)` and no greater than upper; lower close is no less than lower and at most `lower * (1 + 0.10/100)`.
4. Has a valid next-1M-open start and complete, exactly continuous 15M/1H/4H/12H follow-up data for the primary all-horizons sample.
5. Is not the same timestamp as a breakout signal in the same stratum.

A control may later break out during its follow-up. Do not exclude it based on future information.

## Matching

Exact strata: asset, strict/broad definition, and boundary direction.

Use only pre-start covariates:
- normalized close distance to the relevant boundary;
- 15M candle range percentile within the asset's eligible sideways observations;
- frozen 4H channel width;
- frozen 4H directional efficiency;
- recent 1H realized movement/volatility, calculated only from minutes ending no later than the control/breakout signal close.

Use transparent standardized distances. Standardization parameters must be derived from the eligible pre-event feature distributions within each exact stratum, with zero/near-zero scales handled explicitly. Include calendar proximity as a separately reported matching component, not an unexamined hidden weight. Predeclare a maximum overall standardized distance of 2.0. Use greedy global smallest-distance one-to-one matching without replacement within each stratum; label it accurately as greedy matching, not globally optimal assignment. Report unmatched breakout events. Do not relax the distance limit or reuse controls in the primary analysis to inflate pair counts.

Report covariate balance before and after matching using standardized mean differences for every feature, plus distributions and pair distances. If a feature has unusable variance or missingness, report it and do not silently omit it.

## Future-outcome rule

Do **not** exclude a control because it later breaks out during its follow-up window. Instead, separately report the incidence of a same-direction breakout during each follow-up horizon. Matching must never use future MFE, MAE, return, re-entry, or later breakout status.

## Outcomes

From the next eligible 1M open, calculate identically for breakout and matched-control observations:
- 15M, 1H, 4H and 12H directional MFE and non-positive adverse excursion (MAE).
- Median, mean, P75 and P90 MFE/MAE.
- Net directional close-to-close movement at each horizon.
- Frequency of reaching 0.25%, 0.50%, 1.00%, 1.50% and 2.00% favourable movement, plus time to first favourable threshold.
- For breakout events: return-inside and ending-inside frequencies, retained for continuity with prior study.
- For controls: same-direction breakout incidence during each follow-up horizon.
- Complete sample counts, unmatched counts, and incomplete-horizon exclusions.
- Paired event-level differences (breakout minus matched control). Any bootstrap must resample time blocks or event clusters, not treat overlapping observations as independent; label intervals approximate.

## Safeguards

- Validate all 20 accepted breakout event counts before matching. If any count differs, stop and print a validation failure; do not calculate matched results.
- Use only information available at each event/control start for matching.
- Keep horizons and calculations identical for matched pairs.
- Report overlap/dependence and matching quality, including standardized differences before/after matching.
- No entries, stops, targets, fees, slippage, funding, fills, or strategy simulation are part of this study.
- No local files are written or modified by the calculation.

## Interpretation

Any observed differences are conditional descriptive associations in this sample, not causal effects or executable trading edges. If differences are small or inconsistent across assets, the descriptive evidence does not support treating a channel break as unusually informative by itself.
