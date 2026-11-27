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


## 17. Trust-root separation and identity architecture

`docs/TRUST_ROOT_SEPARATION_AND_IDENTITY_ARCHITECTURE.md` defines logical trust domains and operation-level identity responsibilities for human authority, policy, dispatcher, registry, workflow platform, worker/provider, evidence store/verifier, independent reviewer, and checkpoint witness. It specifies prohibited cross-domain capabilities, an operation-to-identity matrix, twelve independence tests, credential lifecycle requirements, repository/default-branch implications, and evidence required for an independent security review.

This is a vendor-neutral proposal only. It does not select or provision identities, credentials, keys, services, repositories, or workflows. Effective permissions and trust-root independence remain UNKNOWN until independently demonstrated. No tests, scripts, workflows, or research operations were run. The agent remains non-operational and G0-05 remains controlling.


## 18. Agent documentation consistency audit

`docs/AGENT_DOCUMENTATION_CONSISTENCY_AUDIT_2026-11-27.md` records a targeted cross-document review of branch/workflow status, phase authority, package-digest custody, event identity and canonicalization, authored-versus-executed test reporting, and the separation of human task disposition from phase-gate closure. It found and corrected one stale “13 agent files” description in the workflow design; the current compare snapshot reports 66 changed files, all under `research_agent/`.

The review found the other examined authority and activation boundaries consistent, while retaining the existing implementation blockers. This is not an exhaustive source audit or security certification. No tests, scripts, workflows, dispatch, scheduling, or research operations were run, and the active G0-05 handoff remains controlling.


## 19. Lifecycle lookup contract clarification

The documentation consistency audit identified an API naming ambiguity between provider-delivery lookup and event-role replay lookup. The registry interface and store-adapter design now define two distinct read ports:

- `lookup_provider_delivery(source_namespace, delivery_id)` returns the complete authenticated provider-delivery aggregate and its linked event-role receipts.
- `lookup_event_receipt(source_namespace, delivery_id, event_role)` returns the receipt for one closed-schema event-level idempotency tuple.

This preserves the distinction between the provider-delivery identity pair and event-level idempotency triple. The unified transaction protocol continues to resolve exact event-role replay before stale-checkpoint rejection. Documentation only; no backend or adapter is implemented.


## 20. Dispatch cancellation and approval-revocation race clarification

`docs/DISPATCH_CANCELLATION_AND_REVOCATION_RACE_AUDIT_2026-11-27.md` records a targeted static comparison of the recovery policy and trusted lifecycle/dispatcher/registry/store contracts. It identified an ambiguity when cancellation arrives after the durable `dispatch_started` commit but before the external provider call.

The unified lifecycle and dispatcher contracts now define that commit as the authorization/attempt linearization point: revocation/cancellation committed first denies dispatch; after the commit, the attempt remains recorded and must be resolved with the same provider idempotency key. Cancellation blocks future attempts but cannot claim non-delivery or erase an in-flight attempt. Single-use approval consumption and final revocation/expiry validation occur atomically with dispatch-start. Cancellation is stored separately from delivery state. Unknown outcomes remain pending/uncertain and are never automatically retried.

The pure recovery classifier remains non-authorizing and does not model cancellation; a future trusted adapter must combine cancellation status with dispatch-attempt state and authenticated provider evidence. No implementation or runtime validation was performed. G0-05 remains controlling.


## 21. Backup restore and anti-rollback recovery protocol

`docs/BACKUP_RESTORE_AND_ANTI_ROLLBACK_AUDIT_2026-11-27.md` records a targeted review of restore acceptance semantics. It identified that the contracts required an independent checkpoint but lacked one consolidated protocol for stale, ahead, forked, or schema-incompatible snapshots and for reconciling approvals and in-flight provider attempts. The unified lifecycle, store adapter, and registry designs now require a frozen restore, exact independent witness comparison, authenticated recovery of missing history only, provider reconciliation by original delivery identity, explicit treatment of missing revocations/consumption as blockers, a signed restore report, and independent human resume authorization.

Documentation only. No backend, witness, backup, or restore mechanism exists; no recovery drill or runtime test was run. G0-05 remains controlling.


## 22. Trust-root administrative independence audit

