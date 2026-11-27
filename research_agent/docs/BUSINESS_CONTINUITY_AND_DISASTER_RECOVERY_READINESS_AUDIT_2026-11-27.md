# Business continuity and disaster-recovery readiness audit — 2026-11-27

## Status and authority

Documentation-only architecture audit of continuity objectives, failure domains, recovery ordering, degraded modes, restore evidence, and safe resumption for a future OKX research agent.

This audit does not inspect or change live infrastructure, VPS state, databases, backups, credentials, GitHub settings, provider accounts, or research datasets. It does not provision a service, select a vendor, configure replication, restore data, execute tests, scripts, workflows, failover, or provider calls. The active Phase 3 G0-05 handoff remains controlling. No operational work is authorized by this document. The agent remains non-operational.

## Executive assessment

The repository now contains substantial design work for event-ledger persistence, witness reconciliation, backup restore, provider dispatch recovery, callback ordering, worker isolation, and emergency suspension. These documents define important pieces, but they do not establish an operational continuity capability.

There is no selected production registry, independent witness, backup provider, worker runtime, callback receiver, notification channel, recovery operator roster, recovery-time objective (RTO), recovery-point objective (RPO), tested restore procedure, or service-level commitment. A written recovery design is not evidence that backups exist, are complete, are restorable, or can be recovered without rollback.

The governing recovery posture must be: preserve evidence, fail closed, reconcile every external side effect, and resume only the least capable safe mode. Availability must never override authorization, data integrity, or the G0-05 prohibition.

## Findings and required resolutions

### BCR-01 — No approved continuity objectives or service criticality model (P0)

Before selecting infrastructure, the owner must classify each component by business criticality and define approved RTO/RPO ranges, maximum tolerable data loss, maximum tolerable uncertainty, maintenance windows, and dependency objectives. Define these separately for:
- trusted assignment/approval registry;
- append-only event ledger and independent witness;
- immutable task/package and input evidence custody;
- provider dispatch and callback receipt history;
- worker execution and scratch;
- reports/artifacts and reviewer access;
- monitoring, alerting, identity, and key-management dependencies.

A single system-wide uptime target is insufficient. The registry, approval state, and dispatch history require stricter integrity and recovery properties than disposable worker compute. If objectives cannot be met, the component must remain unavailable rather than silently weaken its guarantees.

### BCR-02 — Failure domains and common-mode dependencies are not operationally mapped (P0)

Create a versioned dependency and failure-domain register covering provider regions/zones, cloud accounts, organization administrators, identity providers, DNS, network paths, KMS/HSM, backup control plane, witness, artifact store, GitHub Actions, source repository, notification provider, billing/suspension, and human recovery channels.

For every dependency record its owner, administrative root, credential/recovery path, region, failure modes, detection source, fallback, and whether it shares a common control plane with the protected system. A second region or account is not independent if the same compromised identity, administrator, key, or deployment pipeline can delete or rewrite both.

Unknown common-mode dependencies block claims of independent recovery.

### BCR-03 — Backup completeness and recoverability are unproven (P0)

Define backup classes and schedules for immutable registry records, event history, idempotency indexes, assignment/package digests, approval issuance and revocation facts, dispatch attempts, raw provider receipts/callbacks, worker returns, evidence manifests, artifact metadata, policy versions, and independent witness receipts.

Backups must be encrypted, access-separated, immutable or retention-locked where appropriate, independently monitored, and protected against deletion by production administrators. Record exact backup generation, source checkpoint, object counts, byte counts, digest roots, encryption-key version, retention, and restore-test result. A successful backup job or object listing does not prove a complete recoverable backup.

Do not back up ephemeral worker scratch as if it were authoritative evidence. Preserve required forensic evidence under a separate incident-retention policy.

### BCR-04 — Recovery-point consistency must span all coupled records (P0)

