# Phase 3 G0-05 Three-Family Causal Candidate Contract — Preparation V1

**Date:** 2026-11-26  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Sequence:** Gate 0, task G0-05 (after G0-04)  
**Status:** G0-04 ACCEPTED BY DELEGATED PROJECT-OWNER DISPOSITION; G0-05 CONTRACT FINALIZATION AUTHORIZED — CANDIDATE GENERATION NOT YET AUTHORIZED  
**Authority:** Controlling Phase 3 roadmap and the 2026-11-25 candidate-availability/source-timing audit  
**Execution status:** No candidate generator has been run or authorized by this document. No candidates, orders, fills, outcomes, PnL, or strategy results are produced.

## 1. Numbering and dependency control

This is **G0-05**, not a replacement for or parallel execution of G0-04. The ordered work sequence remains:

1. **G0-04 — causal breakout reconstruction and past-only threshold comparison.** Corrected canonical GitHub Actions execution passed on 2026-11-26 (run 45752717022, attempt 1; checked-out revision `8326c1edea66c11391ab614b9ce4afa9be5bc1fd`). The 20/20 historical baseline, 932 historical identity reconciliation, feature/context alignment, output hashes, and corrected classification-matrix uniqueness validation have been checked. The execution evidence is recorded in `2026-11-26_g0_04_implementation_checkpoint_v1.md`. The independent reviewer packet is `2026-11-26_g0_04_independent_review_packet_v1.md`; formal G0-04 acceptance was recorded by delegated project-owner disposition on 2026-11-26; see `2026-11-26_g0_04_acceptance_decision_v1.md`. G0-05 contract finalization is now authorized, but candidate generation remains blocked until the deferred policy and family-specific rules are explicitly frozen.
2. **G0-05 — freeze and implement the causal three-family candidate contract.** This document is preparation only. It does not pre-empt G0-04 results.
3. **Remaining Gate 0 blockers and formal Gate 0 decision.** G0-05 acceptance alone does not close Gate 0. Funding/mark-price and other source/engine blockers recorded in the controlling register remain subject to their own acceptance.
4. Only after a documented Gate 0 pass may the project proceed to Gate 2, then Gate 3, Gate 4, Gate 5, Gate 6, and Gate 7 in that order.

Do not skip, renumber, merge, or mark a task complete because its specification or code has merely been prepared. If G0-04 fails, is inconclusive, or has not been formally accepted, stop at G0-04. Diagnose and repair any defect, rerun if needed, and complete review before unlocking G0-05.

## 2. Purpose and scope

G0-05 must establish a reproducible, causally available candidate-event ledger for all Phase 3 families:

- **Support rejection:** a causally confirmed long-side rejection of the lower/support boundary.
- **Resistance rejection:** a causally confirmed short-side rejection of the upper/resistance boundary.
- **Breakout continuation:** a causally confirmed close beyond the active range boundary, in the breakout direction.
- **Failed-breakout reversal:** a causally confirmed completed 15-minute return inside the prior range after a valid breakout, in the opposite direction.

The four labels above are separate output families/subfamilies. Support and resistance rejection must remain separately reportable. Failed upside and failed downside breakouts must also remain separately reportable. Never pool away asset, direction, boundary side, or family differences.

This is an event/candidate-availability contract, not an execution simulator. A candidate is not an order, a fill, or a profitable trade.

## 3. Decisions deliberately deferred to G0-04

The implementation must not guess or hard-code any of the following before G0-04 is reviewed:

- selected past-only range-width threshold policy;
- selected weighting population (unique completed 4-hour feature rows or joined 15-minute rows);
- selected strict/broad causal threshold definitions and their version identifiers;
- exact eligible snapshot/context population and warm-up treatment;
- accepted cross-pipeline alignment tolerances and any documented exclusions;
- reconciled raw crossing population and final event identities/counts;
- whether any policy/population variant is rejected for instability, missingness, or failed reconciliation.

G0-04's output is not automatically accepted merely because the workflow is green. The reviewer must verify compilation, all synthetic tests, all 20 historical baseline counts, all 932 historical identities reconciled with no unexplained missing identities, context availability/alignment checks, and output manifests/hashes. Any failure or unresolved mismatch blocks G0-05 implementation.

Once G0-04 is accepted, record the chosen threshold policy, population, warm-up, snapshot refresh/validity, source hashes, and exact output artifact references in a dated G0-05 decision record. Preserve all unselected variants as sensitivity evidence; do not overwrite retrospective P25/P40 descriptive results.

## 4. Required input inventory and provenance

Before implementation, inventory and freeze exact paths, Git blob IDs, SHA-256 hashes, schemas, row counts, timestamp units, and source-version identifiers for:

### 4.1 Rejection family
- `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`
- `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv`
- `reports/sideways_detector_original_v1/{ASSET}_features_original_v1.csv`
- canonical `data/market_1m/{ASSET}_USDT_USDT_1m.csv` files.

The source join must preserve the accepted event identity, boundary side, snapshot index, snapshot availability and next-availability, test/segment identity, rejection candle identity, and event anatomy. Do not treat a retrospective cohort label as a live signal without applying the G0-04 accepted causal regime policy.

### 4.2 Breakout continuation family
- G0-04 accepted raw crossing ledger and its input/output manifests;
- canonical five-asset 1-minute data and the accepted complete 15-minute / 4-hour context reconstruction;
- accepted threshold-policy decision and snapshot provenance.

