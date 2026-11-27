# Control-plane authorization and permission-model audit — 2026-11-27

## Scope and authority
Targeted static consistency review of the trust-root/identity architecture, operation-to-identity matrix, approval lifecycle, emergency suspension and resume protocol, trusted registry interface, backend qualification framework, security gap audit, and implementation-readiness gates.

This is a documentation/source-contract audit, not a live permissions audit. No GitHub organization/repository settings, identity provider, accounts, credentials, keys, secrets, infrastructure, workflow, provider, registry, or runtime were accessed or changed. No tests, scripts, workflows, dispatch, or research operations were run. The active Phase 3 G0-05 handoff remains controlling.

## Executive assessment
The architecture already states the correct high-level principle: no actor should both assert authority/evidence and unilaterally control the independent record used to verify it. It also separates human approval, policy authority, dispatcher, registry, worker/provider, evidence verifier, reviewer, witness, task disposition, and phase-gate authority.

The remaining gap is translating logical roles into an enforceable, operation-specific authorization system with explicit deny-by-default permissions, mutually exclusive role combinations, trusted identity attributes, effective-permission verification, and transaction-bound checks. Role names and a matrix do not prove that the underlying GitHub, identity, database, storage, workflow, billing, support, or recovery administrators are independent.

## Findings

### CP-01 — Logical role separation is not yet a complete permission model (P0)
The identity architecture defines trust domains and an operation-to-identity matrix, but it does not yet provide a complete machine-enforceable permission catalogue for every command, record type, field, environment, and administrative path. An implementation could still grant broad CRUD or administrator permissions that collapse the intended separation.

Required:
- Define a closed operation enum and closed resource/action matrix for every registry command, record class, evidence object, workflow, secret, key, checkpoint, audit sink, and provider operation.
- Specify allow and explicit deny rules, default deny, scope constraints, immutable-field rules, and exact identity attributes evaluated.
- Deny wildcard, owner, organization-admin, repository-admin, database-superuser, storage-owner, and broad environment-secret access to routine workload identities.
- Separate control-plane administration from data-plane operation; privileged administration requires independent approval, short-lived elevation, external audit, and dual control where high impact.
- Include indirect paths: workflow edits, action upgrades, runner administration, environment approvals, branch protection, app installation, token minting, billing/support recovery, and backup restoration.

### CP-02 — Role-combination and conflict-of-interest rules are incomplete as a single normative matrix (P0)
Several documents list separate roles and prohibit self-approval, but no single authoritative matrix enumerates every prohibited combination across normal operations and incident recovery. The emergency protocol distinguishes freeze requester, break-glass activator, recovery operator, witness administrator/verifier, independent reviewer, resume authority, and recovery-code deployer; the general architecture is less exhaustive.

Required:
- Publish one normative role-conflict matrix covering approver, revoker, dispatcher, policy maintainer, task author, registry operator/admin, evidence receiver/writer, evidence verifier, worker/provider admin, reviewer, task-acceptance authority, gate authority, witness admin/verifier, backup admin, identity/security admin, deployment admin, incident commander, freeze requester, break-glass activator, recovery operator, and resume approvers.
- Enforce conflicts by stable authenticated subject and common administrative/control roots, not merely different usernames or email addresses.
- Treat shared identity tenant/root administrators, recovery channels, signing-key custodians, and support escalation as common control when they can take over multiple principals.
- Require independent reviewer recommendation before high-impact resume; reviewer cannot also be either resume approver or recovery operator.
- Where separation cannot be demonstrated, mark the capability UNKNOWN/BLOCKED rather than accepting a compensating assertion.

### CP-03 — Approval scope is strong, but command authorization needs a canonical policy decision contract (P0)
Approval documents bind immutable approvals to exact operation, task, assignment revision, package digest, workflow, repository/ref, input commit, handoff/policy, scope, expiry and nonce. Registry and dispatcher contracts require revalidation at the operation boundary. A common canonical decision contract is still needed so every adapter evaluates the same facts.

Required:
- Define a versioned authorization-decision input containing authenticated subject/issuer/audience, credential/key status, requested operation, resource IDs/revisions/digests, task and package digests, repo/ref, workflow path/SHA/run/attempt, input commit, current handoff/policy revision, approval ID/digest, trusted time, registry checkpoint, assignment version, emergency-hold state, and evidence freshness.
- Define deterministic deny reasons and a single policy decision point; enforcement must occur inside the same transaction as approval consumption and protected state transition.
- Bind the decision result to the exact request digest and return an immutable decision receipt.
- Missing, stale, conflicting, unverifiable, or caller-supplied-only attributes must deny. No client-side preflight or cached ALLOW may authorize a later operation.
- Every privileged operation must re-read current policy and handoff at its own boundary.

