# Sideways-channel breakout and retest: final timing-corrected empirical results (V1)

**Study status:** descriptive, read-only research; not a strategy backtest.  
**Assets:** BTC, ETH, SOL, DOGE, AVAX.  
**Common 1-minute timestamps:** 569,125.  
**Complete candles per asset:** 37,941 15M and 2,370 4H.

## Method

- Sideways context uses the prior 12 completed 4H candles (48 hours): channel width, directional efficiency, and adjacent-candle overlap.
- Strict definition: channel width at or below full-sample P25, directional efficiency <= 0.30, overlap >= 0.70.
- Broad definition: channel width at or below full-sample P40, directional efficiency <= 0.30, overlap >= 0.70.
- Full-sample P25/P40 thresholds are retrospective exploratory cutoffs, not live-calibrated thresholds.
- Breakout is a 15M close beyond the relevant 48H channel boundary; the first 15M candle after a new 4H context snapshot is suppressed.
- 15M close labels are mapped to the final 1M candle within that 15M candle (timestamp = signal close label minus one minute). Follow-up begins at the next 1M candle open.
- Follow-up horizons: 15M, 1H, 4H, 12H. Only complete horizons are retained.
- Retest band approach and actual crossing of the original boundary are measured separately. Retest hold is assessed at the next completed 15M close after retest, when that confirmation falls within the horizon.
- No files/data were changed by the local calculation.

## Breakout event counts

| Asset | Broad lower | Broad upper | Strict lower | Strict upper |
|---|---:|---:|---:|---:|
| BTC | 91 | 115 | 62 | 81 |
| ETH | 87 | 77 | 51 | 51 |
| SOL | 117 | 96 | 77 | 71 |
| DOGE | 81 | 75 | 55 | 65 |
| AVAX | 84 | 109 | 64 | 83 |

## Broad P40: 12-hour follow-up summary

All values are percentages except median MFE/MAE, which are percentage price excursions. MFE is favourable excursion in breakout direction; MAE is adverse excursion. "Returned inside" means price entered the original channel at least once during the horizon. "Ended inside" means the horizon's ending close was inside.

| Asset | Direction | Median MFE | Median MAE | Returned inside | Ended inside | Band approach | Boundary penetration | Median first approach (min) | Retest hold* |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | Lower | 1.0195 | -0.7735 | 81.32 | 42.86 | 85.71 | 13.19 | 9 | 78.21 |
| BTC | Upper | 1.0564 | -0.7643 | 91.30 | 51.30 | 90.43 | 9.57 | 6 | 67.31 |
| ETH | Lower | 1.0224 | -1.1622 | 79.31 | 50.57 | 80.46 | 10.34 | 12 | 77.14 |
| ETH | Upper | 1.2748 | -1.4900 | 90.91 | 53.25 | 94.81 | 18.18 | 8 | 73.97 |
| SOL | Lower | 1.3245 | -1.2350 | 87.18 | 44.44 | 89.74 | 11.97 | 8 | 65.71 |
| SOL | Upper | 1.0167 | -1.4609 | 85.42 | 47.92 | 90.63 | 16.67 | 6 | 68.97 |
| DOGE | Lower | 1.6602 | -1.1009 | 82.72 | 40.74 | 88.89 | 12.35 | 6.5 | 62.50 |
| DOGE | Upper | 1.4912 | -1.1946 | 86.67 | 46.67 | 90.67 | 21.33 | 10.5 | 67.65 |
| AVAX | Lower | 1.8926 | -1.4659 | 79.76 | 44.05 | 84.52 | 26.19 | 12 | 59.15 |
| AVAX | Upper | 1.3983 | -1.4992 | 88.07 | 52.29 | 83.49 | 21.10 | 10 | 59.34 |

*Retest hold is conditional on retests with a valid next-15M-close confirmation inside the horizon. It is not a percentage of all breakout events.*

## Key interpretation

1. Breakouts often extend and revisit the old channel during the same 12-hour period. These are not contradictory: MFE records the best favourable excursion at any time, while returned-inside records whether price later/also re-entered the channel.
2. For broad P40, 12H median MFE is positive in every asset/direction, ranging from about 1.02% to 1.89% in the displayed table. These are excursions, not realized trade returns.
3. Broad P40 12H return-inside rates range from 79.31% to 91.30%. Ending-inside rates are lower (40.74% to 53.25%); a temporary re-entry does not mean the final close remained inside.
4. Band approaches are frequent (about 83.49% to 94.81% by 12H in broad P40), while actual original-boundary penetration is much less frequent (about 9.57% to 26.19%).
5. Median penetration depth is zero in the supplied output because the median is taken across all events, including band approaches that do not cross the original boundary. This is compatible with a nonzero penetration percentage.
6. Strict P25 and broad P40 results are directionally similar in many respects; neither definition establishes a reliable breakout or retest edge.
7. Retest-hold rates are conditional and should not be compared with all-event breakout rates as if they shared a denominator.

## Timing correction and quality notes

An earlier version aligned the 15M close label directly to a 1M opening timestamp, shifting the follow-up start. This final version corrects the mapping: the final 1M candle inside the signal is at signal close label minus one minute, and follow-up begins at the next 1M candle. The first follow-up minute is included in retest search. Earlier breakout/retest outputs are superseded and should not be treated as final.

## Limitations

- Full-sample channel-width quantiles are retrospective and not suitable as live thresholds without chronological calibration.
- Rolling 48H contexts overlap; event observations are not independent.
- MFE/MAE and channel re-entry do not establish executable fills or profitability.
- No stop/target collision ordering, order-book liquidity, fees, slippage, funding, partial fills, or position sizing are modeled.
- Retest hold is a descriptive close-location condition, not a tested trade outcome.
- The source provenance and exact instrument identity of the local 1M CSVs remain unverified independently.

## Research conclusion

The five-asset sample supports a descriptive picture of **post-breakout extension coexisting with substantial channel re-entry**. Retests are common as approaches, but actual penetration of the old boundary is much less common. Cross-asset differences exist, but the results do not justify a trading rule or profitability claim. Any later strategy test must be a separate, explicitly authorized, causal test with realistic execution costs and chronological out-of-sample evaluation.
