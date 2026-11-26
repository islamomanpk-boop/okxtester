# Threat model and failure-injection matrix

## Status, scope, and authority

**Design-only threat analysis and proposed future validation plan.** This document grants no implementation, execution, dispatch, persistence, workflow, scheduling, test, failure-injection, gate-closure, or phase-advancement authority.

The current Phase 3 G0-05 handoff remains controlling. It prohibits running the relevant scripts, tests, and workflows and prohibits research code/data changes. This document is limited to the isolated agent-design area. No test or failure injection described below has been run.

The scope is the proposed research-agent lifecycle: trusted task definition, assignment preparation, human approval, dispatch, delivery, worker return, evidence verification, supervisor review, human disposition, event recording, and recovery. A trusted assignment registry and dispatcher are assumed as future components; neither currently exists.

## Security objectives

1. Preserve integrity and availability of the protected research branch and canonical research data.
2. Require authenticated, current, narrowly scoped approval before any protected operation.
3. Bind assignment, approval, dispatch, return, review, and disposition to immutable identities and exact content digests.
4. Prevent replay, duplicate, stale, concurrent, and uncertain requests from causing duplicate work or silent state changes.
5. Treat worker-controlled content and metadata as untrusted until independently authenticated and verified.
6. Preserve an auditable lifecycle history with a protected checkpoint and recoverable transaction semantics.
7. Keep task acceptance, research-gate closure, and phase advancement as separate human authorities.
8. Fail closed when identity, policy, handoff, provenance, persistence, or delivery state cannot be established.

## Protected assets

| Asset | Required property | Compromise consequence |
|---|---|---|
| Canonical research branch and source data | Integrity, availability, provenance | Research contamination or loss |
| Current handoff and phase/gate policy | Integrity, freshness, authority | Prohibited work or premature advancement |
| Trusted queue and task digests | Integrity, uniqueness | Unauthorized or altered assignments |
| Assignment package bytes and digest | Immutable binding | Worker receives scope different from reviewed scope |
| Human approval and revocation records | Authenticity, scope, freshness | Unauthorized operation |
| Workflow identity and pinned revision | Authenticity, integrity | Forged provenance or malicious execution |
| Worker identity and delivery receipt | Authenticity, attribution | Spoofed worker or false delivery state |
| Evidence bytes and commit manifest | Integrity, provenance | Fabricated or mismatched evidence |
| Registry, event log, idempotency index | Integrity, atomicity, durability | Lost, duplicated, contradictory lifecycle |
| Protected checkpoint and assignment version | Rollback resistance, concurrency | Replayed state or conflicting transitions |
| Artifact storage and review records | Integrity, provenance, availability | False completion evidence |
| Secrets and service identities | Confidentiality, least privilege | Privilege escalation or impersonation |
| Backups and recovery metadata | Integrity, freshness, recoverability | Undetected rollback or unrecoverable state |

## Actors and trust boundaries

- **Project owner / authorized human approver:** authorizes only the exact operation and scope shown through a separately authenticated approval channel.
- **Supervisor/reviewer:** assesses returned evidence; worker assertions are not verified facts.
- **Worker agent:** outside the trusted registry boundary. Its output, identifiers, timestamps, summaries, action declarations, and hashes are untrusted claims.
- **GitHub repository and Actions platform:** provide platform identities and run metadata only when independently derived from authenticated platform context and checked against pinned policy.
- **Trusted dispatcher:** future privileged component that revalidates approval and handoff policy at the operation boundary and records dispatch/delivery facts.
- **Trusted registry/store:** future authority for immutable assignment revisions, approvals, idempotency, lifecycle events, materialized state, and protected checkpoints.
- **Artifact provider:** stores outputs; artifact existence or filename alone does not authenticate uploader or contents.
- **Repository contributors/maintainers:** legitimate collaborators are not automatically trusted to change protected policy, workflow identity, approval roots, or registry state.
- **External dependencies and Actions:** supply-chain inputs that may be compromised, retagged, or unexpectedly upgraded.
- **Operations/admin personnel:** may restore backups or change settings; privileged mistakes can bypass correct application logic.

