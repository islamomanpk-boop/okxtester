# Evidence-pipeline integrity and human-acceptance audit — 2026-11-27

## Scope and authority
Targeted static review of the worker submission schema, evidence verifier, integrated review pipeline, assignment-return binding, review-artifact builder, report/artifact verification contracts, trusted dispatcher/registry designs, and human-disposition lifecycle.

Documentation-only audit. No source code, research data, workflow, permissions, provider, storage, or runtime was changed. No tests, scripts, artifact parsing, uploads, dispatch, or research execution were performed. The active Phase 3 G0-05 handoff remains controlling.

## Executive assessment
The current pure modules have useful layered safeguards: strict submission schemas; closed worker-declared action vocabulary; path and digest shape checks; task/package binding; byte-hash comparison against a supplied commit manifest; structural review before evidence review; in-memory report construction; and explicit separation of review eligibility from task completion and gate closure.

These controls are not yet a trusted end-to-end evidence pipeline. The critical missing element is authenticated, durable custody from the moment raw worker bytes arrive through immutable evidence storage, independent provenance derivation, reviewer inspection, and human disposition. Current verifier inputs and report metadata are supplied by callers; current artifact bundle creation is in-memory; provider delivery and receiver identity are not operational; and no trusted registry persists a complete review record or binds human acceptance to an immutable review digest.

## Findings

### EP-01 — Raw return custody and authenticated receipt are absent (P0)
The current assignment-return API receives an already-parsed Python dictionary. It does not authenticate transport, retain exact raw bytes, compute a receiver-side raw-byte digest, generate a trusted receipt ID, enforce return-delivery idempotency, or persist arrival order and receipt time.

Required:
- Authenticate the return source and derive provider/source namespace, delivery ID, attempt ID, assignment revision, and receipt time from trusted transport context.
- Enforce a raw-byte size limit before buffering; persist exact raw bytes immutably and compute the receiver-side digest before parsing.
- Atomically record receiver-generated return ID, raw digest, authenticated source metadata, idempotency index, lifecycle event, assignment version, and checkpoint before parsing/acknowledgment.
- Parse only retained bytes using strict UTF-8 and strict JSON/schema rules. Preserve malformed bytes with a bounded parse-error record; never discard or silently normalize them.
- Exact duplicate identity/facts returns the original receipt; same identity with changed bytes/facts is quarantined as a security conflict. Different delivery IDs with identical bytes remain separate observed arrivals.

### EP-02 — Evidence verification trusts caller-supplied manifest and checkout bytes (P0)
The evidence verifier checks declared paths and hashes against the manifest and bytes passed to it. It explicitly cannot authenticate their origin, exact checkout, cleanliness, or commit provenance. A well-formed but attacker-selected manifest/byte map can therefore make the pure verifier return verified without proving that the data came from the trusted commit.

Required:
- Derive repository identity, ref, commit SHA, workflow path/revision, run/attempt, checkout state, and file manifest from authenticated platform context and an independently inspected checkout.
- Verify actual checkout HEAD equals the expected immutable commit and prove checkout cleanliness before deriving evidence bytes.
- Build the manifest from the exact Git tree/checkout with explicit treatment of submodules, symlinks, executable modes, LFS pointers, generated/untracked files, case collisions, and path encoding.
- Keep the trusted manifest and checkout bytes inaccessible to worker mutation; verifier identity must be separate from worker and reviewer write permissions.
- Record authenticated provenance and manifest digest in the trusted registry, not only in a caller-provided report field.

### EP-03 — Manifest completeness and path-to-object semantics need an explicit contract (P1)
The verifier checks each submitted evidence path against a path-to-hash manifest and checks the corresponding supplied bytes. It does not establish that the caller's manifest is a complete inventory of the intended commit, that every manifest entry was independently read, or that the evidence path refers to an immutable stored object rather than a later mutable path. It also accepts additional entries in the caller-supplied file map that are not part of the evidence list.

Required:
- Define whether the manifest is a complete commit inventory or an explicitly scoped evidence allowlist; name and hash the manifest type/version.
- Validate exact manifest construction and completeness at the trusted checkout boundary; reject duplicate/case-fold-colliding or noncanonical paths.
- Bind each evidence item to immutable object ID, byte length, media/type classification, commit/tree identity, and receiver-computed digest.
- Reject unreferenced or unexpected file-map entries where the API contract intends an exact evidence set, or explicitly label them as ignored and never include them as verified evidence.
- Preserve symlink and Git tree semantics rather than treating every path as an ordinary regular file.

### EP-04 — Worker source references and narrative claims are not independently corroborated (P1)
Worker source_ref, description, summary, findings, and action declarations are worker-authored claims. A byte hash proves equality to the supplied manifest, not that a cited passage supports a finding, that the source is authoritative, or that a claimed action occurred.

