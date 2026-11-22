# Daily and Weekly Movement Thresholds — Five-Asset Study

**Date recorded:** 2026-11-22  
**Project:** Price Action V1  
**Assets:** BTC, ETH, SOL, DOGE, AVAX  
**Status:** Read-only descriptive research; no strategy/backtest run.

## 1. Data and sample

The calculations read the existing one-minute CSV files in `~/okx_scalping_data` and used only timestamps common to all five assets.

- Common one-minute timestamps: 569,125
- First common timestamp: 2025-10-20 08:50 UTC
- Last common timestamp: 2026-11-19 14:14 UTC
- Complete daily periods retained: 393 per asset
- Complete weekly periods retained: 54 per asset

A daily period is a UTC calendar day with exactly 1,440 common one-minute observations. A weekly period is Monday 00:00 UTC through Sunday 23:59 UTC with exactly 10,080 common one-minute observations. The first complete period is excluded from both summaries because its close-to-close return has no preceding complete-period close. This leaves 393 daily and 54 weekly observations.

Only existing data was read. No files were created or modified by the calculations. The weekly calculation was rerun after correcting the week key to floor timestamps to UTC midnight before subtracting the weekday number. The first weekly attempt returned zero periods and its NaN outputs are invalid; the corrected weekly results below supersede it.

## 2. Definitions

- Period range (%) = (period high − period low) / period open × 100.
- Close-to-close return (%) = (current period close / previous complete period close − 1) × 100.
- Absolute return threshold counts use the absolute value of close-to-close return, so either an up or down move qualifies.
- Thresholds are inclusive: at least 1%, 2%, 3%, 5%, or 10%.
- Percentages are counts divided by the number of retained periods (393 daily or 54 weekly).

High-low range is not directional return and is not a measure of how much a strategy could capture after fees, slippage, funding, and execution constraints.

## 3. Daily movement threshold results

Each cell is count (percentage of 393 daily periods).

### Daily high-low range

| Asset | ≥1% | ≥2% | ≥3% | ≥5% | ≥10% |
|---|---:|---:|---:|---:|---:|
| BTC | 377 (95.93%) | 301 (76.59%) | 196 (49.87%) | 63 (16.03%) | 3 (0.76%) |
| ETH | 387 (98.47%) | 354 (90.08%) | 280 (71.25%) | 139 (35.37%) | 17 (4.33%) |
| SOL | 392 (99.75%) | 373 (94.91%) | 315 (80.15%) | 170 (43.26%) | 29 (7.38%) |
| DOGE | 393 (100.00%) | 370 (94.15%) | 317 (80.66%) | 181 (46.06%) | 28 (7.12%) |
| AVAX | 393 (100.00%) | 386 (98.22%) | 345 (87.79%) | 210 (53.44%) | 33 (8.40%) |

### Daily absolute close-to-close return

| Asset | ≥1% | ≥2% | ≥3% | ≥5% | ≥10% |
|---|---:|---:|---:|---:|---:|
| BTC | 215 (54.71%) | 108 (27.48%) | 51 (12.98%) | 19 (4.83%) | 2 (0.51%) |
| ETH | 233 (59.29%) | 153 (38.93%) | 98 (24.94%) | 40 (10.18%) | 5 (1.27%) |
| SOL | 261 (66.41%) | 179 (45.55%) | 126 (32.06%) | 46 (11.70%) | 8 (2.04%) |
| DOGE | 270 (68.70%) | 167 (42.49%) | 119 (30.28%) | 40 (10.18%) | 10 (2.54%) |
| AVAX | 281 (71.50%) | 197 (50.13%) | 128 (32.57%) | 56 (14.25%) | 10 (2.54%) |

## 4. Weekly movement threshold results

Each cell is count (percentage of 54 weekly periods).

### Weekly high-low range