## Trust roots and independence requirements

No component may establish its own provenance solely from values it supplies itself.

| Fact / trust root | Must be established by | Must not be accepted solely from |
|---|---|---|
| Human approval identity and intent | Authenticated approval channel with auditable actor identity | Workflow input, queue field, worker message |
| Exact approved operation | Approval bound to task digest, assignment revision, operation, workflow SHA, branch, handoff revision, and input commit | Generic approved flag |
| Workflow identity and revision | Platform run context plus protected expected identity/revision | Worker metadata or artifact manifest |
| Repository/ref/commit | Authenticated platform context and independently checked checkout HEAD | Worker-supplied commit string |
| Handoff and gate status | Authoritative protected research-branch source, re-read at operation boundary | Stale task package or agent-branch copy |
| Assignment/package digest | Trusted registry storing canonical package bytes and digest before dispatch | Worker-returned digest |
| Dispatch and delivery | Authenticated provider response/receipt and stable provider delivery identity | Local sent flag or worker assertion |
| Worker identity | Authenticated delivery/return channel | Name, task ID, or unverified signature field |
| Evidence manifest | Trusted checkout-derived manifest for exact commit | Worker-declared manifest alone |
| Event-log head/checkpoint | Protected registry storage with atomic update and rollback controls | Checkpoint stored beside mutable log |
| Artifact provenance | Authenticated workflow run, expected artifact association, independent file/hash verification | Artifact name, path, or contents alone |
| Backup freshness | Independently protected monotonic checkpoint or equivalent external anchor | Backup-local timestamp alone |

Compromise of a worker or a single workflow must not be sufficient to forge approval, rewrite the protected checkpoint, or manufacture trusted delivery/review provenance. If the platform cannot provide this separation, permissions must be narrowed or the system must remain inactive.

## Threat register

Severity is a proposed impact rating; likelihood is unassessed. Controls below are requirements to verify, not claims that they are implemented.

