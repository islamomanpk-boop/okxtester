# OKX Research Agent

`okx-research-agent` is a free-first, deterministic research-operations agent for the OKX Price Action V1 repository. It is designed to organize approved work, inspect permitted evidence, and produce reproducible reports through GitHub Actions.

## Current status

- Foundation configuration, fail-closed safety controller, phase-ordered task queue, and empty trusted allowlist are present.
- Agent execution and scheduling remain disabled.
- Repository inspection is read-only by default.
- No unattended general-purpose LLM is assumed or required.
- Reports are intended for GitHub Actions artifacts.
- Work is organized in the agreed order: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5.
- No automatic merge or write to the research branch is permitted.
- The safety controller, task queue, report builder, and artifact-preparation layer have not been runtime-tested; no scripts, tests, or workflows have been run as part of this setup.
- The safety controller binds approvals to the SHA-256 hash of the exact queued task definition; changing its phase, operation, scope, or restrictions invalidates that approval.
- Trusted policy JSON loading rejects duplicate object keys rather than accepting the parser's last-value-wins behavior.
- The safety controller validates every queue entry's full contract (including blocked future-phase tasks) and rejects duplicate queue IDs, malformed allowlist hashes, duplicate allowlist approvals, phase-priority mismatches (with strict integer typing), boolean-type confusion, missing human-gate advancement rules, unsupported or missing policy keys, schema-version drift, and weakened global operation defaults, incomplete task contracts, duplicate scope/prohibition entries, unsupported task fields, missing mandatory prohibitions, and non-human completion authority. It also enforces read-only repository access, the exact isolated branch policy, no automatic merge/research-branch commits, and disabled scheduling.
- The public runtime authorization function loads policy only from fixed repository configuration paths; policy injection is isolated to a private test seam.
- Markdown report rendering flattens line breaks and escapes Markdown control characters in untrusted findings and metadata; untrusted values are not placed inside Markdown code spans, preventing delimiter breakout.
- Report validation enforces a strict top-level schema, the fixed `okx-research-agent` identity, string-only narrative lists, canonical UTC timestamps ending in `Z` with shortest fractional formatting, normalized safe manifest paths, finite JSON values, and only allowlisted non-completion statuses (`preflight_only`, `blocked`, `skipped`, `not_run`). Task-definition hashing additionally rejects non-string object keys, non-finite numbers, and Python-only values before canonical JSON serialization. The safety controller and report builder now use the same digest function; a report-task binding verifier checks task ID, phase, and digest against the exact trusted task object.
- While the current G0-05 lock is active, all Phase 3 task authorization is denied, regardless of task labels.
- Only tasks marked `queued` in the currently active phase are eligible for future evaluation; later phases remain blocked.

## Hard safety boundary: Phase 3 G0-05

The current G0-05 handoff requires read-only reconciliation and explicitly prohibits running scripts, tests, or workflows, changing code or data, generating candidates, backtesting, making PnL claims, selecting strategies, or closing G0-05. This restriction takes precedence over general agent permissions. The agent must not bypass it through another workflow, task, or trigger.

## Permission model

Every proposed task must pass all of these checks before it can be considered for execution:

1. The task ID is explicitly present in the trusted task allowlist.
2. Its phase is recognized and has the relevant permission.
3. No current handoff or gate restriction prohibits the operation.
4. The operation is in the controller's narrow read-only allowlist.
5. The agent execution master switch is enabled.

A missing, ambiguous, malformed, or conflicting permission means **deny**. The task itself cannot grant its own permission. The current trusted allowlist is intentionally empty.

## Components