| Asset | ≥1% | ≥2% | ≥3% | ≥5% | ≥10% |
|---|---:|---:|---:|---:|---:|
| BTC | 54 (100.00%) | 54 (100.00%) | 54 (100.00%) | 51 (94.44%) | 17 (31.48%) |
| ETH | 54 (100.00%) | 54 (100.00%) | 54 (100.00%) | 53 (98.15%) | 33 (61.11%) |
| SOL | 54 (100.00%) | 54 (100.00%) | 54 (100.00%) | 53 (98.15%) | 38 (70.37%) |
| DOGE | 54 (100.00%) | 54 (100.00%) | 54 (100.00%) | 53 (98.15%) | 41 (75.93%) |
| AVAX | 54 (100.00%) | 54 (100.00%) | 54 (100.00%) | 54 (100.00%) | 43 (79.63%) |

### Weekly absolute close-to-close return

| Asset | ≥1% | ≥2% | ≥3% | ≥5% | ≥10% |
|---|---:|---:|---:|---:|---:|
| BTC | 45 (83.33%) | 41 (75.93%) | 30 (55.56%) | 16 (29.63%) | 5 (9.26%) |
| ETH | 49 (90.74%) | 37 (68.52%) | 33 (61.11%) | 22 (40.74%) | 9 (16.67%) |
| SOL | 44 (81.48%) | 41 (75.93%) | 34 (62.96%) | 25 (46.30%) | 13 (24.07%) |
| DOGE | 49 (90.74%) | 45 (83.33%) | 41 (75.93%) | 30 (55.56%) | 10 (18.52%) |
| AVAX | 49 (90.74%) | 44 (81.48%) | 38 (70.37%) | 28 (51.85%) | 13 (24.07%) |

## 5. Descriptive findings

1. AVAX had the highest frequency of large daily and weekly high-low ranges in this sample: daily range ≥5% occurred on 53.44% of days; weekly range ≥10% occurred in 79.63% of weeks.
2. BTC had the lowest frequency of large ranges: daily range ≥5% occurred on 16.03% of days; weekly range ≥10% occurred in 31.48% of weeks.
3. DOGE had the highest daily frequency of absolute close-to-close moves ≥1% (68.70%). AVAX was next at 71.50%, which is actually higher; therefore AVAX led this measure, with DOGE second.
4. AVAX led daily absolute close-to-close moves ≥1% (71.50%) and ≥2% (50.13%). DOGE led weekly absolute close-to-close moves ≥2%, ≥3%, and ≥5%.
5. SOL and AVAX tied for the highest frequency of weekly absolute close-to-close moves ≥10% (24.07%).
6. The difference between range frequency and absolute close-to-close-return frequency is substantial. For example, AVAX had a weekly range ≥10% in 79.63% of weeks, but an absolute weekly close-to-close return ≥10% in only 24.07%. A large excursion within a period often does not translate into an equally large net close-to-close move.
7. Daily range ≥5% was much more common for SOL, DOGE, and AVAX than for BTC in this sample. This may make those assets interesting for later volatility/regime research, but does not establish a trading edge.

## 6. Interpretation limits and quality cautions

- These are descriptive historical frequencies, not forecasts or evidence of strategy profitability.
- High-low range does not say whether a move was orderly, whether a signal was available before it happened, or whether an entry/exit could capture it.
- Close-to-close returns omit the path taken inside each day or week.
- The weekly sample contains only 54 observations, so weekly percentages are less statistically stable than daily percentages.
- The results depend on the current dataset's provenance and volume/instrument-unit uncertainty. This analysis does not independently verify the original exchange API source or exact instrument IDs.
- Using the five-asset common timestamp intersection makes the sample synchronized, but the exact UTC boundaries and full-period filters must be preserved in future comparisons.
- No claims of manipulation, predictable direction, or persistent future bearish/bullish bias are inferred from these tables.

## 7. Research implications and next steps

Keep these as descriptive inputs for later work, not strategy parameters yet.

Next research topics remain:
1. Rolling 30-day and 90-day movement/volatility behaviour and chronological subperiod comparison.
2. Sideways/ranging-market behaviour, including duration and transitions.
3. Sudden jumps, fast reversals, and extreme-volatility episodes, without labelling them manipulation absent evidence.
4. Time-of-day and weekday behaviour.
5. Cross-coin correlation, BTC lead/lag, and connectedness.
6. Separating volatility from executable opportunity and net profitability after costs.

Backtests and experiments remain paused until explicitly authorized.
