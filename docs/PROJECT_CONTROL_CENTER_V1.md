# OKX Price Action V1 — Project Control Center

**Status:** Active project control document  
**Project:** OKX Multi-Regime Price Action V1  
**Canonical repository:** `islamomanpk-boop/okxtester`  
**Canonical working branch:** `price-action-v1`  
**Last control review:** 2026-11-25

This document is the project-level navigation and control record. It does not replace detailed research protocols, phase roadmaps, source data, reports, or engineering specifications. Those remain in their specialist locations and must be linked here when discovered or created.

## 1. Project identity and boundaries

The project is **Price Action V1**, a five-phase market-regime research programme for OKX swap market data. The five phases are:

1. **Phase 1 — Uptrend / Bullish**
2. **Phase 2 — Downtrend / Bearish**
3. **Phase 3 — Sideways / Range**
4. **Phase 4 — Choppy / High Volatility**
5. **Phase 5 — Transition / Expansion**

The agreed execution sequence is: complete the currently active Phase 3 fully first; then proceed Phase 1 → Phase 2 → Phase 4 → Phase 5. Phase 1 remains paused until Phase 3 is formally completed or explicitly rejected. After that handoff, continue the remaining numbered phases in order without skipping. Do not change this user-agreed sequence casually.

Keep this project separate from older adaptive-bot, EMA-pullback, and unrelated trading projects.

## 2. Repository and branch authority

### Canonical research home

- Repository: `islamomanpk-boop/okxtester`
- Working branch: `price-action-v1`
- This branch is the primary home for Price Action research code, protocols, tests, reports, decisions, and durable project documentation.

### Supporting/operational repository

- Repository: `islamomanpk-boop/okxtester_private`
- Branch currently used for newer VPS/GitHub Actions work: `main`
- Treat this as supporting operational infrastructure and a source of work that must be reconciled into the canonical research record.
- Do not silently split project truth across repositories. When a result or useful implementation exists here, record its exact path, commit, workflow run, and artifact in the canonical project documentation. Do not blindly copy or merge files; inspect history, dependencies, and provenance first.

### Local and remote data safeguards

- Preserve raw market data and historical research outputs.
- Do not delete, reset, overwrite, force-push, or move valuable project data as routine cleanup.
- Local funding CSVs and other private/local source files must not be committed or uploaded unless explicitly authorized.
- GitHub is the durable versioned research record; local working copies must be reconciled carefully before pull/push operations.
- Do not assume a workflow success means a research gate passed.

## 3. Current project status

### Current active phase: Phase 3 — Sideways / Range

**Core descriptive research:** substantially complete and archived.

**Execution and trading-system research:** still active and incomplete.

The completed descriptive archive includes:
- Historical sideways detector and regime snapshots.
- Boundary reconstruction and boundary-interaction/penetration taxonomy.
- Rejection episode/retest anatomy for the archived selected cohort.
- Early-path sequence and follow-through study.
- Calendar moving-block bootstrap contrasts.
- Per-asset and leave-one-asset-out robustness work.
- Breakout prior-test classification.
- Breakout forward-path outcomes.
- Five-asset source-quality and timestamp-alignment preflight.
- V6 matched-control investigation and its formal rejection because balance and joint common support were inadequate. Preserve this negative result; do not reopen the rejected cohort to force an outcome comparison.

The descriptive studies are observational research. They do not prove causality, executable fills, profitability, or live readiness.

### Phase 3 trade families

All three families are in scope and must be researched separately before any combined portfolio:
1. **Support/resistance rejection:** long from confirmed support rejection; short from confirmed resistance rejection.
2. **Breakout continuation:** long after confirmed resistance break; short after confirmed support break, including separate continuation and retest hypotheses.
3. **Failed-breakout reversal:** short after failed upside break; long after failed downside break, with causal re-entry/reclaim confirmation.

Do not turn descriptive event labels directly into orders without a separate causal signal-availability and execution specification.