| ID | Threat / attack path | Impact | Required prevention and detection | Recovery / residual risk |
|---|---|---|---|---|
| T-01 | Compromised worker fabricates findings, IDs, hashes, timestamps, or completion claims | False audit trail; unsafe decision | Treat returns as declarations; bind to trusted assignment; verify bytes against independently derived manifest; retain raw return | Quarantine and request revision; research correctness still needs human review |
| T-02 | Worker changes scope or package after approval | Unauthorized work | Store canonical package bytes/digest in registry; compare complete package at return; immutable revision IDs | Revoke assignment and investigate deliveries from that revision |
| T-03 | Stolen, replayed, expired, or over-broad approval | Unauthorized operation | Strong approver authentication; operation/scope-bound approval; expiry, revocation, nonce/single-use policy; recheck at dispatch boundary | Revoke approval/credentials; reconcile any possibly started operation |
| T-04 | Contributor changes policy, queue, workflow, or allowlist | Privilege escalation | Protected branches/reviews; narrow write permissions; immutable workflow SHA; policy digest; independent approval root | Disable dispatch; compare trusted refs and restore verified source |
| T-05 | Compromised workflow or impersonated workflow identity | Forged provenance or unauthorized dispatch | Pin workflow identity/revision; least-privilege token; protected environment approval; independently verify run context | Suspend workflow, rotate credentials, assess registry exposure |
| T-06 | Compromised GitHub App, token, or provider integration | Forged events, approvals, returns, or delivery | Separate identities/permissions; short-lived credentials; scoped installation; audit logs; registry credentials unavailable to worker | Revoke integration, rotate secrets, reconcile provider records |
| T-07 | Actions/dependency supply-chain compromise or mutable tags | Malicious execution or evidence manipulation | Pin third-party actions by immutable commit SHA; constrain dependencies; review upgrades; provenance/SBOM where available | Disable affected workflow and rotate exposed credentials |
| T-08 | Duplicate identical delivery or webhook retry | Duplicate work or events | Stable source-namespace/delivery-ID/event-role key; replay lookup before stale-check; exact-facts comparison | Return original committed receipt; no second transition |
| T-09 | Reused delivery ID with changed facts | Conflicting or forged lifecycle event | Compare all normalized facts; reject changed replay and alert | Quarantine source; preserve attempted facts and original receipt |
| T-10 | Concurrent dispatches or registry writers | Double dispatch, lost update, inconsistent sequence | Atomic global checkpoint and per-assignment CAS; uniqueness constraints; transaction over state/event/index/checkpoint | Re-read committed winner and reconcile; never assume both succeeded |
| T-11 | Response lost after commit | Retry duplicates action | Persist receipt with idempotency key; replay query before stale-check; respond only after commit | Query by idempotency key; do not create new delivery identity |
| T-12 | Crash before/during commit or partial persistence | Orphan state or inconsistent index | One atomic transaction for assignment state, event, idempotency index, checkpoint | Roll back uncommitted transaction; verify post-restart invariants |
| T-13 | Stale global checkpoint or assignment version | Overwrite or out-of-order transition | Check both versions inside transaction; reject stale new writes; exact committed replay remains idempotent | Reload authoritative state and re-evaluate |
| T-14 | Approval expires or is revoked during dispatch race | Work proceeds after authority withdrawn | Define linearization point; revalidate at protected operation boundary; serialize/reconcile revoke versus dispatch | If remote start ambiguous, mark uncertain and manually reconcile |
| T-15 | Cancellation races with dispatch | Incorrect cancelled/delivered state | Atomic transition and explicit race semantics; provider cancellation receipt; local cancellation is not proof of remote retraction | Preserve both facts; reconcile provider state; no automatic redispatch |
| T-16 | Worker spoofs task/assignment/return identity | Return attached to wrong work | Authenticated return channel; assignment-bound nonce/receipt; verify revision and package digest from registry | Reject and quarantine; investigate credential compromise |
| T-17 | Malformed, deeply nested, non-finite, oversized, or schema-drifted return | Parser crash, validation bypass, resource exhaustion | Strict schema, duplicate-key rejection, size/depth limits, finite numbers, safe paths, fail-closed parser | Retain bounded raw evidence securely; return for revision |
| T-18 | Evidence manifest or bytes altered/mismatched | False provenance or substitution | Derive manifest from exact checkout; recompute each hash; verify HEAD and clean checkout independently | Mark invalid; preserve mismatch and request new evidence |
| T-19 | Artifact spoofing, substitution, or wrong run association | False completion evidence | Verify provider/run association, expected name, exact file set, hashes, embedded manifest, trusted context | Quarantine; reacquire from authenticated run |
| T-20 | Store outage, partition, or provider timeout | Unknown commit/delivery state | Explicit pending/unknown state; durable idempotency; no automatic retry when delivery uncertain | Query authoritative store/provider; manual reconciliation if unprovable |
| T-21 | Event-chain corruption or checkpoint tampering | Audit history untrustworthy | Hash-chain verification; checkpoint outside mutable log; independent monitoring and backups | Freeze lifecycle; restore only from independently anchored history |
| T-22 | Backup rollback or stale database restore | Replayed approvals/events; lost revocations | Monotonic external checkpoint/epoch; backup freshness verification; restore drills; key separation | Remain inactive until external-anchor and provider reconciliation succeeds |
| T-23 | Cross-runtime canonicalization mismatch | Digest/signature ambiguity | Explicit canonicalization version; shared cross-language vectors; preserve v1 semantics; domain separation | Reject mismatch; never silently rehash historical events |
| T-24 | Rate limits, quota, or concurrency exhaustion | Delayed work or denial of service | Bounded batch, backoff, queue limits, per-source quotas, observable retry state | Pause safely; resume from trusted state without changing delivery identity |
| T-25 | Accidental operator error or mistaken approval | Unintended work or irreversible transition | Human-readable exact scope; operation-bound confirmation; separation of duties for high impact | Revoke before dispatch where provable; otherwise reconcile |
| T-26 | Admin or registry-root compromise | Full lifecycle forgery or protected-state alteration | Separate admin/runtime identities; managed or hardware-backed keys where feasible; dual control; external audit/checkpoint anchor | Critical incident: suspend automation, rotate trust roots, independently reconstruct history |

