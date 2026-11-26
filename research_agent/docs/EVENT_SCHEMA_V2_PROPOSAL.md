# Event schema v2 proposal

## Status and authority

Proposal only. This document does not change the v1 event implementation, authorize a v2 implementation, select a persistence backend, or permit task execution, dispatch, scheduling, tests, workflows, research changes, gate closure, or phase advancement. The current Phase 3 G0-05 handoff remains controlling.

This proposal resolves the event-vocabulary gap identified in `TRUST_BOUNDARY_CROSSWALK_2026-11-26.md`. It is a design decision for review, not an approved implementation specification.

## Decision

Adopt a separately versioned v2 event envelope for the future trusted assignment registry. Preserve the current v1 task event ledger as a legacy, immutable format. Do not retrofit v1 event names or payloads to represent new lifecycle transitions.

The future registry should own one append-only, globally sequenced transition log. Each event carries task and assignment identities where applicable, and each registry transaction updates the materialized registry state, idempotency indexes, event log, and protected checkpoint atomically.

The v2 log is the authoritative history for assignment lifecycle transitions. Existing v1 events may be imported as explicitly labelled legacy observations only after a separately reviewed mapping; they must not be silently rewritten, re-hashed, or treated as authenticated v2 transitions.

## Why this choice

A separate typed v2 envelope provides:

- backwards compatibility for all existing v1 hashes and meanings;
- explicit schema-level validation for each lifecycle transition;
- one ordering authority across assignments, approvals, deliveries, returns, and reviews;
- a clear atomic transaction boundary with registry state and idempotency indexes;
- room to version canonicalization independently of the legacy Python serializer.

A separate unrelated log without a single registry sequence would make ordering and atomic linkage harder to reason about. Extending v1 in place would risk changing historical semantics and hashes. The v2 registry log therefore becomes the future source of lifecycle truth, while v1 remains preserved historical evidence.

## V2 envelope

The following is a conceptual field contract, not a ready-to-implement JSON schema:

| Field | Requirement |
|---|---|
| `schema_version` | Exact integer `2`; booleans are invalid |
| `event_id` | Stable globally unique identifier derived by the trusted adapter |
| `sequence` | Strictly increasing registry-wide integer assigned transactionally |
| `event_type` | Exact allowlisted v2 event name |
| `occurred_at_utc` | Canonical UTC occurrence timestamp |
| `recorded_at_utc` | Trusted adapter's canonical UTC commit/record time |
| `task_id` | Required for task-bound events |
| `task_definition_sha256` | Exact trusted task-definition digest |
| `assignment_id` | Required for assignment lifecycle events |
| `assignment_revision` | Positive integer revision for revisioned assignments |
| `assignment_package_sha256` | Required when an event refers to an exact prepared package |
| `approval_id` | Required for approval/revocation events |
| `delivery_id` | Authenticated upstream delivery identity where applicable |
| `source_namespace` | Trusted adapter-derived provider/tenant/channel namespace |
| `source_type` | Allowlisted authenticated source category |
| `source_ref` | Stable, non-secret source reference |
| `payload` | Event-type-specific strict object; no arbitrary authority fields |
| `previous_event_sha256` | Prior registry event digest, or the defined genesis value |
| `event_sha256` | Digest over the versioned canonical envelope excluding this digest field |

The adapter, not the worker, assigns `sequence`, derives source identity, and controls the trusted timestamps and hash-chain fields. Worker-provided values for these fields are declarations and must never be accepted as authentication.

## Proposed event vocabulary

All names below are proposed and require review before implementation.