Do not start from the old 932-event selected-signal list. That list is a reconciliation reference only. The accepted G0-04 raw crossing ledger is the source population.

### 4.3 Failed-breakout reversal family
- accepted Module B descriptive lifecycle event/source identities;
- the corresponding source breakout identity and G0-04 causal breakout eligibility/provenance;
- canonical 1-minute and complete 15-minute bars needed to independently verify the return-inside confirmation.

The descriptive Module B archive is a source for event anatomy and reconciliation, not proof that its original full-sample regime labels are live-knowable.

### 4.4 Input integrity rules
- Fail closed on missing, duplicate, malformed, or hash-mismatched source inputs.
- Assert exact expected schemas and unique key constraints before joining.
- Assert monotonic timestamps, complete-bar rules, and explicit UTC millisecond timestamp semantics.
- Never silently inner-join away unmatched source events. Emit left/right reconciliation counts and row-level mismatch reasons.
- Preserve raw source rows and original identities; do not mutate accepted historical archives.

## 5. Canonical candidate record

Every emitted candidate must carry the following immutable or explicitly versioned fields. Use null only where a field is genuinely inapplicable, and document the reason.

### 5.1 Identity and classification
- `candidate_id`: deterministic, immutable identifier derived from the canonical source identity plus family/rule version; collision-checked.
- `source_event_id`: immutable source event identity.
- `family`: one of `SUPPORT_REJECTION`, `RESISTANCE_REJECTION`, `BREAKOUT_CONTINUATION`, `FAILED_BREAKOUT_REVERSAL`.
- `instrument_id`, `asset`, `side` (`LONG` / `SHORT`), `boundary_side` (`LOWER` / `UPPER`).
- `regime_definition_version`, `candidate_rule_version`, `source_pipeline_version`.
- `cohort_definition`, `strict_broad_label` (or explicit not-applicable), `overlap_cluster_id`.

### 5.2 Boundary and context provenance
- `snapshot_id`, `snapshot_available_at_ts_ms`, `snapshot_valid_from_ts_ms`, `snapshot_valid_until_ts_ms`.
- `frozen_upper_boundary`, `frozen_lower_boundary`.
- `threshold_policy_id`, `threshold_population_id`, `threshold_value`, `threshold_calibration_start_ts_ms`, `threshold_calibration_end_ts_ms`, `threshold_prior_observation_count`.
- `source_file_paths`, `source_git_blob_ids`, `source_sha256_manifest_id`.

Threshold fields must reference the accepted G0-04 decision exactly. Do not recompute or silently substitute a threshold in the candidate generator.

### 5.3 Signal and availability timestamps
- `signal_candle_open_ts_ms`, `signal_candle_close_ts_ms`, `signal_available_at_ts_ms`.
- `confirmation_rule_id`, `confirmation_bar_interval_ms`, `confirmation_status`.
- `first_eligible_execution_bar_open_ts_ms`.
- `source_breakout_candidate_id` for failed-breakout reversal, otherwise null.
- `event_observed_at_ts_ms` where distinct from confirmation/availability.

All timestamps must be UTC epoch milliseconds. Signal candle open, close, availability, and first eligible execution-bar open must remain distinct fields; never overload one timestamp to mean another.

### 5.4 Event lifecycle and censoring
- `decluster_policy_id`, `repeated_signal_group_id`, `overlap_cluster_id`.
- `invalidation_reference_type`, `invalidation_reference_value`, `invalidation_reference_ts_ms`.
- `expiry_rule_id`, `expiry_ts_ms`.
- `censoring_reason`, `exclusion_reason`, `ambiguity_flags`.
- `candidate_status` (for example eligible, rejected, expired, censored); allowed values must be frozen in the implementation contract.

No candidate may disappear without a recorded disposition. A source event may produce zero or more candidate records only where the frozen rule explicitly permits it; every one-to-one/one-to-many mapping must be documented and reconciled.

## 6. Family-specific timing and eligibility contracts

### 6.1 Support/resistance rejection

- Preserve the exact source rejection candle and its original open timestamp.
- The accepted source convention records `first_strong_rejection_ts_ms` as the 15-minute candle **open**. It is not available at that open.
- Set `rejection_confirmed_at_ts_ms = first_strong_rejection_ts_ms + 900000`, subject to verifying the complete 15-minute candle and source mapping.
- Set the first eligible 1-minute execution bar open to the confirmation timestamp, never to a minute inside the rejection candle.
- Support rejection maps to LONG; resistance rejection maps to SHORT, unless a separately approved rule explicitly rejects that mapping.
- Verify that the exact frozen boundary snapshot was available no later than signal availability and remains valid through confirmation. Snapshot validity is the half-open interval `[snapshot_available_at_ts_ms, snapshot_next_available_at_ts_ms)`. Require `rejection_confirmed_at_ts_ms < snapshot_next_available_at_ts_ms`; equality is expired, not inclusive. The source audit found 40 broad and 29 nested strict rejection events whose 15-minute confirmation equals the next snapshot availability; preserve their source rows but disposition them as `SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION`, not candidates. See `2026-11-26_g0_05_rejection_snapshot_validity_audit_v1.md`.
- Freeze the repeated-test/de-clustering rule, minimum separation, invalidation reference, and expiry before producing candidate rows. Do not infer these from future outcomes.
- Keep support and resistance results separate.

### 6.2 Breakout continuation