### CP-04 — Permission inheritance and GitHub-specific authority need a deployment evidence gate (P0)
The repository audit is static and prior workflow inventory is not an effective-permission export. Organization/repository defaults, workflow/job permissions, reusable workflows, GITHUB_TOKEN, GitHub Apps, environments, branch protections, self-hosted runners, secrets and administrators can create indirect authority beyond source declarations.

Required before any GitHub activation:
- Export and independently review organization/repository Actions policies, default workflow permissions, allowed actions, app installations, runner groups, environments/reviewers, secrets scope, branch/ruleset protections, deploy keys, webhooks, and administrative membership.
- Require explicit least-privilege workflow/job permissions; pin third-party actions to reviewed immutable commit SHAs; pin reusable workflows and dependencies.
- Use isolated ephemeral hosted runners for untrusted tasks; prohibit self-hosted/VPS runners and privileged caches/secrets.
- Restrict workflow dispatch entrypoint and actor; validate actor authorization independently rather than treating workflow dispatch permission as business approval.
- Prove that agent branch or artifact content cannot modify the trusted entrypoint, policy, task queue, verifier, or approval path.
- Capture effective permissions and identity context as signed/versioned deployment evidence; re-audit after any organization/repository setting, workflow, app, runner, or branch-rule change.

### CP-05 — Administrative and emergency powers need explicit resource boundaries (P1)
Emergency freeze, credential containment, deny-only revocation lane, break-glass, witness, and resume are separated in design, but exact technical capability boundaries and API/resource allowlists are not consolidated in one place.

Required:
- Freeze may only assert deny/hold for an enumerated service scope and incident; it cannot write approval, task, assignment, evidence, review, or gate records.
- Credential containment may disable/revoke named credentials, sessions, or keys in the independent identity plane; it cannot mint replacement authority or clear the hold.
- Restricted revocation lane may append revocation/invalidation for existing exact approval IDs/digests only; it must reject positive authorization, assignment mutation, dispatch, task disposition, gate action, or unrelated event.
- Witness may attest/reject monotonic checkpoints; it cannot mutate registry or authorize commands.
- Break-glass may access only pre-enumerated recovery commands and isolated resources; it cannot change role policy, witness state, audit destination, approval authority, or resume.
- Resume requires a separate two-human quorum and reviewer recommendation, bound to exact checkpoint/recovery report/service scope/expiry; it must not implicitly re-enable dispatch or research authority.
- Provide negative tests for every prohibited command/resource pair before activation, when authorized.

### CP-06 — Identity lifecycle and session assurance need more operational detail (P1)
The architecture requires stable subject, issuer, audience, validity, key ID and revocation status, plus human strong authentication and short-lived workload credentials. The effective assurance policy still needs explicit enrollment, authentication strength, session freshness, reauthentication, device/recovery trust, and revocation propagation.

Required:
- Define human enrollment/proofing, phishing-resistant MFA where supported, session max age, step-up authentication for approvals/revocations/acceptance/gate decisions, and trusted device/session requirements.
- Define workload identity issuance, audience, token TTL, allowed network/workload binding, key rotation, issuer trust, and no reusable static credentials.
- Define subject deprovisioning, role-change propagation, emergency revocation latency, key compromise scope, and treatment of approvals issued during a suspected compromise interval.
- Ensure account recovery cannot silently bypass the independent approver/resume quorum.
- Log authentication and authorization decisions to an independently administered audit sink without exposing secrets.

### CP-07 — Policy changes and emergency policy overrides need versioned governance (P1)
Policy authority is logically separate from dispatcher and worker, but the complete change process, dual review, activation delay, rollback behavior, and emergency deny-only policy semantics are not consolidated.

Required:
- Store policy/handoff revisions immutably with digest, author, reviewer, activation time, source commit, and signed change record.
- Require independent review for changes to task allowlists, phase order, action vocabulary, scope, permissions, or policy enforcement code.
- Policy rollback must create a new revision; never rewrite history. Restore cannot reactivate an old permissive policy without fresh authorization.
- Emergency policy may only narrow/deny capability; positive emergency overrides are forbidden.
- Dispatch-time decision must bind to exact active policy revision and handoff digest.

### CP-08 — Authorization telemetry and periodic access review need measurable controls (P1)
The documents require external audit and monitoring but do not yet define minimum event fields, alert thresholds, access recertification cadence, or revocation service-level objectives.

Required:
- Record subject, issuer, audience, credential/key ID, session/authentication context, operation, resource, decision, reason, policy revision, approval digest, request digest, registry sequence, workflow/run context, timestamp, and correlation/incident ID.
- Alert on denied privileged operations, role changes, policy changes, token issuance anomalies, secret access, workflow permission changes, runner changes, witness gaps, break-glass use, and audit-export failures.
- Define access recertification and key/credential rotation cadence, revocation propagation objective, audit retention, and independent evidence owner.
- Detect impossible role combinations, common-root concentration, stale credentials, dormant privileged accounts, and privilege drift.

