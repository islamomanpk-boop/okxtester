# Implementation readiness and exit criteria

## 1. Purpose and authority

This checklist is the consolidated control document for deciding whether the OKX research agent may move from a documented, non-operational scaffold toward a narrowly bounded implementation and, later, controlled activation.

It consolidates the threat model, security gap audit, backend selection framework, registry interface, unified lifecycle transaction specification, activation decision, and current research handoff restrictions.

**This document grants no authority.** It does not approve a backend, create credentials or infrastructure, authorize code/test/workflow execution, permit worker dispatch, enable schedules, close a research gate, or advance a phase. The active Phase 3 G0-05 handoff remains controlling. Where any checklist item conflicts with that handoff, the handoff wins.

Status vocabulary:

- **PASS** — supported by current, reviewable evidence for the exact scope and version.
- **FAIL** — evidence demonstrates the requirement is not met.
- **UNKNOWN** — evidence is missing, incomplete, stale, caller-supplied without independent verification, or not independently reviewed.
- **BLOCKED** — work is prohibited by the current handoff or lacks required owner authorization.

An UNKNOWN is never a PASS. A document describing a control is not evidence that the control is deployed or operating.

## 2. Current readiness snapshot

| Area | Current status | Reason |
|---|---|---|
| Deterministic safety/review primitives | PARTIAL / UNKNOWN | Source and tests are authored; relevant tests have not been run. |
| Assignment and review data contracts | DESIGN PRESENT | Pure modules exist; trusted runtime integration does not. |
| Trusted registry/backend | BLOCKED | No backend selected, implemented, or proven. |
| Independent identity and approval roots | UNKNOWN | No operational identities or approval channel established. |
| Package digest custody | BLOCKED | Package digest is calculated but no trusted dispatcher/registry retains it. |
| Authenticated dispatch and delivery | BLOCKED | No dispatcher, provider integration, or authenticated delivery reconciliation. |
| Durable event log and checkpoint | BLOCKED | Current ledger/persistence modules are pure in-memory primitives. |
| Repository/workflow activation bridge | BLOCKED | Default branch is `main`; isolated agent-branch workflow alone is not dispatchable through workflow_dispatch. No main change is authorized. |
| Runtime validation | BLOCKED | Current G0-05 handoff prohibits relevant scripts, tests, and workflows. |
| Scheduling/event triggers | BLOCKED | No activation approval; agent is not operational. |
| Research authority | BLOCKED | G0-05 remains open/conditional; no candidate, backtest, PnL, strategy, or phase-gate authority. |

This is a conservative design-readiness assessment, not a runtime health report.

## 3. Gate A — research authority and scope

All items must PASS before any research-facing operation is considered.

- [ ] A1. Obtain the current authoritative research handoff from the protected research branch and record its exact commit, path, and content hash.
- [ ] A2. Confirm the handoff explicitly permits the exact proposed operation, files, data, and validation method.
- [ ] A3. Confirm the task is in the agreed phase order: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5.
- [ ] A4. Confirm predecessor gates are human-authorized closed before any later phase is eligible.
- [ ] A5. Confirm task scope and prohibitions are exact, bounded, and hashed; no task can self-grant authority.
- [ ] A6. Confirm no prohibited research execution is hidden in helper scripts, tests, workflow steps, dependencies, or subprocesses.
- [ ] A7. Confirm task acceptance, research-gate closure, and phase advancement are separate human decisions.

**Current result: BLOCKED.** The active G0-05 handoff prohibits the relevant scripts, tests, and workflows and does not authorize candidate generation, backtesting, PnL conclusions, strategy selection, gate closure, or phase advancement. No agent path may bypass it.

Required evidence: exact handoff revision and independent supervisor sign-off for the proposed operation. A stale or superseded handoff is not sufficient.

## 4. Gate B — owner decisions before backend implementation

These are decisions for the project owner; a technical recommendation is not a selection.

