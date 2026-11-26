# Agent Validation and Activation Checklist

## Current decision

**Status: hardened scaffold; runtime activation blocked.**

The repository contains the configuration, ordered task queue, hash-bound safety controller, read-only preflight dispatcher, and deterministic report formatter. No agent-specific workflow has been added or enabled. No agent task, script, test, or workflow has been executed.

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
- [x] Safety controller rejects duplicate/empty phase-order entries, duplicate JSON object keys, malformed queue entries, duplicate queue IDs, malformed allowlist hashes, duplicate allowlist IDs, phase-priority mismatches, and missing human-gate advancement rules; malformed inputs fail closed.
- [x] Safety controller validates the complete contract of every queue entry, including blocked future-phase tasks, rather than validating only the selected task; duplicate scope/prohibition entries are rejected.
- [x] Safety controller enforces a strict task contract: required fields, non-empty scope, mandatory prohibited-action list, human-only completion authority, and no unsupported task fields, even when a changed task is re-hashed.
- [x] Public runtime authorization accepts only the task payload and loads policy from fixed repository paths; policy injection is confined to a private test seam.
- [x] Task preflight uses the trusted repository policy rather than passing a caller-supplied queue into the authorization boundary.
- [x] Added 19 focused safety-controller denial/allowance tests, including task-contract omissions, unsupported fields, non-human completion authority, relabelled Phase 3 tasks, malformed inputs, public policy-injection rejection, malformed unrelated queue contracts, and duplicate prohibition entries; authored but not executed.
- [x] Read-only preflight dispatcher has no executor, subprocess, or write capability.
- [x] Preflight dispatcher returns a stable result envelope for every path, rejects malformed queue objects and rows, and fails closed on malformed or internally inconsistent authorization results.
- [x] Report formatter validates repository-contained inputs, rejection of symlinked path components, normalized unique manifest paths, SHA-256 values, commit SHA format, and canonical UTC timestamps ending in Z.
- [x] Report schema rejects unsupported top-level fields, non-string finding entries, Boolean schema versions, Windows-style manifest paths, non-finite JSON values, and unsupported/completion-claim statuses; only preflight_only, blocked, skipped, and not_run are accepted.
- [x] Added a checkout-manifest verifier that detects missing files and byte/hash mismatches. Its scope is explicitly limited to current checkout bytes; it does not assert that those bytes belong to the reported Git commit or that the checkout is clean.
- [x] Markdown reports explicitly disclose that caller-supplied repository/branch/commit/run metadata is not authenticated by schema validation, manifest hashes are declarations until independently checked, and reports are not task-completion evidence or gate approval.
- [x] Added 19 report-builder regression tests covering deterministic rendering, malformed provenance, duplicate and unsafe paths, strict schema/timestamp validation, external paths, symlinks, Markdown injection, completion-claim status rejection, and explicit provenance/metadata limitation disclosures; authored but not executed.
- [x] Markdown report rendering flattens untrusted line breaks and escapes Markdown control characters in findings and metadata.
- [x] Added 10 preflight tests for malformed queues and rows, duplicate task IDs, trusted-queue boundary, stable denial envelopes, inconsistent/malformed authorization results, and preflight-only behavior; authored but not executed.
- [x] Total regression tests authored: 48 (19 safety-controller, 19 report-builder, 10 task-runner); none executed.
- [x] Static configuration/source consistency review completed against the branch files.

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
2. A human reviewer must inspect the exact task definition and approve its SHA-256 hash in the trusted allowlist.
3. The agent execution and queue execution switches must remain disabled until the validation checks above pass.
4. The safety controller must be tested against both allowed and denied cases, including phase override denial, missing prior-gate closure, the active G0-05 lock, tampered task payloads, and missing/malformed policy files.
5. A future workflow must use least-privilege GitHub permissions, explicit branch filters, concurrency protection, bounded artifact retention, and no secrets unless separately justified.
6. Initial automation must be manual-dispatch only and preflight/report-only. Event-driven and scheduled triggers remain disabled until manual operation is independently validated.
7. No automatic commits, merges, canonical research-data changes, VPS deployment, or secret/permission changes.
8. Human authority remains required for gate closure and phase advancement.

## Completion definition

The agent is considered operational only after the permitted runtime checks pass, a manually triggered preflight produces a correct artifact, safety-denial cases are demonstrated, and the human reviewer approves activation. Merely creating these files does not count as success.
