# Provider callback ingestion, replay, and ordering audit — 2026-11-27

## Scope and method

Targeted static protocol review of the provider idempotency/receipt contract, provider crash-recovery audit, unified lifecycle transaction specification, trusted dispatcher contract, backend interface, and restore/witness requirements.

Documentation-only. No provider, account, credentials, code, tests, scripts, workflow, network request, callback endpoint, dispatch, scheduling, VPS access, or research operation was used.

## Executive result

The existing design requires authenticated provider observations, immutable raw evidence, observation-specific replay identities, atomic persistence with lifecycle projection/checkpoint/outbox, and conservative handling of stale or uncertain status. It did not yet provide one sufficiently explicit callback-receiver protocol covering signature verification, delivery acknowledgment, duplicate/conflicting event IDs, out-of-order events, event gaps, key rotation, and callbacks after cancellation or terminal state.

The callback receiver must be an evidence-ingestion boundary, not a direct state-mutating webhook handler. Arrival order is not provider event order. A successful HTTP response is not proof that callback contents are authentic or that status was applied.

## Findings and required resolutions

### CB-01 — Authenticate exact raw callback bytes before interpreting payload (P0)

Capture exact body bytes and signature metadata; compute receiver digest and length before parsing. Verify the provider signature/MAC over the exact provider-defined byte sequence, bound to provider namespace, account, endpoint, key ID/version, algorithm, timestamp/nonce, and provider qualification version. Never reconstruct signed bytes from parsed JSON. Enforce documented timestamp tolerance and replay rules using trusted receiver time. Unknown, expired, malformed, revoked, or unverifiable keys fail closed. Preserve key-rotation overlap and verification-key identity. Strictly parse only after authentication; reject invalid UTF-8, duplicate JSON keys, non-finite numbers, schema drift, excessive nesting, and oversized payloads. Raw evidence and normalized payload remain separate immutable records.

### CB-02 — Durable receipt must precede successful acknowledgment (P0)

Allocate a receiver-owned receipt ID and derive provider delivery identity from authenticated provider namespace/account, provider event ID, and closed event role. Atomically persist raw bytes/digest/length, relevant headers, authentication provenance, immutable facts digest, initial received-unprocessed disposition, and durable processing-outbox record. Only after commit may the receiver return the provider-prescribed success acknowledgment. If commit outcome is unknown, resolve by exact identity and facts digest first. Exact replay returns the original receipt; changed facts under the same identity is a security conflict. HTTP 2xx means only durable receipt for processing, not semantic acceptance or status application.

### CB-03 — Duplicate delivery and conflicting event-ID reuse (P0)

Enforce uniqueness on provider namespace, account scope, provider event ID, and event role. The immutable facts digest covers attempt binding, assignment revision, package/request digest, provider key/scope, event identity, raw digest/length, signature provenance, status/version, and timestamps. Exact same identity and facts returns the original receipt without another lifecycle event. Same identity with changed bytes, signature context, attempt binding, or status is quarantined; never overwrite. Different event IDs with identical bytes remain distinct observations linked by content digest. If the provider lacks stable event IDs, use a documented receiver identity bound to authenticated delivery metadata and raw digest; body-hash deduplication alone is not event identity.

### CB-04 — Arrival order is not provider event order (P0)

Prefer provider-monotonic event sequence, cursor, or resource revision scoped to the provider job. Store provider event time and receiver observation time separately; neither alone establishes total order unless provider semantics guarantee it. Retain every authenticated observation. Older sequence/version is stale evidence and cannot regress projection. Same sequence/version with conflicting facts freezes that job projection pending reconciliation. Sequence gaps trigger authenticated history/query reconciliation. Without monotonic ordering, do not infer order from callback arrival time; query authoritative current status and retain the callback as evidence. Terminal states cannot be overwritten by later nonterminal observations. Contradictory later terminal evidence is retained and escalated, not resolved by last-write-wins.

### CB-05 — Bind every callback to exactly one committed dispatch attempt (P0)

