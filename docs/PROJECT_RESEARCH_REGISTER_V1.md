# OKX Price Action V1 — Repository Reconciliation and Research Register V1

**Review date:** 2026-11-25  
**Canonical repository/ref:** `islamomanpk-boop/okxtester@price-action-v1`  
**Canonical tree commit reviewed:** `42ab2ed543eb59a755f8f9fe2605ad720ac36574`  
**Supporting repository/ref:** `islamomanpk-boop/okxtester_private@main`  
**Supporting tree commit reviewed:** `cbeeae0fb61fcaa702a594543e6e440318520dce`  
**Status:** Initial full tracked-tree reconciliation; no files deleted, moved, or overwritten.

This register is the navigation index for existing Price Action work. It records the repository snapshot actually inspected and distinguishes confirmed Price Action assets from likely unrelated legacy material. It is not a claim that every historical workflow run or every CSV has been independently re-executed.

## 1. Authority and repository roles

- **Canonical research record:** `okxtester`, branch `price-action-v1`. Research protocols, reusable code, tests, reports, evidence, decisions, and project documentation belong here.
- **Supporting operations:** `okxtester_private`, branch `main`. Its current tracked contents are VPS/data operations and Phase 3 readiness/range-measurement workflows. Reconcile useful results into the canonical record; do not blindly merge repositories.
- **Branch snapshot:** canonical branch head was `42ab2ed...`; canonical `main` was separately observed at `1239bae75cddffa03fb84aba54b96e72a9e79af3`. The supporting repository had only `main` at `cbeeae0...`.
- Preserve local-only funding inputs and other private source files. Their absence from Git is intentional where documented.

## 2. Five-phase project register

| Phase | Regime | Current register status | Boundary / next action |
|---|---|---|---|
| 1 | Uptrend / Bullish | Preflight foundation only; not active | Five-asset source preflight script/test exists. Do not begin until Phase 3 is formally completed under the current user-directed sequence. |
| 2 | Downtrend / Bearish | Not yet evidenced as started in this reconciliation | No completion claim. Start only after Phase 1 closeout. |
| 3 | Sideways / Range | **ACTIVE — descriptive core complete; execution research incomplete** | Continue the eight-gate roadmap below. |
| 4 | Choppy / High Volatility | Not yet evidenced as started in this reconciliation | No completion claim. Start only after Phase 3 and preceding phases. |
| 5 | Transition / Expansion | Not yet evidenced as started in this reconciliation | No completion claim. Start only after preceding phases. |

The agreed execution sequence is: **finish the currently active Phase 3 completely first; then Phase 1 → Phase 2 → Phase 4 → Phase 5**. Phase 1 remains paused until Phase 3 is formally completed or explicitly rejected. After the Phase 3 handoff, continue the remaining numbered phases in order without skipping. Do not use older handoff wording in historical closeout documents to override the current control center.

## 3. Phase 3 research register

The following statuses reflect archived code, tests, reports, and the formal scope audit. “Completed” means the specified descriptive study has archived evidence; it does not mean a trading strategy or executable edge has been validated.

| ID | Workstream | Status | Evidence locations | Gate mapping / limitation |
|---|---|---|---|---|
| P3-01 | Historical sideways detector and regime snapshots | Completed descriptive foundation | `research/sideways_detector_original_v1.py`, `research/sideways_detector_v1.py`, `reports/sideways_detector_v1/`, original archive and detector checkpoints | G0/G1; freeze exact detector version and provenance for downstream use. |
| P3-02 | Historical boundary reconstruction and test counts | Completed descriptive foundation | `research/sideways_boundary_events_historical_v1.py`, `reports/sideways_boundary_events_historical_v1/`, tests and historical reconstruction spec/audit checkpoints | G1; descriptive event ledger, not an order ledger. |
| P3-03 | Boundary interaction / penetration taxonomy | Completed | `research/sideways_boundary_interaction_taxonomy/sideways_boundary_interaction_taxonomy_v1.py`, matching test, workflow, `reports/sideways_boundary_interaction_taxonomy_v1/` | G1; 153,540 candle-level observations. Distinguishes approach, touch, wick penetration, close outside, and re-entry; candle rows are dependent. |
| P3-04 | Rejection episode / retest anatomy | Completed for archived selected cohort | `research/sideways_rejection_episode_retest_anatomy_v1.py`, test, workflow, `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/` | G1; 1,992 eligible events, four horizons. Not a complete signal-to-fill study. |
| P3-05 | Rejection early-path sequence and follow-through | Completed descriptive study | `research/sideways_rejection_early_path_sequence_followthrough_v1.py`, test, workflow, `.../early_path_followthrough_v1/` | G1; observational associations, not causal/executable outcomes. |
| P3-06 | Calendar moving-block bootstrap | Completed exploratory uncertainty analysis | `research/sideways_rejection_block_bootstrap_v1.py`, `research/sideways_rejection_sequence_block_bootstrap_v1.py`, tests, `.../sequence_block_bootstrap_v1/` | G1; does not establish causality or profitability. |
| P3-07 | Per-asset / leave-one-asset-out robustness | Completed with small-sample caveats | `research/sideways_rejection_matched_asset_robustness_v1.py`, test, `.../asset_robustness_v1/` | G1; small matched-pair counts and residual design limitations. |
| P3-08 | Breakout prior-boundary-test classification | Completed descriptive study | `research/breakout_test_count/breakout_test_count_study_v1.py`, test, workflow, `reports/breakout_prior_test_count_v1/` | G1; classifications do not establish a trading rule. |
| P3-09 | Breakout forward-path outcomes | Completed descriptive study | `research/breakout_forward_outcomes/breakout_forward_outcome_study_v1.py`, test, workflow, `reports/breakout_forward_outcome_v1/` | G1; forward MFE/MAE/path outcomes are not executable PnL. |
| P3-10 | Pre-event matched-control investigation | Rejected for outcome comparison; retained | `research/matched_controls/`, `research/sideways_rejection_pre_event_matched_controls_*.py`, corresponding tests/workflows, `.../pre_event_matched_controls_v1..v6/` and V7–V10.11 diagnostic archives | G1; V6 cohort failed balance/joint-support requirements. Do not rematch or compare future outcomes using these pairs. Preserve all versions. |
| P3-11 | Five-asset 1M source quality and alignment | Prior preflight completed; runtime/source provenance reconciliation remains part of G0 | `reports/1m_data_quality_audit_2026-11-20.md`, `reports/cross_asset_timestamp_alignment.*`, `research/phase1_uptrend_data_preflight_v1.py` and test | G0; current market-data blobs are in Git despite an older doc saying raw data is local. Resolve documentation/source-of-truth discrepancy and freeze hashes. |
| P3-12 | Funding coverage and source manifest | **Local five-file audit passed; fail-closed engine contract implemented and focused CI passed; strict real-input/mark-price acceptance remains open** | `src/funding_coverage.py`, `src/funding_coverage_audit.py`, tests, `docs/research_checkpoints/2026-11-25_funding_coverage_and_engine_callsite_inventory_v1.md`, funding manifest/report archive | G0/G5; `simulate_trade` now requires an explicit coverage contract; portfolio validates schedule and coverage; workflow run 45624704814 passed compile plus seven focused test groups. CI uses synthetic fixtures. Exact settlement marks remain unverified; current experiment loader labels candle-close proxy. Keep G0-03 partially implemented until remaining real-input integration and mark policy are accepted. |
| P3-13 | Comprehensive rejection lifecycle (continuation/pullback, signal-level retests, depth, hold/failure, repeated crosses, candle anatomy) | **ACCEPTED — descriptive Module A complete** | `research/phase3_rejection_lifecycle_v1_1.py`, `tests/test_phase3_rejection_lifecycle_v1_1.py`, `reports/phase3_rejection_lifecycle_v1_1/PHASE3_REJECTION_LIFECYCLE_CLOSEOUT_V1_1.md` | G1; 1,992 events, 3,028 retest episodes, 7,968 horizon rows, 380 overlap clusters; 12 synthetic tests passed. No strategy/PnL inference. The old 2,095-cohort 1M follow-up remains superseded preliminary work and must not be reused. |
| P3-14 | Comprehensive failed-breakout / reversal lifecycle | **ACCEPTED — descriptive Module B V1.1 complete** | `research/phase3_breakout_lifecycle_v1_1.py`, `tests/test_phase3_breakout_lifecycle_v1_1.py`, `reports/phase3_breakout_lifecycle_v1_1/PHASE3_BREAKOUT_LIFECYCLE_CLOSEOUT_V1_1.md`, and the accepted reproducibility workflows recorded in that closeout | G1; 1,592 events, 6,368 complete event/horizon rows, 244 group summaries, 454 overlap clusters; 23/23 synthetic tests passed in the accepted same-revision reproducibility runs; 6,368/6,368 comparisons passed across the 18 fields available in the frozen forward archive. Five retest fields are explicitly descriptive-only because the benchmark lacks them. No orders/fills/costs/PnL. Module B formally accepted; Gate 1 descriptive lifecycle scope complete. |
| P3-15 | Same-signal execution resolution comparison (1M/3M/5M/15M) | Open | Controlling roadmap only | G2; same completed 15M cohort, first eligible execution bar at/after signal availability. |
| P3-16 | Candidate entry definitions and realistic fill/miss rules | Open | Existing execution-engine foundations/specifications; no Phase 3 entry study closeout | G3; market-style, pullback/limit, retest, and lower-timeframe confirmation hypotheses. OHLC touch is not guaranteed fill. |
| P3-17 | Stop, target, and trade management | Open | Existing generic engine/backtest docs and code are infrastructure only | G4; freeze structural/volatility stop and target/management hypotheses before outcome testing. |
| P3-18 | Execution engine acceptance for Phase 3 | Partial / open | `src/execution_engine.py`, `src/portfolio_backtester.py`, `src/funding_coverage.py`, docs and deterministic tests | G5; validate costs in risk sizing, spread/slippage, funding/mark policy, gaps/collisions, partial/missed fills, expiry, concurrency, shared equity. |
| P3-19 | Frozen Phase 3 family-specific strategy backtests | Not started / not authorized | Controlling roadmap | G6; only after G0–G5 pass. Test rejection, breakout continuation, failed-breakout reversal separately before combinations. |
| P3-20 | Chronological untouched out-of-sample validation | Not started | Controlling roadmap | G7; predeclare chronological splits, no shuffling or OOS peeking. |

