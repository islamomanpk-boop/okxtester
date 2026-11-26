# Trusted registry backend interface specification

## Status and authority

**Design-only contract.** This document defines minimum backend-neutral semantics for a future trusted assignment registry. It does not select a database, cloud provider, identity provider, worker provider, or deployment topology, and it does not authorize implementation, tests, workflows, dispatch, scheduling, or research execution.

The Phase 3 G0-05 handoff remains controlling. No registry operation described here is live. Existing pure modules remain non-persistent and non-authorizing.

## 1. Design goals and trust boundaries

The registry is the single durable authority for assignment lifecycle state. It must preserve immutable task definitions, assignment revisions, exact package bytes/digests, approvals/revocations, dispatch attempts, authenticated provider receipts, raw worker returns, supervisor reviews, human dispositions, a globally sequenced lifecycle event log, idempotency indexes, and protected checkpoints.

Separate trust domains are required for:
1. reviewed task/policy/handoff source;
2. human approval and revocation authority;
3. workflow/dispatcher identity;
4. registry/store and protected checkpoint;
5. worker/provider delivery and returns;
6. checkout-derived evidence;
7. supervisor/reviewer; and
8. backup/recovery witness.

Workers must never write task definitions, approvals, revocations, expected package digests, checkpoints, review decisions, or phase-gate records. A workflow must not self-approve its protected operation. A store administrator must not silently rewrite history or roll back the checkpoint.

## 2. Immutable record model

Every record has a schema version, stable ID, canonical representation and creation provenance. Corrections create new records/events; committed records are never edited in place.

| Record | Required binding |
|---|---|
| Task definition | task ID, exact canonical bytes, digest, phase, operation, handoff revision, scope, prohibitions, source commit |
| Assignment | assignment ID, task ID/digest, current revision, status, per-assignment state version |
| Assignment revision | assignment/revision IDs, parent revision, exact package bytes and digest |
| Approval | approval ID, assignment revision/package digest, task digest, exact operation, repo/ref, workflow identity/revision, input commit, handoff/policy revision, scope, approver, issue/expiry, nonce/consumption policy |
| Revocation | revocation ID, approval ID, revoker identity, effective sequence/time, reason |
| Dispatch attempt | attempt ID, assignment revision/package digest, approval ID, authenticated workflow run/attempt, provider idempotency key |
| Provider receipt | provider namespace, delivery ID, attempt ID, authenticated receipt bytes/digest, status, observed time |
| Worker return | return ID, assignment/revision/package digest, authenticated delivery identity, raw immutable payload bytes/digest |
| Review | review ID, return ID/payload digest, reviewer, review-policy version, structural and evidence results, review digest |
| Human disposition | disposition ID, assignment revision, review digest, human identity, accepted/rejected/needs-revision, reason/time |
| Phase-gate disposition | separate gate/evidence digest and authorized human decision; prohibited under current G0-05 handoff |
| Lifecycle event | global sequence, event ID/type/version, subject IDs, authenticated source, canonical payload, previous hash, event hash |
| Idempotency record | authenticated source namespace, delivery ID, event role, normalized facts digest, original receipt/sequence |
| Checkpoint | global registry version, latest event sequence/hash, generation and independent integrity proof |

Changing scope, handoff, input commit, workflow revision or package requires a new assignment revision and fresh approval.

## 3. Backend-neutral interface

A backend may expose methods, RPCs or commands, but must implement equivalent semantics.

### Trusted read ports

- `load_policy_snapshot()`: authenticated policy, handoff revision, phase order and prohibitions.
- `load_task(task_id)`: exact immutable task bytes and independently verified digest.
- `load_assignment(assignment_id)`: consistent current revision, state and state version.
- `load_assignment_package(assignment_id, revision)`: exact stored bytes and digest.
- `load_approval(approval_id)`: approval and revocation state from trusted authority.
- `lookup_delivery(source_namespace, delivery_id, event_role)`: original receipt or absence.
- `load_events(after_sequence, limit)`: bounded ordered range with verifiable chain context.
- `load_checkpoint()`: protected checkpoint plus external integrity proof.
- `reconcile_assignment(assignment_id)`: consistent view of attempts, receipts, returns, reviews and dispositions.

Protected reads require authenticated identity and snapshot/version consistency; unrelated table reads without a consistent snapshot are insufficient.

### Transactional command ports

Equivalent atomic commands are required for `prepare_assignment`, `record_approval`, `revoke_approval`, `start_dispatch`, `record_delivery_uncertain`, `confirm_delivery`, `cancel_assignment`, `receive_worker_return`, `complete_supervisor_review`, `record_human_disposition`, and `record_phase_gate_disposition` (disabled while prohibited).

Each command receives authenticated caller context, exact subject IDs, expected global checkpoint/version, expected assignment state version, idempotency identity and operation-specific data. Actor, repository, workflow, commit, approval and delivery identities must not be trusted merely because they appear in a payload.

A successful command returns an authenticated receipt only after commit: command/event IDs, idempotency key and facts digest, committed sequence/hash, resulting global and assignment versions, affected record IDs/digests, timestamp and transaction ID. A timeout is an unknown outcome; reconcile by idempotency key before retry.

## 4. Atomicity and concurrency

One lifecycle transition must atomically commit:
1. immutable new records;
2. lifecycle event and hash linkage;
3. idempotency index;
4. materialized assignment state and per-assignment version;
5. global sequence and protected checkpoint; and
6. transaction receipt/outbox record, if used.

No partial commit may be represented as success. Every transition checks and advances both the global registry version and the per-assignment state version in the same transaction. The durable atomic commit is the linearization point.

