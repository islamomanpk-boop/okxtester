# Sideways Feature Distributions — 48H Baseline V1

Date recorded: 2026-11-22  
Project: Price Action V1  
Branch: `price-action-v1`

## Purpose

Record empirical distributions for three candidate 48-hour (12 completed 4H candle) sideways-market features across BTC, ETH, SOL, DOGE, and AVAX. This is descriptive research only; no sideways threshold has been selected and no strategy has been tested.

## Data and method

- Read-only use of the existing five 1M CSVs in `~/okx_scalping_data`.
- Inner join across assets produced 569,125 common minute timestamps.
- Each asset was resampled into UTC epoch-aligned 4H OHLC candles.
- Only complete 4H candles with 240 common minute observations were retained.
- Each asset had 2,370 complete 4H candles and 2,358 valid rolling 48H feature windows.
- Channel width: (rolling 12-candle highest high / rolling 12-candle lowest low - 1) × 100.
- Directional efficiency: absolute difference between the last close and close 12 bars earlier, divided by the sum of the 12 absolute close-to-close changes.
- Adjacent candle overlap: intersection length of each adjacent pair's high-low intervals divided by the smaller of the two candle ranges, clipped to [0,1]; then averaged over 11 adjacent pairs in the 12-candle window. Zero smaller-range pairs were treated as missing.
- Quantiles reported at 10%, 25%, 40%, 50%, 60%, 75%, and 90%.

## Channel width percentiles (%)

| Asset | P10 | P25 | P40 | P50 | P60 | P75 | P90 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BTC | 2.412 | 3.242 | 3.948 | 4.423 | 4.980 | 6.086 | 8.266 |
| ETH | 3.185 | 4.245 | 5.475 | 6.219 | 7.133 | 8.998 | 11.753 |
| SOL | 3.647 | 5.067 | 6.115 | 6.856 | 7.872 | 9.842 | 13.129 |
| DOGE | 3.750 | 5.166 | 6.264 | 7.134 | 7.917 | 10.118 | 13.820 |
| AVAX | 4.494 | 5.705 | 6.916 | 7.758 | 8.601 | 10.511 | 14.443 |

## Directional efficiency percentiles

| Asset | P10 | P25 | P40 | P50 | P60 | P75 | P90 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BTC | 0.048 | 0.134 | 0.220 | 0.284 | 0.343 | 0.455 | 0.609 |
| ETH | 0.047 | 0.135 | 0.223 | 0.275 | 0.339 | 0.453 | 0.621 |
| SOL | 0.057 | 0.132 | 0.213 | 0.262 | 0.322 | 0.430 | 0.598 |
| DOGE | 0.050 | 0.131 | 0.208 | 0.257 | 0.318 | 0.420 | 0.584 |
| AVAX | 0.049 | 0.120 | 0.193 | 0.250 | 0.317 | 0.425 | 0.583 |

## Mean adjacent-candle overlap percentiles

| Asset | P10 | P25 | P40 | P50 | P60 | P75 | P90 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BTC | 0.681 | 0.728 | 0.757 | 0.776 | 0.794 | 0.823 | 0.862 |
| ETH | 0.694 | 0.736 | 0.766 | 0.786 | 0.803 | 0.832 | 0.868 |
| SOL | 0.669 | 0.720 | 0.752 | 0.769 | 0.786 | 0.819 | 0.859 |
| DOGE | 0.665 | 0.717 | 0.755 | 0.775 | 0.792 | 0.821 | 0.857 |
| AVAX | 0.663 | 0.711 | 0.744 | 0.762 | 0.781 | 0.809 | 0.850 |

## Preliminary observations

1. Channel width differs substantially by asset. Median 48H width ranges from 4.42% for BTC to 7.76% for AVAX. This supports testing asset-relative or volatility-normalized channel thresholds rather than applying one absolute percentage to every coin.
2. Directional-efficiency distributions are comparatively similar. Median values range from 0.250 to 0.284, and P75 values from 0.420 to 0.455. This supports investigating shared efficiency thresholds, but does not prove that one threshold is optimal.
3. Median adjacent-candle overlap is also relatively similar, ranging from 0.762 to 0.786.
4. These are marginal feature distributions. They do not show how often all three conditions occur together. Joint candidate-state frequencies must be calculated before assessing any classifier.
5. The 48H windows overlap heavily, so adjacent observations are dependent. Window counts must not be described as independent market episodes.

## Next research step

Calculate candidate joint sideways states using:
- Channel width at or below each asset's rolling-feature full-sample P25, P40, and P50 (exploratory retrospective comparisons only).
- Directional efficiency at or below 0.20, 0.30, and 0.40.
- Mean adjacent overlap at or above 0.50, 0.60, and 0.70.

Report candidate-state frequencies, then compare episode counts and durations under explicit consecutive-window rules. Do not select a final classifier solely because it labels a convenient percentage of history. Full-sample quantiles are retrospective; a live-capable classifier must estimate thresholds from past data only and apply them forward.

After a 4H state is confirmed at the close of its final 4H candle, measure subsequent 15M behaviour only. Do not back-label the 15M candles that occurred before the 4H state was knowable.

## Limitations

- No trading strategy, execution simulation, or profitability calculation was performed.
- OHLC overlap is a descriptive proxy and does not reveal intrabar order.
- Results depend on the exact overlap formula and 4H bar alignment.
- Data provenance remains incompletely verified: project configuration refers to OKX USDT perpetuals, but original 1M CSV API source and exact instrument identifiers have not been independently confirmed.
