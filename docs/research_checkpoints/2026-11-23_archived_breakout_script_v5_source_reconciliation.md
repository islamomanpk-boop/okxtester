# Archived breakout script source reconciliation after V5

Date: 2026-11-23  
Branch: `price-action-v1`  
Inspected source: `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh`  
Related runtime: `research/validation/breakout_event_previous_selected_gate_diagnostic_v5.py`  
Status: historical event reproduction remains HOLD.

## Source facts confirmed by inspection

The archived script:
- Loads the five 1-minute asset files, intersects timestamps across assets, and builds each asset's 4H and 15M bars from that common 1-minute index.
- Resamples with `origin="epoch"`, `label="left"`, `closed="left"`, requiring 240 1-minute observations for a complete 4H candle and 15 for a complete 15M candle.
- Builds the 48-hour channel from 12 completed 4H bars.
- Calculates the historical ER12 absolute-price formula using the close change over 12 bars divided by the rolling sum of 12 absolute close changes.
- Calculates overlap as the rolling mean of 11 adjacent valid-pair overlaps.
- Drops rows with missing feature values before calculating P25/P40 width quantiles on the unique 4H feature rows.
- Marks each feature snapshot available at its 4H bar start plus four hours, then maps it backward-as-of to 15M bar-start timestamps.
- Uses `selected & previous_selected & same_snapshot` as the event eligibility gate.
- Applies the upper/lower crossing test against the current frozen channel boundary, using the prior 15M close for the crossing condition.

## Reconciliation with V5

V5 explicitly tested the archived `previous_selected` gate against the current-selected-only mask, with both unique-4H and joined-15M quantile populations. All four combinations returned identical event counts and 0/20 matches to the historical expected counts.

The archived source uses the unique-4H quantile population. V5's unique-4H thresholds were:
- BTC: P25 3.242203251%, P40 3.947937289%.
- ETH: P25 4.245214260%, P40 5.474563343%.
- SOL: P25 5.067174178%, P40 6.114541712%.
- DOGE: P25 5.165724421%, P40 6.264057580%.
- AVAX: P25 5.704867571%, P40 6.916215821%.

These differ from several thresholds recorded in the historical accepted checkpoint, which often correspond to the joined-15M population. However, V5 demonstrated that switching quantile population did not change any of the 20 reconstructed event counts in this diagnostic.

## Interpretation

The archived script's visible event gate is now tested and does not explain the historical count discrepancy. Its unique-4H quantile population also does not explain the count discrepancy. The archived script as currently stored therefore does not independently reproduce or substantiate the historical accepted 20-count table.

This is a source-provenance finding, not proof that the historical run never occurred. The contemporaneous source/version and output that produced the historical counts remain unidentified.

## Next action

Do not run the archived full study as a substitute for resolving event provenance; it includes forward-outcome calculations and is not a read-only event-count-only audit. Recover the historical run's exact script revision, command, and captured output/log, preferably from Git history or saved conversation artifacts. If unavailable, establish a new explicitly versioned event engine and report its counts as new results rather than altering rules to force the historical table.

## Research restriction

**HOLD:** no matched controls, matching, forward outcomes, inference, or profitability work until event provenance and counts are reconciled or a new event engine is formally accepted with transparent versioning.
