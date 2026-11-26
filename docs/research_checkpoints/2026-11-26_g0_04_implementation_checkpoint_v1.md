# G0-04 Causal Breakout Reconstruction — Implementation Checkpoint

**Date:** 2026-11-26  
**Branch:** price-action-v1  
**Status:** IMPLEMENTED IN REPOSITORY; NOT YET EXECUTED ON CANONICAL DATA

## Files added

- research/phase3_g0_04_causal_breakout_reconstruction_v1.py
- .github/workflows/phase3-g0-04-causal-breakout-reconstruction.yml

The workflow is manual-dispatch only, checks out price-action-v1, grants contents: read, runs Python 3.11 with pinned NumPy/Pandas, compiles the script, runs synthetic tests, then attempts the full descriptive reconstruction. It uploads artifacts for 14 days. It does not commit generated reports or write to source data.

## Frozen controls implemented

1. Verify the five canonical 1M SHA-256 hashes before parsing; validate schema, row counts, timestamps and OHLCV.
2. Require the exact 569,125-row common minute index and 60-second cadence.
3. Rebuild complete right-labelled 15M/4H bars with left-closed intervals.
4. Reproduce the recovered lagged 12-candle context, efficiency and overlap formulas.
5. Backward as-of join 15M closes to context; fail on missing/future assignments.
6. Compare finite context timestamps and channel geometry to the detector feature ledgers using the predeclared one-4H offset and absolute tolerance 1e-9 (zero relative tolerance).
7. Reproduce all 20 historical full-sample event counts before computing any causal threshold or raw-event output. Any mismatch stops the run.
8. Discover raw same-context 15M close crossings without starting from the historical 932-event selected ledger.
9. Use a common 180-prior-completed-context clock for all six variants: Fixed-180, Expanding-prior and Rolling-180, each with unique-4H and joined-15M weighting.
10. Permit a partial current context to receive a threshold based only on fully covered prior contexts; partial contexts cannot enter calibration.
11. Preserve one row per event identity, attach six strict/broad variant pairs, and assert strict is nested in broad.
12. Reconcile the historical 932 unique signal identities. A missing historical identity in the raw scan is a hard stop.
13. Emit descriptive manifests, context/coverage audit, historical baseline, threshold table, raw event ledger, reconciliation, summaries and output hashes.

## Synthetic checks included

The script's --self-test covers right-labelled 15M bars, incomplete 4H exclusion, equal-time context availability, rejection of future context assignment, 180-context warm-up, the six policy/population rows, fixed/rolling/expanding prior counts, exclusion of current-context width, exclusion of a partial prior context, strict/broad percentile nesting, and duplicate historical identity collapse.

These checks have been added but have **not yet been executed**. The full canonical-data reconstruction has also **not been executed**. No causal results, event counts, threshold policy choice or Gate 0 closure are claimed.

## Run instructions

From GitHub on mobile or desktop:
1. Open repository islamomanpk-boop/okxtester.
2. Select branch price-action-v1.
3. Open Actions and select **Phase 3 G0-04 Causal Breakout Reconstruction**.
4. Choose **Run workflow**, keep branch price-action-v1, and confirm.
5. Wait for the job to finish. Inspect the compile/synthetic-test step before trusting the reconstruction step.
6. Download artifact phase3-g0-04-causal-reconstruction-<run id> if uploaded.

GitHub Actions continues running if the phone is locked or switched off. ChatGPT does not continue working independently while no message is being exchanged.

## Stop / governance

A successful workflow run would only produce descriptive causal-eligibility evidence for G0-04. It would not close G0-04/G0-05 by itself, authorize candidate generation, or permit execution simulation, Gate 2, strategy backtesting or PnL. Gate 0 remains CONDITIONAL HOLD until all required evidence and independent reviews pass.
