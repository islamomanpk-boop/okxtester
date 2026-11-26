# Unified trusted lifecycle transaction specification

## Status and authority

Proposal only. This document reconciles the event schema v2, trusted assignment registry, trusted store adapter, and dispatcher contracts into one backend-neutral transaction model. It does not approve implementation or select a backend.

The current Phase 3 G0-05 handoff remains controlling. No task execution, dispatch, schedule, test, workflow, research-data/code change, gate closure, or phase advancement is authorized by this specification. The agent remains non-operational.

## 1. Normative architecture decision

Use one **trusted assignment registry** as the authoritative lifecycle service. It owns:

- immutable task/assignment/package records and revisions;
- authenticated operation approvals and revocations;
- delivery attempts and idempotency indexes;
- raw worker-return receipts;
- structural/evidence review records;
- authenticated human task dispositions;
- one globally sequenced v2 registry event log;
- materialized current state and protected checkpoint.

The v1 event ledger remains unchanged as legacy evidence. It is not a second live authority for v2 lifecycle state. No v1 event is silently promoted, rewritten, or re-hashed.

The registry may use multiple physical tables/objects, but all authoritative changes for one transition must share one atomic transaction boundary. If the chosen backend cannot provide this, implementation is blocked until a separately reviewed transactional outbox/inbox protocol proves equivalent guarantees.

## 2. Identity model

Keep these identifiers distinct; never overload one for another.

| Identifier | Issuer | Purpose |
|---|---|---|
| `task_id` + task-definition digest | Trusted queue/policy | Identifies the exact authorized task definition |
| `assignment_id` | Registry | Stable identity of one assignment lineage |
| `assignment_revision` | Registry | Immutable package revision within that lineage |
| `assignment_package_sha256` | Registry | Digest of exact canonical package bytes |
| `approval_id` | Authenticated approval service | One exact, scoped human approval |
| `dispatch_attempt_id` | Dispatcher | One attempt to initiate delivery |
| `source_namespace` + `delivery_id` | Authenticated platform/provider | Idempotency identity of an incoming trigger or delivery |
| `return_id` | Trusted receiver | One immutable received worker-return payload |
| `review_id` | Supervisor service | One review of one exact return |
| `event_id` + registry sequence | Registry | One immutable ordered lifecycle event |
| `checkpoint_version` + digest | Protected store | Rollback/concurrency anchor for the registry head |

An assignment revision is immutable. A change to task digest, package bytes, scope, prohibitions, handoff revision, workflow identity, input commit, or operation requires a new revision and fresh approval where approval is required.

## 3. One event log, two concurrency checks

The v2 registry log has a single monotonically increasing global sequence and hash chain. This provides total ordering across assignments and approvals.

Each assignment also has a monotonically increasing `state_version`. This prevents stale writers from transitioning one assignment based on an old state.

A successful transition must satisfy both:

1. the caller's expected registry checkpoint/version matches the current protected global head (except exact replay, which is resolved first); and
2. the caller's expected assignment state version matches the current assignment state.

Both are checked and advanced in the same transaction. The global sequence is allocated transactionally. No client chooses a sequence, event hash, or checkpoint.

## 4. Authoritative transaction protocol

Every state-changing command follows this protocol. Read-only queries do not append events.

### Phase A — authenticate and normalize

1. Authenticate the caller at the platform/service boundary.
2. Derive actor, source namespace, delivery identity, repository, ref, workflow identity, run/attempt, and provider context from authenticated transport metadata.
3. Reject worker-supplied claims as sources of authority. They may be retained as untrusted payload fields only.
4. Validate strict input types, schema version, bounded size, and closed event/command schema.

### Phase B — replay before concurrency rejection

5. In the transaction, look up the authenticated idempotency tuple `(source_namespace, delivery_id, event_role)`.
6. If it exists, compare the complete canonical immutable facts and operation binding:
   - exact match: return the original committed receipt without changing state, event log, sequence, or checkpoint;
   - mismatch: reject as an integrity/security conflict and preserve the original record.
7. Only if no exact prior delivery exists, compare the expected protected checkpoint/version and assignment state version. A mismatch rejects the new transition without side effects.