- [ ] B1. Repository topology: separate agent repository, or an explicitly reviewed minimal activation bridge in the existing repository's default branch.
- [ ] B2. Hosting and trust boundary: approved service/runtime boundary and administrative ownership.
- [ ] B3. Human authority roles: who may approve, revoke, accept task returns, and close research gates; how each identity is authenticated.
- [ ] B4. Approval channel: independent of worker-controlled queue fields, workflow inputs, and worker returns.
- [ ] B5. Data residency, privacy, retention, and permitted evidence content.
- [ ] B6. Budget and cost ceilings for storage, compute, workflow minutes, provider calls, logs, and backups.
- [ ] B7. Worker provider and delivery contract: documented idempotency-key scope, retention window, exact replay/body-mismatch semantics, authenticated receipts/callbacks, authoritative query/absence semantics, status consistency, and cancellation behavior.
- [ ] B8. Independent checkpoint/anti-rollback witness and administrative separation.
- [ ] B9. Recovery objectives: approved RPO/RTO, backup frequency, restore test cadence, and incident owner.
- [ ] B10. Trusted workflow identity: repository, workflow path, immutable workflow revision, run identity, actor identity, and checkout commit derivation.
- [ ] B11. Canonicalization contract for future v2 events, including explicit version and cross-language test vectors. Existing v1 event hashes and semantics remain immutable.
- [ ] B12. Operational owner and independent reviewer for every readiness gate.
- [ ] B13. Independent deny-only emergency hold, credential-containment path, and external incident audit destination.
- [ ] B14. Two-human resume quorum with distinct subject identities and independently administered credential/recovery paths; neither approver may hold a conflicting incident/recovery/reviewer/witness/deployment role.
- [ ] B15. Restricted deny-only approval-revocation lane is separately authorized, atomic, witnessed, and incapable of granting authority or clearing the emergency hold.

**Current result: UNKNOWN / BLOCKED.** No provider, region, account, database, credential, approval service, checkpoint witness, or repository topology has been selected or provisioned.

Required evidence: dated owner decision record, options considered, rejected alternatives, accountable owner, and independent review. Do not silently infer decisions from a design recommendation.

## 5. Gate C — independent trust roots and identity

- [ ] C1. Human approval identity is independently authenticated and cannot be asserted by the worker or dispatcher payload.
- [ ] C2. Dispatcher identity is workload-authenticated and limited to exact approved operations.
- [ ] C3. Registry identity and authorization policy are independent from worker-controlled inputs.
- [ ] C4. Workflow identity is derived from authenticated platform context, not user-supplied run metadata.
- [ ] C5. Worker identity and provider delivery receipts are authenticated; untrusted worker claims remain declarations.
- [ ] C6. Evidence storage and integrity verification are independently protected from the worker.
- [ ] C7. Checkpoint witness is outside the registry's sole administrative rollback domain.
- [ ] C8. Reviewer identity and human disposition are authenticated and auditable.
- [ ] C9. Trust-root administrators, credentials, and recovery procedures are documented with separation of duties.
- [ ] C10. Revocation and credential-compromise procedures are tested before operational use.
- [ ] C11. Emergency credential containment remains possible during registry freeze without mutating frozen registry history; affected approvals remain denied/UNKNOWN until append-only revocation events are witnessed.
- [ ] C12. Resume quorum is tested against common identity-provider/root recovery compromise and role-conflict/self-approval.
- [ ] C13. The emergency revocation lane accepts only exact existing approval revocations/invalidation and cannot perform any positive authorization or unrelated lifecycle transition.

Required evidence: identity architecture, trust-boundary diagram, role/permission matrix, provider documentation, authentication configuration, negative authorization tests, and independent security review.

A caller-supplied field such as `actor`, `approved_by`, `workflow_sha`, `checkout_clean`, or `delivery_confirmed` is not trusted evidence merely because it appears in a valid JSON object.