| Event type | Meaning | Required binding |
|---|---|---|
| `task_observed` | Trusted system observed an eligible task definition | task ID + task digest |
| `assignment_prepared` | Immutable assignment package was created and retained | task + assignment ID/revision + package digest |
| `assignment_revision_created` | New immutable revision supersedes a prior prepared revision | assignment ID + prior/new revision + new package digest |
| `approval_recorded` | Authenticated human or policy authority approved one exact operation | approval ID + assignment revision + operation + scope digest |
| `approval_revoked` | Previously recorded approval was revoked | approval ID + revocation authority/reference |
| `dispatch_started` | Trusted dispatcher began one delivery attempt | assignment revision + approval ID + attempt ID |
| `delivery_pending_or_unknown` | Delivery outcome cannot yet be established | attempt ID + authenticated provider request/delivery reference |
| `delivery_confirmed` | Trusted provider response or authenticated receipt confirms delivery | attempt ID + provider delivery ID + assignment digest |
| `assignment_cancelled` | Trusted authority cancelled an assignment revision | assignment revision + cancellation authority |
| `worker_submission_received` | Authenticated receiver stored a worker return | assignment revision + return ID + raw return digest |
| `review_completed` | Supervisor review result was durably recorded | return ID + review digest + assignment revision |
| `human_disposition_recorded` | Human accepted, rejected, or requested revision for one reviewed assignment | review digest + assignment revision + authenticated actor |
| `phase_gate_disposition_recorded` | Separately authorized human recorded a phase-gate decision | phase + exact gate evidence digest + authenticated actor |

No event alone grants execution permission. In particular, `approval_recorded` must be validated against the current policy at the operation boundary, and `human_disposition_recorded` is not phase-gate closure. The phase-gate event is a separate authority and must remain disabled while the controlling handoff prohibits closure.

## Event-specific payload rules

Each event type must have a closed payload schema. Unknown keys are rejected. Payloads contain facts needed to explain the transition, not caller-controlled state overrides.

- Approval payloads bind the exact operation, workflow file and immutable workflow SHA where applicable, repository, branch, task digest, handoff revision, input commit, scope digest, issue time, expiry, and revocation policy. Approval identity and actor identity come from the authenticated approval channel.
- Assignment payloads bind the canonical package digest, immutable package object reference, task digest, scope/prohibitions digest, handoff ID, and assignment revision.
- Dispatch payloads bind attempt ID, approval ID, workflow identity, and the exact assignment revision. They must not contain secrets or credentials.
- Delivery payloads distinguish confirmed, rejected, pending, and unknown outcomes. A timeout is not a confirmed failure and does not authorize retry.
- Return payloads bind the raw received bytes digest, authenticated transport identity, assignment revision, and receiver-generated return ID. Worker declarations remain untrusted.
- Review payloads bind the return digest, evidence-verification result digest, reviewer identity, and disposition eligibility. Structural eligibility is not research correctness.
- Human disposition payloads bind the exact review digest and assignment revision. Accepted task status remains distinct from phase-gate closure.

## Identity and idempotency

The trusted adapter derives a stable source namespace from authenticated provider/tenant, repository/workspace, and channel context. It obtains delivery identity from the authenticated upstream event or receiver. It must not trust a worker-supplied namespace, actor, delivery ID, or source reference.

Use a durable unique key on `(source_namespace, delivery_id, event_role)` where one upstream delivery can legitimately create multiple event roles. Derive `event_id` from a versioned unambiguous canonical encoding of that tuple. Also enforce unique `event_id` and unique registry sequence.

An exact replay returns the original committed receipt, even if the caller's checkpoint is stale. Reuse of an idempotency key with changed event facts is rejected. A new event requires the expected protected checkpoint/version to match. Concurrent first deliveries must resolve through the uniqueness constraint and re-read the winning record.

## Ordering and transaction boundary

One transaction must:

1. authenticate and derive source/delivery identity before entering the state transition;
2. load and verify the current registry snapshot and protected checkpoint;
3. resolve exact replay before rejecting a stale checkpoint;
4. verify approval validity and current handoff/policy at the protected operation boundary;
5. validate event-specific schema and current state-machine transition;
6. allocate the next registry sequence and event hash;
7. append the event;
8. update materialized assignment/approval/delivery/return/review state;
9. update idempotency indexes and protected checkpoint;
10. commit all changes atomically and return a receipt.

If the selected backend cannot provide this transaction, a separately specified transactional outbox/inbox protocol must prove equivalent atomicity and recovery. Independent writes to an event file, assignment record, and checkpoint are not sufficient.