## 4. Phase 3 controlling documents

These documents govern current Phase 3 work. Read them before starting or changing a Phase 3 study.

1. Project-wide research rules: `docs/RESEARCH_GOVERNANCE_RULES_V1.md`
2. Phase 3 scope reconciliation: `reports/sideways_phase3_research_archive_v1/PHASE3_SCOPE_COMPLETENESS_AUDIT_V1.md`
3. Phase 3 completion/scope decision: `reports/sideways_phase3_research_archive_v1/PHASE3_COMPLETION_DECISION_V1.md`
4. Phase 3 execution/backtest roadmap: `docs/research_checkpoints/2026-11-25_phase3_execution_and_backtest_roadmap_v1.md`
5. Phase 3 knowledge synthesis: `reports/sideways_phase3_research_archive_v1/PHASE3_KNOWLEDGE_SYNTHESIS_V1.md`
6. Phase 3 boundary lifecycle closure protocol: `docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md`
7. Rejection lifecycle V1.1 overlap-cluster amendment: `docs/research_checkpoints/2026-11-25_phase3_rejection_lifecycle_v1_1_overlap_cluster_amendment.md`
8. Rejection lifecycle Module A closeout: `reports/phase3_rejection_lifecycle_v1_1/PHASE3_REJECTION_LIFECYCLE_CLOSEOUT_V1_1.md`
9. Evidence-backed repository research register: `docs/PROJECT_RESEARCH_REGISTER_V1.md`

The Phase 3 execution roadmap has the single ordered gate sequence:

- **Gate 0:** Archive and source readiness audit.
- **Gate 1:** Complete descriptive lifecycle work.
- **Gate 2:** Compare 1M, 3M, 5M, and 15M execution using the same completed 15M signal cohort.
- **Gate 3:** Compare predeclared candidate entry definitions.
- **Gate 4:** Research stops, targets, and trade management.
- **Gate 5:** Accept the execution engine and its inputs.
- **Gate 6:** Backtest each Phase 3 trade family separately.
- **Gate 7:** Chronological validation with untouched out-of-sample data.

Do not renumber, skip, or silently redefine these gates. The earlier five-gate checklist is a condensed view; the eight-gate roadmap above is the controlling execution/backtest sequence. Preserve both documents and reconcile their item-level mapping rather than maintaining competing gate systems.

### Current gate decision

**Gate 0: CONDITIONAL HOLD — not passed.** Funding source coverage/hash items G0-01/G0-02 passed for the five actual local files audited in Termux. The explicit fail-closed funding contracts are now integrated in both engines and the focused GitHub workflow passed; real-input integration and exact settlement-mark acceptance remain open. Critical G0-04/G0-05 work remains: freeze Phase 3 event provenance/availability and build the separate three-family range candidate generator. Fee/instrument assumptions, mark-price fidelity, contract rounding, and remaining execution realism are also open. No Phase 3 strategy PnL backtest until all required gates permit it.

The latest detailed blocker register and evidence in the controlling roadmap/audit supersede informal chat summaries. When new evidence closes an item, update the relevant source document with commit/run/artifact references and tests before changing its status.


## 4A. Repository reconciliation and research register

The evidence-backed repository and five-phase research index is `docs/PROJECT_RESEARCH_REGISTER_V1.md`. It records the canonical and supporting repository snapshots, Phase 3 workstream statuses, Gate 0–7 mapping, known unrelated legacy candidates, and the next reconciliation actions. It is an index, not a replacement for the underlying protocols, scripts, tests, reports, or source artifacts.

Cleanup rule: do not delete ambiguous or historical provenance material. Explicit EMA-pullback files are flagged as candidates only; no deletion is authorized until dependencies are checked and the user approves the exact path list.


### Newly frozen Gate 1 protocol

`docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md` defines the two descriptive lifecycle modules: rejection retest/cross lifecycle and breakout return-inside/reclaim/reversal lifecycle. It was frozen before implementation. Rejection Module A and breakout Module B are now both formally accepted as descriptive lifecycle studies. Module B closeout: `reports/phase3_breakout_lifecycle_v1_1/PHASE3_BREAKOUT_LIFECYCLE_CLOSEOUT_V1_1.md`. The five outside-retest fields absent from the frozen forward archive are accepted only as descriptive measurements, not independently cross-validated.


### Gate 1 progress

Rejection lifecycle Module A is accepted as a descriptive study: 1,992 events, 3,028 retest episodes, 7,968 horizon rows, and 380 overlap clusters; 12 synthetic tests passed. See `reports/phase3_rejection_lifecycle_v1_1/PHASE3_REJECTION_LIFECYCLE_CLOSEOUT_V1_1.md`. Breakout lifecycle Module B is now formally ACCEPTED as descriptive evidence. Its 1,592 events, 6,368 horizon rows, 244 group summaries, 23 synthetic tests and same-revision deterministic rerun are recorded in the formal closeout report. The five retest fields absent from the frozen benchmark remain descriptive-only limitations. With Module A also accepted, Gate 1 is COMPLETE. Gate 0 remains CONDITIONAL HOLD, so Gate 2 remains closed.

## 5. Mandatory research governance

The full standard is `docs/RESEARCH_GOVERNANCE_RULES_V1.md`. Its rules are mandatory for every phase and study.

### Before any study

Create or update a version-controlled protocol that records:
1. Research question and why it matters.
2. Hypothesis and competing explanations (or exploratory label).
3. Data, population, dates, assets, source files, inclusion/exclusion rules.
4. Method and unit of analysis.
5. Causal timestamp/no-look-ahead, gap, and complete-bar safeguards.
6. Decision criteria.
7. Stopping rule.
8. Practical decision that the result could change.

Freeze thresholds and parameters before examining outcomes that they could influence.

### After any study

Archive:
1. What was tested.
2. Evidence, sample sizes, coverage, uncertainty, robustness, and negative findings.
3. Plain-language lesson.
4. Decision: accept, reject, defer, or investigate.
5. Practical implication.
6. Limitations and unknowns.
7. Code/version, source hashes, tests, workflow run, and archive paths.
8. One next question or a justified stop.

A successful script, test, workflow, or artifact upload alone does not complete a study or gate.

### Interpretation safeguards

- Separate descriptive association, prediction, causality, and executable trading performance.
- Never claim profitability from MFE/MAE, forward returns, or target-touch rates alone.
- Preserve null, adverse, failed, rejected, and superseded work.
- Account for overlapping events and serial dependence.
- Do not tune thresholds or matching rules to force favourable sample sizes/results.
- No broad parameter sweeps or final-test peeking.
- Missing funding must never be silently treated as zero.
- Do not infer intrabar ordering from OHLC when it is ambiguous; use conservative rules or label ambiguity.

## 6. Shared evidence and infrastructure rules

Evidence that applies across phases must be stored once in a shared, discoverable location and referenced by later phases, rather than re-created independently.

Examples include:
- Five-asset market-data quality and timestamp alignment.
- Funding coverage, settlement timestamps, hashes, and provenance.
- Fee, spread, slippage, mark-price, and instrument specifications.
- Reusable execution-engine safeguards and tests.
- Portfolio risk, sizing, and accounting conventions.

A completed data audit does not prove an execution engine correctly consumes the data. A tested reusable component does not prove every caller is integrated. Track these separately.

Current shared market universe in the existing research: BTC, ETH, SOL, DOGE, and AVAX OKX swaps. Any change in assets, instrument identity, or time coverage must be explicit and documented.

## 7. File and evidence management standard

Use this layout as the project-wide organizing convention; preserve established specialist folders and do not move existing archives merely to make the tree look uniform.

