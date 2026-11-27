# Research-data integrity, access-control and privacy audit — 2026-11-27

## Status and authority

Targeted documentation-only audit of future research-data access, evidence handling, immutable source preservation, worker input/output boundaries, privacy, retention, and deletion.

This audit does not inspect or copy protected research datasets, open databases, access the VPS, enumerate secrets, change file permissions, alter data, add code, create workflows, configure storage, or select a data provider. It does not run tests, scripts, queries, scans, or research computations. The active Phase 3 G0-05 handoff remains controlling. No research data, definitions, manifests, permissions, secrets, or infrastructure were changed. The agent remains non-operational.

## Executive assessment

The agent's source-level safety design limits task operations and the worker-isolation design calls for minimal immutable inputs, no ambient secrets, deny-all network, and quarantined outputs. Evidence-pipeline documents also recognize that caller-supplied manifests and mutable paths do not establish trusted source custody. These are design controls, not proof of a deployed data-access boundary.

No operational data catalog, authoritative classification, task-to-file authorization service, immutable evidence store, source snapshot service, privacy/retention policy, or independently enforced read-only mount has been established. A worker must not be trusted to enforce its own data permissions or to preserve the integrity of files it can access.

## Findings and required resolutions

### DATA-01 — No authoritative research-data inventory and classification (P0)

Before any future data access, create a versioned inventory of the approved datasets and source objects. For each dataset, record owner, authoritative source, purpose, phase, allowed operations, sensitivity/classification, schema/version, provenance, update cadence, retention, region, access roles, integrity mechanism, and approved consumers.

Define a closed classification scheme at minimum distinguishing public/reference material, internal research material, restricted operational data, credentials/secrets, and personal or regulated information. Classification must be based on actual content and obligations, not merely directory name or file extension. Mixed-content objects inherit the strictest applicable controls unless an independently reviewed field-level policy proves safe separation.

Unknown owner, origin, classification, license, or permitted use means deny access pending review. A repository checkout is not automatically a data catalog or authorization grant.

### DATA-02 — Task-specific data authorization must be independent and exact (P0)

A task's prose scope is not an access-control mechanism. Before any worker starts, a trusted authorization layer must resolve the exact task revision into an immutable input manifest containing approved object identities, versions, digests, byte limits, allowed operations, and purpose.

Enforce authorization outside the worker using isolated per-assignment mounts or object capabilities:
- default deny for all paths, buckets, databases, tables, and objects;
- explicit exact-object allowlists, not broad directory or wildcard grants;
- read-only access for research source inputs;
- no access to credentials, home directories, unrelated repository content, other assignments, private user files, or host metadata;
- no worker ability to widen, replace, or reinterpret its manifest;
- short-lived access bound to task, assignment revision, worker identity, and expiry;
- revocation and expiry enforced by the storage/runtime boundary, not a cooperative process.

Any path not explicitly in the signed/trusted manifest is inaccessible. A task cannot grant itself data access, and a worker return cannot prove which files it actually read.

### DATA-03 — Original research evidence needs immutable custody (P0)

Preserve original inputs as immutable, versioned objects. Record receiver/source identity, source URI or repository identity, exact commit/tree/object version, byte length, cryptographic digest, acquisition time, trusted receiver time, schema, and custody history. For Git sources, preserve tree semantics, modes, symlinks, submodules, LFS pointers, and path encoding. For database exports, record query/export definition, snapshot or transaction identity, schema, timezone, row counts, and consistency boundary.

Use separate source, normalized/derived, and worker-output namespaces. A derived dataset must point to its parent objects and transformation definition; it must never overwrite or masquerade as original evidence. Corrections create new versions with explicit supersession links, not in-place edits. Hashes prove byte equality only relative to trusted custody; they do not prove the source is true or complete.

### DATA-04 — Read-only must be enforced below application code (P0)

A Python API or task instruction saying "read-only" is insufficient. Future source data should be mounted or exposed through a platform-enforced read-only interface with no write/delete/rename/permission-change capability. The worker must have no source-store credentials, database write role, repository push token, host mount, Docker socket, or storage-administrator API.

Test the boundary against direct system calls, symlinks, hard links, path traversal, alternate encodings, case-fold collisions, temporary files, database journal/WAL files, sidecars, memory-mapped files, and subprocesses. Read-only access must not permit mutation through a second path or shared writable cache. If a source format requires writable scratch state, copy only the minimum required input into a separate disposable scratch volume; never put scratch on the authoritative source mount.

### DATA-05 — Database and snapshot consistency require explicit controls (P0)

No live research database was inspected in this audit. Before any database access, document each engine and storage format, transaction/snapshot semantics, journal/WAL behavior, encryption, schema, access roles, backup and restore path, and concurrent-writer model.