Bind provider job ID and idempotency key to the exact immutable dispatch attempt, request-envelope digest, package digest, assignment revision, provider account/endpoint scope, and qualification version. Unknown, ambiguous, cross-account, mismatched-key, mismatched-digest, or multiply-bound callbacks are retained as quarantined evidence and cannot mutate assignments. Callbacks arriving before the local attempt is known are held for reconciliation, not heuristically attached. Late callbacks after cancellation, approval revocation, expiry, or local terminal disposition remain immutable observations with explicit late/ineligible classification; they cannot silently reopen or complete an assignment.

### CB-06 — Callback processing needs its own atomicity and recovery boundary (P0)

Use a durable processing outbox with explicit received-unprocessed, verified-pending-reconciliation, applied, quarantined, and processing-unknown dispositions. Verification and attempt binding precede trusted projection. In one registry transaction, append immutable observation/event, update provider-event idempotency index, derive permitted delivery projection, advance assignment/global versions, internal checkpoint, and witness outbox. Unknown transaction outcome is resolved by the same event identity and facts digest before retry. Exact replay returns original receipt; changed facts conflict. External witness acknowledgment remains a separate stage; protected writes stay frozen while witness-pending. Restart reprocesses durable receipts by identity and re-verifies retained raw bytes; it never synthesizes a missing callback or status.

### CB-07 — Key rotation, revocation, and verifier compromise (P1)

Retain immutable key-version metadata and effective validity intervals from an authenticated provider key-distribution source. Record the key version and verifier/policy version used for every callback. Unknown key, invalid signature, revoked key, or ambiguous validity interval fails closed. Key compromise triggers independent deny-only emergency hold and credential containment; it does not rewrite historical raw evidence. Re-evaluation occurs only through a controlled incident process. Provider signing-key rotation and local receiver-key rotation are distinct facts.

## Normative callback receiver sequence

1. Enforce endpoint, transport, size, header, and content-type limits.
2. Capture exact raw bytes and signature metadata; compute receiver digest/length.
3. Authenticate provider namespace/account and verify signature against exact provider-defined bytes and known key version.
4. Strictly parse and validate schema; preserve raw bytes independently.
5. Derive stable provider event identity and complete immutable facts digest.
6. Atomically persist raw receipt, identity/index, authentication provenance, received-unprocessed disposition, and processing outbox.
7. Acknowledge transport only after durable receipt commit; acknowledgment does not mean status application.
8. Process outbox item: bind to exactly one committed attempt; check replay/conflict, provider sequence/gaps, cancellation, revocation, and terminal context.
9. Quarantine mismatch, stale/conflicting order, missing sequence, unknown binding, or unverifiable status; query provider history where supported.
10. For an applicable observation, atomically append lifecycle evidence and update derived projection/checkpoint/witness outbox.
11. Await exact external witness acknowledgment before using the new projection for protected decisions.
12. On crash/replay, resolve the same receipt/event identity and facts digest; never create a new provider job or duplicate lifecycle transition.

## Required synthetic callback conformance cases

Test duplicate callback delivery; same event ID with changed body/signature/account/attempt; invalid signature, unknown/expired/revoked key, timestamp and nonce replay; invalid UTF-8, duplicate JSON keys, non-finite values, oversized/nested payloads and schema drift; all out-of-order accepted/running/completed permutations; same sequence with conflicting status; missing sequence/cursor; stale callback after terminal state; unknown job, wrong account/key/request digest, ambiguous attempt; callback before local dispatch visibility and after cancellation/revocation/expiry/terminal disposition; crashes before and after raw receipt commit, acknowledgment, processing, projection transaction, and witness acknowledgment; receiver outage and lost acknowledgment; key compromise during ingestion.

Oracles must prove raw evidence is never lost after acknowledgment, exact replay never duplicates a transition, conflicting replay never overwrites, stale events never regress state, gaps are not skipped, unknown binding never mutates an assignment, and witness-pending state never authorizes protected writes. Synthetic identities/data only; never contact a real provider, worker, or research task.

## Current status

Protocol clarification only. No provider, account, endpoint, callback receiver, signing key, registry, witness, or backend is selected or implemented. No tests, scripts, workflows, network requests, provider calls, dispatch, scheduling, VPS access, or research operations were run. The agent remains non-operational and Phase 3 G0-05 remains controlling.
