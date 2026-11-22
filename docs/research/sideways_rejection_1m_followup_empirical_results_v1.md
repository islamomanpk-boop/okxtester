# Sideways Boundary Rejection: 1M Follow-up Study v1

**Status:** Completed descriptive research; read-only local calculation.  
**Dataset:** Five-asset common 1-minute intersection, 569,125 candles.  
**Assets:** BTC, ETH, SOL, DOGE, AVAX.  
**Research branch:** `price-action-v1`.

## Purpose

Measure what happens after a strong 15-minute rejection at the upper or lower boundary of an exploratory 48-hour sideways channel. Follow-up is measured with subsequent 1-minute highs and lows. Compare rejection events with non-touch control candles sampled by 15-minute candle-range quartile.

This is a price-path study, not a strategy backtest.

## Method

- 4H bars are used to classify sideways conditions with a 48H (12-bar) channel.
- Candidate definitions: STRICT_P25 and BROAD_P40, using asset-specific full-sample channel-width quantiles, directional efficiency <= 0.30 and average overlap >= 0.70.
- 4H state is applied only after the 4H bar closes.
- A strong upper rejection touches the outer 10% upper channel zone and closes back below the inner edge while remaining inside the channel. Lower rejection is symmetric.
- Rejection episodes count only their first strong rejection.
- Signal is confirmed at the completed 15M close. Follow-up starts at the next 1M candle open and uses subsequent 1M highs/lows.
- Horizons: 1H (60 1M bars), 4H (240), 12H (720).
- Favourable/adverse excursions are measured from the first post-signal 1M open, in the direction of the rejection.
- Target-hit rates are the fraction whose favourable excursion reaches 0.25%, 0.50%, or 1.00%; median hit time is calculated among hits.
- Controls are non-touch 15M bars sampled up to three per rejection event and matched by candle-range quartile.
- No local files were written or changed.

## Event counts

Strong rejection event counts (upper / lower):

| Asset | Strict upper | Strict lower | Broad upper | Broad lower |
|---|---:|---:|---:|---:|
| BTC | 105 | 90 | 135 | 134 |
| ETH | 97 | 91 | 133 | 126 |
| SOL | 139 | 129 | 177 | 177 |
| DOGE | 121 | 90 | 147 | 132 |
| AVAX | 131 | 127 | 192 | 158 |

Controls were sampled at up to three per event. Some control counts at 12H are lower than the initial count because full follow-up coverage was not available for every control.

## Broad P40: 1H comparison

Percentage of events reaching a favourable excursion target:

| Asset | Direction | Rejection >=0.25% | Control >=0.25% | Rejection >=0.50% | Control >=0.50% | Rejection >=1.00% | Control >=1.00% |
|---|---|---:|---:|---:|---:|---:|---:|
| BTC | Upper | 45.9 | 42.0 | 24.4 | 18.8 | 6.7 | 5.9 |
| BTC | Lower | 41.8 | 46.5 | 22.4 | 19.7 | 6.0 | 4.7 |
| ETH | Upper | 52.6 | 51.6 | 30.1 | 24.8 | 12.8 | 7.5 |
| ETH | Lower | 59.5 | 52.1 | 27.0 | 25.9 | 7.1 | 7.1 |
| SOL | Upper | 56.5 | 55.9 | 28.8 | 32.2 | 10.7 | 9.6 |
| SOL | Lower | 55.9 | 56.3 | 19.8 | 31.3 | 5.6 | 11.3 |
| DOGE | Upper | 60.5 | 59.0 | 35.4 | 32.4 | 10.9 | 11.3 |
| DOGE | Lower | 59.1 | 58.1 | 31.1 | 33.6 | 6.8 | 8.3 |
| AVAX | Upper | 59.9 | 61.8 | 36.5 | 37.5 | 12.5 | 13.4 |
| AVAX | Lower | 62.7 | 58.9 | 33.5 | 31.6 | 8.9 | 11.4 |

