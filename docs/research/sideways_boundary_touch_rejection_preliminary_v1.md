# Sideways Boundary Touch and Rejection — Preliminary Results (2026-11-22)

## Scope and method
Read-only descriptive calculation on the five existing 1-minute datasets, inner-joined on common timestamps (569,125 common minute candles). Resampled to 2,370 complete 4H candles and 37,941 complete 15M candles per asset. The exploratory 48H sideways labels used existing strict P25 and broad P40 channel-width thresholds, directional efficiency <= 0.30 and average adjacent-candle overlap >= 0.70. 4H feature timestamps were shifted to the 4H close before mapping to 15M bars.

Boundary zones tested: outermost 5%, 10%, and 15% of each channel. A touch candle's high/low entered the relevant zone. A counted rejection candle touched the zone and closed within the channel. Ratios are candle counts, not independent visits or trade win rates.

## 10% zone results (strict P25)
| Asset | Upper touch candles | Upper closes inside | Upper ratio | Lower touch candles | Lower closes inside | Lower ratio |
| BTC | 633 | 352 | 55.61% | 579 | 284 | 49.05% |
| ETH | 646 | 365 | 56.50% | 549 | 289 | 52.64% |
| SOL | 707 | 473 | 66.90% | 816 | 530 | 64.95% |
| DOGE | 684 | 439 | 64.18% | 525 | 323 | 61.52% |
| AVAX | 724 | 476 | 65.75% | 698 | 453 | 64.90% |

## 10% zone results (broad P40)
| Asset | Upper touch candles | Upper closes inside | Upper ratio | Lower touch candles | Lower closes inside | Lower ratio |
| BTC | 907 | 517 | 57.00% | 809 | 440 | 54.39% |
| ETH | 871 | 497 | 57.06% | 828 | 449 | 54.23% |
| SOL | 936 | 603 | 64.42% | 1,177 | 741 | 62.96% |
| DOGE | 832 | 517 | 62.14% | 840 | 541 | 64.40% |
| AVAX | 1,008 | 731 | 72.52% | 896 | 562 | 62.72% |

## 5%, 10%, 15% sensitivity
Across assets and both state definitions, the reported candle-level rejection ratio generally rises with wider zones. This is expected because a wider zone captures more candles. Therefore 10% is retained as a practical primary descriptive definition, with 5% and 15% as sensitivity checks, not because the data proves 10% is optimal.

## Preliminary breakout output — not accepted as final
The initial script printed 12-hour return-inside rates for first outside closes. Illustrative strict P25 upper-side values were BTC 85.25%, ETH 78.85%, SOL 81.82%, DOGE 86.36%, AVAX 83.10%. These are not accepted as reliable failed-breakout estimates because event-start logic used a shifted series after filtering to selected sideways rows. Selected rows can be separated in time, so the previous row in that filtered frame may not be the immediately preceding 15M candle. Event identification must be rebuilt on the full continuous 15M timeline, with explicit previous-bar state and frozen boundary per event.

## Methodological limitations and next correction
1. Touch and rejection counts are 15M candle counts. Consecutive touches cluster; the printed episode count is a simple consecutive-true run count over filtered selected rows, which can join bars separated by non-selected intervals. It must not be interpreted as true touch episodes.
2. The rejection ratio is not the probability that a boundary visit reverses. A stricter rejection definition should require a touch of the outer zone followed by a close back beyond the inner edge of that zone, while still inside the channel. Report both close-inside and close-beyond-zone variants.
3. Rebuild touch episodes on the full 15M timeline, splitting episodes at non-selected periods and at channel-confirmation updates, and freeze each confirmed channel boundary for its subsequent 4H segment.
4. Rebuild breakout events on the full timeline. Define an event as the first 15M close outside the active frozen boundary after the immediately previous 15M close was inside. De-cluster until re-entry or a stated timeout. Track future 1H/4H/12H outcomes from the next 15M candle, even if the sideways label later turns off. Report sample counts and incomplete tail exclusions.
5. Full-sample channel quantiles are retrospective exploratory thresholds, not live/causal thresholds.
6. Results are descriptive, not evidence of strategy profitability. No fees, spread, slippage, funding, liquidity or order execution modelled. Data provenance is not independently verified.

## Decision
Keep 10% outer channel zone as the primary descriptive boundary-touch definition, with 5% and 15% sensitivity comparisons. Do not use the initial breakout return-inside percentages as findings. Next research step is a corrected full-timeline event study with stricter rejection variants, properly clustered touch episodes, and de-clustered breakout events.

No local files were written or changed by the calculation.