- Use only the G0-04 accepted raw crossing population and selected past-only threshold policy.
- Require complete 15-minute signal bars and the accepted completed 4-hour context.
- A crossing is valid only under the accepted same-context crossing rule and while that frozen snapshot is active.
- The 15-minute signal timestamp is its close label. Availability is at that completed close; the first eligible 1-minute bar opens at that timestamp.
- Long follows an upper/resistance break; short follows a lower/support break.
- Do not merge continuation entry with a retest-entry hypothesis. Retest execution belongs to later Gate 2/Gate 3 research.
- Freeze repeated-cross/de-clustering, invalidation, expiry, and whether a same-context second crossing is a new event or part of an existing episode.

### 6.3 Failed-breakout reversal

- Require a valid, causally eligible source breakout candidate; retrospective Module B labels alone are insufficient.
- Earliest proposed confirmation is a **completed 15-minute close back inside** the frozen prior range. This is a proposal to be accepted or rejected explicitly before implementation.
- Failed upside break maps to SHORT; failed downside break maps to LONG.
- The first eligible 1-minute execution bar opens at or after the completed return-inside close availability timestamp.
- Preserve same-bar ambiguity, reclaim ambiguity, gaps, missing bars, and incomplete 15-minute bars as explicit flags or censoring reasons. Do not infer intrabar ordering from OHLC.
- Link every reversal candidate to its source breakout candidate and preserve the full event chain.
- If the project rejects completed 15-minute return-inside as the confirmation rule, document a separately justified replacement and test it before candidate generation.

## 7. Universal fail-closed validation rules

Reject or quarantine the affected event with a machine-readable reason if any of the following occurs:

1. A required source file, row, column, source identity, hash, or snapshot is missing.
2. A source identity or candidate identity is duplicated unexpectedly.
3. Input bars are non-monotonic, duplicated, malformed, or incomplete under the frozen bar-completeness rule.
4. A context snapshot was not available at or before signal availability, or its half-open validity interval ended at or before confirmation.
5. The event lies outside the snapshot's declared validity interval.
6. The signal availability timestamp precedes the confirmation timestamp.
7. The first eligible execution bar opens before signal availability.
8. A rejection candidate uses any part of its rejection candle as post-confirmation data.
9. A breakout candidate cannot be reproduced from the accepted raw crossing ledger and threshold version.
10. A failed-breakout reversal lacks a valid linked source breakout or completed return-inside confirmation.
11. A many-to-many join, ambiguous identity, or unresolved source mismatch occurs.
12. An OHLC touch is treated as a guaranteed order fill, or a synthetic fill/price is created.

Validation must report rejected/quarantined counts and reasons by asset, family, side, and source version. Do not silently drop failures.

## 8. Required reconciliation and reporting

At minimum, produce:

- frozen input manifest with Git blob IDs and SHA-256 hashes;
- source schema and row-count audit;
- source-to-candidate identity reconciliation for each family;
- candidate ledger with the complete canonical schema;
- family/asset/side/boundary/threshold-policy count summaries;
- strict/broad nesting and overlap/de-clustering audit;
- timestamp/availability audit, including first eligible execution bar;
- snapshot availability/validity audit;
- missing, duplicate, rejected, censored, and ambiguous event ledger;
- deterministic run metadata, code revision, environment versions, output hashes;
- synthetic test report and reproducibility instructions.

Reconciliation tables must show input events, eligible events, emitted candidates, rejected/quarantined events, and unexplained unmatched events. Unexplained unmatched events must be zero for acceptance; any intentional exclusion requires a named, predeclared reason.

## 9. Minimum synthetic test matrix

Before canonical data execution, write deterministic synthetic tests for:

1. Rejection candle open is not treated as confirmation; confirmation is at completed 15-minute close.
2. No 1-minute execution bar inside the rejection candle is eligible.
3. First eligible 1-minute bar equals or follows signal availability.
4. Snapshot available exactly at signal close is accepted only if it is also within the declared validity interval.
5. Snapshot available one millisecond after signal close is rejected.
6. Confirmation exactly at `snapshot_next_available_at_ts_ms` is rejected as expired; confirmation one millisecond before the endpoint is eligible if all other rules pass.
7. Partial 15-minute and 4-hour bars are excluded.
8. Missing source rows and hash mismatches fail closed.
9. Duplicate source and candidate identities are detected.
10. Out-of-order and duplicate timestamps fail closed.
11. Support rejection maps to long and resistance rejection maps to short.
12. Upper breakout maps to long and lower breakout maps to short.
13. Failed upside maps to short and failed downside maps to long.
14. Failed-breakout candidate without a valid source breakout is rejected.
15. Return-inside confirmation cannot be taken from an incomplete 15-minute candle.
16. Same-bar ambiguity is preserved and never resolved by assumed OHLC path.
17. Strict cohort is nested within broad cohort where the accepted threshold policy defines nested cohorts.
18. Repeated crossings follow the frozen de-clustering policy deterministically.
19. Every input event has an explicit emitted/rejected/censored disposition.
20. Repeated runs on identical inputs produce identical IDs, rows, and output hashes (excluding explicitly volatile run metadata).

Add tests for every additional edge case discovered in G0-04 review. Do not reduce the matrix to a small happy-path test.

## 10. Execution boundary and prohibited work

G0-05 may build and validate a descriptive causal candidate-availability ledger only after its dependencies and decisions are accepted.