## 6. Gate D — trusted registry and transaction semantics

- [ ] D1. One authoritative registry owns assignment revisions, package bytes/digests, approvals/revocations, dispatch attempts, delivery records, returns, reviews, human dispositions, event sequence, materialized state, and protected checkpoint.
- [ ] D2. Existing v1 event ledger remains immutable legacy evidence; no silent schema or hash migration.
- [ ] D3. Future v2 schema has explicit versioning, closed event types and payload schemas, canonicalization version, and independent shared test vectors.
- [ ] D4. Global registry checkpoint/version and per-assignment state version are both checked and advanced atomically.
- [ ] D5. Assignment state, event append, delivery idempotency index, and checkpoint update commit in one transaction or a separately proven equivalent protocol.
- [ ] D6. Replay lookup occurs before stale-checkpoint rejection; exact replay returns the original receipt.
- [ ] D7. Reuse of an idempotency identity with different normalized facts is rejected.
- [ ] D8. Provider delivery identity and event-level idempotency identity are distinct, documented, and uniquely constrained.
- [ ] D9. Package canonical bytes and dispatcher-computed digest are retained before dispatch in a trusted store.
- [ ] D10. Approval is operation-bound and rechecked for scope, expiry, revocation, handoff revision, workflow identity, task digest, branch, and input commit at the protected operation boundary.
- [ ] D11. Cancellation, revocation, dispatch, and delivery races have explicit serializable outcomes.
- [ ] D12. No external delivery is retried automatically while delivery is pending or uncertain.
- [ ] D13. Error taxonomy distinguishes conflict, exact replay, permanent denial, transient failure, and uncertain commit outcome.
- [ ] D14. Backup/restore preserves event chain, idempotency indexes, package objects, assignment state, and checkpoint consistently.
- [ ] D15. Rollback/restore is detected using an independent monotonic witness or equivalent proof.

Required evidence: selected backend's documented transaction guarantees, schema and constraints, conformance tests using synthetic data, concurrency/race test results, replay tests, restore evidence, and independent reviewer approval. A product feature list or vendor marketing page is insufficient.

## 7. Gate E — assignment, dispatch, return, and review integrity

- [ ] E1. Assignment package is rebuilt from the trusted task and current preflight result.
- [ ] E2. Exact package bytes and digest are retained by the trusted registry before delivery.
- [ ] E3. Dispatch requires a distinct, authenticated, operation-bound approval.
- [ ] E4. Dispatch attempt retains the exact provider key, full provider-defined key scope, provider qualification version, immutable request-envelope digest/reference, and durable provider-delivery record.
- [ ] E5. Delivery confirmation is backed by authenticated provider receipt/query evidence bound to attempt, key scope, and exact request digest, with signature/transport provenance and monotonic status handling.
- [ ] E6. Timeout, missing response, missing artifact, or worker silence is classified as pending/uncertain—not proof of non-delivery.
- [ ] E17. Provider idempotency retention exceeds the bounded reconciliation horizon with a safety margin; after possible expiry the system queries only and never resubmits.
- [ ] E18. Provider lookup documents visibility delay and authoritative absence semantics; transient not-found cannot be treated as non-delivery.
- [ ] E19. No provider request bytes leave the dispatcher before the atomic dispatch_started commit; post-commit submission uses the exact retained request envelope.
- [ ] E20. Provider acceptance followed by dispatcher crash before receipt persistence is recoverable through authenticated query/history by the original provider key/job ID; callback-only providers without a durable inbox are rejected.
- [ ] E21. Provider observation identity is distinct from delivery/command/witness identities; raw observation, immutable facts digest, observation index, state projection, event, checkpoint, and witness outbox commit atomically.
- [ ] E22. Crash injection proves safe recovery at every boundary: dispatch commit, request transmission, provider acceptance, response receipt, observation commit, external witness publish/ack, and client response; exact retries never create duplicate jobs/events.
- [ ] E7. A return is bound to the exact assignment revision and independently retained package digest.
- [ ] E8. Worker-submitted evidence references are checked against independently derived checkout commit and file manifest.
- [ ] E9. Downloaded artifact identity, provider run identity, expected run/attempt, file set, and hashes are verified.
- [ ] E10. Evidence-byte integrity is not represented as source truth, research correctness, or task completion.
- [ ] E11. Structural review and evidence verification failures stop or return the submission for revision.
- [ ] E12. Human task disposition is authenticated and bound to the exact review/assignment.
- [ ] E13. Phase-gate closure and phase advancement require separate authority and remain prohibited unless the research handoff permits them.

