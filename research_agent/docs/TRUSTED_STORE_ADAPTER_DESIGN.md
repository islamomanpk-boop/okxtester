# Trusted store adapter design (proposal only)

## Status

Design proposal only. No persistence backend is selected, implemented, configured, or activated. The current G0-05 handoff remains authoritative and prohibits running scripts, tests, and workflows. This document grants no execution, dispatch, scheduling, write, or research authority.

## Why an adapter is still missing

The event ledger and persistence contract are pure in-memory decision primitives. They validate event shape and hash-chain continuity, identify exact delivery replays, and detect stale expected-head checkpoints. They do not authenticate event sources, retain a protected head, or provide atomic compare-and-append. A process restart therefore has no trustworthy durable state unless a separately reviewed store and trust root are introduced.

## Required adapter boundary

A future adapter should expose a deliberately small interface:

- `load_snapshot()`: return the ledger plus an independently protected head checkpoint and checkpoint version.
- `append_if_current(expected_checkpoint, event)`: atomically verify the stored checkpoint, enforce unique upstream event identity, append the event, and advance the protected checkpoint in one transaction.
- `lookup_provider_delivery(source_namespace, delivery_id)`: resolve the complete authenticated upstream delivery aggregate, including all linked per-role event receipts.
- `lookup_event_receipt(source_namespace, delivery_id, event_role)`: resolve one event-role receipt for exact event-level replay.
- `verify_snapshot()`: verify event schemas, hash links, unique IDs, checkpoint-to-head equality, and checkpoint authenticity before any state is used.

These are interface requirements, not implemented functions. No current module should pretend this interface exists.

## Stable delivery identity and event IDs

The current pure ledger schema has one globally unique `event_id`; it does not have separate `source` and `delivery_id` columns. The future adapter must bridge that shape explicitly rather than treating the coarse `source` enum (`github_workflow`, `human_review`, or `worker_return`) as a globally unique namespace.

- Derive a stable, opaque source namespace from authenticated context. It should distinguish the relevant provider/tenant or installation, repository or workspace, and authenticated channel where applicable. Do not put credentials or unnecessary personal data in the namespace.
- Obtain `delivery_id` from the authenticated upstream delivery mechanism. Never accept a worker-supplied delivery ID or namespace as proof of origin.
- Treat `(source_namespace, delivery_id)` as the authenticated **provider-delivery identity**, unique in the delivery index. If that delivery creates one lifecycle event, use one fixed event role. If it creates multiple legitimate lifecycle events, identify each with `(source_namespace, delivery_id, event_role)`; the role is a closed, schema-defined value, not caller-arbitrary text.
- Derive each global `event_id` deterministically from the canonical, unambiguous event-level tuple `(source_namespace, delivery_id, event_role)`. Do not use naive delimiter concatenation, which can be ambiguous.
- Enforce uniqueness for the provider-delivery pair, the event-level tuple, and each derived `event_id`. Keep the provider-delivery row linked to its per-role event receipts so `lookup_provider_delivery(source_namespace, delivery_id)` resolves the complete delivery aggregate without trusting worker data; `lookup_event_receipt(source_namespace, delivery_id, event_role)` resolves one event-level idempotency record.
- Keep `source` as the ledger's allowlisted category. Populate `source_ref` with a stable, non-secret reference to the authenticated source event/resource; do not overload it as the delivery ID unless its semantics are explicitly fixed.
- For a retry, reproduce the same event facts, including the same canonical `occurred_at_utc`. Prefer an authenticated upstream occurrence timestamp. If the source has none, the adapter must durably retain the first accepted timestamp alongside the delivery identity and reuse it; generating a fresh processing timestamp on every retry would make an otherwise identical delivery appear to have changed facts.
- If one authenticated delivery legitimately produces multiple ledger events, derive a distinct deterministic event identity for each event role using an additional fixed role discriminator, and document that mapping. Never reuse one delivery identity for different event facts.

The existing `append_event()` and `prepare_append()` APIs remain unchanged and purely in-memory. They can enforce exact replay only after the adapter has supplied the same globally unique `event_id` and identical event facts.

## Canonicalization and hash interoperability

The current ledger implementation hashes Python `json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)` output. That gives a deterministic byte representation for this implementation, but it is not a declared cross-language standard such as RFC 8785/JCS. In particular, JSON number formatting and Unicode/key ordering can differ between runtimes even when parsed values are semantically equivalent.

Before a non-Python writer or verifier is introduced, the integration must either (a) adopt a versioned RFC 8785/JCS-compatible canonicalization contract and shared test vectors, or (b) explicitly constrain all ledger writes and verification to a pinned Python serializer/runtime. The current schema permits finite floating-point values, so the selected contract must specify number handling. Do not silently migrate existing event hashes; any canonicalization change requires an explicit versioned migration plan and verification of historical records.

