# Architecture dependency and integration-gap audit — 2026-11-27

## Scope and authority

Static, documentation-only review of the agent modules and contracts on `agent/okx-research-agent-v1`. This audit distinguishes implemented pure functions, in-memory composition, documented future contracts, and absent operational adapters. It does not run tests/scripts/workflows, inspect live services, access research datasets, provision resources, or change permissions. The active Phase 3 G0-05 handoff remains controlling.

## Executive result

The repository contains a meaningful deterministic scaffold, but not an operational agent. The strongest integration today is an in-memory, non-dispatching path from trusted queue snapshot through preflight, batch planning, assignment packaging, return review, and report construction. Event, persistence, recovery, evidence and review components are mostly pure functions whose security depends on future callers and adapters.

The principal architectural gap is not another isolated helper. It is the absence of a trusted runtime boundary that authenticates inputs, retains immutable state, atomically authorizes protected transitions, performs bounded delivery, receives authenticated returns, and independently records evidence. Wiring the current functions together without those trust roots would create an attractive but unsafe appearance of end-to-end operation.

## Integration map

| Layer | Present component(s) | Current connection | Missing operational dependency |
|---|---|---|---|
| Policy and task definitions | config, safety_controller | Fixed-file task/policy evaluation | Authenticated policy publisher, versioned approvals, effective permission proof |
| Preflight and planning | task_runner, batch_planner | Queue snapshot → non-authorizing preflight → plan | Authorized positive readiness semantics; no live dispatch authority |
| Coordination/package | orchestration_coordinator, assignment_package | In-memory plan → prepared package | Durable registry and independent package-digest custody |
| Worker delivery | none | Not connected | Authenticated dispatcher, provider contract, operation-bound approval |
| Worker isolation | design documents only | No runtime connection | Disposable sandbox, data grants, resource/egrss enforcement |
| Return receipt | assignment_return | Parsed return + caller-supplied expected digest | Authenticated raw-byte receiver, durable receipt, trusted digest lookup |
| Evidence verification | evidence_verifier | Bytes checked against caller-supplied manifest | Independently derived commit/object manifest and immutable evidence store |
| Structural/research review | supervisor_review, review_pipeline | Structure then evidence-integrity checks | Trusted source validation and independent human reviewer workflow |
| Human disposition | documented contract | No operational write path | Authenticated append-only decision bound to exact review/evidence revision |
| Reports/artifacts | report_builder, artifact_preparation, review_artifact | In-memory three-file bundles | Trusted workflow context, authenticated uploader/store, retention and access controls |
| Event history | event_ledger | Pure hash-chain validation | Authenticated event source, durable atomic append, protected head and witness |
| Persistence/concurrency | persistence_contract | In-memory optimistic preparation | Transactional backend, global/per-assignment CAS, unique indexes |
| Recovery | recovery_policy | Advisory classification | Authenticated observations, reconciled provider state, durable lifecycle state |
| Monitoring/continuity | design documents | No operational connection | Independent telemetry, alert routes, backup/restore, on-call and runbooks |

## Findings

### INT-01 — The in-memory orchestration path is not a trusted transaction (P0)

The coordinator composes queue/preflight/planning/package/recovery views, but does not atomically reserve an assignment, retain its package digest, or commit a state transition. A caller can observe a plan that becomes stale immediately. Required: a trusted registry transaction that revalidates task, handoff, policy, phase, approval, and assignment revision at the protected operation boundary.

### INT-02 — Authorization semantics and readiness semantics are conflated (P0)

The current safety controller intentionally denies execution while execution switches are off and the allowlist is empty. The batch planner therefore cannot produce an allowed assignment under current configuration. A future readiness-only inspection must be explicitly non-authorizing and must never be reinterpreted as dispatch permission. Do not enable execution switches to make a readiness report appear positive.

### INT-03 — Package digest custody is not connected (P0)

The package builder calculates a digest and the return reviewer expects an independently retained digest, but no trusted dispatcher/registry stores and later retrieves that value. Required: immutable package bytes/digest, task revision, handoff, workflow/run and delivery identity committed before dispatch; worker content cannot supply the expected digest.

### INT-04 — No authenticated dispatcher or delivery provider exists (P0)

No operation-bound approval, workload identity, provider adapter, exact request envelope, idempotency contract, durable attempt record, or authenticated delivery receipt is wired. Required: dispatch-start linearization transaction, provider-specific key scope/retention/query guarantees, signed receipt or authenticated status observation, and no automatic retry under uncertainty.

### INT-05 — Return review starts after trust-sensitive parsing (P0)

The current return API receives a parsed dictionary and caller-supplied package digest. It does not establish who sent the bytes, when they arrived, whether bytes were altered, or whether a receipt was durably recorded before parsing. Required: authenticate transport/raw bytes, persist receiver identity + raw digest + stable receipt ID + assignment binding before parsing, then apply strict UTF-8/JSON and replay/late-arrival rules.

### INT-06 — Evidence verifier does not establish manifest authenticity or completeness (P0)

It verifies bytes against a caller-supplied manifest and commit context. That is a useful pure primitive, not proof that the manifest covers all required files or came from the trusted commit tree. Required: workflow-derived commit/tree identity, independently generated complete object manifest, exact object semantics, immutable evidence custody, and authenticated retrieval.

### INT-07 — Structural validity can be mistaken for research correctness (P0)

Supervisor review validates submission structure, declared actions, and safety claims. Evidence hash agreement proves only byte equality against supplied facts. Neither establishes source truth, methodology correctness, completeness, or research conclusion validity. Required: independent research review criteria and human reviewer evidence bound to exact immutable source/evidence revisions.

### INT-08 — Human acceptance is not a durable integrated transition (P0)

