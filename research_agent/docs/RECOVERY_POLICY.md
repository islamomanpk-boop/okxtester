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

## Validation

Eleven regression tests are authored in `tests/test_recovery_policy.py`; they have not been executed. Runtime validation remains prohibited while the active Phase 3 G0-05 handoff forbids relevant tests and workflows.
