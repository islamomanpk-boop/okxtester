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

### 3.1 Internal commit and external witness acknowledgment

The internal registry transaction and an independently administered checkpoint witness are distinct trust-domain operations. Unless a backend proves a genuine cross-system atomic commit, the specification does not claim that both advance atomically.

The database transaction atomically commits the immutable event, materialized state, idempotency indexes, global and assignment versions, internal head checkpoint, and a durable witness-outbox record containing the exact checkpoint tuple and predecessor. This database commit is the lifecycle transition's linearization point.

A separate publisher advances the external witness monotonically and obtains an authenticated witness receipt. The registry records that receipt and the acknowledged witness version in a subsequent transaction. The witness must reject rollback, forks, wrong registry/epoch, same-sequence conflicting digest, and broken predecessor; exact replay returns the original witness receipt.

Between database commit and witness acknowledgment, the registry is durably witness-pending/degraded. It may inspect state and reconcile the exact outbox item, but no further protected lifecycle transition may commit: no approval consumption, dispatch, eligible return acceptance, review completion, human disposition, or restore resume. A lost publish/acknowledgment response is reconciled using the same checkpoint identity, never by creating another event or sequence. On restart, all pending outbox items must be reconciled before protected writes resume. An outbox row is not proof of witness acceptance; database and witness receipts are separate evidence.

Within the database transaction, serialize global-head compare/advance and assignment-state-version compare/update together. Allocate sequence from the locked/compared current head. On serialization failure, deadlock, or unique-key race, abort the whole transaction, reload one consistent snapshot, resolve exact replay before stale-version rejection, and revalidate all current policy, approval, assignment, and transition preconditions. Never retry only the final insert using stale observations.

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
| Cancel assignment | Authenticated cancellation authority; current assignment and dispatch-attempt state | Cancellation record + `assignment_cancelled` event + state version + checkpoint | Prevents future dispatch attempts; an already committed dispatch intent remains in-flight/pending and must be reconciled |
| Receive return | Authenticated receiver; known confirmed delivery; exact assignment binding | Raw payload bytes/ref + receiver digest + return ID + `worker_submission_received` event + checkpoint | `submission_received` |
| Complete review | Exact immutable return; trusted checkout/manifest context; review pipeline completed | Review record + `review_completed` event + checkpoint | `review_completed` |
| Record human disposition | Authenticated human decision tied to exact review and assignment revision | Immutable disposition + `human_disposition_recorded` event + state version + checkpoint | Task disposition recorded |
| Record phase-gate decision | Separate explicit human authority and controlling handoff permits it | Separate gate decision + `phase_gate_disposition_recorded` event + checkpoint | Gate disposition only |

The current G0-05 restriction blocks the protected operations above wherever they conflict with the controlling handoff. This matrix describes future semantics, not current permission.

## 6. Delivery, revocation, and cancellation race rules

The registry transaction that commits `dispatch_started` is the authorization/attempt linearization point. The external provider call is necessarily outside that transaction; therefore database state and provider acceptance cannot be made one atomic action.

- Before the `dispatch_started` transaction commits, cancellation or approval revocation that commits first wins: the dispatcher must deny and must not call the provider.
- The `dispatch_started` transaction must atomically revalidate the exact approval, expiry, revocation state, handoff/policy, assignment state, and idempotency identity; consume a single-use approval; and persist the immutable dispatch attempt and stable provider idempotency key.
- Once that transaction commits, the authorized attempt is irrevocably recorded. A later cancellation or approval revocation prevents any new attempt/revision under that authority but cannot retroactively withdraw, erase, or declare the committed attempt unsent.
- If cancellation commits after `dispatch_started` but before the provider call, the dispatcher must still resolve the already-committed attempt using its original provider idempotency key. It must not silently drop the call and later classify the attempt as not dispatched. If the provider offers a documented cancellation API, it may be invoked only as a separate authenticated operation with its own approval and receipt; it does not rewrite the original attempt.
- If the provider call may have started, or its outcome is unknown, retain `delivery_pending_or_unknown` and reconcile the same provider identity. Never create a fresh identity or automatically retry.
- A provider receipt, including an accepted or rejected response, must be authenticated and bound to the exact attempt, assignment revision, and package digest. A transport-level success alone is insufficient unless provider semantics prove acceptance.
- If the provider lacks durable idempotency and queryable outcome/reconciliation, the design remains blocked. Default decision: do not dispatch.

Cancellation is therefore a durable stop for future work, not a claim that an already-authorized in-flight attempt was recalled. The registry must expose cancellation and dispatch state separately; it must never collapse them into one ambiguous `cancelled` state.

### 6.1 Approval issuance, revocation, consumption, and renewal

Approval issuance facts are immutable. The approval record contains the authenticated issuer/approver, unique approval ID and nonce, exact operation/scope binding, trusted issue time, expiry, and schema version. Revocation and consumption are separate append-only lifecycle facts; implementations must not mutate an approval row to extend expiry, clear revocation, or reset consumption. Current status is a derived view over the immutable approval and verified ordered lifecycle events.

