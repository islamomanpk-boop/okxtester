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
- `lookup_provider_delivery(source_namespace, delivery_id)`: the complete authenticated provider-delivery aggregate, including all linked per-role event receipts and the original delivery/dispatch receipt.
- `lookup_event_receipt(source_namespace, delivery_id, event_role)`: the original receipt for one closed-schema lifecycle-event role, or absence. This is the event-level idempotency lookup used by the transaction replay protocol.
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

### Internal transaction versus external witness

The backend transaction atomically commits registry records, lifecycle event, idempotency indexes, materialized state, global/assignment versions, internal head checkpoint, and a durable outbox item for the independent checkpoint witness. This database commit is the registry transition's linearization point. Do not claim the external witness participates in the database ACID transaction unless the selected platform proves that exact cross-system guarantee.

A separate witness publisher advances the external monotonic checkpoint and obtains an authenticated receipt. The registry records the receipt/acknowledged version in a subsequent transaction. Until acknowledgment of the exact committed head, protected writes are frozen in witness-pending/degraded mode; read-only reconciliation is permitted. Restart must reconcile all pending outbox items before protected operations resume. Lost responses use the same checkpoint identity. An outbox row is not a witness receipt.

The witness rejects rollback, forks, wrong registry/epoch, non-monotonic sequence, broken predecessor, and same-sequence conflicting digest; exact replay returns the original receipt. Database commit receipt and witness receipt remain distinct.

Global checkpoint advancement and per-assignment state-version comparison/update must be serialized together in the database transaction. On serialization failure, deadlock, or uniqueness conflict, abort all writes, reload a consistent snapshot, resolve exact replay first, and revalidate current approval, policy, assignment state, and transition. Never retry a partial insert or reuse stale preconditions.

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

Approval lifecycle invariants:
- Approval issuance facts are immutable; revocation and consumption are separate append-only records/events. Current status is derived from verified history and trusted service time, never from a mutable approval-status field alone.
- Enforce unique approval IDs and issuer-scoped nonces. A nonce is bound to one immutable approval digest; reuse with another approval or delivery identity is rejected.
- Exact issuance or revocation replay returns the original receipt; changed facts under the same idempotency identity are rejected. A second conflicting revocation cannot rewrite the first.
- Revocation is monotonic. No un-revoke, reactivation, expiry extension, or in-place renewal is permitted.
- Renewal requires a new approval ID and nonce, fresh authenticated human decision, current policy/handoff check, and complete new scope binding. The prior approval remains terminal in history.
- Expiry is checked using trusted transaction/service time inside the same serialized operation transaction. A client timestamp or request-arrival time cannot preserve an approval past expiry.
- If consumption/dispatch-start commits first, later revocation blocks future use but does not erase or recall that attempt. Provider-side cancellation is a distinct authenticated command with its own idempotency and receipt.
- Missing or unverifiable issuance, revocation, consumption, nonce-index, or checkpoint history makes approval status UNKNOWN and denies protected operations.


## 7. Dispatch and provider requirements

Dispatch remains disabled unless the provider supports durable idempotency plus queryable outcome, or a documented query/reconciliation protocol that prevents duplicate work. Otherwise unattended delivery is prohibited.

Sequence: load exact stored package; authenticate dispatcher; revalidate handoff/policy/approval; atomically record dispatch start and unique provider key; invoke provider; commit authenticated receipt or explicit uncertain outcome. Timeouts, missing artifacts and worker silence do not prove non-delivery. Never automatically retry an uncertain attempt. Cancellation and provider acceptance races must be serialized; cancellation cannot erase an accepted receipt.

## 8. Return, review and human authority

Authenticate return source and bind it to exact assignment revision, package digest and delivery attempt. Preserve raw payload bytes before parsing. Review binds immutable return ID/digest, task/revision, trusted package digest, authenticated checkout commit and independently derived evidence manifest, review policy/version and reviewer identity.

Evidence byte integrity is not source truth or research correctness. Structural eligibility is not task completion. Human task disposition is not phase-gate closure. Gate decisions require separate authority and evidence and remain unavailable while the handoff prohibits them.

### Return receipt command semantics

`receive_worker_return` must receive authenticated transport context plus the exact raw byte stream, not a worker-supplied parsed object as the authoritative receipt. The adapter enforces a byte-size bound, stores bytes immutably, computes the receiver digest, and atomically commits return ID, authenticated return-delivery idempotency record, receipt event, assignment binding/eligibility, and checkpoint before parsing. Parsing is strict and occurs only from retained bytes; malformed raw bytes remain auditable and cannot enter review.

Enforce unique `(return_source_namespace, return_delivery_id)`. The immutable facts digest covers dispatch attempt, assignment/revision, expected package digest, authenticated source, raw digest/length, and meaning-bearing transport metadata. Exact replay returns the original receipt; changed replay is quarantined and rejected without altering the original. A distinct delivery ID with identical bytes is linked by payload digest as duplicate content and is not automatically eligible for a second review.

The command must resolve the provider delivery to a committed dispatch attempt and load the exact protected package. It records a receiver-derived eligibility classification from trusted state/time. Review identity is idempotently bound to return ID, raw digest, assignment revision, reviewer identity, and policy version. Human disposition is independently authenticated and bound to one exact review digest. Receipt, review, task disposition, and phase-gate disposition remain separate records and authorities.

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

Restore must reconcile the internal database head and durable witness outbox against the external witness before classifying an ahead snapshot as a fork. A head exactly one sequence ahead is witness-pending only if one durable outbox item exactly extends the witness tuple (registry, epoch, sequence, head digest, predecessor); replay that same tuple and record the authenticated witness receipt without creating a new event. At most one unacknowledged checkpoint is allowed because protected writes freeze while pending. If the witness is ahead, recover exact missing history from an independently authenticated append-only source. Any larger unexplained lead, missing/mismatched outbox, broken predecessor, same-sequence fork, or identity/schema mismatch fails closed. Resume requires full provider-attempt, approval/revocation/consumption, assignment, and raw-return reconciliation plus separate human authorization bound to the exact recovered checkpoint.

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


## Independent emergency-hold enforcement

Every protected command must be denied when an applicable emergency hold is active or its status, authenticity, freshness, scope, or monotonic epoch cannot be verified. The hold is deny-only and is not an approval source.

The selected implementation must prove a race-safe operation boundary: protected commits after the hold's effective linearization point are rejected, while an operation already committed before that point remains an immutable attempt to reconcile. A stale cached “no hold” result is insufficient. The design must bind each protected transaction to a fresh authenticated hold epoch/fencing value and prove that hold activation invalidates or fences later commits. If the chosen security plane cannot provide this guarantee, disable the dispatcher/registry ingress through an independently controlled credential or gateway kill switch and keep the affected capability offline until in-flight operations are reconciled. Do not claim an instantaneous freeze without a demonstrated linearization and revocation-latency bound.

During registry freeze or witness-pending state, the security plane may disable credentials/sessions/keys and maintain the external incident hold, but may not write registry approval-revocation events. After exact witness reconciliation, append and witness the required approval revocations/invalidation before releasing the hold. The external hold and registry approval history are separate facts and audit sources.