### Risk priorities

**Critical design blockers before live dispatch:** T-02, T-03, T-05, T-06, T-10, T-11, T-12, T-14, T-15, T-20, T-21, T-22, T-26.

**High-priority validation before worker returns can influence disposition:** T-01, T-08, T-09, T-16, T-17, T-18, T-19, T-23.

**Operational resilience and hygiene:** T-04, T-07, T-24, T-25.

No likelihood estimate, quantitative risk score, or residual-risk acceptance is made. Risk acceptance requires explicit project-owner approval after platform, backend, identity model, and workflow topology are selected.

## Failure-injection matrix

This is a future test plan only. Expected results are test oracles, not evidence that implementation currently meets them.

| ID | Injected condition | Expected safe oracle | Evidence to retain |
|---|---|---|---|
| F-01 | Process terminates before transaction begins | No state/event/index/checkpoint change | Before/after registry snapshot |
| F-02 | Termination after event construction but before commit | No partial durable transition | Rollback record and unchanged checkpoint |
| F-03 | Termination during commit | All-or-nothing result | Transaction outcome and post-restart invariants |
| F-04 | Commit succeeds but response is dropped | Retry returns original receipt; no second event/delivery | Idempotency key, receipt, event count |
| F-05 | Identical delivery submitted repeatedly | One logical transition; same receipt returned | Request facts and receipt identity |
| F-06 | Same delivery ID replayed with changed facts | Reject and alert; original unchanged | Original and rejected normalized facts |
| F-07 | Two writers append against same global checkpoint | At most one new transition wins | Request IDs, CAS outcomes, final sequence |
| F-08 | Two writers change same assignment version | At most one conflicting transition wins | Assignment version and conflict response |
| F-09 | Stale checkpoint with exact committed replay | Original receipt returned; no duplicate append | Replay lookup and unchanged event head |
| F-10 | Stale checkpoint for new delivery | Conflict; no mutation | Expected/current checkpoint and state |
| F-11 | Approval expires immediately before dispatch | Dispatch denied | Expiry, boundary decision, no provider request |
| F-12 | Approval revoked concurrently with dispatch | Defined serialized outcome; ambiguous remote start becomes uncertain | Registry order and provider receipt/query |
| F-13 | Cancellation races with provider acceptance | Preserve both observations; cancellation not treated as proof of non-delivery | Cancel request, provider response, final state |
| F-14 | Worker returns different package/assignment digest | Reject binding; no completion/gate approval | Registry digest and received digest |
| F-15 | Worker spoofs task, assignment, or delivery receipt | Reject identity mismatch | Authenticated channel identity and rejected payload |
| F-16 | Evidence path is absolute, traversal, drive path, symlink escape, or contains controls | Reject unsafe reference | Raw path and validator disposition |
| F-17 | Duplicate JSON keys, NaN/Infinity, excessive nesting, or oversized return | Bounded fail-closed rejection without crash | Parser result and bounded diagnostic |
| F-18 | Evidence bytes differ from trusted commit manifest | Verification fails; return for revision | Expected/actual hashes and commit context |
| F-19 | Checkout HEAD differs or checkout is dirty | Provenance verification fails | Expected/actual HEAD and dirty status |
| F-20 | Artifact missing/extra/altered files or wrong run association | Artifact verification rejects | Artifact metadata, inventory, hashes |
| F-21 | Store unavailable before request | No dispatch; blocked/unavailable result | Store error and proof no provider call occurred |
| F-22 | Store times out after possible commit | Unknown until idempotency/provider reconciliation; no fresh retry identity | Request identity, provider status, registry query |
| F-23 | Event hash modified or event removed/reordered | Chain verification fails; lifecycle actions freeze | First failing sequence and protected checkpoint |
| F-24 | Checkpoint rolled back with stale backup | Detect against independent anchor; remain inactive | Backup epoch, external anchor, reconciliation |
| F-25 | Canonical JSON generated by second runtime | Shared vectors match or version mismatch is rejected | Runtime versions, vectors, canonical bytes/hashes |
| F-26 | Approval key, workflow token, or worker credential revoked mid-session | New boundary actions denied; active/uncertain operations reconciled | Revocation time, identity, operation outcomes |
| F-27 | API quota/rate or concurrency limit reached | Bounded pause/backoff; no lost task or duplicate dispatch | Provider response, queue state, retry record |
| F-28 | Workflow disabled, wrong revision/branch, or excessive permissions | Preflight denies before protected operation | Run context, policy comparison, permission snapshot |
| F-29 | Valid-schema event comes from wrong source identity | Authentication rejects before registry append | Verified principal and rejected request |
| F-30 | Human task acceptance is submitted as phase-gate closure | Reject authority mismatch; gate remains unchanged | Assignment review, disposition, separate gate state |

