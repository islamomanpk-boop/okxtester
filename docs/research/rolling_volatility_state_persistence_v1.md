# Rolling Volatility State Frequency and Persistence — Five-Asset Study

**Project:** Price Action V1  
**Branch:** `price-action-v1`  
**Date recorded:** 2026-11-22  
**Assets:** BTC, ETH, SOL, DOGE, AVAX  
**Status:** Descriptive research only; no strategy testing.

## Purpose

Measure how frequently each asset's rolling daily-return volatility falls into low, normal, or high historical states, and describe the lengths of consecutive episodes. This follows the rolling 30-day/90-day behaviour study.

## Data and method

- Read the existing five 1-minute CSV files from `~/okx_scalping_data`; no files were written or modified.
- Common timestamp intersection: 569,125 minute bars.
- For each asset, aggregate only complete UTC days with 1,440 common minute observations.
- Complete daily observations: 394 per asset, 2025-10-21 through 2026-11-18.
- Daily close-to-close percentage returns: `close.pct_change() * 100`.
- Rolling volatility: trailing 30 or 90 daily returns' sample standard deviation (`rolling(window).std()`).
- Valid rolling observations: 364 for 30D and 304 for 90D.
- Per asset and window, define LOW as volatility at/below its own full-sample 25th percentile, HIGH as at/above its own 75th percentile, and NORMAL as the interval between.
- Consecutive identical labels are grouped into episodes. Episode duration is the number of rolling observations in that run.

## Results

### Rolling volatility state thresholds

| Asset | Window | Q25 low threshold | Q75 high threshold | Observations |
|---|---:|---:|---:|---:|
| BTC | 30D | 1.683% | 2.348% | 364 |
| BTC | 90D | 1.976% | 2.881% | 304 |
| ETH | 30D | 2.338% | 3.585% | 364 |
| ETH | 90D | 2.765% | 3.825% | 304 |
| SOL | 30D | 2.437% | 3.600% | 364 |
| SOL | 90D | 2.884% | 3.856% | 304 |
| DOGE | 30D | 2.347% | 4.051% | 364 |
| DOGE | 90D | 2.578% | 4.058% | 304 |
| AVAX | 30D | 3.053% | 4.181% | 364 |
| AVAX | 90D | 3.100% | 4.093% | 304 |

### 30-day state episodes

Each asset has 91 LOW, 182 NORMAL, and 91 HIGH observations (25%, 50%, 25%) by construction.

| Asset | State | Episodes | Median episode days | Longest episode days |
|---|---|---:|---:|---:|
| BTC | LOW | 5 | 21.0 | 27 |
| BTC | NORMAL | 14 | 9.0 | 39 |
| BTC | HIGH | 8 | 1.0 | 57 |
| ETH | LOW | 12 | 3.5 | 24 |
| ETH | NORMAL | 21 | 3.0 | 46 |
| ETH | HIGH | 8 | 3.0 | 42 |
| SOL | LOW | 5 | 19.0 | 26 |
| SOL | NORMAL | 11 | 18.0 | 41 |
| SOL | HIGH | 6 | 9.5 | 40 |
| DOGE | LOW | 5 | 19.0 | 46 |
| DOGE | NORMAL | 15 | 5.0 | 37 |
| DOGE | HIGH | 10 | 4.0 | 39 |
| AVAX | LOW | 5 | 8.0 | 41 |
| AVAX | NORMAL | 11 | 16.0 | 42 |
| AVAX | HIGH | 6 | 12.0 | 31 |

### 90-day state episodes

Each asset has 76 LOW, 152 NORMAL, and 76 HIGH observations (25%, 50%, 25%) by construction.

| Asset | State | Episodes | Median episode days | Longest episode days |
|---|---|---:|---:|---:|
| BTC | LOW | 5 | 12.0 | 47 |
| BTC | NORMAL | 10 | 11.0 | 62 |
| BTC | HIGH | 4 | 5.5 | 63 |
| ETH | LOW | 3 | 10.0 | 64 |
| ETH | NORMAL | 7 | 11.0 | 90 |
| ETH | HIGH | 4 | 4.0 | 66 |
| SOL | LOW | 6 | 9.5 | 39 |
| SOL | NORMAL | 13 | 4.0 | 62 |
| SOL | HIGH | 6 | 2.5 | 65 |
| DOGE | LOW | 4 | 3.5 | 68 |
| DOGE | NORMAL | 8 | 2.0 | 90 |
| DOGE | HIGH | 3 | 6.0 | 68 |
| AVAX | LOW | 5 | 16.0 | 27 |
| AVAX | NORMAL | 12 | 4.5 | 78 |
| AVAX | HIGH | 7 | 6.0 | 51 |

## Interpretation

- The coin-specific thresholds differ materially. BTC's 30D HIGH threshold is 2.348%, while AVAX's is 4.181%. A common absolute volatility threshold would therefore classify these assets differently.
- In the 30D series, BTC and ETH show relatively short median HIGH episodes (1 and 3 days), while SOL and AVAX show longer medians (9.5 and 12 days). DOGE's median HIGH episode is 4 days.
- In the 90D series, all five assets have longer maximum runs in at least some states. This is expected in part because a 90-observation rolling standard deviation changes more slowly than a 30-observation measure.
- SOL's 30D LOW episodes have a 19-day median; DOGE's 30D LOW episodes also have a 19-day median. These are observations about this sample and this retrospective classification, not forecasts.
- The maximum episode length is not the typical duration. For example, BTC's 30D HIGH episodes have a 1-day median despite one run reaching 57 days; the distribution of episode lengths is uneven.

## Critical limitations

1. The state shares of 25%/50%/25% are imposed by full-sample quantile thresholds. They do **not** show that an asset naturally spends those exact proportions of time in each state.
2. Thresholds use the full historical sample, including future observations relative to any historical date. This is retrospective descriptive classification, not a causal/live signal. A deployable regime classifier must calculate thresholds using only information available at the time (for example, expanding or trailing historical quantiles).
3. Consecutive rolling windows overlap heavily. A 30D value shares 29 of 30 daily returns with the next value; a 90D value shares 89 of 90. This mechanically smooths the series and can inflate apparent persistence. Episode lengths are not independent market-regime durations.
4. Episode length is counted in rolling-observation dates, not the duration of a directly observed underlying market state.
5. This measures return volatility, not directional predictability, executable opportunity, stop-loss distance, or strategy profitability.
6. The underlying candle source/instrument provenance remains not independently verified; see the separate provenance checkpoints.
7. Sample covers only 394 complete daily bars. Findings are descriptive and should be revisited with additional history and robust out-of-sample methods.

## Research implications and next work

- Keep coin-specific volatility scales under consideration, but do not select SL/TP values from these thresholds or episode lengths.
- Before designing an adaptive risk model, investigate volatility clustering with less mechanically overlapping measures, such as non-overlapping 30-day blocks, and test causal rolling/expanding thresholds.
- Continue market-structure research: trend, range, breakout, failed breakout, pullback, and reversal behaviour. Later compare structure-based, volatility-based, and hybrid stop concepts.
- Maintain a shared portfolio risk budget. If a wider stop is eventually justified, position size must be reduced to preserve the same planned dollar risk.
- No backtests or experiments are authorized by this checkpoint. Research remains paused from strategy execution.

**Conclusion:** The data supports further investigation of asset-specific and condition-aware risk distances, but this episode analysis is preliminary. Its quantile construction and overlapping windows prevent treating the reported state shares or run lengths as live regime rules.
