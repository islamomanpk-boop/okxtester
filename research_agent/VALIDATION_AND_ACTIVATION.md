# Agent Validation and Activation Checklist

## Current decision

**Status: hardened scaffold; runtime activation blocked.**

The repository contains the configuration, ordered task queue, hash-bound safety controller, read-only preflight dispatcher, deterministic report formatter, preflight-to-artifact orchestration, bounded batch planner, supervisor review gate, pure evidence-integrity verifier, and integrated structural/evidence review pipeline. No agent-specific workflow has been added or enabled. No agent task, script, test, or workflow has been executed.

The current Phase 3 G0-05 handoff remains authoritative. It prohibits the relevant script/test/workflow execution and research code/data changes. The agent must not be used to bypass that restriction.

## Completed implementation

- [x] Isolated agent branch created from the approved research-branch baseline.
- [x] Free-only deterministic operating mode documented.
- [x] Phase order fixed: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5.
- [x] Phase permissions and global prohibitions defined.
- [x] Initial six-task queue created; later phases remain blocked.
- [x] Trusted task allowlist created and intentionally left empty.
- [x] Safety controller requires exact queue-task equality and a trusted SHA-256 approval for that exact task definition.
- [x] Safety controller requires an explicit phase-level read-only opt-in; missing, denied, or unknown overrides fail closed.
- [x] Safety controller requires explicit human-authorized closure of every prior phase gate before a later phase can be authorized.
- [x] Safety controller enforces the active global G0-05 lock against every Phase 3 task, regardless of task labels, preventing relabelling bypasses.
- [x] Safety controller rejects duplicate/empty phase-order entries, duplicate JSON object keys, malformed queue entries, duplicate queue IDs, malformed allowlist hashes, duplicate allowlist IDs, phase-priority mismatches (strict integer typing), branch-policy boolean type confusion, unsupported/missing policy keys, schema-version drift, weakened global operation defaults, and missing human-gate advancement rules; malformed inputs fail closed.
- [x] Safety controller validates the complete contract of every queue entry, including blocked future-phase tasks, rather than validating only the selected task; duplicate scope/prohibition entries are rejected.
- [x] Safety controller requires read-only repository access, the exact isolated agent/research branch policy, disabled automatic merge/research-branch commits, and explicitly disabled scheduling.
- [x] Safety controller enforces a strict task contract: required fields, non-empty scope, mandatory prohibited-action list, human-only completion authority, and no unsupported task fields, even when a changed task is re-hashed.
- [x] Public runtime authorization accepts only the task payload and loads policy from fixed repository paths; policy injection is confined to a private test seam.
- [x] Task preflight uses the trusted repository policy rather than passing a caller-supplied queue into the authorization boundary.
- [x] Added 32 focused safety-controller denial/allowance tests, including task-contract omissions, unsupported fields, non-human completion authority, relabelled Phase 3 tasks, malformed inputs, public policy-injection rejection, malformed unrelated queue contracts, duplicate prohibition entries, enabled scheduling, and branch-policy drift; authored but not executed.
- [x] Read-only preflight dispatcher has no executor, subprocess, or write capability.
- [x] Preflight dispatcher returns a stable result envelope for every path, including queue-load and unexpected authorization failures; it rejects malformed queue objects and rows and fails closed on malformed or internally inconsistent authorization results.
- [x] Report formatter validates repository-contained inputs, rejection of symlinked path components, normalized unique manifest paths, SHA-256 values, commit SHA format, and canonical UTC timestamps ending in Z.
- [x] Report schema rejects unsupported top-level fields, non-string finding entries, Boolean schema versions, Windows-style manifest paths, non-finite JSON values, and unsupported/completion-claim statuses; only preflight_only, blocked, skipped, and not_run are accepted.
- [x] Added a checkout-manifest verifier that detects missing files and byte/hash mismatches.
- [x] Added a report provenance verifier that binds task identity to the exact trusted task, compares repository/branch/commit claims against caller-supplied trusted workflow context, requires actual HEAD to equal the expected commit, requires an explicit clean-checkout assertion, and rechecks manifest bytes. It does not query Git or authenticate the caller; the future workflow must obtain these runtime facts from trusted event context and independently verify checkout cleanliness.
- [x] Added an preflight-only report factory that rejects queue summaries, inconsistent decisions, and any execution claim; in-memory artifact bundle builder that validates trusted run ID/attempt format and report run binding, then produces exactly `report.json`, `report.md`, and `artifact_manifest.json` with deterministic names and SHA-256 hashes for both report files. It performs no filesystem writes or upload; `verify_artifact_files()` checks the actual downloaded artifact name and run ID/attempt against trusted workflow context, exact file completeness, embedded-manifest consistency, strict JSON without duplicate keys or NaN/Infinity, both report-file hashes, canonical JSON/Markdown consistency, and report/manifest identity. The future workflow must upload the complete bundle atomically and run this verifier against downloaded artifact contents.
- [x] Markdown reports explicitly disclose that caller-supplied repository/branch/commit/task-hash/run metadata is not authenticated by schema validation, manifest hashes are declarations until independently checked, and reports are not task-completion evidence or gate approval.
- [x] Report schema requires a task-definition SHA-256 and provides canonical JSON hashing shared with the safety controller, plus a verifier that binds report task ID, phase, and digest to the exact trusted queue task; digest inputs are restricted to strict JSON values (string object keys, finite numbers, arrays, objects, and JSON scalars), rejecting Python-only values and ambiguous key coercion. The workflow must compute it from the exact trusted queue object.
- [x] Added 50 report-builder regression tests covering deterministic rendering, malformed provenance, duplicate and unsafe paths, strict schema/timestamp validation, fixed agent identity, external paths, symlinks, Markdown injection, completion-claim status rejection, and explicit provenance/metadata limitation disclosures; authored but not executed.
- [x] Markdown report rendering flattens untrusted line breaks and escapes Markdown control characters in findings and metadata; untrusted values are kept outside Markdown code spans to prevent delimiter breakout.
- [x] Added 27 preflight tests for malformed queues and rows, duplicate task IDs and JSON keys, non-standard JSON constants, trusted-queue boundary, stable denial envelopes, inconsistent/malformed authorization results, and preflight-only behavior; authored but not executed.
- [x] Added `artifact_preparation.py` to connect trusted queue lookup, single-task preflight, preflight-only report generation, and in-memory artifact bundling. It is restricted to the repository and isolated agent branch; denied preflight becomes a `blocked` report. It performs no task work, queue mutation, filesystem writes, upload, or scheduling. Workflow metadata remains caller-supplied until independently obtained and verified by a future workflow; authored but not runtime-tested.
- [x] Added 7 artifact-preparation regression tests for blocked-artifact creation, branch/repository restrictions, dirty checkout, HEAD mismatch, and task identity; authored but not executed.
- [x] Added `batch_planner.py` to prepare a bounded batch only from exact per-task preflight approvals. It enforces the fixed five-phase sequence, stops at the earliest queued phase if nothing there passes preflight, caps batch size, and never authorizes the queue, executes tasks, or changes state.
- [x] Batch planner assignments now carry the trusted task's handoff ID, full scope, prohibited-action list, and canonical task-definition digest so a future worker receives the complete boundary rather than a title-only prompt.
- [x] Added `supervisor_review.py` to validate untrusted worker submissions against the exact trusted task digest, required evidence-reference structure, declared actions, and gate-authority boundary. Valid submissions are only ready for human review; evidence bytes and research correctness are explicitly unverified. No completion or gate is approved.
- [x] Added 17 supervisor-review regression tests covering valid-but-human-review-only submissions, prohibited and unknown action labels, gate-closure claims, missing evidence, task digest/identity mismatch, unsafe traversal, Windows-drive and control-character paths, malformed hashes, blockers, unknown fields, malformed status types, and inconsistent completion claims; authored but not executed.
- [x] Added `evidence_verifier.py` to compare worker evidence declarations and checkout bytes against a path/hash manifest tied to an expected commit SHA. It rejects unsafe/duplicate paths, missing files, manifest/commit mismatch, malformed hashes, and byte mismatches. The caller must authenticate the checkout and derive the manifest; the module itself has no GitHub, filesystem, or network access. Passing checks never approves completion or gate closure; see `EVIDENCE_VERIFICATION.md`.
- [x] Added 10 evidence-verifier regression tests for matching bytes, worker-hash mismatch, checkout-byte mismatch, missing files, absent manifest paths, commit mismatch, unsafe/duplicate/single-backslash paths, malformed manifest hashes, and empty evidence; authored but not executed.
- [x] Added `review_pipeline.py` to connect structural worker-submission review to evidence-byte verification. Structural/safety failures stop before evidence verification; any evidence integrity failure downgrades the submission to `return_for_revision`. The pipeline never approves task completion or gate closure and relies on caller-supplied checkout context; see `REVIEW_PIPELINE.md`.
- [x] Added 6 integrated-review regression tests for valid-but-human-review-only results, worker hash mismatch, checkout byte mismatch, commit mismatch, structural safety rejection, and empty evidence; authored but not executed.
- [x] Added `assignment_package.py` to bind one exact trusted task, preflight result, and planner assignment into a non-dispatchable worker handoff package. It carries the task digest, handoff ID, scope, prohibitions, and submission schema; it cannot dispatch or authorize execution.
- [x] Added 9 assignment-package regression tests for allowed/denied preflight handling, task/plan mismatches, human-only authority, and non-dispatch boundaries; authored but not executed.
- [x] Added `assignment_return.py` to bind a returned submission to the exact prepared package before supervisor/evidence review. It rejects blocked/tampered packages and does not claim dispatch or delivery.
- [x] Added 5 assignment-return regression tests for valid human-only review, blocked packages, tampered scope/digest, and dispatch claims; authored but not executed.
- [x] Added `review_artifact.py` to connect assignment-bound review results to the existing strict report and in-memory artifact builder. Worker claims remain explicitly unverified declarations, report status stays `not_run`, and human completion/gate authority is preserved; see `docs/REVIEW_ARTIFACT.md`.
- [x] Added 6 review-artifact regression tests for completion-claim containment, evidence-integrity blockers, tampered assignment rejection, repository/branch/commit boundaries, and no dispatch/upload claims; authored but not executed.
- [x] Total regression tests authored: 178 (32 safety-controller, 50 report-builder, 27 task-runner, 7 artifact-preparation, 9 batch-planner, 17 supervisor-review, 10 evidence-verifier, 6 integrated-review, 9 assignment-package, 5 assignment-return, 6 review-artifact); none executed. Safety policy and CLI task JSON reject duplicate object keys and non-standard NaN/Infinity constants.
- [x] Static configuration/source consistency review completed against the branch files.
- [x] Added `PHASE_SUPPORT_MATRIX.md` documenting reusable support and queue coverage across all five phases in the agreed order; later phases remain gated by predecessor closure and their own handoffs.
- [x] Added a safety-controller regression test that checks the checked-in phase configuration, queue ordering, per-phase task presence, later-phase blocked statuses, and human-authorized gate dependency; authored but not executed.
- [x] Documented the future event-driven operating model and all-phase research capability categories; logical event names are not yet wired to GitHub triggers, and event/scheduled automation remains disabled.
- [x] Verified repository default branch is `main`; GitHub requires a `workflow_dispatch` workflow file to exist on the default branch. The current agent-branch-only/manual-dispatch design is blocked unless the user authorizes a minimal main-branch dispatcher or chooses a separate agent repository. No such change is authorized or made.

