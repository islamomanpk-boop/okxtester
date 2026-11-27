# Synthetic backend proof-of-capability plan

## 1. Purpose and status

This plan defines how a future backend candidate could be evaluated against the trusted registry contract using synthetic records only. It is intentionally vendor-neutral. It does not select a backend, create an account/resource, provision credentials, execute tests, authorize implementation, or permit research-data access.

The plan is subordinate to:
- `IMPLEMENTATION_READINESS_AND_EXIT_CRITERIA.md`
- `TRUSTED_BACKEND_SELECTION_FRAMEWORK.md`
- `TRUSTED_REGISTRY_BACKEND_INTERFACE_SPEC.md`
- `UNIFIED_TRUSTED_LIFECYCLE_TRANSACTION_SPEC.md`

**Current status: DESIGN ONLY / NOT RUN.** No backend candidate has been selected. No proof-of-capability test has been executed. The active Phase 3 G0-05 handoff remains authoritative and prohibits relevant scripts, tests, and workflows. This plan does not create an exception.

## 2. Entry conditions

Do not begin a proof-of-capability exercise until every entry condition is evidenced:

- [ ] The project owner has selected a candidate architecture class for evaluation, without treating evaluation as procurement or production selection.
- [ ] The approved test environment is isolated from the research repository's protected branches, market data, VPS, production identities, and existing research workflows.
- [ ] The environment uses synthetic task IDs, synthetic assignments, synthetic approvals, synthetic worker identities, and fabricated evidence bytes.
- [ ] Test credentials are newly provisioned, least-privilege, time-bounded, and contain no production or research access.
- [ ] The backend's transaction, uniqueness, consistency, isolation, backup, restore, and audit guarantees are documented by authoritative technical sources.
- [ ] An independent reviewer approves the test design, expected outcomes, data lifecycle, and cleanup plan.
- [ ] The current research handoff and project owner explicitly authorize the exact test environment and operations.
- [ ] Cost, request-rate, storage, retention, and automatic-shutdown limits are configured and independently checked.

If any entry condition is UNKNOWN, FAIL, or BLOCKED, do not run the exercise.

## 3. Synthetic fixture model

Use a closed fixture namespace that cannot be confused with real research records. Example values below are illustrative only.

| Object | Synthetic fixture |
|---|---|
| Registry | `poc-registry-001` |
| Task | `poc-task-phase3-001` |
| Assignment | `poc-assignment-001` |
| Assignment revision | `1` |
| Package digest | SHA-256 of canonical synthetic package bytes |
| Approval | `poc-approval-001` |
| Dispatch attempt | `poc-dispatch-001` |
| Provider delivery | `poc-provider-delivery-001` |
| Worker return | `poc-return-001` |
| Review | `poc-review-001` |
| Event sequence | Test-local monotonic integer |
| Checkpoint | Test-local registry version plus independent witness value |

Fixture requirements:

- No real symbols, timestamps, prices, market-data paths, research candidate IDs, credentials, or personal data.
- Every object has a fixed schema version and deterministic fixture generator version.
- Every expected digest is independently calculated by the test harness and retained outside the backend under test.
- Every test starts from a known isolated state and records the exact backend configuration and test run identity.
- Reset/cleanup is explicit, verified, and cannot touch any non-test environment.

## 4. Required test families

### POC-1 — atomic multi-record commit

**Setup:** Prepare a synthetic transition that must update assignment state, append one event, insert an idempotency record, and advance the protected checkpoint.

**Exercise:** Commit once, then inject a failure at each persistence boundary in a disposable test environment.

**Pass:** The observable state is either entirely before the transaction or entirely after it. No partial combination is visible. A successful receipt is returned only after the complete commit is durable.

**Fail:** Assignment state advances without event/checkpoint, event appears without idempotency index, checkpoint advances without state, or success is returned for an uncommitted transaction.

**Evidence:** Before/after snapshots, transaction outcome, durable read-after-write result, fault-injection trace, and reviewer reproduction.

### POC-2 — global and per-assignment concurrency

**Setup:** Two independent clients read the same global checkpoint and the same assignment state version.

**Exercise:** Race two conflicting transitions for the same assignment; then race transitions for different assignments against one global checkpoint.

**Pass:** At most one conflicting stale transition commits. Global sequence/checkpoint remains monotonic and gap semantics are documented. Every accepted transition is serializable or has an explicitly proven equivalent ordering. No lost update occurs.

**Fail:** Both conflicting updates commit, an event is lost, a sequence is duplicated, or assignment state and global checkpoint disagree.

**Evidence:** Client traces, committed event order, state versions, transaction conflict results, and independent consistency check.

