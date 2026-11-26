# Trusted persistence contract

## Purpose

`engine/persistence_contract.py` defines a pure optimistic-concurrency decision for the append-only event ledger. It prepares an append only when the caller's independently trusted expected head matches the validated current ledger head.

## Outcomes

- `append_prepared`: new event validated and prepared against the current head.
- `stale_checkpoint`: a new event was proposed against an outdated head; the returned ledger is unchanged and the caller must reload and reconcile.
- `idempotent_replay`: the same stable upstream event ID and identical event facts already exist; no second event is added.
- Reusing an event ID with different facts, malformed checkpoints, or an invalid existing ledger raises a validation error.

## Critical limitation

This is **not** a persistence adapter and does not provide atomic compare-and-swap. It performs no file/database/GitHub I/O, locking, source authentication, dispatch, queue mutation, task-state change, or authorization. Two callers can both prepare against the same head; only an atomic trusted store can ensure that one wins.

A future adapter must:

1. Authenticate the event source and delivery identity independently; never trust worker-supplied source claims alone.
2. Load the ledger and its latest head checkpoint from trusted storage.
3. Verify the ledger chain and compare its head with an independently protected checkpoint.
4. Atomically append only if the stored head still equals the expected head (transaction or compare-and-swap).
5. Persist the new event and protected head checkpoint atomically, or use a recovery protocol that cannot accept a split update.
6. Enforce unique stable event IDs and make delivery retries idempotent.
7. Re-check the current handoff, task digest, phase gate, and allowlist at the actual operation boundary.
8. Keep human-only completion and gate-closure authority.

A hash chain alone is not source authentication or tamper-proof storage. An attacker able to replace the whole ledger can rebuild the chain from genesis unless a trusted head/checkpoint is retained separately.

## Validation status

Eight regression tests have been authored for matching/stale checkpoints, idempotent replay, event-ID reuse, malformed checkpoint data, and corrupt ledgers. They have **not** been executed. The active Phase 3 G0-05 handoff still prohibits running the relevant tests and workflows.
