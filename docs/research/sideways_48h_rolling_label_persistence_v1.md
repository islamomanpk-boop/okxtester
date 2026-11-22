# Sideways Rolling-Label Persistence — 48H Candidates V1

Date: 2026-11-22  
Repository branch: `price-action-v1`

## Purpose

Record persistence statistics for two exploratory 48-hour sideways candidates across BTC, ETH, SOL, DOGE, and AVAX.

- STRICT_P25: 48H channel width at or below the asset-specific P25; directional efficiency <= 0.30; mean adjacent 4H candle overlap >= 0.70.
- BROAD_P40: same conditions, but channel width at or below asset-specific P40.

The 48H features are calculated from 12 completed 4H candles. A new rolling observation is produced every 4H. Channel thresholds are full-sample retrospective percentiles.

## Data

- Common minute timestamps: 569,125.
- Complete 4H candles per asset: 2,370.
- Valid rolling 48H feature windows per asset: 2,358.
- No local files were written or changed by the calculation.

## Results

### BTC

| Metric | STRICT_P25 | BROAD_P40 |
|---|---:|---:|
| Channel threshold | 3.242% | 3.948% |
| Qualifying windows | 401 | 601 |
| Qualifying share | 17.01% | 25.49% |
| Consecutive-label clusters | 106 | 147 |
| Median reported persistence (windows × 4h) | 12h | 12h |
| Mean reported persistence | 15.13h | 16.35h |
| P75 reported persistence | 20h | 20h |
| P90 reported persistence | 32h | 33.6h |
| Longest reported persistence | 64h | 80h |
| Clusters with persistence >=12h | 62 | 93 |
| >=24h | 20 | 30 |
| >=48h | 4 | 8 |
| >=72h | 0 | 1 |
| >=96h | 0 | 0 |
| >=168h | 0 | 0 |

### ETH

| Metric | STRICT_P25 | BROAD_P40 |
|---|---:|---:|
| Channel threshold | 4.245% | 5.475% |
| Qualifying windows | 415 | 620 |
| Qualifying share | 17.60% | 26.29% |
| Consecutive-label clusters | 98 | 142 |
| Median reported persistence | 12h | 12h |
| Mean reported persistence | 16.94h | 17.46h |
| P75 reported persistence | 24h | 24h |
| P90 reported persistence | 36h | 40h |
| Longest reported persistence | 84h | 92h |
| Clusters with persistence >=12h | 58 | 83 |
| >=24h | 26 | 40 |
| >=48h | 4 | 8 |
| >=72h | 1 | 2 |
| >=96h | 0 | 0 |
| >=168h | 0 | 0 |

### SOL

| Metric | STRICT_P25 | BROAD_P40 |
|---|---:|---:|
| Channel threshold | 5.067% | 6.115% |
| Qualifying windows | 409 | 607 |
| Qualifying share | 17.35% | 25.74% |
| Consecutive-label clusters | 107 | 147 |
| Median reported persistence | 12h | 12h |
| Mean reported persistence | 15.29h | 16.52h |
| P75 reported persistence | 20h | 22h |
| P90 reported persistence | 37.6h | 36h |
| Longest reported persistence | 64h | 72h |
| Clusters with persistence >=12h | 57 | 85 |
| >=24h | 21 | 37 |
| >=48h | 5 | 7 |
| >=72h | 0 | 1 |
| >=96h | 0 | 0 |
| >=168h | 0 | 0 |

### DOGE

| Metric | STRICT_P25 | BROAD_P40 |
|---|---:|---:|
| Channel threshold | 5.166% | 6.264% |
| Qualifying windows | 407 | 606 |
| Qualifying share | 17.26% | 25.70% |
| Consecutive-label clusters | 100 | 133 |
| Median reported persistence | 12h | 12h |
| Mean reported persistence | 16.28h | 18.23h |
| P75 reported persistence | 20h | 24h |
| P90 reported persistence | 36h | 40h |
| Longest reported persistence | 80h | 84h |
| Clusters with persistence >=12h | 51 | 77 |
| >=24h | 24 | 40 |
| >=48h | 5 | 13 |
| >=72h | 2 | 2 |
| >=96h | 0 | 0 |
| >=168h | 0 | 0 |

### AVAX

| Metric | STRICT_P25 | BROAD_P40 |
|---|---:|---:|
| Channel threshold | 5.705% | 6.916% |
| Qualifying windows | 430 | 624 |
| Qualifying share | 18.24% | 26.46% |
| Consecutive-label clusters | 102 | 139 |
| Median reported persistence | 12h | 12h |
| Mean reported persistence | 16.86h | 17.96h |
| P75 reported persistence | 24h | 24h |
| P90 reported persistence | 39.6h | 40h |
| Longest reported persistence | 92h | 92h |
| Clusters with persistence >=12h | 55 | 81 |
| >=24h | 29 | 38 |
| >=48h | 5 | 11 |
| >=72h | 2 | 4 |
| >=96h | 0 | 0 |
| >=168h | 0 | 0 |

## Cross-asset observations

1. Both candidates produce similar qualifying-window shares across all five assets: strict approximately 17.0–18.2%, broad approximately 25.5–26.5%.
2. BROAD_P40 produces more qualifying windows and clusters, as expected.
3. Under BROAD_P40, DOGE has 13 clusters and AVAX 11 clusters with reported persistence >=48h, versus 7–8 for BTC, ETH, and SOL.
4. The longest reported persistence is 92h for ETH and AVAX under BROAD_P40; BTC reaches 80h, SOL 72h, DOGE 84h.
5. These descriptive differences do not establish that one asset has more independently occurring sideways regimes. Rolling windows overlap substantially.

## Important duration interpretation correction

The exploratory script reports episode persistence as:

`number_of_consecutive_qualifying_windows × 4 hours`

This is the number of 4H label steps represented by a consecutive run. It is not the full calendar coverage of the underlying rolling windows.

Each qualifying label represents a 48H window. If a run contains N consecutive qualifying labels, and each new label begins 4H after the previous one, the union of their covered calendar intervals is:

`48 hours + (N - 1) × 4 hours`

For example, three consecutive qualifying labels have 12h of label-step persistence by the script's convention, but their rolling windows collectively cover 56h of calendar time.

Therefore:
- Preserve the script's reported duration as **label-step persistence**.
- If useful, calculate the union coverage separately using 48h + (N-1)*4h.
- Neither measure is the independently established duration of a market regime.
- The rolling labels share 44 of 48 hours between adjacent observations, mechanically creating persistence.

## Limitations

- Full-sample percentile thresholds are retrospective and cannot be treated as known live thresholds.
- Consecutive rolling labels overlap heavily and are not independent observations.
- The feature set is an exploratory proxy, not a validated ground-truth sideways label.
- No breakout outcome, trading performance, execution, fees, or profitability was tested.
- Original 1M candle API provenance and exact instrument identifiers remain incompletely verified.

## Next research steps

1. Correctly report both label-step persistence and union calendar coverage for these 48H windows.
2. Compare 24H (6 × 4H candles), 48H (12 × 4H), and 72H (18 × 4H) horizons with the same causal feature definitions.
3. For each horizon, calculate asset-specific retrospective channel percentiles as exploratory thresholds, and clearly mark them as non-live.
4. Compare strict/broad candidate frequencies and persistence across horizons.
5. Then inspect 15M movement inside confirmed 4H sideways contexts and subsequent breakout/failed-breakout behaviour.