## Deferred validation

These checks must not be run while the current G0-05 handoff prohibits them:

- [ ] Python syntax/import validation.
- [ ] Execute safety-controller tests, including phase override denial, missing prior-gate closure, active global Phase 3 lock with relabelled tasks, duplicate phase order, malformed input denial, policy-injection rejection at the public runtime API, allowlist mismatch, task mutation, unknown operation, and disabled switches.
- [ ] Execute report-builder tests for valid reports, malformed manifests, path traversal, UTC timestamps, commit SHA format, deterministic digests, and hostile Markdown/newline inputs.
- [ ] Execute preflight tests for malformed queues, duplicate task IDs, and no-execution behavior.
- [ ] End-to-end dry-run of the preflight dispatcher.
- [ ] GitHub Actions workflow validation and a manual workflow run.

A static source review is not a substitute for these runtime checks.

## Conditions before any activation

1. The applicable research handoff must explicitly permit the proposed validation and execution scope. Do not infer permission from this checklist.
2. Resolve the default-branch activation constraint: either explicitly authorize a minimal reviewed dispatcher on `main`, or approve a separate agent repository; do not alter `main` or create another repository implicitly.
3. A human reviewer must inspect the exact task definition and approve its SHA-256 hash in the trusted allowlist.
4. The agent execution and queue execution switches must remain disabled until the validation checks above pass.
5. The safety controller must be tested against both allowed and denied cases, including phase override denial, missing prior-gate closure, the active G0-05 lock, tampered task payloads, and missing/malformed policy files.
6. A future workflow must use least-privilege GitHub permissions, explicit branch filters, concurrency protection, bounded artifact retention, and no secrets unless separately justified.
7. Initial automation must be manual-dispatch only and preflight/report-only. Event-driven and scheduled triggers remain disabled until manual operation is independently validated.
8. No automatic commits, merges, canonical research-data changes, VPS deployment, or secret/permission changes.
9. Human authority remains required for gate closure and phase advancement.

## Completion definition

The agent is considered operational only after the permitted runtime checks pass, a manually triggered preflight produces a correct artifact, safety-denial cases are demonstrated, and the human reviewer approves activation. Merely creating these files does not count as success.
