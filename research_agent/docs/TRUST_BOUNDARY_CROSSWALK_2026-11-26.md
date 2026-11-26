# Trusted-boundary cross-contract audit — 2026-11-26

## Status and authority

Static documentation/code inspection only. This audit changes no research logic and grants no execution, test, dispatch, persistence, workflow, scheduling, gate-closure, or phase-advancement authority. The current Phase 3 G0-05 handoff remains controlling and prohibits the relevant scripts, tests, and workflows.

The audit compares the assignment-package/return modules, event ledger, optimistic persistence primitive, orchestration coordinator, and the three future design contracts:
- `docs/TRUSTED_ASSIGNMENT_REGISTRY_DESIGN.md`
- `docs/TRUSTED_DISPATCHER_CONTRACT.md`
- `docs/TRUSTED_STORE_ADAPTER_DESIGN.md`

## Findings

### 1. Lifecycle event vocabulary is incomplete — implementation blocker

The registry and dispatcher designs require authenticated records for approval, dispatch start, delivery pending/unknown, delivery confirmation, cancellation/revocation, and potentially assignment revision. The current `engine/event_ledger.py` allowlists only:

- `task_observed`
- `assignment_prepared`
- `worker_submission_received`
- `review_completed`
- `human_disposition_recorded`

The current schema therefore cannot directly represent several transitions the future state machine requires. The pure recovery policy can classify delivery states, but that does not create durable event types or authenticated observations.

**Required resolution before any adapter implementation:** choose one explicit, versioned event-schema evolution plan. Options include adding a versioned event envelope with an allowlisted lifecycle vocabulary, or maintaining a separate typed registry transition log with a rigorously specified atomic link to the existing ledger. Do not overload `task_observed` or put transition names in arbitrary payload fields as a substitute for schema-level validation. Do not silently change historical hashes or existing event meanings. Define migration/backward-compatibility rules and shared test vectors before implementation.

Candidate future event names for review (not approved or implemented): `approval_recorded`, `assignment_prepared`, `dispatch_started`, `delivery_pending_or_unknown`, `delivery_confirmed`, `assignment_cancelled`, `worker_submission_received`, `review_completed`, `human_disposition_recorded`, and `assignment_revision_created`. The final vocabulary must distinguish facts that come from different authenticated sources.

### 2. Existing persistence primitive is not a registry transaction — known design boundary

`engine/persistence_contract.py` prepares an in-memory append against an expected ledger head. It does not lock, authenticate the caller, retain a checkpoint, persist an assignment row, enforce a delivery-index uniqueness constraint, or atomically update a registry state version. Its result flags correctly remain non-persistent and non-authorizing.

**Required resolution:** the future adapter must implement one transaction boundary for assignment state, event record, delivery idempotency index, and protected checkpoint, or specify and independently prove an equivalent transactional outbox/inbox protocol. A sequence of unrelated writes is insufficient.

### 3. Assignment digest currently has no independent durable owner — known design boundary

`engine/orchestration_coordinator.py` calculates package digests and explicitly marks `package_digest_stored=False`. `engine/assignment_return.py` requires an independently supplied expected package digest and verifies the complete supplied package against a rebuilt canonical package, but the module cannot authenticate or retain that expected digest itself.

**Required resolution:** the future registry must retain both exact canonical package bytes (or immutable content-addressed object) and the dispatcher-computed digest before delivery. Return review must load the expected package and digest from that trusted registry, never from the worker return. The existing module API remains a pure review primitive until that trusted adapter exists.

### 4. Approval and task allowlisting are distinct authorities — preserve separation

The safety controller's task-definition allowlist hash is not an authenticated, single-use approval to run a workflow or deliver a worker assignment. The dispatcher/registry designs correctly require a separate approval record bound to the exact operation, workflow SHA, task digest, branch, handoff revision, scope, and input commit.

**Required resolution:** no future workflow input, queue field, worker declaration, or task allowlist entry may stand in for the authenticated approval record. Approval must be rechecked for expiry/revocation and exact scope at the protected operation boundary.

### 5. Source authentication remains outside all current pure modules

The event ledger validates source category and reference shape but cannot authenticate the source. The evidence verifier compares bytes against a caller-supplied commit manifest but cannot authenticate the manifest or checkout. The assignment-return path receives expected digest, task, manifest, and bytes as arguments; it cannot prove who supplied them.

