# Consolidated implementation roadmap and dependency gates — 2026-11-27

## Purpose and authority

This roadmap consolidates the current agent design, implementation inventory, integration gaps, security audits, and controlling research restrictions into one ordered execution plan. It is a planning artifact only. It does not authorize implementation, testing, workflow changes, data access, dispatch, deployment, or phase advancement. The current Phase 3 G0-05 handoff remains controlling and overrides this roadmap.

## Executive status

The project has substantial documentation and deterministic, pure/in-memory building blocks. It does not yet have a trusted end-to-end operational lifecycle. The present work is therefore architecture and preparation, not operational completion. The central missing capability is a trusted control plane joining authenticated authority, durable atomic state, immutable evidence, bounded execution, and independent review.

Current state: NOT OPERATIONAL. No unattended worker is running. No production backend, registry, dispatcher, provider adapter, authenticated return receiver, worker sandbox, independent witness, monitoring plane, backup service, or approved activation bridge is configured. Authored tests have not been executed under the current G0-05 restriction.

## Non-negotiable invariants

1. Current handoff and phase/gate restrictions take precedence over all queue labels, planner output, workflow triggers, and this roadmap.
2. Complete Phase 3 G0-05 reconciliation under the controlling handoff; do not advance or close it without authorized evidence and human disposition.
3. Preserve the agreed phase order: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5.
4. Agent branch isolation; no merge, write, or automatic commit to the protected research branch.
5. Deny by default. Workers cannot grant themselves authority, approve tasks, close gates, or change policy.
6. No research-data mutation, candidate generation, backtesting, PnL conclusions, or strategy selection outside a later explicit authorization.
7. Unknown identity, provenance, provider outcome, witness state, evidence completeness, or permission means hold/quarantine—not retry or assume success.
8. Recovery begins isolated, read-only, and non-dispatching. Restoring service does not restore permission to act.
9. No secrets in source, reports, prompts, or worker inputs; no VPS or self-hosted runner access for the agent.
10. Documentation, authored tests, static review, and synthetic design are not evidence of runtime validation.

## Workstream inventory and current disposition

| Workstream | Existing foundation | Missing proof or capability | Disposition |
|---|---|---|---|
| Policy and task definitions | Strict schemas, task digests, fail-closed controller, phase order | Authenticated policy publisher, effective permission exports, operation-bound approvals | Designed/partly implemented; runtime unverified |
| Planning and assignment | Preflight, non-authorizing batch planner, package builder | Durable assignment reservation and independent package-digest custody | Pure/in-memory only |
| Registry and event history | Event-chain primitives, persistence contract, backend interface | Authenticated API, ACID transactions, uniqueness/CAS, durable state, independent witness | Not implemented |
| Dispatcher and provider | Detailed dispatch, idempotency, callback and recovery contracts | Provider selection, workload identity, durable attempt, authenticated receipts and reconciliation | Not implemented |
| Worker execution | Isolation/resource/data-access requirements | Disposable sandbox, deny-all egress, exact read-only grants, hard quotas, kill/fence and cleanup | Design only |
| Return and evidence | Structural review, byte-hash verifier, report builders | Raw-byte authenticated receiver, receipt-before-parse, trusted complete manifest, immutable evidence store | Pure primitives only |
| Research review and acceptance | Supervisor structural checks and human-authority boundaries | Independent methodology/source review and authenticated immutable human disposition | Not integrated |
| Artifacts and workflow | In-memory report bundle and verification functions | Trusted workflow context, artifact upload/download round-trip, default-branch topology | Not operational |
| Monitoring and incident response | Threat/observability/hold/runbook designs | Independent telemetry, alerts, operators, effective emergency hold and tested response | Design only |
| Backup and continuity | Restore, anti-rollback, disaster-recovery specifications | Backup inventory, independent witness, isolated restore, measured RTO/RPO and drills | Not operational |
| Supply chain | Dependency/build provenance audit | Locked dependencies, approved builder, SBOM/signatures, immutable workflow/image pins, runtime verification | Not operational |

## Ordered roadmap and exit gates

### Gate 0 — Research authority and G0-05 closure

**Goal:** Finish the currently authorized Phase 3 reconciliation without bypassing its restrictions.

