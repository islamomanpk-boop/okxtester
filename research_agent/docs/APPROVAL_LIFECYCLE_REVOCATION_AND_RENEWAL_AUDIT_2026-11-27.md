# Approval lifecycle, revocation, and renewal audit — 2026-11-27

## 1. Scope and authority

Targeted static review of:
- `UNIFIED_TRUSTED_LIFECYCLE_TRANSACTION_SPEC.md`
- `TRUSTED_REGISTRY_BACKEND_INTERFACE_SPEC.md`
- `TRUSTED_ASSIGNMENT_REGISTRY_DESIGN.md`
- `TRUSTED_DISPATCHER_CONTRACT.md`
- `DISPATCH_CANCELLATION_AND_REVOCATION_RACE_AUDIT_2026-11-27.md`
- `TRUST_ROOT_SEPARATION_AND_IDENTITY_ARCHITECTURE.md`
- `IMPLEMENTATION_READINESS_AND_EXIT_CRITERIA.md`

This review examines whether approval issuance, expiry, revocation, single-use consumption, replay, and renewal have one consistent immutable lifecycle. It does not inspect a deployed approval provider or registry; none is selected or operating.

The active Phase 3 G0-05 handoff remains controlling. This audit authorizes no implementation, tests, scripts, workflows, dispatch, scheduling, research execution, credentials, or infrastructure.

## 2. Executive finding

**Core dispatch-time revocation serialization is already specified correctly.** The unified lifecycle requires approval revalidation, expiry/revocation checks, single-use consumption, and immutable dispatch-attempt creation in one transaction. Revocation committed before that transaction wins; a dispatch-start committed first remains an auditable attempt and cannot be erased by later revocation.

The remaining gap is the complete approval-record lifecycle around that boundary. The documents do not yet state one consolidated, normative rule set for:
- immutable approval facts versus derived mutable status;
- approval-ID and nonce uniqueness;
- whether expiry can ever be extended in place;
- whether a revoked or consumed approval can be reactivated;
- whether renewal requires a new approval ID and fresh human authentication;
- exact replay versus conflicting duplicate issuance/revocation;
- what revocation means after the approval has already been consumed and dispatch has started;
- how approval status is reconstructed after restore without treating missing history as active.

This is a documentation-contract gap, not evidence of an implemented vulnerability. No live approval mechanism exists.

## 3. Findings

### A-01 — Approval record immutability and revocation-state representation need alignment

The registry design describes an immutable approval record but also lists expiry/revocation state among its bound fields. The backend interface separately models a distinct immutable revocation record. Without an explicit rule, implementers could interpret revocation as an in-place mutation of the approval row.

**Resolution required:** approval issuance facts are immutable. Revocation, consumption, and any administrative invalidation are separate append-only events/records. Current status is derived from the approval plus its ordered lifecycle events and trusted service time; never rewrite the original approval.

### A-02 — Renewal and extension are not explicitly distinguished

The contracts say scope changes require fresh approval and expired approvals cannot be revived by replaying earlier workflow input. They do not explicitly prohibit changing expiry on the same approval ID or reactivating a revoked/consumed approval.

**Resolution required:** no in-place extension, renewal, un-revocation, or reactivation. A renewed authorization is a new immutable approval with a new approval ID, fresh authenticated human decision, new nonce, explicit expiry, and a complete binding to the current exact scope. It does not reset or replace the history of the prior approval.

### A-03 — Approval ID and nonce uniqueness need explicit transactional enforcement

The interface lists a nonce/consumption policy, but the reviewed lifecycle rules do not fully state global uniqueness, one-time issuance semantics, or how concurrent duplicate approval submissions resolve.

**Resolution required:** enforce unique approval ID and unique nonce in the approval issuer's namespace; bind nonce to approver, exact approval facts, and issuer. Exact delivery replay returns the original receipt; same idempotency identity with changed facts is rejected. Reuse of a nonce under a different delivery identity is rejected, not interpreted as a new approval.

### A-04 — Revocation is monotonic, but its event/idempotency behavior needs to be explicit

The existing documents say revocation is authenticated and durable, but do not fully distinguish exact duplicate revocation from a conflicting second revocation or a purported un-revoke.