Provide a consistent read snapshot or immutable export with an exact snapshot identity. Do not let a worker open an authoritative SQLite database in a mode that may create or modify journals, WAL, SHM, lock, or metadata files. A read-only flag alone must be verified against the actual mount and filesystem permissions. Avoid live database files when a consistent immutable export is available. Never copy credentials or production connection strings into worker inputs.

A partial export, inconsistent snapshot, unknown timezone, schema mismatch, or concurrent update must be recorded as incomplete/UNKNOWN, not treated as a complete research sample.

### DATA-06 — Data lineage and transformation provenance must be first-class (P1)

Every derived object should carry a lineage record binding:
- parent object IDs, versions, and digests;
- exact task and assignment revision;
- source commit/tree or database snapshot identity;
- transformation code and configuration digests;
- runtime image, dependency lock, and policy digests;
- parameters, random seeds where applicable, and time boundaries;
- row/object counts and deterministic validation summaries;
- creation time and trusted producer identity;
- output object ID, byte length, and digest.

Separate worker-declared lineage from independently collected runtime facts. Do not infer source completeness, correctness, or reproducibility from a worker's narrative. Missing parent, changed input, unknown code version, or unbound output blocks promotion into trusted research evidence.

### DATA-07 — Data minimization and privacy controls are not operationally established (P0)

Before data access, perform a purpose and privacy review for each dataset. Determine whether it contains personal information, account identifiers, credentials, contact details, user-generated content, commercially sensitive information, or regulated records. Do not infer that market or exchange data is non-sensitive merely because it is financial or historical.

Minimize fields and rows to the approved task. Prefer pseudonymous stable identifiers or aggregation when exact identity is not required. Keep re-identification keys outside the worker boundary. Prohibit collection of unrelated personal data and secrets. Do not place raw restricted data in prompts, logs, issue comments, email/notification payloads, or public artifacts.

Define lawful basis/contractual permission where applicable, data residency, cross-border transfer restrictions, processor/subprocessor terms, encryption, access audit, retention, deletion, incident notification, and data-subject obligations with the owner/legal reviewer before any regulated or personal data is processed. Unknown obligations are a blocker.

### DATA-08 — Worker outputs and derived artifacts must be quarantined (P0)

Treat every worker-created file, report, notebook, archive, database, executable, and metadata field as untrusted. Write only to a per-assignment quarantine area with hard byte/file/count limits and no path into source storage. No output is automatically merged, copied into canonical datasets, executed, rendered with active content, or used as a new task input.

Before reviewer access, validate archive expansion limits, file count, path safety, symlink and hard-link behavior, MIME/type, encoding, parser safety, executable bits, embedded macros/scripts, nested archives, decompression bombs, and secret leakage. Do not execute or open active content in a privileged reviewer environment. Preserve raw bytes and digest before parsing; sanitized previews are separate derived objects.

A reviewer may inspect quarantined output. Promotion to a trusted evidence namespace requires an explicit human disposition and a separate authorized promotion operation bound to exact output digests. Human task acceptance and research-gate closure remain separate.

### DATA-09 — Cross-assignment and cross-tenant isolation must be proven (P0)

Every assignment receives a unique data namespace and scratch volume. Deny discovery or access to other assignments' inputs, outputs, caches, logs, process state, temporary directories, environment variables, and metadata. No shared writable cache or database is allowed across trust levels. Shared immutable objects may be deduplicated only behind an authorization check that does not reveal object existence or metadata to unauthorized workers.

Enforce isolation at the host/provider boundary, not only by unique directory names. Validate cleanup after normal completion, timeout, crash, cancellation, and emergency hold. Residual volumes, snapshots, swap, crash dumps, logs, and cache entries require an explicit retention/deletion policy and verifiable cleanup evidence.

### DATA-10 — Secret and credential non-disclosure requires independent controls (P0)

Worker inputs must contain no long-lived credentials, tokens, signing keys, provider API secrets, repository write tokens, database passwords, or cloud metadata access. Do not inject secrets as environment variables, mounted files, command-line arguments, task payloads, or inherited process state.

If a future task genuinely requires access to a protected external resource, use a separate broker with narrowly scoped, short-lived, audience-bound capabilities and independently approved operations. Prefer a brokered data export over giving the worker a credential. Egress remains deny-all by default; any exception must be separately reviewed, destination-allowlisted, logged, time-bounded, and incapable of reaching arbitrary hosts or metadata services.

Scan outbound artifacts and logs for secret patterns, but do not treat scanners as a substitute for preventing secret access. A suspected leak triggers quarantine and credential-containment procedures; never automatically rotate/reissue credentials from worker code.

### DATA-11 — Retention, deletion, legal hold, and backups need a coherent policy (P1)

Define separate retention schedules for authoritative source snapshots, derived data, raw worker returns, quarantined outputs, promoted evidence, logs, backups, and incident records. Include owner, purpose, legal/contractual minimums, maximum retention, deletion method, backup expiry, and proof of deletion.

