# Dispatch cancellation and revocation race audit — 2026-11-27

## Scope and method

Targeted static comparison of:
- `engine/recovery_policy.py`
- `docs/TRUSTED_DISPATCHER_CONTRACT.md`
- `docs/UNIFIED_TRUSTED_LIFECYCLE_TRANSACTION_SPEC.md`
- `docs/TRUSTED_REGISTRY_BACKEND_INTERFACE_SPEC.md`
- `docs/TRUSTED_ASSIGNMENT_REGISTRY_DESIGN.md`
- `docs/TRUSTED_STORE_ADAPTER_DESIGN.md`
- `docs/IMPLEMENTATION_READINESS_AND_EXIT_CRITERIA.md`

No code, tests, scripts, workflows, provider calls, or research operations were executed. This audit and the associated edits are documentation-only on the isolated agent branch. The current Phase 3 G0-05 handoff remains controlling.

## Finding R-01 — cancellation after durable dispatch intent was underspecified

The unified lifecycle matrix said cancellation resulted in a cancelled state where no irreversible delivery had occurred, while its race section said cancellation after the durable dispatch-start boundary could not erase the attempt. The dispatcher contract did not define whether a cancellation arriving after the dispatch-intent transaction but before the external provider call should suppress that call, leave it pending, or require reconciliation.

This is a distributed-transaction boundary: the registry commit and external provider call cannot be one atomic action. Treating cancellation as proof of non-delivery could therefore lose an authorized attempt or allow unsafe redelivery.

**Resolution recorded in the unified lifecycle and dispatcher contracts:**

1. The atomic `dispatch_started` registry commit is the authorization/attempt linearization point.
2. Cancellation or revocation committed before that transaction wins; dispatch is denied and the provider is not called.
3. That transaction atomically revalidates approval, expiry/revocation, handoff/policy, assignment state and idempotency identity, consumes a single-use approval, and records the immutable attempt plus stable provider key.
4. After commit, the attempt remains irrevocably recorded. Later cancellation/revocation blocks future attempts but cannot assert that the existing attempt was never sent.
5. If cancellation lands between registry commit and provider invocation, the dispatcher resolves the already-committed attempt with its original provider idempotency key. It must not silently drop the attempt and relabel it undispatched. Any provider-side cancellation is a separate authenticated operation with its own approval and receipt.
6. Unknown outcomes remain pending/uncertain and are reconciled using the same provider identity; no automatic retry or new identity is allowed.
7. Cancellation state is represented separately from dispatch/delivery state; it must not overwrite an in-flight attempt.

## Finding R-02 — approval consumption and revocation serialization needed one explicit transaction boundary

The registry interface already required atomic single-use consumption and specified that a revocation committed first denies the operation, while an operation committed first records the approval state used. The unified lifecycle now makes the exact dispatch-start transaction the shared linearization point and requires approval revalidation and consumption inside it. This avoids a check-then-use gap between approval lookup and dispatch-intent persistence.

## Cross-check of recovery behavior

The existing pure `classify_assignment_recovery()` remains deliberately conservative:
- `dispatch_started` + no return → `delivery_pending_or_unknown`, reconcile before any retry;
- `delivery_uncertain` + no return → manual delivery reconciliation, no automatic retry;
- no branch authorizes dispatch/retry, changes queue state, or approves task/gate completion.

The pure classifier does not model cancellation as a distinct input and does not authenticate observations. That is acceptable for its present narrow role, but a future trusted registry/recovery adapter must combine cancellation status with the independent dispatch-attempt state and provider receipt. Do not expand the pure classifier into an operational cancellation controller without a separately approved schema and handoff.

## Remaining implementation blockers

- No transactional registry/backend exists to enforce the stated serialization.
- No approval service, dispatcher identity, provider delivery channel, idempotency receipt, or cancellation API is selected or implemented.
- Provider cancellation semantics, if any, remain provider-specific and unverified.
- No failure-injection test has demonstrated the race outcomes.
- The current handoff prohibits the relevant runtime validation; all such tests remain blocked.
- No tests/scripts/workflows were run; the agent remains non-operational.

## Disposition

Documentation-level inconsistency corrected in the unified lifecycle and dispatcher contracts. This is not implementation approval, dispatch authorization, a backend selection, or a change to the research handoff.