**Resolution required:** one approval may have at most one effective revocation transition. Exact authenticated replay is idempotent and returns the original receipt. Changed revocation facts under the same identity are an integrity conflict. Un-revocation is forbidden; a new authorization requires a new approval ID and nonce.

### A-05 — Post-consumption revocation must not imply provider-side cancellation

The dispatch race audit correctly says a revocation after `dispatch_started` cannot erase or relabel the attempt as unsent. The broader approval lifecycle should state that revocation still blocks any future operation under that approval, but does not recall an already committed attempt or revoke provider acceptance retroactively.

**Resolution required:** if delivery cancellation is desired after dispatch-start, it is a distinct authenticated provider-cancellation operation, with its own exact scope, approval where required, idempotency identity, receipt, and lifecycle event. Approval revocation and provider cancellation are never conflated.

### A-06 — Expiry semantics need a clear linearization rule

The contracts require trusted service time at the operation boundary, but should make clear that approval validity is evaluated inside the same transaction that consumes it and commits the protected operation. A request received before expiry but committed after expiry must not pass based on a client timestamp.

**Resolution required:** use trusted registry/approval-service time inside the serialized transaction. The approval must be unexpired at the transaction's authorization point. A committed dispatch attempt remains historically valid as an attempt even if the approval expires later; expiry blocks future operations, not the already committed event.

### A-07 — Restore must derive status conservatively

The backup/restore protocol already says missing revocation or consumption history blocks an operation. The approval lifecycle should explicitly require replay of the immutable event history and comparison with the independent checkpoint before any status is considered active.

**Resolution required:** no approval is considered active from an approval row alone. Missing, divergent, or unverifiable issuance/revocation/consumption history, nonce index, or checkpoint means status UNKNOWN and operation denied.

## 4. Normative approval lifecycle

The following state model is recommended for the future registry contract. It is a derived view; underlying records/events remain immutable.

| Derived status | Meaning | Permitted next transition |
|---|---|---|
| `issued_active` | Authenticated immutable approval exists; not expired, revoked, consumed, or invalidated | Consume once for exact authorized operation; revoke; expire by trusted time |
| `consumed` | Exact protected operation committed atomically with single-use consumption | No reuse; retain attempt/receipt history |
| `revoked` | Authenticated revocation committed before consumption | Terminal; no reactivation |
| `expired` | Trusted service time is at/after expiry before operation commit | Terminal; no extension or reactivation |
| `invalidated_by_scope_change` | Bound task/package/workflow/handoff/branch/input/operation facts no longer match | Terminal for that approval; issue a new approval only after fresh review |
| `unknown` | Missing history, failed integrity/checkpoint verification, or ambiguous status | Deny; reconcile through authenticated recovery |

Precedence is conservative: integrity/lineage failure yields `unknown`; a committed consumption remains historical fact; a committed revocation before consumption makes the approval unusable; expiry is evaluated at the protected transaction's trusted time. No status transition may reverse a terminal state.

### 4.1 Issuance

1. Authenticate the human approver independently; verify role, scope, session strength, and current authority.
2. Construct immutable canonical approval facts: approval ID, issuer/namespace, approver subject, nonce, operation enum, exact repository/ref, workflow path and immutable SHA, task ID/digest, assignment/revision/package digest, handoff/policy revision, input commit, scope/prohibitions, issued-at, expires-at, and schema/canonicalization version.
3. Validate bounded lifetime and trusted issuer time; reject caller-supplied timestamps as authority.
4. Enforce uniqueness for approval ID and nonce atomically.
5. Append `approval_issued` and retain the issuance receipt/checkpoint. Exact replay returns the original receipt; changed facts or reused nonce are rejected.
6. Never create a broad standing approval or infer approval from allowlisting, preflight, workflow actor, or prior task acceptance.

### 4.2 Revocation

