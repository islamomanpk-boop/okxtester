# Trust-root administrative independence audit — 2026-11-27

## 1. Purpose and scope

This is a targeted documentation-only audit of whether the proposed human approval channel, independent checkpoint witness, registry administrator, workflow/dispatcher identity, and recovery authority are independent in practice—not merely named as separate logical components.

Reviewed documents:
- `TRUST_ROOT_SEPARATION_AND_IDENTITY_ARCHITECTURE.md`
- `TRUSTED_REGISTRY_BACKEND_INTERFACE_SPEC.md`
- `TRUSTED_BACKEND_SELECTION_FRAMEWORK.md`
- `IMPLEMENTATION_READINESS_AND_EXIT_CRITERIA.md`
- `TRUSTED_ASSIGNMENT_REGISTRY_DESIGN.md`
- `TRUSTED_STORE_ADAPTER_DESIGN.md`
- `THREAT_MODEL_AND_FAILURE_INJECTION_MATRIX.md`

This review compares documented requirements and unresolved decisions. It does not inspect deployed cloud accounts, organization settings, identity-provider tenants, credential stores, billing owners, audit-log exports, or actual administrator assignments. No real-world independence can therefore be certified.

The active Phase 3 G0-05 handoff remains controlling. This audit authorizes no implementation, tests, workflow changes, dispatch, scheduling, research execution, account/resource creation, credential provisioning, or permission changes.

## 2. Executive finding

**Logical separation is well specified; administrative independence is UNKNOWN.**

The architecture already states that separation must be evaluated across actual administrative accounts, credentials, service principals, APIs, storage, deployment pipelines, and recovery procedures. The backend-selection framework also correctly warns that multiple services under one administrator credential are not independent trust roots.

However, the reviewed documents do not yet provide a concrete administrative dependency graph or evidence showing who can:
- administer or recover the human approval identity/channel;
- change registry data, schema, service code, or database access;
- alter, replace, disable, or roll back the checkpoint witness;
- control the identity provider, organization/tenant owner account, billing owner, or root recovery path;
- change workflow definitions, environments, secrets, runners, or workload identity trust;
- alter audit-log retention/export or suppress security alerts;
- invoke break-glass access or restore backups.

This is not proof that such a shared administrator exists. It means the architecture has not established that one compromised owner account, identity-provider administrator, root credential, recovery operator, or deployment pipeline could not control several nominally separate domains.

**Current status: UNKNOWN / BLOCKED.** Do not treat the proposed approval channel, registry, witness, or reviewer as operationally independent until the evidence in section 6 exists.

## 3. Findings

### F-01 — Logical roles are separated, but the administrative control plane is not mapped

The identity architecture separates human authority, policy, dispatcher, registry, workflow platform, worker/provider, evidence store, independent witness, and reviewer. It explicitly says independence must be assessed across actual administrators and credentials.

The backend framework similarly permits one vendor to host multiple components only if their identities, permissions, administrative roles, and rollback domains remain meaningfully separated.

What is missing is a concrete graph of administrative principals and their transitive powers. Separate service names, projects, databases, or API endpoints do not establish independence if one organization owner, cloud root, identity-provider administrator, or shared automation identity can reconfigure all of them.

**Required correction:** evaluate administrative control as a graph of principals, credentials, control-plane APIs, recovery paths, and data-plane permissions. Record shared ancestors and the maximum compromise blast radius.

### F-02 — Human approval-channel independence is specified at the application level, not the account-recovery level

The approval channel must authenticate a human, bind approval to an exact operation and scope, and remain independent of worker/dispatcher assertions. But the reviewed requirements do not explicitly trace who can reset the approver's account, enroll or replace MFA factors, issue impersonation tokens, alter approval policy, administer the identity tenant, or recover the channel's signing keys.

A separate login or application is insufficient if its owner or identity administrator can silently impersonate the approver or rewrite the approval audit record.

**Required correction:** document approver account ownership, identity issuer and tenant administrators, MFA recovery, signing-key custody, approval-policy administrators, audit-log administrators, and independent revocation/recovery controls. High-impact approval should require a second independently authenticated control where feasible; emergency recovery must not silently manufacture a valid approval.

### F-03 — Checkpoint-witness independence lacks an explicit common-root compromise test

The design correctly requires the witness to sit outside the registry's sole rollback/admin domain and warns against storing the only backup under the same administrator and credential boundary.

The remaining gap is transitive control: a shared organization owner, identity provider, cloud root, key-management administrator, deployment pipeline, billing suspension authority, or recovery operator may be able to disable or replace both registry and witness, or prevent witness access during restore.