Required:
- Store worker declarations separately from reviewer observations and independently verified facts.
- Resolve each source reference to a stable immutable source identity (commit/path/line range or external source ID/version) and record exact retrieved bytes or a durable source snapshot where permitted.
- Require reviewer annotations to distinguish direct evidence, inference, unsupported assertion, contradiction, and unresolved question.
- Do not infer execution history from actions_performed; use trusted runtime telemetry and platform audit events.
- A valid digest must never be described as research correctness, source truth, completeness, or task completion.

### EP-05 — Evidence integrity result can be mistaken for broader approval (P1)
The integrated pipeline correctly sets completion and gate approval false and requires human review. However, verified only means byte equality relative to supplied manifest/bytes. A structurally valid completed worker submission can be ready_for_human_review; this is a review queue disposition, not acceptance. Partial/blocked submissions and empty evidence sets need equally explicit status treatment.

Required:
- Keep independent statuses for raw-return authentication, assignment binding, delivery binding, evidence-byte integrity, source authenticity, research assessment, supervisor review, human task disposition, and phase-gate disposition.
- No single verified, ready, accepted, or completed field may collapse these dimensions.
- Empty evidence is not an integrity pass. Missing required evidence, incomplete manifest, unavailable source, or verifier exception remains unresolved/blocked.
- Human reviewer must see worker-declared status separately from verifier/reviewer status and must not inherit worker's completed label as authoritative.

### EP-06 — Report/artifact construction does not itself provide durable custody or uploader authentication (P0)
The review-artifact builder creates a three-file bundle in memory and correctly labels worker claims, report status not_run, and human review requirements. It does not write or upload artifacts. Its workflow metadata, commit manifest, file bytes, checkout-clean assertion, and run identifiers are caller inputs. Artifact-file verification can verify expected names/content hashes against trusted expected context, but artifact existence/name/content alone does not authenticate uploader or platform run.

Required:
- Future workflow must derive run, actor, workflow revision, repository/ref/commit, permissions, and checkout status from authenticated platform context.
- Bind uploaded artifact to a specific authenticated run ID/attempt, immutable artifact identity, uploader principal, workflow revision, task/assignment/review IDs, and exact report/evidence digests.
- Verify downloaded bytes and artifact metadata independently; reject artifacts from a different run, attempt, workflow, repository, branch, or assignment revision.
- Store raw evidence and derived reports separately with immutable retention and access audit; a report is a view, not the only evidence copy.
- Treat upload success as storage acknowledgment only, not review or acceptance.

### EP-07 — Reviewer identity, evidence immutability, and separation of duties are not operational (P0)
The design specifies an independent reviewer and human-only disposition, but no authenticated reviewer identity, immutable review store, or actual permission separation is deployed. If a reviewer can alter source evidence or rewrite the record they review, the review trail is not independent.

Required:
- Give reviewers read-only access to raw return bytes, immutable evidence objects, trusted provenance, and prior lifecycle events.
- Store reviewer annotations and disposition as separate append-only records with authenticated subject, timestamp, policy version, assignment revision, review digest, evidence-set digest, and decision rationale.
- Separate evidence writer/receiver, reviewer, task-acceptance authority, phase-gate authority, registry administrator, and witness administration.
- Prevent reviewers from modifying the evidence object or rewriting prior review/disposition records.
- Preserve dissent, superseding review, and correction as new linked records; never overwrite the original review.

### EP-08 — Human task acceptance must bind to exact reviewed bytes and state (P0)
The design separates task disposition from phase-gate closure, but the trusted transaction must enforce that the human is accepting the exact immutable return and review they inspected. A stale review, changed evidence set, changed assignment revision, or changed handoff must invalidate the acceptance request.

Required:
- Bind human task disposition to task digest, assignment revision/package digest, receiver return ID/raw digest, evidence-set digest, review record ID/review digest, reviewer identity, policy/handoff revision, and current registry sequence.
- Revalidate current handoff and policy at disposition commit; ensure no unresolved evidence, late/revoked return, or superseding review invalidates eligibility.
- Use authenticated human identity, explicit decision enum, trusted transaction time, idempotency identity, and atomic append-only event/checkpoint update.
- Acceptance means only task acceptance. Phase-gate closure remains a separate authenticated decision with its own evidence, authority, and current-handoff check.

### EP-09 — Retention, access, privacy, and deletion policy is not selected (P1)
The design discusses immutable raw returns, backups, artifacts, and recovery, but the project has not selected retention periods, data classification, storage region, encryption/key custody, access logging, legal deletion handling, or backup retention. Immutability must not be confused with unlimited retention or ungoverned exposure.

Required:
- Owner-approved classification and retention schedule for raw returns, evidence, derived reports, reviewer notes, audit events, and backups.
- Encryption in transit and at rest with independent key administration and rotation/revocation procedures.
- Least-privilege access, authenticated downloads, access logs, export controls, and incident response for evidence exposure.
- Define lawful deletion/retention exceptions without silently rewriting the audit chain; use tombstone/redaction metadata and key destruction only under an approved policy that preserves required integrity evidence.
- Document data residency, worker/provider processing, sensitive-data exclusion, and cost/retention ceilings before provider selection.

