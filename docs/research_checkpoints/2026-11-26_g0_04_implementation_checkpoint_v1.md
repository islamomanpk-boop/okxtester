# G0-04 Causal Breakout Reconstruction — Implementation Checkpoint

**Date:** 2026-11-26  
**Branch:** price-action-v1  
**Status:** CORRECTED CANONICAL EXECUTION AND RAW-INPUT RECOMPUTATION PASSED; FORMAL G0-04 ACCEPTANCE PENDING REVIEW DISPOSITION

## Files added

- research/phase3_g0_04_causal_breakout_reconstruction_v1.py
- .github/workflows/phase3-g0-04-causal-breakout-reconstruction.yml

The workflow supports manual dispatch and push triggers on `price-action-v1` for the G0-04 source/workflow paths, checks out the triggering branch revision, grants contents: read, runs Python 3.11 with pinned NumPy/Pandas, compiles the script, runs synthetic tests, then attempts the full descriptive reconstruction. It uploads artifacts for 14 days. It does not commit generated reports or write to source data.

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


## Independent reviewer packet prepared — 2026-11-26

A bounded review packet is now available at [2026-11-26_g0_04_independent_review_packet_v1.md](2026-11-26_g0_04_independent_review_packet_v1.md). It freezes the corrected source commit, workflow/job, artifact ID and ZIP hash, and supplies a reviewer checklist plus explicit ACCEPT / REJECT / INCONCLUSIVE disposition template. This is preparation only; no reviewer identity or sign-off has been fabricated. G0-04 remains technically passed but formally pending an actual independent reviewer disposition. G0-05 implementation remains blocked; Gate 0 remains CONDITIONAL HOLD.


## Independent AI review — artifact-level results and residual evidence — 2026-11-26

A separate AI reviewer (Kimi / Moonshot AI) inspected the exact G0-04 artifact ZIP and reported an **INCONCLUSIVE** disposition, narrowly due to unavailable raw 1-minute input CSVs and inability to independently regenerate the historical baseline from those raw inputs. This is not a rejection and is not formal acceptance.

The reviewer independently recomputed the artifact ZIP SHA-256 against the frozen value; all seven output-file hashes; threshold-table structure (65,310 rows, unique keys, strictly earlier calibration endpoints, 180-row fixed/rolling windows, expanding prior counts, 16 joined 15-minute rows per prior context, P25 <= P40); 2,861 raw event identities; all 34,332 strict/broad variant flags from the threshold table; and all 120 reconciliation dimensions from the raw event output. The reviewer reported zero variant-flag mismatches, zero raw-source mismatches in the reconciliation output, and no issue above MINOR in the inspected scope. The reviewer did not inspect the five raw 1-minute inputs or independently derive the baseline from market data; do not describe these items as independently verified.

Additional direct repository inspection performed after that report:
- Retrieved the historical classification ledger and all five detector feature ledgers from the repository.
- Independently checked the classification ledger: 4,776 source classification rows; exactly 932 distinct signal identities; definitions exactly STRICT_P25 and BROAD_P40; zone levels exactly 5, 10, and 15; zero null/invalid zone values; zero duplicate full classification rows at identity + definition + zone grain.
- This confirms the reported zone-null condition is a **validator robustness gap**, not a defect present in the actual frozen ledger.
- The repository connector returned no contents for the five 1-minute market CSV paths, so their hashes and full market-data recomputation remain outstanding. Detector-ledger files were retrieved but have not yet been independently recomputed against the missing market inputs.

The reviewer also recorded descriptive-only observations to preserve: 262 raw events are in calibration warm-up and ineligible under all variants; two SOL events have undefined efficiency/overlap and are ineligible; and 12 legacy ratio-based efficiency values exceed 1. These are not automatically defects; preserve the legacy formula and explicitly document its interpretation rather than imposing the detector efficiency's [0,1] bound. The baseline percentile population question is resolved: the original `research/breakout_test_count/breakout_test_count_study_v1.py` computes P25/P40 from `joined[\"channel_width\"].dropna()`, i.e. the joined 15-minute observation population. The G0-04 historical baseline uses the same joined-row population, so this aspect matches the original study. Supporting archive: `docs/research_checkpoints/2026-11-24_breakout_prior_test_count_study_audit_v1.md`.

### Defensive validation repair

The historical classification validator previously dropped null values before checking the allowed zone set. It has now been strengthened to reject null or non-numeric zone values before checking the exact {5, 10, 15} set.

- Repair commit: `86b49598d676b6ab00649bf31d4490ffbb1e608f`
- Workflow run: [45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179)
- Run status at checkpoint update: IN PROGRESS.
- The frozen review target remains commit `8326c1edea66c11391ab614b9ce4afa9be5bc1fd` and its artifact. The repair is a subsequent defensive validation revision and must pass its own workflow before it can replace the canonical implementation target.

**Current disposition:** G0-04 remains technically executed and substantially artifact-audited, but formally **INCONCLUSIVE / acceptance pending** because raw input hash verification and independent market-data baseline regeneration remain open. G0-05 implementation and candidate generation remain blocked; Gate 0 remains CONDITIONAL HOLD. No execution simulation, strategy backtest, or PnL work is authorized.


### Follow-up verification of original quantile population — 2026-11-26

The independent AI review left a question about whether historical P25/P40 quantiles were calculated over joined 15-minute observations or unique 4-hour contexts. This was resolved by inspecting the original prior-test study implementation and its audit checkpoint:
- Original implementation: `research/breakout_test_count/breakout_test_count_study_v1.py`; `original_events()` calculates `widths = joined["channel_width"].dropna()`, then `quantile(0.25)` and `quantile(0.40)`.
- Original audit: `docs/research_checkpoints/2026-11-24_breakout_prior_test_count_study_audit_v1.md`; records 20/20 event counts and 10/10 quantile reproductions.
- Conclusion: the historical baseline's joined-15-minute population is consistent with the original study method; this reviewer question is closed.

