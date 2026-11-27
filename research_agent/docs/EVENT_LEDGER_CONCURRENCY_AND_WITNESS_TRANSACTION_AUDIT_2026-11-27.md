# Event-ledger, concurrency, and transaction-boundary audit — 2026-11-27

## Status and authority

Targeted static review of the event ledger, optimistic-concurrency helper, trusted-store adapter, event-v2 proposal, and unified lifecycle transaction specification. No tests, scripts, workflows, dispatch, scheduling, VPS access, or research operations were run. The G0-05 handoff remains controlling.

## Executive result

The pure v1 ledger primitives are appropriately non-authorizing. They validate strict JSON-compatible values, event shape, unique event IDs, canonical UTC timestamps, and the full previous-hash chain. Exact event-ID replay returns the original facts; changed facts under the same ID are rejected. The optimistic-concurrency helper correctly distinguishes exact replay from a stale new append and returns an isolated unchanged snapshot on conflict.

The future adapter documentation is strong about source identity, replay-before-stale-checkpoint, unique constraints, concurrent first-delivery races, and atomic registry updates. The major unresolved architecture point is the relationship between an atomic database transaction and an independently administered checkpoint witness. If the witness is truly external, it cannot normally be advanced in the same database transaction. The documents currently use wording that can be read as requiring both, without defining the commit/acknowledgment protocol for the gap between them.

## Findings

### TX-01 — External witness and database commit need a two-layer protocol (P0)

The unified specification requires one atomic transaction for records, event log, indexes, materialized state, assignment version, and checkpoint. The trusted-store design also requires the head checkpoint to be independently protected. If "independent" means a separate service/account/security domain, the external witness cannot generally participate in the database's ACID transaction.

Required clarification:
1. The registry database stores an internal head/checkpoint and a durable witness-outbox row in the same atomic transaction as event, state, and idempotency indexes. This database commit is the lifecycle transition's linearization point.
2. A separate witness publisher sends the committed registry ID, monotonic epoch, sequence, event-head digest, schema/canonicalization versions, and previous witness digest to the independently administered witness.
3. The witness enforces monotonic compare-and-advance and exact replay. Same tuple returns the original witness receipt; lower sequence, same-sequence different digest, wrong registry/epoch, or broken predecessor is rejected.
4. Until the witness confirms the committed head, the registry is in a durable witness-pending/degraded state. No new protected transition, approval consumption, dispatch, return acceptance, human disposition, or restore-resume operation may proceed. Read-only inspection and exact reconciliation may continue.
5. After witness acknowledgment, persist the witness receipt/acknowledged version in a separate registry transaction. If that acknowledgment write fails, retry by the same witness idempotency identity; do not republish a different checkpoint or roll back the already committed lifecycle event.
6. On crash/restart, reconcile every committed outbox item against the witness before enabling protected writes. If witness is unavailable or ahead/divergent, fail closed and invoke the restore/incident protocol.

An outbox row is not proof the witness advanced. A database commit receipt and an external witness receipt are distinct evidence objects. Do not claim cross-system atomicity.

### TX-02 — Global serialization and assignment concurrency must share one transaction (P0)

The design correctly requires both a global registry checkpoint/version and per-assignment state version. It should explicitly require the selected backend's isolation/locking/CAS behavior to prevent write skew and sequence allocation races. A unique sequence constraint alone detects a collision but does not ensure the loser safely re-reads and revalidates every precondition.

Required transaction rule: serialize the global-head advance and the target assignment-version compare/update in one transaction; allocate sequence from the locked/compared current head; use unique constraints for sequence, event ID, provider-delivery identity, event-role identity, approval/nonce, return ID, and other stable identifiers. On serialization failure/deadlock/unique race, abort the whole transaction, reload one consistent snapshot, resolve exact replay first, and revalidate all policy, approval, assignment, and state-transition conditions. Never retry only the final insert or reuse stale approval/state observations.

### TX-03 — Witness outage and uncertain commit outcomes need distinct recovery states (P0)

The store design says a timeout with unknown commit outcome must reconcile by delivery ID. The external witness introduces another uncertainty: the database commit may have succeeded while witness publication or acknowledgment is unknown. Distinguish at least:
- database transaction definitely not committed;
- database commit confirmed, witness pending;
- witness accepted, acknowledgment receipt not yet recorded locally;
- fully witnessed/acknowledged;
- conflicting or unverifiable witness state.