- Enforce uniqueness of approval ID and issuer-scoped nonce. A nonce is bound to the exact approval facts and cannot be reused under another approval ID or delivery identity.
- Exact issuance/revocation replay returns the original receipt without new state changes. Reuse of an identity with changed facts is an integrity conflict.
- Revocation is monotonic. It cannot be undone; an expired, revoked, consumed, or scope-invalidated approval cannot be reactivated.
- Renewal always creates a new approval ID and nonce after a fresh authenticated human decision and full current-scope revalidation. Never extend expiry in place or reuse an old approval ID.
- The protected transaction evaluates expiry using trusted service time and atomically revalidates revocation and unused status while committing the operation and single-use consumption. Client timestamps do not determine validity.
- If revocation commits first, deny the protected operation. If consumption/dispatch-start commits first, preserve that immutable attempt and approval-state receipt; later revocation blocks future use but does not recall or rewrite the attempt.
- A committed dispatch attempt that needs to be stopped requires a separate authenticated provider-cancellation operation and receipt. Approval revocation is not provider cancellation.
- If issuance, revocation, consumption, nonce-index, event-chain, or checkpoint history is missing or unverifiable after restore, approval status is UNKNOWN and the operation is denied. An approval row alone never proves active status.


## 6.2 Orthogonal lifecycle dimensions and recovery projection

The authoritative lifecycle is not one flat status enum. The registry preserves and derives separate, linked dimensions:

1. immutable assignment lineage and revision;
2. approval issuance, consumption, revocation, and trusted-time expiry;
3. each dispatch attempt and its authenticated provider observations;
4. assignment/attempt cancellation as a separate monotonic fact;
5. raw return receipts and receiver-derived eligibility;
6. immutable supervisor review records;
7. authenticated human task disposition; and
8. separate human phase-gate disposition.

A command validates the relevant dimension and all cross-dimension invariants. For example, a return may be durably received but ineligible because it is late, malformed, or not bound to a confirmed attempt; a cancelled assignment may still have an unresolved committed dispatch attempt; and a `needs_revision` disposition does not create a new assignment revision. Do not collapse these cases into a single `cancelled`, `returned`, or `completed` status.

The existing `engine/recovery_policy.py` is only an advisory projection over delivery state, review state, and human disposition. It omits cancellation, approval lifecycle, multiple attempts, return eligibility, assignment revisions, and phase-gate state. It cannot authorize or determine full lifecycle recovery. A future trusted adapter must load a consistent registry snapshot, verify the event chain/checkpoint and authenticated sources, validate the relevant approval and policy at the operation boundary, and apply the exact transition transaction. The helper's output is never a durable state transition or sole authoritative status.

Required transition invariants:
- cancellation before dispatch-start commit denies the attempt; cancellation after commit preserves and reconciles that exact attempt while blocking future attempts;
- later authenticated provider evidence resolves the same attempt and never creates a replacement attempt;
- late, malformed, duplicate-conflicting, or unbound raw returns are preserved but cannot enter normal review/completion;
- exact duplicate receipt/review/disposition replay returns the original receipt; changed facts conflict;
- revision requests require a separately prepared immutable revision and fresh applicable approval;
- human task disposition and phase-gate disposition remain independent.

## 7. Return, review, and human authority rules

The receiver stores raw return bytes before parsing and computes the digest itself. Worker-supplied IDs, hashes, timestamps, task claims, and package claims are comparisons only.

The receiver loads the expected assignment/package from the registry, verifies the package bytes against the retained digest, and binds the return to the exact delivery. It then supplies trusted repository/branch/commit/manifest context to the existing review pipeline.

A structurally valid submission and verified evidence bytes establish only review eligibility and byte integrity. They do not establish research correctness or task completion.

Human task disposition must be authenticated and bound to the exact review digest and assignment revision. Phase-gate closure is a separate authority and event. A task acceptance must never advance the phase automatically.

### 7.1 Worker-return receipt, replay, and eligibility protocol

The receiver is a separate trusted boundary; the current dictionary-based `assignment_return.py` helper is not this receiver. Before any parser or review code runs, the receiver must:

1. Authenticate the return transport and derive the source namespace, return-delivery ID, dispatch attempt, assignment revision, and receipt time from trusted transport metadata. Worker fields cannot supply these facts.
2. Enforce a configured maximum raw payload size. Preserve the exact received bytes in immutable storage and compute the receiver-side SHA-256 over those exact bytes. Do not hash a reserialized parsed object and label it the raw digest.
3. Atomically record the raw receipt, receiver-generated `return_id`, raw digest, byte length, authenticated delivery binding, and idempotency index before parsing. If commit outcome is uncertain, reconcile by the same authenticated return-delivery identity.
4. Parse only retained bytes using strict UTF-8 and strict JSON/schema validation. Reject duplicate keys, non-finite numbers, unsupported values, and unknown schema versions. Preserve malformed bytes and a bounded parse-error classification; malformed returns are not review-eligible. Any normalized form is stored separately and bound to raw digest plus parser/schema/normalization versions.
5. Resolve the delivery identity to a committed dispatch attempt and protected assignment revision. Load and verify the exact retained package bytes/digest from the registry. Worker-claimed task, assignment, package, timestamp, and return IDs are untrusted comparisons only.
6. Enforce unique return transport identity `(return_source_namespace, return_delivery_id)`. Exact key + identical complete immutable facts returns the original receipt and `return_id`; it creates no second receive event or review path. Same key + changed facts is a changed-replay security conflict: preserve the original, quarantine the conflicting arrival, and do not overwrite or accept it.
7. A different authenticated delivery key with identical raw bytes is a separately observed arrival linked by payload digest, not automatically an exact replay. Mark duplicate content and apply an explicit registry policy before any additional review. Never deduplicate solely by worker-declared identifiers, timestamps, or digest.
8. Assign a receiver-derived eligibility classification: `eligible_for_review`, `received_late_after_cancel`, `received_after_expiry`, `received_after_revocation`, `delivery_binding_unknown`, `assignment_or_package_mismatch`, or `malformed_payload`. Eligibility is based on authenticated registry state and trusted service time, never a worker field. Preserve ineligible raw receipts; they cannot enter the normal completion path. Any separately authorized forensic inspection remains non-completion evidence.
9. Bind each immutable review to `return_id`, raw digest, assignment revision, trusted checkout/manifest context, reviewer identity, and reviewer-policy version. Exact review replay returns the original receipt. A corrected review is a new linked record; it never overwrites history.
10. Bind every human disposition to one exact review digest and assignment revision, with its own authenticated idempotency identity. Define explicit supersession semantics for any later human decision. Neither receipt nor review may create a disposition. Phase-gate disposition remains separate.

The atomic transaction must include raw-receipt metadata, immutable return ID, idempotency index, lifecycle event, assignment-state update where applicable, and protected checkpoint. A raw object stored without its corresponding authoritative receipt is not accepted as a committed return. A receipt whose raw object cannot be retrieved and re-hashed is an integrity failure.

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
| Approval expires/revokes or cancellation races with dispatch | If revocation/cancellation commits before `dispatch_started`, deny provider call; if `dispatch_started` commits first, preserve the attempt and reconcile/call only with its original idempotency key; never rewrite history |

A database backup is not itself a trust root. The protected checkpoint must be retained independently enough to detect rollback of a self-consistent but stale database snapshot.

### Restore acceptance protocol

A restore is a security-sensitive state transition, not routine database startup. The service must remain in a non-dispatching, read-only recovery mode until all checks below pass.

1. Freeze dispatch, approval consumption/revocation processing, assignment transitions, return acceptance, and human disposition writes. Preserve the failed instance and backup as immutable incident evidence.
2. Authenticate the restore operator and restore source. Load the independent checkpoint witness through a separately controlled identity and verify its signature/authenticity, registry identity, monotonic epoch, global sequence, head digest, schema/canonicalization versions, and witness freshness.
3. Verify the restored database's registry identity, epoch, global sequence/head digest, complete event chain, assignment state versions, immutable package/return/review digests, unique indexes, and transaction consistency.
4. Require an exact match between restored state and the independently witnessed checkpoint tuple. A lower sequence/epoch is stale; a higher sequence, different digest at the same sequence, wrong registry identity, or incompatible schema/version is a fork or integrity conflict. Every mismatch fails closed. Never choose whichever copy is newer based only on its local timestamp.
5. If the backup is behind, restore missing committed history only from an independently authenticated append-only recovery source that proves the exact missing sequence and event digests. Do not reconstruct missing approvals, revocations, dispatch attempts, receipts, returns, or dispositions from workflow inputs, worker artifacts, logs without authenticated provenance, or operator recollection. If complete authoritative history cannot be recovered, keep the registry inactive and require a documented human incident decision; do not silently create a new genesis.
6. Reconcile every nonterminal dispatch against the authenticated provider using its original delivery identity/idempotency key. Resolve committed-but-unacknowledged attempts, pending/unknown deliveries, provider acceptance/rejection, and any provider-side cancellation receipt. No new delivery identity or retry is permitted while any prior outcome is unresolved.
7. Confirm that approvals/revocations, expiry, cancellation flags, consumed single-use approvals, and assignment revisions are at least as current as the witness-protected head. An approval absent from the restored snapshot must never be presumed active; a revocation or consumption event missing from restored state blocks the affected operation.
8. Verify backup integrity, package/return object availability, access-control separation, and independent witness reachability. Record a signed restore report containing backup ID, registry ID, pre/post epoch and sequence, checkpoint digest, recovered ranges, unresolved provider deliveries, reviewer identities, and explicit resume decision.
9. Require independent human review and a separate resume authorization bound to the exact restored checkpoint and recovery report. Only then may the registry return to service; scheduling/dispatch remain separately gated.

A restore that cannot prove exact checkpoint lineage is not accepted. A clean database integrity check alone is insufficient.

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