Required evidence: current authoritative handoff; completed independent Copilot review or documented disposition; reconciled source/canonical mapping findings; explicit treatment of the conditional CENSORED plus non-null confirmation timestamp edge case; any required real-row validation only if a future handoff explicitly authorizes it; owner/reviewer disposition.

Exit: controlling handoff explicitly permits the next exact scope and the relevant human gate is recorded. Until then, no scripts, tests, workflows, code/data changes, candidate generation, backtests, or G0-05 closure.

### Gate 1 — Owner decisions and trust topology

**Goal:** Decide the architecture boundaries before selecting products or building adapters.

Decisions: same repository versus separately governed agent repository; hosting/account/region; trusted registry architecture; independent identity and approval roots; witness model; canonicalization/versioning; data classification/residency/retention; worker provider; alerting and recovery ownership; budget and operational burden; component RTO/RPO.

Exit: written owner decisions and threat-reviewed trust-domain/role-conflict matrix. No credentials or accounts need be created during this decision gate.

### Gate 2 — Supply chain and build foundation

**Goal:** Make every future executable component reproducible and attributable.

Required: complete dependency/tool inventory; platform-specific hash locks; package-source policy; isolated builder; immutable workflow/action/image references; SBOM; signed provenance tied to source, materials, builder and output digest; signer separation and revocation; vulnerability/malicious-package handling; runtime digest verification.

Exit: independent verification of a synthetic build/release record and negative substitution/tampering cases. No worker build or deployment before this gate.

### Gate 3 — Data and evidence foundation

**Goal:** Protect source research evidence and define exactly what a task may inspect.

Required: data classification; task-bound exact-object grants; immutable source snapshots; read-only enforcement; complete object manifests; provenance and schema/version semantics; privacy minimization; secret scanning; retention/deletion and legal-hold rules; assignment isolation; output quarantine; prompt/data-injection handling.

Exit: synthetic access-control and evidence-integrity proof demonstrates no write, traversal, cross-assignment read, unapproved export, secret exposure, or untrusted-output promotion.

### Gate 4 — Trusted registry and event transaction

**Goal:** Establish one authenticated, durable source of lifecycle truth.

Required: backend passes every mandatory qualification gate; authenticated command API; immutable task/assignment/package/approval records; transaction-bound policy and emergency-hold fencing; atomic event + materialized state + idempotency index + checkpoint + witness outbox; global and per-assignment concurrency; exact replay semantics; external monotonic witness and authenticated receipt; protected backup/anti-rollback.

Exit: independent synthetic proof of concurrent commits, replay, conflicts, revocation races, crash recovery, witness outage, rollback detection, and no partial state.

### Gate 5 — Authorization and dispatcher

**Goal:** Permit only exact, current, approved operations and make delivery uncertainty safe.

Required: operation-bound human approval; fresh authorization at dispatch linearization point; exact task/handoff/phase/package/revision binding; narrow dispatcher identity; provider-qualified idempotency scope/retention/query guarantees; durable attempt before call; authenticated provider receipts; cancellation/revocation race handling; no blind retries.

Exit: synthetic provider simulator proves one logical delivery under duplicates and preserves UNKNOWN when acceptance/receipt is uncertain.

### Gate 6 — Isolated worker runtime

**Goal:** Run only bounded approved tasks in disposable environments.

Required: per-assignment disposable strong sandbox; fixed reviewed image; no root/host sockets/mounts; no ambient secrets; exact read-only inputs; deny-all network except explicitly reviewed necessities; CPU/memory/PID/disk/time/output/concurrency/cost ceilings; external kill/fence; output quarantine; verified cleanup and telemetry.

Exit: negative synthetic isolation and resource-exhaustion tests pass independently. No research VPS or self-hosted runner.

### Gate 7 — Authenticated return and evidence custody

**Goal:** Accept only authentic, task-bound, replay-safe worker returns.

Required: authenticate exact raw bytes; durable receiver receipt and raw digest before parse/ack; strict decoding/schema; receiver identity and assignment revision binding; duplicate/conflict/late-return rules; independently derived complete source manifest; immutable evidence objects; trusted retrieval and hash verification.

Exit: synthetic tests prove tamper, replay, wrong-task, stale-revision, missing-object, manifest omission, late-return and crash recovery are rejected or quarantined.

### Gate 8 — Independent review and human disposition

**Goal:** Separate structural integrity, research correctness, task acceptance and phase-gate authority.