### CP-09 — Human task acceptance, phase-gate authority, and platform administration must remain distinct (P0)
The architecture correctly separates task acceptance from phase-gate closure. The implementation must also prevent repository or platform administrators from implicitly becoming research approvers merely because they can merge, dispatch, change workflow permissions, or alter protected branches.

Required:
- Define separate authenticated roles and command permissions for task acceptance and phase-gate disposition.
- Gate authority must require explicit current handoff permission, predecessor-gate evidence, exact reviewed evidence digest, and separate immutable decision.
- Repository merge/admin rights, workflow dispatch rights, registry administration, and artifact access do not imply research approval.
- A person with platform administration may participate as a human approver only through the independent approval channel and conflict checks; platform privileges alone never grant that authority.
- Current G0-05 prohibition remains an unconditional deny, regardless of administrative or emergency role.

### CP-10 — Resume must not imply dispatch authorization (P0)
The emergency protocol binds resume to a checkpoint and recovery-report digest and explicitly says dispatch remains separately gated. This must be a hard state-machine invariant: successful emergency resume returns the control plane only to a restricted, non-dispatching state until normal operation-specific approval and all readiness gates pass.

Required:
- Define distinct states for emergency-held, recovery-in-progress, restored-read-only, security-revocation-pending, resumed-read-only, and operationally-enabled.
- Resume quorum may transition only to resumed-read-only with dispatch, scheduling, provider calls, and research operations still disabled.
- A separate normal activation decision must revalidate all readiness gates, current handoff, permissions, identities, backend/witness, provider and worker isolation before enabling any exact capability.
- Any critical UNKNOWN, witness pending, unresolved provider attempt, stale policy, or role conflict returns to hold/deny.
- Never let a recovery workflow or break-glass grant toggle workflow dispatch, schedules, branch permissions, or research gate state.

## Consolidated authorization decision sequence
1. Authenticate principal; validate issuer, audience, subject, credential/key, session assurance, and revocation state.
2. Resolve effective roles and common administrative roots; reject prohibited role combinations.
3. Load current policy and handoff revisions from trusted sources and verify digests.
4. Resolve exact resource, task, assignment revision, package/evidence/review digests and expected state versions.
5. Verify operation-specific approval, scope, nonce, expiry using trusted time, revocation and consumption status.
6. Verify emergency hold, witness status, checkpoint, global version, and per-assignment version.
7. Evaluate the closed authorization policy; missing or ambiguous attributes deny.
8. Commit authorization consumption and protected state transition atomically, with idempotency and immutable audit receipt.
9. Reconcile provider/external effects separately; never infer success from a local command result.
10. Emit security telemetry to an independent audit destination and alert on policy violations or degraded trust.

## Role-conflict baseline
| Role A | Role B | Minimum rule |
|---|---|---|
| Worker | Approver / revoker / reviewer / registry writer | Prohibited |
| Dispatcher | Approver / policy maintainer / reviewer / task acceptor / gate authority | Prohibited |
| Task or policy author | Sole approver of own change / gate authority for resulting work | Prohibited |
| Registry administrator | Sole witness administrator / sole audit administrator / sole approver | Prohibited |
| Evidence receiver/writer | Independent reviewer of same evidence | Prohibited |
| Reviewer | Evidence writer / registry history editor / resume approver for same incident | Prohibited |
| Recovery operator | Witness verifier / independent reviewer / resume approver | Prohibited |
| Witness administrator/verifier | Registry administrator / approver / dispatcher | Prohibited |
| Freeze requester / break-glass activator | Resume approver for same incident | Prohibited |
| Resume approver 1 | Resume approver 2 under common takeover-capable root | Prohibited |
| Platform/repository administrator | Implied research approver by virtue of admin rights | Prohibited |
| Task acceptor | Automatic phase-gate authority | Prohibited |

Different accounts under one common takeover-capable identity, recovery, signing-key, or administrative root count as one control domain for independence analysis.

## Current status and hard boundary
- This audit identifies requirements and contract gaps; it does not establish that any live account, permission, role, secret, workflow, or service is misconfigured.
- No effective permission exports, identity-provider configuration, GitHub settings, credentials, secrets, accounts, infrastructure, or provider state were accessed or changed.
- No tests, scripts, workflows, dispatch, scheduling, provider calls, or research operations were run.
- No backend, identity provider, role assignment, or authorization service has been selected or implemented.
- The agent remains non-operational. Phase 3 G0-05 remains controlling; no role, approval, administrative privilege, emergency hold, or recovery mechanism overrides that handoff.