## Required trust and transaction sequence

1. Authenticate the caller at the transport boundary. Derive source namespace, source identity, and delivery ID from a trusted GitHub/platform event or authenticated human-review channel; never accept worker-provided `source`, `source_ref`, namespace, or delivery identity as proof.
2. Resolve the event to the exact trusted queued task and current task-definition digest. Re-read the controlling handoff, phase gate, allowlist, and branch policy at the operation boundary.
3. Load the durable ledger, delivery index, and protected checkpoint from a store with access controls independent of the worker.
4. Verify the complete hash chain and confirm that the independently protected checkpoint matches the current ledger head (including the empty-ledger case).
5. Canonicalize and validate the event using the existing pure ledger primitives; derive its global `event_id` from the authenticated delivery identity as specified above.
6. In one database transaction or true compare-and-swap operation, first look up the authenticated `(source_namespace, delivery_id)` under the store's uniqueness/transaction guarantees. If it already exists, compare the complete canonical event facts: return the original receipt for an exact replay even when the caller's expected checkpoint is now stale; reject changed facts. This replay path must not append or advance the checkpoint.
7. Only when no delivery record exists, require the stored checkpoint/version to equal the snapshot loaded in step 3; reject stale new-event writers without changing ledger, delivery index, or checkpoint.
8. Enforce uniqueness for both the authenticated source namespace plus stable delivery ID and the derived global event ID. Handle concurrent first deliveries by allowing only one transaction to insert; a losing transaction must re-read the winning record and apply the exact-replay-versus-conflicting-facts rule, not append a second event.
9. Append the event, record its delivery-index entry, and advance the protected checkpoint atomically. A split write is not acceptable unless a separately specified recovery protocol can prove which side committed.
10. Return a receipt containing the committed event digest and checkpoint version. The receipt is evidence of storage only, not task completion or gate approval.

## Backend selection criteria

Do not choose a backend until the operational environment and trust boundary are approved. Evaluate candidates against:

- atomic transactions or compare-and-swap semantics;
- durable retention and backup/restore behavior;
- unique constraints for idempotency keys;
- authenticated writer identity and least-privilege access;
- separation between worker-controlled data and protected checkpoint state;
- auditability, retention, recovery, and administrative access;
- cost and operational burden for a free-first setup;
- ability to revalidate repository branch, task digest, handoff, phase gate, and allowlist before each protected operation.

A GitHub artifact alone is not an adequate mutable ledger or protected checkpoint: artifacts are immutable run outputs and do not provide a transactional append primitive. A repository file commit could provide history but is not automatically a safe compare-and-swap authority and must not be allowed to write to the protected research branch.

## Recovery and failure semantics

- Crash before transaction commit: no event, delivery-index entry, or checkpoint advancement is visible; retry using the same authenticated delivery ID.
- Crash after atomic commit but before response: retry resolves to the already-committed event and returns its receipt.
- Stale checkpoint: reload, verify, and reconcile; never silently rebase a human disposition or worker submission.
- Checkpoint mismatch or invalid chain: fail closed and require human investigation; do not rebuild or reset the trust root automatically.
- Restore: freeze all privileged transitions; compare registry identity, monotonic epoch, sequence, head digest, schema/canonicalization versions, and chain against the independent witness. Reject stale, ahead, forked, or mismatched snapshots; reconcile every outstanding provider delivery with its original identity; require independent human resume authorization tied to a signed recovery report. Never synthesize missing approval, revocation, dispatch, or disposition history.
- Duplicate delivery ID with changed facts: reject and preserve the original event.
- Store unavailable: retain no claimed success; report persistence as unknown only if commit outcome cannot be established, then reconcile by delivery ID before retrying.

## Authority separation

Persisting `human_disposition_recorded` records a human decision but does not itself establish who the human was; that identity must be authenticated by the trusted source adapter. An accepted task is not a closed phase gate. Gate closure, phase advancement, execution authorization, dispatch, and research conclusions remain separate human-authorized operations.

## Implementation gate

Before implementation, obtain explicit approval for a backend and its identity/access model. Then produce a threat model and failure-injection plan, implement the adapter on the isolated agent branch, and arrange independent review. Runtime tests and workflow validation must wait until the controlling research handoff permits them. Do not create secrets, change repository permissions, enable workflows, or touch the VPS as part of this design step.

## Current state

- Existing event ledger and optimistic-concurrency modules remain pure and non-persistent.
- No backend, credentials, protected checkpoint, transaction, or durable store is configured.
- No task execution, dispatch, scheduling, workflow run, research code/data change, gate closure, or phase advancement is authorized by this proposal.
