# Assignment recovery policy

## Purpose

`engine/recovery_policy.py` classifies an assignment's next safe handling step from three observations: delivery state, review state, and (when review is complete) human disposition. It is a deterministic decision table, not a dispatcher, scheduler, persistent state machine, or source-authentication mechanism.

## Recovery paths

| Delivery observation | Review observation | Human disposition | Classification / next step |
|---|---|---|---|
| Not dispatched | Not received | None | Hold for explicit dispatch authorization |
| Dispatch started | Not received | None | Reconcile delivery before any retry |
| Delivery uncertain | Not received | None | Manual reconciliation; never auto-retry |
| Delivery confirmed | Not received | None | Wait for submission or human timeout review |
| Delivery confirmed | Submission received | None | Assignment-bound supervisor review |
| Delivery confirmed | Review completed | None | Request human disposition |
| Delivery confirmed | Review completed | Accepted | Record task acceptance; keep phase gate separate |
| Delivery confirmed | Review completed | Rejected | Return to human for replanning |
| Delivery confirmed | Review completed | Needs revision | Request revision under human supervision |

Impossible combinations and unknown values fail closed.

## Trust and authority limits

- All three inputs are observations; this module does not authenticate their source. A future adapter must verify workflow run/delivery IDs, assignment-package digest, worker-return bytes, review result, and human actor/decision independently.
- A delivery timeout is not proof of non-delivery. The policy deliberately blocks automatic retry when dispatch is in progress or delivery is uncertain.
- A human acceptance is task-level only. It does not close G0-05 or any phase gate, advance phase order, or authorize a later task.
- Every output sets automatic dispatch/retry, task completion approval, phase-gate closure, and queue mutation to false.
- The module performs no I/O, dispatch, scheduling, queue mutation, event persistence, or authorization.

## Explicit scope boundary: advisory projection, not authoritative state

This classifier is deliberately a small projection over delivery, review, and human-disposition observations. It is not the complete assignment lifecycle state machine, and its output must never be persisted as the sole authoritative assignment status or used to authorize a protected operation.

In particular, the current input schema does not represent:
- assignment cancellation or provider-side cancellation;
- approval issuance, expiry, revocation, or single-use consumption;
- multiple dispatch attempts and their individual provider receipts;
- raw return receipt, malformed payload, duplicate/conflicting replay, or late-return eligibility;
- immutable assignment revision identity and package digest;
- review identity/policy version or human actor/disposition identity;
- phase-gate disposition.

A future trusted registry must keep these dimensions separate and derive current projections from immutable authenticated events. Cancellation is orthogonal to delivery: it blocks future attempts but does not erase a committed dispatch attempt. Approval validity is checked independently inside each protected transaction. A raw return receipt is not necessarily an eligible submission. A `needs_revision` disposition is not authorization to create or dispatch a new revision. Task acceptance never implies phase-gate closure.

Do not call this helper as the sole recovery authority when any omitted dimension may affect the decision. The trusted adapter must validate the full current registry state, approval, handoff/policy, attempt identity, return eligibility, and expected state versions before proposing or committing a transition. This helper remains advisory and non-authorizing.

## Validation

Eleven regression tests are authored in `tests/test_recovery_policy.py`; they have not been executed. Runtime validation remains prohibited while the active Phase 3 G0-05 handoff forbids relevant tests and workflows.