Required evidence: end-to-end synthetic lifecycle traces, tamper tests, duplicate-return tests, wrong-assignment tests, provider receipt validation, and independent review. No real research task is needed for these proofs.

## 8. Gate F — workflow, repository, and runner security

- [ ] F1. Repository topology and default-branch activation mechanism are approved before workflow implementation.
- [ ] F2. Any workflow-dispatch entrypoint exists on the actual default branch; an isolated branch-only workflow is not assumed dispatchable.
- [ ] F3. Workflow source is pinned to reviewed immutable commit identities where supported; third-party actions are pinned to full commit SHAs.
- [ ] F4. Workflow permissions are explicitly minimal at workflow and job level.
- [ ] F5. No inherited research workflow is reused or dispatched as an agent activation shortcut.
- [ ] F6. Workflow inputs are identifiers only; they cannot grant authority or override trusted policy.
- [ ] F7. Checkout repository, ref, commit SHA, cleanliness, workflow path/SHA, run ID, attempt, and actor are derived from authenticated runtime context.
- [ ] F8. No self-hosted/VPS runner is used unless separately threat-modelled, approved, isolated, and independently validated.
- [ ] F9. Secrets are least-privilege, short-lived where possible, scoped to exact environments, and unavailable to untrusted pull requests/worker content.
- [ ] F10. Dependency versions, provenance, supply-chain policy, and update process are reviewed.
- [ ] F11. Artifacts are uploaded only after schema/provenance checks and are downloaded/reverified before acceptance.
- [ ] F12. Logs redact secrets and sensitive market/user data while retaining audit evidence.
- [ ] F13. Concurrency groups, rate limits, maximum batch size, timeouts, and cost ceilings are enforced.
- [ ] F14. Workflow cancellation and partial failure leave recoverable, unambiguous registry state.
- [ ] F15. Manual preflight/report-only readiness is reviewed before any dispatch-capable workflow is considered.
- [ ] F16. Scheduled and event-driven triggers require separate approval after manual operation is proven.

**Current result: BLOCKED.** The repository default branch is `main`. The agent branch is isolated, and no main-branch activation bridge or separate agent repository has been approved. No agent workflow is active. Existing research workflows are not an acceptable workaround.

Required evidence: reviewed workflow diff, immutable action references, permissions audit, authenticated context tests, runner isolation evidence, artifact verification evidence, and explicit owner approval for the chosen topology.

## 9. Gate G — runtime validation and failure injection

Validation may begin only when the active handoff explicitly permits the exact test scope.

