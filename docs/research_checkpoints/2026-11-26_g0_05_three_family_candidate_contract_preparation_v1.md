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
