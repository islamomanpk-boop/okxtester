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

The agreed research order is numerical: Phase 1, Phase 2, Phase 3, Phase 4, Phase 5. The current user-directed priority is to finish the remaining Phase 3 execution/trading-system research before handing off to Phase 1. The current phase order and handoff must not be changed casually.

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

**Gate 0: CONDITIONAL HOLD — not passed.** Existing research and infrastructure were found, but critical readiness items remain. In particular: verify and freeze the exact source/event ledger provenance; prove causal signal availability; reconcile actual funding inputs and engine integration; verify mark-price, instrument, and fee assumptions; and ensure missing funding fails closed. No Phase 3 strategy PnL backtest until the required gates permit it.

The latest detailed blocker register and evidence in the controlling roadmap/audit supersede informal chat summaries. When new evidence closes an item, update the relevant source document with commit/run/artifact references and tests before changing its status.


## 4A. Repository reconciliation and research register

The evidence-backed repository and five-phase research index is `docs/PROJECT_RESEARCH_REGISTER_V1.md`. It records the canonical and supporting repository snapshots, Phase 3 workstream statuses, Gate 0–7 mapping, known unrelated legacy candidates, and the next reconciliation actions. It is an index, not a replacement for the underlying protocols, scripts, tests, reports, or source artifacts.

Cleanup rule: do not delete ambiguous or historical provenance material. Explicit EMA-pullback files are flagged as candidates only; no deletion is authorized until dependencies are checked and the user approves the exact path list.

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

## 9. Immediate next action

Do not start a new Phase 3 experiment yet. First complete a repository-wide reconciliation of the two known repositories and the Phase 3 archive against the eight-gate roadmap. Build an evidence-backed register of every existing study, script, test, report, workflow, artifact, status, limitations, and gate mapping. This will prevent duplicate work and replace informal progress estimates with a traceable project record.

**Project rule:** The assistant owns continuity, organization, and status tracking. The user should not have to remember filenames, completed studies, or governance rules.
