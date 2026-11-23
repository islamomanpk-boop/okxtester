# Breakout previous-selected gate diagnostic V5 — runtime results

Date: 2026-11-23  
Branch: `price-action-v1`  
Script: `research/validation/breakout_event_previous_selected_gate_diagnostic_v5.py`  
Status: diagnostic completed; historical event reproduction remains HOLD.

## Purpose

Test whether the archived breakout/retest event mask's previous-selected requirement explains the discrepancy between the historical accepted event counts and independently reconstructed counts. The diagnostic crossed two quantile populations with two event-mask variants:

1. Unique 4H feature rows + current-selected and same-snapshot mask.
2. Unique 4H feature rows + archived previous-selected gate.
3. Joined 15M rows + current-selected and same-snapshot mask.
4. Joined 15M rows + archived previous-selected gate.

The calculation used the exact historical ER12 absolute-price formula, 12-bar channel, available-valid-pair overlap, 4H feature availability at close, backward as-of 15M mapping, efficiency <= 0.30, overlap >= 0.70, and same-snapshot condition. No thresholds or masks were tuned to target the expected counts.

## Runtime integrity

- Common 1-minute timestamps: 569,125.
- Unique 4H feature rows: 2,358 per asset.
- Joined 15M rows: 37,721 per asset.
- Script completed and reported read-only behavior.
- No controls, forward outcomes, matching, inference, or profitability calculations were performed.
- No files were written or modified by the diagnostic.

## Quantile thresholds

Percentages:

| Asset | Unique 4H P25 | Unique 4H P40 | Joined 15M P25 | Joined 15M P40 |
|---|---:|---:|---:|---:|
| BTC | 3.242203251 | 3.947937289 | 3.242203251 | 3.948630141 |
| ETH | 4.245214260 | 5.474563343 | 4.242326420 | 5.481886231 |
| SOL | 5.067174178 | 6.114541712 | 5.067043049 | 6.114541712 |
| DOGE | 5.165724421 | 6.264057580 | 5.165724421 | 6.264057580 |
| AVAX | 5.704867571 | 6.916215821 | 5.703624733 | 6.916215821 |

## Event counts

All four combinations returned the same counts. The table below records those counts once; the historical expected counts are shown for comparison.

| Asset | Definition | Upper actual | Upper expected | Lower actual | Lower expected |
|---|---|---:|---:|---:|---:|
| BTC | P25 | 60 | 81 | 54 | 62 |
| BTC | P40 | 84 | 115 | 69 | 91 |
| ETH | P25 | 47 | 51 | 46 | 51 |
| ETH | P40 | 67 | 77 | 75 | 87 |
| SOL | P25 | 53 | 71 | 76 | 77 |
| SOL | P40 | 74 | 96 | 102 | 117 |
| DOGE | P25 | 62 | 65 | 52 | 55 |
| DOGE | P40 | 73 | 75 | 71 | 81 |
| AVAX | P25 | 66 | 83 | 63 | 64 |
| AVAX | P40 | 77 | 109 | 79 | 84 |

Exact historical matches:
- Unique 4H + current-selected: 0/20.
- Unique 4H + archived previous-selected: 0/20.
- Joined 15M + current-selected: 0/20.
- Joined 15M + archived previous-selected: 0/20.

## Interpretation

1. Adding the archived previous-selected requirement did not change any event count in this implementation and dataset.
2. Switching between unique 4H and joined 15M quantile populations changed some threshold values slightly, but did not change any event count.
3. Neither candidate explains the historical count discrepancy.
4. The 20 historical expected counts remain an archival record of previously reported results, not an independently reproduced result.
5. The original event engine's exact source/provenance remains unresolved.

## Research decision

**HOLD — do not construct matched controls or calculate forward outcomes, matching, inference, or profitability.** First recover the exact contemporaneous script/command/output that produced the historical counts, or transparently establish a new versioned event engine and document its differences. Do not tune thresholds, masks, or feature rules to force a match.

## Next audit direction

Continue source-provenance and event-construction audit rather than another arbitrary parameter sweep. Inspect the archived script's complete data preparation and timestamp mapping against the exact historical run; identify any differences in the 15-minute series construction, feature availability/join behavior, valid-row filtering, and signal timestamp convention. Preserve each diagnostic and its result separately.