### 3.1 Matched-control decision — permanent negative finding

The V6 matched-control branch and follow-up V7–V10.11 audits are preserved, not active work. Balance and joint common support were inadequate; V10.11 did not repair this. Do not widen thresholds, rematch, or use the pairs for future outcome contrasts. The rejected method is a completed research decision, not a missing task.

## 4. Controlling Phase 3 gate sequence

The single controlling roadmap is `docs/research_checkpoints/2026-11-25_phase3_execution_and_backtest_roadmap_v1.md`.

| Gate | Required outcome | Current status |
|---|---|---|
| G0 | Archive/source readiness: exact source/event ledgers and hashes, causal availability, market/funding inputs, instrument/fee/mark provenance | **CONDITIONAL HOLD — not passed**; funding file coverage G0-01/G0-02 closed for audited Termux files; G0-03 fail-closed contract implemented and focused CI passed but full acceptance remains open |
| G1 | Complete descriptive lifecycle for rejection, breakout continuation, and failed-breakout reversal | **COMPLETE — descriptive lifecycle scope accepted**; P3-13 rejection Module A and P3-14 breakout/failed-breakout Module B both formally accepted. This does not imply strategy execution or profitability validation. |
| G2 | Compare 1M/3M/5M/15M execution on identical completed 15M signals | Open |
| G3 | Freeze and compare causal entry methods with fill/miss/expiry rules | Open |
| G4 | Freeze and study stop, target, and management hypotheses | Open |
| G5 | Accept single-trade and portfolio engines with realistic costs/funding and deterministic tests | Partial/open |
| G6 | Backtest each Phase 3 family separately under frozen risk/accounting rules | Not authorized |
| G7 | Chronological validation with untouched OOS data | Not started |

**Current hard stop:** Do not run Phase 3 strategy PnL backtests until G0–G5 have documented passes. Gate 0 remains conditional hold. The roadmap, G0 audit, and G0-03 funding checkpoint are the source of truth for individual blockers.

## 5. Supporting repository inventory

The complete recursive Git tree for `okxtester_private@main` was inspected (12 tracked files; tree not truncated). Its files are operational or Phase 3 support:

- Workflows: `okx-build-aligned-dataset.yml`, `okx-download-monitor.yml`, `okx-final-data-audit.yml`, `okx-phase3-range-measurement.yml`, `okx-phase3-readiness-audit.yml`, VPS data/health workflows, and two safe-cleanup workflow variants.
- Research: `research/PHASE3_REMAINING_RESEARCH_PROGRAMME.md`, `research/phase3_range_measurement.py`, `research/phase3_readiness_audit.py`.

No file in this 12-file supporting snapshot was classified as unrelated to Price Action operations. Do not delete this repository or its VPS workflows as “old files”; it contains supporting infrastructure and recent Phase 3 readiness work. Cleanup workflows are not evidence that cleanup has been performed.

## 6. Canonical repository snapshot and file classification

Historical snapshot: the canonical recursive Git tree was inspected at `42ab2ed...` and reported 1,325 tracked blobs. The updated 2026-11-25 inventory at commit `e025e1188c266b2c678b47de7953a65aa0a4ee30` is recorded in Section 12 below; use that newer snapshot for current counts.

Top-level tracked inventory:

| Area | Tracked files | Classification |
|---|---:|---|
| `.github/workflows/` | 34 | Price Action research, funding tests, Phase 1 preflight, archive checks, and VPS monitoring; retain pending workflow-by-workflow review. |
| `data/market_1m/` | 5 | Five core asset source datasets; retain. |
| `docs/` | 163 | Governance, specifications, research, provenance, and checkpoints. Includes some legacy-project provenance investigations; do not bulk-delete. |
| `reports/` | 1,001 | Research evidence and archives. Includes some clearly named EMA-pullback outputs and large generic exit-experiment archives requiring provenance review before cleanup. |
| `research/` | 48 | Phase 3 studies, breakout studies, matched-control audits, Phase 1 source preflight, and historical provenance scripts. |
| `src/` | 68 | Shared Price Action structure, signal, funding, execution, portfolio and audit components, plus separately named EMA-pullback code. |
| `tests/` | 38 | Tests for the above study and shared components. |
| `scripts/` | 1 | Repository sync helper; inspect before changing. |
| root files | 2 | `.gitignore`, `README.md`. |

### 6.1 Confirmed likely unrelated legacy EMA-pullback files — 12 deletion candidates only

The following 16 paths are explicitly named for the older EMA-pullback project and are the clearest non-Price-Action candidates in the canonical tree:

**Reports (5)**
- `reports/ema_pullback_diagnostic_by_regime.csv`
- `reports/ema_pullback_diagnostic_by_side_exit.csv`
- `reports/ema_pullback_diagnostic_overall.csv`
- `reports/ema_pullback_v1_1_holding_period_experiment.csv`
- `reports/ema_pullback_v1_1_summary.csv`

**Source (6)**
- `src/backtest_ema_pullback.py`
- `src/backtest_ema_pullback_v1_1.py`
- `src/backtest_ema_pullback_v1_1_audited.py`
- `src/backtest_ema_pullback_v1_1_risk_corrected.py`
- `src/diagnose_ema_pullback_losses.py`
- `src/diagnose_ema_pullback_v1_1.py`
- `src/validate_ema_pullback_inputs.py`

**Decision:** These are flagged for possible removal from the canonical Price Action branch, but **nothing has been deleted**. Before any deletion, inspect import/workflow dependencies and preserve an export/archive or other recovery route. The user must approve the exact deletion list. A filename alone is not enough to delete a file.

### 6.2 Not deletion candidates without further evidence

- `docs/research_checkpoints/*adaptive_bot*` and `*scalp*`: these are provenance-search/audit notes explaining recovery of shared five-asset data and historical source material. They are not themselves bot implementations; retain unless a later audit proves otherwise.
- `reports/exit_experiments/` (729 files) and `reports/exit_experiments_telemetry_v1/`: large and potentially legacy, but the current tree alone does not establish whether any are relied on by Price Action execution/portfolio components. Trace scripts, manifests, and dependencies before classifying.
- Generic execution, portfolio, funding, signal, cost-sensitivity, and performance code/reports: retain as potentially shared Price Action infrastructure until dependency and history review proves otherwise.
- Five `data/market_1m/*.csv` source files: retain. Never delete core market data during project cleanup.
- All Phase 3 reports, failed runs, rejected matching versions, and source hashes: retain permanently.

## 7. Next actions — in order

1. Finish content-level reconciliation of the canonical repository's Phase 3 protocols, code, tests, report manifests, run metadata, and workflow history. This register is a first evidence-backed index; it does not claim every 981 report blob has been read individually.
2. Audit the generic `reports/exit_experiments/` archive against its generating scripts, configs, manifests, and consumers. Classify each batch as Price Action, legacy EMA-pullback, or unknown.
3. Inspect dependencies and history for the 12 explicit EMA-pullback candidates. Present the final exact deletion proposal to the user before deleting anything.
4. Reconcile the three supporting-repo Phase 3 files and workflow run/artifact provenance into canonical documentation. Do not copy blindly.
5. Continue the controlling Phase 3 Gate 0 blockers; do not run strategy PnL backtests while G0 is on hold.
6. Update this register and the Project Control Center after each material decision or completed gate.

## 8. Preservation and cleanup policy

- This register does not authorize deletion, force-push, reset, moving, or overwriting.
- Do not delete a file merely because it is not obviously Phase 3; Phases 1, 2, 4, and 5 belong to the same Price Action project.
- Do not delete historical audit notes merely because they mention older projects; some document data provenance needed by Price Action.
- Any cleanup must be path-specific, dependency-checked, recoverable, and approved before execution.
- Keep the canonical research branch as the single project truth; supporting operational work must be linked with exact repo/ref/path/commit/workflow/artifact provenance.


## 9. Workflow and supporting-repository reconciliation update — 2026-11-25

### Supporting repository run evidence