The idempotency tuple is scoped by event role because one authenticated platform delivery may legitimately produce a small, fixed set of distinct records. The allowed roles and their cardinality must be explicit per command. Arbitrary role strings are forbidden.

### Phase C — revalidate authority and transition

8. Verify registry snapshot, v2 hash chain, checkpoint authenticity, assignment/package digests, unique indexes, and state consistency.
9. Re-read the current controlling handoff and policy from the trusted source. Verify exact task digest, repository, isolated branch, phase, operation, scope, prohibitions, global switches, and allowlist.
10. For a protected operation, validate the authenticated approval at the operation boundary: actor/authority, exact operation, assignment revision/package digest, workflow path and immutable SHA, repository/ref, handoff revision, input commit, scope digest, expiry, single-use state, and revocation state.
11. Validate the state-machine transition from the current authenticated prior state. Reject impossible, expired, revoked, cancelled, stale, or ambiguous transitions.

A queue allowlist hash, task preflight, planner output, assignment package, or prior readiness approval is never a substitute for the exact approval required by the current operation.

### Phase D — commit all authoritative facts atomically

12. Allocate the next global event sequence and compute the v2 event digest using the declared canonicalization version.
13. Append the event and update the relevant materialized state.
14. Update the assignment state version where assignment state changes.
15. Insert/update the authenticated idempotency index and any provider delivery index.
16. Advance the protected checkpoint/version.
17. Commit all changes atomically.
18. Return a receipt only after commit. The receipt states exactly what was durably recorded; it never implies worker execution, task completion, research correctness, or gate closure.

## 5. Command-to-event and transaction matrix

| Command | Preconditions | Atomic writes | Resulting state |
|---|---|---|---|
| Prepare assignment | Exact queued task; permitted preflight; policy/handoff check; package canonicalized | Immutable assignment revision + package bytes/ref + digest + `assignment_prepared` event + checkpoint | `prepared_not_dispatched` |
| Record approval | Authenticated human approval for exact operation and immutable scope | Immutable approval record + `approval_recorded` event + checkpoint | Approval active for exact scope |
| Revoke approval | Authenticated revocation authority; exact approval ID | Revocation record + `approval_revoked` event + checkpoint | Approval unusable for future protected operations |
| Start dispatch | Exact revision; valid delivery approval; fresh policy/handoff check; unused delivery identity | Dispatch intent/attempt + `dispatch_started` event + idempotency index + state version + checkpoint | `dispatch_started` |
| Record uncertain delivery | Authenticated timeout/lost-response observation | Delivery state + `delivery_pending_or_unknown` event + state version + checkpoint | `delivery_pending_or_unknown` |
| Confirm delivery | Authenticated provider receipt bound to attempt and package digest | Receipt + `delivery_confirmed` event + state version + checkpoint | `delivery_confirmed` |
| Cancel assignment | Authenticated cancellation authority | Cancellation record + `assignment_cancelled` event + state version + checkpoint | Cancelled where no irreversible delivery already occurred |
| Receive return | Authenticated receiver; known confirmed delivery; exact assignment binding | Raw payload bytes/ref + receiver digest + return ID + `worker_submission_received` event + checkpoint | `submission_received` |
| Complete review | Exact immutable return; trusted checkout/manifest context; review pipeline completed | Review record + `review_completed` event + checkpoint | `review_completed` |
| Record human disposition | Authenticated human decision tied to exact review and assignment revision | Immutable disposition + `human_disposition_recorded` event + state version + checkpoint | Task disposition recorded |
| Record phase-gate decision | Separate explicit human authority and controlling handoff permits it | Separate gate decision + `phase_gate_disposition_recorded` event + checkpoint | Gate disposition only |

The current G0-05 restriction blocks the protected operations above wherever they conflict with the controlling handoff. This matrix describes future semantics, not current permission.

## 6. Delivery and cancellation race rules

- Persist a durable dispatch intent and stable idempotency identity before making the external delivery call.
- A request being constructed or sent is not proof of provider acceptance or worker receipt.
- If the external call times out, record pending/unknown if authenticated facts permit; otherwise leave commit outcome unknown and reconcile using the same identity.
- Never automatically issue a second delivery for pending/unknown state.
- Approval revocation and cancellation are serialized against dispatch authorization. If dispatch has already crossed the durable dispatch-start boundary, later cancellation cannot erase the attempt or assert non-delivery.
- Provider confirmation must be authenticated and bound to the exact attempt, assignment revision, and package digest.
- If the provider lacks idempotent delivery or queryable receipts, the risk must be explicitly accepted by a human before any future dispatch design can proceed. Default decision: do not dispatch.

