# Sideways Boundary Interaction Taxonomy V1 — SOL Source Hash Correction

Date: 2026-11-24
Branch: `price-action-v1`
Status: Hash-manifest correction verified; historical study not yet rerun.

## 1. Scope

Corrected one incorrect expected SHA-256 value for the SOL 15-minute source CSV in:

`research/sideways_boundary_interaction_taxonomy/sideways_boundary_interaction_taxonomy_v1.py`

Added a regression test in:

`tests/test_sideways_boundary_interaction_taxonomy_v1.py`

No source data, frozen taxonomy specification, or provenance checkpoint was changed.

## 2. Verified SOL source hash

The verified SOL CSV SHA-256 is:

`5b34cbb006497ecd7ebe0cfa67b25b4230cb769d6362d278991171a8f6da2d33`

The local SOL source CSV, its preserved backup, and the existing data-provenance checkpoint agree with this value.

The script previously contained this incorrect expected value, with one extra `1`:

`5b34cbb006497ecd7ebe0cfa67b25b4230cb769d6362d2789911711a8f6da2d33`

The script now contains the verified value. The provenance checkpoint remains unchanged.

## 3. Failure evidence and preservation

The initial historical run stopped at SOL during source-hash verification. The preserved log is:

`reports/sideways_boundary_interaction_taxonomy_v1_run_2026-11-24.log`

The log records a `ValueError` for an SOL 15-minute SHA-256 mismatch. The mismatch was caused by the incorrect expected hash in the script, not by a change to the source CSV.

The taxonomy output directory was checked after the failed run and was empty. No report output from that failed attempt needed to be removed or overwritten.

The failed run log is retained as research evidence. It must not be overwritten.

## 4. Code and test correction

Changed files:

1. `research/sideways_boundary_interaction_taxonomy/sideways_boundary_interaction_taxonomy_v1.py`
   - Corrected the SOL expected SHA-256 constant.
2. `tests/test_sideways_boundary_interaction_taxonomy_v1.py`
   - Imported `EXPECTED_15M_SHA256`.
   - Added a regression test verifying that the SOL manifest hash equals the verified provenance hash.

No unrelated files are part of this correction.

## 5. Verification

After the correction:

- Python compilation passed for the taxonomy script and its test file.
- The taxonomy unit-test suite passed: 21 tests, 0 failures.
- `git diff --check` reported no whitespace errors.
- The local script hash, actual SOL CSV hash, and preserved provenance hash were verified to match.

The source-hash check remains enabled by default. The `--skip-source-hash-check` option was not used to bypass this failure.

## 6. GitHub synchronization

At the time of diagnosis, GitHub branch `price-action-v1` still contained the earlier incorrect script hash and the earlier test file. The local correction therefore requires a reviewed commit and push, followed by remote verification.

The existing provenance checkpoint on GitHub already contains the correct SOL hash and is not to be modified.

## 7. Next action — pending

After this correction is committed and verified on GitHub:

1. Confirm the taxonomy output directory is empty.
2. Rerun the historical taxonomy study using the original source-hash verification.
3. Use a new, unique run-log filename; preserve the failed log above.
4. Inspect every generated report and integrity audit.
5. Record the actual study results and limitations in a separate results checkpoint.

This checkpoint documents only the hash-manifest correction. It does not claim that the historical taxonomy study has completed or passed its output audits.
