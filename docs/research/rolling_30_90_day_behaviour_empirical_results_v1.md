# Rolling 30-Day and 90-Day Behaviour — Five-Asset Empirical Research

**Project:** Price Action V1  
**Branch:** `price-action-v1`  
**Analysis date:** 2026-11-22  
**Data examined:** Existing local one-minute OHLC CSVs for BTC, ETH, SOL, DOGE and AVAX.  
**Status:** Read-only descriptive research; no strategy/backtest run and no local data files modified.

## 1. Purpose

Measure how volatility and daily movement vary over rolling 30-day and 90-day windows, and compare chronological quarterly behaviour. This is intended to inform later risk-model and SL/TP research. It does not establish profitable trading rules or predict future movement.

## 2. Data and method

- Source files read: `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv` for BTC, ETH, SOL, DOGE and AVAX.
- Input rows reported by the run: BTC 569,125; ETH 569,125; SOL 569,126; DOGE 569,126; AVAX 569,127.
- Inner-joined common timestamps: 569,125.
- Each asset was restricted to the common timestamp index before aggregation.
- UTC daily candles were formed from common minute bars; only days containing exactly 1,440 common minute observations were retained.
- Each asset yielded 394 complete UTC days, 2025-10-21 through 2026-11-18.
- Daily range percentage: `(daily high - daily low) / daily open * 100`.
- Daily close-to-close return: `(daily close / previous complete daily close - 1) * 100`.
- Rolling volatility: sample standard deviation (`ddof=1`) of daily close-to-close percentage returns over the trailing 30 or 90 daily observations.
- Rolling average range: arithmetic mean of daily range percentages over the trailing window.
- Rolling average absolute return: arithmetic mean of absolute daily close-to-close percentage returns over the trailing window.
- Rolling windows are overlapping. They are not independent observations.
- Quarterly summaries use calendar quarters. 2025Q4 and 2026Q4 are partial periods in this dataset; 2026Q4 ends on 2026-11-18.

The daily return for the first complete day is unavailable because the previous complete daily close is not in this daily series. Consequently there are 364 valid rolling 30-day windows and 304 valid rolling 90-day windows per asset.

## 3. Rolling-window results

All values are percentages. “Vol median/P10/P90” summarize the distribution of rolling volatility observations across the available sample. “Latest” is the final available rolling window ending 2026-11-18.

| Asset | Window | Valid windows | Vol median | Vol P10 | Vol P90 | Median rolling avg range | Median rolling avg absolute return | Latest vol | Latest avg range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 30D | 364 | 2.101 | 1.398 | 2.747 | 3.228 | 1.502 | 2.276 | 3.347 |
| BTC | 90D | 304 | 2.060 | 1.820 | 3.077 | 3.199 | 1.516 | 2.166 | 3.077 |
| ETH | 30D | 364 | 3.016 | 1.876 | 3.947 | 4.467 | 2.068 | 3.061 | 4.648 |
| ETH | 90D | 304 | 2.961 | 2.575 | 4.045 | 4.332 | 2.006 | 2.662 | 4.191 |
| SOL | 30D | 364 | 3.122 | 2.091 | 4.260 | 5.043 | 2.326 | 3.117 | 5.003 |
| SOL | 90D | 304 | 3.013 | 2.763 | 4.032 | 4.806 | 2.228 | 3.244 | 5.097 |
| DOGE | 30D | 364 | 3.412 | 2.076 | 4.558 | 5.213 | 2.371 | 3.211 | 5.067 |
| DOGE | 90D | 304 | 3.451 | 2.394 | 4.425 | 5.145 | 2.276 | 3.740 | 5.755 |
| AVAX | 30D | 364 | 3.457 | 2.659 | 5.078 | 5.736 | 2.546 | 4.125 | 6.399 |
| AVAX | 90D | 304 | 3.921 | 2.984 | 4.336 | 5.651 | 2.632 | 4.673 | 6.567 |

## 4. Quarterly chronological comparison

All movement figures are percentages. “Daily return volatility” is the standard deviation of daily close-to-close percentage returns within each quarter.

### BTC

| Quarter | Days | Average daily range | Average absolute daily return | Daily return volatility |
|---|---:|---:|---:|---:|
| 2025Q4 | 72 | 3.732 | 1.606 | 2.077 |
| 2026Q1 | 90 | 4.225 | 2.083 | 3.085 |
| 2026Q2 | 91 | 3.171 | 1.468 | 1.927 |
| 2026Q3 | 92 | 2.851 | 1.341 | 2.030 |
| 2026Q4* | 49 | 3.014 | 1.470 | 1.987 |

### ETH

| Quarter | Days | Average daily range | Average absolute daily return | Daily return volatility |
|---|---:|---:|---:|---:|
| 2025Q4 | 72 | 5.578 | 2.373 | 3.225 |
| 2026Q1 | 90 | 5.803 | 2.847 | 4.075 |
| 2026Q2 | 91 | 4.285 | 1.905 | 2.662 |
| 2026Q3 | 92 | 3.900 | 1.792 | 2.862 |
| 2026Q4* | 49 | 4.252 | 1.879 | 2.662 |

### SOL