## Required end-to-end evidence lifecycle
1. Receive: authenticate provider transport and assignment/attempt binding; enforce raw size limit.
2. Preserve: persist raw bytes and receiver digest immutably; commit receipt/idempotency/event/checkpoint before acknowledging.
3. Parse: strict decoding/schema; retain malformed arrivals and classify them without losing raw bytes.
4. Bind: load trusted assignment/package digest and delivery record from registry; compare all identities and exact package revision.
5. Derive provenance: authenticate workflow/checkout context; verify exact commit and clean state; derive complete, versioned manifest.
6. Verify bytes: compare receiver-held evidence bytes against independently derived manifest and object digests; record exact verifier version and result.
7. Review claims: keep worker assertions separate; reviewer checks source authority, relevance, support, contradiction, completeness, and research interpretation.
8. Publish report: create immutable report bound to raw return, assignment, evidence set, workflow run, verifier version, and review record; upload/store with authenticated run provenance.
9. Human disposition: authenticated human decision bound to exact review/evidence digests and current handoff; append-only and idempotent.
10. Gate decision: separate human authority and separate event; never infer from task acceptance.
11. Recover: reconcile receipts, object hashes, event chain, registry checkpoint, witness, retention state, and all pending writes before resuming.

## Mandatory future validation cases
Use synthetic fixtures and disposable infrastructure only, after explicit authorization and when the controlling handoff permits the exact validation:
- Forged worker commit/hash/source reference; caller-selected manifest; dirty checkout; HEAD mismatch; untracked/generated file; submodule/LFS/symlink/mode mismatch.
- Raw return altered after receipt; duplicate delivery; same ID with changed bytes; malformed UTF-8/JSON; oversized payload; truncated upload; parser crash.
- Evidence path traversal, case collision, duplicate path, missing file, extra file-map entry, symlink escape, archive bomb, active content, polyglot and MIME mismatch.
- Evidence object replacement after review; report/artifact swapped across run/attempt/repository/branch/assignment; artifact uploader mismatch; stale artifact replay.
- Reviewer/receiver/admin permission overlap; reviewer evidence mutation; review digest changed before acceptance; handoff/task/assignment revision changes before disposition.
- Duplicate human disposition; changed facts under same idempotency key; acceptance racing with cancellation/revocation/late return/new review; witness outage and restore rollback.
- Retention expiry, legal hold, deletion/tombstone, key revocation, unauthorized download, backup restore, and audit access.

Pass criteria: no untrusted caller can forge provenance or replace raw evidence; every state transition is immutable, authenticated, idempotent, and checkpointed; reviewers can inspect exact evidence without modifying it; task acceptance binds to the exact reviewed digest; gate closure remains separate; uncertainty fails closed.

## Current status and blockers
- Pure source-level validation exists, but trusted transport, raw-byte receiver, immutable evidence store, authenticated workflow context, trusted manifest derivation, artifact uploader binding, reviewer identity, and human disposition service are not implemented.
- The evidence verifier and review pipeline cannot authenticate caller-supplied manifests, bytes, or workflow context.
- The report bundle is built in memory; no artifact upload or durable evidence storage is active.
- No retention, data residency, encryption/key custody, or evidence access policy has been selected.
- No tests, scripts, workflows, provider calls, artifact uploads, reviewer actions, or research operations were run.
- The agent remains non-operational. Phase 3 G0-05 remains controlling; this audit grants no dispatch, execution, task acceptance, gate closure, or phase advancement authority.


## Follow-up — evidence-object retention and deletion consistency

Cross-checking the evidence pipeline against the trusted store adapter, unified lifecycle transaction specification, backup/restore protocol, and research-data access audit confirms that the design separates three concerns which must remain separate in implementation:

1. **Integrity custody:** raw return bytes and original evidence are retained as immutable, digest-addressed objects; a receipt is not valid if its referenced bytes cannot be retrieved and re-hashed.
2. **Lifecycle/audit history:** object receipt, digest, lineage, review and disposition references remain append-only. Retention expiry or an approved deletion must not silently rewrite or remove the historical event chain.
3. **Retention/privacy disposition:** immutability is not unlimited retention. Owner/legal-approved schedules must separately define retention, legal holds, backup expiry, access, deletion exceptions, tombstone/redaction metadata, and any key-destruction process. Deleting a primary object while recoverable replicas/backups remain is not complete deletion.

No direct contradiction was found: the current documents consistently leave retention periods, region, encryption/key custody, and deletion authority unselected pending owner/legal review. The operationally important unresolved design detail is how an approved deletion or key-destruction event affects later evidence-verification status and restore eligibility. A future policy must specify that outcome explicitly (for example, retained digest/receipt with object state marked lawfully unavailable, rather than reporting the bytes as still verifiable). Legal hold and unresolved incident evidence must block deletion; restore must not resurrect expired/deleted objects as silently accessible copies.

This is a specification gap, not a current data-loss or privacy incident. No objects, backups, logs, or live datasets were accessed or changed. No code or tests were changed or executed; the G0-05 handoff remains controlling.