No operational identity-bound append-only path connects reviewer decision to exact return, evidence-set digest, review result, task revision, and handoff. Task acceptance must remain distinct from G0-05 closure and phase advancement. Required: authenticated disposition transaction with immutable reviewer identity, decision, rationale, timestamp, and exact reviewed digests.

### INT-09 — Artifact generation is in-memory and uploader trust is external (P1)

The builders create and verify a fixed three-file bundle, but do not write, upload, authenticate the artifact service, or enforce retention/access. Required: future workflow obtains trusted GitHub context, verifies clean exact checkout, uploads complete bundle, downloads it, verifies actual run/task/commit context, and retains independent upload/retrieval evidence.

### INT-10 — Event and registry lifecycle are not one atomic durable system (P0)

The event ledger and persistence contract are pure. No source authentication, database transaction, protected checkpoint, uniqueness index, or external witness integration exists. Required: atomic event + materialized state + idempotency index + checkpoint update, with external witness outbox/receipt protocol and fail-closed reconciliation.

### INT-11 — Recovery policy consumes observations it cannot authenticate (P0)

The recovery classifier is advisory. It cannot determine whether a provider accepted a request, whether cancellation/revocation won a race, or whether a return is authentic. Required: derive recovery state only from registry records and authenticated provider/receiver receipts; UNKNOWN remains a hold, not a retry instruction.

### INT-12 — Worker sandbox and data-access policy are not enforceable yet (P0)

Isolation, exact-object data grants, read-only snapshots, network denial, resource ceilings, output quarantine and cleanup are design requirements only. Required: independently configured runtime controls and negative synthetic validation before any worker receives data or executes.

### INT-13 — Monitoring, backup and disaster recovery have no live control plane (P1)

Observability and continuity audits define controls, but no telemetry provider, alert route, backup inventory, restore test, RTO/RPO or recovery roster is configured. Required: owner decisions, independent trust domains, evidence-preserving runbooks and synthetic drills before pilot.

### INT-14 — Workflow activation topology remains blocked (P0)

The agent workflow is isolated on a non-default branch; same-repository manual dispatch requires a workflow on `main`. No separate repository or main-branch bridge is approved. The inherited research workflows are not a substitute and must not be dispatched under G0-05. Required: explicit owner topology decision and separately reviewed minimal activation path, after handoff permits validation.

### INT-15 — Independent review and validation are still outstanding (P0)

The Copilot G0-05 review is not evidenced as complete, and authored tests remain unexecuted. Required: receive and reconcile independent review, then wait for explicit handoff permission before any exact validation scope. Do not claim test coverage as test success.

## Dependency order — safest integration sequence

1. **Authority and evidence freeze:** obtain the current handoff, reconcile independent G0-05 review, and preserve phase order. No code/test/workflow execution while prohibited.
2. **Owner decisions:** choose repository topology, trust domains, identity/approval model, data classification, retention/residency, recovery objectives, budget, and independent witness requirements.
3. **Trusted data and evidence foundation:** define exact object manifests, immutable source snapshots, access broker, lineage, privacy rules, and output quarantine.
4. **Registry and event transaction:** select backend only after qualification; implement authenticated event intake, immutable assignment/package/approval records, atomic state/idempotency/checkpoint writes, and independent witness reconciliation.
5. **Authorization and dispatcher:** implement operation-bound approvals, exact task/handoff/phase revalidation, dispatch-start linearization, provider-specific idempotency and authenticated receipt reconciliation.
6. **Worker runtime:** implement disposable per-assignment isolation, read-only data grants, deny-all egress, resource limits, telemetry, kill/fence, and verified cleanup.
7. **Return receiver and evidence custody:** authenticate raw bytes, durable receipt before parse, replay/late-return rules, independent manifests, immutable objects, and assignment-bound evidence.
8. **Review and human disposition:** separate structural checks, research correctness review, task acceptance, and phase-gate authority; persist each as distinct authenticated events.
9. **Artifact and observability integration:** workflow-derived provenance, verified upload/download, independent monitoring, incident response, backups and restore drills.
10. **Activation:** resolve default-branch topology; manual preflight/report-only first, only after exact handoff permission and independent validation.
11. **Unattended triggers:** schedule/event-driven operation is a later, separate approval after manual operation, recovery, security and budget controls pass.

This is a dependency graph, not authorization to start the next phase.

## Integration acceptance criteria

A future end-to-end synthetic integration is acceptable only when it demonstrates all of the following with independently retained evidence:
- exact task/handoff/policy/phase and immutable package digest binding;
- authorization checked at the operation boundary and revocation/cancellation race-safe;
- atomic registry/event/idempotency/checkpoint state with external witness acknowledgment;
- one logical delivery under duplicate requests, and no unsafe retry under uncertain provider outcome;
- authenticated raw return receipt and assignment-bound immutable evidence;
- manifest completeness and byte integrity against independently derived source;
- separate structural review, research correctness review, task acceptance and gate closure;
- complete artifact round-trip verification against trusted workflow context;
- isolated worker with exact read-only data access, no ambient secrets, deny-all egress, hard resource limits;
- restore and witness reconciliation with no rollback, evidence loss, or duplicate provider attempt;
- independent monitoring, alerting, incident hold and read-only recovery;
- explicit proof that no phase/gate/task authority was inferred from a worker or artifact.

## Current status and non-claims

This is a static architecture audit. No modules were executed, no tests/scripts/workflows run, no services or providers contacted, no research data accessed, no permissions/secrets altered, and no infrastructure created. No end-to-end integration is operational. The agent remains non-operational; no unattended work is running. G0-05 remains controlling and prohibits the relevant validation/execution scope.
