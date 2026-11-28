# OKX Price Action V1 — Project Control Center

**Status:** Active project control document  
**Project:** OKX Multi-Regime Price Action V1  
**Canonical repository:** `islamomanpk-boop/okxtester`  
**Canonical working branch:** `price-action-v1`  
**Last control review:** 2026-11-28

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

Continue Gate 0 evidence reconciliation; do not implement a candidate generator yet. The causal-timing audit has identified an unresolved live-regime calibration decision, and the existing descriptive labels are not eligible as live signals.

1. **Reconcile existing 1M-to-15M/4H aggregation evidence before repeating work.** The checkpoints `docs/research_checkpoints/2026-11-22_1m_to_15m_4h_aggregation_audit.md` and `docs/research_checkpoints/2026-11-23_termux_15m_4h_ohlcv_aggregation_pass.md` already report exact OHLCV matches for five assets (37,941 15M bars and 2,370 4H bars per asset) using epoch-anchored, left-closed, left-labelled complete buckets. This establishes aggregation equivalence for the files compared in those audits; it does not establish the original acquisition lineage, that the compared local files are byte-identical to every current canonical snapshot, or VPS runtime equivalence. Verify the audit inputs/manifests and preserve those scope limits.
2. Resolve canonical 1M source acquisition provenance, original OKX instrument/volume semantics, and VPS downloader/runtime lineage. Do not infer provenance from matching asset names or matching OHLCV alone.
3. Specify and compare past-only regime-threshold calibration policies without optimizing strategy PnL. Record the calibration window, warm-up, update cadence, availability timestamp and leakage tests. Freeze no policy until its rationale and validation criteria are documented.
4. Resolve the remaining family-specific causal definitions and source-availability requirements for rejection, breakout continuation and failed-breakout reversal. Align immutable candidate IDs, regime versions, boundaries, confirmation/availability timestamps, first eligible 1M bars, expiry/invalidation and overlap/de-clustering.
5. Reconcile VPS market/funding inputs with canonical sources; verify runtime funding integration and exact settlement mark-price policy.
6. Verify fee schedules, instrument/contract specifications, lot/tick rounding and execution-engine real-input readiness.
7. Close each Gate 0 blocker with reproducible evidence, then issue an explicit Gate 0 decision. Only after Gate 0 is formally passed may Gate 2 execution-resolution research begin. Gates 3–7 remain sequentially closed; no strategy PnL backtest is authorized.

**Candidate-generation rule:** source/timing audits and protocol design may continue, but do not build or run the candidate generator until the past-only regime policy and three-family candidate contract are formally frozen and the Gate 0 governance permits implementation.

## Latest Gate 0 evidence update — 2026-11-25

The expanded read-only VPS inventory [45648774228](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45648774228) completed successfully after the audit was widened to generic source/config files and CSV headers and the event tokens were narrowed to avoid generic-word false positives. It found no candidate evidence in the six inspected categories and no static content keyword hits. This is scoped to the configured VPS/project/repository roots and scan rules; it is not proof of global absence. The earlier generic `reclaim` hit in an unrelated cleanup workflow was reviewed and rejected as a false positive. Full evidence and artifact digest are in research register Section 12.13.

G0-10 documentation correction: `docs/execution_data_audit_v1.md` now corrects the stale claim that current market data is local-only. The five canonical one-minute CSVs are tracked under `data/market_1m/`, and the exact byte sizes, Git blob IDs and SHA-256 values are recorded in that document and Module B run metadata. This closes the documentation contradiction only; VPS downloader lineage, runtime equivalence and refresh/retention controls remain unverified.

**Current gate decision remains unchanged:** Gate 0 CONDITIONAL HOLD; Gate 1 COMPLETE (descriptive lifecycle only); Gate 2 remains closed. No strategy PnL backtest is authorized.


### Candidate availability and causal-timing blocker — 2026-11-25

The read-only audit in `docs/research_checkpoints/2026-11-25_phase3_candidate_availability_audit_v1.md` is now recorded in research register Section 12.14. It confirms the rejection-family 15-minute candle-close availability convention, the completed 15-minute/4-hour breakout source chain and first eligible one-minute bar timing, and a critical causal limitation: historical STRICT_P25 / BROAD_P40 thresholds were calculated from the full feature sample. Those historical regime labels are descriptive only and must not be treated as live-knowable candidate signals.