**Required resolution:** the future workflow/adapter must derive repository, ref, workflow identity, run/attempt, actor, event/delivery identity, commit, and manifest from authenticated platform/checkout context. Worker-supplied metadata remains untrusted. The registry must keep approval and checkpoint data outside worker write access.

### 6. Canonicalization must be selected before cross-runtime integration

The current event and task/package hashing use Python JSON serialization with sorted keys, compact separators, UTF-8, and non-finite values rejected. This is deterministic for the documented Python implementation, but it is not a declared cross-language canonicalization standard.

**Required resolution:** either pin every writer/verifier to a specified Python runtime and serializer implementation, or introduce a versioned RFC 8785/JCS-compatible contract with shared independent test vectors. Do not migrate existing event hashes without an explicit versioned migration and historical verification plan.

### 7. Delivery uncertainty must not be treated as retry permission

The recovery policy classifies dispatch-started and uncertain delivery as requiring reconciliation and disallows automatic retries. The registry/dispatcher designs preserve this correctly.

**Required resolution:** stable authenticated provider delivery identity, durable idempotency index, authenticated receipt, and protected checkpoint must all be reconciled before another request. A worker timeout, missing artifact, or absent response is not proof that delivery did not happen.

### 8. Human disposition and phase-gate closure remain separate

The review pipeline and assignment-return modules deliberately do not approve task completion or gate closure. The registry design also separates authenticated human disposition from phase-gate closure.

**Required resolution:** persist task acceptance only as a human disposition bound to the exact assignment revision and review digest. Phase-gate closure and phase advancement require their own separate authenticated decision and must still respect the controlling research handoff.

## Cross-contract implementation order

The following is a dependency order, not permission to begin implementation:

1. Resolve event vocabulary/versioning and canonicalization compatibility.
2. Approve repository topology, trusted-store backend, service identities, approval channel, retention, and backup/restore model.
3. Specify a unified transaction schema for assignment records, approval records, delivery index, returns, reviews, event log, and protected checkpoint.
4. Specify authenticated platform-context extraction and operation-boundary handoff/policy revalidation.
5. Produce threat model and failure-injection matrix, including concurrent dispatch, duplicate delivery, lost response, commit uncertainty, cancellation races, stale approvals, backup rollback, and malicious worker returns.
6. Implement only after explicit authorization and after the controlling G0-05 handoff permits the exact code/test/workflow scope.
7. Independently review before any manual readiness workflow. Keep actual worker delivery and scheduled/event-driven operation separately gated.

## Current verified limitations

- No trusted assignment registry or backend exists.
- No protected assignment digest store or event-ledger checkpoint exists.
- No authenticated dispatcher, worker-delivery channel, or return receiver exists.
- No agent-specific workflow is active.
- No tests, scripts, or workflows were run for this audit.
- No research code/data, canonical research definitions, protected research branch, default branch, secrets, permissions, VPS, or runner configuration were changed.
- The current G0-05 handoff remains authoritative; no task execution, dispatch, scheduling, candidate generation, backtesting, PnL claim, strategy selection, gate closure, or phase advancement is authorized.


## 9. Follow-up resolution — versioned event model and unified transaction

The event-vocabulary decision is now documented in:
- `EVENT_SCHEMA_V2_PROPOSAL.md` — preserve v1 unchanged and propose a separate v2 registry lifecycle log.
- `UNIFIED_TRUSTED_LIFECYCLE_TRANSACTION_SPEC.md` — define the global registry sequence, per-assignment state version, replay-before-stale-check ordering, authenticated operation-boundary approval, and atomic commit of state/event/idempotency/checkpoint.

This resolves the **documentation-level architecture choice**: one trusted assignment registry owns one globally sequenced v2 lifecycle log; per-assignment state versions provide an additional compare-and-swap guard; the existing v1 ledger remains immutable legacy evidence. It does not resolve backend selection, identity provisioning, approval-channel implementation, checkpoint trust root, cross-language canonicalization vectors, or transaction failure testing.

The unified specification is a proposal, not implementation authority. The original G0-05 restrictions remain controlling. No tests, scripts, workflows, dispatch, or protected-branch changes were performed.
