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


## 10. Follow-up threat analysis and failure-injection plan

The new docs/THREAT_MODEL_AND_FAILURE_INJECTION_MATRIX.md records protected assets, actors, trust boundaries, independence requirements for approval/workflow/registry/evidence roots, 26 threat scenarios, and 30 proposed failure-injection cases with expected safe oracles and evidence to retain.

The analysis identifies atomic state/event/idempotency/checkpoint persistence, operation-boundary approval, authenticated delivery, anti-rollback recovery, and trust-root separation as critical design blockers. It distinguishes worker-claim validation, evidence-byte integrity, task disposition, and phase-gate authority.

This is a documentation-level risk analysis and future test plan only. Likelihood and residual-risk acceptance are not asserted. No failure injection, tests, scripts, or workflows were run. The current G0-05 handoff remains controlling; no activation or protected-branch change is authorized.


## 11. Security control gap audit

`docs/SECURITY_CONTROL_GAP_AUDIT_2026-11-26.md` maps the threat register to inspected pure modules and lifecycle proposals. It distinguishes present source-level restrictions from partial caller-supplied verification, design-only trust controls, and unestablished operational components. The main blockers are independent trust roots, atomic durable registry transactions, retained package digests, authenticated operation-boundary approval, authenticated dispatch/delivery/return, and anti-rollback recovery.

This was a bounded static source/document review, not an exhaustive workflow or deployment audit. No tests, scripts, workflows, or failure injections were run. G0-05 remains controlling; the agent remains non-operational.


## 12. Backend-neutral registry interface contract

`docs/TRUSTED_REGISTRY_BACKEND_INTERFACE_SPEC.md` now consolidates the minimum future backend semantics: immutable record model; authenticated read ports; atomic lifecycle command ports; global and per-assignment concurrency tokens; replay-before-stale-check idempotency; exact operation-bound approval/revocation; provider idempotency/queryability; return/review/human-authority separation; error taxonomy; and independent anti-rollback recovery evidence.

This is a contract for later design/implementation review, not a backend choice or implementation. It does not resolve repository topology, identity/approval provider, canonicalization vectors, provider selection, or checkpoint witness. No code, tests, workflows, dispatch, or protected-branch changes were made. G0-05 remains controlling and the agent remains non-operational.


## 13. Idempotency identity reconciliation

A focused cross-document review found that the store-adapter and assignment-registry drafts described the provider-delivery identity as `(source_namespace, delivery_id)`, while the v2/unified lifecycle contract requires `(source_namespace, delivery_id, event_role)` for event-level replay where one delivery can produce multiple legitimate lifecycle events. These are complementary identity levels, not competing alternatives.

The documents are now aligned: the pair is the unique authenticated provider-delivery identity; the triple is the unique event-level idempotency identity with a closed schema-defined role. Each derived event ID is based on the event-level tuple. The provider-delivery record links its per-role event receipts, and replay checks complete normalized facts before stale-checkpoint rejection. A fixed single role may be used where one delivery maps to exactly one event.

This is a documentation-level consistency correction only. No event schema, hash, code, test, workflow, dispatch, or research artifact was changed or executed. G0-05 remains controlling.


## 14. Backend selection decision framework

`docs/TRUSTED_BACKEND_SELECTION_FRAMEWORK.md` translates the registry contract and threat model into mandatory qualification gates, architecture-class comparisons, trust-domain topology, a weighted scorecard, unresolved owner decisions and a staged proof-of-capability process. It identifies managed relational transaction stores as the first class worth evaluating, not as a selected provider; every candidate must prove atomic dual-version updates, replay behavior, identity separation and independent anti-rollback.

No provider was researched/selected, no account or resource created, no credential provisioned, and no tests or workflows run. This remains a design artifact; G0-05 is still controlling.


## 15. Consolidated implementation readiness and exit criteria

`docs/IMPLEMENTATION_READINESS_AND_EXIT_CRITERIA.md` consolidates the research-authority boundary, owner decisions, independent trust-root requirements, registry transaction semantics, assignment/dispatch/return integrity, workflow and runner security, authorized validation, operational readiness, evidence-register fields, ordered exit criteria, and non-negotiable stop conditions.

The checklist distinguishes PASS, FAIL, UNKNOWN, and BLOCKED; missing or caller-supplied evidence cannot count as PASS. It records the present system as a documented, non-operational foundation: no backend or trust roots selected, no trusted package-digest custody or authenticated dispatcher, no active agent workflow, and no authorized runtime validation. The repository default-branch activation constraint is retained as a blocker rather than worked around.

This is a documentation-only readiness control. It does not approve implementation, backend selection, repository creation, a `main` change, workflow activation, credential/resource provisioning, tests, scripts, dispatch, scheduling, or research execution. The active G0-05 handoff remains authoritative.


## 16. Synthetic backend proof-of-capability plan

`docs/SYNTHETIC_BACKEND_PROOF_OF_CAPABILITY_PLAN.md` defines a vendor-neutral future evaluation protocol using synthetic identities and records only. It specifies entry conditions, twelve test families covering atomic transactions, dual concurrency, replay/idempotency, identity levels, approval/revocation, package digest custody, delivery uncertainty, authenticated returns, workflow provenance, canonicalization, checkpoint rollback/restore, and least privilege; it also defines evidence retention, global acceptance rules, stop conditions, and cleanup.

The plan is not a test report and does not select or qualify any provider. No candidate was evaluated, no account/resource/credential was created, and no tests or workflows were run. Execution remains blocked pending owner decisions, isolated environment approval, independent review, and explicit authorization consistent with the active G0-05 handoff.