G0-04/G0-05 remain OPEN / CRITICAL. Before any candidate generator is implemented, a past-only regime-threshold/calibration policy and a single causal candidate contract covering rejection, breakout continuation and failed-breakout reversal must be specified and frozen. The failed-breakout return-inside 15-minute close is only a proposed confirmation point, not an accepted rule. No candidate generation, Gate 2 execution comparison or strategy PnL backtest is authorized.

The next research step is to reconcile any available raw 15-minute source files against exact 15-minute aggregation from the five tracked canonical one-minute datasets, including hashes, bar counts, close-time labels and missing-bar handling. Do not claim source equivalence until those checks are reproducibly completed.


### VPS downloader SQL and export semantics — 2026-11-25

The static downloader review is now complete through the SQL/export layer. See `docs/research_checkpoints/2026-11-25_phase3_vps_downloader_sql_export_update_semantics_v1.md` and research register Section 12.19. The inspected source uses a SQLite upsert that **updates existing candle rows** on `(inst_id, ts)` conflicts; the operational DB is therefore mutable, not an immutable acquisition archive. The confirmed-only CSV export selects the timestamp, OHLC, all three volume fields and confirmation flag, filters `confirm=1` and `ts>=START_MS`, and sorts ascending. The timestamp remains an integer in the CSV; the source's one-minute gap check uses 60,000 timestamp units.

This closes source-code understanding of the conflict clause and export filter, but not runtime snapshot identity, byte identity with canonical Git data, immutable history, timestamp provenance, or volume-unit validation. Gate 0 remains CONDITIONAL HOLD. The workflow was static-only; no downloader, API request, SQLite operation, VPS service change or data cleanup was performed.


A follow-up safe-constant extraction also confirmed the VPS downloader's lower bound is 2025-10-20 00:00:00 UTC and its exact CSV headers are `ts, open, high, low, close, vol, volCcy, volCcyQuote, confirm`. This start date matches the separate funding manifest's first timestamp, but does not prove the market CSVs begin there or that VPS exports are byte-identical to canonical Git data. See research register Section 12.20 and the same downloader checkpoint.


### VPS market CSV snapshot reconciliation — 2026-11-25

A read-only manifest audit of the five actual VPS CSV exports and targeted SQLite checks is recorded in `docs/research_checkpoints/2026-11-25_phase3_vps_market_csv_snapshot_audit_v1.md` and research register Section 12.21. All five exports begin at 2025-10-20 00:00 UTC and their row counts match the SQLite `confirm=1` counts exactly. The CSVs have different final timestamps (BTC 09:41 through AVAX 11:40 UTC on 2026-11-25), so the VPS snapshot still needs explicit cross-asset alignment. One internal SOL CSV gap is explained by a historical SQLite row at 2026-08-28 08:30 UTC with `confirm=0`; it is present in the database but excluded by the confirmed-only export filter. Do not impute or change this row. First compare its current OKX history-candles confirmation flag, then complete five-asset timestamp alignment. Gate 0 remains CONDITIONAL HOLD; no strategy PnL backtest is authorized.


A targeted public OKX history-candles probe has now confirmed the old SOL 2026-08-28 08:30 UTC row itself is returned with `confirm=0`, and its OHLCV/volume fields match the VPS SQLite row exactly. The single internal gap in the confirmed-only SOL CSV is therefore consistent with the exchange response and the `confirm=1` export filter, not a demonstrated local missing-row or export mismatch. Do not relabel or fill it. See research register Section 12.22 and the VPS snapshot checkpoint. The reason for the exchange's historical `confirm=0` remains unknown; cross-asset alignment is still the next step.


The explicit VPS five-asset timestamp-set audit is complete: 578,021 common timestamps from 2025-10-20 00:00 UTC through 2026-11-25 09:41 UTC; union 578,141; 120 timestamps outside the intersection. Differences are explained by staggered per-asset end times and the single SOL 2026-08-28 08:30 UTC candle that OKX itself returns with `confirm=0`. The common timeline preserves that one-minute hole; do not impute it. See research register Section 12.23 and the VPS snapshot checkpoint. Next source task is OHLCV-level comparison of the separate VPS snapshot with canonical Git data, without overwriting either dataset.


