# Breakout Feature Formula Diagnostic V2 — Runtime Results

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** completed; 0/20 exact matches in all four variants  
**Research gate:** matched-control study remains HOLD.

## Runtime integrity

User ran:

```bash
git pull --ff-only origin price-action-v1
python research/validation/breakout_event_feature_formula_diagnostic_v2.py
```

Pull fast-forwarded local branch from `14eb5c3` to `662e8e2`. The diagnostic completed without runtime error.

- Common synchronized 1M timestamps: 569,125.
- Each asset: 2,359 joined feature rows for ER11 variants; 2,358 for ER12 variants.
- Joined-15M width quantiles reproduced the historical threshold values to displayed precision for all five assets.
- No controls, forward outcomes, matching, or profitability calculations were run.
- Script states no files were written or modified.

## Exact event-count results

Expected count order in each row below is the historical reference. Actual results are listed as `actual / expected`.

| Asset | Variant | P25 upper | P25 lower | P40 upper | P40 lower |
|---|---|---:|---:|---:|---:|
| BTC | ER11, strict overlap | 63/81 | 52/62 | 85/115 | 70/91 |
| ETH | ER11, strict overlap | 48/51 | 43/51 | 61/77 | 68/87 |
| SOL | ER11, strict overlap | 53/71 | 69/77 | 71/96 | 93/117 |
| DOGE | ER11, strict overlap | 57/65 | 45/55 | 63/75 | 62/81 |
| AVAX | ER11, strict overlap | 66/83 | 63/64 | 83/109 | 81/84 |
| BTC | ER11, available overlap | 63/81 | 52/62 | 85/115 | 70/91 |
| ETH | ER11, available overlap | 48/51 | 43/51 | 61/77 | 68/87 |
| SOL | ER11, available overlap | 53/71 | 69/77 | 71/96 | 93/117 |
| DOGE | ER11, available overlap | 57/65 | 45/55 | 63/75 | 62/81 |
| AVAX | ER11, available overlap | 66/83 | 63/64 | 83/109 | 81/84 |
| BTC | ER12, strict overlap | 60/81 | 54/62 | 84/115 | 69/91 |
| ETH | ER12, strict overlap | 47/51 | 46/51 | 67/77 | 75/87 |
| SOL | ER12, strict overlap | 53/71 | 76/77 | 74/96 | 102/117 |
| DOGE | ER12, strict overlap | 62/65 | 52/55 | 73/75 | 71/81 |
| AVAX | ER12, strict overlap | 66/83 | 63/64 | 77/109 | 79/84 |
| BTC | ER12, available overlap | 60/81 | 54/62 | 84/115 | 69/91 |
| ETH | ER12, available overlap | 47/51 | 46/51 | 67/77 | 75/87 |
| SOL | ER12, available overlap | 53/71 | 76/77 | 74/96 | 102/117 |
| DOGE | ER12, available overlap | 62/65 | 52/55 | 73/75 | 71/81 |
| AVAX | ER12, available overlap | 66/83 | 63/64 | 77/109 | 79/84 |

**Exact matches: 0/20 in every variant.**

## Interpretation

1. Neither tested directional-efficiency lookback reproduces the historical event population.
2. Strict versus available-pair overlap produced identical event counts in this run. This makes overlap handling a lower-priority explanation for this dataset/implementation, but does not establish general equivalence of the formulas.
3. P25/P40 width thresholds remain consistent with the historical reference to displayed precision. The unresolved discrepancy is therefore not explained by the tested quantile population/threshold values alone.
4. The counts are not uniformly lower in every cell: some ER12 lower-direction counts move closer to the historical reference, while upper counts and several broad counts remain different. No variant is accepted.
5. The archived historical 20-count PASS remains a record of previously reported results, not an independently reproduced result.

## Next investigation priority

Do not keep varying efficiency and overlap formulas blindly. Inspect the exact 4H feature-to-15M availability convention and the sideways predicate construction in the archived script versus the historical detector, including:
- whether each 4H row is indexed by candle open or candle close;
- whether the 12-bar channel includes the current completed 4H candle or ends at the prior one;
- whether the 4H feature row is joined to the 15M candle by its start, close, or next-available timestamp;
- exact null/valid-row handling for each predicate before the width quantile is computed;
- whether the quantile population includes only rows with all other sideways features valid.

A new diagnostic must isolate one documented source difference at a time, print feature-row and event-count effects, and must not tune to expected counts.

## Decision

- Matched-control construction: **HOLD**.
- Forward outcome calculations: **HOLD**.
- Historical expected counts: unchanged.
- No parameter or formula selected based on count matching.
- Preserve all prior scripts and reports unchanged.