- `docs/` — governance, architecture, specifications, roadmaps, protocols, decision records.
- `src/` — reusable production/research code and tests.
- `research/` — study-specific scripts and reproducible research implementations.
- `reports/` — immutable or versioned outputs, summaries, manifests, and evidence archives.
- `.github/workflows/` — reproducible automation.
- `data/` or local data locations — source/derived data, with privacy and size safeguards; never casually commit raw/private files.

For each study, keep its protocol, code, tests, output, summary/decision, and workflow provenance linked. Use versioned names (V1, V2, etc.) for materially different methods; do not silently overwrite an earlier result. Keep a study register and phase register updated whenever meaningful work is completed.

## 8. Operating procedure for the assistant

I am responsible for maintaining project continuity and should not make the user act as the project's memory or file manager.

Before starting work:
1. Read this control center and the applicable phase roadmap/governance.
2. Inspect the canonical repository and current branch history, including prior research and artifacts where accessible.
3. Search both canonical and supporting repositories for existing work before proposing a new study.
4. Check whether the question was already answered, partially answered, or rejected.
5. Identify the exact next unfinished numbered item and its dependencies.
6. State the research question/protocol before implementation when required.

While working:
- Prefer read-only inspection first.
- Use the existing canonical branch and established folders.
- Preserve existing files and outputs; no destructive cleanup.
- Use automation only when reproducible and appropriate; report exactly what ran.
- Do not ask the user to repeat information already in project records.
- Ask only for genuinely missing decisions or high-risk/destructive actions.
- Never claim direct VPS access; distinguish GitHub workflow execution from independent shell access.

After working:
- Update the source-of-truth document(s), study/phase register, and this control center when status materially changes.
- Record commit SHA, workflow run URL, artifact path, data hashes, and test results as applicable.
- Reconcile supporting-repository work into the canonical record without blindly copying.
- Give the user a concise plain-language report: what changed, evidence, decision, limitations, and next step.

## 9. Repository reconciliation status — 2026-11-25

The first cross-repository inventory and Gate 1 lifecycle reconciliation are recorded in `docs/research_checkpoints/2026-11-25_repository_reconciliation_checkpoint_02.md` and `docs/research_checkpoints/2026-11-25_phase3_moduleB_independent_review_timing_finding.md`.

- Canonical `okxtester@price-action-v1`: recursive tree inspected at commit `e025e1188c266b2c678b47de7953a65aa0a4ee30`; 1,360 tracked blobs (1,421 tree entries including 61 directories). Counts: 34 workflows, 48 research Python files, 38 test Python files, 1,001 report files, 163 docs, 68 shared source files, five tracked 1M market datasets, and one helper script.
- Supporting `okxtester_private@main`: recursive tree inspected at `ad5aac7294f0650e800ad834a1642f335915a649`; 12 tracked blobs (three research scripts and nine workflows). It remains supporting VPS/data infrastructure, not a replacement for the canonical research archive.
- Supporting Phase 3 range-measurement and Gate 0 inventory workflow results are linked in the register. Their successful execution is not a Gate 0 pass. The VPS inventory did not find event/signal timestamps, funding history, fee history or an execution engine in its inspected roots; the separate canonical Termux funding-file audit does not prove those inputs are installed or consumed by the VPS runtime.
- Module B formal closeout is complete; its five unbenchmarked lifecycle fields are explicitly restricted to descriptive-only use. Gate 1 is COMPLETE, while Gate 0 remains CONDITIONAL HOLD.
- The older master checklist and five-gate supporting checklist remain historical aids; the eight-gate roadmap is controlling.

## 10. Immediate next action

Continue content-level reconciliation of the Phase 3 archive and Gate 0 dependencies. In order:
1. Resolve VPS source/event availability and provenance, and build/test the separate three-family Phase 3 range candidate generator.
2. Reconcile VPS market/funding inputs with canonical sources; verify runtime funding integration and exact settlement mark-price policy.
3. Verify fee schedules, instrument/contract specifications, lot/tick rounding and execution-engine real-input readiness.
4. Close each Gate 0 blocker with reproducible evidence, then issue an explicit Gate 0 decision.
5. Only after Gate 0 is formally passed may Gate 2 execution-resolution research begin. Gates 3–7 remain sequentially closed; no strategy PnL backtest is authorized.