## State-machine constraints

- An assignment revision is immutable after preparation. Changes create a new revision and package digest.
- Approval is single-purpose, exact-scope, time-bounded, revocable, and bound to the exact revision and workflow identity.
- Dispatch cannot begin without a currently valid authenticated approval and a fresh policy/handoff check.
- A delivery timeout or missing response enters pending/unknown; it never automatically returns to prepared or permits retry.
- Cancellation/revocation races are serialized against dispatch in the same trusted transaction boundary. If dispatch has already started, cancellation does not rewrite history; the system reconciles the actual delivery outcome.
- A worker return is accepted only against a registry-retained assignment revision and package digest.
- Review completion is not task acceptance. Human task disposition is not phase-gate closure.
- Phase-gate disposition remains a separate human-authorized operation and is prohibited by the current G0-05 handoff.

## Canonicalization and versioning

V2 must declare its canonicalization algorithm and version in the envelope or immutable registry metadata. Prefer RFC 8785 JSON Canonicalization Scheme with independently generated cross-language test vectors. Specify treatment of Unicode, numbers, timestamps, and unsupported values. Reject non-finite numbers, duplicate keys, non-string keys, and values outside the declared JSON data model.

Do not assume that Python `json.dumps(sort_keys=True)` is cross-language canonicalization. Do not change v1 hashing. A v2 canonicalization upgrade requires a new explicit version and a migration plan; historical v1 and earlier v2 hashes remain verifiable under their original contracts.

Required shared vectors include nested objects with reordered keys, Unicode edge cases, integer and fractional numbers, negative zero handling, empty payloads, timestamps with and without fractional seconds, duplicate-key rejection, and malformed/non-JSON values. At least two independent implementations should produce identical canonical bytes and digests before cross-runtime use.

## Legacy compatibility and migration

- Existing v1 records remain byte-for-byte and hash-for-hash unchanged.
- V1 records are not automatically promoted to authenticated v2 events.
- If historical v1 data is imported, record it as a legacy evidence reference with original digest, original schema version, import actor/source, and an explicit statement that its original authentication limits remain.
- Never fabricate missing approval, dispatch, delivery, or actor facts from v1 payloads.
- Mixed v1/v2 chains are prohibited unless a future migration specification defines an explicit bridge record and independent verification rules.
- The initial v2 registry may begin at a new genesis checkpoint while retaining a read-only reference to the v1 ledger head.

## Failure and recovery requirements

- Crash before commit: no partial event, state, index, or checkpoint update is visible.
- Crash after commit before response: exact retry returns the original receipt.
- Stale checkpoint: reject a new event without mutation; reload and reconcile.
- Conflicting duplicate delivery: preserve original event and raise a security/integrity error.
- Checkpoint rollback, chain break, invalid transition, or invalid approval: fail closed and require human investigation.
- Store uncertainty: do not claim success; reconcile by authenticated idempotency key before retrying.
- Backup restore must detect rollback against an independently retained checkpoint or external trust anchor; restoring a self-consistent old database is not sufficient.

## Required review and implementation gates

Before implementation, separately approve:

1. The event vocabulary, envelope, payload schemas, state machine, and legacy rules.
2. The canonicalization contract and cross-language test vectors.
3. Registry backend, authenticated identities, protected checkpoint, retention, backup, and restore design.
4. Threat model and failure-injection matrix covering concurrent writes, duplicate deliveries, lost responses, approval expiry/revocation, cancellation races, stale checkpoints, and backup rollback.
5. Exact implementation scope and a controlling handoff that permits code/tests/workflows.

Until those approvals and the controlling handoff change, this remains documentation only. No tests or scripts should be run under the current G0-05 restriction.

## Current limitations

- V1 event ledger remains unchanged and supports only its existing five event types.
- No v2 schema, registry, store, dispatcher, approval channel, or delivery receiver is implemented.
- No cross-language canonicalization vectors have been created or executed.
- No event has been persisted by a trusted adapter.
- No workflow, agent execution, dispatch, schedule, or unattended worker is active.