A recoverable checkpoint is not just a database snapshot. It must bind the registry state, event sequence/head, idempotency/delivery indexes, package and approval facts, dispatch attempts, callback/return receipts, witness checkpoint, policy version, and immutable evidence references.

The backup protocol must establish a consistent cut across those records. If systems cannot participate in one transaction, use explicit prepare/checkpoint/receipt barriers and record which sources are ahead, behind, or pending. Never infer consistency from matching wall-clock timestamps.

Any missing event, unexplained sequence gap, fork, duplicate identity with changed facts, missing evidence object, or checkpoint mismatch means recovery is blocked pending reconciliation.

### BCR-05 — Restore must be staged, isolated, and non-dispatching (P0)

Restore into an isolated recovery environment with no provider egress, no worker dispatch, no schedule, no repository write token, and no ability to mutate production state. Verify image/build provenance, policy version, encryption keys, schema migrations, backup digest, witness checkpoint, and all referenced evidence before exposing restored state.

The first restored mode must be read-only and non-dispatching. Do not attach production credentials or resume callbacks until identity, authorization, and replay controls are independently reviewed. A restore operation must not itself consume approvals, create attempts, advance task states, or resume scheduled work.

Production cutover requires an explicit owner-approved recovery plan, independent reviewer, and separately authorized change. No automatic failover may bypass this gate.

### BCR-06 — External side effects require reconciliation before replay (P0)

For every assignment and provider attempt, reconcile:
- committed dispatch-start identity and exact request digest;
- provider idempotency key, scope, retention, and query capability;
- authenticated provider acceptance/rejection/status receipts;
- callback sequence/cursor and raw receipt custody;
- worker job identity and delivery state;
- cancellation and approval revocation timing;
- return receipt, raw bytes digest, and assignment revision binding.

A timeout, missing receipt, or restored database row does not prove that the provider did not accept the request. Never create a new attempt or new idempotency identity merely because local state was lost. Query the original provider identity where its documented guarantees permit. If status is unavailable, expired, incomplete, or contradictory, retain UNKNOWN/UNCERTAIN and block retry and resumption.

### BCR-07 — Witness outage and checkpoint divergence require explicit degraded modes (P0)

Define distinct states for witness unavailable, database ahead by exactly one durable outbox event, witness ahead of database, multiple unacknowledged events, forked history, invalid receipt, and unknown witness identity.

Only the exact single-successor outbox case already defined in the trusted transaction protocol may be eligible for controlled reconciliation. Protected writes remain frozen while witness acknowledgment is pending. Witness-ahead, multiple pending events, fork, missing outbox, or invalid receipt means read-only hold and independent investigation.

Do not substitute a backup copy of the witness, local hash chain, or database administrator assertion for the independent checkpoint.

### BCR-08 — Identity, key, and policy recovery can invalidate otherwise intact data (P0)

Recovery must account for lost, expired, rotated, revoked, or compromised signing keys; identity-provider outage; MFA/recovery-factor loss; policy rollback; stale workflow revisions; and compromised administrator sessions.

Use independently protected key backups or documented reissuance/revocation ceremonies. Never restore a revoked key or old policy as active merely because it appears in a backup. Reconcile key status and policy version against an independent current source. If authenticity cannot be established, preserve the data but keep all privileged operations denied.

Break-glass access must remain incident-bound, time-limited, dual-controlled, independently logged, and incapable of authorizing dispatch or normal resume. The emergency deny-only plane must remain available independently of the primary registry.

### BCR-09 — Schema migration and software rollback can corrupt lifecycle meaning (P1)

Every persisted schema and event version needs a compatibility matrix and deterministic migration plan. Preserve original immutable records and hashes; migrations create versioned derived representations and must not rewrite historical event bytes or silently change enum meanings.

Test forward-read, backward-read where supported, mixed-version deployment, interrupted migration, duplicate migration, and rollback. A rollback must not downgrade approval/revocation facts, event sequence, witness checkpoint, provider receipts, or assignment revisions. If old software cannot safely interpret newer state, it must refuse writes and enter read-only mode.