### Canonical Git vs VPS OHLCV reconciliation — 2026-11-25

The five-asset overlap comparison is complete and saved in `docs/research_checkpoints/2026-11-25_phase3_vps_canonical_ohlcv_reconciliation_v1.md` and research register Section 12.24. Every matched timestamp has exact OHLC equality. Canonical Git `vol` equals VPS `volCcy` exactly on all matched timestamps for all five assets; OKX defines `volCcy` as base-currency volume for derivatives and VPS `vol` as contract quantity. The execution-data audit now records this mapping and requires explicit volume units. The only timestamp exception is the known SOL 2026-08-28 08:30 UTC row returned by OKX with `confirm=0`, present in SQLite and canonical Git but excluded from the confirmed-only VPS CSV. The VPS snapshot is a wider, later dataset; preserve both snapshots separately. Gate 0 remains CONDITIONAL HOLD.


### Full-window funding mark-price coverage — 2026-11-25

The full-window public mark-price audit is saved in `docs/research_checkpoints/2026-11-25_phase3_full_window_mark_price_coverage_audit_v1.md` and research register Section 12.25. All 5,940 audited funding timestamps matched exact 4H mark-candle opens; 2,375 candles per asset, all confirmed, no gaps. A 60-point 1M sample matched the 4H open exactly at every point. The 4H mark-open proxy is much closer to trade 1M open (pooled mean absolute 0.650 bps) than trade 1M close (7.514 bps). This is the best-supported public proxy candidate, not an exact settlement mark. No engine mode changed; G0-03/G0-09 remain OPEN and Gate 0 remains CONDITIONAL HOLD.


The full 5,940-row event-time 4H mark-price candidate snapshot is now versioned at `data/funding_mark_price_proxy_candidate_v1/` (CSV SHA-256 `22e2894a8c467777f9ee90d5824deaf243a8b3d6e44ebff7f7d33b3e88c4cc82`, commit `adaf25d7a27c1e01def1a14a011c99be99186c67`). Its manifest explicitly says exact settlement mark is unverified, proxy policy is not accepted, and engine mode is unchanged.


### G0-05 independent source verification — 2026-11-28

