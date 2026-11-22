# Original Breakout Event Reproduction Check — PASS

**Date:** 2026-11-22  
**Project:** Price Action V1  
**Branch:** `price-action-v1`  
**Status:** Accepted reproduction check; event-count gate passed  
**Scope:** Read-only reconstruction of the accepted timing-corrected breakout event masks. No matching, strategy testing, execution simulation, or profitability analysis.

## Result

All 20 accepted event counts were reproduced exactly across BTC, ETH, SOL, DOGE, and AVAX.

- Common synchronized 1-minute timestamps: **569,125**
- Non-consecutive intervals in the common timestamp index: **0**
- Complete 15-minute candles per asset: **37,941**
- Complete 4-hour candles per asset: **2,370**
- Validation: **20/20 PASS**

## Reproduced event counts

| Asset | Definition | Lower events | Upper events |
|---|---|---:|---:|
| BTC | Broad P40 | 91 | 115 |
| BTC | Strict P25 | 62 | 81 |
| ETH | Broad P40 | 87 | 77 |
| ETH | Strict P25 | 51 | 51 |
| SOL | Broad P40 | 117 | 96 |
| SOL | Strict P25 | 77 | 71 |
| DOGE | Broad P40 | 81 | 75 |
| DOGE | Strict P25 | 55 | 65 |
| AVAX | Broad P40 | 84 | 109 |
| AVAX | Strict P25 | 64 | 83 |

## Recomputed channel-width thresholds

Thresholds were recomputed dynamically from each asset's joined channel-width observations using the 25th and 40th percentiles. Values below are percentages.

| Asset | P25 | P40 |
|---|---:|---:|
| BTC | 3.242203 | 3.948630 |
| ETH | 4.242326 | 5.481886 |
| SOL | 5.067043 | 6.114542 |
| DOGE | 5.165724 | 6.264058 |
| AVAX | 5.703625 | 6.916216 |

These full-sample quantiles are retrospective exploratory thresholds, not live-calibrated thresholds.

## Event-definition integrity

The reproduction preserved the accepted final event masks:

- 48-hour context from 12 completed 4-hour candles.
- Sideways condition uses the selected channel-width percentile, directional efficiency ≤ 0.30, and mean overlap ≥ 0.70.
- A breakout requires the prior 15-minute close to be at or inside the frozen channel boundary and the current close to cross outside it.
- Both prior and current 15-minute observations must share the same 4-hour context snapshot.
- No additional previous-sideways requirement was introduced.
- No event de-clustering or cooldown was introduced.
- The 15-minute signal label is mapped to the final minute of its signal candle; follow-up begins at the next minute.
- Event eligibility for this reproduction check required the final signal minute to exist and at least 15 subsequent minute rows for the 15-minute follow-up.

## Interpretation and limitations

This PASS establishes that the accepted breakout event masks and event counts can be reconstructed from the available five-asset dataset using the recorded method.

It does **not** validate:
- matched-control candidate construction or matching quality;
- feature balance or standardized mean differences;
- follow-up outcome calculations;
- statistical significance or uncertainty;
- fills, fees, slippage, funding, or executable trading performance;
- strategy profitability or a tradable edge;
- original exchange/API provenance of the underlying 1-minute data.

The small differences between these dynamically recomputed thresholds and earlier rounded/reference values for ETH, SOL, and AVAX do not affect the event-count reproduction: all 20 counts match exactly.

## Next gate

Proceed to code review of the replacement matched-control script. Do not interpret matched-control results until its implementation is reviewed and the script passes its own validation checks. This reproduction run itself was read-only and wrote no local files.