It must not:
- create orders, fills, or synthetic execution prices;
- assume OHLC touches fill resting orders;
- calculate trade PnL, expectancy, win rate, drawdown, or profitability;
- select stops, targets, entry methods, or position sizing;
- run Gate 2 execution-resolution comparisons;
- run Gate 3 entry-method comparisons;
- run Gate 4 stop/target optimization;
- run strategy backtests or OOS validation;
- change or delete accepted historical evidence, source market data, or prior research outputs.

G0-05 acceptance does not by itself pass Gate 0. Funding/settlement/mark-price, fees/slippage, source provenance, and execution-engine readiness blockers remain governed by their existing numbered work items and the controlling register. Gate 2 onward remain blocked until formal Gate 0 acceptance and subsequent gates pass in order.

## 11. G0-05 acceptance checklist

G0-05 can be proposed for acceptance only when all applicable items are evidenced:

- [ ] G0-04 independently reviewed and formally accepted; all prerequisite outputs and hashes frozen.
- [ ] Past-only threshold policy and population selected from G0-04 evidence with documented rationale; retrospective full-sample P25/P40 kept separate.
- [ ] Snapshot availability and validity semantics frozen.
- [ ] Rejection confirmation, de-clustering, invalidation, and expiry rules frozen.
- [ ] Breakout continuation availability and raw source reconciliation frozen.
- [ ] Failed-breakout confirmation and source-breakout linkage frozen.
- [ ] Canonical candidate schema implemented without missing required provenance.
- [ ] All synthetic tests pass, including G0-04-derived edge cases.
- [ ] All canonical inputs pass hashes, schema, completeness, and timestamp checks.
- [ ] Every source event has a reconciled disposition; no unexplained missing identities.
- [ ] Candidate counts reconcile by asset, family, side, boundary, and policy.
- [ ] Independent review confirms no look-ahead, no premature availability, and no execution/PnL leakage.
- [ ] Deterministic rerun reproduces candidate identities and substantive outputs.
- [ ] A dated closeout records ACCEPTED / REJECTED / CONDITIONAL HOLD with evidence links and limitations.

If any critical item fails, status remains OPEN / BLOCKED or CONDITIONAL HOLD. Do not lower the acceptance standard to obtain a pass.

## 12. Immediate next action

**Do not run G0-05 while G0-04 is running.** Continue preparation only. When G0-04 completes:

1. Inspect the exact workflow run, every job step, logs, and uploaded artifact.
2. Verify compile and synthetic tests before reading canonical outputs.
3. Verify the 20/20 historical baseline counts, 932/932 identity reconciliation, cross-pipeline alignment, complete-context coverage, threshold-policy tables, and output hashes.
4. Record G0-04 acceptance or failure with exact evidence.
5. Only after acceptance, finalize the deferred G0-05 decisions and implement the generator/tests/workflow as the next numbered task.

**Current disposition:** G0-04 is accepted by delegated project-owner disposition with review limitations preserved. G0-05 contract finalization and synthetic-test design are authorized. Canonical candidate generation remains blocked until the selected threshold policy/population, snapshot semantics, rejection/de-clustering/invalidation/expiry rules, and all family-specific confirmation rules are frozen in a dated decision record. Gate 0 remains CONDITIONAL HOLD. No execution simulation, strategy backtest, or PnL work is authorized.


## G0-04 execution status update — 2026-11-26

G0-04 canonical execution has completed successfully and its artifact has been inspected. The implementation checkpoint records the run ID, checked-out revision, 20/20 historical baseline reproduction, 932-identity reconciliation, cross-pipeline checks, partial-tail coverage exception, and independently verified output hashes.

**This is not formal G0-04 acceptance.** G0-05 remains preparation-only and blocked until the independent review and dated G0-04 closeout are completed. No candidate generator, candidate ledger, order/fill simulation, PnL, or strategy backtest is authorized by this update.


## G0-04 latest evidence update — 2026-11-26

The null/invalid historical zone-level validator repair is complete. Corrected source revision `86b49598d676b6ab00649bf31d4490ffbb1e608f` passed workflow run [45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179), job `139694830125`, and produced artifact `15087542445` with ZIP SHA-256 `ef6204b546b49880675514ff76b4f6cb86e2821ba2b0d1d5412549927388f0a1`.

The implementation checkpoint now records additional direct checks against the five raw 1-minute files: all five SHA-256 values independently match metadata; 569,125 common timestamps are identical across assets; source cadence/OHLCV checks show no defects; a separate raw-data recomputation reproduces all 20 historical counts and all 10 quantiles; and all five detector ledgers match 2,358 rebuilt contexts each within (10^{-9}). The actual historical classification ledger has 4,776 rows and 932 distinct identities, with no null zones or duplicate full-grain classifications.

These checks materially close the evidence gaps raised in the preliminary Kimi review, but they are documented as a separate assistant-side audit and do not change Kimi's own INCONCLUSIVE report. Formal G0-04 acceptance still requires an explicit project-owner disposition under the review standard. Therefore this G0-05 document remains PREPARATION ONLY: implementation and candidate generation are blocked; Gate 0 remains CONDITIONAL HOLD; no execution simulation, backtesting or PnL is authorized.


## 13. Authoritative G0-04/G0-05 status and superseding decisions — 2026-11-26

This section supersedes any earlier sentence in this preparation document that says G0-04 acceptance is pending, that G0-05 remains blocked pending G0-04, or that the threshold/family timing decisions remain deferred. Earlier status paragraphs are retained as historical chronology, not current instructions.

