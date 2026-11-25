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

The controlling user-directed sequence is numerical: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5, with the current explicit instruction to finish Phase 3 execution/trading-system research before handing off to Phase 1. The Phase 3 handoff pause is therefore still in force. Do not use older handoff wording in historical closeout documents to override the current control center.

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
| P3-13 | Comprehensive rejection lifecycle (continuation/pullback, signal-level retests, depth, hold/failure, repeated crosses, candle anatomy) | Partial / open | Existing rejection anatomy and early-path studies plus `docs/research_checkpoints/2026-11-22_post_signal_retest_execution_research_roadmap.md` and related addenda | G1; complete the explicitly missing lifecycle items only after protocol and source ledger are reconciled. |
| P3-14 | Comprehensive failed-breakout / reversal lifecycle | Open | Breakout prior-test and forward-outcome studies exist; no complete accepted lifecycle archive demonstrated | G1; define return-inside, reclaim, reversal, retest, hold/failure, timing, de-clustering, and post-retest continuation with causal timestamps. |
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
| G1 | Complete descriptive lifecycle for rejection, breakout continuation, and failed-breakout reversal | Partial; P3-13/P3-14 remain |
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

The canonical recursive Git tree was inspected at `42ab2ed...`; GitHub reported **1,325 tracked blobs and tree not truncated**.

Top-level tracked inventory:

| Area | Tracked files | Classification |
|---|---:|---|
| `.github/workflows/` | 31 | Price Action research, funding tests, Phase 1 preflight, archive checks, and VPS monitoring; retain pending workflow-by-workflow review. |
| `data/market_1m/` | 5 | Five core asset source datasets; retain. |
| `docs/` | 157 | Governance, specifications, research, provenance, and checkpoints. Includes some legacy-project provenance investigations; do not bulk-delete. |
| `reports/` | 981 | Research evidence and archives. Includes some clearly named EMA-pullback outputs and large generic exit-experiment archives requiring provenance review before cleanup. |
| `research/` | 45 | Phase 3 studies, breakout studies, matched-control audits, Phase 1 source preflight, and historical provenance scripts. |
| `src/` | 68 | Shared Price Action structure, signal, funding, execution, portfolio and audit components, plus separately named EMA-pullback code. |
| `tests/` | 35 | Tests for the above study and shared components. |
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