Do not perform destructive schema migration during emergency recovery.

### BCR-10 — Recovery sequencing and role separation need executable runbooks (P1)

Create owner-approved runbooks for regional outage, registry corruption, witness outage, identity compromise, key compromise, artifact loss, callback backlog, provider outage, worker-runtime compromise, ransomware, and accidental deletion.

Each runbook must identify trigger/evidence, incident commander, freeze authority, recovery operator, witness verifier, independent reviewer, data/privacy owner, provider liaison, resume approvers, required records, decision points, stop conditions, and communication channel. One person or common credential must not be able to freeze, rewrite history, verify their own restore, and resume dispatch.

Runbooks must distinguish restoring service availability from restoring permission to perform work. Resume from incident hold may restore read-only visibility only; normal task dispatch requires separate current authorization.

### BCR-11 — Monitoring and human communication are themselves failure dependencies (P1)

Define independent detection for missed backups, stale witness, checkpoint lag, callback backlog, artifact retention expiry, restore failure, key expiry, identity-provider outage, region failure, and unacknowledged incident alerts. Monitor-of-monitor and synthetic heartbeat must not depend solely on the system being monitored.

Provide at least two independently controlled alert routes and an escalation path for unavailable primary communications. Alert acknowledgment, silence, ticket closure, or notification failure must never change task authorization, clear a hold, or count as recovery approval. Avoid placing secrets or raw restricted research data in notifications.

### BCR-12 — Capacity, quotas, and cost exhaustion need safe behavior (P1)

Define tested ceilings and reserved capacity for registry transactions, witness publication, callback ingestion, evidence storage, artifact retention, logs, and recovery operations. Protect critical control-plane capacity from worker or report bursts. Apply bounded queues, backpressure, admission control, and explicit overload states.

Quota exhaustion must stop new assignments and preserve existing receipts/state; it must not drop events, silently shorten retention, skip verification, or fall back to weaker storage. Cost limits and billing suspension are part of the failure model, but cost recovery must not bypass authorization.

### BCR-13 — Continuity evidence and restore drills must be independently retained (P1)

Every future drill should produce an immutable record containing scenario ID, environment identity, backup/checkpoint IDs, software/policy versions, start/end trusted times, operators and reviewers, expected/actual RTO/RPO, object/event counts, digest roots, external witness receipts, unresolved discrepancies, and explicit pass/fail/blocked disposition.

A drill passes only if all critical invariants are proven, not merely because a service starts. Keep drill evidence outside the environment under test and prevent the operator from editing or deleting the result. Synthetic exercises must precede any production restore or failover exercise.

### BCR-14 — Data residency, privacy, and incident evidence survive recovery (P1)

Backups, replicas, logs, snapshots, and forensic copies inherit the source data's classification and residency restrictions. Recovery must not move data to an unapproved region or provider. Preserve legal holds and deletion obligations across replicas and backup expiry. Incident evidence must be access-restricted and retained only under an approved schedule.

If the approved recovery location, processor terms, key custody, or cross-border transfer status is unknown, restore only into an isolated environment pending owner/privacy/legal review.

## Minimum recovery checkpoint

A future trusted checkpoint should bind, at minimum:

- repository, branch, exact commit/tree, build/image digest, policy and schema versions;
- registry sequence/head, event-ledger head, idempotency indexes, and independent witness sequence/receipt;
- exact task, assignment revision, task digest, package digest, approval IDs and immutable revocation/consumption facts;
- dispatch attempt IDs, provider request digests, idempotency keys, provider job IDs, raw receipts, callback sequence/cursor, and reconciliation status;
- worker delivery and return receipt identities, raw return digests, evidence object IDs/digests, and reviewer/human disposition references;
- backup IDs, snapshot IDs, object counts/bytes, digest roots, encryption key versions, retention and region;
- trusted checkpoint time, issuer identity/signature, and restore-validation record.

This checkpoint is an integrity reference, not a bearer credential and not an instruction to resume.