Required: independent source/methodology review criteria; reviewer identity and conflict checks; immutable review record bound to exact return/evidence digests; authenticated append-only human disposition; distinct task acceptance and phase-gate decision; no worker authority over either.

Exit: review and disposition records survive replay/restore and cannot be edited or self-approved by worker, dispatcher, platform administrator, or same reviewer where prohibited.

### Gate 9 — Artifact, monitoring and incident integration

**Goal:** Produce independently verifiable outputs and detect failures without granting action authority.

Required: trusted workflow/run/commit context; clean checkout proof; artifact upload/download verification; independent telemetry and source-health heartbeat; severity/escalation; monitor-of-monitor; privacy-safe notifications; emergency deny-only hold; out-of-band credential containment; tested incident roles/runbooks.

Exit: synthetic artifact round-trip, monitoring outage, compromised identity, and emergency-hold race scenarios pass. Acknowledgement or alert closure never clears a hold.

### Gate 10 — Backup, recovery and continuity

**Goal:** Prove that failure and restore do not lose evidence, roll back authority, or duplicate external work.

Required: component RTO/RPO; common-mode failure map; encrypted/immutable backups; consistent checkpoint across registry, event, witness, approvals, attempts, receipts, returns and evidence; isolated no-egress restore; key/policy revalidation; provider attempt reconciliation; independent recovery review; measured drills.

Exit: synthetic restore/failover evidence meets approved objectives and preserves all invariants. Recovery yields read-only mode; dispatch requires separate authorization.

### Gate 11 — Workflow activation and manual preflight

**Goal:** Resolve actual GitHub activation topology and prove a harmless report-only run.

Required: owner-approved default-branch bridge or separate repository; minimal reviewed workflow; least-privilege effective permission exports; immutable action references; exact handoff permitting validation; isolated manual preflight only; trusted run context and artifact round-trip; independent reviewer sign-off.

Exit: successful report-only synthetic run with no worker dispatch, no research-data mutation, no protected branch write, and externally retained evidence. The inherited Phase 3 workflow is not a substitute and must not be dispatched under the current handoff.

### Gate 12 — Bounded pilot, then unattended automation

**Goal:** Progress from manually supervised synthetic work to approved low-risk work, then separately to scheduled/event-driven operation.

Required: all preceding gates PASS; owner-approved task scope; current handoff; empty/limited allowlist populated only by exact human-approved task digests; budgets/quotas; on-call coverage; kill switch; independent review; measured pilot evidence.

Exit: manual supervised pilot accepted first. Scheduled/event-driven triggers require a separate approval, bounded schedules, event filters, idempotency, quotas, pause behavior, and evidence that missed/duplicate triggers cannot create duplicate work.

## Cross-gate blockers that cannot be waived by convenience

- G0-05 controlling handoff and incomplete independent review.
- No owner decision on repository activation topology.
- No selected/qualified registry backend or independent trust roots.
- No durable trusted package-digest custody.
- No authenticated dispatcher, provider receipts, or return receiver.
- No enforced worker/data sandbox.
- No complete independent evidence manifest/custody.
- No tested backup, witness, recovery, monitoring, or incident control plane.
- No executed tests under a handoff that permits them.

## Work allowed now

Until the handoff changes, continue only non-invasive documentation/static review on the isolated agent branch, and do not create a parallel route around G0-05. The independent Copilot review already requested should be collected and assessed before issuing another review assignment. Do not alter main, create repositories, provision services, change permissions/secrets, access the VPS, dispatch workflows, run scripts/tests, or modify research code/data.

## Status vocabulary

- PASS: exact acceptance evidence independently verified for the defined scope.
- FAIL: evidence demonstrates the criterion is not met.
- UNKNOWN: evidence is absent, incomplete, or cannot be authenticated.
- BLOCKED: a controlling authority, dependency, or safety restriction prohibits progress.
- NOT RUN: validation was not executed; never describe as passing.

Documentation completeness is not implementation readiness. A gate may move to PASS only on independently verifiable evidence, and only the authorized human authority may approve the corresponding transition.

## Current project status

Roadmap committed as planning documentation only. No provider, backend, account, region, credentials, workflow, runner, sandbox, monitoring, backup, or integration was selected or configured. No tests, scripts, workflows, research data, provider calls, VPS actions, deployments, or phase/gate changes were performed. The agent remains non-operational, no unattended work is running, and Phase 3 G0-05 remains controlling.
