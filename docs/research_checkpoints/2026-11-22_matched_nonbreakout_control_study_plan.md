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
- Preserve STRICT_P25 and BROAD_P40 channel-width cutoffs from the prior study for comparability. Clearly label full-sample quantiles as retrospective exploratory thresholds.
- Preserve frozen upper/lower channel boundaries and the timing correction: 15M close label maps to the final 1M candle at close label minus one minute; follow-up starts at the next 1M candle open.
- Use the same event de-clustering and first-15M-after-context-refresh suppression as the final timing-corrected breakout study.

## Control definition

For each breakout event, construct a candidate control from a 15M candle that:
1. Is in the same asset, same strict/broad definition, and same upper/lower direction.
2. Has the same valid sideways-context conditions and a frozen channel snapshot.
3. Closes inside the channel (not a breakout) but approaches the corresponding boundary, using the same 10% inner boundary zone as the breakout study's retest-band concept.
4. Has complete follow-up data for the relevant horizons.
5. Is not the breakout event itself or part of its de-clustered breakout episode.

Match controls using only information available at the control timestamp. Prioritize:
- Same asset, boundary direction and sideways definition (exact strata).
- Similar normalized distance of the 15M close to the relevant boundary.
- Similar 15M candle range percentile (within that asset/context).
- Similar 4H channel width and directional efficiency.
- Similar recent 1H realized movement/volatility.
- Prefer nearby calendar time where possible, while avoiding controls from the same event episode.

Use nearest-neighbour matching with a predeclared maximum standardized distance and report unmatched breakout events. Use one control per event where possible; controls should not be reused in the primary matched sample. If matching without replacement leaves too few controls, report that limitation rather than silently relaxing the criteria. A secondary sensitivity analysis may allow up to three controls per event and must be labelled separately.

## Important future-outcome rule

Do **not** exclude a control because it later breaks out during its follow-up window. That would select controls using future information. Instead, retain the control and separately report how often controls themselves experience a same-direction breakout during each follow-up horizon. This makes the comparison interpretable as outcomes conditional on the starting observation, not as a comparison against paths guaranteed never to break out.

## Outcomes

From the next eligible 1M open, calculate identically for breakout and matched-control observations:
- 15M, 1H, 4H and 12H directional MFE and adverse excursion.
- Median, mean, P75 and P90 MFE/MAE.
- Net directional close-to-close movement at each horizon.
- Frequency of reaching 0.25%, 0.50%, 1.00%, 1.50% and 2.00% favourable movement.
- Time to first favourable threshold.
- For breakout events: return-inside and ending-inside frequencies, retained for continuity with prior study.
- For controls: same-direction breakout incidence during each follow-up horizon.
- Complete sample counts, unmatched counts, and incomplete-horizon exclusions.

Report paired event-level differences (breakout minus its matched control) and bootstrap confidence intervals using time-block or event-cluster resampling rather than treating every overlapping observation as independent. Also show raw distributions and medians; do not rely only on p-values.

## Safeguards

- Use only data available at each event/control start for matching.
- Do not match on future MFE, MAE, return, channel re-entry, or later breakout status.
- Keep horizons and calculations identical for matched pairs.
- Report overlap/dependence and matching quality, including standardized differences before/after matching.
- Do not infer a trading edge or profitability from excursions or target-touch frequencies.
- No entries, stops, targets, fees, slippage, funding, fills, or strategy simulation are part of this study.
- No local files are written or modified by the planned calculation.

## Interpretation

If breakout observations show larger directional movement than matched controls, that is evidence of a conditional association in this sample, not proof of a causal breakout effect or an executable trading edge. If differences are small or inconsistent across assets, the descriptive evidence does not support treating a channel break as unusually informative by itself.
