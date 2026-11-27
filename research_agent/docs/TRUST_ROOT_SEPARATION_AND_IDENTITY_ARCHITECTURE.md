# Trust-root separation and identity architecture

## 1. Purpose and status

This document defines a vendor-neutral trust-domain model for a future OKX research-agent control plane. It identifies which identities may assert which facts, which records each domain may control, and the independence properties that must be demonstrated before any operational implementation.

It is a design proposal only. It does not select an identity provider, hosting platform, registry backend, worker provider, or evidence store. It does not create credentials, accounts, infrastructure, workflows, or permissions. It grants no dispatch, execution, task-acceptance, gate-closure, or phase-advancement authority.

The active Phase 3 G0-05 handoff remains controlling. The agent remains non-operational.

## 2. Core security objective

No actor or component may both:
1. assert a fact that grants authority or establishes trusted evidence; and
2. unilaterally create, alter, or erase the independent record used to verify that fact.

The system must preserve separation between:
- human authorization;
- policy and task eligibility;
- workflow execution identity;
- assignment and package custody;
- external worker delivery;
- evidence storage and verification;
- independent event/checkpoint recovery;
- human review and research-gate disposition.

A valid signature or authenticated identity proves which principal made a statement. It does not prove the statement is true, the principal is authorized for this operation, or the underlying research conclusion is correct.

## 3. Proposed trust domains

These are logical domains, not selected products or deployed services.

| Domain | Owns or asserts | Must not control |
|---|---|---|
| Human authority | Authenticated approvals, revocations, task disposition, separate gate decisions | Worker code, its own approval verification, evidence bytes, registry history deletion |
| Policy authority | Versioned task/phase rules and handoff constraints | Human approval identity, workflow execution, registry checkpoint rollback |
| Dispatcher | Validated request and external delivery attempt | Approval issuance, task policy mutation, worker return truth, human disposition |
| Trusted registry | Immutable assignment revisions, package digests, lifecycle events, state, idempotency index | Independent approval credentials, external checkpoint witness, worker-controlled records |
| Workflow platform | Authenticated workflow/run/actor context | Research gate decisions, registry data outside scoped API, long-lived broad secrets |
| Worker provider | Delivery receipt and provider-side delivery status | Approval, task definition, package digest authority, research evidence verification |
| Worker | Work product and evidence declarations | Trusted package digest, registry, approvals, workflow identity, reviewer decision |
| Evidence store | Immutable/content-addressed evidence objects and retrieval audit | Evidence truth claims, approval issuance, lifecycle state transitions |
| Independent witness | Monotonic checkpoint or signed checkpoint receipts | Registry event creation, task approval, worker execution |
| Independent reviewer | Review finding and human recommendation | Worker source artifacts, trusted registry history, approval identity |

Separation must be evaluated across actual administrative accounts, credentials, service principals, APIs, storage, deployment pipelines, and recovery procedures—not merely separate module names.

## 4. Identity classes and claims

Every authenticated principal must have a stable subject identifier, issuer, audience, validity period, credential/key identifier, and revocation status. Authorization must be operation-specific and based on trusted context.

### 4.1 Human approver

Permitted claims:
- approve one exact operation against one task digest, assignment revision, branch, handoff revision, workflow identity, and input commit;
- revoke a prior approval;
- record a human task disposition after review;
- make a separate phase-gate decision only when the active research handoff permits it.

Prohibited:
- using a worker-supplied `approved_by` string as identity;
- approving broad future tasks through a queue flag;
- converting task acceptance into gate closure;
- using the same unreviewed automation identity as both approver and dispatcher.

Approval record must include unique approval ID, authenticated subject, operation enum, exact scope digest, policy/handoff revisions, issued/expiry times, revocation state, and an independently verifiable audit reference.

### 4.2 Policy authority

Policy authority supplies the exact task schema, phase order, prohibitions, allowlist, and current handoff binding. It must be versioned and integrity-protected.

Policy eligibility is not a human approval. A task being allowlisted does not authorize delivery or execution. Policy changes require a separate reviewed change process and must not be writable by worker or dispatcher identities.

### 4.3 Dispatcher workload identity