- Phase 3 range measurement workflow run **45613180053** completed successfully: https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45613180053. This is an exploratory descriptive range-measurement artifact only; it does not pass Gate 0 or Gates 1–4.
- Phase 3 Gate 0 readiness inventory workflow run **45620563733** completed successfully: https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45620563733. Its workflow explicitly says inventory-only and does not auto-approve a gate.
- Aligned five-coin dataset build run **45612158710** and final data alignment audit run **45611757117** completed successfully. Their workflows use read-only SQLite access and preserve the raw database.
- Scheduled download/VPS monitor run **45623691013** completed successfully. This is operational health evidence, not a research gate result.
- Safe VPS cleanup and some VPS data-audit workflow runs failed; no cleanup is inferred from those failures. VPS/data deletion is outside this research reconciliation.

### Conflicting five-gate document corrected

The supporting repository's `research/PHASE3_REMAINING_RESEARCH_PROGRAMME.md` previously described itself as the canonical source of truth with five gates. That conflicts with the current eight-gate roadmap in the canonical repository. Its header has now been clarified as a historical condensed checklist; the canonical eight-gate roadmap remains controlling. Supporting-repo commit: `ad5aac7294f0650e800ad834a1642f335915a649`.

### Funding/execution contract workflow regression found and corrected

Canonical workflow history showed:
- Run **45570913178** passed all listed funding/execution compile and focused test steps.
- Runs **45572264154** and **45575145332** failed at the compile step; all later test steps were skipped.
- Comparing the changes after the passing run showed the new read-only OKX demo API inspection script was added to the compile command. The workflow's line-continuation before that script had two trailing backslashes instead of one.
- The extra backslash was corrected in `.github/workflows/funding-engine-contract-tests.yml`, commit `5b9b487b8081113470e5da490c4465262dd08672`.
- A new run **45624704814** was triggered by the fix and subsequently **completed successfully**: https://github.com/islamomanpk-boop/okxtester/actions/runs/45624704814. The compile step and all seven focused test groups completed successfully. This resolves the immediate workflow syntax regression; it does not by itself pass Phase 3 Gate 0 or authorize strategy backtesting.

This is a workflow syntax/command assembly correction only. It does not change engine code, data, or research conclusions. Gate 0 remains conditional hold until the full blocker register is formally closed.


## 10. Exit-experiment archive classification and result reconciliation — 2026-11-25

A deeper source-to-output audit was completed for the two large exit-experiment folders. They must not be treated as Phase 3 range-strategy research, and they must not be deleted as unrelated legacy files.

### 10.1 Original exit-experiment archive

- Source runner: `src/run_exit_experiments.py`; batch runner: `src/run_exit_experiment_batch.py`; frozen matrix builder: `src/exit_experiment_config.py`.
- Candidate generator: `src/trade_candidate_engine.py`, explicitly documented in `docs/trade_candidate_engine_v1.md` as **Model A trend candidates only**. It emits no trend candidate for `NO_TREND`; SIDEWAYS/range strategies are expressly separate research.
- Signal input path expected by the runner: `~/okx_adaptive_bot/reports/price_action_signals/`; execution candles/funding expected under `~/okx_scalping_data/`. The outputs are historical five-asset trend-candidate exit experiments, not candidates generated from the frozen Phase 3 boundary/rejection/breakout event ledgers.
- Matrix: 66 configurations (22 baseline, 22 trailing-stop, 22 trailing-take-profit). The committed manifest has 66 rows and all 66 marked completed. The comparison has 66 result rows. The folder has 729 tracked files: 66 × 11 expected experiment artifacts plus 3 batch-level files (manifest, comparison, log).
- Shared cohort: 17,943 candidates; five assets; synchronized 1M execution window 2025-10-20 08:50 UTC to 2026-11-19 14:14 UTC; 569,125 execution minutes; starting equity $1,000; risk fraction 0.5%; max gross exposure 1.0x; configured taker fee 0.05% per side and slippage 2 bps per side; funding uses an explicitly labelled candle-close proxy in the loader.
- Reconciled result: all 66 configurations finished below starting equity. Net return range was approximately **−99.89% to −34.34%**; maximum drawdown range approximately **47.72% to 99.89%**. Even the least-bad configuration lost approximately 34.34% over this historical sample. This is an important negative finding for that trend-candidate/exit setup, not a Phase 3 result.
- Research limitation: the 66-way full-sample matrix is exploratory historical evidence. No untouched chronological out-of-sample validation is evidenced by this archive. Do not select the least-bad row as an optimal exit, do not transfer its parameters to Phase 3, and do not treat the run as proof that Phase 3 rejection/breakout/reversal signals lose money.

**Classification:** retain as historical Price Action trend-pipeline and shared execution/portfolio/funding-engine evidence; exclude from Phase 3 signal-family conclusions. The use of a legacy-named input directory is a provenance dependency to document, not proof that the generated candidate logic is an unrelated EMA-pullback strategy.

### 10.2 Telemetry rerun archive

- `reports/exit_experiments_telemetry_v1/` contains 25 tracked files: the batch-level files plus the expected artifacts for only two completed experiments.
- Its manifest records 66 planned configurations: 2 completed, 1 left in `running`, and 63 `pending`. This is an incomplete/stale rerun snapshot, not a second completed 66-configuration study.
- Preserve its log and manifest as failed/incomplete operational history. Do not merge its partial results into the original 66-row comparison or claim that all telemetry experiments completed.

### 10.3 Gate mapping

These experiments are relevant only as historical shared-engine integration evidence and possibly background for G4 exit hypothesis generation. They do not pass Phase 3 G1 (range event lifecycle), G2 (same Phase 3 signal cohort at multiple execution resolutions), G3 (range entry rules), G4 (frozen Phase 3 exits), G6, or G7. The full-sample matrix must not be used to pre-select Phase 3 parameters. Preserve the negative results and the incomplete telemetry run.

### 10.4 Cleanup disposition

Neither exit-experiment folder is approved for deletion. The 729-file original archive is a completed, reproducible historical negative finding; the 25-file telemetry archive records an incomplete rerun. Retain both unless a future dependency/provenance review establishes a safe archival move and the user approves it.


## 11. Gate 1 protocol and historical rejection-cohort reconciliation — 2026-11-25

### 11.1 Frozen lifecycle protocol

Committed `docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md` (commit `1ebf38c7febbe8f778935069b2344c344c345667`, clarified in `9ff63478ddc6a31aefaa17cbdf6eae38710a6322`) and overlap-cluster amendment `docs/research_checkpoints/2026-11-25_phase3_rejection_lifecycle_v1_1_overlap_cluster_amendment.md`.

It defines two separate descriptive modules:
- Module A: complete rejection lifecycle, distinct retest episodes, inward separation, boundary close-through/reclaim, repeated close-to-close crosses, and reuse of accepted signal-candle anatomy.
- Module B: breakout outside retest, 1M return-inside, completed-15M return-inside confirmation, breakout-side reclaim, inside retest after failure, and reversal-direction path.

The protocol freezes the source populations, time-zero/availability conventions, 10% primary boundary band and 20% rejection separation geometry, no-gap/no-lookahead rules, same-bar ambiguity, censoring, event de-clustering, output fields, synthetic test requirements, and stopping criteria. Module A has now passed its 12 synthetic tests and historical source/output audit. Its closeout is `reports/phase3_rejection_lifecycle_v1_1/PHASE3_REJECTION_LIFECYCLE_CLOSEOUT_V1_1.md`; workflow run 45627723414 succeeded and outputs are committed under `reports/phase3_rejection_lifecycle_v1_1/`. Module B remains open. No strategy PnL, entry/exit simulation, or parameter optimization is authorized.

### 11.2 Earlier rejection follow-up is superseded preliminary evidence

`docs/research/sideways_rejection_1m_followup_empirical_results_v1.md` and the 2026-11-22 provisional post-rejection checkpoint describe an older 1M follow-up and non-touch controls sampled by candle-range quartile. The older checkpoint explicitly records 2,095 cohort checks and says its outcome-calculation audit was pending. Later accepted anatomy specifications explicitly prohibit using the prior unreconciled 2,095-event cohort/results and establish the reproducible source population of 1,154 broad + 838 nested strict events (1,992 eligible rows across those nested cohorts).

**Disposition:** preserve the older report/checkpoints for historical provenance, but classify their results as superseded preliminary evidence, not accepted Phase 3 findings. Do not use their control comparison, counts, or outcome values in candidate design or Gate 2. The accepted anatomy/early-path and current lifecycle protocol use the reconciled event ledger and exact snapshot joins.

### 11.3 Immediate implementation order

1. **Completed:** reproduce and hash the accepted rejection source ledger, frozen feature snapshots, minute candles, and event anatomy inputs; run Module A and independently audit its 1,992 events, 3,028 episodes, 7,968 horizons, and 380 overlap clusters.
2. **Next:** reproduce and hash the accepted breakout classifications, links, original-source identity and minute candles.
3. Build and test Module B in isolation.
4. Run Module B under the frozen protocol, archive all event-level evidence, and issue the overall Gate 1 closeout. Do not advance to Gate 2 until Module B passes or is formally rejected.


## 12. Cross-repository and Phase 3 inventory update — 2026-11-25

