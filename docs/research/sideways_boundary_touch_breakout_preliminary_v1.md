# Sideways Boundary Touch and Breakout Study — Preliminary Corrected Results

Date: 2026-11-22
Repository: islamomanpk-boop/okxtester
Branch: price-action-v1

## Scope and method

Read-only descriptive calculation on the five existing 1-minute datasets, joined on their common timestamps (569,125 common minute candles). Complete 4H and 15M bars were resampled from the common series. A 48-hour channel used the rolling high and low of 12 complete 4H bars. Exploratory sideways labels used asset-specific full-sample channel-width P25 (STRICT_P25) or P40 (BROAD_P40), directional efficiency <= 0.30, and average adjacent-candle overlap >= 0.70. A 4H feature snapshot became available only after that 4H bar closed.

Boundary zones were tested at 5%, 10%, and 15% of channel width. A touch means the 15M high/low reaches the outer zone. Broad rejection means the candle closes back inside the channel. Strong rejection means it closes beyond the inner edge of the touched zone while remaining inside the channel.

Breakout event: a selected sideways-state 15M candle closes outside its applicable channel boundary while the immediately preceding full-timeline 15M close was at or inside that boundary. Follow-up starts on the next 15M candle. The boundary is frozen at the breakout event. Outcomes are descriptive: any return inside during the horizon, whether the final close is inside, and maximum extension beyond the frozen boundary.

## Primary 10% boundary results

Candle counts are shown as touch candles / broad rejection candles / strong rejection candles. These are candle counts, not independent touch events.

### STRICT_P25

| Asset | Upper | Lower |
|---|---:|---:|
| BTC | 633 / 352 / 160 | 579 / 284 / 125 |
| ETH | 646 / 365 / 184 | 549 / 289 / 143 |
| SOL | 707 / 473 / 224 | 816 / 530 / 212 |
| DOGE | 684 / 439 / 206 | 525 / 323 / 150 |
| AVAX | 724 / 476 / 205 | 698 / 453 / 206 |

### BROAD_P40

| Asset | Upper | Lower |
|---|---:|---:|
| BTC | 907 / 517 / 207 | 809 / 440 / 205 |
| ETH | 871 / 497 / 241 | 828 / 449 / 208 |
| SOL | 936 / 603 / 290 | 1,177 / 741 / 294 |
| DOGE | 832 / 517 / 240 | 840 / 541 / 220 |
| AVAX | 1,008 / 731 / 314 | 896 / 562 / 250 |

## Breakout event counts and 12-hour follow-up

Events are detected upper/lower breakout starts. Returned inside is the proportion of tested events whose future 15M closes returned inside the frozen boundary at least once during the next 12 hours. Ended inside means the final close at the 12-hour horizon was inside. Median extension is the median event-level maximum future wick extension beyond the frozen boundary.

### STRICT_P25

| Asset | Upper events | Upper returned inside | Upper ended inside | Upper median extension | Lower events | Lower returned inside | Lower ended inside | Lower median extension |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 62 | 85.48% | 46.77% | 1.297% | 57 | 68.42% | 38.60% | 1.326% |
| ETH | 54 | 79.63% | 55.56% | 1.531% | 50 | 74.00% | 48.00% | 1.210% |
| SOL | 56 | 82.14% | 60.71% | 1.110% | 79 | 77.22% | 40.51% | 1.599% |
| DOGE | 67 | 85.07% | 52.24% | 1.119% | 53 | 69.81% | 47.17% | 1.824% |
| AVAX | 71 | 83.10% | 38.03% | 2.672% | 63 | 76.19% | 50.79% | 2.268% |

### BROAD_P40

| Asset | Upper events | Upper returned inside | Upper ended inside | Upper median extension | Lower events | Lower returned inside | Lower ended inside | Lower median extension |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 88 | 85.23% | 47.73% | 1.216% | 72 | 69.44% | 38.89% | 1.305% |
| ETH | 75 | 81.33% | 57.33% | 1.454% | 79 | 74.68% | 48.10% | 1.333% |
| SOL | 78 | 80.77% | 50.00% | 1.279% | 106 | 75.47% | 42.45% | 1.597% |
| DOGE | 81 | 82.72% | 53.09% | 1.247% | 72 | 70.83% | 43.06% | 1.910% |
| AVAX | 84 | 83.33% | 40.48% | 2.238% | 81 | 72.84% | 44.44% | 2.397% |

## Important implementation audit

The output contains a display/assignment bug in the episode summary: the lower-side strong-rejection episode count was printed in the upper-side line as well. Therefore, do not use the printed upper/lower strong-rejection episode ratios. The candle-level touch and rejection counts above are unaffected.

The episode helper groups by consecutive touch candles and confirmed 4H snapshot, but this implementation does not explicitly test timestamp continuity. If there are missing 15M bars, a gap between rows could be treated as consecutive. A future implementation should explicitly require a 15-minute timestamp step.

Breakout starts are detected against the current 4H snapshot boundary and the immediately preceding full-timeline close. Consecutive outside closes do not repeatedly trigger unless price first closes back at/inside and crosses again. Because the channel boundary can update every 4H, a boundary shift can itself affect the crossing test; future research should separate price crossing a frozen boundary from boundary movement.

The 12-hour follow-up is not a binary failure rate: an event may return inside and then extend outside again. The ended-inside measure helps distinguish temporary return from final location, but neither measure evaluates trade entry, stop placement, costs, or profitability. Event samples are modest and follow-up windows may overlap.

## Preliminary research conclusions

- The 10% zone provides a useful central comparison, but no zone width is established as optimal.
- Touches and closes back inside are common enough to justify further study; strong rejection is more selective.
- A return inside at least once is frequent after the sampled breakouts, but the final 12-hour location is materially different. Temporary re-entry should not be equated with a failed breakout.
- AVAX shows larger median maximum extension in several breakout groups, consistent with its higher observed movement scale, but the sample is limited.
- STRICT_P25 and BROAD_P40 produce broadly similar qualitative patterns, while BROAD_P40 selects more bars/events.
- These are retrospective descriptive findings only. Full-sample channel quantiles are not causal live thresholds. No strategy profitability is established.

## Next research correction

Before any strategy hypothesis is considered, rerun the episode summary with separate upper/lower counters and explicit 15-minute continuity checks. Then measure post-touch movement from the touch/rejection candle close over 1H, 4H, and 12H, including favourable and adverse excursion, and compare it with a matched non-touch baseline. Keep all work read-only and preserve chronological causality.