`docs/TRUST_ROOT_ADMINISTRATIVE_INDEPENDENCE_AUDIT_2026-11-27.md` records a targeted review of whether the proposed approval channel, registry administrator, checkpoint witness, workflow/deployment authority, and recovery roles are independent across actual administrative accounts and transitive control paths. The logical trust-domain model is consistent, and the backend framework already warns that services sharing one administrator credential are not independent. However, no administrative dependency graph, effective permission exports, identity-provider/root recovery inventory, witness retention administration proof, break-glass separation evidence, or independent audit/billing dependency analysis exists yet.

The audit therefore rates administrative independence UNKNOWN / BLOCKED—not failed, and not demonstrated. It adds a concrete evidence matrix and ten future correlated-compromise scenarios. No provider, account, credential, key, service, or topology was selected or provisioned; no tests, scripts, workflows, dispatch, scheduling, or research operations were run. The agent remains non-operational and G0-05 remains controlling.


## 23. Approval lifecycle, revocation, and renewal audit

`docs/APPROVAL_LIFECYCLE_REVOCATION_AND_RENEWAL_AUDIT_2026-11-27.md` records a targeted review of approval issuance, immutable scope, expiry, single-use consumption, revocation, replay, renewal, and restore semantics. Existing contracts already serialize approval revalidation/consumption with dispatch-start and preserve a committed attempt if revocation follows. The review identified missing explicit rules for immutable issuance facts, separate append-only revocation/consumption events, unique approval IDs/nonces, monotonic revocation, no in-place expiry extension or reactivation, fresh approval IDs/nonces for renewal, trusted-time expiry checks, and UNKNOWN status when lifecycle history is incomplete.

The unified lifecycle, backend interface, assignment registry, and dispatcher contracts now carry these clarifications. This is documentation-only: no approval service, registry, nonce store, dispatcher, or provider exists; no tests, scripts, workflows, dispatch, scheduling, or research operations were run. The agent remains non-operational and G0-05 remains controlling.


## 24. Worker-return lifecycle, replay, and late-arrival audit

`docs/WORKER_RETURN_LIFECYCLE_REPLAY_AUDIT_2026-11-27.md` records a targeted static review of `engine/assignment_return.py` and the lifecycle/registry/dispatcher contracts. The current helper accepts an already-parsed dictionary and caller-supplied package digest; it does not authenticate a return transport, retain/hash raw bytes, allocate a receiver-owned return ID, bind a provider delivery, persist a receipt, classify late arrivals, or enforce duplicate-return/review idempotency. It correctly remains review-only and explicitly does not verify dispatch/delivery or approve task/gate completion.

The audit makes the future contract precise: authenticated return-delivery identity; immutable raw-byte capture and receiver hash before strict parsing; exact replay returning the original receipt; changed replay quarantined without overwriting; distinct delivery IDs with identical payload bytes linked but not automatically reviewed twice; trusted binding to dispatch attempt and retained package; immutable late/cancelled/expired/revoked/malformed eligibility; review identity bound to return digest/revision/policy; and human disposition bound to one exact review digest. The unified lifecycle, assignment registry, backend interface, and dispatcher documents now carry these requirements. This is documentation-only: no receiver/backend exists, no tests or failure injections were run, and no dispatch, workflow, schedule, VPS, or research operation was performed. The agent remains non-operational and G0-05 remains controlling.


## 25. Lifecycle state-machine and recovery-policy consistency audit

`docs/LIFECYCLE_STATE_MACHINE_RECOVERY_CONSISTENCY_AUDIT_2026-11-27.md` compares the recovery classifier with the future registry/dispatcher lifecycle. The classifier is conservative for its limited delivery/review/disposition inputs, but it omits cancellation, approval lifecycle, multiple attempts/provider receipts, return eligibility, assignment revisions, authenticated human identity, and phase-gate state. It must remain advisory and cannot serve as the authoritative assignment state or sole recovery decision.

The recovery-policy documentation and unified transaction specification now explicitly separate immutable assignment revision, approval lifecycle, per-attempt delivery state, cancellation, raw return receipt/eligibility, review, task disposition, and phase-gate disposition. They clarify that cancellation is orthogonal to delivery, later provider evidence resolves the same attempt, late/ineligible returns remain preserved but excluded from normal completion, revision requests do not authorize a new revision, and task acceptance does not close a phase gate. Documentation-only; no code, tests, workflows, dispatch, scheduling, or research operations were performed. The agent remains non-operational and G0-05 remains controlling.


