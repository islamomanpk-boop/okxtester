# G0-04 Causal Breakout Reconstruction — Implementation Checkpoint

**Date:** 2026-11-26  
**Branch:** price-action-v1  
**Status:** CANONICAL EXECUTION PASSED; FORMAL ACCEPTANCE PENDING INDEPENDENT REVIEW

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

The original implementation checkpoint was superseded by the execution evidence below. No threshold policy has been selected and no Gate 0 closure is claimed.

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


## Canonical execution record — 2026-11-26

**Disposition:** TECHNICAL PASS; FORMAL G0-04 ACCEPTANCE PENDING INDEPENDENT REVIEW.

- Workflow run: [45749524341](https://github.com/islamomanpk-boop/okxtester/actions/runs/45749524341), attempt 6; job 139679417084 completed with conclusion SUCCESS.
- Checked-out branch and code revision: `price-action-v1`, `29e59e010d48ce6f9de7066b88e91795ee126ea8`. The metadata now records the actual checked-out commit using `git rev-parse HEAD`.
- Python 3.11.18, NumPy 2.1.3 and pandas 2.2.3. Compile and synthetic contract tests passed.
- Canonical reconstruction completed with `DESCRIPTIVE_RECONSTRUCTION_COMPLETE_BASELINE_20_OF_20`; all 20 historical baseline counts reproduced.
- Five-asset input manifest: exact common 1-minute index of 569,125 timestamps; SHA-256 hashes recorded for all five source files. SOL/DOGE/AVAX have 1/1/2 rows respectively outside the common intersection, as recorded in the manifest.
- Detector cross-pipeline feature checks: 2,358 matched contexts per asset, tolerance 1e-9. Historical one-bar-lag channel checks: 2,357 matched contexts per asset, tolerance 1e-9.
- Each asset has one explicitly reported final partial 15-minute context containing 10 rows; it is not treated as a fully covered prior calibration context.
- Historical 932-identity reconciliation: zero raw-source mismatches across all 120 asset/direction/policy/population/definition summary rows.
- Outputs: 65,310 threshold-context rows and 2,861 unique raw crossing rows. Seven output-file SHA-256 values in run metadata were independently recomputed and all matched.
- Artifact: [phase3-g0-04-causal-reconstruction-45749524341](https://github.com/islamomanpk-boop/okxtester/actions/runs/45749524341/artifacts/15086205202), artifact ID 15086205202; ZIP SHA-256 `ad9087acfcf71d17125b503fc2cd6aeeab06a486d57be1d742dfc0a65528dab6`.

**Review limitations / next gate:** This is a descriptive reconstruction, not a selected causal threshold policy and not an execution or profitability test. The expected partial-tail coverage exception is documented, not silently discarded. The independent review must still inspect the complete output semantics and confirm the frozen controls before formal G0-04 acceptance. G0-05 implementation/candidate generation remains blocked until that acceptance. Gate 0 remains CONDITIONAL HOLD; no strategy backtest, orders, fills, execution simulation or PnL work is authorized.


## Second-pass artifact/code audit — 2026-11-26

**Disposition:** ASSISTANT-SIDE TECHNICAL AUDIT PASSED; THIS IS NOT THE REQUIRED INDEPENDENT REVIEW OR FORMAL G0-04 ACCEPTANCE.

The reconstruction source and canonical artifact were reviewed again after the successful run. The review checked the source's fail-closed input hash/schema/continuity checks; complete right-labelled bar construction; separation of detector and historical one-bar-lag contexts; backward-only as-of assignment; baseline-before-output sequencing; 180-prior-completed-context threshold clock; exclusion of partial contexts from calibration; unique raw event keys; strict/broad nesting; historical identity reconciliation; and output manifest semantics.

Independent recomputation from the downloaded artifact confirmed:
- 65,310 threshold rows, with unique asset/snapshot/policy/population keys.
- Every calibration endpoint is strictly earlier than its classified snapshot.
- Fixed-180 and Rolling-180 rows use exactly 180 prior contexts; Expanding-Prior rows use at least 180.
- Joined-15M calibration counts equal exactly 16 rows per prior context.
- All P25 values are no greater than corresponding P40 values.
- 2,861 raw crossing identities are unique; all 12 strict/broad variant labels are populated.
- Exactly 932 raw events are marked as historical selected identities.
- The 120 reconciliation dimensions (5 assets × 2 directions × 3 policies × 2 populations × 2 definitions) are present, with zero historical raw-source mismatches.
- All 20 baseline counts and the five-asset cross-pipeline/coverage checks remain as recorded above.

No code or artifact defect was identified in this second-pass scope. This check is performed by the same assistant workflow and must not be represented as an independent human/reviewer sign-off. The formal reviewer must still verify the source and artifact against the frozen controls and record their own disposition. Until then, G0-04 remains technically passed but formally pending; G0-05 implementation/candidate generation remains blocked, Gate 0 remains CONDITIONAL HOLD, and no strategy backtest is authorized.


## Corrected source-validation execution — 2026-11-26

**Disposition:** CORRECTED CANONICAL EXECUTION SUCCESS; FORMAL G0-04 ACCEPTANCE STILL PENDING INDEPENDENT REVIEW.

- Workflow run: [45752717022](https://github.com/islamomanpk-boop/okxtester/actions/runs/45752717022), attempt 1; job 139684635786 completed SUCCESS on branch `price-action-v1`.
- Exact checked-out source revision: `8326c1edea66c11391ab614b9ce4afa9be5bc1fd`.
- Dependency installation, Python compilation, synthetic contract tests, full fail-closed descriptive reconstruction, and artifact upload all completed successfully.
- The historical source ledger is a classification matrix: signal identities intentionally repeat across the two definitions (STRICT_P25/BROAD_P40) and three zone levels (5/10/15%). The corrected validator checks uniqueness at the full classification-row grain before collapsing to the 932 distinct signal identities. It also rejects null/invalid timestamps before integer conversion.
- Artifact: [phase3-g0-04-causal-reconstruction-45752717022](https://github.com/islamomanpk-boop/okxtester/actions/runs/45752717022/artifacts/15085744573), artifact ID 15085744573; ZIP SHA-256 `11f6908b191d3b66bd4d17ef5a3e5d05f7f37050f9565ceeea05f4abc4571bfe`.
- Artifact metadata reports `DESCRIPTIVE_RECONSTRUCTION_COMPLETE_BASELINE_20_OF_20`, code revision `8326c1e...`, and exact common 1-minute index 569,125.
- Independent artifact inspection confirmed all 20/20 historical baseline counts; 65,310 threshold rows; 2,861 raw crossing events; 120 reconciliation dimensions; zero raw-source mismatches; and all seven output SHA-256 hashes match the manifest. Five-asset detector checks each matched 2,358 contexts; historical lag checks each matched 2,357 contexts, with the documented two boundary rows and final partial 15-minute context exception.
- Scope remains descriptive only. This run does not authorize candidate generation, execution simulation, strategy backtesting or PnL. The previous assistant-side review is not an independent reviewer sign-off. G0-04 formal acceptance remains pending; G0-05 implementation remains blocked; Gate 0 remains CONDITIONAL HOLD.
