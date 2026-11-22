# Recovery Note: Sideways Detector Research and Formula Provenance

Date: 2026-11-22
Branch: price-action-v1
Status: **Prior parameter decisions recovered; exact original web bibliography and exact original implementation not recovered. Formula reconstruction remains subject to explicit sign-off before code acceptance.**

## 1. Prior agreed study decisions recovered from conversation history

The user's earlier research decisions for the repeated 4H boundary study were:
- Build a 48-hour channel from 12 complete 4H candles.
- Apply the sideways classification only after the relevant 4H candle has closed.
- Use asset-specific full-sample channel-width percentiles: strict P25 and broad P40. These are retrospective/exploratory thresholds, not live-calibrated values.
- Require directional efficiency <= 0.30.
- Require average adjacent-candle range overlap >= 0.70.
- Freeze the resulting channel boundaries for the downstream 15M touch/rejection/breakout analysis.
- Primary boundary zone was 10% of channel width, after considering 5%, 10%, and 15% alternatives.
- Wick touch and close-back-inside rejection are distinct concepts.
- Repeated test separation was later fixed at 20% of channel width.

The existing EMA/ADX regime classifier is not the detector for this experiment.

## 2. Candidate mathematical reconstruction: directional efficiency

A standard, well-documented efficiency/trend ratio is:

ER_t = abs(C_t - C_(t-n)) / sum(i=0..n-1, abs(C_(t-i) - C_(t-i-1)))

For this study, the natural 48-hour implementation is n=12 on 4H closes, spanning 12 close-to-close changes across the 12-bar window. It is bounded [0,1]; low values indicate a path with substantial back-and-forth movement relative to net displacement. The study's threshold is <= 0.30.

This formula is supported by:
- Graham Capital Management / CME Group research note, "The Trendiness of Markets" (August 2017), which defines Trend Ratio as absolute endpoint price change divided by the sum of absolute intervening price changes: https://www.cmegroup.com/content/dam/cmegroup/education/files/trendiness-of-markets-august-2017.pdf
- Kaufman efficiency-ratio references, including the excerpt from "Smarter Trading": https://c.mql5.com/3/133/Kaufman.Perry-Smarter.Trading.Improving.Performance.In.Changing.Markets.pdf
- Technical explanation: https://www.marketvolume.com/technicalanalysis/efficiencyratio.asp

Important: the exact prior conversation's source citation and whether the calculation used 12 close-to-close increments or an alternative 12-bar indexing convention were not preserved. The above is a candidate reconstruction, not proof of the original code.

## 3. Candidate mathematical reconstruction: adjacent 4H range overlap

For each adjacent pair of 4H candles a,b, define:
- shared = max(0, min(high_a, high_b) - max(low_a, low_b))
- union = max(high_a, high_b) - min(low_a, low_b)
- overlap_ratio = shared / union, when union > 0

Then mean_overlap is the arithmetic mean of overlap_ratio over the 11 adjacent pairs inside a 12-candle window (subject to exact window indexing being frozen).

A directly inspectable implementation of this shared-range / union-range ratio appears in MQL5's 2026 "Price Action Analysis Toolkit Development (Part 58): Range Contraction Analysis and Maturity Classification Module", in OverlapRatioWindow(): https://www.mql5.com/en/articles/21109
The implementation calculates intersection as min(highs)-max(lows), union as max(highs)-min(lows), clips non-positive intersection to zero, divides intersection by union, and averages across adjacent pairs.

A separate OHLC research note describes shared range between consecutive bars and averaging overlap observations: https://tradersweek.com/research/articles/constructing-ohlc-range-overlap-and-bar-pattern-filters

Important: these sources support a defensible overlap measure, but do not prove that this was the exact formula selected in the user's earlier research. Other normalizations (e.g., overlap divided by the smaller candle range) exist and would materially change the scale. The 0.70 threshold must not be used with an alternative denominator without revalidation.

## 4. Channel width and percentile

The study's channel is the high-low envelope of the 12 complete 4H candles:
- upper = max(high over 12 candles)
- lower = min(low over 12 candles)
- width_pct = (upper - lower) / reference_price

The exact reference_price used to normalize width (e.g. latest close, midpoint, or another value) is not captured in the recovered protocol excerpt. Nor is it fully documented whether P25/P40 thresholds were calculated from all historical snapshots or a specific calibration sample, though the prior protocol labels them full-sample and retrospective. These details must be recovered from the user's original deep-research notes or explicitly specified before implementing percentiles.

## 5. What is and is not recovered

Recovered from prior conversation:
- 12 complete 4H bars / 48 hours.
- Strict P25 and broad P40 channel-width cohorts.
- Directional efficiency <= 0.30.
- Mean adjacent range overlap >= 0.70.
- Classify after 4H close.
- Freeze boundaries for downstream event analysis.
- 10% boundary touch zone and 20% separation rule.

Not recovered:
- Exact original external bibliography from the earlier deep-web session.
- Exact code-level definition and indexing for directional efficiency.
- Exact overlap normalization and treatment of zero-width/zero-union pairs.
- Exact width normalization reference and percentile calibration universe.
- Exact causal availability timestamp and whether rolling snapshots overlap every 4H bar or use another schedule.

## 6. Acceptance gate before coding

Do not silently claim that the candidate formulas are the original formulas. Before implementation is accepted:
1. Freeze the directional-efficiency formula and 12-bar indexing.
2. Freeze the overlap formula and denominator.
3. Freeze channel-width normalization and P25/P40 calibration universe.
4. Freeze rolling snapshot cadence and the availability timestamp.
5. Add hand-calculated unit tests for all metrics and boundary cases.
6. Run event-level audits and compare counts with the provisional 2,095 cohort events. A mismatch is an investigation, not a reason to tune definitions to force matching counts.

No trading edge or profitability claim follows from these definitions.
