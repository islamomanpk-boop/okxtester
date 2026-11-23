# Matched-Control Rebuild — Event Gate Runtime Failure V1

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** HOLD — event reconstruction not validated; matching prohibited  
**Runtime:** user's Termux environment  
**Script:** `research/matched_controls/matched_control_event_gate_v1.py`

## Runtime result

The user pulled commit `14eb5c3` and ran the event gate against the five-asset source data.

Data checks:
- Common synchronized 1M timestamps: 569,125 — PASS.
- Common timestamp continuity: every interval exactly one minute — PASS.
- Complete 4H bars: 2,370 per asset — passed script's guard.
- Complete 15M bars: 37,941 per asset — passed script's guard.
- Dynamically recomputed joined-15M width quantiles reproduce the documented accepted thresholds to the displayed precision.

Thresholds (%):

| Asset | P25 | P40 |
|---|---:|---:|
| BTC | 3.242203251 | 3.948630141 |
| ETH | 4.242326420 | 5.481886231 |
| SOL | 5.067043049 | 6.114541712 |
| DOGE | 5.165724421 | 6.264057580 |
| AVAX | 5.703624733 | 6.916215821 |

## Event count comparison

| Asset | Broad lower actual/expected | Broad upper actual/expected | Strict lower actual/expected | Strict upper actual/expected |
|---|---:|---:|---:|---:|
| BTC | 70/91 | 85/115 | 52/62 | 63/81 |
| ETH | 68/87 | 61/77 | 43/51 | 48/51 |
| SOL | 93/117 | 71/96 | 69/77 | 53/71 |
| DOGE | 62/81 | 63/75 | 45/55 | 57/65 |
| AVAX | 81/84 | 83/109 | 63/64 | 66/83 |

**Validation: 0/20.** The script stopped before control construction and outcome calculations, as designed.

## Interpretation — important correction

This is not a new finding that candle-label alignment alone caused the discrepancy. The accepted-source conflict checkpoint `2026-11-23_breakout_event_reproduction_conflict_hold.md` already recorded that the prior independent diagnostic produced 0/20 for both unique-4H and joined-15M quantile populations, with both accepted-mask and archived-mask variants. It explicitly concluded that the exact producing source/method was unresolved.

The new gate independently confirms that the current reconstructed joined-15M implementation still does not reproduce the historical 20-count reference. Threshold agreement is not sufficient to establish event-mask agreement.

The earlier `2026-11-22_original_breakout_event_reproduction_pass.md` is retained as a record of the historical reported PASS, but it must not be treated as independently verified evidence until the producing source and contemporaneous output are recovered or the methodology is transparently re-established.

## Research hold

- Do not construct matched controls from these 0/20 events.
- Do not change filters, thresholds, candle labels, or timing merely to force the expected counts.
- Do not treat the prior 1,290 pairs as accepted evidence.
- Keep this failed runtime output as a debugging/audit record, not an empirical result.

## Next action

Resolve the original event-engine specification/source discrepancy before matched controls. The audit must explicitly enumerate and test the remaining plausible differences in:
1. exact completed-candle construction and 15M label convention;
2. 4H feature row availability and snapshot join key;
3. joined quantile population and null-row handling;
4. exact directional-efficiency and adjacent-overlap rolling-window alignment;
5. event timestamp interpretation and prior/current close selection;
6. accepted source data version and contemporaneous output provenance.

Any candidate variant must be justified from source/method evidence, not selected because it happens to match counts. Once the event engine is established, freeze it, add unit tests, reproduce the accepted counts if justified, and only then resume matched-control construction.

## Preservation

The failed run is intentionally preserved. It is not a reason to overwrite the original script or alter the accepted historical checkpoint.
