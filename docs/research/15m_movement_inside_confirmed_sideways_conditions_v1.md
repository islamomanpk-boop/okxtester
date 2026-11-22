# 15M Movement Inside Confirmed Sideways Conditions V1

Research status: descriptive, read-only calculation; not a strategy test.

## Dataset and method

- Five assets: BTC, ETH, SOL, DOGE, AVAX.
- Source files: existing 1-minute CSVs in the local research data directory.
- Common timestamp intersection: 569,125 minute candles.
- Complete bars: 2,370 4H candles and 37,941 15M candles per asset.
- 4H bars and 15M bars are UTC-aligned to epoch boundaries.
- Sideways horizons: 24H (6 4H bars), 48H (12 bars), 72H (18 bars).
- Channel width: rolling maximum high / rolling minimum low - 1.
- Directional efficiency: absolute close-to-close net move over the horizon divided by the sum of absolute consecutive 4H close changes.
- Candle overlap: intersection of adjacent 4H candle ranges divided by the smaller range; averaged over the horizon's adjacent pairs.
- STRICT_P25: channel width at or below the asset/horizon full-sample 25th percentile, efficiency <= 0.30, average overlap >= 0.70.
- BROAD_P40: same, but channel width at or below the asset/horizon full-sample 40th percentile.
- A 4H state is shifted forward by four hours and only applied to 15M candles beginning at or after its confirmation time. Each 15M candle is assigned the latest already-confirmed state.
- 15M range = (high-low)/open * 100; body = absolute close/open - 1 in percent; close-change = absolute close-to-close percentage change.
- No local files were written or changed by the calculation.

## 48H primary-reference results

Median 15M range (%):

| Asset | STRICT_P25 | BROAD_P40 |
|---|---:|---:|
| BTC | 0.1694 | 0.1837 |
| ETH | 0.2243 | 0.2433 |
| SOL | 0.2699 | 0.2958 |
| DOGE | 0.2882 | 0.3128 |
| AVAX | 0.3306 | 0.3508 |

48H BROAD_P40 15M range threshold frequencies:

| Asset | >=0.25% | >=0.50% | >=1.00% | >=2.00% |
|---|---:|---:|---:|---:|
| BTC | 31.50% | 7.55% | 0.82% | 0.08% |
| ETH | 48.34% | 15.13% | 2.72% | 0.31% |
| SOL | 61.56% | 19.67% | 3.40% | 0.38% |
| DOGE | 65.19% | 20.84% | 3.55% | 0.37% |
| AVAX | 72.80% | 26.89% | 4.46% | 0.37% |

## Full horizon results

The following compact tables show mean and median 15M range, plus the percentage of 15M candles whose range reached at least 0.50%.

### Mean 15M range (%)

| Asset | 24H strict | 24H broad | 48H strict | 48H broad | 72H strict | 72H broad |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 0.2083 | 0.2295 | 0.2193 | 0.2335 | 0.2236 | 0.2404 |
| ETH | 0.2825 | 0.3101 | 0.2937 | 0.3197 | 0.3047 | 0.3216 |
| SOL | 0.3386 | 0.3766 | 0.3406 | 0.3728 | 0.3438 | 0.3640 |
| DOGE | 0.3418 | 0.3861 | 0.3594 | 0.3843 | 0.3646 | 0.3831 |
| AVAX | 0.4062 | 0.4333 | 0.4086 | 0.4282 | 0.4111 | 0.4331 |

### Median 15M range (%)

| Asset | 24H strict | 24H broad | 48H strict | 48H broad | 72H strict | 72H broad |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 0.1558 | 0.1749 | 0.1694 | 0.1837 | 0.1787 | 0.1886 |
| ETH | 0.2141 | 0.2374 | 0.2243 | 0.2433 | 0.2367 | 0.2519 |
| SOL | 0.2720 | 0.2996 | 0.2699 | 0.2958 | 0.2744 | 0.2941 |
| DOGE | 0.2674 | 0.3043 | 0.2882 | 0.3128 | 0.2963 | 0.3122 |
| AVAX | 0.3236 | 0.3480 | 0.3306 | 0.3508 | 0.3369 | 0.3529 |

### Percentage of 15M candles with range >=0.50%

| Asset | 24H strict | 24H broad | 48H strict | 48H broad | 72H strict | 72H broad |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 6.20 | 7.37 | 6.66 | 7.55 | 6.54 | 8.06 |
| ETH | 11.65 | 13.84 | 12.98 | 15.13 | 13.26 | 14.98 |
| SOL | 15.13 | 19.96 | 15.83 | 19.67 | 16.16 | 18.70 |
| DOGE | 15.42 | 21.02 | 18.00 | 20.84 | 18.13 | 20.56 |
| AVAX | 23.00 | 27.10 | 23.91 | 26.89 | 24.32 | 27.03 |

## Comparison with unconditional 15M baseline

Previously measured unconditional median 15M ranges were BTC 0.239%, ETH 0.324%, SOL 0.385%, DOGE 0.388%, AVAX 0.413%.

For the 48H BROAD_P40 sample, median range was lower by approximately:
- BTC: 23%
- ETH: 25%
- SOL: 23%
- DOGE: 19%
- AVAX: 15%

This is a descriptive comparison across the same underlying sample, not a causal estimate. The regime selection is retrospective because full-sample channel quantiles are used.

Unconditional >=0.50% range frequencies were BTC 14.4%, ETH 26.6%, SOL 33.7%, DOGE 33.8%, AVAX 37.7%. The 48H BROAD_P40 frequencies were 7.55%, 15.13%, 19.67%, 20.84%, and 26.89%, respectively.

## Main observations

1. Sideways classification is associated with lower typical 15M candle ranges than the unconditional baseline for all five assets.
2. Sideways does not mean motionless. In the 48H BROAD_P40 sample, 7.55% to 26.89% of 15M candles still had ranges of at least 0.50%, depending on the asset.
3. The cross-asset ranking is consistent: BTC has the smallest typical 15M movement; AVAX has the largest, with ETH, SOL and DOGE between them.
4. BROAD_P40 generally selects more candles and has somewhat larger movement statistics than STRICT_P25. This is expected because it permits wider channel widths.
5. Horizon differences are not monotonic for every asset/metric. No single horizon can yet be declared best.
6. 15M body and absolute close-to-close movement are very similar because the bars are contiguous and the next 15M open is generally the prior 15M close. Small differences may arise from price gaps/rounding or the separate formulas.

## Important limitations and follow-up checks

- Channel quantiles are calculated using the full sample. These labels are exploratory and not causal/live-ready thresholds.
- 4H state is held until the next confirmed 4H label; the assigned 15M observations are subsequent to confirmation. This is intended to avoid lookahead in the 15M measurement.
- The horizons and state samples overlap substantially; observations are not independent.
- The same 15M candle can be included in more than one horizon/definition comparison. Do not add sample counts across conditions.
- Candle range is not a tradable profit measure. This study does not model entries, exits, spread, fees, slippage, funding, order fills or intrabar path.
- The results do not establish that range-fading or any other sideways strategy is profitable.
- Data-source provenance for the underlying 1M CSVs is still not independently verified.

Next research: measure range position (upper/middle/lower thirds), internal 15M oscillations, boundary tests and rejection/penetration, followed by breakout and failed-breakout behaviour. Preserve the same confirmation-time discipline.
