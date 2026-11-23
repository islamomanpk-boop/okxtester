# Historical breakout report versus recovered source — reconciliation

Date: 2026-11-23  
Branch: `price-action-v1`  
Status: event engine remains HOLD.

## Historical artifacts compared

1. `docs/research/sideways_breakout_retest_timing_corrected_empirical_results_v1.md`
2. `docs/research_checkpoints/2026-11-22_original_breakout_event_reproduction_pass.md`
3. `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh`
4. `docs/research_checkpoints/2026-11-23_breakout_previous_selected_gate_diagnostic_v5_runtime_results.md`

## Confirmed facts

- The empirical-results report records the same 20 breakout event counts as the 2026-11-22 reproduction PASS checkpoint.
- The PASS checkpoint records joined-15M width quantiles and an event mask without an additional previous-sideways requirement.
- The recovered 506-line archived script calculates width quantiles from unique 4H feature rows and uses `selected & previous_selected & same_snapshot`.
- V5 tested unique-4H and joined-15M quantile populations, each with and without the archived previous-selected gate. All four combinations produced 0/20 exact matches to the historical table.
- The Git history for the archived script shows only its preservation commit (`61f87be`); that is when this archived file was added to the repository, not evidence of a historical source revision that generated the report.
- The empirical-results report's original commit (`9dbd53c4e3c499eccbe71fec87c73671e553f4f8`) added the report only; the source-recovery status checkpoint records that the full producing Python code was not included in that commit.

## Important distinction

The recovered archived script is a preserved source artifact, but it has not been shown to be the exact code that generated the historical report's 20 event counts. The report and accepted PASS checkpoint preserve the historical counts and methodology summary, but do not provide the complete event-producing implementation.

The separate `research/sideways_boundary_events_historical_v1.py` implementation reconstructs repeated boundary-touch tests and first strong rejections. It is a different event study and cannot be substituted for the breakout/retest event-count engine. Its 6/6 integrity pass validates its own ledger only.

## Interpretation

There are at least two distinct source/method descriptions in the repository:
- the historical accepted breakout baseline: joined-15M quantiles, no extra previous-sideways gate, expected counts as in the empirical-results report;
- the recovered archived script: unique-4H quantiles and a previous-selected gate.

Neither the V5 reconstruction variants nor the archived source currently substantiate the historical 20-count table. Do not describe the recovered script as the verified producer of those counts.

## Required next action

Recover the exact code from the original 2026-11-22 conversation or another contemporaneous artifact that generated the report. Preserve it verbatim as a separate file if found. If it cannot be recovered, create a new versioned event engine from a frozen specification and clearly report it as a new baseline, not as reproduction of the historical report.

## Research restriction

**HOLD:** no matched controls, forward outcomes, matching, inference, or profitability calculations until the exact historical producer is recovered and reproduced, or a new engine is explicitly approved with transparent versioning.