## 7. Return, review, and human authority rules

The receiver stores raw return bytes before parsing and computes the digest itself. Worker-supplied IDs, hashes, timestamps, task claims, and package claims are comparisons only.

The receiver loads the expected assignment/package from the registry, verifies the package bytes against the retained digest, and binds the return to the exact delivery. It then supplies trusted repository/branch/commit/manifest context to the existing review pipeline.

A structurally valid submission and verified evidence bytes establish only review eligibility and byte integrity. They do not establish research correctness or task completion.

Human task disposition must be authenticated and bound to the exact review digest and assignment revision. Phase-gate closure is a separate authority and event. A task acceptance must never advance the phase automatically.

## 8. Canonicalization and immutable history

- V1 hashes remain governed by the existing v1 Python serialization contract and are never rewritten.
- V2 must select and version an explicit canonicalization contract before implementation; RFC 8785/JCS is the preferred candidate, subject to test-vector validation.
- Canonicalization version is immutable registry metadata and is included in the hash domain separation.
- Event digest input includes schema version, canonicalization version, registry ID, sequence, previous digest, and all immutable event facts except the digest field itself.
- Reject duplicate keys, non-string keys, non-finite numbers, unsupported values, ambiguous timestamps, and unknown fields.
- Shared independent test vectors are required before multiple runtimes can write or verify v2 events.

## 9. Crash, retry, and recovery semantics

| Failure point | Required outcome |
|---|---|
| Before transaction commit | No partial authoritative writes; retry same idempotency identity |
| Commit succeeds, response lost | Exact retry returns original receipt |
| Concurrent duplicate delivery | Unique constraint selects one winner; loser re-reads and compares complete facts |
| Stale global checkpoint or assignment version | Reject new transition without mutation |
| Duplicate identity with changed facts | Integrity conflict; preserve original |
| External delivery outcome unknown | Reconcile same provider identity; no automatic retry |
| Registry/event/checkpoint mismatch | Stop all writes; preserve evidence; human investigation |
| Backup restore behind protected checkpoint | Reject service startup/operations until independently reconciled |
| Approval expires/revokes during dispatch race | Transaction ordering determines whether dispatch crossed the authorized boundary; preserve both facts, never rewrite history |

A database backup is not itself a trust root. The protected checkpoint must be retained independently enough to detect rollback of a self-consistent but stale database snapshot.

## 10. Minimum backend acceptance criteria

A candidate backend is unsuitable unless it provides or can rigorously compose:

- atomic multi-record transactions or proven equivalent;
- serializable/compare-and-swap behavior for global checkpoint and per-assignment state version;
- durable unique constraints for idempotency and identifiers;
- authenticated service identities and least-privilege separation from workers;
- immutable/content-addressed package and raw-return storage;
- protected checkpoint with rollback detection;
- reliable backup/restore and retention;
- audit logs and operational observability;
- bounded cost, quotas, concurrency, and failure recovery.

GitHub Actions artifacts are suitable for immutable run outputs, not a mutable transactional registry. Repository commits are not automatically a trusted compare-and-swap store. No backend is selected here.

## 11. Implementation gates and current status

Before implementation, obtain separate approval for repository topology, backend, identity/access model, approval channel, retention, and backup/restore. Complete a threat model and failure-injection matrix. Independently review the schema and transaction design. Then obtain a controlling handoff that explicitly permits the exact code, test, and workflow scope.

Current status:

- V2 is a proposal only; v1 implementation and hashes are unchanged.
- No registry, database, approval service, dispatcher, delivery channel, or receiver exists.
- No authenticated lifecycle event has been persisted by a trusted adapter.
- No agent workflow, schedule, dispatch, or unattended worker is active.
- No tests, scripts, or workflows were run for this specification.
- No research branch, default branch, research data, secrets, permissions, VPS, or runner configuration was changed.