| Quarter | Days | Average daily range | Average absolute daily return | Daily return volatility |
|---|---:|---:|---:|---:|
| 2025Q4 | 72 | 6.304 | 2.713 | 3.581 |
| 2026Q1 | 90 | 6.224 | 2.981 | 4.046 |
| 2026Q2 | 91 | 4.801 | 2.227 | 2.929 |
| 2026Q3 | 92 | 4.446 | 2.142 | 2.964 |
| 2026Q4* | 49 | 4.700 | 1.989 | 2.766 |

### DOGE

| Quarter | Days | Average daily range | Average absolute daily return | Daily return volatility |
|---|---:|---:|---:|---:|
| 2025Q4 | 72 | 6.166 | 2.930 | 3.662 |
| 2026Q1 | 90 | 6.624 | 3.085 | 4.434 |
| 2026Q2 | 91 | 4.519 | 1.803 | 2.436 |
| 2026Q3 | 92 | 5.002 | 2.216 | 3.414 |
| 2026Q4* | 49 | 4.917 | 2.171 | 2.924 |

### AVAX

| Quarter | Days | Average daily range | Average absolute daily return | Daily return volatility |
|---|---:|---:|---:|---:|
| 2025Q4 | 72 | 6.418 | 3.151 | 4.017 |
| 2026Q1 | 90 | 6.004 | 2.866 | 4.080 |
| 2026Q2 | 91 | 5.339 | 2.315 | 3.116 |
| 2026Q3 | 92 | 5.644 | 2.640 | 4.107 |
| 2026Q4* | 49 | 6.257 | 2.769 | 3.918 |

*2026Q4 is partial, covering 2026-10-01 through 2026-11-18 in the available complete-day data. 2025Q4 is also partial, beginning 2025-10-21.*

## 5. Empirical observations

1. **BTC is the lowest-volatility asset in this sample.** Its rolling volatility median is about 2.1% for both windows, substantially below the other four assets.
2. **ETH and SOL form an intermediate group in typical rolling volatility.** Their rolling medians are close, although SOL has higher rolling average daily range and absolute return in these summaries.
3. **DOGE is more volatile than BTC, ETH and SOL by rolling median volatility.** Its latest 90-day volatility (3.740%) is higher than its latest 30-day reading (3.211%), suggesting the broader recent window captures more elevated variation.
4. **AVAX is the clearest high-volatility outlier.** Its 90-day rolling volatility median (3.921%) is higher than its 30-day median (3.457%). Its latest 90-day value (4.673%) exceeds its own historical rolling 90-day P90 (4.336%). Its latest rolling average daily range is also high at 6.567%.
5. **The five assets generally experienced higher daily movement in 2026Q1 than in 2026Q2.** BTC, ETH, SOL and DOGE show lower daily return volatility in Q2 than Q1. AVAX also fell from 4.080% to 3.116%, but rose again to 4.107% in Q3 and remained elevated in the partial Q4.
6. **AVAX's movement stayed comparatively high through the later quarters.** Its Q4 partial-period average daily range is 6.257%, compared with 5.644% in Q3. This is a descriptive observation, not evidence that the next period will behave similarly.
7. **Range, absolute return and return volatility measure different things.** A large intraday high-low range does not mean the close-to-close return was equally large, nor does it prove a tradable opportunity existed after costs.

## 6. Research implications — not trading decisions

- Do not select fixed coin-specific stop-loss or take-profit percentages from these descriptive tables alone.
- Later candidate risk models should compare structure-based, volatility-based and hybrid stop placement.
- Position sizing should preserve the same intended dollar risk: a wider stop should normally mean a smaller position, subject to contract specifications and portfolio exposure limits.
- Consider volatility adaptation as a state-dependent input rather than assigning one permanent distance to each coin.
- Any later thresholds must be estimated using development data only, then frozen for chronological validation and out-of-sample evaluation. Full-sample percentiles in this report are retrospective descriptions and must not be used as live, causal thresholds.
- A high-volatility asset can have large adverse excursions, spread/slippage, stop distance and funding costs. High movement is not synonymous with profitability.
- Strategy conclusions require later execution-aware testing, fees, slippage, funding, realistic fills and portfolio-level risk controls. No such test was performed here.

## 7. Limitations and next research

- The data's original exchange/API provenance and exact instrument identity remain unverified. The file names and prior project configuration do not independently prove source.
- The volume unit is not addressed in this analysis.
- Only complete UTC days were retained; partial boundary days were excluded.
- The sample covers roughly 13 months, with only 394 complete days. The 90-day windows overlap heavily and are not independent.
- Quarterly groups at the beginning and end of the sample are partial and should not be compared as if they were full quarters.
- These are descriptive OHLC statistics, not order-book, spread, liquidity, slippage or executable-fill measurements.
- Next research step: characterize volatility-state frequency and persistence using clearly labelled retrospective thresholds, then examine market structure (trends, ranges, breakouts, failed breakouts, pullbacks and reversals). Avoid lookahead when later translating any state definition into a strategy.

**Conclusion:** The observed evidence supports researching asset-aware and volatility-aware risk models, especially for AVAX and DOGE, but it does not yet justify choosing different SL/TP values or claiming any approach is profitable.