### 13.1 G0-04 disposition

G0-04 was accepted by delegated project-owner technical disposition on 2026-11-26. The decision and limitations are recorded in `2026-11-26_g0_04_acceptance_decision_v1.md`. Kimi's original AI-review verdict remains INCONCLUSIVE; no human review is claimed. The acceptance is based on the combined reproducibility and raw-source audit recorded in the implementation checkpoint and acceptance decision.

For clarity, run 45752717022 (checked-out revision `8326c1e...`) and run 45756061179 (validator correction at `86b4959...`) are separate G0-04 executions. The latter's job/artifact and digest are pinned in the acceptance decision. Do not conflate their source revisions or artifacts.

### 13.2 Decisions now frozen for G0-05 contract work

The controlling decisions are:
- `2026-11-26_g0_05_threshold_policy_population_decision_v1.md`: primary `EXPANDING_PRIOR + UNIQUE_4H_FEATURE_ROWS`, 180 prior completed contexts for warm-up, with FIXED_180, ROLLING_180 and JOINED_15M_ROWS retained as sensitivity variants.
- `2026-11-26_g0_05_rejection_snapshot_validity_audit_v1.md`: snapshot validity is half-open; rejection confirmation must be strictly before the next snapshot availability. Preserve 40 broad / 29 nested strict expired-at-confirmation source classifications with explicit exclusion dispositions.
- `2026-11-26_g0_05_family_timing_contract_decisions_v1.md`: frozen family direction mappings and confirmation timing, including completed-15-minute failed-breakout return-inside confirmation linked to a valid causal source breakout.

### 13.3 Candidate event lifecycle semantics

G0-05 creates a point-in-time candidate-availability/disposition ledger, not a persistent order or position simulator. Therefore:
- Support/resistance rejection and breakout continuation are point events. They do not remain active as executable orders; order expiry/invalidation is NOT APPLICABLE at this gate. Preserve source test-rank/repeated-cross identity and overlap-cluster metadata. Do not drop overlapping source events or invent a de-clustering rule that removes observations.
- Rejection repeated tests remain distinct according to the accepted source identity (asset, definition, direction, snapshot index, segment ID, test rank, test-start timestamp). Existing source protocol separation and test-rank fields are retained; G0-05 adds no second independent rejection episode detector.
- Breakout continuation uses each unique raw G0-04 crossing identity. A subsequent distinct raw crossing remains a distinct source event; preserve overlap-cluster metadata and do not collapse it into one candidate.
- Failed-breakout reversal is a child event linked to a valid causal breakout candidate. It can confirm only on a completed 15-minute close back inside the original frozen boundary, no later than 12 hours after source breakout signal availability. If no confirmation occurs by the horizon, disposition `EXPIRED_NO_RETURN_INSIDE_WITHIN_12H`; if a data gap/incomplete bar prevents resolution, use an explicit censored disposition. The source breakout boundary is immutable through the failure lifecycle.
- The candidate first-eligible-minute field is an availability timestamp, not an order instruction or fill.

### 13.4 Contract implementation and test workflow

The pure, data-independent contract primitives are implemented in `research/phase3_g0_05_candidate_contract_v1.py`, with synthetic tests in `tests/test_phase3_g0_05_candidate_contract_v1.py`. Workflow `phase3-g0-05-candidate-contract-tests.yml` compiles and runs those tests only. This workflow does not read canonical market data and does not generate candidate records.

The initial test suite covers snapshot endpoint validity, rejection close timing, exact first eligible minute, minute-gap rejection, direction mappings, complete 15-minute confirmation, failed-breakout source linkage, inside-close confirmation, 12-hour expiry, deterministic candidate IDs, explicit dispositions, and deterministic serialization.

### 13.5 Current authorization boundary

**Authorized now:** contract/test refinement, source inventory, source-key/schema/hash validation design, and synthetic CI tests.

**Not yet authorized:** canonical source joins that emit candidate records, candidate counts as research findings, orders, fills, execution simulation, PnL, strategy backtesting, or any Gate 2+ work.

Canonical candidate generation remains blocked until:
1. Exact canonical G0-04 artifact contents are available and independently inspected for the raw crossing ledger and threshold table.
2. All rejection, detector-feature, market-data and Module B source blob IDs/schemas/row counts are frozen and their required joins are proven one-to-one or explicitly one-to-many.
3. The candidate output schema and all event disposition values are finalized.
4. The complete synthetic edge-case matrix passes in CI.
5. A source-only dry-run proves every input row receives a deterministic disposition without writing candidate outputs.
6. Reproducibility and row-level reconciliation checks are specified and reviewed.

**Current status:** G0-04 ACCEPTED. G0-05 CONTRACT IMPLEMENTATION / SOURCE INVENTORY IN PROGRESS. CANONICAL CANDIDATE GENERATION NOT AUTHORIZED. Gate 0 remains CONDITIONAL HOLD. No execution simulation, strategy backtest, or PnL work is authorized.


## 14. G0-05 implementation progress — 2026-11-26

### 14.1 Contract primitives and synthetic CI