### 12.1 Canonical repository snapshot

The full recursive tree for `islamomanpk-boop/okxtester@price-action-v1` was read at commit `e025e1188c266b2c678b47de7953a65aa0a4ee30`; GitHub reported no tree truncation. It contains 1,421 tree entries: 1,360 tracked blobs and 61 directories.

| Area | Current tracked files |
|---|---:|
| `.github/workflows/` | 34 |
| `data/market_1m/` | 5 |
| `docs/` | 163 |
| `reports/` | 1,001 |
| `research/` | 48 |
| `scripts/` | 1 |
| `src/` | 68 |
| `tests/` | 38 |
| Root files | 2 |
| **Total blobs** | **1,360** |

A broad Phase 3/sideways/breakout filename filter finds 43 research Python files, 36 test Python files, and 30 workflows. This is an inventory filter, not a count of 43 accepted studies: it includes historical diagnostics, matched-control versions, superseded scripts and provenance investigations. Do not treat every matching file as current evidence.

### 12.2 Supporting repository snapshot and role

The separate private repository `islamomanpk-boop/okxtester_private@main` was inspected at commit `ad5aac7294f0650e800ad834a1642f335915a649`; its recursive tree contains 12 tracked blobs and is not truncated:
- Three research scripts: `PHASE3_REMAINING_RESEARCH_PROGRAMME.md`, `phase3_range_measurement.py`, and `phase3_readiness_audit.py`.
- Nine workflows: aligned dataset build, download monitor, final data audit, Phase 3 range measurement, Phase 3 readiness audit, VPS data audit/health monitor, and two safe-cleanup variants.

The private repository's programme document explicitly marks itself as a historical condensed five-gate checklist and defers to the canonical eight-gate roadmap. Keep it as supporting documentation; do not copy it over the canonical roadmap.

### 12.3 Supporting workflow evidence and limits

- Range measurement run [45613180053](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45613180053) succeeded. Its script calculates exploratory ATR, Bollinger-width, rolling-range and momentum distributions from aligned 1M inputs aggregated into completed 15M, 4H and 1D bars. It is not an event ledger, signal generator, causal entry study or Gate 1 pass.
- Gate 0 read-only inventory run [45620563733](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45620563733) succeeded and uploaded artifact `okx-phase3-gate0-readiness-inventory`. The report status is inventory-only. It found one SQLite `candles` table with 2,890,411 rows and candle timestamps, but no signal/event timestamp field or signal/event table in the inspected database; no funding-history, fee-history/configuration or execution-engine candidate was found in the inspected VPS project/repository roots. This is scoped absence, not proof those resources do not exist elsewhere.
- Aligned dataset build run [45612158710](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45612158710), final data alignment audit [45611757117](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45611757117), and download/VPS monitor [45636441925](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45636441925) succeeded. These support data-pipeline/operational provenance only; they do not certify the Phase 3 event definitions or execution inputs.
- The canonical Termux funding-file audit closed G0-01/G0-02 for five audited local processed funding files. That evidence does not establish that the VPS runtime has the same files, nor does it close exact settlement-mark valuation, fee/instrument assumptions or engine-side real-input integration.

### 12.4 Phase 3 lifecycle evidence reconciled

P3-13 rejection Module A remains accepted as a descriptive study under its own closeout report. P3-14 breakout Module B's historical run and output-level independent audit are complete; formal closeout remains pending. The independent audit checkpoint records the exact event/horizon/group reconciliation and limitations. Gate 1 remains PARTIAL / OPEN. No Gate 2 execution-resolution study is authorized until the controlling Gate 0 and Gate 1 dependencies are accepted.

### 12.5 Remaining reconciliation work

1. Finish the formal Module B closeout against every frozen protocol criterion, including explicit disposition of the five lifecycle retest fields missing from the frozen forward benchmark.
2. Reconcile VPS SQLite/data-generation provenance and exact five-asset source/instrument identity with canonical 1M sources; do not assume the VPS and Termux environments are interchangeable.
3. Verify Phase 3 signal/event availability timestamps and the three-family candidate-generation design required by G0.
4. Close the remaining G0 funding mark-price, fee, instrument, and real-input engine integration blockers.
5. Complete the report-manifest and workflow/artifact provenance audit for the remaining Phase 3 studies. The 1,001-file reports directory has not been read file-by-file; this register is an evidence-backed index, not a claim that every archived report has been individually reviewed.


### 12.6 Module B follow-up workflow evidence — 2026-11-25