- `config/agent_config.json` — identity, operating mode, scheduling defaults, and global prohibitions.
- `config/phase_permissions.json` — phase order and operation-level permission boundaries.
- `config/task_queue.json` — initial phase-ordered task definitions and dependencies.
- `config/task_allowlist.json` — trusted task-definition hash approvals; currently empty.
- `engine/safety_controller.py` — fail-closed evaluator that requires an exact queue match, a trusted SHA-256 approval, an active phase, and read-only permission; it never executes tasks.
- `engine/event_ledger.py` — pure append-only event-chain primitives with stable-ID replay handling and hash-chain verification. It performs no persistence, authorization, task-state mutation, or gate closure; a future trusted store must retain the ledger head independently. See [EVENT_LEDGER.md](EVENT_LEDGER.md).
- `engine/persistence_contract.py` — pure optimistic-concurrency preparation for event-ledger appends. It detects stale head checkpoints and accepts exact replays without duplicating events; it is not an atomic store and performs no persistence. See [PERSISTENCE_CONTRACT.md](docs/PERSISTENCE_CONTRACT.md).
- [Trusted store adapter design](docs/TRUSTED_STORE_ADAPTER_DESIGN.md) — proposal-only requirements for a future authenticated, durable, atomic event store. No backend is selected or implemented.
- [Event schema v2 proposal](docs/EVENT_SCHEMA_V2_PROPOSAL.md) — proposal to preserve v1 hashes and introduce a separately versioned, globally sequenced lifecycle log for trusted assignment-registry transitions; not implemented or approved.
- [Unified trusted lifecycle transaction specification](docs/UNIFIED_TRUSTED_LIFECYCLE_TRANSACTION_SPEC.md) — reconciles the v2 event log, assignment registry, store, and dispatcher into one atomic transaction protocol; proposal only.
- [Trusted dispatcher contract](docs/TRUSTED_DISPATCHER_CONTRACT.md) — design-only approval, package-retention, authenticated delivery, return, replay, and failure-handling contract. No dispatcher or delivery channel is implemented.
- [Trusted assignment registry design](docs/TRUSTED_ASSIGNMENT_REGISTRY_DESIGN.md) — proposal-only immutable assignment, approval, delivery, return, review, and transaction-boundary requirements. No registry or backend is implemented.
- [Trusted registry backend interface specification](docs/TRUSTED_REGISTRY_BACKEND_INTERFACE_SPEC.md) — backend-neutral record model, read/transaction ports, atomicity and idempotency rules, operation-bound approval, provider requirements, recovery and conformance criteria; design only, no backend selected or implemented.
- [Trusted backend selection framework](docs/TRUSTED_BACKEND_SELECTION_FRAMEWORK.md) — mandatory qualification gates, backend architecture-class comparison, trust topology, weighted evaluation scorecard, owner decisions and staged evaluation; no provider selected or resources created.
- [Implementation readiness and exit criteria](docs/IMPLEMENTATION_READINESS_AND_EXIT_CRITERIA.md) — consolidated PASS/FAIL/UNKNOWN/BLOCKED gates for owner decisions, trust roots, registry transactions, dispatch, workflow security, authorized validation, operations, evidence retention, and stop conditions; checklist only, not activation authority.
- [Synthetic backend proof-of-capability plan](docs/SYNTHETIC_BACKEND_PROOF_OF_CAPABILITY_PLAN.md) — vendor-neutral synthetic-only conformance scenarios for atomicity, concurrency, replay, approval, package custody, delivery uncertainty, provenance, rollback, and least privilege; design only, not run.
- [Trust-root separation and identity architecture](docs/TRUST_ROOT_SEPARATION_AND_IDENTITY_ARCHITECTURE.md) — defines independent human, policy, dispatcher, registry, workflow, worker, evidence, reviewer, and checkpoint trust domains plus operation-level identity controls; proposal only, no identities provisioned.
- [Approval lifecycle, revocation, and renewal audit](docs/APPROVAL_LIFECYCLE_REVOCATION_AND_RENEWAL_AUDIT_2026-11-27.md) — defines immutable approval issuance, monotonic revocation, single-use consumption, fresh-ID renewal, trusted-time expiry, and fail-closed recovery semantics; documentation-only.
- [Trust-root administrative independence audit](docs/TRUST_ROOT_ADMINISTRATIVE_INDEPENDENCE_AUDIT_2026-11-27.md) — audits cross-domain administrator, identity-provider, witness, deployment, recovery, audit-log, and billing dependencies; independence remains UNKNOWN pending real permission evidence; documentation-only.
- [Backup restore and anti-rollback recovery audit](docs/BACKUP_RESTORE_AND_ANTI_ROLLBACK_AUDIT_2026-11-27.md) — defines fail-closed restore acceptance, independent checkpoint comparison, in-flight delivery reconciliation, and human resume authorization; documentation-only.
- [Dispatch cancellation and revocation race audit](docs/DISPATCH_CANCELLATION_AND_REVOCATION_RACE_AUDIT_2026-11-27.md) — resolves the cancellation-after-dispatch-intent ambiguity, approval-consumption race, and uncertain-delivery recovery boundary; documentation-only, no tests or dispatch.
- [Provider delivery idempotency and receipt audit](docs/PROVIDER_DELIVERY_IDEMPOTENCY_AND_RECEIPT_AUDIT_2026-11-27.md) — specifies provider key scope/retention, immutable request binding, authenticated receipts, query semantics, and safe uncertain-delivery handling; design-only.
- [Security architecture contradiction audit](docs/SECURITY_ARCHITECTURE_CONTRADICTION_AUDIT_2026-11-27.md) — reconciles emergency denial versus frozen registry writes, independent resume quorum, approval immutability, and distinct cancellation/revocation semantics; design-only.
- [Emergency suspension, break-glass, and resume protocol](docs/EMERGENCY_SUSPENSION_BREAK_GLASS_AND_RESUME_PROTOCOL_2026-11-27.md) — defines deny-only emergency freeze, dual-control recovery access, independent review, external audit, and multi-party resume; design-only.
- [Restore and witness reconciliation audit](docs/RESTORE_AND_WITNESS_RECONCILIATION_AUDIT_2026-11-27.md) — distinguishes a legitimate outbox-backed witness-pending commit from rollback/fork during disaster recovery; documentation-only.
- [Event-ledger concurrency and witness transaction audit](docs/EVENT_LEDGER_CONCURRENCY_AND_WITNESS_TRANSACTION_AUDIT_2026-11-27.md) — audits v1 hash/replay and optimistic concurrency, and clarifies the two-phase database commit/external checkpoint-witness acknowledgment protocol; documentation-only.
- [Lifecycle state-machine and recovery consistency audit](docs/LIFECYCLE_STATE_MACHINE_RECOVERY_CONSISTENCY_AUDIT_2026-11-27.md) — distinguishes the advisory recovery classifier from the full trusted lifecycle, including cancellation, approvals, attempts, return eligibility, revisions, human disposition, and phase-gate state; documentation-only.
- [Worker-return lifecycle, replay, and late-arrival audit](docs/WORKER_RETURN_LIFECYCLE_REPLAY_AUDIT_2026-11-27.md) — audits raw-byte receipt, authenticated delivery binding, duplicate/conflicting return replay, late-return eligibility, review idempotency, and human-disposition separation; documentation-only, no receiver or tests exist.
- [Agent documentation consistency audit](docs/AGENT_DOCUMENTATION_CONSISTENCY_AUDIT_2026-11-27.md) — targeted cross-document review of branch/workflow status, phase authority, package digest custody, event identity/canonicalization, and human gate boundaries; one stale inventory count corrected.
- [Security control gap audit](docs/SECURITY_CONTROL_GAP_AUDIT_2026-11-26.md) — maps threat controls to inspected modules, design-only requirements, activation blockers, and implementation priorities.
- [Threat model and failure-injection matrix](docs/THREAT_MODEL_AND_FAILURE_INJECTION_MATRIX.md) — lifecycle threat register, trust-root independence, failure oracles, and future validation plan; no tests or injections executed.
- [Trusted-boundary cross-contract audit](docs/TRUST_BOUNDARY_CROSSWALK_2026-11-26.md) — static comparison of lifecycle events, persistence, assignment digest custody, approvals, authentication, canonicalization, and human authority; records implementation blockers without authorizing work.
- [Integration audit](docs/INTEGRATION_AUDIT_2026-11-26.md) — current module connections, deny-only preflight consequence, missing trusted persistence/dispatch links, and ordered activation gates.
- `engine/orchestration_coordinator.py` — composes one trusted queue/preflight snapshot, phase-ordered planning, assignment packages and optional recovery guidance into a non-dispatching in-memory snapshot. Package digests are calculated but not claimed as independently stored; caller recovery observations remain unauthenticated. See [ORCHESTRATION_COORDINATOR.md](ORCHESTRATION_COORDINATOR.md).
- `engine/recovery_policy.py` — classifies safe next steps for prepared, in-flight, uncertain, delivered, returned, reviewed, and human-disposition states. It never auto-dispatches or retries; uncertain delivery requires manual reconciliation. See [RECOVERY_POLICY.md](docs/RECOVERY_POLICY.md).
- `engine/task_runner.py` — preflight-only queue dispatcher with exact single-task checks and a bounded whole-queue visibility summary; it has no subprocess, script, test, workflow, or research executor.
- `engine/report_builder.py` — deterministic JSON/Markdown reports, safe input manifests, provenance checks, in-memory artifact bundle creation, and downloaded-artifact verification. It performs no filesystem writes or uploads.
- `engine/artifact_preparation.py` — joins the trusted queue, one task's preflight result, the preflight-only report factory, and in-memory artifact bundling. It is restricted to this repository and isolated agent branch. A denial becomes a blocked audit artifact; the module performs no task work, queue updates, filesystem writes, uploads, or scheduling. Runtime workflow metadata must be independently supplied and verified by a future workflow. See [ARTIFACT_PREPARATION.md](ARTIFACT_PREPARATION.md).
- `engine/batch_planner.py` — `build_runtime_batch_plan()` loads queue and preflight data from fixed runtime sources (no caller-supplied queue/result), then creates a bounded phase-ordered plan carrying task scope, prohibitions, handoff ID, and digest. `build_batch_plan()` is only the pure planning/test seam. Neither function authorizes or executes work or changes task state. See [BATCH_PLANNER.md](BATCH_PLANNER.md).
- `engine/supervisor_review.py` — validates untrusted worker submissions against the exact trusted task, including task digest, a fail-closed allowlist of declared read-only actions, evidence-reference shape (including Windows drive-path rejection), and safety claims. A valid submission is only marked ready for human review; evidence bytes and research correctness remain unverified, and task/gate completion are never approved. See [SUPERVISOR_REVIEW.md](SUPERVISOR_REVIEW.md).
- `engine/evidence_verifier.py` — compares worker-declared evidence hashes and checkout bytes against a caller-supplied manifest for one exact commit. It is pure/read-only and does not authenticate the caller or obtain Git data; a future workflow must supply trusted commit context. Passing integrity checks never approves task completion or gate closure. See [EVIDENCE_VERIFICATION.md](EVIDENCE_VERIFICATION.md).
- `engine/review_pipeline.py` — joins structural supervisor review with independent evidence-integrity checks. Structural/safety failures stop before evidence verification; hash or byte mismatches return the submission for revision. A passing result remains human-review-only. See [REVIEW_PIPELINE.md](REVIEW_PIPELINE.md).
- `engine/assignment_package.py` — binds the exact trusted task, preflight outcome, and batch-planner entry into a complete worker handoff. It carries the handoff ID, scope, prohibitions, digest, and submission schema; it never dispatches a worker or grants execution authority. Under the active G0-05 lock it records a blocked package. See [ASSIGNMENT_PACKAGE.md](ASSIGNMENT_PACKAGE.md).
- `engine/assignment_return.py` — verifies a returned submission against the exact prepared assignment and a separately retained trusted package SHA-256 before supervisor/evidence review. A worker-returned digest is not trusted; the future dispatcher must retain and supply the expected digest independently. It rejects blocked or tampered packages; it does not prove dispatch or delivery and never approves completion.
- `engine/review_artifact.py` — converts an assignment-bound supervisor/evidence review into the existing provenance-checked, in-memory report bundle. Worker claims remain labelled declarations, malformed non-JSON or excessively nested values receive safe type-marker rendering, report status stays `not_run`, and human-only completion authority is preserved. See [REVIEW_ARTIFACT.md](docs/REVIEW_ARTIFACT.md).
- Regression coverage authored but not executed: 32 safety-controller, 51 report-builder, 28 task-runner, 7 artifact-preparation, 12 batch-planner, 18 supervisor-review, 10 evidence-verifier, 6 integrated-review, 10 assignment-package, 13 assignment-return, 8 review-artifact, 13 event-ledger, 9 persistence-contract, 11 recovery-policy, and 8 orchestration-coordinator tests (236 total). None have been executed because the active G0-05 handoff prohibits the relevant validation.
- `.github/workflows/` — no agent-specific workflow is installed yet. The first future workflow must be manual-dispatch only and preflight/report-only; event-driven and scheduled triggers require separate validation and approval.

## Full-project phase coverage

See [PHASE_SUPPORT_MATRIX.md](PHASE_SUPPORT_MATRIX.md) for the shared operating model and queue coverage across all five phases in the agreed order: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5. The agent is reusable across the full project; Phase 3 is only the current active phase. Later phases remain blocked until predecessor gates are human-authorized closed and their own handoffs permit work.

## Validation and activation gates

See [VALIDATION_AND_ACTIVATION.md](VALIDATION_AND_ACTIVATION.md) for completed setup, deferred runtime checks, and conditions for safe activation. Static review does not count as runtime validation.

## Activation policy

See [ACTIVATION_DECISION.md](ACTIVATION_DECISION.md) for the default-branch dispatch constraint and the reviewed activation options. The preferred isolation path is a separate agent repository; no repository creation or `main`-branch change is authorized by that recommendation.

Creating this scaffold does not authorize running it. Do not add or enable any agent workflow until the safety controller, task allowlist, and independent validation are complete and the applicable research handoffs permit execution. The G0-05 handoff remains authoritative even if a future agent configuration is changed.