- [ ] G1. Static review is complete and records exact reviewed commit and files.
- [ ] G2. Unit tests execute in an isolated environment against synthetic fixtures only.
- [ ] G3. Integration tests use a non-production backend/account and synthetic task/evidence content.
- [ ] G4. Concurrent update tests prove global and per-assignment compare-and-swap behavior.
- [ ] G5. Duplicate delivery/replay tests prove exactly-once logical effects under repeated requests.
- [ ] G6. Lost response and uncertain commit tests prove no unsafe retry.
- [ ] G11. Provider key scope/retention, same-key changed-body behavior, expired-key handling, stale/not-found queries, authenticated webhook replay, and out-of-order status observations pass synthetic tests.
- [ ] G12. Provider-acceptance/lost-receipt and every dispatcher/registry/witness crash point pass synthetic restart and idempotent-replay tests.
- [ ] G7. Cancellation/revocation races prove no operation proceeds after authorization is invalidated.
- [ ] G8. Tampered package, evidence, manifest, artifact, workflow identity, and checkpoint tests fail closed.
- [ ] G9. Backup rollback and restore tests prove anti-rollback and consistency.
- [ ] G10. Malformed JSON, duplicate keys, non-finite numbers, path traversal, symlink escape, and schema drift tests fail closed.
- [ ] G11. Independent reviewer inspects test design, results, and retained evidence.
- [ ] G12. Test report clearly separates authored tests, executed tests, passing tests, skipped tests, and failures.

Required evidence: reproducible commands, environment identity, exact commit, test output, fixture provenance, failure-injection results, and independent review. A test count in documentation is not proof tests passed.

**Current result: BLOCKED.** Regression tests are authored but have not been executed because the current G0-05 handoff prohibits relevant validation.

## 10. Gate H — operations and production readiness

These items apply only after the earlier gates pass and an explicitly approved limited pilot exists.

- [ ] H1. Named operational owner and on-call/escalation path.
- [ ] H2. Monitoring for queue age, workflow failures, registry conflicts, delivery uncertainty, artifact verification failures, and budget consumption.
- [ ] H3. Alerts for unauthorized access, stale/revoked approvals, checkpoint mismatch, event-chain break, and unexpected phase/task activity.
- [ ] H4. Documented incident response, independent emergency hold, credential revocation, worker suspension, and safe shutdown.
- [ ] H13. Emergency freeze, out-of-band credential containment, delayed registry revocation, independent resume quorum, and audit export have passed approved synthetic incident exercises.
- [ ] H5. Tested backup/restore and disaster recovery with approved RPO/RTO.
- [ ] H6. Bounded retention, deletion, and access-review policy.
- [ ] H7. Rate, concurrency, runtime, retry, and cost ceilings enforced in trusted policy.
- [ ] H8. Periodic independent access, workflow, dependency, and trust-root review.
- [ ] H9. Change management for policy, task definitions, handoffs, workflow revisions, schemas, and backend migrations.
- [ ] H10. Separate approval for any expansion from manual pilot to event-driven or scheduled operation.
- [ ] H11. Safe shutdown leaves no pending delivery or ambiguous state silently retried.
- [ ] H12. Operational metrics do not reward task completion at the expense of research correctness or safety.

Required evidence: runbooks, alert tests, incident exercise, restore evidence, budget controls, access review, and signed pilot acceptance.

## 11. Required evidence register

Every gate decision must have a durable record containing:

| Field | Requirement |
|---|---|
| Gate and control IDs | Exact checklist references |
| Decision | PASS, FAIL, UNKNOWN, or BLOCKED |
| Scope | Repository, branch, workflow/backend version, task/phase, and operation |
| Evidence | Immutable URLs/IDs, commit SHA, artifact digest, or test report |
| Evidence origin | Authenticated source and retrieval method |
| Reviewer | Named accountable independent reviewer |
| Owner | Person accountable for remediation/decision |
| Date | UTC decision timestamp |
| Expiry/recheck | When evidence becomes stale or must be revalidated |
| Exceptions | Explicit scope, reason, approver, expiry, and compensating control |

A gate cannot PASS if required evidence is missing, unauthenticated, stale, or reviewed only by its author. Exceptions cannot override the research handoff or any non-waivable prohibition.

## 12. Ordered exit criteria

The order below is a dependency sequence, not an authorization to proceed.