**Project rule:** The assistant owns continuity, organization, and status tracking. The user should not have to remember filenames, completed studies, or governance rules.


- Module B same-revision reproducibility is now confirmed: [workflow 45645349572](https://github.com/islamomanpk-boop/okxtester/actions/runs/45645349572) repeated the 23-test suite and frozen historical generation with analysis code, tests, inputs and schema unchanged; the output-commit step found no report changes. The formal closeout is now complete; the five unbenchmarked fields are explicitly descriptive-only. See register Section 12.12 and the closeout report.
- The first enhanced Gate 0 scan was found to contain self-match/cross-category false positives and was explicitly invalidated in register Section 12.9. The corrected read-only audit [45647247070](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45647247070) passed all steps on `okxtester_private@main` `87e80fbb71d2ffae0d7498bf17384807aec7b356`. It found no candidate event data, signal timestamps, funding history, fees, provenance records or execution engine in the inspected VPS roots; SQLite integrity is OK with 2,890,411 candle rows. This is scoped inventory evidence only, not proof of global absence or Gate 0 acceptance. Gate 0 remains CONDITIONAL HOLD. Details: register Section 12.11.


## Latest Gate 0 evidence update — 2026-11-25

The expanded read-only VPS inventory [45648774228](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45648774228) completed successfully after the audit was widened to generic source/config files and CSV headers and the event tokens were narrowed to avoid generic-word false positives. It found no candidate evidence in the six inspected categories and no static content keyword hits. This is scoped to the configured VPS/project/repository roots and scan rules; it is not proof of global absence. The earlier generic `reclaim` hit in an unrelated cleanup workflow was reviewed and rejected as a false positive. Full evidence and artifact digest are in research register Section 12.13.

G0-10 documentation correction: `docs/execution_data_audit_v1.md` now corrects the stale claim that current market data is local-only. The five canonical one-minute CSVs are tracked under `data/market_1m/`, and the exact byte sizes, Git blob IDs and SHA-256 values are recorded in that document and Module B run metadata. This closes the documentation contradiction only; VPS downloader lineage, runtime equivalence and refresh/retention controls remain unverified.

**Current gate decision remains unchanged:** Gate 0 CONDITIONAL HOLD; Gate 1 COMPLETE (descriptive lifecycle only); Gate 2 remains closed. No strategy PnL backtest is authorized.


### Candidate availability and causal-timing blocker — 2026-11-25

The read-only audit in `docs/research_checkpoints/2026-11-25_phase3_candidate_availability_audit_v1.md` is now recorded in research register Section 12.14. It confirms the rejection-family 15-minute candle-close availability convention, the completed 15-minute/4-hour breakout source chain and first eligible one-minute bar timing, and a critical causal limitation: historical STRICT_P25 / BROAD_P40 thresholds were calculated from the full feature sample. Those historical regime labels are descriptive only and must not be treated as live-knowable candidate signals.

G0-04/G0-05 remain OPEN / CRITICAL. Before any candidate generator is implemented, a past-only regime-threshold/calibration policy and a single causal candidate contract covering rejection, breakout continuation and failed-breakout reversal must be specified and frozen. The failed-breakout return-inside 15-minute close is only a proposed confirmation point, not an accepted rule. No candidate generation, Gate 2 execution comparison or strategy PnL backtest is authorized.

The next research step is to reconcile any available raw 15-minute source files against exact 15-minute aggregation from the five tracked canonical one-minute datasets, including hashes, bar counts, close-time labels and missing-bar handling. Do not claim source equivalence until those checks are reproducibly completed.