## 26. Event-ledger concurrency and external-witness transaction audit

`docs/EVENT_LEDGER_CONCURRENCY_AND_WITNESS_TRANSACTION_AUDIT_2026-11-27.md` statically reviewed the v1 event ledger, optimistic-concurrency helper, store-adapter contract, v2 event proposal, and unified lifecycle design. Existing pure helpers correctly validate event hashes/shape and exact replay, and reject stale new appends; they do not persist or provide atomic compare-and-swap. The future adapter already specifies authenticated delivery identity, replay-before-stale-checkpoint, unique constraints, concurrent first-delivery reconciliation, and atomic registry updates.

The audit identified a precision gap: a database transaction cannot normally atomically advance a separately administered external checkpoint witness. The store adapter, unified lifecycle spec, and backend interface now define two distinct phases: (1) atomic database commit of event/state/indexes/internal checkpoint plus durable witness outbox; (2) separate monotonic witness advancement and authenticated acknowledgment. Protected writes remain frozen while witness-pending; restart reconciles pending outbox records before resuming. Database and witness receipts are distinct. The documents also require whole-transaction abort/reload/revalidation after serialization, deadlock, or uniqueness conflicts. No implementation or tests were run; no backend/witness is selected or active. Agent remains non-operational and G0-05 remains controlling.


## 27. Restore and witness reconciliation audit

`docs/RESTORE_AND_WITNESS_RECONCILIATION_AUDIT_2026-11-27.md` reviews restore after the two-stage database-commit/external-witness protocol. A database head exactly one sequence ahead of the witness is not automatically a fork: it is witness-pending only when one durable outbox item exactly extends the authenticated witness tuple. Restore must replay that exact checkpoint identity, obtain the witness receipt, and record acknowledgment without creating a new event. At most one unacknowledged checkpoint is allowed while protected writes are frozen. A witness-ahead database requires exact missing history from an independently authenticated source; unexplained leads, missing/mismatched outbox, broken predecessor, fork, or identity/schema mismatch fail closed. Provider attempts, approval issuance/revocation/consumption, assignment revisions, and raw-return binding must be reconciled before separate human resume authorization. No backend or witness exists and no restore tests were run; G0-05 remains controlling.


## 28. Emergency suspension, break-glass, and resume authority

`docs/EMERGENCY_SUSPENSION_BREAK_GLASS_AND_RESUME_PROTOCOL_2026-11-27.md` defines deny-only emergency freeze, two-person short-lived break-glass activation, role separation among recovery operator/witness verifier/reviewer/resume authority, independent append-only incident audit, and multi-party resume bound to the exact checkpoint and recovery report. Emergency freeze may be triggered immediately by a designated authenticated reporter; it cannot resume service or authorize work. Break-glass cannot issue approvals, rewrite history/witness, alter policy, suppress audit, or bypass G0-05. The trust-root architecture, administrative independence audit, and unified lifecycle spec now reference these controls. Actual administrative independence and effective permissions remain UNKNOWN; no credentials, accounts, infrastructure, or workflows were provisioned or changed.


## 29. Security architecture contradiction audit and emergency-denial reconciliation

`docs/SECURITY_ARCHITECTURE_CONTRADICTION_AUDIT_2026-11-27.md` compares the unified lifecycle, registry, backend/store, approval, restore, trust-root, emergency, and readiness contracts. It resolved four documentation ambiguities: emergency credential containment versus frozen registry writes; the exact independent two-human resume quorum; immutable approval issuance facts versus derived revocation status; and separation of assignment cancellation, approval revocation, credential revocation, and provider-side cancellation.

The emergency protocol now uses an independent deny-only security-plane hold. Credential/session/key containment can proceed out of band, but approval-revocation events are not appended while the registry is witness-pending. After the current head is reconciled, only a restricted deny-only security-revocation lane may append exact approval revocation/invalidation events; it cannot grant authority or clear the hold, and its resulting checkpoint must be externally witnessed before hold release. Affected approvals remain unusable/UNKNOWN meanwhile. The backend contract also requires race-safe hold fencing at the protected commit boundary; if this cannot be proven, ingress must be independently disabled and the capability remain offline. Resume requires two distinct human approvers with independent credential/admin recovery paths, separate from requester, recovery, witness, reviewer, and deployment roles. The readiness checklist now includes these gates. All controls remain design-only; no identity, service, credential, permission, test, workflow, or infrastructure was provisioned or changed. G0-05 remains controlling.