1. **Design freeze:** reconcile contracts and this checklist; mark unresolved contradictions and owner decisions.
2. **Owner decisions:** select repository topology, trust domains, identities, approval channel, backend evaluation criteria, delivery provider, checkpoint witness, retention, and budget.
3. **Proof of capability:** compare backend candidates using synthetic data only; prove atomicity, concurrency, idempotency, authenticated identity, and anti-rollback without research data or production credentials.
4. **Independent design review:** review threat model, data model, trust roots, provider guarantees, and failure oracles.
5. **Implementation authorization:** obtain explicit authorization for exact files, environment, tests, and workflow scope, and confirm the current research handoff permits it.
6. **Isolated implementation and validation:** implement only the approved scope; run synthetic unit/integration/failure tests only when authorized.
7. **Manual readiness workflow:** separately review default-branch topology, immutable workflow identity, minimal permissions, runner isolation, and artifact verification. Preflight/report-only first.
8. **Limited pilot decision:** require independent evidence review and explicit human approval before any worker dispatch.
9. **Event-driven/scheduled decision:** separate approval after manual pilot evidence; enforce quotas, monitoring, rollback, and shutdown.
10. **Research task authorization:** each research task still requires its own exact handoff, task approval, phase eligibility, and human completion/gate decisions.

## 13. Non-negotiable stop conditions

Stop and return to human review if any of the following occurs:

- The active handoff is missing, changed, ambiguous, or prohibits the operation.
- Task, assignment, package, workflow, checkout, or evidence identity cannot be independently verified.
- Approval is stale, revoked, incorrectly scoped, or cannot be authenticated.
- Registry checkpoint, event chain, state version, idempotency index, or backup witness conflicts.
- Delivery is pending or uncertain and cannot be reconciled.
- A replay uses the same idempotency identity with different facts.
- A worker claims gate closure, phase advancement, strategy approval, PnL success, or authority it does not possess.
- Evidence bytes or artifact provenance do not match the trusted source.
- A required trust root shares an unreviewed administrative/control domain with the component it is meant to constrain.
- A proposed workaround touches protected research branches, default-branch activation, secrets, permissions, VPS, self-hosted runners, or production resources without explicit approval.
- Any validation would violate the active handoff.

## 14. Current conclusion

The project has a substantial documented safety and review foundation, but it is **not implementation-ready for a trusted operational control plane and is not operational**. The largest remaining blockers are owner decisions, independent trust roots, a transactional registry and protected checkpoint, retained package digest custody, authenticated approval/dispatch/delivery, the default-branch activation topology, and authorized independent runtime validation.

The immediate safe work is limited to documentation reconciliation and static planning on `agent/okx-research-agent-v1`. Do not create a repository, change `main`, alter the protected research branch, enable workflows, provision credentials/resources, use the VPS/self-hosted runner, or run tests/scripts/workflows under the current restrictions.

No backend is selected. No operational workflow is active. No worker is dispatched. No research task is executed. The G0-05 handoff remains authoritative.


## 12. Worker execution isolation and resource limits — mandatory pre-dispatch gate

The worker runtime is a separate high-risk trust boundary. Identity separation and a container label are not proof of sandbox isolation. Before any worker dispatch, the selected runtime must independently demonstrate the controls in [Worker execution isolation and resource-limits audit](WORKER_EXECUTION_ISOLATION_AND_RESOURCE_LIMITS_AUDIT_2026-11-27.md): disposable per-assignment strong isolation; non-root/no capabilities/no host mounts or sockets; exact read-only input allowlist; no ambient or long-lived secrets; deny-all network with approved proxy-only exceptions; fixed immutable runtime/dependency provenance; hard externally enforced CPU/memory/PID/disk/time/network/output/concurrency/cost limits; separate artifact inspection; trusted telemetry, kill/fence, host quarantine, and verified cleanup.

Required evidence includes effective runtime configuration, negative tests for host/credential/metadata/internal-network access, filesystem escape and privilege escalation, cross-assignment contamination, egress bypass, resource exhaustion, kill-switch races, artifact attacks, and cleanup. Tests must use synthetic fixtures and disposable infrastructure, and require separate authorization after the active research handoff permits the exact validation. Until independently reviewed evidence exists, worker isolation and resource limits are UNKNOWN/BLOCKED and dispatch is prohibited.


