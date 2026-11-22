# Sideways Horizon Comparison: 24H, 48H and 72H V1

Date: 2026-11-22  
Repository: `islamomanpk-boop/okxtester`  
Branch: `price-action-v1`

## Purpose

Compare three exploratory sideways-market measurement horizons using complete 4H candles across BTC, ETH, SOL, DOGE and AVAX:

- 24H = 6 consecutive 4H candles
- 48H = 12 consecutive 4H candles
- 72H = 18 consecutive 4H candles

For each asset and horizon, two candidate labels are compared:

- STRICT_P25: channel width <= the asset/horizon full-sample 25th percentile, directional efficiency <= 0.30, mean adjacent-candle overlap >= 0.70.
- BROAD_P40: channel width <= the asset/horizon full-sample 40th percentile, directional efficiency <= 0.30, mean adjacent-candle overlap >= 0.70.

This is descriptive research, not strategy testing.

## Data and calculation

- Five existing 1-minute CSVs were inner-joined on timestamp.
- Common minute candles: 569,125.
- Complete 4H candles per asset: 2,370.
- Valid rolling windows: 2,364 (24H), 2,358 (48H), 2,352 (72H).
- 4H resampling is UTC, epoch-anchored; only complete 240-minute candles retained.
- Channel width = (rolling maximum high / rolling minimum low - 1) × 100.
- Directional efficiency = absolute net close movement divided by the sum of absolute close-to-close movements over the corresponding horizon.
- Candle overlap = intersection of adjacent candle high-low ranges divided by the smaller candle range; the feature is the rolling mean across adjacent pairs in the horizon.
- Channel percentile thresholds are computed separately for each asset and horizon from the full sample.
- Each new rolling label advances by 4 hours.

For an episode with N consecutive qualifying labels and horizon H, label-step persistence is N × 4 hours. The union of the rolling windows' calendar coverage is H + (N - 1) × 4 hours.

## Cross-asset averages

| Horizon | STRICT_P25 qualifying windows | BROAD_P40 qualifying windows |
|---|---:|---:|
| 24H | 11.92% | 18.17% |
| 48H | 17.49% | 26.03% |
| 72H | 20.50% | 31.07% |

These averages are arithmetic averages of the five asset percentages.

## Asset-specific results

Each cell is shown as **threshold / qualifying-window share / episode count / median calendar coverage / P90 calendar coverage / longest calendar coverage**. Channel thresholds are percentages; calendar durations are hours.

### 24H horizon

| Asset | STRICT_P25 | BROAD_P40 |
|---|---|---|
| BTC | 2.084 / 11.63% / 135 / 24 / 36 / 48 | 2.649 / 18.10% / 194 / 28 / 40 / 56 |
| ETH | 2.880 / 12.44% / 132 / 28 / 36 / 72 | 3.566 / 19.33% / 195 / 28 / 40 / 72 |
| SOL | 3.296 / 11.38% / 131 / 24 / 36 / 72 | 4.109 / 17.30% / 191 / 28 / 36 / 72 |
| DOGE | 3.447 / 12.14% / 139 / 24 / 36 / 56 | 4.306 / 18.02% / 210 / 24 / 36 / 60 |
| AVAX | 3.820 / 12.01% / 136 / 26 / 36 / 68 | 4.657 / 18.10% / 198 / 28 / 36 / 68 |

Episodes with calendar coverage >=48h / >=72h / >=96h / >=168h:

| Asset | STRICT_P25 | BROAD_P40 |
|---|---|---|
| BTC | 2 / 0 / 0 / 0 | 3 / 0 / 0 / 0 |
| ETH | 4 / 1 / 0 / 0 | 5 / 1 / 0 / 0 |
| SOL | 2 / 1 / 0 / 0 | 3 / 1 / 0 / 0 |
| DOGE | 2 / 0 / 0 / 0 | 3 / 0 / 0 / 0 |
| AVAX | 2 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |

### 48H horizon

| Asset | STRICT_P25 | BROAD_P40 |
|---|---|---|
| BTC | 3.242 / 17.01% / 106 / 56 / 76 / 108 | 3.948 / 25.49% / 147 / 56 / 77.6 / 124 |
| ETH | 4.245 / 17.60% / 98 / 56 / 80 / 128 | 5.475 / 26.29% / 142 / 56 / 84 / 136 |
| SOL | 5.067 / 17.35% / 107 / 56 / 81.6 / 108 | 6.115 / 25.74% / 147 / 56 / 80 / 116 |
| DOGE | 5.166 / 17.26% / 100 / 56 / 80 / 124 | 6.264 / 25.70% / 133 / 56 / 84 / 128 |
| AVAX | 5.705 / 18.24% / 102 / 56 / 83.6 / 136 | 6.916 / 26.46% / 139 / 56 / 84 / 136 |