### Invariants across all injections

- Failed or uncertain operations never silently become accepted.
- A new transition is committed atomically with its event, idempotency index, and protected checkpoint.
- Exact replay is idempotent; changed replay is rejected.
- Global and per-assignment concurrency versions are checked at the same transaction boundary.
- Approval is never inferred from task labels, queue content, workflow inputs, worker returns, or artifact metadata.
- Dispatch requires live handoff and exact approval revalidation at the operation boundary.
- Uncertain delivery is reconciled, never automatically retried.
- Worker claims never replace independently derived platform, checkout, registry, or provider facts.
- Evidence integrity does not establish research correctness.
- Task acceptance does not close a research gate; gate closure needs its own authorized human decision.
- Backup recovery must reconcile against an independent monotonic trust anchor before lifecycle actions resume.

## Proposed validation sequence

1. Freeze the threat-model version and select topology, registry backend, approval channel, service identities, artifact provider, and backup model.
2. Map every trust root to an independently authenticated source; any missing root is a hard blocker.
3. Specify transaction linearization points for approval/revocation, dispatch/cancellation, replay, return receipt, and human disposition.
4. Implement registry/store and dispatcher only after explicit authorization and after the controlling research handoff permits the exact scope.
5. Create deterministic unit tests for schemas, canonicalization vectors, idempotency, transitions, and authority separation.
6. Create isolated integration tests using a disposable registry and mock provider; inject crashes and network faults at each transaction boundary.
7. Test concurrency for duplicate delivery, global checkpoint races, assignment races, and cancellation/dispatch races.
8. Test restart, store outage, corrupted chain, stale-backup restore, and independent checkpoint reconciliation.
9. Independently review test code, fixtures, oracles, permissions, and workflow identity before any live manual readiness workflow.
10. Keep production dispatch, event-driven triggers, and scheduled operation as separate approvals after manual validation.

## Validation stop conditions

The system remains inactive if any of the following holds: approver or worker identity cannot be authenticated; approval is not bound to exact operation/scope; workflow identity is not pinned; package digest is not independently retained; no atomic registry transaction exists; no protected checkpoint independent of the mutable log exists; delivery provider is non-idempotent or unqueryable; delivery uncertainty is unresolved; evidence manifest cannot be independently derived; canonicalization is ambiguous; or backup restore lacks a trustworthy anti-rollback anchor.

## Current project reality

- Current modules are pure/preparatory components. They do not implement the trusted registry, durable transaction, authenticated approval channel, dispatcher, or delivery receiver.
- The v1 event ledger remains unchanged; v2 lifecycle and unified transaction documents are proposals only.
- The actual default branch is main; a workflow existing only on the agent branch is insufficient for manual dispatch. No main-branch activation bridge or separate agent repository is authorized.
- No agent-specific workflow is active and no unattended worker is running.
- The Phase 3 G0-05 handoff remains authoritative. No scripts, tests, workflows, or failure-injection scenarios were executed for this document.
- No research code/data, canonical definitions, protected research branch, default branch, secrets, permissions, VPS, or runner configuration were changed.

This document is a threat-analysis and validation-planning artifact, not security certification, runtime-readiness evidence, or permission to activate the agent.
