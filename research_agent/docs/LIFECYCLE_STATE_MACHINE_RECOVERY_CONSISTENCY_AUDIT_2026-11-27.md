# Lifecycle state-machine and recovery-policy consistency audit — 2026-11-27

## Status and authority

Targeted static comparison of `engine/recovery_policy.py`, its documentation, and the unified lifecycle/registry contracts. No tests, scripts, workflows, dispatch, scheduling, VPS access, or research operations were run. This documentation-only review grants no execution authority. The Phase 3 G0-05 handoff remains controlling.

## Executive result

The recovery classifier is conservative for the small set of delivery/review/disposition combinations it accepts. It rejects impossible combinations and never authorizes dispatch, retry, task completion, queue mutation, or phase-gate closure. However, it is not a complete lifecycle state machine and should not be used as the authoritative assignment state.

The future registry contracts model more dimensions than the helper: cancellation, approval revocation/consumption/expiry, delivery attempts and provider receipts, raw return eligibility, assignment revisions, review identity, task disposition, and separate phase-gate disposition. The helper compresses these into three inputs and cannot distinguish several security-relevant situations. This is an intentional boundary, but the design must explicitly prevent consumers from mistaking its output for a full lifecycle state.

## Findings

### SM-01 — Cancellation is absent from recovery inputs (P0)

The classifier has no cancellation observation. Therefore it cannot distinguish an ordinary delivered assignment awaiting return from one cancelled after delivery, nor classify a late return after cancellation. It must not be called as the sole recovery decision when cancellation may exist.

Required model: cancellation is an orthogonal, monotonic assignment/attempt fact. It does not overwrite delivery state. Future recovery input must include authenticated cancellation state and effective registry sequence, then route late returns to preserved-but-ineligible handling. A cancellation before dispatch-start denies dispatch; after dispatch-start it blocks future attempts but does not assert non-delivery or erase the committed attempt.

### SM-02 — Revocation, expiry, and approval consumption are absent (P0)

The classifier does not accept approval identity/status, expiry, revocation, or consumption. Its output cannot determine whether a new protected operation remains authorized. Recovery status must never be used as an approval check. Every protected operation must independently revalidate current approval and policy inside its atomic transaction.

### SM-03 — Delivery state collapses multiple distinct facts (P1)

`dispatch_started` maps to pending/unknown, while `delivery_uncertain` is separately represented. The classifier does not model provider acceptance/rejection receipts, provider-side cancellation, multiple attempts, or whether an uncertainty has since been reconciled. A later authenticated receipt should be a new ordered event that resolves the same attempt; it must not create a new attempt or erase the earlier uncertainty observation.

The registry should preserve immutable attempt and receipt history and derive current delivery state from the ordered authenticated events. Do not treat a mutable state label as the sole source of truth.

### SM-04 — Return eligibility is not represented by the review-state enum (P0)

The helper accepts only `not_received`, `submission_received`, and `review_completed`. It cannot represent malformed, duplicate-content, changed-replay conflict, unknown delivery binding, assignment/package mismatch, late-after-cancel, after-expiry, or after-revocation returns.

These are receipt/eligibility dimensions, not synonyms for “not received.” A raw receipt may exist while no eligible submission exists. Preserve raw arrival and derived eligibility separately; only eligible returns may enter normal supervisor review. Ineligible/forensic inspection must never become task completion evidence.

### SM-05 — Revision requests are not modeled as new assignment revisions (P1)

`needs_revision` maps to `revision_requested`, but the helper does not create or identify a new immutable assignment revision, fresh approval, new package digest, or link to the prior revision. A revision request is only a human disposition; it does not authorize a replacement package or dispatch. Any new revision must be separately prepared and approved under current policy.

### SM-06 — Human disposition lacks exact review binding and supersession semantics in the helper (P1)

The helper receives a disposition string, not an authenticated actor, disposition ID, review digest, assignment revision, or idempotency key. It can classify only. The registry must persist a human-authenticated disposition bound to one exact review digest and revision. Duplicate exact decisions return the original receipt; conflicting decisions require explicit, separately authenticated supersession rules. A second worker return or repeated review must not create another acceptance path.

### SM-07 — No explicit transition graph for orthogonal lifecycle dimensions (P1)

The documents describe command preconditions but need a single clear state model separating:
- immutable assignment revision;
- approval lifecycle (issued, consumed, revoked, expired/invalid);
- dispatch-attempt lifecycle (prepared, started, provider pending/unknown, confirmed/rejected, provider-cancelled where supported);
- assignment cancellation flag;
- return receipts and eligibility;
- review lifecycle;
- human task disposition; and
- phase-gate disposition.