External delivery occurs outside the database transaction. The registry first records a dispatch attempt; until authenticated provider evidence is committed, state remains pending/uncertain.

## 5. Idempotency and replay

Use two linked identity levels: `(source_namespace, delivery_id)` is the unique authenticated provider-delivery identity; `(source_namespace, delivery_id, event_role)` is the unique lifecycle-event idempotency identity when one delivery emits multiple legitimate events. Event role is a closed schema-defined value. Source namespace must be authenticated. Normalize complete semantic facts, then look up the event-level idempotency tuple **before** rejecting a stale checkpoint:
- same key + same facts: return original receipt, no second event;
- same key + changed facts: reject as changed replay and raise a security signal;
- new key: verify global and assignment versions and current state, then atomically commit.

The facts digest covers subject IDs, revision, package/task digests, operation, approval, provider receipt, source identity and meaning-bearing payload. Delivery ID alone is insufficient.

## 6. Approval and revocation

Task allowlisting is not operation approval. Approval binds to task digest, assignment/revision/package digest, repository/ref/input commit, workflow identity and immutable revision, handoff/policy revision, exact operation/scope, approver, issue/expiry and nonce/consumption policy.

Immediately before the protected operation, re-read approval, revocation, handoff and policy. A prior preflight ALLOW, queue field, worker declaration or workflow input is not approval. Expired, revoked, mismatched or unverifiable approvals fail closed. Single-use consumption is atomic with the authorized operation.

Revocation races are serialized: if revocation commits first, deny; if the operation commits first, record the exact approval state/sequence used. Revocation never erases historical facts.

## 7. Dispatch and provider requirements

Dispatch remains disabled unless the provider supports durable idempotency plus queryable outcome, or a documented query/reconciliation protocol that prevents duplicate work. Otherwise unattended delivery is prohibited.

Sequence: load exact stored package; authenticate dispatcher; revalidate handoff/policy/approval; atomically record dispatch start and unique provider key; invoke provider; commit authenticated receipt or explicit uncertain outcome. Timeouts, missing artifacts and worker silence do not prove non-delivery. Never automatically retry an uncertain attempt. Cancellation and provider acceptance races must be serialized; cancellation cannot erase an accepted receipt.

## 8. Return, review and human authority

Authenticate return source and bind it to exact assignment revision, package digest and delivery attempt. Preserve raw payload bytes before parsing. Review binds immutable return ID/digest, task/revision, trusted package digest, authenticated checkout commit and independently derived evidence manifest, review policy/version and reviewer identity.

Evidence byte integrity is not source truth or research correctness. Structural eligibility is not task completion. Human task disposition is not phase-gate closure. Gate decisions require separate authority and evidence and remain unavailable while the handoff prohibits them.

## 9. Error taxonomy

| Error | Required behavior |
|---|---|
| `AUTHENTICATION_FAILED` | deny; do not downgrade identity |
| `AUTHORIZATION_DENIED` | stop and request human review |
| `STALE_HANDOFF_OR_POLICY` | rebuild/review assignment; fresh approval |
| `APPROVAL_EXPIRED_OR_REVOKED` | deny; never reuse |
| `STATE_CONFLICT` | reconcile; no blind retry |
| `EXACT_REPLAY` | return original receipt |
| `CHANGED_REPLAY` | reject and alert |
| `INVALID_TRANSITION` | reject without state change |
| `DELIVERY_OUTCOME_UNKNOWN` | reconcile; no automatic retry |
| `INTEGRITY_FAILURE` | quarantine affected scope and stop |
| `BACKEND_UNAVAILABLE` | fail closed; no offline authorization |
| `SCHEMA_VERSION_UNSUPPORTED` | reject; preserve raw bytes for investigation |

Errors must not leak secrets or protected data.

## 10. Backup and anti-rollback

Backups contain a consistent snapshot of events, immutable records, idempotency indexes, materialized state and checkpoint metadata. Restore into isolation; verify schema versions, full event chain, package/return digests, idempotency uniqueness and materialized state by replay; compare checkpoint against an independently held monotonic/signed witness; reconcile provider deliveries; require explicit human authorization before reconnecting dispatch.

An internally valid hash chain cannot detect restoration of an older internally consistent chain. Anti-rollback therefore requires an independent monotonic or externally witnessed checkpoint. Define encryption, access, retention and separately approved restore exercises.

## 11. Conformance plan (not executed)

Independent acceptance evidence must cover concurrent atomic commits; global and per-assignment stale-token rejection; exact replay after checkpoint advancement; changed replay rejection; concurrent first-delivery races; approval expiry/revocation races; cancellation/provider races; timeout after provider acceptance; crash/restart without duplicate delivery; raw return/package binding; tampered event/package/checkpoint/evidence rejection; stale-backup rollback detection; unknown schema fail-closed behavior; role separation; authenticated receipt verification.

These are requirements only. No test code, tests, failure injections or implementation are included.

## 12. Current status and decisions still required

- No backend, hosting boundary, identity/approval provider or service identity is selected.
- No authenticated registry API, durable checkpoint, dispatcher or delivery channel exists.
- Current `event_ledger.py` and `persistence_contract.py` remain pure in-memory primitives.
- Event v1 remains unchanged; v2 and unified transaction documents remain proposals.
- Package digests are calculated but not independently stored.
- No agent workflow is active; the agent is not operational.
- No tests, scripts, workflows, dispatch, scheduling, VPS access or research execution were performed for this specification.
- G0-05 remains authoritative and blocks prohibited Phase 3 execution and gate actions.

Before implementation, the project owner must explicitly select repository topology, backend/hosting, independent identity and approval roots, canonicalization version, checkpoint witness, retention/backup policy and provider capability. Any implementation must be separately authorized against the then-current handoff.
