# Owner decision register and pre-implementation blockers — 2026-11-27

## Purpose and authority

This register consolidates decisions that must be made by the repository/project owner or a separately authorized security/operations owner before the future agent control plane can be implemented or activated. It is a planning aid, not an approval record, authorization grant, procurement request, or implementation instruction.

The active Phase 3 G0-05 handoff remains controlling. This document does not authorize code changes, tests, scripts, workflows, dispatch, scheduling, research execution, credentials, accounts, provider selection, infrastructure, VPS access, or changes to repository settings.

## Immediate hard stop

**G0-05 remains open and its current handoff prohibits relevant script/test/workflow execution and research code/data changes.** No agent workflow, queue task, Copilot instruction, manual dispatch, or alternate branch may bypass that handoff. Any future scope change requires a fresh, explicit handoff and the appropriate human authorization.

## Owner decisions required before operational implementation

| ID | Decision | Evidence-based recommendation | Required decision owner | Blocked work until decided |
|---|---|---|---|---|
| OD-01 | Research authority and exact G0-05 exit criteria | Preserve current lock; require canonical real-row materialization, collision checks, and explicit handoff closure evidence before Phase 3 authorization changes. | Project/research owner | Any Phase 3 execution, test or gate closure |
| OD-02 | Hosting and data-residency boundary for the control plane | Evaluate managed transactional backend classes first; reject research VPS/local SQLite/GitHub artifacts as sole authoritative registry. Select only after all backend qualification gates are evidenced. | Project owner + security/operations owner | Backend procurement/provisioning |
| OD-03 | Independent identity and human authentication provider | Require independent approver, revoker, reviewer, dispatcher and recovery identities; define MFA/session assurance, recovery and administrative-root separation before selection. | Security/identity owner | Approval service and privileged operations |
| OD-04 | Authoritative policy and approval governance | Use immutable, versioned policy releases; fresh approval for every scope/revision change; no in-place extension, renewal or reactivation; missing history means UNKNOWN/deny. | Project owner + security owner | Policy publisher and approval lifecycle |
| OD-05 | Transactional registry and anti-rollback witness | Require atomic event/state/idempotency/checkpoint/outbox commit, global and assignment concurrency, independent witness and tested restore reconciliation. | Security/architecture owner | Trusted registry implementation |
| OD-06 | Worker execution provider and isolation strength | Require disposable per-assignment strong isolation, no ambient secrets, deny-all network by default, fixed reviewed image, resource/cost ceilings and independent artifact inspection. | Security/operations owner | Worker runtime and unattended execution |
| OD-07 | Provider delivery and callback model | Require documented idempotency scope/retention, durable outcome queries or authenticated callbacks, ordering/gap reconciliation, and no retry while outcome is uncertain. | Integration owner + security owner | Automated dispatch and delivery recovery |
| OD-08 | Worker-return and evidence retention | Decide retention periods, privacy classification, raw-byte custody, artifact immutability, data residency and deletion/legal-hold process without weakening audit integrity. | Project owner + data/privacy owner | Return receiver and evidence store |
| OD-09 | Human review, task acceptance and phase-gate authority | Keep worker, evidence writer, reviewer, task acceptor and phase-gate authority distinct; acceptance binds exact reviewed bytes and review digest; phase closure remains separately authorized. | Research owner + security owner | Task completion and phase advancement |
| OD-10 | Monitoring, incident response and emergency resume | Name independent alert owner, security custodian, recovery operator, witness verifier and two-human resume quorum; define out-of-band credential containment. | Security/operations owner | Any production or unattended mode |
| OD-11 | GitHub workflow activation topology | Resolve default-branch `workflow_dispatch` constraint using a reviewed minimal bridge or separately approved isolated agent repository; do not modify `main` or create a repository without explicit authorization. | Repository owner | Any GitHub Actions activation |
| OD-12 | Dependency, build and release provenance | Require complete dependency inventory, immutable action/image references, reproducible build evidence, SBOM and independently verifiable signed provenance before trusted deployment. | Security/build owner | Trusted release and deployment |
| OD-13 | Cost, quota and service-level limits | Define hard spend ceilings, concurrency/rate limits, retention costs, alert thresholds and safe pause behavior; free-only design must not silently rely on paid services. | Project owner + operations owner | Provider selection and scheduled operation |
| OD-14 | Independent assurance and pilot exit criteria | Require independent review of trust roots, adversarial synthetic validation, restore/incident drills, and a bounded supervised pilot before considering unattended triggers. | Project owner + independent reviewer | Unattended scheduling or event triggers |

## Recommended decision order

1. Preserve the G0-05 lock and complete the research handoff on its own evidence.
2. Confirm hosting/data-residency, identity ownership, policy governance and the independent security boundary.
3. Select and qualify the transactional registry, witness and recovery model.
4. Define provider delivery, worker isolation, raw-return custody and evidence retention.
5. Define human review/disposition and monitoring/incident ownership.
6. Resolve GitHub activation topology, supply-chain release controls and hard cost limits.
7. Complete independent assurance and supervised pilot criteria before any unattended schedule/event trigger.

## Current known decisions versus unresolved choices

### Already established
- Agent remains isolated to `agent/okx-research-agent-v1`; no automatic merge or commit to `price-action-v1`.
- Repository access is read-only by default; task and phase permissions are deny-by-default.
- No workflow, schedule, provider, registry, identity service, credential, sandbox, or backend is operational.
- G0-05 remains controlling; no Phase 3 execution, tests or workflows.
- No research VPS or self-hosted runner is part of the agent runtime design.
- Human task acceptance and phase-gate closure are separate decisions.

### Not selected or not evidenced
- Backend vendor/service, identity provider, witness service, worker provider, provider API, callback transport, artifact store, monitoring destination, hosting region, retention period, spend ceiling, and independent assurance provider.
- Actual administrative independence of GitHub, identity, database, storage, billing, support, recovery and witness administrators.
- Effective GitHub token permissions, protected-branch enforcement, immutable action pins, trusted build provenance, and the future activation bridge.

Do not interpret the recommendations in this register as decisions already made. Each unresolved item needs a named accountable owner, documented evidence, explicit decision, and revision-controlled approval before dependent work begins.

## Non-claims

No owner decision has been recorded by this document. No vendor was selected, account or service created, credential provisioned, repository setting changed, workflow enabled, code/test/script executed, research data accessed, provider called, or infrastructure/VPS modified. The agent remains non-operational.