Only the final fully witnessed state may unlock the next protected write under the conservative policy. Exact retries use the original database idempotency key and witness idempotency key. Never create a second event or sequence because a response was lost.

### TX-04 — Current in-memory primitives are intentionally not the transaction (P1)

The v1 append and prepare helpers do not authenticate source identity, persist state, lock a head, enforce database uniqueness, allocate a registry-wide sequence, or update assignment projections. This is documented correctly; the functions must remain described as pure decision primitives and must not be wired into an unattended worker as if they provide CAS.

### TX-05 — Canonicalization is versioned only for future v2 (P1)

The v1 Python JSON serializer is deterministic for its implementation but is not a cross-runtime standard. The adapter and event-v2 proposal correctly require either a pinned Python serializer/runtime or a versioned JCS-compatible contract with shared test vectors before multiple runtimes participate. Preserve v1 hashes unchanged; never silently re-hash existing events.

### TX-06 — Input/resource bounds belong at the trusted adapter boundary (P1)

The pure v1 helper accepts arbitrary-size strings, payloads, and nested JSON-compatible structures and does not enforce transport byte limits or adapter resource budgets. This is acceptable for a pure in-memory primitive, but the future adapter must impose bounded raw/event sizes, nesting/depth, collection counts, string lengths, transaction duration, retry count, and replay lookup limits before parsing or hashing. Parser failures and resource-limit rejections must preserve authenticated raw evidence where applicable and must not partially commit lifecycle state.

## Existing controls that passed static review

- Full v1 hash-chain verification and unique event-ID validation.
- Exact replay with same event ID/facts; conflicting reuse rejected.
- Canonical UTC timestamp validation, including shortest fractional-second representation.
- Strict JSON-compatible value validation and rejection of non-finite numbers/non-string object keys.
- Stale checkpoint rejection for new events; exact replay resolved before stale-head conflict.
- Conflict returns an independent unchanged ledger snapshot.
- Future adapter contract specifies authenticated source namespace, stable delivery ID, closed event-role identity, complete-facts replay comparison, unique constraints, concurrent first-delivery winner re-read, and atomic event/index/checkpoint commit.
- V2 design specifies one global sequence and atomic updates to event log, materialized state, idempotency indexes, and checkpoint.

## Required document updates

The trusted-store adapter, unified lifecycle specification, and backend interface now distinguish the internal transactional checkpoint from the external witness acknowledgment, define the durable outbox/reconciliation state machine, and require full transaction revalidation after concurrency conflicts. The event ledger and persistence helper remain unchanged.

## Stop conditions and current status

No backend, witness service, registry, adapter, database, or credentials are selected or active. No code or tests were changed or executed. No workflow, dispatch, schedule, VPS, research branch, or protected data was touched. The agent remains non-operational; G0-05 remains authoritative.


## Follow-up static finding — hash-chain validity is not lifecycle-semantic validity

The current `engine/event_ledger.py` validator checks each event's closed field set, supported event/source labels, strict JSON-compatible payload shape, canonical UTC timestamp syntax, unique event IDs, previous-event hash linkage, and recomputed event digest. It does not enforce cross-event lifecycle semantics. In particular:

- It does not require `occurred_at_utc` values to be nondecreasing along ledger order. The hash chain proves sequence integrity as serialized, not chronological ordering of event occurrence claims.
- It does not require all events for one `task_id` to carry the same `task_definition_sha256`, nor does it model an explicit assignment-revision identity that would distinguish legitimate revisions from accidental digest changes.
- It does not enforce event-type transition rules, source/event-type compatibility, or event-specific payload schemas. The payload is only required to be a strict JSON object.
- It does not derive or validate a materialized assignment lifecycle projection. The separate recovery classifier is advisory and has a deliberately smaller state model.

These are not hash-chain failures and do not invalidate the ledger's stated role as an append-only integrity primitive. They do mean that `validate_event_ledger(...).valid == True` must not be interpreted as proof that the event history is chronologically or semantically valid. A future trusted lifecycle validator should validate authenticated source receipts, explicit assignment/revision identity, event-type-specific payload schemas, allowed state transitions, monotonic registry sequence, and the relevant time-order semantics against one consistent registry snapshot. Where out-of-order provider observations are legitimate, preserve provider occurrence time separately from trusted receipt/registry sequence rather than imposing a simplistic timestamp sort.

This is a static source observation; no malformed ledger was constructed or test executed. No code was changed. The pure ledger remains non-authorizing and has no persistence or source authentication.