## Recovery state decision table

| Observed condition | Permitted posture |
|---|---|
| All protected stores and independent witness agree; evidence references verify | Isolated read-only recovery review |
| Database is exactly one event ahead with matching durable witness outbox | Freeze protected writes; reconcile that exact outbox |
| Witness is ahead, multiple events pending, or any fork/gap exists | Read-only hold; investigate; no replay |
| Provider attempt outcome is unknown or receipt history incomplete | Preserve original attempt identity; query/reconcile; no new attempt |
| Approval/key/policy authenticity or revocation status is unknown | Deny privileged operations; recover trust roots independently |
| Evidence object is missing, digest differs, or lineage is incomplete | Quarantine affected assignment; do not promote or accept |
| Restore drill evidence is missing or reviewer is not independent | Recovery remains BLOCKED |
| Human recovery review passes | May authorize read-only visibility; dispatch still requires separate authorization |

## Synthetic continuity validation matrix

Before any production use, design and execute synthetic-only drills for:

1. Primary region unavailable during a registry transaction.
2. Process crash before and after atomic event commit.
3. Database restored one event behind its independent witness.
4. Database restored exactly one event ahead with a durable outbox.
5. Witness restored behind, ahead, forked, or unavailable.
6. Backup is truncated, stale, corrupted, or missing an object.
7. Backup object digest matches but manifest omits a required object.
8. Provider accepted a dispatch but local receipt persistence failed.
9. Callback arrives during restore or is replayed out of order.
10. Approval revoked while identity service or registry is unavailable.
11. Signing key revoked after backup creation.
12. Schema migration is interrupted halfway through.
13. Old binary starts against a newer event schema.
14. Artifact store is unavailable while worker returns arrive.
15. Notification provider and primary identity provider fail together.
16. Quota or billing suspension occurs during evidence retention.
17. Restored worker environment attempts network egress or dispatch.
18. Recovery operator and witness verifier share an administrative root.
19. Restore location violates data-residency restrictions.
20. Emergency hold is active while a recovery workflow requests service resumption.

Each drill must prove no duplicate provider attempt, no loss or rewrite of immutable evidence, no rollback of approval/revocation or witness state, no cross-assignment data exposure, no dispatch during recovery, and no phase/gate advancement. A passing synthetic drill does not authorize production activation.

## Ordered recovery protocol

1. Detect and declare the incident using independently retained telemetry.
2. Invoke the independent deny-only hold; if it cannot be proven effective, disable dispatcher and registry ingress at the platform boundary.
3. Preserve logs, raw receipts, backups, snapshots, and forensic evidence; prevent routine cleanup.
4. Contain compromised identities, sessions, keys, runners, and provider credentials out of band.
5. Inventory affected components, regions, identities, tasks, assignments, attempts, objects, and external recipients.
6. Select a recovery point only after comparing database state, event history, independent witness, and backup evidence.
7. Restore into isolated, non-dispatching, no-egress environment.
8. Verify build, policy, schema, identity, key, event, witness, package, approval, provider, return, evidence, and retention integrity.
9. Reconcile every in-flight or uncertain provider attempt against its original identity.
10. Obtain independent recovery review and record all discrepancies and residual uncertainty.
11. Keep service in read-only mode unless and until separate human resume authorization is granted.
12. Treat normal activation, new assignments, schedules, and provider dispatch as a separate later authorization decision.

Any failed verification returns to read-only hold or BLOCKED. No operator may waive a missing witness, unknown provider outcome, incomplete evidence, or unverified identity for convenience.

## Current status and non-claims

This audit is a design review only. No RTO/RPO has been approved, no provider or region selected, no backup inspected or created, no restore or failover performed, no continuity drill executed, no key or identity recovered, and no production runbook activated. No code, tests, scripts, workflows, permissions, credentials, data, or infrastructure were changed or run. The agent remains non-operational; no unattended work is running. Phase 3 G0-05 remains controlling.
