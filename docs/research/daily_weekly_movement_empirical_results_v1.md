# Five-Asset Daily and Weekly Movement Results — 2026-11-22

## Status
First empirical daily/weekly movement calculation completed from existing local 1-minute CSVs. Read-only; no source data or project files modified. Backtests remain paused.

## Input and sample
Files:
- ~/okx_scalping_data/BTC_USDT_USDT_1m.csv
- ~/okx_scalping_data/ETH_USDT_USDT_1m.csv
- ~/okx_scalping_data/SOL_USDT_USDT_1m.csv
- ~/okx_scalping_data/DOGE_USDT_USDT_1m.csv
- ~/okx_scalping_data/AVAX_USDT_USDT_1m.csv

The calculation inner-joined all five timestamp indexes:
- Common 1-minute candles: 569,125
- First common timestamp: 2025-10-20 08:50 UTC
- Last common timestamp: 2026-11-19 14:14 UTC
- Complete daily observations reported: 393 per asset
- Complete weekly observations reported: 54 per asset

## Definitions used
- Daily/weekly range % = (period high - period low) / period open * 100.
- Daily/weekly close-to-close return % = current complete period close / previous complete period close - 1.
- Average absolute return = mean of absolute close-to-close returns.
- Median absolute return = median of absolute close-to-close returns.
- P90/P95 = 90th/95th percentile of period range.
- Up/down frequencies are based on the sign of close-to-close returns; zero returns are not counted in either.

Only complete UTC days (1,440 common minute bars) and complete Monday-Sunday UTC weeks (10,080 common minute bars) were retained. The first complete period's return is excluded because there is no prior complete period close.

## Daily results — common sample

| Coin | Periods | Mean range | Median range | P90 range | P95 range | Mean absolute return | Median absolute return | Up | Down |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 393 | 3.414% | 2.991% | 5.867% | 7.130% | 1.605% | 1.188% | 47.84% | 52.16% |
| ETH | 393 | 4.769% | 4.049% | 8.517% | 9.916% | 2.175% | 1.470% | 49.87% | 50.13% |
| SOL | 393 | 5.299% | 4.506% | 9.112% | 10.588% | 2.438% | 1.762% | 46.82% | 53.18% |
| DOGE | 393 | 5.460% | 4.780% | 9.084% | 11.417% | 2.443% | 1.688% | 43.26% | 56.74% |
| AVAX | 393 | 5.871% | 5.154% | 9.435% | 11.232% | 2.725% | 2.000% | 46.06% | 53.94% |

## Weekly results — common sample

| Coin | Periods | Mean range | Median range | P90 range | P95 range | Mean absolute return | Median absolute return | Up | Down |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 54 | 9.368% | 7.828% | 15.619% | 18.964% | 4.476% | 3.554% | 42.59% | 57.41% |
| ETH | 54 | 12.837% | 11.514% | 20.645% | 26.872% | 5.710% | 3.942% | 40.74% | 59.26% |
| SOL | 54 | 14.307% | 12.912% | 22.993% | 27.436% | 6.477% | 4.438% | 37.04% | 62.96% |
| DOGE | 54 | 14.931% | 13.887% | 23.450% | 29.868% | 6.717% | 6.217% | 33.33% | 66.67% |
| AVAX | 54 | 16.079% | 14.303% | 25.893% | 29.775% | 7.377% | 5.367% | 33.33% | 66.67% |

## Initial observations — not trading conclusions
1. AVAX has the largest average daily range (5.871%) and weekly range (16.079%) in this sample; BTC has the smallest (3.414% daily; 9.368% weekly).
2. The mean daily range is about 1.72 times BTC for AVAX (5.871 / 3.414), but this is a historical descriptive ratio, not a forecast.
3. Average absolute daily close-to-close returns range from 1.605% BTC to 2.725% AVAX.
4. Average absolute weekly close-to-close returns range from 4.476% BTC to 7.377% AVAX.
5. Weekly up frequencies are below 50% for all five in this sample. This is descriptive and does not imply a persistent future bearish edge.
6. DOGE and SOL have similar average absolute daily returns (2.443% and 2.438%), despite differences in range and return distribution.
7. P90/P95 ranges show materially larger movement in the upper tail than the median. Tail events need separate analysis.

## Methodological cautions
- These are descriptive statistics for the observed sample, not expected profit, executable range, or evidence of strategy profitability.
- High-low range is not directional return and cannot be treated as a captureable trading move.
- Daily/weekly range uses period open as denominator; returns are close-to-close.
- The weekly sample has only 54 complete weeks, so weekly estimates are less stable than daily estimates.
- The same common timestamp sample was used for every coin. Individual-history outputs were identical in this run because the common sample excluded only the incomplete leading/trailing periods relevant to these complete buckets.
- Pandas emitted a deprecation warning for DatetimeIndex.dayofweek; calculation completed and results were produced. A future rerun should use day_of_week, but no rerun is necessary now.

## Next research steps
Keep experiments paused. Continue read-only research:
1. Daily and weekly threshold frequencies (range and absolute close-to-close return at 1%, 2%, 3%, 5%, 10%).
2. Daily/weekly movement by UTC weekday and time-of-day.
3. Rolling 30-day and 90-day volatility/range changes and chronological subperiod comparisons.
4. Sideways/ranging market behaviour, sharp jumps/gaps, and volatility clustering.
5. Cross-coin correlations and lead/lag/connectedness.
6. Separate descriptive findings from hypotheses and later strategy tests.

No backtest, downloader, data transformation, or file-writing calculation was performed as part of the local measurement. Only this research checkpoint is committed.
