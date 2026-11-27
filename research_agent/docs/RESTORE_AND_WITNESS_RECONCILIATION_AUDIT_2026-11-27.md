# Restore recovery and external-witness reconciliation audit — 2026-11-27

## Scope and authority

Targeted static review of the existing backup/anti-rollback audit, unified lifecycle restore protocol, trusted-store adapter, and backend interface after introduction of the database-commit plus external-witness-outbox protocol.

No tests, scripts, workflows, provider calls, dispatch, scheduling, VPS access, or research operations were performed. The Phase 3 G0-05 handoff remains authoritative.

## Executive result

The prior restore protocol correctly requires an isolated restore, authenticated independent checkpoint, exact chain/state verification, provider reconciliation, protection against missing approval revocation/consumption history, and separate human resume authorization.

A new ambiguity exists after the witness-outbox design: restore rules that simply reject every database head ahead of the external witness can misclassify a legitimate committed-but-not-yet-witnessed transaction as a fork. Conversely, treating any ahead database as a pending transaction would allow fabricated or incomplete history. Recovery must reconcile the exact durable outbox identity and predecessor before deciding.

## Findings

### RW-01 — distinguish a legitimate witness-pending commit from a fork (P0)

The database transaction is the lifecycle linearization point and atomically commits event/state/indexes/internal checkpoint plus the witness-outbox item. External witness advancement happens afterward. Therefore, a crash can leave the database exactly one committed checkpoint ahead of the witness.

Restore must:
1. Keep all protected writes and dispatch frozen.
2. Verify the restored database's full chain and internal checkpoint, and verify the external witness independently.
3. If the database head equals the witness head, verify exact tuple equality and continue to outstanding-delivery reconciliation.
4. If the database head is exactly one successor of the witness head and contains one matching durable outbox item whose registry/epoch/sequence/head digest/predecessor exactly extend the witness tuple, classify it as witness-pending—not as a fork. Publish/replay that exact tuple using the same witness idempotency identity, obtain the authenticated witness receipt, and durably record acknowledgment. No new lifecycle event or sequence is created.
5. If the database is ahead by more than one sequence, has no matching outbox, has a broken predecessor, or has any other unexplained discrepancy, fail closed and recover only from independently authenticated exact history. Do not infer legitimacy from local timestamps or a self-asserted pending flag.
6. If the witness is ahead of the restored database, recover every missing committed event/state transition from an independently authenticated append-only source with exact sequence/digest proof. A local outbox cannot replace missing event history.
7. Same-sequence different digest, wrong registry/epoch, schema/canonicalization mismatch, or an unprovable gap is an integrity incident. No automatic genesis/reset.

The conservative protocol should allow at most one unacknowledged witness-outbox checkpoint at a time, because protected writes are frozen while witness-pending. This makes the legitimate pending case bounded and unambiguous.

### RW-02 — witness reconciliation must precede approval or dispatch restoration (P0)

A restored approval row is never sufficient evidence of active approval. After checkpoint and outbox reconciliation, replay the authoritative event history to derive issuance, expiry under trusted time, revocation, single-use consumption, assignment revision, cancellation, and dispatch state. Missing or unverifiable revocation/consumption/nonce history means UNKNOWN and deny.

### RW-03 — restore must preserve provider and return uncertainty (P0)

Before resume, reconcile every committed dispatch attempt against the provider using its original identity/idempotency key, including accepted-but-unacknowledged, pending/unknown, rejected, and provider-cancelled outcomes. Do not issue a new delivery identity while any attempt is unresolved. Verify raw return receipt bytes/digests and their exact assignment/revision/attempt binding. Preserve late, malformed, duplicate-content, conflicting-replay, and unbound returns; do not convert them into review-eligible submissions merely because a backup restored.

### RW-04 — witness outage is a hold, not a bypass (P1)

If the witness is unavailable, signature/authentication fails, freshness cannot be established, or an outbox acknowledgment cannot be reconciled, remain in read-only recovery mode. A human cannot waive missing cryptographic history by choosing the newest local backup. Resume authorization must bind to the exact reconciled checkpoint and signed recovery report, and remains separate from workflow/dispatch authorization.

## Required document updates

The unified restore protocol, trusted-store recovery semantics, and backend interface now distinguish:
- database head equal to witness head;
- exactly one valid outbox-backed successor awaiting witness acknowledgment;
- witness ahead of database, requiring authenticated history recovery;
- unexplained multi-sequence lead, fork, wrong epoch/registry, or missing outbox, requiring fail-closed incident handling.

They also require one pending witness checkpoint maximum and complete approval, provider-delivery, and raw-return reconciliation before resume.

## Current state

No backend, witness, registry, backup system, recovery identity, or provider integration exists. No restore drill or failure-injection test has been run. No code/tests/workflows or research artifacts were changed or executed. Agent remains non-operational; G0-05 remains controlling.
