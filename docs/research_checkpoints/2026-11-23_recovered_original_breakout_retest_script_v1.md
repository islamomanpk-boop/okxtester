# Recovered Original Breakout and Retest Research Script — 2026-11-23

## Status

The user recovered and pasted the complete original command titled **SIDEWAYS BREAKOUT CONTINUATION AND RETEST STUDY**. The exact supplied artifact has been preserved unchanged in:

- `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh`

GitHub branch: `price-action-v1`

Preservation commit: `61f87befb36636c2f5b200b14d11c38344675ec6`

The file was fetched back from GitHub after the commit and verified:
- 506 lines
- starts with the supplied `cd ~/okxtester` and Python heredoc wrapper
- ends with the supplied heredoc terminator
- contains the original `previous_selected` condition and next-minute timing logic

This is a verbatim preservation checkpoint, not a claim that the script has been independently executed or validated against the accepted event counts.

## Timing logic in the recovered script

- 15M bars are left-labelled and left-closed; their index is the bar start.
- The 15M event bar is treated as confirmed at `event_time + 15 minutes`.
- The 1M follow-up begins at that exact next-minute timestamp.
- The first follow-up minute is included in the retest search.
- The original event boundary is frozen for each event.
- Subsequent completed 15M bars are used for return-inside checks.
- Horizons are 1H, 4H and 12H.

This is consistent with the accepted timing convention documented in the research record, subject to execution and reproduction tests.

## Initial review findings — not yet changed

The original file must remain immutable. The following points require explicit testing in a separate reproduction/validation implementation:

1. **Additional previous-sideways filter:** the script defines `valid_cross = selected & previous_selected & same_snapshot`. The accepted 20-count breakout reproduction specification requires `sideways & same_snapshot & crossing` and does not include a previous-bar-sideways requirement. This difference may change event counts.
2. **Quantile population:** the script calculates P25/P40 from `features["width"]` after dropping missing feature rows. The accepted breakout reproduction record describes thresholds calculated from the joined channel-width observation sample. Verify the exact population and thresholds; do not silently substitute historical sideways-detector thresholds.
3. **Adverse excursion convention:** the script reports adverse excursion as a positive magnitude. The matched-control specification defines non-positive MAE. Any comparison must use an explicitly documented consistent sign convention.
4. **Unused variable:** `inside` is calculated but not used in the output records. This is not changed in the archived original.
5. **Validation gate:** this script's printed event counts have not yet been shown to reproduce the accepted 20 asset/definition/direction counts. Do not use its follow-up outcomes for matched-control conclusions until exact reproduction passes.

## Next steps

1. Keep this recovered source unchanged.
2. Build a separately named reproduction/validation script based on the accepted breakout specification.
3. Validate all 20 event counts and threshold populations. Any mismatch is a stop condition.
4. Only after a full pass, audit follow-up eligibility, outcome formulas and matched controls.
5. Preserve each new script, test, command, result and decision in GitHub under the Golden Rule.

## Research integrity

This recovery does not establish profitability, predictive value, exchange provenance, or matched-control validity. No strategy backtest or live-trading conclusion is authorized by this checkpoint.
