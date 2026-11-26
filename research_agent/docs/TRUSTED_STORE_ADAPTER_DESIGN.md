# Trusted store adapter design (proposal only)

## Status

Design proposal only. No persistence backend is selected, implemented, configured, or activated. The current G0-05 handoff remains authoritative and prohibits running scripts, tests, and workflows. This document grants no execution, dispatch, scheduling, write, or research authority.

## Why an adapter is still missing

The event ledger and persistence contract are pure in-memory decision primitives. They validate event shape and hash-chain continuity, identify exact delivery replays, and detect stale expected-head checkpoints. They do not authenticate event sources, retain a protected head, or provide atomic compare-and-append. A process restart therefore has no trustworthy durable state unless a separately reviewed store and trust root are introduced.

## Required adapter boundary

A future adapter should expose a deliberately small interface:

- `load_snapshot()`: return the ledger plus an independently protected head checkpoint and checkpoint version.
- `append_if_current(expected_checkpoint, event)`: atomically verify the stored checkpoint, enforce unique upstream event ID, append the event, and advance the protected checkpoint in one transaction.
- `lookup_delivery(source, delivery_id)`: resolve retries against the stable upstream delivery identity.
- `verify_snapshot()`: verify event schemas, hash links, unique IDs, checkpoint-to-head equality, and checkpoint authenticity before any state is used.

These are interface requirements, not implemented functions. No current module should pretend this interface exists.

## Required trust and transaction sequence

1. Authenticate the caller at the transport boundary. Derive source identity and delivery ID from a trusted GitHub/platform event or authenticated human-review channel; never accept worker-provided `source`, `source_ref`, or delivery identity as proof.
2. Resolve the event to the exact trusted queued task and current task-definition digest. Re-read the controlling handoff, phase gate, allowlist, and branch policy at the operation boundary.
3. Load the durable ledger and protected checkpoint from a store with access controls independent of the worker.
4. Verify the complete hash chain and confirm that the independently protected checkpoint matches the current ledger head (including the empty-ledger case).
5. Canonicalize and validate the event using the existing pure ledger primitives.
6. In one database transaction or true compare-and-swap operation, require the stored checkpoint/version to equal the snapshot loaded in step 3; reject stale writers without changing either ledger or checkpoint.
7. Enforce a unique constraint on the authenticated source plus stable delivery ID. An exact replay returns the original event; reuse with different facts is rejected.
8. Append the event and advance the protected checkpoint atomically. A split write is not acceptable unless a separately specified recovery protocol can prove which side committed.
9. Return a receipt containing the committed event digest and checkpoint version. The receipt is evidence of storage only, not task completion or gate approval.

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

- Crash before transaction commit: no event or checkpoint advancement is visible; retry using the same authenticated delivery ID.
- Crash after atomic commit but before response: retry resolves to the already-committed event and returns its receipt.
- Stale checkpoint: reload, verify, and reconcile; never silently rebase a human disposition or worker submission.
- Checkpoint mismatch or invalid chain: fail closed and require human investigation; do not rebuild or reset the trust root automatically.
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
