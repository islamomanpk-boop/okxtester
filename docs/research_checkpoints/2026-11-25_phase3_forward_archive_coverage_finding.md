# Phase 3 — Forward Archive Coverage Finding

**Date:** 2026-11-25  
**Applies to:** Phase 3 Module B historical validation.  
**Status:** Evidence-based validation-scope clarification.

## Finding

The frozen reference file `reports/breakout_forward_outcome_v1/breakout_forward_outcomes_v1.csv` has no columns for outside retest approach, boundary penetration, retest elapsed minutes, retest depth, or retest hold. Its actual header was inspected directly.

The immutable recovered source `research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py` has Git blob SHA `95d2975947c449f3813d80ee7b12008db14f071f`. That source calculates and prints retest summaries but explicitly ends with a read-only/no-files-written statement. It does not create the accepted forward-outcome CSV or persist row-level retest observations.

The accepted forward-outcome metadata describes a separate archived study with 19,104 horizon rows. The CSV therefore supports cross-checking only the measurements it actually stores. Treating absent retest columns as mismatches was an invalid comparison contract, not evidence that the newly calculated retest values are wrong.

## Validation treatment

- Keep the accepted archive immutable.
- Cross-check all common archived price-path fields against the accepted CSV.
- Record the five unavailable lifecycle fields explicitly in run metadata.
- Do not claim the retest metrics have independent historical-reference validation.
- Keep retest calculations and synthetic tests intact; no definitions or thresholds are relaxed.
- Module B remains pending until the complete historical workflow and independent review pass.

## Unavailable archived fields

- `outside_retest`
- `outside_retest_boundary_crossed`
- `outside_retest_minutes`
- `outside_retest_depth_pct_of_boundary`
- `outside_retest_hold`