The actual historical classification ledger was also independently fetched and checked at repository branch `price-action-v1`: 4,776 rows, 932 distinct signal identities, definitions exactly STRICT_P25/BROAD_P40, zone levels exactly 5/10/15, zero null/invalid zone values, and zero duplicate full classification rows. This confirms the zone-null concern is a validator robustness issue only; the actual ledger contains no null zone values.


## Corrected validator run and independent raw-input recomputation — 2026-11-26

The defensive zone-level validation repair completed successfully.

- Source commit: `86b49598d676b6ab00649bf31d4490ffbb1e608f`
- Workflow run: [45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179)
- Job: `139694830125`, conclusion SUCCESS; all workflow steps passed.
- Artifact: [phase3-g0-04-causal-reconstruction-45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179/artifacts/15087542445), artifact ID `15087542445`.
- Artifact ZIP SHA-256: `ef6204b546b49880675514ff76b4f6cb86e2821ba2b0d1d5412549927388f0a1`.
- Metadata records exact code revision `86b49598d676b6ab00649bf31d4490ffbb1e608f`, common index 569,125 and descriptive-only scope.
- All seven output-file SHA-256 values were independently recomputed and match the artifact manifest.
- Compared with the prior corrected artifact from run 45752717022, all seven output files are byte-identical and all five input manifest hashes are unchanged. The zone-null validator repair therefore changed validation only, not research outputs.

### Direct raw-input integrity and baseline recomputation

The five raw 1-minute CSV blobs were retrieved directly from the repository at the same branch data revision and independently checked, rather than relying only on the artifact's recorded manifest:

| Asset | Source rows | SHA-256 matches metadata | Duplicate / out-of-order timestamps | Non-1m steps | Invalid OHLCV |
|---|---:|---|---:|---:|---:|
| BTC | 569,125 | Yes | 0 | 0 | 0 |
| ETH | 569,125 | Yes | 0 | 0 | 0 |
| SOL | 569,126 | Yes | 0 | 0 | 0 |
| DOGE | 569,126 | Yes | 0 | 0 | 0 |
| AVAX | 569,127 | Yes | 0 | 0 | 0 |

The first 569,125 timestamps are identical across all five assets, producing the exact 569,125-row common index. SOL and DOGE each have one additional trailing minute; AVAX has two. All five source hashes exactly match `run_metadata.json`.

A separate implementation of the original breakout-study equations was run directly against these raw market rows. It independently rebuilt completed 15-minute and 4-hour bars, historical one-completed-4H-candle-lagged contexts, joined 15-minute observations, P25/P40 quantiles and breakout crossing counts. It did not use the G0-04 output baseline CSV or the source's hard-coded expected-count dictionary as its calculation input.

| Asset | P25 | P40 | Strict lower / upper | Broad lower / upper |
|---|---:|---:|---:|---:|
| BTC | 3.2422032509 | 3.9486301407 | 62 / 81 | 91 / 115 |
| ETH | 4.2423264197 | 5.4818862309 | 51 / 51 | 87 / 77 |
| SOL | 5.0670430487 | 6.1145417121 | 77 / 71 | 117 / 96 |
| DOGE | 5.1657244208 | 6.2640575798 | 55 / 65 | 81 / 75 |
| AVAX | 5.7036247335 | 6.9162158210 | 64 / 83 | 84 / 109 |

All 20 historical counts independently reproduce the frozen baseline, and all 10 quantiles reproduce the original study values within its stated tolerance. This closes the raw-input and independent-baseline evidence gap identified in the Kimi report, subject to review of this audit record and its method.

### Direct detector-ledger cross-check

The five original detector feature ledgers were independently compared against detector contexts rebuilt from the raw 1-minute files. Each asset matched all 2,358 detector-ledger rows on timestamp, upper, lower, channel width, directional efficiency and mean overlap. No timestamp or value mismatch was found. Maximum absolute numerical difference was (3.33\times10^{-16}), below the (10^{-9}) tolerance. Each asset produced 2,370 complete 4-hour bars.

The historical classification ledger was also directly checked: 4,776 rows; 932 distinct signal identities; exact definitions STRICT_P25/BROAD_P40; exact zone levels 5/10/15; zero null/invalid zone values; zero duplicate full-grain rows at identity + definition + zone level.

### Interpretation and remaining governance

The separate AI reviewer Kimi's own report remains labelled INCONCLUSIVE because Kimi did not personally access the raw CSVs. The additional direct checks above were performed separately and close the evidence gap within this project-side audit; they do not retroactively change Kimi's disposition or constitute a human sign-off.

The four descriptive observations from Kimi remain documented: 262 raw events in warm-up are ineligible under all variants; two SOL events with undefined efficiency/overlap are ineligible; 12 legacy ratio-based efficiency values exceed 1 and must not be confused with detector efficiency; and the actual classification ledger contains no null zone values despite the validator gap that has now been fixed.

**Current disposition:** technical reconstruction, corrected validation, artifact integrity, raw input hashes, common-index integrity, baseline counts/quantiles, and detector-ledger cross-checks have now passed. Formal G0-04 acceptance still requires the project owner to decide whether the independent AI review plus this separately documented assistant-side raw-data recomputation satisfies the project's review standard, and to record that disposition. G0-05 implementation/candidate generation remains blocked; Gate 0 remains CONDITIONAL HOLD. No execution simulation, strategy backtesting, or PnL work is authorized.