These dimensions must not be collapsed into one enum. Each command validates its own prior state plus cross-dimension invariants in one atomic transaction.

## Recommended authoritative model

Use immutable event history plus derived projections. Keep the following dimensions separate:

1. **Assignment/revision:** prepared immutable revision; a change creates a linked new revision.
2. **Approval:** immutable issuance, consumption and monotonic revocation events; expiry derived using trusted service time. No recovery classifier grants approval.
3. **Dispatch attempt:** each attempt has its own immutable identity and provider idempotency key. Uncertain outcomes reconcile the same attempt; no automatic retry.
4. **Cancellation:** separate monotonic assignment/attempt flag/event. It blocks future work but does not rewrite attempt history.
5. **Return receipt:** raw bytes, authenticated transport identity, receiver digest and receipt status. Receipt existence is distinct from review eligibility.
6. **Review:** immutable and bound to one eligible return, exact package/revision, trusted evidence context and reviewer-policy version.
7. **Task disposition:** authenticated human decision bound to one exact review/revision. Revision request does not itself create or dispatch a new revision.
8. **Phase gate:** separate human authority and evidence; never inferred from task acceptance.

For every transition, validate global checkpoint and assignment state version, replay identity before stale-version rejection, current handoff/policy, exact approval where required, and the allowed prior state. Commit event, immutable records, idempotency index, materialized projections, state version, and checkpoint atomically.

## Required handling of key edge cases

| Situation | Required outcome |
|---|---|
| Cancel before dispatch-start commit | Deny; no provider call |
| Cancel after dispatch-start commit | Preserve attempt; reconcile same provider identity; block future attempts |
| Revocation after dispatch-start | Preserve committed attempt; block future approval use |
| Delivery uncertain then provider confirms same attempt | Append authenticated confirmation; resolve same attempt |
| Return arrives after cancellation/expiry/revocation | Preserve raw receipt; classify ineligible for normal completion |
| Malformed return bytes | Preserve/hash raw bytes; parse error; no review |
| Exact duplicate return delivery | Return original receipt; no second review path |
| Same return identity, changed facts | Quarantine conflict; preserve original |
| Duplicate review request | Return original review receipt |
| Needs-revision disposition | Record human request only; new revision requires separate preparation/approval |
| Duplicate human acceptance | Exact replay returns original disposition; conflicting decision requires explicit supersession |
| Task accepted | Task disposition only; phase gate remains separate |

## Scope and limitations

This was a targeted static consistency review, not an exhaustive formal verification or runtime state-machine test. The recovery helper remains useful as a small conservative advisory classifier, but its output is not a durable state transition, full lifecycle state, authorization decision, or proof that inputs are authentic.

No code or tests were changed or executed. The agent remains non-operational; no backend, receiver, registry, dispatcher, or workflow is active. G0-05 remains authoritative.


## Follow-up — registry/recovery/legacy-ledger boundary reconciliation

A further static cross-check of `engine/recovery_policy.py`, `engine/event_ledger.py`, `docs/TRUSTED_ASSIGNMENT_REGISTRY_DESIGN.md`, `docs/TRUSTED_DISPATCHER_CONTRACT.md`, and `docs/UNIFIED_TRUSTED_LIFECYCLE_TRANSACTION_SPEC.md` found the following boundary is consistent in the current proposals:

- The v1 event ledger is explicitly a legacy, non-authoritative hash-chain primitive. Its five event types and three source categories do not model the complete lifecycle and do not authenticate sources.
- The v2 registry proposal is the sole future authoritative lifecycle service. It introduces immutable assignment revisions, approval issuance/consumption/revocation, per-attempt provider observations, raw return receipts/eligibility, reviews, human dispositions, global sequence and assignment state versions.
- The recovery classifier remains an advisory projection over delivery, review and human-disposition observations. It must not be promoted to a persisted authoritative state or used to authorize an operation.
- Cancellation remains orthogonal to delivery; approval expiry/revocation/consumption remains independently checked at every protected operation; late or ineligible returns remain preserved but excluded from normal completion.

No contradictory instruction was identified in these reviewed documents. This is a targeted consistency result, not proof that a future registry implementation satisfies the contracts. A future migration must not import v1 hash-chain validity as proof of v2 event authenticity, sequence, state-transition legality, or approval status. Existing v1 records remain unchanged and must not be silently promoted or re-hashed.

No source code or tests were changed or executed. The active G0-05 handoff remains controlling.