**Required correction:** identify witness account/tenant ownership, root and delegated administrators, signing-key custody, write/read identities, retention-lock administrators, recovery path, billing/availability dependency, and external audit source. Demonstrate that registry administrators cannot alter witness history and witness administrators cannot write registry events or approve work. If a common provider-level root cannot be eliminated, explicitly classify the residual correlated-compromise risk and require an additional external witness or independent human hold before resumption.

### F-04 — Registry administration and application/service administration are not yet distinguished in an evidence-backed matrix

The registry API is intended to enforce invariants; the database/store is intended to retain immutable records; administrators must not silently rewrite history. The documents do not yet enumerate separately the powers of:
- application deployers;
- registry API operators;
- database data-plane writers;
- database/control-plane administrators;
- backup/restore operators;
- key-management administrators;
- audit-log administrators;
- tenant/root owners.

A database administrator may be unable to edit an append-only application API but still be able to restore a prior snapshot, alter access policies, disable retention, or replace keys. Conversely, an application deployer may change code to misuse a legitimate service identity.

**Required correction:** create a per-operation permission matrix for read, append, update, delete, restore, policy change, deploy, key rotation, log export/deletion, and emergency disablement. Include effective inherited permissions and indirect capabilities, not only nominal role names.

### F-05 — Break-glass and recovery authority may collapse the separation model unless independently controlled

The identity architecture requires break-glass controls with dual control, narrow scope, expiry, and post-incident review. The restore protocol requires freeze, witness reconciliation, provider reconciliation, and independent human resume authorization.

The reviewed documents do not yet define whether the same people or credentials can both invoke break-glass and approve the resulting resume, nor whether a recovery administrator can alter the witness, approval records, and audit trail used to justify recovery.

**Required correction:** separate emergency activation, recovery execution, checkpoint verification, and resume authorization. Require two distinct authenticated people or independently controlled principals for high-impact recovery. Log break-glass use to an external append-only destination that the recovery operator cannot administer. A recovery operator must not be able to self-certify the restore or resume dispatch.

### F-06 — Workflow/deployment control is a potential bridge across otherwise separate trust domains

Workflow identity is correctly required to come from authenticated platform context. However, a principal able to change the protected workflow revision, environment approvals, secret access, runner configuration, or identity federation policy may be able to impersonate the dispatcher or access registry credentials.

Likewise, a deployment pipeline that can update registry code and the service identity policy can undermine the separation between registry application and store administrator.

**Required correction:** inventory repository/org owners, workflow maintainers, environment approvers, runner administrators, secret administrators, OIDC/federation policy administrators, and deployment approvers. Pin and review workflow revisions and dependencies. No single workflow author or runner administrator should be able to both alter privileged code and independently approve its production authority.

### F-07 — Audit-log independence and billing/availability dependencies are under-specified

The design requires auditability, retention, and incident response, but the administrative independence of logs is not mapped. If a principal can change both the system and its only audit trail, post-incident verification is weak. A shared billing owner or provider account suspension path can also disable both registry and witness even if data-write permissions are separate.

**Required correction:** export security and administrative events to an independently administered retention destination; document who can change retention, delete exports, disable collection, or suspend the accounts. Treat shared billing, support, domain/DNS, and tenant recovery as correlated availability/control dependencies, even where they do not directly grant data-write access.

## 4. Required administrative independence model

Before choosing a provider or approving implementation, produce an explicit matrix with at least these rows:

| Control domain | Must be separately identified | Evidence required |
|---|---|---|
| Human approval | Approver, approver account recovery, MFA/key issuer, approval-policy admin | Authenticated identity configuration, recovery policy, approval audit export, negative impersonation tests |
| Registry application | Deployer, runtime identity, API policy owner | Deployment permissions, immutable revision, service identity scopes, independent approval |
| Registry data | Data-plane writer, database admin, backup/restore admin | Effective ACL/IAM exports, transaction permissions, restore rights, immutable audit evidence |
| Checkpoint witness | Witness writer, witness reader/verifier, witness admin, root recovery | Separate account/tenant proof, key custody, retention controls, rollback/disablement tests |
| Workflow platform | Repo/org owner, workflow author, environment approver, runner admin, secret admin, federation admin | Effective repository/org/environment/runner permissions and exact workflow identity policy |
| Evidence and artifacts | Evidence writer, verifier, retention admin, reviewer | Object immutability, content hash verification, access logs, separation of write/review |
| Identity provider | Tenant/root admin, federation admin, MFA recovery admin, signing-key admin | Admin role exports, conditional access, recovery logs, cross-domain blast-radius analysis |
| Recovery/break-glass | Incident commander, restore operator, witness verifier, resume approver | Dual-control procedure, immutable external incident log, role separation, expiry and post-incident review |
| Audit and billing | Audit-log admin, retention admin, billing/account owner, provider support recovery | Independent log export and retention; shared account/availability dependencies documented |