The dispatcher authenticates as a workload identity, not as a human. Its token must be audience-restricted, short-lived where supported, and scoped to a small set of registry commands.

It may:
- read the exact eligible task and policy context;
- prepare a package;
- request validation of an existing approval;
- initiate one approved dispatch operation;
- record authenticated provider receipts.

It may not:
- create or modify human approval records;
- alter task definitions or phase permissions;
- overwrite package digest after approval;
- accept worker returns or human dispositions;
- close a research gate;
- bypass the active handoff.

### 4.4 Registry service identity

The registry authenticates callers and enforces transition invariants inside the transaction boundary. Its service identity must not be exposed to worker code. It must not trust caller-supplied claims for workflow identity, approval status, checkout provenance, or delivery confirmation.

Registry administrators must not be able to silently rewrite history without independent checkpoint mismatch becoming detectable.

### 4.5 Workflow identity

Workflow provenance must be derived from authenticated platform context and independently checked against expected values:
- repository immutable identity;
- workflow file path and exact revision;
- workflow run ID and attempt;
- triggering actor identity and event type;
- ref/branch and checkout commit;
- actual checkout cleanliness and input manifest;
- job identity and permission context.

Workflow inputs may identify a task or request, but must not grant approval or supply authoritative provenance. A branch name alone is not a workflow identity.

### 4.6 Worker identity

Worker identity proves which provider/worker instance submitted a return. It does not prove task completion. Worker content, metadata, evidence descriptions, claimed actions, and timestamps remain untrusted until independently bound and verified.

The worker must have no credentials that can write to approvals, registry state, protected checkpoints, research branches, or trusted evidence indexes.

### 4.7 Evidence verifier and reviewer

Evidence verification must consume expected commit and manifest information from authenticated workflow/registry context, not worker claims. It should be a separate least-privilege component from the worker and dispatcher.

The reviewer must be able to inspect immutable evidence and provenance without having write permission over the evidence or registry event history being reviewed.

### 4.8 Independent checkpoint witness

The witness stores or attests a monotonic checkpoint independently of the registry's administrative rollback domain. It must detect restoration of an older but internally consistent registry snapshot.

The witness must not have permission to rewrite registry events, approve assignments, or initiate dispatch. A backup stored under the same administrator and credential boundary as the registry is not independent anti-rollback evidence.

## 5. Operation-to-identity authorization matrix

| Operation | Required authenticated principal | Additional conditions |
|---|---|---|
| Read task and policy | Dispatcher or reviewer | Read-only scope; current handoff binding |
| Prepare assignment package | Dispatcher | Exact queued task; valid preflight; trusted task digest |
| Store package bytes/digest | Registry service | Immutable revision; independent digest computation |
| Approve dispatch | Human approver | Operation-bound, exact package/task/workflow scope, unexpired and not revoked |
| Start dispatch | Dispatcher | Approval revalidated in same protected operation boundary |
| Confirm delivery | Provider-authenticated receipt/query via trusted adapter | Stable provider delivery identity and idempotent replay |
| Receive worker return | Authenticated worker/provider channel | Exact assignment revision and retained package digest |
| Verify evidence | Independent verifier | Authenticated checkout context and manifest; byte-level verification |
| Complete structural review | Reviewer service/identity | Trusted task and assignment binding; evidence checks |
| Accept task | Human reviewer/authority | Exact review digest and assignment revision |
| Close phase gate | Separate human authority | Explicit current handoff permission and phase predecessor requirements |
| Advance phase | Separate policy-controlled human decision | Gate closure independently verified |
| Restore registry | Recovery administrators under dual control | Witness reconciliation, chain verification, audited restore |
| Revoke credentials | Identity/security administrator | Incident procedure and independent audit |

No row may be authorized solely by a worker declaration, workflow input, task queue status, task allowlist hash, or artifact filename.

## 6. Independence tests

A proposed deployment must answer and demonstrate all of the following:

1. Can the worker modify or impersonate the human approval record? It must not.
2. Can the dispatcher create, extend, or revoke its own approval? It must not.
3. Can a workflow input or actor-controlled field make an unapproved task eligible? It must not.
4. Can a registry administrator rewrite history and also roll back the only checkpoint witness? They must not share that unilateral capability.
5. Can the worker replace the package digest used by return review? It must not.
6. Can a provider receipt be forged by the worker or dispatcher without provider authentication? It must not.
7. Can a reviewer change the evidence being reviewed without detection? They must not.
8. Can the evidence verifier accept a manifest supplied only by the worker? It must not.
9. Can a task-acceptance identity also close a research gate without a separate decision? It must not.
10. Can a recovery administrator restore a stale snapshot and resume dispatch before witness reconciliation? They must not.
11. Can one compromised credential access all trust domains? It must not.
12. Can any role silently expand its permissions through repository defaults, inherited workflow permissions, or broad environment secrets? It must not.

Each answer requires effective-permission evidence and adversarial negative tests, not just an architecture diagram.

## 7. Credential and key lifecycle requirements

Before activation, define:
- issuer and audience restrictions for every token;
- short-lived workload credentials and rotation policy;
- key custody, signing algorithms, key identifiers, and verification policy;
- human MFA/strong authentication and approval session controls;
- revocation propagation and maximum revocation latency;
- emergency credential disablement and service shutdown;
- separation between production, test, and synthetic proof-of-capability credentials;
- secret redaction, audit logging, and access review;
- break-glass process with dual control, narrow scope, expiry, and post-incident review.
- emergency freeze is deny-only and may be triggered by one authenticated designated reporter; it cannot resume service or authorize protected writes;
- break-glass activation requires two distinct authenticated principals, short-lived incident-bound scope, independent notification, and an external append-only audit record;
- recovery operator, witness verifier, independent reviewer, and resume authority are separate principals for high-impact recovery; no self-approval;
- break-glass cannot issue/renew approvals, rewrite event history or witness state, change policy, suppress audit, or authorize dispatch;
- resume requires independent multi-party authorization bound to the exact reconciled checkpoint and signed recovery-report digest; dispatch remains separately gated.


Never put credentials in task definitions, artifacts, worker prompts, repository files, logs, or generated reports. A secret available to untrusted worker-controlled code is considered exposed to that code.

## 8. Repository and workflow topology implications

The repository's actual default branch is `main`. A `workflow_dispatch` workflow present only on `agent/okx-research-agent-v1` is not by itself an available manual dispatch entrypoint under the current repository topology.

Possible future architectures remain owner decisions:
- a separate agent repository with its own default branch and isolated permissions, reading only approved research evidence;
- a minimal, reviewed entrypoint on the existing default branch that invokes a separately pinned and reviewed agent implementation;
- another platform with an independently authenticated control plane.

No option is selected here. Do not modify `main`, create a repository, add a workflow, change permissions, or enable triggers without explicit owner approval. Do not dispatch inherited research workflows as a workaround.

Any chosen topology must prove that the workflow identity and policy revision cannot be replaced by worker-controlled content and that the default-branch entrypoint is reviewed independently.

## 9. Required evidence before design approval

A trust-root separation review must include:

- system and data-flow diagrams with administrative boundaries;
- identity inventory with issuer, audience, subject, permissions, credential owner, and revocation path;
- operation-to-identity matrix with effective permission exports;
- approval record schema and exact operation binding;
- registry administrator and checkpoint-witness independence proof;
- workflow provenance derivation and branch/default-branch activation design;
- worker/provider authentication and delivery receipt contract;
- evidence-store immutability and reviewer access model;
- key rotation, revocation, emergency shutdown, and incident procedures;
- negative tests for every independence test in section 6;
- independent security reviewer decision with dated evidence references.

Unknown or caller-asserted controls remain UNKNOWN. A provider feature description, proposed role name, or architecture diagram is not proof of deployed separation.

## 10. Current conclusion and hard boundary

This document makes the trust-root and identity requirements explicit but does not resolve owner choices or operational proof. No identity provider, account, credential, key, service, database, worker provider, evidence store, or checkpoint witness has been selected or provisioned. No workflow is active and no worker is dispatched.

The agent remains non-operational. No tests, scripts, workflows, or research operations were executed. No protected research branch, default branch, secrets, permissions, VPS, or self-hosted runner were changed.

The active Phase 3 G0-05 handoff remains authoritative. No implementation or validation may proceed where it conflicts with that handoff.