Deletion must be authorized, scoped to immutable object IDs, idempotent, audited, and prevented where legal hold or unresolved incident evidence applies. A worker cannot delete source evidence or shorten retention. Backup and replicated copies must follow the same policy; deleting a primary object while recoverable copies remain is not complete deletion. Restore must preserve object identity, lineage, access controls, and anti-rollback witness checks.

Do not select arbitrary retention periods before owner, legal, and data-residency review.

### DATA-12 — Integrity, availability, and privacy incidents need detection and response (P1)

Connect data events to the observability plane using object IDs and digests, not raw sensitive content. Detect unexpected source mutation, manifest drift, missing objects, checksum mismatch, unauthorized reads, access outside the task manifest, abnormal read volume, export spikes, cross-assignment access, secret exposure, retention bypass, and incomplete deletion.

Define evidence-preserving runbooks for source corruption, accidental overwrite, suspected exfiltration, privacy incident, credential exposure, compromised worker, and restore divergence. Preserve original bytes and access logs; contain through independently authorized deny-only controls; identify affected objects, tasks, assignments, recipients, and copies; notify the appropriate owner/security/privacy authority; and resume only through the separate readiness and human-authorization process.

Monitoring must not reveal sensitive payloads or become a second data-exfiltration path.

### DATA-13 — Data access must be bounded and observable (P1)

Record every grant, read session, object access, export, denial, revocation, and cleanup using authenticated platform identity and immutable task/assignment/object identifiers. Capture trusted receiver time, operation, byte/row count, policy version, input-manifest digest, and outcome. Avoid logging raw values or secret-bearing query parameters.

Set owner-approved per-task limits for object count, bytes, rows, query cost, duration, and export size. Exceeding a limit stops access and raises an alert; it does not authorize automatic expansion. Detect bulk enumeration and repeated denied-path probing. Ensure audit logs are outside worker control and retained independently.

### DATA-14 — Synthetic data-boundary validation is mandatory before access (P1)

Create synthetic-only tests proving:
1. An unlisted path/object is denied even when guessed.
2. A task cannot add a path or broaden a wildcard in its own payload.
3. Read-only mount rejects write, rename, delete, chmod, link, and metadata mutation.
4. Symlink, hard-link, traversal, Unicode normalization, case-fold, and alternate-separator escapes are denied.
5. SQLite or other database access cannot create/modify journal, WAL, SHM, lock, or sidecar files on source.
6. Snapshot consistency detects concurrent changes or incomplete export.
7. Worker A cannot enumerate/read Worker B's input, output, cache, logs, or scratch.
8. Scratch cleanup is verified after timeout, crash, and cancellation.
9. Secret values and metadata endpoints are inaccessible to the worker.
10. Egress denial prevents exfiltration and arbitrary DNS/proxy bypass.
11. Output archive traversal, symlink, executable, macro, oversized and decompression-bomb cases are quarantined.
12. Source object digest changes are detected and original bytes remain available.
13. Derived data without complete lineage cannot be promoted.
14. Sensitive fields are minimized or pseudonymized before worker access.
15. Retention expiry and legal hold are enforced across replicas and backups.
16. Deletion request cannot remove held evidence or silently leave recoverable copies.
17. Access log tampering or monitoring outage is independently detected.
18. A privacy/security incident during emergency freeze cannot use alert acknowledgement to authorize access or resume.
19. Output secret scanning detects seeded canaries without disclosing the canary in alert text.
20. A restore from stale or divergent backup cannot silently change source identity or authorization.

Oracles must prove default-deny access, source immutability, assignment isolation, no ambient secrets, lineage completeness, privacy minimization, and no worker authority to promote/delete/reclassify data. No tests are run or authorized by this document.

## Minimum trusted data-access manifest

A future per-assignment manifest should be immutable and versioned and include:
- manifest ID, schema version, policy version, and canonical digest;
- repository/source namespace and immutable commit/tree/snapshot identity;
- exact object IDs/paths, versions, digests, byte lengths, and classifications;
- approved purpose, task ID/digest, assignment ID/revision, worker identity, and expiry;
- permitted operations and explicit denied capabilities;
- schema/format and snapshot consistency metadata;
- privacy review and minimization decision reference;
- parent/derived lineage references where applicable;
- trusted issuer identity and signature/receipt.

The worker must not be able to alter the manifest or use it as a bearer token outside its exact assignment. The manifest authorizes only the enumerated read capabilities; it does not authorize dispatch, task completion, data promotion, or research-gate closure.

## Current status and non-claims

This is a targeted architecture and source-contract audit, not a live data inventory, privacy assessment, access-control test, database inspection, or integrity scan. No protected research dataset or VPS data was accessed. No data was copied, modified, deleted, classified, or exported. No privacy/legal determination, storage provider, region, retention schedule, access broker, or evidence store was selected. No code, tests, scripts, workflows, permissions, credentials, or integrations were changed or run. The agent remains non-operational, no unattended work is running, and Phase 3 G0-05 remains controlling.
