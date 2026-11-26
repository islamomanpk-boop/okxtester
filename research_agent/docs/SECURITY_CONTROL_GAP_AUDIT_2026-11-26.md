# Security control gap audit — 2026-11-26

## Status and authority

**Static design/source audit only.** This document compares the threat model, future lifecycle specifications, and current pure Python modules. It does not execute code, tests, scripts, workflows, or failure injections and does not authorize implementation or activation.

The Phase 3 G0-05 handoff remains controlling. No protected research branch, research data/definitions, default branch, permissions, secrets, VPS, or runner configuration is changed by this document.

This is a bounded source review, not a security certification or a complete audit of every workflow, dependency, deployment setting, GitHub permission, or external provider. “Implemented” below means a control is present in the inspected pure module at source level; it does not establish runtime deployment, authenticated inputs, or operational effectiveness.

## Executive assessment

The agent has a useful **non-dispatching safety and review foundation**, but it does not yet have the trusted operational control plane needed to run unattended or deliver assignments securely.

- **Present in pure modules:** strict task/preflight validation; phase-ordered planning; non-dispatchable assignment packages; package-binding checks when an independently retained expected digest is supplied; worker-submission structural review; evidence-byte hash checking against a caller-supplied manifest; report/artifact-bundle validation; conservative recovery classification; and append-only v1 ledger primitives.
- **Specified but not implemented:** authenticated human approvals/revocations; a trusted assignment registry; atomic durable state/event/idempotency/checkpoint transactions; authenticated dispatcher and worker delivery/return channels; protected package-digest retention; authenticated source identities; independent artifact-provider/run authentication; protected anti-rollback checkpoints; and transactional backup/restore.
- **Not demonstrated / remains a hard blocker:** any deployed trusted backend, independently authenticated approval channel, dispatch/delivery integration, durable lifecycle persistence, workflow identity pinning, least-privilege runtime configuration, independent trust anchor, live handoff revalidation at a dispatch boundary, and failure-injection evidence.

The current design should remain **non-operational**. The safe next implementation order is not “turn on the agent”; it is to select and threat-review the trust roots/backend, then implement a minimal registry transaction boundary and authenticated approval/dispatch adapters only after the controlling handoff permits the exact work.

## Status definitions

- **Present (pure module):** source-level deterministic validation/decision exists, but callers or a future adapter may still need to authenticate inputs and provide trusted context.
- **Specified only:** a design document defines the control, but no operational implementation was found in the inspected source.
- **Partial:** a useful subset exists, with an explicit trust, atomicity, provenance, or deployment gap.
- **Not established:** no sufficient implementation or evidence was identified in this bounded review.
- **Blocked:** implementation/testing is not authorized under the current G0-05 handoff.

## Control-by-control matrix