- Pure contract primitives: `research/phase3_g0_05_candidate_contract_v1.py`.
- Synthetic suite: `tests/test_phase3_g0_05_candidate_contract_v1.py`.
- Workflow: `.github/workflows/phase3-g0-05-candidate-contract-tests.yml`.
- Latest verified run: [45781945291](https://github.com/islamomanpk-boop/okxtester/actions/runs/45781945291), checked-out revision `eeb6cdb0dbb3eda2cc7c03a5e11e9c56a60c3fb6`, job `139779287523`.
- Python compile: PASS.
- Synthetic tests: **31/31 PASS**.

The suite covers half-open snapshot validity, rejection close confirmation, exact first eligible minute, minute gaps, family direction mapping, complete 15-minute component bars, linked failed-breakout reversal, completed-close return-inside, 12-hour expiry, deterministic IDs/serialization, causal width/efficiency/overlap thresholds, and strict-within-broad validation.

Two intermediate CI failures were traced to an escaped newline in the test import statement; the corrected test file was committed and the final 31-test run passed. These failures were test-source syntax defects, not failures in the market data or G0-04 evidence.

### 14.2 G0-04 artifact independently rechecked

The G0-04 artifact was downloaded again and its ZIP SHA-256 independently matched the recorded digest. All seven member-file hashes match `run_metadata.json`. The direct checks found:
- 2,861 raw crossing rows, all unique at (asset, direction, signal_time_ms, context_snapshot_ms);
- 932 historical selected identities present;
- 20/20 historical baseline rows passed;
- 120 historical reconciliation rows and zero raw-source mismatches;
- 65,310 threshold rows, 21,770 per policy, P25 <= P40 throughout and at least 180 prior contexts;
- all six policy/population event totals reproduce the threshold decision record.

The detailed ZIP and member hashes are recorded in `2026-11-26_g0_05_canonical_source_manifest_v1.md`.

### 14.3 Remaining G0-05 work

The following remain before canonical candidate generation:
1. Independently compute SHA-256 for the rejection boundary ledger, event-anatomy ledger, five detector feature ledgers, and Module B event/horizon ledgers.
2. Freeze and test exact source join keys, cardinality expectations and all unmatched-row disposition rules.
3. Implement a read-only source reconciliation/dry-run that produces disposition coverage only and emits no candidate ledger.
4. Expand synthetic tests for source joins, duplicate keys, causal threshold lookup at exact snapshot availability, invalid feature values, missing source rows, and failed-breakout lifecycle censoring.
5. Only after these pass, request/record authorization to run the canonical candidate generator.

**Current status:** G0-04 ACCEPTED; G0-05 contract primitives and 31 synthetic tests pass. G0-05 source manifest is partially verified; source reconciliation dry-run remains pending. Candidate generation, execution simulation, strategy backtesting and PnL remain prohibited.


## 15. Source-only causal disposition and schema freeze — 2026-11-26

The G0-05 candidate/disposition schema is now recorded in `2026-11-26_g0_05_candidate_disposition_schema_v1.md`. It freezes the status/reason enums, physical source identity, cohort membership handling, provenance fields, timestamp fields, and the rule that point-event rejection/continuation records have no active-order expiry at this gate.

Latest source-only audit:
- Workflow [45782827341](https://github.com/islamomanpk-boop/okxtester/actions/runs/45782827341) passed.
- Artifact [15098494434](https://github.com/islamomanpk-boop/okxtester/actions/runs/45782827341/artifacts/15098494434), ZIP SHA-256 `3dad432c4a9c8a81364b93b0a2e0cbd66c70e54716fc2e704536094c2a8f84ea`.
- All 7 rejection-family source blob pins and SHA-256 values passed.
- All Module B event/horizon SHA-256 values matched frozen metadata.
- G0-04 threshold flags were independently recomputed across 15,594 event/variant joins; all matched.
- The 262 raw G0-04 warm-up events were explicitly accounted for by asset.
- Rejection source rows collapsed to 1,154 unique physical test identities while preserving all 1,992 strict/broad source-row IDs and memberships. The strict physical cohort is nested within broad.
- Source-only causal rejection disposition: 942 strict eligible, 141 broad-only eligible, 2 not regime-eligible, 29 warm-up, 40 snapshot-expired. These are not candidate output rows.
- Module B's 1,592 definition rows map to 932 unique source identities; all 932 match the G0-04 raw crossing ledger.

**Current status:** G0-04 ACCEPTED. G0-05 schema, 31 synthetic tests, and read-only source provenance/identity/causal-threshold audit are passing. Next task is to extend synthetic tests around the source-to-physical-event collapse and family-specific disposition accounting, then implement a deterministic source-only disposition dry-run. Canonical candidate generation remains blocked pending that dry-run and its review. No orders, fills, execution simulation, PnL, strategy backtests or Gate 2+ work are authorized.


## 16. Expanded G0-05 synthetic suite — 2026-11-26

The contract implementation now includes:
- underlying physical rejection identity independent of historical strict/broad cohort labels;
- lossless collapse of strict/broad source rows while preserving both original source row IDs;
- fail-closed validation that strict historical membership is nested within broad;
- source-only causal rejection disposition using the exact snapshot validity interval, completed 15-minute confirmation, expanding-prior P25/P40 thresholds, efficiency <= 0.30 and overlap >= 0.70.

Latest synthetic CI run: [45783013949](https://github.com/islamomanpk-boop/okxtester/actions/runs/45783013949), job `139782802699` — SUCCESS. Python compilation passed and **43/43 tests passed**.

The added tests cover physical identity collapse, preservation of both cohort source-row IDs, broad-only events, strict-without-broad rejection, duplicate membership rejection, strict/broad causal outcomes, threshold warm-up, snapshot endpoint expiry, exact completed-15-minute timing and snapshot availability at the rejection bar open.

**Current status:** G0-04 ACCEPTED. G0-05 source provenance, raw identity reconciliation, causal threshold re-computation, candidate/disposition schema and 43 synthetic tests pass. The next controlled task is a deterministic row-level source-disposition dry-run with exact first-eligible-minute checks. It must remain a source disposition audit, not a candidate generator. Canonical candidate generation remains blocked until that dry-run reconciles every source row and its output is reviewed.

## 17. Row-level G0-05 source-disposition dry-run — 2026-11-26

The exact first-eligible-minute source-only dry-run is now implemented in `research/phase3_g0_05_source_manifest_audit_v1.py`. It runs only after the pinned source audit and G0-04 artifact checks. It verifies all five market 1-minute SHA-256 values and row counts before timestamp membership checks, then writes three row-level disposition CSVs.

Latest workflow [45784746198](https://github.com/islamomanpk-boop/okxtester/actions/runs/45784746198), job `139788574173`, commit `5aeafd08f063cb4c515fa2b4c000fa526fb95a38` — SUCCESS. Artifact [15100091580](https://github.com/islamomanpk-boop/okxtester/actions/runs/45784746198/artifacts/15100091580), ZIP SHA-256 `8616483b6932bdd0e9976ba31e150b2d93882455365e51cad180a1d94e23eda9`, independently verified.

| Population | Source rows | Eligible | Rejected | Expired | Censored |
|---|---:|---:|---:|---:|---:|
| Unique physical rejections | 1,154 | 1,083 | 31 | 40 | 0 |
| Raw breakout crossings | 2,861 | 1,038 | 1,823 | 0 | 0 |
| Unique failed-breakout events | 932 | 736 | 30 | 166 | 0 |

All 2,857 rows marked eligible passed exact first-minute timestamp membership. There were zero missing/gapped first eligible minutes. No timestamp was shifted to a nearby bar. Failed-breakout expiry requires a complete 12-hour horizon; incomplete horizons remain censored by rule. The output ledgers preserve physical event identities, original cohort row IDs/memberships, family labels, and family direction mapping.

The contract synthetic CI now reports **49/49 tests passing** in [run 45783985772](https://github.com/islamomanpk-boop/okxtester/actions/runs/45783985772), including exact-minute and 12-hour boundary cases.

**Current status:** G0-04 ACCEPTED. G0-05 contract and 49 synthetic tests pass; source provenance, threshold recomputation, row-level source dispositions and exact first-minute checks pass. Next is independent row-level reconciliation/review of the three disposition CSVs and mapping semantics. Canonical candidate generation remains blocked until that review is complete. No orders, fills, execution simulation, PnL or strategy backtesting are authorized.


## 18. Independent raw 1-minute membership verification — 2026-11-26

The previously recorded independent-review limitation concerning separate re-hashing of the five raw 1-minute datasets has now been resolved by a separate verifier and workflow. Full evidence is recorded in `2026-11-26_g0_05_independent_exact_minute_verification_v1.md`.

- Corrected source audit: [45800976161](https://github.com/islamomanpk-boop/okxtester/actions/runs/45800976161) — SUCCESS; checked-out commit `7406bd52d93d10128bc8ea18416366917223b5dc`; artifact ID `15106648767`; ZIP SHA-256 `f8e7f802606ac4b6a977f79e3103b21fa44733cedae833d724a3c6260c2ea517`.
- Independent verifier: [45801631819](https://github.com/islamomanpk-boop/okxtester/actions/runs/45801631819) — SUCCESS; job `139846060250`; artifact ID `15107586311`; ZIP SHA-256 `d40b1a565e47d65222836a20c625765b75d47108cb5b33c82c3b115c9b5f22fe`.
- Five raw 1-minute inputs: all five SHA-256 values and expected row counts independently matched; all timestamp grids were strictly increasing, duplicate-free, minute-aligned and continuous.
- All 2,857 eligible timestamps were independently found in the relevant raw asset timestamp index. All 2,090 non-eligible rows had blank first-eligible timestamp fields.
- Family dispositions remained rejection 1,083/31/40/0; breakout continuation 1,038/1,823/0/0; failed-breakout reversal 736/30/166/0 (eligible/rejected/expired/censored).

The first independent run [45801067586](https://github.com/islamomanpk-boop/okxtester/actions/runs/45801067586) intentionally failed closed because it consumed a stale artifact predating the eligible-only timestamp correction. The workflow was amended to select the successful source-audit artifact at the exact correction commit; the subsequent independent run passed. Both runs and the correction are retained in the evidence record.

**Updated status:** The raw 1-minute hash/grid/membership limitation is closed. This does not close all G0-05 acceptance criteria. Complete contract review, remaining source/schema/reporting requirements, deterministic candidate-ledger implementation and its review remain open. Canonical candidate generation remains unauthorized; no execution simulation, strategy backtest, PnL or phase transition is authorized.


## 19. Frozen disposition reason-code enforcement — 2026-11-26

A further contract review found that the source-only ledger's reason labels were not fully aligned with the frozen status/reason enum. Eligible broad-only rows had been using `CAUSAL_BROAD_ONLY` as a reason, and failed-breakout source-ineligible rows used an unapproved reason string. The source audit also did not apply the shared reason validator to every row.

The issue is corrected in source-audit commit `253f187b0da75f76c585fed6f4ec416cd28c5ddc`. Every row is now validated against the frozen status/reason/censoring contract. Cohort labels remain in separate fields; eligible rows use `reason_code=NONE`; source-ineligible failed-breakout rows use `NO_VALID_SOURCE_BREAKOUT`.

Evidence:
- Source audit [45802145534](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802145534) — SUCCESS; artifact ID `15106714247`; ZIP SHA-256 `ef08831a8ad5bbb6326d4847b842b2e229cee4cdd174e4292cddbc45c96aa5bb`.
- Synthetic tests [45802241180](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802241180) — SUCCESS; **80/80 tests passed**.
- Independent minute verifier [45802348522](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802348522) — SUCCESS; artifact ID `15107686762`; ZIP SHA-256 `cf5d687ec36d0a6d906cb81f26becbca01e68553297ff422ab59ca69f9004c62`. It reran all five raw source hash/grid checks and all 2,857 exact eligible-minute memberships against the reason-validated source-audit artifact.

The earlier failed synthetic run [45802163583](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802163583) exposed one stale test fixture without reason fields; the fixture was corrected and the succeeding 80-test run is the controlling test evidence.

**Updated status:** G0-05 source identity, causal-threshold, horizon, row-level disposition, exact-minute, and reason-code audits have passed their recorded checks. The canonical candidate schema/output, complete family/asset/side/overlap reporting, full independent review, deterministic candidate-output rerun, and formal G0-05 closeout remain open. No canonical candidates or trading tests have been authorized.


## 20. Structured disposition summaries and latest independent minute verification — 2026-11-26

The source-only audit now emits deterministic grouped summaries by asset/disposition, family/LONG-SHORT/disposition/reason, source direction/disposition, causal cohort/disposition and reason code. Source-audit run [45802587303](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802587303) passed at commit `a1ef8721f3f770fb46079c09ea039da75a7e920e`; artifact ID `15108166636`; ZIP SHA-256 `456c683375d20ebef8a852421d235e745d2c79f62be29d2eea18045d59b455cc`. The new deterministic grouping test passed in the **81/81** synthetic suite [45802605906](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802605906).

The independent exact-minute verifier was rerun against this grouped-summary artifact:
- Workflow [45802702444](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802702444) — SUCCESS.
- Artifact ID `15107996832`.
- ZIP SHA-256 `e05759ff6fa9b73178de85a21f62f014e66c3dbbe3718ff675c21b3ebd7ff317`, independently recomputed after download.
- Report status `INDEPENDENT_EXACT_MINUTE_MEMBERSHIP_PASS`; all five raw inputs re-hashed and checked; all 2,857/2,857 eligible timestamps present; all 2,090 non-eligible first-minute fields blank.

**Current status:** Source-only provenance, identity, Module B horizon, exact-minute, disposition-reason and grouped-count checks pass. Remaining G0-05 work is the canonical output field mapping and implementation, historical cohort preservation for breakout, overlap/repeated-signal metadata convention, complete source-to-candidate schema validation, full independent review and deterministic candidate-output reproducibility. Canonical candidate generation remains unauthorized; no execution simulation, strategy backtest, PnL or phase transition is authorized.


## 21. Raw breakout historical cohort membership — 2026-11-26

The G0-04 raw crossing ledger's `was_historical_selected` flag is now reconciled by exact source identity to Module B's event rows. The breakout source-disposition ledger preserves historical `BROAD_P40` and `STRICT_P25` membership separately from the causal cohort.

- Source audit [45802913642](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802913642) — SUCCESS; artifact ID `15108411917`; ZIP SHA-256 `181b395393c9f7d012c282b64d862f10f83639f974543acf3b139a20e7d7f6e5`.
- Synthetic suite [45802929770](https://github.com/islamomanpk-boop/okxtester/actions/runs/45802929770) — SUCCESS; **86/86 tests passed**.
- Raw crossings: 1,929 with no historical selected membership, 272 BROAD_P40-only, and 660 with both BROAD_P40 and STRICT_P25. No strict-only event is permitted.
- The selected flag must agree with exact-key Module B membership; mismatches, unknown cohort labels and strict-without-broad fail closed.

This preserves the important distinction between retrospective historical cohorts and G0-04 causal expanding-prior eligibility. The historical 932 are not treated as the only causal eligible source population.

The independent minute workflow is being advanced to this latest source-audit artifact before its next run. Overlap-cluster/repeated-signal metadata and the complete canonical candidate field mapping remain open. Candidate generation and trading tests remain unauthorized.


## 22. Latest independent verification after breakout cohort reconciliation — 2026-11-26

The independent minute verifier was rerun against the source-audit artifact containing the breakout historical-membership join:
- Workflow [45803028375](https://github.com/islamomanpk-boop/okxtester/actions/runs/45803028375) — SUCCESS; job `139850895093`.
- Artifact ID `15107712661`; ZIP SHA-256 `f4be33a3abc238c2d972e89f8ba0a8a9eca846b3036b531e4d66898f0fbdb9ab`, independently recomputed after download.
- Report `INDEPENDENT_EXACT_MINUTE_MEMBERSHIP_PASS`; 2,857/2,857 eligible timestamps present; five raw market files independently re-hashed and their timestamp grids checked.

The current source-only checks therefore pass for identity, historical/causal cohort separation, disposition reason codes, grouped counts and exact first-minute membership. The canonical candidate output field mapping and overlap/repeated-signal metadata convention remain unresolved. G0-05 remains open and candidate generation remains unauthorized.
