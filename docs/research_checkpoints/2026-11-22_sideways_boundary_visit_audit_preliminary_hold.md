# Sideways Boundary Visit Audit — Preliminary Hold

**Date:** 2026-11-22  
**Status:** PRELIMINARY AUDIT ONLY — NOT ACCEPTED AS FINAL REJECTION EVENT COUNTS  
**Scope:** BTC, ETH, SOL, DOGE, AVAX; 15M observations inside strict P25 and broad P40 48H sideways contexts.  
**Execution:** Read-only calculation on existing 1M CSVs. No local files were written or changed. No strategy backtest or profitability analysis was run.

## Data and context checks

- Common 1M timestamps: 569,125.
- Non-consecutive intervals in the common 1M timeline: 0.
- Each asset: 37,941 complete 15M bars and 2,370 complete 4H bars.
- Dynamic channel-width thresholds reproduced:
  - BTC P25 3.242203%, P40 3.948630%.
  - ETH P25 4.242326%, P40 5.481886%.
  - SOL P25 5.067043%, P40 6.114542%.
  - DOGE P25 5.165724%, P40 6.264058%.
  - AVAX P25 5.703625%, P40 6.916216%.

## Preliminary results

Counts below are **touch visits / visits containing at least one strong rejection**. In this run, touch visits equal touch candles in every group, meaning every detected touch was an isolated 15M candle under the current visit definition.

| Asset | Strict upper | Strict lower | Broad upper | Broad lower |
|---|---:|---:|---:|---:|
| BTC | 974 / 174 | 960 / 112 | 1364 / 225 | 1365 / 189 |
| ETH | 923 / 189 | 883 / 146 | 1262 / 241 | 1356 / 197 |
| SOL | 958 / 168 | 1222 / 190 | 1280 / 215 | 1793 / 279 |
| DOGE | 940 / 196 | 889 / 162 | 1138 / 221 | 1360 / 252 |
| AVAX | 1058 / 193 | 1064 / 206 | 1453 / 295 | 1383 / 240 |

The reported first/second/third/fourth-or-later strong rejection counts by visit number are descriptive counts within each 4H snapshot, aggregated across the sample. They are not independent observations or evidence that later tests are more/less likely to reject.

## Important limitations and reconciliation hold

1. The touch definition is a wick entering the outer 10% channel zone. A visit ends at the first non-touch 15M candle, a timestamp gap, or a changed 4H snapshot. Because every touch was isolated, this run did not demonstrate multi-candle visit grouping.
2. The strong rejection definition requires the close to move back beyond the inner edge of the 10% boundary zone while remaining inside the opposite channel boundary.
3. The resulting strong-rejection counts equal the earlier candidate rejection-candle counts, but differ materially from the older 1M-follow-up report references:
   - BTC strict upper/lower 174/112 vs 105/90; broad 225/189 vs 135/134.
   - ETH strict 189/146 vs 97/91; broad 241/197 vs 133/126.
   - SOL strict 168/190 vs 139/129; broad 215/279 vs 177/177.
   - DOGE strict 196/162 vs 121/90; broad 221/252 vs 147/132.
   - AVAX strict 193/206 vs 131/127; broad 295/240 vs 192/158.
4. These older counts are not acceptance targets. The difference remains unexplained. Do not treat either set as the definitive accepted rejection event population until the old event definitions and timestamp mapping are reconciled.
5. The visit number resets within each 4H snapshot. Aggregated visit-number counts are not independent samples; many observations share the same context and market period.
6. No post-signal outcomes, retest performance, fees, fills, or profitability were calculated.

## Next required work

Before accepting the event cohort, audit the visit structure and reconcile the older report's exact touch/rejection masks, 4H snapshot handling, and 15M-to-1M event timestamp mapping. Then freeze the event definitions and perform the dedicated post-rejection path study with exact 1M continuity checks and explicit denominators.

**Conclusion:** Preliminary diagnostic only. No strategy or trading conclusion is supported.