## 13. Evidence custody, independent review, and human acceptance — mandatory pre-acceptance gate

Before any worker return can be treated as eligible for human task acceptance, the future system must satisfy [Evidence-pipeline integrity and human-acceptance audit](EVIDENCE_PIPELINE_INTEGRITY_AND_HUMAN_ACCEPTANCE_AUDIT_2026-11-27.md). Minimum requirements: authenticated raw-byte receipt and immutable custody before parsing; receiver-generated digest and idempotency; trusted assignment/attempt/package binding; authenticated workflow and clean-checkout provenance; independently derived complete/versioned commit manifest; immutable evidence objects and separate report artifacts; authenticated artifact/run association; reviewer read-only access and append-only review record; and human disposition bound to exact return, evidence-set, review, assignment and handoff digests. Retention, encryption/key custody, data residency, and access policy must be owner-approved.

Evidence-byte equality is not source authenticity, research correctness, or task completion. Worker status and source references remain declarations. A human task acceptance must not imply phase-gate closure; gate closure remains a separate authority and event. Until every required control is independently implemented and validated, evidence custody and human acceptance are UNKNOWN/BLOCKED. The active G0-05 handoff continues to prohibit execution and validation work that it does not expressly permit.


## 14. Control-plane authorization and effective permissions — mandatory pre-activation gate


## 15. Operational observability and incident detection — mandatory pre-activation gate


## 16. Software supply-chain and build provenance — mandatory pre-activation gate


## 17. Research-data integrity, access control and privacy — mandatory pre-activation gate

Before any worker receives research data, satisfy [Research-data integrity, access-control and privacy audit](RESEARCH_DATA_INTEGRITY_ACCESS_CONTROL_AND_PRIVACY_AUDIT_2026-11-27.md). Required evidence includes: owner-approved data inventory/classification; exact task/assignment-bound object manifests; independent default-deny authorization; per-assignment isolated read-only mounts or object capabilities; immutable source snapshots and receiver-side digests; verified database snapshot/journal behavior; complete parent-to-derived lineage; purpose-based privacy review and field minimization; quarantined output parsing and promotion; cross-assignment isolation and cleanup proof; no ambient credentials or unrestricted egress; audited access, retention, deletion, backup and legal-hold policy; and synthetic negative tests for path escape, mutation, exfiltration, privacy leakage, and restore divergence.

A task description, repository checkout, path convention, application-level read-only flag, worker-reported hash, or successful checksum against a caller-supplied manifest is not sufficient authorization or proof of source custody. Unknown data owner, origin, classification, privacy obligation, snapshot consistency, access identity, or lineage is UNKNOWN/BLOCKED. Workers cannot alter source evidence, widen access, promote outputs, or delete protected records.

**Current result: UNKNOWN / BLOCKED.** No live data catalog, classification, access broker, immutable evidence store, database snapshot service, privacy/retention policy, region, or storage provider is selected or configured. No research datasets, database, or VPS data were accessed or changed. No code, tests, scripts, workflows, permissions, credentials, or integrations were changed or run. The agent remains non-operational and G0-05 remains controlling.

Before building, promoting, or starting any worker image or workflow, satisfy [Software supply-chain and build-provenance audit](SOFTWARE_SUPPLY_CHAIN_AND_BUILD_PROVENANCE_AUDIT_2026-11-27.md). Required evidence includes: complete direct/transitive dependency and tool inventory; platform-specific hash-locked dependencies; owner-approved package-source policy; isolated least-privilege builder; immutable source/build/base-image/action references; signed provenance tied to exact source, lock, materials, builder and output digest; complete SBOM; independently governed signing and revocation roots; vulnerability and malicious-package policy; immutable release records; cache and registry integrity; runtime verification of the exact approved image/action/policy digests; and synthetic negative tests for tampering, substitution, compromised signing roots, poisoned caches, and runtime drift.