| Threat/control area | Current source-level control | Status | Gap / activation blocker |
|---|---|---|---|
| Task schema, duplicate IDs, strict JSON, mandatory prohibitions | Safety controller and task runner enforce fixed schemas and fail-closed decisions | Present (pure module) | Runtime policy files and caller identity still need trusted deployment/provenance |
| Phase order and G0-05 lock | Planner enforces Phase 3 → 1 → 2 → 4 → 5; controller has independent G0-05 lock | Present (pure module) | Must re-read authoritative live handoff at every future operation boundary |
| Batch planning | Single queue snapshot, per-task preflight, earliest-phase stop, bounded plan-only output | Present (pure module) | Planner is not authorization or dispatch |
| Assignment package integrity | Canonical package builder and digest; assignment-return compares rebuilt package against expected digest | Partial | Expected digest is not currently retained in an independent trusted store; orchestration explicitly marks digest as not stored |
| Worker submission structure | Supervisor review checks task binding, action labels, claims, evidence refs, and authority boundaries | Present (pure module) | Worker identity and return-channel authenticity are external and absent |
| Evidence file integrity | Evidence verifier recomputes bytes against a supplied commit manifest and expected commit | Partial | Manifest, bytes, checkout identity, and expected commit are caller-supplied until a trusted workflow derives/authenticates them |
| Checkout/report provenance | Report builder can compare expected context, HEAD, clean status, and manifest hashes when given trusted values | Partial | Metadata/context is not authenticated by the pure module; no trusted workflow currently supplies it |
| Report schema and artifact file hashes | Strict report builder and exact three-file bundle verification | Present (pure module) | Hashes do not authenticate artifact uploader/provider or prove task execution |
| Artifact provider/run identity | Design specifies run-bound artifact checks | Not established | No active workflow/provider adapter or authenticated artifact provenance |
| v1 event ledger/hash chain | Append-only in-memory event validation, canonical hashing, replay checks | Partial | Python serialization is not a cross-runtime standard; no trusted durable store or external checkpoint |
| Persistence/CAS | Persistence contract prepares append and detects stale checkpoint | Partial | It is explicitly not atomic CAS and performs no persistence; concurrent callers can both prepare |
| v2 global event sequence | Event v2 and unified transaction specs define ordering | Specified only | No v2 schema/registry implementation |
| Dual concurrency control | Unified transaction spec requires global checkpoint plus per-assignment version in one transaction | Specified only | No database transaction, uniqueness constraints, or concurrency proof |
| Atomic state + event + idempotency + checkpoint | Unified transaction and registry designs require all-or-nothing writes | Specified only | No backend or adapter; critical blocker |
| Authenticated approval and revocation | Approval envelope and operation-boundary rules are documented | Specified only | No authenticated approval service, key management, expiry/revocation store, or single-use enforcement |
| Live handoff/policy revalidation | Dispatcher/registry contracts require a fresh check at operation boundary | Specified only | No dispatcher exists to enforce it |
| Workflow identity/revision pinning | Contract specifies workflow path and immutable SHA binding | Specified only | No active agent workflow, trusted platform-context adapter, or demonstrated SHA pinning |
| Dispatch and delivery | Dispatcher contract defines separate dispatch-started and confirmed delivery facts | Not established | No dispatcher, provider integration, receipt verification, or delivery identity store |
| Lost response / uncertain delivery | Recovery classifier conservatively distinguishes pending/unknown and forbids auto-retry | Partial | Inputs are unauthenticated observations; no provider reconciliation adapter or durable idempotency |
| Cancellation/revocation race | Registry and unified transaction specs define serialized race semantics | Specified only | No transaction engine or provider cancellation semantics |
| Authenticated worker return | Contracts specify authenticated receiver and assignment binding | Not established | No worker identity/channel authentication or durable raw-return receiver |
| Human task disposition | Recovery/report/review modules preserve human-only task/gate authority | Partial | No authenticated human disposition service or immutable disposition registry |
| Separate phase-gate closure | Modules explicitly do not approve gate closure; designs keep it separate | Present as a restriction | Actual authenticated gate-disposition mechanism is absent and must remain disabled under current handoff |
| Event-chain/checkpoint anti-tamper | v1 chain validation exists; v2 design requires protected checkpoint | Partial | Checkpoint is not independently anchored; no rollback-resistant store |
| Backup/restore anti-rollback | Threat model and v2 design describe external anchor requirement | Specified only | No backup system, restore procedure, or recovery drill evidence |
| Cross-runtime canonicalization | v1 implementation uses deterministic Python JSON serialization; v2 proposal calls for versioned JCS/shared vectors | Partial | No v2 canonicalizer or cross-runtime test vectors; do not migrate v1 hashes |
| Rate limiting/quota recovery | Batch size is bounded in planner | Partial | No provider rate-limit policy, retry budget, or durable queue scheduler |
| Least privilege and secret isolation | Design documents require separated identities and no worker access to registry secrets | Specified only | No runtime permissions, secrets, environment protection, or deployment audit established |
| Supply-chain action pinning | Threat model calls for immutable action SHA pins | Not established | No full workflow/action/dependency audit in this gap review |
| Monitoring and incident response | Designs identify audit and stop conditions | Specified only | No active monitoring, alerting, incident process, or operator runbook evidence |
| Failure injection and recovery validation | 30 future cases specified in threat matrix | Blocked | No injections/tests executed; current handoff prohibits relevant execution |

## Highest-priority blockers

### P0 — trust roots and durable authority

1. **Choose the independent trust roots.** Decide how human identity/approval, workflow identity, provider identity, registry administration, and anti-rollback checkpoint are authenticated. A workflow must not be its own approval root.
2. **Select a backend with proven atomicity.** It must commit assignment state, event, idempotency index, global checkpoint, and per-assignment version atomically, or provide a separately reviewed equivalent transactional protocol.
3. **Retain immutable assignment bytes and digest before delivery.** The expected digest must be independently retained, not supplied by the worker or reconstructed from its return.
4. **Implement approval/revocation at the operation boundary.** Approval must bind exact task/package revision, operation, workflow SHA, branch, handoff revision, input commit, scope, expiry, and single-use state.
5. **Implement authenticated dispatch and delivery reconciliation.** Dispatch intent, delivery confirmation, timeout/unknown, and cancellation must be distinct authenticated states. Unknown delivery must never trigger an automatic new attempt.