### POC-3 — exact replay and conflicting replay

**Setup:** Submit a valid event with a stable source namespace, delivery ID, event role, and normalized facts.

**Exercise:** Repeat the exact request after the registry checkpoint has advanced. Then reuse the same idempotency identity with one changed fact.

**Pass:** Exact replay returns the original logical receipt without a second state transition, even with a stale caller checkpoint. Changed facts under the same identity are rejected and do not mutate state.

**Fail:** Exact replay duplicates effects, stale-checkpoint handling rejects a legitimate replay before checking idempotency, or changed facts are accepted.

**Evidence:** Idempotency index, original/replay receipts, event count, state version, and conflicting-request denial.

### POC-4 — uniqueness and identity levels

**Setup:** Generate provider-delivery identity `(source_namespace, delivery_id)` and event identity `(source_namespace, delivery_id, event_role)`.

**Exercise:** Attempt duplicate provider delivery, multiple legitimate roles for one delivery, duplicate event role, and same delivery ID under a different authenticated source namespace.

**Pass:** Provider delivery is unique at its declared level; each allowed event role is unique at event level; roles are schema-closed; source namespace cannot be spoofed by caller input.

**Fail:** Duplicate delivery is silently accepted, unrelated sources collide, or arbitrary event roles bypass schema validation.

**Evidence:** Constraints, accepted/rejected records, authenticated source context, and exact identity derivation.

### POC-5 — approval scope, expiry, and revocation

**Setup:** Create synthetic approvals bound to one operation, task digest, assignment revision, workflow identity, branch, handoff revision, and input commit.

**Exercise:** Attempt operation with wrong operation, changed task digest, changed workflow SHA, expired approval, revoked approval, wrong branch, and stale handoff revision. Race revocation against the protected operation.

**Pass:** Every mismatch is denied at the operation boundary. Revocation and operation have a deterministic atomic ordering; no operation begins on an approval that has already been revoked in the authoritative order.

**Fail:** A queue flag, workflow input, worker claim, or task allowlist hash can substitute for approval; stale or revoked approval proceeds.

**Evidence:** Approval record, authenticated caller context, denial reasons, transaction order, and audit event.

### POC-6 — package digest custody and tamper detection

**Setup:** Prepare a canonical synthetic assignment package and independently compute its digest.

**Exercise:** Store it, retrieve it, then alter one field, reorder semantically significant list content, alter schema version, replace package bytes, or submit a worker-returned digest instead of the registry value.

**Pass:** The exact retained package bytes/digest are recoverable; every mutation is detected; review loads expected bytes/digest from the trusted registry, not from the return payload.

**Fail:** Worker can redefine the expected digest, a package can be silently replaced, or serialization ambiguity yields different packages with an accepted digest.

**Evidence:** Canonical package bytes, digest receipts, tamper attempts, and independent recomputation.

### POC-7 — delivery uncertainty and no unsafe retry

**Setup:** Use a provider simulator or non-production provider with controllable response loss.

**Exercise:** Simulate request accepted but response lost; provider timeout before acceptance; duplicate request; and provider status unavailable.

**Pass:** Registry records pending/uncertain delivery; recovery queries the same provider identity or requires human reconciliation. No new dispatch attempt is automatically created while outcome is uncertain.

**Fail:** Timeout or missing response is interpreted as proof of non-delivery and causes automatic resend.

**Evidence:** Provider request/receipt log, registry state, recovery decision, and proof no second attempt was issued.

### POC-8 — authenticated delivery and return binding

**Setup:** Deliver one synthetic package to a worker simulator and create a signed/authenticated delivery receipt and return.

**Exercise:** Try a forged receipt, wrong worker, wrong assignment revision, wrong package digest, replayed return, and valid return with tampered evidence bytes.

**Pass:** Only authenticated provider context and a return bound to the exact retained assignment are accepted for review. Evidence hash mismatch downgrades or rejects review.

**Fail:** Worker-supplied metadata authenticates itself, or a return for another assignment is accepted.

**Evidence:** Identity claims, provider receipt validation, package lookup, return binding, and evidence verification result.

### POC-9 — workflow and checkout provenance

**Setup:** Use a disposable test workflow/repository with synthetic content.

**Exercise:** Supply wrong repository, branch, workflow path, workflow revision, run attempt, actor, checkout SHA, dirty checkout, or manifest hash.

**Pass:** Trusted context is derived from authenticated platform/runtime sources and independently checked. Any mismatch blocks artifact acceptance.

**Fail:** Caller-provided metadata is trusted without verification or a clean-checkout claim is accepted without checking actual state.

