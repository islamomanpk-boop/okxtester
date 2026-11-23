# Breakout Feature Formula Audit — Diagnostic V2

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** source review completed; next read-only runtime diagnostic prepared; results pending  
**Research gate:** matched-control study remains HOLD.

## Review completed

The following GitHub sources were fetched and compared:

- `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh`
- `research/validation/breakout_event_count_variant_diagnostic_v1.py`
- `research/matched_controls/matched_control_event_gate_v1.py`
- `research/sideways_detector_original_v1.py`
- Historical accepted-result, source-audit, conflict-hold, and runtime-failure checkpoints.

The repository tree was also inspected for other breakout/retest/event source files and run artifacts. The preserved archived script and reports exist, but no contemporaneous raw terminal log or input-file hash manifest for the historical 20/20 run was identified in the inspected research tree.

## Findings

1. The archived breakout script calculates directional efficiency using **11 close changes (12 closes)**:
   - absolute close-to-close net change over 11 intervals;
   - divided by the sum of 11 absolute percentage close changes.

2. The separate historical sideways detector calculates directional efficiency using **12 close changes (13 closes)**. Its source explicitly documents 13 close observations and 12 changes. This is a source-grounded alternative that the prior four-way diagnostic did not test.

3. The archived breakout script's adjacent-overlap calculation uses a rolling mean requiring all 11 adjacent-pair ratios to be valid. The historical sideways detector instead averages the available finite adjacent-pair ratios and returns missing only when none are valid. This is a second source-grounded difference that the prior diagnostic did not test.

4. The previous diagnostic tested unique-4H versus joined-15M width quantiles and archived versus accepted previous-sideways masks. All four combinations produced 0/20 exact matches. Therefore these two dimensions alone do not resolve the discrepancy.

5. The current event gate uses the archived 11-change efficiency and strict 11-pair overlap calculation. Its joined-15M thresholds agree with the historical reference to displayed precision, but its event counts remain 0/20.

6. The original accepted result report records the 20 counts, but the exact historical input hashes and contemporaneous run log were not found in the inspected GitHub research tree. This leaves data-version/run provenance as a separate unresolved question. No claim is made that the candle files changed.

## New diagnostic code

Added:
- `research/validation/breakout_event_feature_formula_diagnostic_v2.py`
- Commit: `d0ad063d90337567f0d10a433439e8a33afac13e`

The read-only diagnostic tests a 2×2 set of feature alternatives grounded in the two existing source implementations:

- ER: 11 changes / 12 closes versus 12 changes / 13 closes.
- Overlap: require all 11 valid pairs versus average the available valid pairs.

All variants retain:
- the five-asset common 1M timestamp intersection;
- complete epoch-aligned 15M and 4H candles;
- 12-bar channel width;
- joined-15M P25/P40 quantiles recomputed dynamically;
- backward-as-of feature availability mapping;
- same-snapshot prior/current breakout crossing;
- no previous-sideways filter, no cooldown, and no de-clustering.

The script prints all 20 counts and thresholds for every variant. It does not write files, construct controls, calculate forward outcomes, or select a variant merely because it matches.

## Next Termux command

After pulling the branch, run:

```bash
cd ~/okxtester || exit 1
git pull --ff-only origin price-action-v1
python research/validation/breakout_event_feature_formula_diagnostic_v2.py
```

Preserve the complete output. A variant match is not automatically accepted: its formula must first be justified against the historical method. If none matches, continue the provenance investigation without tuning.

## Hold conditions

- Do not construct matched controls or calculate matched outcomes.
- Do not alter the accepted historical count table.
- Do not overwrite the archived original script or prior diagnostics.
- Do not claim the exact historical producing source has been recovered.
- Preserve the diagnostic output and interpretation in a separate checkpoint after the runtime run.