## 30. Provider delivery idempotency and receipt audit

`docs/PROVIDER_DELIVERY_IDEMPOTENCY_AND_RECEIPT_AUDIT_2026-11-27.md` tightens the dispatcher-to-provider boundary. It requires provider-specific key scope and retention evidence, exact immutable request-envelope binding, no provider side effect before the atomic `dispatch_started` commit, authenticated raw receipts/callbacks, monotonic status observations, and documented query/absence semantics. Same-key resubmission is permitted only inside a proven deduplication window with the exact retained request; after possible key expiry the system must query only and never resubmit. Unresolved outcomes remain UNKNOWN and require escalation. The dispatcher, unified lifecycle, backend interface, store adapter, and implementation-readiness gates were updated. No provider is selected or qualified; dispatch remains blocked and the agent non-operational. No tests, scripts, workflows, provider calls, or research operations were run; G0-05 remains controlling.

## 31. Provider dispatch crash recovery and lost-receipt protocol

`docs/PROVIDER_DISPATCH_CRASH_RECOVERY_AUDIT_2026-11-27.md` enumerates crash points from before dispatch-start through provider submission/acceptance, provider-observation commit, external witness acknowledgment, and lost dispatcher response. It clarifies that dispatch_started proves only an authorized attempt was recorded, not that provider submission/acceptance occurred. Acceptance followed by a crash before receipt persistence must be reconstructed through authenticated provider query/history by the original key/job identity; providers without durable query/history or a separately proven durable callback inbox are not qualified for unattended delivery. Provider-observation identity is separate from command, delivery, and witness identities; raw evidence, immutable facts digest, observation index, state projection, event, checkpoint and witness outbox commit atomically. Exact replay returns the original receipt; conflicting replay fails closed. The unified lifecycle, dispatcher contract, backend interface and readiness gates were updated. No provider, dispatcher, registry or witness is implemented; no tests, scripts, workflows, provider calls or research operations were run. G0-05 remains controlling.


## 32. Provider callback ingestion, replay, and ordering audit

`docs/PROVIDER_CALLBACK_INGESTION_AND_ORDERING_AUDIT_2026-11-27.md` defines the future callback-receiver boundary: authenticate exact raw bytes before parsing; persist raw evidence, immutable event identity/facts, and a processing outbox before successful transport acknowledgment; distinguish transport receipt from semantic status application; make exact replay idempotent and conflicting event-ID reuse a security conflict; order observations by provider sequence/version rather than arrival time; reconcile gaps and conflicting terminal observations; bind every callback to exactly one committed attempt; and keep witness-pending projections from authorizing protected decisions. The dispatcher and backend interface now reference these requirements. No callback receiver, provider, signing key, backend, or witness is selected or implemented. No tests, scripts, workflows, network requests, provider calls, dispatch, or research operations were run; the agent remains non-operational and G0-05 remains controlling.


## 33. Provider status reconciliation and terminal consistency audit

`docs/PROVIDER_STATUS_RECONCILIATION_AND_TERMINAL_CONSISTENCY_AUDIT_2026-11-27.md` closes a documentation gap across provider query APIs, callback streams, history, dashboards, and local projections. It rejects universal source precedence and defines source qualification by authentication, exact scope/attempt binding, version/order, consistency horizon, completeness, and retention. Delivery, execution, cancellation, evidence quality, reconciliation, task disposition, and phase-gate disposition remain orthogonal. Not-found proves absence only under documented authoritative semantics; partial history, gaps, expiry, unavailable sources, and conflicting terminal observations remain UNKNOWN. Reconciliation is immutable and cannot authorize retry or human task/gate acceptance. The unified lifecycle, dispatcher, and backend interface now reference these requirements. No provider or integration is selected or implemented; no tests, scripts, workflows, network requests, provider calls, dispatch, scheduling, VPS access, or research operations were run. The agent remains non-operational and G0-05 remains controlling.


## 34. Worker execution isolation and resource-limits audit