1. Authenticate a principal with explicit revocation authority; derive identity from the trusted channel.
2. Bind revocation to one exact approval ID and immutable approval digest; record revoker, trusted timestamp, reason code, source identity, and idempotency identity.
3. Serialize revocation against operation consumption using the same registry transaction boundary and current global/assignment version.
4. If revocation commits first, all later protected operations using that approval are denied.
5. If consumption/dispatch-start commits first, preserve that operation and its approval-state/sequence receipt; revocation blocks any future operation under the approval but does not erase, rewrite, or claim recall of the committed attempt.
6. Exact replay is idempotent; conflicting replay is rejected. Un-revocation is not supported.

### 4.3 Consumption and operation boundary

1. Revalidate the complete approval binding, current policy/handoff, assignment revision, workflow identity, branch, input commit, operation, expiry, revocation, nonce, and unused status inside the protected transaction.
2. Evaluate expiry using trusted transaction/service time, not client time or workflow input.
3. Atomically append the operation event and `approval_consumed` event/record (or a single event carrying both facts), bind the exact approval digest and event sequence, and persist the dispatch attempt/idempotency identity.
4. A committed consumption cannot be reset by retry, workflow rerun, backup restore, changed run ID, or a new delivery ID.
5. If transaction outcome is uncertain, reconcile by the same trusted idempotency identity before any further operation. Never mint a replacement identity to evade uncertainty.

### 4.4 Renewal and scope changes

- Expiry extension, reactivation, un-revocation, or reuse of an approval ID is forbidden.
- Renewal means a new approval record with a new approval ID and nonce, a fresh authenticated human decision, current policy/handoff checks, and a newly computed complete scope binding.
- Any change to task digest, assignment revision/package digest, repository/ref, workflow path/SHA, handoff/policy revision, input commit, operation class, or scope requires a new approval.
- The old approval remains expired, revoked, consumed, or invalidated in history. A new approval does not rewrite or revive it.
- A new approval does not automatically authorize a second delivery if an earlier attempt is pending/uncertain; reconcile the original attempt first.

## 5. Required concurrency and recovery scenarios

Future synthetic conformance tests should demonstrate:
1. Revocation commits just before consumption: operation denied, no provider call.
2. Consumption commits just before revocation: one immutable attempt retained; revocation blocks subsequent operations.
3. Two concurrent consumes of one approval: exactly one succeeds.
4. Two concurrent revocations: one effective revocation; exact replay returns same receipt.
5. Same approval ID with altered expiry/scope: rejected.
6. Same nonce with another approval ID or delivery identity: rejected.
7. Expiry boundary: transaction before expiry may pass; transaction at/after expiry fails using trusted service time.
8. Expiry extension or un-revoke request: rejected; fresh approval ID required.
9. Exact replay after revocation/consumption: returns original historical receipt only, never a new authorization.
10. New delivery ID attempting to reuse consumed approval: denied.
11. Revocation after dispatch-start but before provider response: attempt remains pending/uncertain and reconciles using original provider key; no silent drop or new attempt.
12. Restore missing revocation/consumption/nonce history: approval status UNKNOWN; all affected operations denied until authenticated reconciliation.

These are test requirements only; none has been run.

## 6. Cross-document corrections required

- Registry design: clarify that approval issuance facts are immutable and revocation/consumption are separate append-only lifecycle events, not mutable fields.
- Backend interface: define approval ID/nonce uniqueness, monotonic status derivation, no renewal-in-place, and exact replay/conflicting replay behavior.
- Unified lifecycle: add explicit issue/revoke/consume/renewal semantics and state precedence.
- Dispatcher contract: clarify that any renewal is a fresh approval ID and that approval consumption is immutable; distinguish revocation from provider cancellation.
- Recovery/restore: status UNKNOWN and deny if approval lifecycle or nonce history is incomplete.
- Readiness gate: retain revocation race tests as BLOCKED until the controlling handoff permits synthetic validation.

## 7. Current status and hard boundary

- Approval/dispatch lifecycle exists only as a design proposal.
- No approval service, registry, dispatcher, backend, identity, nonce store, or provider channel is implemented or selected.
- No credentials, keys, accounts, infrastructure, or permission changes were made.
- No tests, scripts, workflows, dispatch, scheduling, VPS access, or research operations were run.
- The agent remains non-operational.
- The active Phase 3 G0-05 handoff remains authoritative.

This is a targeted contract audit, not a live-system security finding, runtime validation, or authorization to activate the agent.