For each principal, record: immutable subject ID, issuer/tenant, account owner, credential type, effective permissions, inherited roles, control-plane APIs, data-plane access, recovery/reset powers, audit visibility, revocation path, and whether the same principal can assume another role.

Do not place secrets, tokens, recovery codes, or private keys in the repository or reports.

## 5. Correlated-compromise scenarios to add to future validation

The existing threat and failure matrices cover compromised roots, stolen credentials, approval/revocation races, checkpoint rollback, and excessive workflow permissions. The following scenarios make cross-domain administrator compromise explicit:

1. **Shared tenant owner:** one identity-provider or cloud organization owner can reset approver, registry admin, and witness-admin credentials. Expected: independence gate fails; no activation.
2. **Shared root recovery:** one root recovery path can regain both registry and witness accounts. Expected: classify as common root; require external witness and independent resume control or remain inactive.
3. **Shared deployment authority:** one pipeline identity can deploy registry code and alter dispatcher/federation policy. Expected: deny production deployment until separate approvals and immutable provenance are demonstrated.
4. **Witness retention administrator:** witness admin can shorten retention, delete checkpoints, or disable audit export. Expected: witness is not an independent anti-rollback anchor until controls prevent or externally record this.
5. **Approval recovery takeover:** identity admin can reset MFA or replace approval signing keys without an independent alert/hold. Expected: approvals from affected interval are untrusted; freeze and reconcile.
6. **Break-glass self-approval:** restore operator can invoke emergency access and authorize resume alone. Expected: reject resume; require a distinct independently authenticated approver.
7. **Shared audit control:** same principal can alter system state and delete the only audit evidence. Expected: no audit-independence PASS.
8. **Shared billing/suspension:** one billing/account owner can disable registry and witness simultaneously. Expected: record correlated availability risk and define an independent recovery/hold procedure.
9. **Workflow/runner compromise:** runner administrator can replace code and read a dispatcher credential. Expected: revoke affected identity, suspend dispatch, reconcile any uncertain attempts.
10. **Provider support escalation:** provider support or account recovery can assume control of both domains without independent notification. Expected: treat as a common privileged recovery path and require documented compensating controls.

These are proposed test oracles only. None has been executed.

## 6. Evidence required to change UNKNOWN

A future independent reviewer must obtain and verify, for the exact selected topology and version:

1. Administrative dependency graph showing every common tenant, owner, root credential, identity provider, key manager, deployment pipeline, support recovery path, billing owner, and audit destination.
2. Effective permission exports for each service, database, witness, workflow, environment, runner, secret store, identity provider, and audit destination.
3. Proof of separate administrative and recovery domains, or a documented residual-risk decision with compensating controls.
4. Demonstration that no one principal can both approve an operation and alter the authoritative approval record or its only audit evidence.
5. Demonstration that registry administrators cannot rewrite/roll back the witness and witness administrators cannot write registry events or approvals.
6. Demonstration that deployers cannot self-approve privileged code or change the identity policy that authorizes their own deployment.
7. Dual-control break-glass and restore/resume evidence, including external audit records.
8. Negative tests for every scenario in section 5, run only in an approved synthetic environment.
9. Dated independent reviewer sign-off, exact configuration/version identifiers, evidence hashes, exceptions, expiry, and accountable owner.

A diagram, provider marketing page, separate project name, different service account name, or policy document alone is insufficient. If any critical administrative relationship remains unknown, record UNKNOWN and keep the system inactive.

## 7. Cross-document consistency updates

This audit sharpens, but does not replace, existing requirements:
- Trust-root architecture section 6 already requires independence tests and effective-permission evidence; this audit adds the administrative dependency graph and correlated-compromise cases.
- Backend-selection framework section 3 already warns that multiple services under one administrator credential are not independent; this audit makes transitive root/recovery dependencies explicit.
- Implementation-readiness Gate C9 already requires administrators, credentials, and recovery procedures to be documented; this audit defines the minimum inventory and evidence.
- Threat T-26 already covers admin/root compromise; this audit expands it to common identity, deployment, witness-retention, audit, billing, and recovery paths.
- Backup restore and anti-rollback requirements remain unchanged: no restore may resume privileged operations without independent witness reconciliation and separate human authorization.

No provider or architecture topology is selected by this audit.

## 8. Current status and hard boundary

- Logical trust domains are documented; actual administrative identities and effective permissions are not established.
- No approval channel, identity tenant, registry, checkpoint witness, audit destination, or recovery service is selected or provisioned.
- No credentials, keys, accounts, infrastructure, or permission changes were made.
- No tests, scripts, workflows, dispatch, scheduling, VPS access, or research operations were run.
- The agent remains non-operational.
- The active Phase 3 G0-05 handoff remains authoritative.

This is a targeted documentation audit, not an exhaustive cloud-configuration review, penetration test, security certification, or authorization to activate the agent.
