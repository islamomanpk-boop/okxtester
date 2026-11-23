# Breakout historical ER formula diagnostic V3 — runtime results and hold

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Script:** `research/validation/breakout_event_historical_er_formula_diagnostic_v3.py`  
**Status:** Diagnostic only; event reproduction remains on HOLD.

## Purpose

Test whether the historical sideways detector's exact 12-change absolute-price directional-efficiency formula explains the mismatch between the accepted historical breakout-event count table and the current independent reconstruction.

V3 compared:
1. `ARCHIVED_ER11_PERCENT`: archived 11-change percentage-return efficiency formula.
2. `HISTORICAL_ER12_ABSOLUTE_PRICE`: historical detector formula, `abs(close - close.shift(12)) / close.diff().abs().rolling(12).sum()`.

Overlap used the available-valid-adjacent-pair mean. Both variants used common 1-minute timestamps, complete epoch-aligned 15m/4h candles, a 12-bar channel, joined-15m P25/P40 quantiles, backward as-of feature availability, same-snapshot crossing masks, and no previous-sideways requirement. This was read-only.

## Runtime environment checks

- Common synchronized 1m timestamps: **569,125**.
- Archived ER11 feature rows: **2,359 per asset**.
- Historical ER12 absolute-price feature rows: **2,358 per asset**.

Both formulas returned the same dynamically computed thresholds:

| Asset | P25 | P40 |
|---|---:|---:|
| BTC | 3.242203251% | 3.948630141% |
| ETH | 4.242326420% | 5.481886231% |
| SOL | 5.067043049% | 6.114541712% |
| DOGE | 5.165724421% | 6.264057580% |
| AVAX | 5.703624733% | 6.916215821% |

## Archived ER11 percentage formula — actual vs historical expected

| Asset | P25 upper | P25 lower | P40 upper | P40 lower |
|---|---:|---:|---:|---:|
| BTC | 63 / 81 | 52 / 62 | 85 / 115 | 70 / 91 |
| ETH | 48 / 51 | 43 / 51 | 61 / 77 | 68 / 87 |
| SOL | 53 / 71 | 69 / 77 | 71 / 96 | 93 / 117 |
| DOGE | 57 / 65 | 45 / 55 | 63 / 75 | 62 / 81 |
| AVAX | 66 / 83 | 63 / 64 | 83 / 109 | 81 / 84 |

**Exact matches: 0/20.**

## Historical ER12 absolute-price formula — actual vs historical expected

| Asset | P25 upper | P25 lower | P40 upper | P40 lower |
|---|---:|---:|---:|---:|
| BTC | 60 / 81 | 54 / 62 | 84 / 115 | 69 / 91 |
| ETH | 47 / 51 | 46 / 51 | 67 / 77 | 75 / 87 |
| SOL | 53 / 71 | 76 / 77 | 74 / 96 | 102 / 117 |
| DOGE | 62 / 65 | 52 / 55 | 73 / 75 | 71 / 81 |
| AVAX | 66 / 83 | 63 / 64 | 77 / 109 | 79 / 84 |

**Exact matches: 0/20.**

In the tables, each cell is `actual / historical expected`.

## Interpretation

1. The exact historical 12-change absolute-price ER formula does **not** resolve the event-count discrepancy under the tested reconstruction.
2. The archived 11-change percentage formula also remains inconsistent.
3. Both variants reproduce the same displayed P25/P40 thresholds, but their event counts differ. Threshold agreement alone is not evidence that the full event engine has been reproduced.
4. The V3 test does not establish that every possible historical feature-alignment, channel-window, quantile-population, candle-label, or input-data choice has been ruled out.
5. The historical 20/20 count table remains a record of the previously reported result, not an independently reproduced result.

## Gate decision

**HOLD — do not construct matched controls or calculate forward outcomes.**

No controls, matching, forward outcomes, inference, entries/exits, costs, or profitability calculations were run. V3 wrote no data files and modified no source data.

## Next source-audit priorities

Continue recovering the exact historical producer and contemporaneous run evidence if available. Otherwise, inspect and test source-grounded alternatives one at a time, without tuning to target counts:
- 4h candle label and feature-availability timestamp mapping to 15m observations;
- whether the 12-bar channel includes the current completed 4h candle or ends at the prior candle;
- the exact population used to calculate P25/P40 (including complete/valid predicate availability);
- null-row handling and feature alignment;
- exact 15m signal timestamp mapping and crossing-mask implementation;
- historical raw-input identity, file hashes, and contemporaneous run logs.

Any new reconstruction must be versioned, retain prior diagnostics, and report all 20 counts before any control/outcome work. A match must follow from recovered source/methodology, not parameter tuning.

## Reproduction record

User ran:

```bash
cd ~/okxtester || exit 1
git pull --ff-only origin price-action-v1
python research/validation/breakout_event_historical_er_formula_diagnostic_v3.py
```

The pull fast-forwarded to the commit containing V3 and its methodology checkpoint. Runtime output reported **0/20 exact matches for each of the two formulas**, and explicitly reported that no controls, forward outcomes, matching, or profitability calculations were performed and no files were written or modified.