`docs/WORKER_EXECUTION_ISOLATION_AND_RESOURCE_LIMITS_AUDIT_2026-11-27.md` identifies that logical worker identity separation does not establish process, filesystem, network, credential, or resource isolation. It requires a disposable per-assignment sandbox; minimal immutable input bundle; no host mounts/sockets or ambient credentials; deny-all network with controlled egress only by explicit approval; fixed reviewed tools/images; hard externally enforced CPU, memory, PID, disk, time, bandwidth, output, concurrency and cost ceilings; separate unprivileged artifact inspection; trusted telemetry, kill/fence, and verified cleanup. The threat model and readiness gates must treat runtime isolation as UNKNOWN/BLOCKED until independently tested. No runtime/provider/policy is configured and no tests or sandbox executions were run. The agent remains non-operational and G0-05 remains controlling.


## 35. Evidence-pipeline integrity and human-acceptance audit

`docs/EVIDENCE_PIPELINE_INTEGRITY_AND_HUMAN_ACCEPTANCE_AUDIT_2026-11-27.md` confirms that pure submission/evidence validators provide structural checks and byte comparison only. They cannot authenticate caller-supplied checkout manifests, file bytes, workflow metadata, or raw worker-return transport. The future system must authenticate and durably preserve raw return bytes before parsing; bind return and evidence to the trusted assignment/package and delivery attempt; derive commit/tree manifests from authenticated clean checkout context; retain immutable evidence objects and uploader/run provenance; separate worker claims from reviewer findings; enforce read-only reviewer access; and bind human task disposition to exact return/evidence/review digests and current handoff. Task acceptance and phase-gate closure remain separate. Retention, data residency, encryption/key custody and access policy remain unselected. No receiver, evidence store, artifact upload, reviewer identity or human-disposition service exists; no tests or operations were run. G0-05 remains controlling.


## 36. Control-plane authorization and permission-model audit


## 37. Operational observability and incident-detection audit


## 38. Software supply-chain and build-provenance audit


## 39. Research-data integrity, access-control and privacy audit

`docs/RESEARCH_DATA_INTEGRITY_ACCESS_CONTROL_AND_PRIVACY_AUDIT_2026-11-27.md` identifies the absence of an operational data catalog/classification, task-to-object authorization service, immutable source/evidence store, independently enforced read-only snapshots, privacy/retention policy, and access audit. It requires exact task-bound object manifests, default-deny access, immutable source custody, filesystem/database-level read-only enforcement, snapshot consistency, derived-data lineage, privacy minimization, quarantined outputs, cross-assignment isolation, no ambient secrets, governed retention/deletion, and synthetic boundary validation. A worker cannot widen its data grant, mutate source evidence, promote outputs, or delete protected data. No protected research data, database, or VPS data was accessed or changed; no permissions, code, tests, scripts, workflows, storage, or integrations were configured or run. The agent remains non-operational and G0-05 remains controlling.

`docs/SOFTWARE_SUPPLY_CHAIN_AND_BUILD_PROVENANCE_AUDIT_2026-11-27.md` identifies that worker-isolation requirements for pinned dependencies, fixed images, immutable actions, and trusted runtime provenance are not yet backed by a complete dependency inventory/lock, approved package-source policy, isolated trusted builder, SBOM, signed provenance, signing-key lifecycle, vulnerability process, or independent deployment verifier. It requires immutable action/workflow commit SHAs, image digests, complete transitive dependency hashes, provenance-to-runtime binding, cache isolation, revocation, and synthetic conformance. No dependencies, lockfiles, actions, images, package sources, build services, scanners, signatures, or credentials were changed or configured. No packages were installed and no tests, builds, scripts, workflows, network requests, or deployments were run. The agent remains non-operational and G0-05 remains controlling.

`docs/OPERATIONAL_OBSERVABILITY_AND_INCIDENT_DETECTION_AUDIT_2026-11-27.md` identifies the absence of a deployed end-to-end observability plane and specifies the future read-only monitoring boundary. It defines a closed severity taxonomy; immutable-ID correlation and replay/conflict handling; bounded stuck-assignment and missing-evidence detection; independent alert routing and escalation; acknowledgement, silence, and closure as monitoring-only records; monitoring-of-monitoring; secret/data minimization; trusted time, sequence, and retention; evidence-preserving incident runbooks; and synthetic coverage requirements. Monitoring cannot approve, dispatch, retry, cancel, revoke, clear holds, change policy, close gates, or resume operations. No monitoring vendor, log store, alert manager, notification channel, on-call rotation, incident system, recipient, or retention policy is selected or configured. No tests, scripts, workflows, integrations, network requests, or incident notifications were run. The agent remains non-operational and G0-05 remains controlling.