Episodes with calendar coverage >=48h / >=72h / >=96h / >=168h:

| Asset | STRICT_P25 | BROAD_P40 |
|---|---|---|
| BTC | 106 / 17 / 4 / 0 | 147 / 23 / 8 / 0 |
| ETH | 98 / 19 / 3 / 0 | 142 / 30 / 6 / 0 |
| SOL | 107 / 17 / 4 / 0 | 147 / 28 / 5 / 0 |
| DOGE | 100 / 21 / 3 / 0 | 133 / 33 / 7 / 0 |
| AVAX | 102 / 22 / 5 / 0 | 139 / 31 / 9 / 0 |

### 72H horizon

| Asset | STRICT_P25 | BROAD_P40 |
|---|---|---|
| BTC | 4.163 / 19.47% / 83 / 84 / 123.2 / 176 | 4.924 / 29.42% / 115 / 84 / 126.4 / 212 |
| ETH | 5.681 / 20.32% / 71 / 88 / 120 / 272 | 6.819 / 30.87% / 106 / 84 / 128 / 304 |
| SOL | 6.251 / 20.45% / 70 / 88 / 132 / 184 | 7.864 / 30.44% / 111 / 80 / 132 / 216 |
| DOGE | 6.337 / 21.90% / 63 / 88 / 132 / 244 | 7.818 / 33.42% / 92 / 92 / 132 / 252 |
| AVAX | 7.372 / 20.37% / 74 / 84 / 134.8 / 232 | 8.611 / 31.21% / 98 / 86 / 141.2 / 236 |

Episodes with calendar coverage >=48h / >=72h / >=96h / >=168h:

| Asset | STRICT_P25 | BROAD_P40 |
|---|---|---|
| BTC | 83 / 83 / 18 / 1 | 115 / 115 / 34 / 2 |
| ETH | 71 / 71 / 23 / 2 | 106 / 106 / 35 / 3 |
| SOL | 70 / 70 / 25 / 1 | 111 / 111 / 37 / 2 |
| DOGE | 63 / 63 / 26 / 3 | 92 / 92 / 41 / 4 |
| AVAX | 74 / 74 / 25 / 2 | 98 / 98 / 42 / 2 |

## Findings

1. The 24H definition identifies shorter consolidations. Median calendar coverage is generally 24–28 hours.
2. The 48H definition identifies more established ranges. Median calendar coverage is 56 hours across the reported asset/candidate combinations.
3. The 72H definition produces the longest clusters. Median calendar coverage is approximately 80–92 hours.
4. Qualifying-window share rises with horizon for both candidate definitions. This is not evidence that the market spends more time in sideways regimes: the horizon, channel threshold, and rolling feature distribution all change.
5. DOGE has the largest 72H BROAD_P40 qualifying share (33.42%) and the largest count of broad episodes with at least 96h calendar coverage (41). AVAX has 42 such episodes, the highest count in this comparison.
6. Under 24H BROAD_P40, no asset has an episode reaching 96h calendar coverage. Under 72H BROAD_P40, all five assets have many such clusters.
7. The longer-horizon definitions are useful for studying extended consolidation, while 24H is useful for short consolidation. No single final production definition is selected yet.

## Critical limitations

- Percentile thresholds are calculated using the full sample. They are retrospective and cannot be used as if known in real time.
- Rolling windows advance every 4H and overlap heavily. Adjacent labels share most of their underlying candles; cluster persistence is mechanically increased.
- Calendar coverage is the union of the rolling windows represented by a consecutive run. It is not independent confirmation that the market stayed in one true regime throughout.
- Candidate thresholds are exploratory. No external ground-truth range labels, breakout outcomes, or trading results have been tested.
- The data's original 1M API provenance and exact instrument IDs remain incompletely verified.
- High-low channel width is not the same as executable trading opportunity.

## Decision and next steps

Keep all three horizons in the research set:

- 24H: short consolidation lens.
- 48H: medium consolidation lens.
- 72H: extended consolidation lens.

Do not choose a final classifier or SL/TP values yet.

Next:
1. Inspect 15M candle range, body, close movement, and price location within the range during these 4H sideways contexts.
2. Analyze boundary retests, excursions, and breakouts/failed breakouts after the sideways condition is confirmed, respecting the 4H confirmation time.
3. Compare whether the 24H, 48H, and 72H labels add distinct useful information or mostly duplicate one another.
4. Later test causal expanding/trailing thresholds rather than full-sample percentiles.

No backtests or strategy profitability claims are made in this document.
