# Sideways Market Identification — Methodology V1

Date recorded: 2026-11-22  
Project: Price Action V1  
Branch: `price-action-v1`

## Objective

Develop and compare transparent definitions of sideways/range-bound market conditions for BTC, ETH, SOL, DOGE, and AVAX. The first classification timeframe is 4H. The subsequent study measures 15M behaviour only after a 4H state is confirmed.

This is research methodology, not a trading strategy or profitability test. No strategy testing is authorized by this document.

## Why three measurements

A low-volatility window is not necessarily sideways: price may drift persistently in one direction. Conversely, a volatile window may travel up and down while making little net progress. Use separate measures of total range, directional progress, and overlap.

### 1. Rolling channel width

Use the highest high and lowest low over the latest 12 completed 4H candles (48 hours):

`ChannelWidthPct = (RollingHigh / RollingLow - 1) * 100`

A smaller width indicates a more compact 48-hour price envelope. It does not independently establish sideways behaviour.

### 2. Directional efficiency

Use the latest 12 close-to-close changes:

`DE = abs(last_close - close_12_bars_ago) / sum(abs(each_of_12_close_changes))`

DE is between 0 and 1 (subject to numerical precision). Values near zero indicate little net progress relative to the path travelled; values near one indicate mostly one-directional progress.

### 3. Adjacent-candle range overlap

For each adjacent pair of 4H candles, calculate:

`intersection = max(0, min(high_current, high_previous) - max(low_current, low_previous))`

`overlap_ratio = intersection / min(current_range, previous_range)`

Clip the ratio to [0, 1] and average the 11 adjacent-pair ratios in the 12-candle window. A higher value means more of the smaller candle's range is shared with its neighbour. Handle zero-width candles explicitly rather than dividing by zero.

This is one transparent overlap definition, not a universal standard. Alternative definitions can be compared later.

## Initial candidate grid

For exploratory classification, compare:
- Channel width at or below the asset-specific 25th, 40th, and 50th percentiles.
- Directional efficiency at or below 0.20, 0.30, and 0.40.
- Mean adjacent-candle overlap at or above 0.50, 0.60, and 0.70.

Do not assume a single combination is correct. Report candidate-state frequency, episode count, median/mean episode duration, and asset-by-asset differences. Also inspect the distribution of each feature before selecting thresholds.

Asset-specific channel-width percentiles help account for the different volatility scales observed in the five assets. They must not be mistaken for universal market thresholds.

## Causality and timing

- Build 4H candles from complete common minute observations only.
- Use only the latest 12 fully completed 4H candles for a state decision.
- A state becomes known only at the close of the final 4H candle in its window.
- Do not label earlier 15M candles inside that final 4H candle using a state that was not yet confirmed.
- Apply the confirmed state only to subsequent 15M candles.
- Do not use future pivots, future highs/lows, or future observations to classify the current window.
- When comparing candidate thresholds, full-sample quantiles are exploratory and retrospective. A live-ready rule must estimate thresholds using past/development data only and apply them forward.

## Next empirical steps

1. Calculate the 48-hour channel-width, directional-efficiency, and overlap distributions for each asset.
2. Inspect percentile tables and feature relationships.
3. Compare the candidate threshold grid and quantify how often each definition labels a window sideways.
4. Merge consecutive qualifying windows into episodes using a clearly stated rule; report episode duration and sensitivity to the rule.
5. Once the 4H definition is selected for further study, measure 15M range, body, close movement, boundary tests, excursions, and breakout/failed-breakout behaviour only after the 4H classification is confirmed.
6. Keep breakout and failed-breakout outcomes separate from the initial range classification.

## Interpretation limits

- These are descriptive market-state labels, not proof of a tradable edge.
- Overlapping 48-hour windows are highly dependent; consecutive labels are not independent observations.
- Thresholds can materially change state frequency and episode duration.
- Range width and overlap depend on OHLC construction and bar alignment.
- The five 1M CSVs' original exchange/API provenance and exact instrument identifiers remain incompletely verified. Existing project configuration specifies OKX USDT perpetual markets but does not prove the source of these files.
- Do not infer SL/TP settings or strategy profitability from sideways-state statistics alone.

## Research references

- Channel-breakout definitions using prior high-low channels: https://link.springer.com/article/10.1007/s11408-023-00433-2
- Discussion of range overlap as a trendless-market descriptor: https://nzdr.ru/data/media/biblio/kolxoz/F/FT/Kestner%20L.N.%20Quantitative%20trading%20strategies%20%28MGH%2C%202003%29%28ISBN%200071412395%29%28367s%29_FT_.pdf
- Directionality and volatility in high-frequency time series: https://onlinelibrary.wiley.com/doi/full/10.1002/hf2.10008
