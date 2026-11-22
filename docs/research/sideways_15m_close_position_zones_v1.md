# 15M Close Position Inside Confirmed 48H Sideways Channels — V1

## Purpose

Describe where 15-minute closes occur inside an exploratory 48-hour sideways-channel classification for BTC, ETH, SOL, DOGE and AVAX. This is descriptive market-structure research, not a trading strategy test.

## Data and method

- Five-asset common 1-minute timestamp intersection: 569,125 candles.
- Complete UTC 4H candles: 2,370 per asset.
- Complete UTC 15M candles: 37,941 per asset.
- 48H channel uses 12 completed 4H candles.
- Sideways condition: channel width at or below the asset-specific full-sample P25 (STRICT_P25) or P40 (BROAD_P40), directional efficiency <= 0.30, and average adjacent-candle overlap >= 0.70.
- 4H features are timestamped at the 4H candle close and mapped forward to 15M bars. Each 15M candle is counted once under the latest confirmed state.
- For each selected 15M close, normalized position is (close - confirmed channel low) / (confirmed channel high - confirmed channel low).
- Zones: BELOW (<0), LOWER (0 to <1/3), MIDDLE (1/3 to <2/3), UPPER (2/3 to 1 inclusive), ABOVE (>1).
- Transition tables count transitions between consecutive selected 15M candles only.
- Read-only calculation; no local data files were written.

## 48H strict P25 close-position distribution

Percent of selected 15M closes:

| Asset | Selected bars | Below | Lower | Middle | Upper | Above |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 6,432 | 4.59% | 20.38% | 46.69% | 23.97% | 4.37% |
| ETH | 6,672 | 3.90% | 18.35% | 50.37% | 23.17% | 4.21% |
| SOL | 6,560 | 4.36% | 26.71% | 40.62% | 24.74% | 3.57% |
| DOGE | 6,528 | 3.09% | 22.24% | 47.12% | 23.79% | 3.75% |
| AVAX | 6,880 | 3.56% | 25.35% | 42.62% | 24.87% | 3.60% |

## 48H broad P40 close-position distribution

| Asset | Selected bars | Below | Lower | Middle | Upper | Above |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 9,616 | 3.84% | 23.14% | 45.47% | 23.50% | 4.06% |
| ETH | 9,920 | 3.82% | 20.58% | 49.38% | 22.45% | 3.77% |
| SOL | 9,744 | 4.47% | 27.49% | 41.22% | 23.40% | 3.42% |
| DOGE | 9,721 | 3.08% | 24.62% | 46.13% | 22.94% | 3.24% |
| AVAX | 9,977 | 3.35% | 23.29% | 44.05% | 26.53% | 2.78% |

## Transition observations

The transition matrices show strong persistence in the same zone and frequent movement between neighbouring zones. Direct lower-to-upper and upper-to-lower transitions between adjacent 15M closes were almost absent:
- BTC strict: 2 lower-to-upper, 0 upper-to-lower; broad: 2 and 0.
- ETH strict and broad: 0 and 0.
- SOL strict and broad: 0 and 0.
- DOGE strict and broad: 0 and 0.
- AVAX strict: 0 and 2; broad: 0 and 2.

These direct transitions are not the main measure of range oscillation; price would usually move through the middle zone over several candles. Raw transition counts are not conditional transition probabilities.

## Main descriptive findings

1. The middle third contains the largest share of closes for every asset under both definitions (about 40.6%–50.4%).
2. ETH has the highest middle-third occupancy: 50.37% strict and 49.38% broad.
3. SOL has the highest lower-third occupancy: 26.71% strict and 27.49% broad.
4. AVAX has the highest upper-third occupancy under the broad definition: 26.53%.
5. Closes outside the current confirmed channel are approximately 2.78%–4.59% below and 2.78%–4.37% above, depending on asset and definition.
6. The broad definition selects more candles but retains a similar overall occupancy pattern.

## Interpretation limits and caveats

- These are close-position statistics, not wick-touch, boundary-rejection, or executable-entry statistics.
- Channel boundaries and thirds are recalculated when a new 4H window is confirmed. Therefore, a zone change can reflect moving boundaries as well as price movement.
- The rolling 48H feature windows overlap by 44 hours between adjacent 4H updates; selected states and observations are not independent regimes.
- Full-sample P25/P40 thresholds are retrospective and are not live/deployable thresholds.
- Transition matrices report raw counts, not probabilities or trading edge.
- OHLC bars do not reveal the intrabar order in which high and low occurred.
- No fees, spread, slippage, liquidity, funding, order fills, stop/target paths, or profitability were tested.
- Data-source provenance limitations documented elsewhere in the project remain applicable.

## Next research question

Measure actual 15M wick interaction with the confirmed upper/lower channel boundaries and rejection/follow-through behaviour. Freeze the relevant confirmed boundaries for each observation, distinguish wick touches from closes outside, de-cluster repeated tests, and avoid assuming intrabar high/low order. Then study multi-candle travel between thirds and breakout/failed-breakout behaviour.

## Research status

Descriptive research only. No strategy testing or parameter selection.
