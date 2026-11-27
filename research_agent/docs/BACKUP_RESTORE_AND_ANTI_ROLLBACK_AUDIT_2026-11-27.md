# Backup restore and anti-rollback recovery audit — 2026-11-27

## Scope and method

Targeted static comparison of the trusted assignment registry, trusted store adapter, unified lifecycle transaction specification, recovery policy, threat model, and synthetic backend proof-of-capability plan.

No code, tests, scripts, workflows, provider calls, or research operations were executed. Documentation changes are confined to the isolated agent branch. The controlling Phase 3 G0-05 handoff remains authoritative.

## Finding B-01 — backup integrity checks lacked an end-to-end restore acceptance protocol

The documents correctly required an independent checkpoint and stated that a backup behind that checkpoint must be rejected. They did not consolidate the complete recovery sequence or explicitly distinguish:
- a stale backup with a valid internal event chain;
- a backup ahead of the witness;
- a same-sequence divergent/forked head;
- registry identity or schema/canonicalization mismatch;
- missing revocation or single-use approval-consumption events;
- committed-but-unacknowledged and provider-uncertain dispatches.

A local database consistency check or backup timestamp cannot establish current authoritative state.

**Resolution recorded in the unified lifecycle, store adapter, and assignment registry designs:**

1. Freeze all privileged state transitions and dispatch while restoring.
2. Authenticate restore provenance and the independent witness.
3. Compare registry identity, monotonic epoch, global sequence, head digest, schema/canonicalization versions, and full chain/state integrity.
4. Reject lower/stale, higher/ahead, same-sequence divergent, or incompatible snapshots. Never choose by local timestamp.
5. Recover missing committed history only from an independently authenticated append-only source proving exact sequence/digests. Never recreate approvals, revocations, consumed approvals, dispatches, receipts, returns, or dispositions from worker data or unauthenticated logs.
6. Reconcile all nonterminal provider attempts using their original delivery identities; no new delivery identity or retry while unresolved.
7. Treat missing revocation/consumption history as a blocker, never as evidence that an approval remains active.
8. Produce a signed restore report and require independent human review plus a separate resume authorization bound to the exact recovered checkpoint.

## Cross-check of existing pure recovery behavior

The current `recovery_policy.py` classifies uncertain delivery conservatively and never authorizes automatic retry. The in-memory persistence primitive does not implement backup, witness, durable state, or anti-rollback. Those boundaries remain accurate and unchanged.

## Remaining blockers

- No backend, external checkpoint witness, authenticated recovery log, backup system, or restore operator identity exists.
- No restore drill, crash test, stale-backup test, fork test, or provider reconciliation test has been run.
- Witness freshness, key rotation, witness unavailability, and disaster-recovery RPO/RTO remain owner/backend decisions.
- Runtime validation remains blocked by the active handoff.
- The agent remains non-operational.

## Disposition

Documentation-level restore protocol clarified. No implementation, backend selection, operational authorization, dispatch authorization, or research handoff change.


## Addendum — external witness outbox reconciliation

Following the separate database-commit/external-witness protocol, restore must not classify every database head ahead of the witness as a fork. A head exactly one sequence ahead is witness-pending only if one durable outbox item exactly extends the authenticated witness tuple; replay that exact checkpoint identity and record the authenticated witness receipt without creating another event. At most one unacknowledged checkpoint is permitted while protected writes are frozen. If the witness is ahead, recover exact missing history from an independently authenticated append-only source. Any unexplained lead, missing/mismatched outbox, broken predecessor, same-sequence fork, or registry/epoch/schema mismatch remains fail-closed. See `RESTORE_AND_WITNESS_RECONCILIATION_AUDIT_2026-11-27.md` for the focused review.