The corrected Module B workflow run [45643682550](https://github.com/islamomanpk-boop/okxtester/actions/runs/45643682550) completed successfully on commit `52e89472bf5ea39044376f9f5535e8a07eaa3dcc`: 21/21 synthetic tests passed; the frozen historical run and archive contract validation passed (1,592 events, 6,368 horizon rows, 454 overlap clusters); and the seven-file artifact was uploaded (ID `15036347661`). The output-commit step reported no further report changes.

The two artifact ZIPs from runs 45639123024 and 45643682550 have different SHA-256 digests. A file-level comparison found expected schema changes in the group-summary, horizon and metadata files: the newer version includes horizon-scoped outside/inside same-bar ambiguity columns and event-level totals (107 outside ambiguities, 551 inside ambiguities, 630 confirmed inside retests). The event-level, forward-crosscheck and prior-link report blobs retained their identities. Since the older run predates this schema amendment, this is not a same-code/same-schema determinism comparison. Byte-identical reproducibility on identical code/schema/inputs remains unproven and is a formal closeout item; do not call this a determinism pass.

The follow-up tests specifically add incomplete-horizon censoring and completed-15M failure-close availability coverage. The detailed checkpoint is `docs/research_checkpoints/2026-11-25_phase3_moduleB_independent_review_timing_finding.md`. Module B remains open; Gate 1 remains PARTIAL / OPEN; Gate 2 and strategy PnL backtests remain unauthorized.


### 12.7 Module B protocol regression run — 2026-11-25

Workflow [45644799449](https://github.com/islamomanpk-boop/okxtester/actions/runs/45644799449) passed all workflow stages on `d791361a7fea4aa448907de3dfb5d3559c194d60`. The checked-in test file contains 23 test methods and its synthetic-test step passed, including the added strict-within-broad nesting and duplicate source-event identity tests. Frozen historical generation, archive-contract validation, artifact upload and output-commit step also passed. Artifact ID `15036019010`.

All five principal output CSV SHA-256 values in run metadata match exactly between the corrected historical run at `52e89472bf5ea39044376f9f5535e8a07eaa3dcc` and this run. Cohort totals and ambiguity totals match. This demonstrates cross-revision output consistency, not yet a same-revision deterministic rerun; the latter remains an explicit closeout requirement. Module B and Gate 1 remain open, and no strategy PnL backtest is authorized.


### 12.8 Gate 0 inventory-tool improvement — pending execution

The supporting repository's read-only Gate 0 inventory script was extended at `okxtester_private@main` commit `1c64dcb82f6c61b0bd5016595b5942510054f540` to inspect bounded source/config text for relevant evidence keywords and CSV headers, while recording only file paths and matched terms—not source snippets, credentials, environment values or log contents. Large files and binary datasets remain excluded from content scanning. The inserted scan fragment passed a Python syntax parse, but the updated VPS workflow has **not** yet been observed running; no new VPS evidence or Gate 0 status change is claimed. This enhancement is an inventory aid only and cannot itself establish correctness or acceptance.


### 12.9 Gate 0 audit false-positive review and correction — 2026-11-25

The enhanced supporting-repository audit did run on commit `1c64dcb82f6c61b0bd5016595b5942510054f540`: workflow [45645509580](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45645509580) completed with a successful job and uploaded artifact ID `15036204100` (SHA-256 `3eb875027f2bc037463a49836a225dfe91243de4fa51f14c98a792c614207846`). The SQLite quick check was `ok`; the inspected database had one `candles` table with 2,890,411 rows and only candle columns (`inst_id`, `ts`, OHLCV/quote-volume fields and `confirm`).

However, the first content scan produced **false-positive evidence candidates in all six categories**. Review of the job log and code found that the scanner inspected its own audit script, whose category-token definitions matched themselves, and its evidence helper accepted a keyword hit from any category. A generic `order` token also caused the downloader file to be labelled as an execution-engine candidate. Therefore, the six category statuses from run 45645509580 are invalid as evidence and must not be used to suggest that event data, signal timestamps, funding, fees, provenance or an execution engine were found. The only directly observed runtime fact from this run is the SQLite integrity/table inventory and the bounded candidate-file list.

A correction was committed to the supporting script at `okxtester_private@main` commit `f7c692f2e24b89cde46fd79934254a51741af326`: it excludes the audit script from its own scan, scopes content hits to their declared category, removes generic execution tokens, and allows large CSV files to be inspected by header only while continuing to skip large non-CSV files. **This correction has not yet been confirmed by a subsequent workflow run.** The workflow's optional notification step also logged a malformed-URL error; it is marked continue-on-error, so the overall run/job still concluded successfully. Gate 0 remains CONDITIONAL HOLD; no acceptance change is made.


### 12.10 Module B same-revision reproducibility — confirmed

The repeat run previously missed in the status note is [workflow 45645349572](https://github.com/islamomanpk-boop/okxtester/actions/runs/45645349572), on commit `90d0d5417830fac50a712c4418b6cb65e86c7a1f`. It completed successfully, all 23 synthetic tests passed, the frozen historical workflow completed, and the final output-commit step reported `No report changes to commit.`

A commit comparison from the prior successful analysis revision `d791361a7fea4aa448907de3dfb5d3559c194d60` to `90d0d5417830fac50a712c4418b6cb65e86c7a1f` shows only one workflow-comment change and two documentation changes; the analysis script, test file, frozen input files and report schema were unchanged. The repeat run therefore regenerated the same checked-in research outputs byte-for-byte. The ZIP artifact digests differ (`sha256:3005665e...` versus `sha256:1e2929e5...`), which is packaging-level variation and not a research-output difference; the workflow's no-change output commit is the direct evidence that generated report files were identical. **The same-source / same-test / same-input / same-schema reproducibility criterion is now confirmed.** This supersedes the still-open reproducibility wording in Sections 12.6–12.7.

Module B is not yet formally closed: the five outside-retest lifecycle fields remain absent from the frozen forward archive and are accepted only as descriptive measurements pending an explicit closeout disposition. A formal Module B closeout report and full criterion-by-criterion sign-off remain outstanding. Gate 1 remains PARTIAL / OPEN; Gate 2 remains closed.


### 12.11 Corrected VPS Gate 0 inventory — 2026-11-25

The corrected read-only audit was rerun after excluding self-matches, scoping hits to their own category, and separating downloader code from provenance records. Supporting workflow [45647247070](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45647247070) completed successfully on `okxtester_private@main` commit `87e80fbb71d2ffae0d7498bf17384807aec7b356`; all workflow steps, including the optional notification, passed. Artifact ID `15039230361`, SHA-256 `1eb0fb314193bb90fba2fbf0e1d243464e27f310e43e27e38eec4ce033a058fc`.

The corrected inventory found **no candidate evidence** in the inspected VPS/project/repository roots for event data, signal timestamps, funding history, fees, source-provenance records or an execution engine. The SQLite quick check remained `ok`; the inspected database still contained one `candles` table with 2,890,411 rows and only instrument/time/OHLCV/confirmation columns. The candidate file list included `download_okx.py` and five large per-asset 1M CSVs, but the presence of a downloader script is not proof of archived source provenance or of a working Phase 3 signal/event pipeline. CSV headers and bounded candidate source/config text were scanned; large non-CSV data and binary files were not read as text.

This is scoped negative inventory evidence, not proof that resources do not exist outside the inspected roots or that the downloader is invalid. It strengthens the case that the VPS runtime currently lacks discoverable event/signal, funding, fee, provenance-record and execution-engine inputs at those inspected locations. It does **not** change Gate 0: CONDITIONAL HOLD. Required next work remains source/event timestamp integration, funding runtime integration and settlement mark policy, fee/instrument verification, and execution-engine real-input readiness. No strategy backtest is authorized.


### 12.12 Module B formal closeout and Gate 1 decision — 2026-11-25

Formal closeout report committed at `reports/phase3_breakout_lifecycle_v1_1/PHASE3_BREAKOUT_LIFECYCLE_CLOSEOUT_V1_1.md` (commit `40550c71962a503facafe5e8e62216879344bc3b`). Module B V1.1 is **ACCEPTED as descriptive lifecycle evidence**, with the five outside-retest fields explicitly limited to descriptive-only measurements because they are absent from the frozen forward archive. The report records source reproduction, 1,592-event cohort, 6,368/6,368 forward cross-check rows across 18 available fields, 23/23 synthetic tests, 6,368 complete horizon rows, ambiguity and overlap counts, and same-revision deterministic-output evidence.

Together with the previously accepted Module A rejection lifecycle closeout, the descriptive lifecycle scope in Gate 1 is now **COMPLETE**. This does not pass Gate 0 or authorize Gate 2. Gate 0 remains CONDITIONAL HOLD; Gate 2 execution-resolution research, Gate 3 entries, Gate 4 risk/management, Gate 5 engine acceptance, Gate 6 strategy PnL backtests and Gate 7 OOS validation remain closed/not authorized in sequence. Phase 1 remains paused. The next active work is Gate 0 blocker resolution only.


### 12.13 Expanded Gate 0 inventory precision and market-source provenance correction — 2026-11-25

The supporting read-only Gate 0 audit was expanded at `okxtester_private@main` commit `dba90a7cee4c4508325da16fcf0aab2f972178a4` to include generic source/config formats (`.toml`, `.yaml`, `.yml`, `.ini`, `.cfg`) and CSV headers even when filenames do not contain evidence keywords. It records the number/suffixes scanned and large non-CSV skips; CSV scanning is header-only and tolerates a UTF-8 BOM. Workflow [45648685046](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45648685046) completed successfully but surfaced a false positive: the generic word `reclaim` in unrelated `.github/workflows/safe-vps-cleanup.yml` was labelled as possible event evidence. That category result was rejected, not counted as evidence.

The event category was narrowed to explicit ledger/timestamp identifiers (`event_ledger`, `event_data`, `breakout_event`, `rejection_event`, `range_event`, `signal_event`, `event_timestamp`) at commit `2c52e8d18a4c5c53f3b484f874789cdc01df955c`. Corrected workflow [45648774228](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45648774228) completed successfully; all steps passed. It reported no candidate evidence in any of the six categories (event data, signal timestamps, funding history, fees, source provenance, execution engine), and no static content keyword hits in the expanded scan. This remains a scoped read-only inventory of the configured VPS/project/repository roots and file types; it cannot prove absence outside those roots, discover untracked runtime state beyond its inventory rules, or validate the semantic correctness of any future candidate. Artifact ID `15037889283`, SHA-256 `25e632075729b7e4a94ba6c5d8cc5f98d24eb42251c66d6527e58587ea6bc4ad`.

G0-10 documentation correction: `docs/execution_data_audit_v1.md` now explicitly distinguishes its historical local-input snapshot from the current tracked canonical source. The five files under `data/market_1m/` are tracked in the canonical Git tree. Their exact paths, byte sizes, Git blob IDs and SHA-256 values are recorded in the corrected document and Module B run metadata. This closes the documentation contradiction only; VPS-to-canonical downloader lineage, refresh controls and runtime equivalence remain unverified. No source files were changed or deleted.

Gate 0 remains CONDITIONAL HOLD. No Gate 2 execution comparison or strategy backtest is authorized.


### 12.14 Phase 3 candidate availability/source timing audit — 2026-11-25

Read-only source/timestamp audit committed at `docs/research_checkpoints/2026-11-25_phase3_candidate_availability_audit_v1.md` (commit `e3325daff6672f5aeede2ab0b47f30395ecbeb3f`). It confirms the accepted rejection lifecycle's 15-minute rejection-candle close convention (`first_strong_rejection_ts_ms + 900000`), 4H snapshot availability metadata, and the recovered breakout script's completed 15M close labels, completed 4H context, backward as-of join, and first eligible 1M bar opening at the 15M close timestamp.

A material live-causality blocker is made explicit: `research/sideways_detector_original_v1.py:classify_asset()` calculates P25/P40/P50 channel-width thresholds across the **entire feature sample** and applies them retrospectively. The historical strict/broad labels and breakout cohorts therefore remain descriptive classifications, not live-knowable regime signals. A past-only threshold/calibration policy must be separately frozen before candidate generation. Failed-breakout reversal's proposed earliest confirmation is the completed 15M return-inside close, with opposite breakout direction; this remains a candidate-definition proposal, not an accepted trading rule.

The checkpoint records a minimum candidate-record contract and seven pre-implementation decisions. G0-04/G0-05 remain OPEN / CRITICAL; no candidate generator, execution comparison or strategy backtest is authorized. This audit does not invalidate either accepted descriptive lifecycle closeout.


### 12.18 VPS downloader static semantic review — 2026-11-25

Read-only AST inspection of the VPS `download_okx.py` source is recorded in `docs/research_checkpoints/2026-11-25_phase3_vps_downloader_static_semantic_review.md`. The inspected source SHA-256 is `b2cd563b373ca613e8e26a6a08e628f76a88ad3f927e10000a084279c4f28a01`, matching the preceding file fingerprint checkpoint. Workflow run `45652223245` completed its static inspection and produced sanitized artifact `15040652836`.

The source constructs the five `{asset}-USDT-SWAP` instrument IDs, requests 1M history candles using `instId`, `bar`, and `limit`, and uses the `after` pagination cursor. The request layer has up to eight attempts, a 30-second timeout, exponential delay capped at 30 seconds, checks API response code, and returns response data. The historical loop requires nine-field rows, casts row[0] to integer timestamp, and advances backward using the oldest timestamp with a no-progress guard.

The nine-field API response is mapped positionally into SQLite: row[0] timestamp; row[1:5] OHLC; row[5] `vol`; row[6] `vol_ccy`; row[7] `vol_ccy_quote`; row[8] integer `confirm`. The schema preserves all three volume fields separately. This does not establish their units or downstream suitability. The source uses SQLite `executemany` and commits, but the exact conflict clause and export SELECT/confirmed-only predicate remain unverified because SQL placeholders were redacted in the structural report. Timestamp end-to-end conversion/serialization also remains open.

Gate 0 remains CONDITIONAL HOLD. Source snapshot fingerprint and row-to-column mapping are identified, but historical acquisition-version lineage, exact CSV projection/filter, SQLite conflict/update policy, volume units, timestamp end-to-end semantics, and canonical Git snapshot byte identity remain unresolved. No candidate generation, Gate 2 execution comparison or PnL backtest is authorized. The inspection was static only: no downloader execution, OKX API request, database query/write, VPS modification, service change or cleanup.


### 12.19 VPS downloader SQL, update and CSV export semantics — 2026-11-25

A second read-only AST pass preserved sanitized SQL structure and completed the VPS downloader source review. Checkpoint: `docs/research_checkpoints/2026-11-25_phase3_vps_downloader_sql_export_update_semantics_v1.md`. Supporting workflow [45654166874](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45654166874) completed successfully on `okxtester_private@main` commit `7cbd0b171affbaa31dd4f437f35ccb114e5597ad`; artifact `15042235920`, SHA-256 `a09bba18e44e5e48c52bde379ba92d39cd0714703ee4d0f7c7646ddda63f3e3a`. The inspected VPS downloader SHA-256 remains `b2cd563b373ca613e8e26a6a08e628f76a88ad3f927e10000a084279c4f28a01`.

The exact SQLite insert uses `ON CONFLICT(inst_id, ts) DO UPDATE` and replaces OHLCV, all three volume fields, and `confirm` on a duplicate key. Therefore the VPS database is a mutable latest-state store, not an immutable download ledger; a later response can update a previously stored candle. The exact export query selects `ts, open, high, low, close, vol, vol_ccy, vol_ccy_quote, confirm`, filters to the requested instrument, `confirm=1`, and `ts>=START_MS`, and orders by timestamp ascending. The timestamp is retained as an integer without conversion to seconds; gap checks use 60,000-unit one-minute intervals. The raw database count is separately reported from the confirmed/start-bounded CSV count.

This closes the downloader source-code understanding items for the conflict/update clause and export projection/filter. It does not prove runtime database contents, immutable history, current VPS CSV byte identity with canonical Git data, timestamp provenance beyond source/API semantics, or volume-unit suitability. Gate 0 remains CONDITIONAL HOLD; no candidate generation, Gate 2 execution comparison, strategy PnL backtest, or Phase 1 handoff is authorized. Inspection was static only; no VPS data or services were changed.


### 12.20 VPS downloader start boundary and exact CSV headers — 2026-11-25

A further read-only AST extraction captured safe module constants and the exact CSV header list. Supporting workflow [45654783334](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45654783334) completed successfully on `okxtester_private@main` commit `39f144b9549fa82041380208adb083d5e76530c3`; artifact `15040529786`, SHA-256 `d8075dba2d6d3685583fb634b3b24e65fef67c2564d128594741ed51ec1fd92c`. The downloader source fingerprint remained `b2cd563b373ca613e8e26a6a08e628f76a88ad3f927e10000a084279c4f28a01`.

The downloader's configured start is `2025-10-20 00:00:00 UTC`, converted to milliseconds by `int(START.timestamp() * 1000)`. Its exact CSV header order is `ts, open, high, low, close, vol, volCcy, volCcyQuote, confirm`. The two API volume headers map positionally to SQLite's `vol_ccy` and `vol_ccy_quote` columns. The start boundary matches the first timestamp in the separate five-asset funding manifest, but does not by itself prove the first market-candle timestamp or VPS-to-canonical file identity. Full details are appended to the downloader SQL/export checkpoint.

Gate 0 remains CONDITIONAL HOLD. This is source-constant evidence only; no VPS data, services, or files were changed.


### 12.21 VPS market CSV snapshot and SQLite confirmation reconciliation — 2026-11-25

A metadata-only, read-only audit of the five actual VPS exports is recorded in `docs/research_checkpoints/2026-11-25_phase3_vps_market_csv_snapshot_audit_v1.md`. Supporting workflow [45655914596](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45655914596) completed successfully on `okxtester_private@main` commit `01110f9a8e9e5e61d0db4271a3220a6aa2fa8250`; artifact `15042212515`, SHA-256 `3fe4e98476f906435ef3a6e383a0fdea5389d1a29222cdfdd9102d9c578bfd45`. The workflow streamed CSV metadata and queried SQLite in read-only mode; it uploaded no raw market data.

All five VPS exports have the expected nine-column header and begin at 2025-10-20 00:00 UTC. Exported row counts are BTC 578,022; ETH 578,051; SOL 578,080; DOGE 578,111; AVAX 578,141. No duplicate or out-of-order timestamps, malformed rows, invalid timestamps, invalid OHLC, or invalid volume fields were found. The CSV end timestamps differ across assets (BTC 09:41, ETH 10:10, SOL 10:40, DOGE 11:10, AVAX 11:40 UTC on 2026-11-25), so this snapshot still needs explicit cross-asset timestamp-set reconciliation.

SQLite contains 2,890,411 rows. Per-instrument CSV row counts exactly equal the SQLite counts where `confirm=1`. There are six `confirm=0` rows: one latest incomplete row for each asset, plus a historical SOL row at 2026-08-28 08:30 UTC. That historical SOL row exists in SQLite but is excluded by the confirmed-only CSV predicate, creating the single internal one-minute gap between 08:29 and 08:31 UTC. It must not be imputed or silently relabelled. A narrow current-OKX endpoint check is required to determine whether this historical flag is stale.

The monitor run [45647566750](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45647566750) had reported 5/5 download completion and no running downloader process at 15:39 UTC. The VPS export is a distinct, later, nine-column snapshot than the earlier canonical Git market dataset; do not overwrite the canonical snapshot or treat the file hashes as directly comparable across different schemas/windows.

Gate 0 remains CONDITIONAL HOLD. Next: verify the historical SOL confirmation flag against the current public OKX history-candles response, then perform full five-asset timestamp alignment and source reconciliation. No VPS data was changed; no candidate generation, Gate 2 execution comparison, strategy PnL backtest, or Phase 1 handoff is authorized.


### 12.22 Historical SOL non-confirmed candle verified against current OKX API — 2026-11-25

The historical SOL timestamp responsible for the single internal gap in the confirmed-only VPS CSV was checked against the current public OKX history-candles endpoint. Supporting workflow [45656418316](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45656418316) completed successfully on `okxtester_private@main` commit `48c93964070bbf5634291872dc38e886f4771ce8`; artifact `15042463198`, SHA-256 `832935bdd17e86a412fcb64135cbb4d30ada0f79b50c88db4aaec8627b3d6081`.

For SOL-USDT-SWAP at 2026-08-28 08:30:00 UTC (`1787905800000` ms), the API returned the exact row with HTTP 200 / API code 0 and `confirm=0`. OHLC, `vol`, `volCcy`, and `volCcyQuote` all matched the read-only SQLite row exactly; SQLite also had `confirm=0`. The gap in the confirmed-only CSV is therefore consistent with the exchange's current response and the downloader's `confirm=1` export filter. It is not a local missing row or a demonstrated downloader/export mismatch.

The reason the exchange still marks this old candle unconfirmed is unknown. Preserve the source flag; do not relabel, impute, or modify the VPS row. The checkpoint's disposition is updated accordingly. Gate 0 remains CONDITIONAL HOLD; cross-asset timestamp alignment and the remaining source/execution readiness blockers remain open.


### 12.23 VPS five-asset timestamp-set alignment — 2026-11-25

The explicit streaming timestamp-set comparison is recorded in `docs/research_checkpoints/2026-11-25_phase3_vps_market_csv_snapshot_audit_v1.md`. Supporting workflow [45656654156](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45656654156) completed successfully on `okxtester_private@main` commit `93dd76ff5340e6d1a84d7c7ac1c7131f3eef48c5`; metadata-only artifact `15042707158`, SHA-256 `cd9538989b3a2bd97fd62c459844f421ad2ddfd5944e6b39792a89ed03fa446b`.

The five VPS CSVs have a 578,021-timestamp intersection from 2025-10-20 00:00 UTC through 2026-11-25 09:41 UTC. Their union contains 578,141 timestamps; 120 timestamps lie outside the intersection. Per-asset non-common counts are BTC 1, ETH 30, SOL 59, DOGE 90, AVAX 120. These differences are fully explained by the historical SOL 2026-08-28 08:30 UTC candle that the exchange currently returns with `confirm=0`, plus staggered per-asset final timestamps. The common intersection therefore retains one explicit one-minute hole; no timestamp was imputed.

This completes the timestamp-set characterization of the current VPS snapshot, not its adoption as the canonical research source. It remains a later, separately structured snapshot and still requires OHLCV-level reconciliation with canonical Git data and a versioned source-use decision. Gate 0 remains CONDITIONAL HOLD; no candidate generation, Gate 2 execution comparison, strategy PnL backtest, or Phase 1 handoff is authorized.


### 12.24 Canonical Git vs VPS OHLCV and volume-unit reconciliation — 2026-11-25

The full five-asset overlap comparison is recorded in `docs/research_checkpoints/2026-11-25_phase3_vps_canonical_ohlcv_reconciliation_v1.md`. Supporting workflow [45657820585](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45657820585) completed successfully on `okxtester_private@main` commit `0b798e4def1bd58ff3dbc1612c53fc0e5a986cd0`; artifact `15044456441`, SHA-256 `defe522a466fee197dc36a42cc08889dbc7f16d76468703b5d99771a1e5278e0`. Canonical files were pinned to `okxtester@d7502306e89b0b78980eb9e3c8a39570b3b05966`; both canonical and VPS file hashes matched their recorded manifests.

Every matched timestamp has exact Decimal OHLC equality across all five assets. Matched counts: BTC 569,125; ETH 569,125; SOL 569,125; DOGE 569,126; AVAX 569,127. No OHLC mismatch or non-monotonic timestamps were found. Canonical-only timestamp count is zero for BTC, ETH, DOGE, AVAX and one for SOL: 2026-08-28 08:30 UTC, the known exchange-returned `confirm=0` row that the confirmed-only VPS export excludes. That SOL row's canonical OHLC and volume match the read-only SQLite row.

Crucially, canonical Git `vol` equals VPS `volCcy` exactly on every matched timestamp across all five assets. OKX's official V5 candle schema defines derivative `vol` as contract quantity, `volCcy` as base-currency quantity, and `volCcyQuote` as quote-currency quantity. Thus canonical Git `vol` is base-currency volume, not contract count. This resolves the generic volume-field ambiguity for this dataset pair. The execution-data audit documentation has been updated to require explicit volume-unit labels and normalization for cross-asset volume features.

The VPS snapshot starts earlier and ends later than the canonical Git snapshot; it is not a replacement or byte-identical copy. Exact overlap-value equality does not recover the missing contemporaneous hashes of original Termux inputs or close full upstream acquisition provenance. Preserve both snapshots separately. Gate 0 remains CONDITIONAL HOLD; no candidate generation, Gate 2 execution comparison, strategy PnL backtest, or Phase 1 handoff is authorized.


### 12.25 Full-window public funding mark-price coverage — 2026-11-25

The full audit is documented in `docs/research_checkpoints/2026-11-25_phase3_full_window_mark_price_coverage_audit_v1.md`. It uses the committed PASS funding coverage manifest (SHA-256 `59c08bb34ac82e00e60066dad7e50d0cc62b4097a3580e186251a6c23de67c7e`) to reconstruct the verified 1,188 funding timestamps per asset for 2025-10-20 00:00 UTC through 2026-11-19 16:00 UTC. Public OKX 4H historical mark candles matched all 5,940 funding timestamps exactly: 2,375 candles per asset, all confirmed, zero gaps, zero missing event-time candles. A 60-point 1M mark-candle sample also returned 60/60 exact rows; the 1M mark open equalled the 4H mark open exactly at every sample point.

The VPS run compared all 5,940 events with the full VPS 1M trade dataset. An independent hosted-runner run against canonical Git data reproduced identical mark-candle coverage and 1M cross-resolution sample values; it had 1,185/1,188 trade-candle matches per asset because canonical Git data excludes three start/end boundary events. Pooled mark-4H-open versus trade-1M-open difference had mean absolute 0.650 bps (p05 -2.073, p95 +1.072, p99 +2.122). Mark-4H-open versus trade-1M-close had mean absolute 7.514 bps (p05 -16.217, p95 +15.428, p99 +29.380; observed maximum +363.923 bps). This supports the 4H mark-candle open at the exact funding timestamp as the best-supported public proxy candidate, not as an exact settlement mark.

Main audit run [45659424729](https://github.com/islamomanpk-boop/okxtester/actions/runs/45659424729) passed on commit `fc1e030d95a1c4cbd6a4ca4c46b3640d2d152ef4`, artifact `15043858498`, SHA-256 `632501e666f91c4b7d5b3f88a0345077d986923d308624be874bf370c1250dea`. VPS audit run [45659811546](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45659811546) passed on workflow commit `2d44491649408d89f9c370ca32ed49b5138eaec1`, artifact `15045165371`, SHA-256 `55f1330f735323b1353ca424ee101090bab7f9754432d7fb0858a172c89a76f5`. Synthetic helper tests [45659424766](https://github.com/islamomanpk-boop/okxtester/actions/runs/45659424766) passed.

Recommended but not yet accepted: add a clearly labelled `mark_candle_open_proxy` mode, retain `candle_close_proxy` as a sensitivity comparator, and keep `exact` mode fail-closed without an independently verified settlement mark. No engine mode was changed. The account-bills `px` field for funding-fee bill subtypes 173/174 remains the best candidate for independent realized-settlement validation; no production account bills were accessed. G0-03/G0-09 remain OPEN, Gate 0 remains CONDITIONAL HOLD, and Phase 3 strategy PnL backtests remain unauthorized.


### 12.26 Versioned public mark-price candidate snapshot archived — 2026-11-25

The 5,940-row event-time 4H mark-price dataset from Section 12.25 has been committed to `data/funding_mark_price_proxy_candidate_v1/`:
- CSV: `mark_price_at_funding_4h.csv`
- SHA-256: `22e2894a8c467777f9ee90d5824deaf243a8b3d6e44ebff7f7d33b3e88c4cc82`
- Git blob SHA-1: `7fa9f40cf189193fcd855578f5b7d89600e86e08`
- Size: 396,308 bytes; 1,188 rows per asset; all confirmed.
- Commit: `adaf25d7a27c1e01def1a14a011c99be99186c67`.
- README and manifest are committed alongside the CSV.

The snapshot hash was independently reproduced byte-for-byte by the hosted-runner and VPS-runner audits. The manifest explicitly records `exact_settlement_mark_verified=false`, `funding_proxy_policy_accepted=false`, and `engine_mode_changed=false`. This is an additive candidate research input only; it does not change the current execution engine, close G0-03/G0-09, or authorize PnL backtests.


### 12.27 G0-05 independent source identity, causal disposition and lifecycle verification — 2026-11-28

Step 22 is complete. The independent standard-library verifier at `research/phase3_g0_05_independent_source_verification_v1.py` imports neither the canonical candidate contract nor the primary source-audit implementation. Final workflow [46148537294](https://github.com/islamomanpk-boop/okxtester/actions/runs/46148537294) completed successfully on `price-action-v1` commit `8744a1981237f3aabfe73bacf3cc8bdfa5bb295f`. Evidence artifact `15264717673` (`phase3-g0-05-source-audit-46148537294`) has ZIP SHA-256 `865c8a1a5cf0fc2e0ce9a85df14200d64054738c063275f7ce675d471af48974`.

Independent results:
- Rejection: 1,154 physical identities / 1,992 nested cohort memberships; 1,083 eligible, 31 rejected, 40 expired. The independent check rebuilt source identities, memberships and causal dispositions; accepted Module A cluster IDs remain verified by the primary audit rather than independently re-clustered here.
- Breakout: all 2,861 raw crossings reconcile exactly once; P25/P40 causal flags and dispositions independently recomputed; 1,037 half-open 12-hour interval clusters rebuilt from raw 1M timestamps (BTC 220, ETH 201, SOL 212, DOGE 193, AVAX 211); 1,038 eligible and 1,823 rejected.
- Failed breakout: 1,592 Module B cohort rows collapse to 932 physical identities; all 932 source links and causal-source-cohort inheritance reconcile; the strict half-open 12-hour lifecycle is checked. One observed return-inside exactly at +12h is excluded from canonical confirmation. Final dispositions: 735 eligible, 30 rejected, 167 expired.
- Across the three source-only ledgers: 4,947 rows, 2,856 eligible, 1,884 rejected and 207 expired. These are source disposition rows, not 4,947 independent physical events.

The complete evidence, scope and limitations are recorded in `docs/research_checkpoints/2026-11-28_g0_05_independent_source_verification_closeout_v1.md`.

**Gate boundary:** Step 22 completion does not close G0-05 or Gate 0. The source-only ledgers are not canonical candidate rows; real candidate IDs and failed-breakout source candidate IDs remain unmaterialized. The 60-field contract has synthetic validation only. G0-05 remains OPEN / CRITICAL, Gate 0 remains CONDITIONAL HOLD, and Gate 2+ / strategy PnL backtests remain unauthorized. The next safe task is a read-only pre-generation review reconciling the older field-mapping matrix with the later frozen field-value decisions and confirming family-specific nullability/identity rules before any separately approved canonical build.


### 12.28 G0-05 pre-generation contract review and family-specific source semantics — 2026-11-28

The read-only pre-generation review compared `CANONICAL_REQUIRED_FIELDS`, the canonical serializer and the field-mapping matrix. All 60 required fields are present exactly once in the serializer, with no missing or extra keys; the matrix explicitly covers all 60 fields after adding the grouped overlap-window and NOT_APPLICABLE invalidation mappings.

The review identified that the row validator previously accepted any globally allowed source-reconciliation status/cardinality combination for any family. The validator now enforces:
- Rejection: `EXACT_PHYSICAL_EVENT_COLLAPSE` / `ONE_PHYSICAL_EVENT_TO_ONE_OR_TWO_COHORT_ROWS`, BROAD_P40 membership, one or two source cohort IDs.
- Breakout: `EXACT_SOURCE_MATCH` / `ONE_RAW_CROSSING_TO_ONE_DISPOSITION`, exactly one raw source row ID.
- Failed breakout: `EXACT_LINKED_SOURCE_BREAKOUT` / `ONE_FAILED_BREAKOUT_TO_ONE_SOURCE_BREAKOUT`, one or two cohort IDs plus exact source-breakout linkage/inheritance.

Contract commit `e1affcb1ed585546e181fb4ab7332f0c844f4d45`; tests commit `a2479ed6496f7e698c0f43d940573f7f77cc152f`. Push-triggered synthetic workflow [46149074209](https://github.com/islamomanpk-boop/okxtester/actions/runs/46149074209) completed successfully: **193/193 tests passed**.

**Pre-generation contract review: PASS for these static mapping and family-specific validator checks. Canonical build: HOLD — not authorized.** No real candidate IDs or canonical candidate rows have been generated. G0-05 remains OPEN and Gate 0 remains CONDITIONAL HOLD. The next step requiring project-owner authorization is a separately scoped real canonical candidate/disposition build and real-row validation/artifact review; this does not authorize execution simulation, Gate 2+, strategy PnL backtesting or live trading. Full details and independent-verifier limitations are in `docs/research_checkpoints/2026-11-28_g0_05_independent_source_verification_closeout_v1.md`.


### 12.29 Owner-authorized real G0-05 canonical candidate ledger — 2026-11-28

The project owner explicitly approved real canonical candidate/disposition generation. Normal push-triggered workflow [46149804561](https://github.com/islamomanpk-boop/okxtester/actions/runs/46149804561) succeeded on commit `26ac706767d3f9b490cfa2b8250c13417f46b356`. Artifact `phase3-g0-05-canonical-candidate-ledger-46149804561`, ID `15265550848`, ZIP SHA-256 `e66ea4b16811d158a9b86dfb90113be13cc5fccfc89f1c42b5330fba294456da` (2,587,810 bytes).

The corrected workflow reverified the frozen G0-04 archive, reran the primary source audit and independent source identity/lifecycle verifier, then generated and validated 4,947 real canonical records with exactly 60 fields each. Family counts: SUPPORT_REJECTION 558; RESISTANCE_REJECTION 596; BREAKOUT_CONTINUATION 2,861; FAILED_BREAKOUT_REVERSAL 932. Aggregate dispositions: 2,856 eligible, 1,884 rejected, 207 expired, 0 censored. Rejection: 1,083/31/40 eligible/rejected/expired; breakout: 1,038/1,823/0; failed breakout: 735/30/167. All deterministic IDs, unique family/source identities, full record/ledger checks and 932/932 failed-breakout source-candidate links passed.

Canonical output hashes:
- JSONL `202c44f456af021b9ec8cc642e82c349f4858baadb04bcdb2342973cb752db14`
- CSV `eca9f326bc44a74ba9631bc6b5d4a6c7b5691fea6b59c7031976f7fd7f5ff1a5`

The first real-row attempt exposed a real-data mapping issue: absent historical cohort membership was emitted as the sentinel `NONE`, but the canonical schema expects an empty list. The source mapper was corrected; the successful run reran all upstream checks and the canonical build. No ledger was emitted by the failed attempt.

Detailed checkpoint: `docs/research_checkpoints/2026-11-28_g0_05_canonical_candidate_ledger_build_v1.md`.

**Gate status:** the real canonical build and real-row validation step is complete. G0-05 remains pending final read-only post-build evidence review before formal closure. Gate 0 remains CONDITIONAL HOLD; funding/settlement mark, fees/instrument assumptions, standalone sizing, contract rounding, stop-gap risk and execution-engine acceptance remain separate blockers. No execution simulation, orders, fills, PnL, strategy comparison, Gate 2+ or live trading was performed or authorized.


### 12.30 Final G0-05 canonical ledger and independent post-build review — 2026-11-28

The authoritative final workflow is [46150045661](https://github.com/islamomanpk-boop/okxtester/actions/runs/46150045661), SUCCESS on commit `19a6325780693696890f9f3493a713702e8a8f7f`. It reran the pinned G0-04 ZIP verification, primary source audit, independent source identity/lifecycle verifier, real canonical build/full validator and a separate independent post-build reviewer.

Artifact: `phase3-g0-05-canonical-candidate-ledger-46150045661`, ID `15265023491`, ZIP SHA-256 `0b9464cbeda0a513cea915aae78a1c43aab2b5563448a0e19b247c02b4081935` (2,588,629 bytes). Complete source manifest ID: `8458ca73f07db7d3ff4517123dd0d6b33acb39e99174ecd39056b585a9988c82`.

Final ledger: 4,947 real records, exactly 60 fields each. Family totals: SUPPORT_REJECTION 558; RESISTANCE_REJECTION 596; BREAKOUT_CONTINUATION 2,861; FAILED_BREAKOUT_REVERSAL 932. Dispositions: 2,856 eligible, 1,884 rejected, 207 expired, 0 censored. All candidate IDs recomputed deterministically; family/source identities unique; full row and ledger validators passed; all 932 failed-breakout links/inherited fields passed.

Independent post-build reviewer status: `G0_05_POST_BUILD_EVIDENCE_REVIEW_PASS`. It independently checked the 60-field shape, JSONL/CSV semantic equivalence, canonical output hashes, source-manifest identity, source-to-canonical exact-once reconciliation, deterministic candidate IDs, disposition totals, and all 932 failed-breakout source links and inherited fields.

Canonical file hashes:
- JSONL: `387d376bc269587de6fb48686641cd27e885a2d3bd6c6a8ae96a9a9dd61333d8`
- CSV: `325c714e5923612a711d18a855d1540e1f59b27d26d65636ebabd7578c81bb43`

Detailed checkpoint: `docs/research_checkpoints/2026-11-28_g0_05_independent_source_verification_closeout_v1.md`; dedicated build checkpoint: `docs/research_checkpoints/2026-11-28_g0_05_canonical_candidate_ledger_build_v1.md`.

**Technical disposition:** G0-04 is ACCEPTED. G0-05 implementation, real canonical generation, full validation and independent post-build review are technically complete and READY FOR FORMAL CLOSEOUT. The project owner authorized generation; formal G0-05 acceptance has not yet been recorded and should not be inferred. Gate 0 remains CONDITIONAL HOLD due to independent funding/settlement-mark, fee/instrument, sizing/rounding/gap-risk and execution-engine acceptance blockers. No execution simulation, orders, fills, PnL, Gate 2+ or live trading was performed or authorized.


### 12.31 G0-05 technical acceptance — 2026-11-28

G0-05 is now **ACCEPTED — TECHNICAL CLOSEOUT COMPLETE** under `docs/research_checkpoints/2026-11-28_g0_05_acceptance_decision_v1.md`. The disposition is an assistant technical acceptance based on the owner's explicit canonical-build authorization and complete source, real-row and independent post-build evidence; it is not a human reviewer sign-off.

Accepted scope: frozen source provenance and causal dispositions; three-family source-to-canonical reconciliation; 4,947 real records with exactly 60 required fields; deterministic IDs and uniqueness; full canonical row/ledger validation; 932/932 failed-breakout source links and inheritance; independent post-build review of JSONL/CSV equivalence, output hashes, source-manifest identity, exact-once reconciliation and dispositions.

Final evidence remains workflow [46150045661](https://github.com/islamomanpk-boop/okxtester/actions/runs/46150045661), artifact ID `15265023491`, ZIP SHA-256 `0b9464cbeda0a513cea915aae78a1c43aab2b5563448a0e19b247c02b4081935`.

**Gate 0 remains CONDITIONAL HOLD — not passed.** G0-03 real-input funding/settlement-mark acceptance, G0-07 standalone sizing/rounding/gap risk, G0-08 fee/instrument assumptions and G0-09 exact settlement-mark/execution-engine readiness remain separate blockers. Gate 2+, strategy PnL backtests, orders, fills, execution simulation and live trading remain unauthorized.


### 12.32 G0-03 funding contract integration progress — 2026-11-28

Added standalone/portfolio funding arithmetic parity tests and a read-only local real-input integration harness that exercises the production funding loader and contract validator. It verifies the actual five CSV hashes against the archived manifest, exact scheduled settlement rows, cross-asset timestamp equality, and entry-exclusive/exit-inclusive trade-window boundaries without running trades or calculating PnL.

Funding/execution workflow [46150715018](https://github.com/islamomanpk-boop/okxtester/actions/runs/46150715018) passed **90/90 tests**. New files: `src/test_funding_engine_parity.py`, `src/audit_funding_contract_integration.py`, `src/test_funding_contract_integration.py`. The local integration command and output contract are in `docs/research_checkpoints/2026-11-28_g0_03_funding_contract_integration_v1.md`.

**G0-03 remains PARTIALLY CLOSED / ACCEPTANCE OPEN** until the new harness is run against the user's local Termux CSVs and the resulting JSON is reconciled. The actual files are not in GitHub; synthetic CI does not replace that run. The current production loader uses the explicitly labelled `candle_close_proxy`; exact settlement mark-price fidelity remains a separate blocker. No strategy PnL or real-input trade simulation was performed.