Phase 3 G0-05 Step 22 is complete. The independent source verifier passed in GitHub Actions run [46148537294](https://github.com/islamomanpk-boop/okxtester/actions/runs/46148537294), commit `8744a1981237f3aabfe73bacf3cc8bdfa5bb295f`, artifact `15264717673`. It independently reconciles 1,154 rejection physical identities, 2,861 raw breakout crossings and 932 linked failed-breakout identities; recomputes causal dispositions; rebuilds 1,037 breakout 12-hour overlap clusters; and checks the failed-breakout half-open 12-hour lifecycle, including one exact-endpoint exclusion. Full counts and limitations are in research register Section 12.27 and `docs/research_checkpoints/2026-11-28_g0_05_independent_source_verification_closeout_v1.md`.

This does **not** close G0-05 or Gate 0. The source-only disposition ledgers are not canonical candidate records. Real candidate IDs and linked failed-breakout source candidate IDs remain unmaterialized; the 60-field validator has synthetic-only record coverage. G0-05 remains OPEN / CRITICAL and Gate 0 remains CONDITIONAL HOLD. Other funding/settlement-mark, fee/instrument, sizing/rounding/gap-risk and execution-engine acceptance items remain open. No Gate 2+ work, Phase 3 strategy PnL backtest, or live-trading conclusion is authorized.

**Next safe task:** read-only pre-generation gate review, reconciling the older canonical field-mapping matrix with the later frozen field-value decisions and checking family-specific nullability and identity rules. Any real canonical candidate build requires a separate explicit authorization after that review.


### G0-05 pre-generation contract review — 2026-11-28

The pre-generation static review confirms the 60-field canonical serializer has exactly 60 required keys, all 60 are explicitly covered in the field-mapping matrix, and family-specific source reconciliation/cardinality semantics now fail closed. New synthetic checks passed: [workflow 46149074209](https://github.com/islamomanpk-boop/okxtester/actions/runs/46149074209), **193/193**. The validator now requires rejection physical-collapse semantics and BROAD_P40 membership, one raw crossing row for breakout, and exact one-source-breakout linkage for failed breakout.

This is a **pre-generation contract review PASS only**. It is not a G0-05 or Gate 0 pass. No real candidate IDs, canonical candidate rows, orders, fills, execution simulation or PnL were generated. G0-05 remains OPEN / CRITICAL; Gate 0 remains CONDITIONAL HOLD. The next real canonical candidate/disposition build requires separate explicit project-owner authorization, and even that would not authorize Gate 2+ execution comparison or strategy backtesting. See research register Section 12.28 and `docs/research_checkpoints/2026-11-28_g0_05_independent_source_verification_closeout_v1.md`.


### G0-05 real canonical candidate ledger — 2026-11-28

<badge color="success">Real build and validation passed</badge>

Owner-authorized workflow [46149804561](https://github.com/islamomanpk-boop/okxtester/actions/runs/46149804561) generated 4,947 canonical G0-05 records, exactly 60 required fields each. The full row and ledger validators passed; deterministic IDs and unique family/source identities passed; all 932 failed-breakout source-candidate links resolved. Counts: support rejection 558, resistance rejection 596, breakout continuation 2,861, failed-breakout reversal 932. Aggregate dispositions: 2,856 eligible, 1,884 rejected, 207 expired, 0 censored.

Evidence artifact ID `15265550848`, name `phase3-g0-05-canonical-candidate-ledger-46149804561`, ZIP SHA-256 `e66ea4b16811d158a9b86dfb90113be13cc5fccfc89f1c42b5330fba294456da`. Canonical JSONL SHA-256 `202c44f456af021b9ec8cc642e82c349f4858baadb04bcdb2342973cb752db14`; CSV SHA-256 `eca9f326bc44a74ba9631bc6b5d4a6c7b5691fea6b59c7031976f7fd7f5ff1a5`.

The initial real-data attempt stopped on the `NONE` historical-membership sentinel; the source mapper was corrected to emit an empty list for no historical memberships. The successful workflow then reran source audit, independent verification and canonical validation. Full checkpoint: `docs/research_checkpoints/2026-11-28_g0_05_canonical_candidate_ledger_build_v1.md`.

**Next:** read-only post-build evidence review before formally closing G0-05. Gate 0 remains CONDITIONAL HOLD with separate funding/settlement-mark, fee/instrument, sizing/rounding/gap-risk and execution-engine blockers. No orders, fills, execution simulation, PnL, strategy selection, Gate 2+ or live trading is authorized.


### Final G0-05 evidence status — 2026-11-28

<badge color="success">Canonical build and independent review passed</badge>

Authoritative workflow [46150045661](https://github.com/islamomanpk-boop/okxtester/actions/runs/46150045661) completed successfully. The real G0-05 canonical ledger contains 4,947 records with exactly 60 fields each. All deterministic candidate IDs, unique family/source identities, full contract/ledger validation, 932 failed-breakout links and the separate independent post-build review passed. The reviewer confirmed JSONL/CSV equivalence, output hashes, source-manifest identity and exact-once source reconciliation.

Artifact ID `15265023491`; artifact ZIP SHA-256 `0b9464cbeda0a513cea915aae78a1c43aab2b5563448a0e19b247c02b4081935`. Canonical JSONL SHA-256 `387d376bc269587de6fb48686641cd27e885a2d3bd6c6a8ae96a9a9dd61333d8`; CSV SHA-256 `325c714e5923612a711d18a855d1540e1f59b27d26d65636ebabd7578c81bb43`. Detailed evidence is in research register Section 12.30 and `docs/research_checkpoints/2026-11-28_g0_05_independent_source_verification_closeout_v1.md`.

**Current technical status:** G0-04 ACCEPTED. G0-05 implementation, real candidate generation, full validation and independent post-build review are complete and READY FOR FORMAL CLOSEOUT. Formal G0-05 gate acceptance has not yet been recorded. Gate 0 remains CONDITIONAL HOLD due to separate funding/settlement-mark, fee/instrument, standalone sizing, contract rounding, stop-gap risk and execution-engine blockers. No orders, fills, execution simulation, PnL, strategy comparison, Gate 2+ or live trading was performed or authorized.


### G0-05 formal technical disposition — 2026-11-28

<badge color="success">G0-05 ACCEPTED</badge>

G0-05 is **ACCEPTED — TECHNICAL CLOSEOUT COMPLETE** under `docs/research_checkpoints/2026-11-28_g0_05_acceptance_decision_v1.md`. The decision is an assistant technical acceptance based on the owner's explicit authorization to generate the real canonical ledger and the completed source, real-row and independent post-build evidence; it is not a human reviewer sign-off.

The accepted scope includes 4,947 real canonical records with exactly 60 fields each, deterministic candidate IDs, full row/ledger validation, exact source reconciliation, and 932/932 failed-breakout source links and inherited fields. Final evidence: workflow [46150045661](https://github.com/islamomanpk-boop/okxtester/actions/runs/46150045661), artifact ID `15265023491`.

**Gate 0 remains CONDITIONAL HOLD — not passed.** G0-03, G0-07, G0-08 and G0-09 remain separate blockers. Gate 2+, execution-resolution comparison, orders, fills, execution simulation, strategy PnL backtests and live trading remain unauthorized. Phase 3 remains active; continue through the remaining Gate 0 requirements before any Gate 2 work or phase handoff.


### G0-03 funding integration — 2026-11-28

Funding/execution CI [46150715018](https://github.com/islamomanpk-boop/okxtester/actions/runs/46150715018) passed **90/90 tests**, including new standalone/portfolio funding arithmetic parity tests and read-only real-input contract integration harness tests. The new harness exercises the production loader/validator against the actual five local funding CSVs, checking hashes, schedules, common timestamps and settlement boundary rules without simulating trades or calculating PnL.

**G0-03 remains PARTIALLY CLOSED / ACCEPTANCE OPEN** until the harness is run in the user's Termux environment against the local CSVs and its JSON report is reconciled. The local files are not committed. Run instructions: `docs/research_checkpoints/2026-11-28_g0_03_funding_contract_integration_v1.md`. Current funding loader mode remains explicitly `candle_close_proxy`; exact settlement mark-price fidelity and other Gate 0 blockers remain open.


### G0-07 sizing alignment update — 2026-11-28

The standalone engine's risk sizing was aligned with the portfolio allocator. Both now use the same per-unit planned stop-risk formula, including adverse entry/stop-exit slippage and taker fees on both legs. The shared helper is `calculate_cost_adjusted_risk_per_unit` in `src/execution_engine.py`; the portfolio calls it directly. New long/short tests and an end-to-end quantity-parity test passed in workflow [46154849952](https://github.com/islamomanpk-boop/okxtester/actions/runs/46154849952), commit `8bcc79ab32cb24b6647330baf429f97325768b1f`.

**G0-07 remains OPEN:** stop-gap loss quantification and verified exchange lot/tick/minimum-quantity rounding remain outstanding. G0-08 instrument metadata is a prerequisite for contract rounding. Gate 0 remains CONDITIONAL HOLD; no strategy PnL, execution simulation, orders, fills or live trading are authorized.

### G0-03 real Termux funding integration result — 2026-11-28

<badge color="success">Real-input contract integration passed</badge>

The user's local Termux run of `src/audit_funding_contract_integration.py` returned `REAL_FUNDING_INPUT_CONTRACT_INTEGRATION_PASS`: 5,940 real funding rows across BTC, ETH, SOL, DOGE and AVAX; 1,188 common timestamps identical across assets; entry-exclusive/exit-inclusive trade-window boundaries. The saved local JSON report SHA-256 is `557f59fd4c2aa1588ef0716aca4ed3411c6bc1f19b6702a93336a6ace2067e70`. The report and source CSVs remain on the user's device and were not uploaded. Evidence details: `docs/research_checkpoints/2026-11-28_g0_03_real_termux_funding_integration_reconciliation_v1.md`.

**Scope limit:** exact settlement mark price is still unverified (`candle_close_proxy`; `exact_settlement_mark_price_verified=false`). This passes the real-input integration subtask, not all of G0-03 or G0-09. Gate 0 remains CONDITIONAL HOLD; no strategy PnL, trade/execution simulation, orders, fills or live trading are authorized.