**Evidence:** Raw authenticated platform context, derived provenance record, checkout state, and mismatch tests.

### POC-10 — event chain and canonicalization

**Setup:** Use fixed synthetic event vectors covering Unicode, escaping, integer/decimal edge cases, nulls, nested objects, and ordering.

**Exercise:** Verify across every intended writer/runtime; mutate event payload, previous hash, sequence, schema version, and canonicalization version.

**Pass:** Shared test vectors produce identical canonical bytes and hashes across supported runtimes. Tampering and unsupported versions fail closed. Historical v1 hashes are unchanged.

**Fail:** Cross-runtime disagreement is undocumented, or v1 hashes are silently reinterpreted.

**Evidence:** Versioned vector corpus, canonical byte outputs, hash outputs, and historical v1 verification.

### POC-11 — checkpoint rollback and restore

**Setup:** Create a known event chain and independently retained checkpoint witness.

**Exercise:** Restore an older backup, delete the newest events, roll back idempotency indexes, restore assignment state without checkpoint, and restore checkpoint without state.

**Pass:** Rollback/inconsistency is detected and operations stop pending human reconciliation. A complete approved restore preserves chain, index, package objects, state, and checkpoint consistently.

**Fail:** A stale but internally valid backup is accepted as current or a partial restore permits dispatch.

**Evidence:** Backup manifests, witness comparisons, restore logs, and stop-state verification.

### POC-12 — least privilege and isolation

**Setup:** Create separate synthetic identities for human approver, dispatcher, registry service, worker, reviewer, and backup administrator.

**Exercise:** Attempt cross-role reads/writes, worker access to approval/checkpoint data, dispatcher gate closure, reviewer mutation of raw evidence, and test identity access to any non-test resource.

**Pass:** Each identity can perform only its declared operations; prohibited access is denied and audited.

**Fail:** A single broad credential spans trust domains or worker-controlled identity can modify trusted approvals/checkpoints.

**Evidence:** Effective permissions, denied-operation logs, role matrix, and independent access review.

## 5. Global acceptance rules

A candidate is eligible for further review only if:

1. Every mandatory test family has a PASS with retained reproducible evidence.
2. No mandatory test is UNKNOWN, skipped, waived, or replaced by a vendor assertion.
3. Atomicity, concurrency, idempotency, approval, and anti-rollback properties are demonstrated by adversarial tests, not inferred from happy-path success.
4. An independent reviewer reproduces critical cases and validates evidence origin.
5. Cost, quotas, retention, identity separation, recovery, and shutdown behavior meet owner-approved limits.
6. The candidate passes the mandatory qualification gates in the backend selection framework.

One FAIL on atomicity, concurrency, replay, identity, approval, delivery uncertainty, or anti-rollback rejects the candidate for this control-plane use until the defect is resolved and retested. UNKNOWN is not a conditional pass.

A passing proof-of-capability qualifies only the tested configuration and version for an owner decision. It does not authorize production selection, implementation, worker dispatch, or research execution.

## 6. Evidence package

Retain an immutable, reviewable package containing:

- candidate architecture and exact service/region/configuration identifiers;
- provider documentation versions and exact guarantees relied upon;
- synthetic fixture generator version and fixture hashes;
- test harness commit and dependency lock;
- test case ID, start/end UTC time, run identity, and environment identity;
- exact request/response traces with secrets removed;
- before/after registry snapshots and independent checkpoint witness;
- event-chain and idempotency-index verification;
- failure-injection instructions and results;
- cost/usage summary and cleanup proof;
- failures, skipped cases, deviations, and unresolved limitations;
- independent reviewer findings and dated decision.

Do not store credentials, real research data, or personal data in the evidence package.

## 7. Stop and cleanup rules

Immediately stop the exercise if:
- any test reaches a protected research branch, existing research workflow, VPS, production account, or non-synthetic data;
- an identity accesses a resource outside its approved scope;
- a transaction leaves inconsistent state or a checkpoint cannot be reconciled;
- delivery outcome is uncertain and the provider cannot safely reconcile it;
- cost, rate, or runtime limit is reached;
- test evidence contains a secret or sensitive data;
- the active handoff or owner authorization no longer permits the operation.

Revoke test credentials, stop disposable services, remove synthetic test resources according to the approved retention plan, and verify cleanup independently. Preserve only the approved synthetic evidence package and cleanup receipt.

## 8. Current conclusion

This plan is a future evaluation blueprint, not a test report. No candidate has been evaluated, no backend selected, no resource provisioned, no credential created, and no test run. It does not alter the agent's non-operational status or the current G0-05 restrictions.