A version string, unsigned SBOM, worker assertion, mutable tag, hash without authenticated provenance, or scanner result alone is insufficient. Unknown dependency, builder, signer, provenance, scanner, image, or workflow identity is UNKNOWN/BLOCKED. No worker may install packages, alter its runtime, sign artifacts, publish images, or promote releases. Supply-chain quarantine/revocation must not grant dispatch, retry, rollback, or resume authority.

**Current result: UNKNOWN / BLOCKED.** No complete dependency lock, package-source policy, builder, SBOM, provenance signer, vulnerability scanner, approved image, release registry, or deployment verifier is selected or configured. No dependencies or workflow references were changed; no package installation, build, scan, signature verification, tests, scripts, workflows, network calls, or deployments were performed. The agent remains non-operational and G0-05 remains controlling.

Before any manual operation or unattended execution is considered, satisfy [Operational observability and incident-detection audit](OPERATIONAL_OBSERVABILITY_AND_INCIDENT_DETECTION_AUDIT_2026-11-27.md). Required evidence includes: an owner-approved telemetry inventory and source-health heartbeat for every critical producer; closed, versioned alert taxonomy and objective severity rules; immutable identity-bound correlation and replay/conflict detection; bounded state timers that preserve UNKNOWN and never trigger retries; independently administered SEV-0/SEV-1 notification routes with authenticated delivery receipts and documented human coverage; append-only acknowledgement, escalation, suppression, and closure records; independent monitoring integrity, retention, clock, and configuration-change controls; tested secret/data minimization; evidence-preserving incident runbooks with role separation; and synthetic coverage demonstrating that monitoring has no protected-action authority.

Monitoring failure, missing telemetry, untrusted clocks, unavailable notification routes, or unknown incident ownership is UNKNOWN/BLOCKED, not healthy. Alert acknowledgement or closure must never clear an emergency hold, restore approval, authorize dispatch, change task state, or close a research gate. Emergency freeze and credential containment remain separate independently authenticated capabilities. Emergency resume remains read-only/non-dispatching; normal activation is separate.

**Current result: UNKNOWN / BLOCKED.** No monitoring provider, log/metrics store, alert manager, notification destination, on-call rotation, incident platform, telemetry policy, retention schedule, or recipient is selected or configured. No live telemetry or permissions were inspected. No monitoring integrations, rules, credentials, workflows, tests, scripts, or notifications were created or run. The agent remains non-operational and G0-05 remains controlling.

Before any privileged control-plane operation or GitHub activation, independently satisfy [Control-plane authorization and permission-model audit](CONTROL_PLANE_AUTHORIZATION_AND_PERMISSION_MODEL_AUDIT_2026-11-27.md). Required evidence includes: a closed deny-by-default operation/resource matrix; stable authenticated identities and common-root-aware role-conflict checks; canonical transaction-bound authorization decisions; exact approval/task/assignment/package/workflow/handoff/policy/checkpoint binding; effective organization/repository/workflow/app/runner/environment/secret/branch-rule permission exports; independently audited policy changes; bounded emergency freeze/containment/revocation/witness/break-glass/resume capabilities; session assurance and revocation propagation; independent audit telemetry; and negative authorization tests for every prohibited role/resource/operation combination.

Emergency resume may restore only a read-only, non-dispatching state. It must not enable schedules, provider calls, worker dispatch, research operations, or gate changes. Normal activation is separate and requires all readiness gates plus a then-current handoff authorizing the exact scope. Platform administration, merge rights, workflow dispatch rights, or artifact access do not imply human research authority. Any unresolved common-root conflict, inherited permission, stale policy, unknown identity, or missing effective-permission evidence is UNKNOWN/BLOCKED.