`docs/CONTROL_PLANE_AUTHORIZATION_AND_PERMISSION_MODEL_AUDIT_2026-11-27.md` consolidates the remaining gap between logical trust-domain separation and enforceable operation-specific permissions. It requires a closed deny-by-default operation/resource matrix; common-root-aware role-conflict enforcement; one canonical authorization decision bound to exact task, assignment, package, workflow, handoff, policy, approval and checkpoint facts; transaction-bound approval consumption; effective GitHub permission and administration evidence before activation; strict resource limits for emergency freeze, credential containment, deny-only revocation, witness, break-glass and resume; identity/session assurance; versioned policy governance; and independent authorization telemetry. Emergency resume must return only to a non-dispatching read-only state; normal activation remains a separate decision. No live permissions or identity settings were inspected or changed, no tests or workflows were run, and no implementation was activated. G0-05 remains controlling.


## 40. Business continuity and disaster-recovery boundary

The [business continuity and disaster-recovery readiness audit](BUSINESS_CONTINUITY_AND_DISASTER_RECOVERY_READINESS_AUDIT_2026-11-27.md) adds continuity objectives, common-mode failure-domain analysis, backup completeness, coupled checkpoint consistency, isolated non-dispatching restore, provider-side-effect reconciliation, witness outage states, key/policy recovery, schema migration safety, independent runbooks, capacity exhaustion, and externally retained drill evidence. A backup job, successful service startup, matching wall-clock timestamps, or restored local database does not establish a safe recovery point. Registry/event/witness/package/approval/dispatch/provider/return/evidence identities must reconcile before any protected write or external side effect. Recovery may restore read-only visibility only; normal activation and dispatch require separate current authorization. No RTO/RPO, provider, region, backup, recovery operator roster, or tested restore capability is currently approved or operational.

## 41. Architecture dependency and integration-gap audit

The [architecture dependency and integration-gap audit](ARCHITECTURE_DEPENDENCY_AND_INTEGRATION_GAP_AUDIT_2026-11-27.md) distinguishes pure implemented primitives, in-memory composition, documented contracts, and absent operational adapters. The current strongest path is queue → preflight → plan → prepared package → parsed-return review → in-memory report; it is not a trusted end-to-end lifecycle. Critical missing joins include durable package-digest custody, authenticated dispatcher/provider receipts, raw-byte return receiver, independently derived complete evidence manifest, authenticated human disposition, atomic registry/event/witness transaction, enforced worker/data isolation, and workflow activation. It defines 15 findings and an ordered dependency sequence. This is static design evidence, not operational readiness or permission to integrate/execute.

## 42. Consolidated implementation roadmap and dependency gates

The [consolidated implementation roadmap](CONSOLIDATED_IMPLEMENTATION_ROADMAP_AND_DEPENDENCY_GATES_2026-11-27.md) sequences the work into 13 evidence-backed gates: current G0-05 authority; owner/trust-topology decisions; supply chain; data/evidence; registry/event transaction; authorization/dispatch; worker isolation; authenticated return; independent review/human disposition; artifacts/monitoring/incident controls; backup/recovery; workflow activation/manual preflight; bounded pilot then unattended automation. It explicitly separates implemented pure/in-memory primitives from design-only contracts and absent operational adapters. Gates require independently verifiable evidence; NOT RUN, UNKNOWN, and BLOCKED are not PASS. This roadmap does not authorize implementation or bypass the active handoff.

## 43. Module implementation versus operational readiness

The [module implementation versus operational readiness audit](MODULE_IMPLEMENTATION_VS_OPERATIONAL_READINESS_AUDIT_2026-11-27.md) maps all 15 engine modules to what is actually implemented versus what remains absent. It distinguishes local validation/hash/planning/review primitives from authenticated authority, trusted package-digest custody, durable registry/event transactions, provider dispatch/receipts, raw-byte return custody, complete manifests, human disposition, and operational adapters. Caller-supplied expected values and manifests are not self-authenticating. The 15 corresponding test files are authored only and have not been executed. This is static classification, not runtime validation or activation authority.