### P1 — provenance and return integrity

6. Derive repository, branch, commit, workflow/run identity, clean-checkout state, and evidence manifest from authenticated platform/checkout context.
7. Authenticate the worker return channel and persist raw return bytes/digest before review.
8. Bind artifact verification to authenticated workflow run and provider metadata; file hashes alone are insufficient.
9. Define versioned cross-runtime canonicalization for v2 with shared vectors; preserve v1 hashes and semantics.
10. Establish independent checkpoint/backup anti-rollback and a tested restore procedure.

### P2 — operational hardening

11. Pin all third-party Actions by immutable SHA and audit effective permissions, secrets, environments, runner selection, and dependencies.
12. Add bounded rate-limit handling, retry budgets, monitoring, alerts, incident response, and an operator runbook.
13. Perform independent review and the failure-injection suite in an isolated disposable environment only after explicit authorization and after the controlling handoff permits it.

## Threat-to-control coverage

| Threat IDs | Coverage today | Residual issue |
|---|---|---|
| T-01, T-16, T-17 | Structural review and strict parsing in pure modules | Authenticated return channel, size/depth bounds at receiver, durable raw payload absent |
| T-02, T-14, T-15 | Immutable package checks and race rules specified | Independent digest storage, approval store, transactional dispatcher absent |
| T-03, T-05, T-06 | Approval/workflow/service identity contracts documented | No authenticated roots or operational adapters |
| T-04, T-07 | Policy/branch restrictions documented | Effective permissions and full supply-chain audit not established |
| T-08, T-09, T-11 | v1 replay logic and v2 idempotency design | Durable provider identity and atomic replay index absent |
| T-10, T-12, T-13 | Pure stale-checkpoint preparation and dual-CAS design | No atomic persistence; races remain possible outside a future backend |
| T-18, T-19 | Byte-hash and report/artifact validation | Trusted manifest and provider/run association not established |
| T-20, T-21, T-22 | Conservative recovery guidance and chain validation | Store reconciliation, independent checkpoint, backup restore absent |
| T-23 | v1 deterministic Python hashing and v2 proposal | Cross-runtime standard/vectors not implemented |
| T-24, T-25, T-26 | Bounded planning and documented admin controls | Rate-limit operations, monitoring, key separation, and admin recovery not implemented |

## Required implementation gates

No P0/P1 implementation is authorized by this audit. Once the G0-05 handoff permits an exact scope and the project owner authorizes it, the recommended sequence is:

1. Approve a trust-root and deployment threat model, including backend/provider selection.
2. Define and independently review closed v2 schemas, canonicalization version, shared vectors, and state-transition invariants.
3. Implement a minimal registry transaction adapter with atomic state/event/idempotency/checkpoint and both concurrency versions.
4. Implement authenticated approval/revocation records and exact operation-boundary policy checks.
5. Implement a dispatcher against a mock provider first; do not enable real worker delivery.
6. Implement authenticated return receipt and artifact/run provenance adapters.
7. Run unit, concurrency, crash, replay, rollback, and recovery tests in a disposable isolated environment.
8. Obtain independent review of effective permissions, workflow identity, secrets, supply chain, and recovery.
9. Only then seek separate explicit approval for a bounded manual readiness workflow. Scheduling and event-driven operation remain separate later approvals.

## Current project reality

- This audit reviewed selected design documents and pure source modules. It did not exhaustively inspect all repository workflows, organization settings, provider settings, dependencies, or runner configuration.
- No trusted registry, durable transaction adapter, approval service, dispatcher, delivery channel, authenticated return receiver, or independent checkpoint is active.
- The agent remains non-operational; no workflow is active and no unattended worker is running.
- The current Phase 3 G0-05 handoff remains controlling. No scripts, tests, workflows, or failure injections were run.
- No research code/data, canonical definitions, protected research branch, default branch, secrets, permissions, VPS, or runner configuration were changed.

This audit is a prioritized design/source gap assessment, not proof of runtime security or authorization to activate the agent.