The broad 1H comparison is mixed. ETH upper rejection and BTC upper rejection have higher 0.50% target-hit rates than their controls. Several SOL and AVAX groups do not beat controls. Lower-side results are also mixed. No uniform five-asset rejection advantage is demonstrated.

## Broad P40: 12H favourable/adverse excursion medians

Values are percentages from the first post-signal 1M open.

| Asset | Direction | Rejection favourable | Control favourable | Rejection adverse | Control adverse |
|---|---|---:|---:|---:|---:|
| BTC | Upper | 0.741 | 0.780 | 0.819 | 0.759 |
| BTC | Lower | 0.647 | 0.758 | 1.177 | 0.785 |
| ETH | Upper | 1.367 | 1.015 | 1.155 | 0.927 |
| ETH | Lower | 0.772 | 1.067 | 1.390 | 1.083 |
| SOL | Upper | 1.133 | 1.299 | 1.010 | 1.023 |
| SOL | Lower | 0.888 | 1.023 | 1.450 | 1.300 |
| DOGE | Upper | 1.258 | 1.189 | 0.925 | 0.978 |
| DOGE | Lower | 1.246 | 1.096 | 1.282 | 1.227 |
| AVAX | Upper | 1.712 | 1.452 | 1.219 | 1.345 |
| AVAX | Lower | 1.571 | 1.337 | 1.464 | 1.481 |

Longer-horizon excursions can be large, but controls also move substantially. Some rejection groups have greater favourable excursion; others do not. Adverse excursion remains material, especially for lower-side rejection groups in several assets.

## Strict P25 cross-check: 1H target-hit rate at 0.50%

| Asset | Upper rejection | Upper control | Lower rejection | Lower control |
|---|---:|---:|---:|---:|
| BTC | 23.8 | 19.7 | 20.0 | 16.3 |
| ETH | 25.8 | 21.3 | 27.5 | 21.2 |
| SOL | 21.6 | 28.8 | 17.8 | 23.8 |
| DOGE | 26.4 | 26.2 | 31.1 | 30.0 |
| AVAX | 35.1 | 35.4 | 31.5 | 37.5 |

Strict P25 also produces mixed comparisons. DOGE rejection rates are close to controls; SOL and AVAX rejection rates are below controls in these selected groups.

## Findings and research decisions

1. A strong 15M boundary rejection is not, by itself, a consistently superior signal versus sampled non-touch controls.
2. Differences vary by asset, direction, horizon and strict/broad regime definition. Avoid a universal rule.
3. Longer 4H/12H favourable excursions are not proof of tradable returns. Adverse excursions can be large and may occur before favourable movement.
4. The broad and strict definitions give broadly mixed results, so no classifier or entry rule is selected from this study.
5. Continue with breakout continuation/retest behaviour and the broader post-signal path study. Later compare execution timeframes using identical confirmed 15M signals.

## Limitations

- Channel-width quantiles use the full sample and are retrospective exploratory labels, not causal live thresholds.
- Controls are matched by candle-range quartile, not exact time, volatility state, channel snapshot or calendar regime. They are not a fully matched causal control group.
- Follow-up windows can overlap; observations are not independent.
- Control samples can be fewer than three per rejection event when full horizon coverage is unavailable.
- MFE/MAE are path extrema from the next 1M open; they do not model fills, spread, fees, slippage, funding, liquidity, order queue, stop/target ordering, or executable position sizing.
- A target hit does not imply the target could be captured before an adverse stop; no stop/target collision model is included.
- Median favourable/adverse excursions do not represent net trade expectancy.
- Candle data provenance and volume units remain independently unverified.
- Results are descriptive and must not be interpreted as a profitable strategy or forecast.

## Exact study end notes

- Signal confirmed at completed 15M candle close.
- Follow-up begins at next 1M candle open.
- Follow-up uses subsequent 1M highs and lows.
- Rejection episodes count only their first strong rejection.
- Controls sampled from non-touch bars matched by candle-range quartile.
- Overlapping follow-up windows may occur.
- No fees, fills or profitability modelled.
- Read-only calculation; no files written or changed locally.
