# Agent Validation and Activation Checklist

## Current decision

**Status: scaffold complete; runtime activation blocked.**

The repository contains the configuration, ordered task queue, hash-bound safety controller, read-only preflight dispatcher, and deterministic report formatter. No workflow has been added or enabled. No agent task, script, test, or workflow has been executed.

The current Phase 3 G0-05 handoff remains authoritative. It prohibits the relevant script/test/workflow execution and research code/data changes. The agent must not be used to bypass that restriction.

## Completed implementation

- [x] Isolated agent branch created from the approved research-branch baseline.
- [x] Free-only deterministic operating mode documented.
- [x] Phase order fixed: Phase 3, Phase 1, Phase 2, Phase 4, Phase 5.
- [x] Phase permissions and global prohibitions defined.
- [x] Initial six-task queue created; later phases remain blocked.
- [x] Trusted task allowlist created and intentionally left empty.
- [x] Safety controller requires exact queue-task equality and a trusted SHA-256 approval for that exact task definition.
- [x] Safety controller checks the active phase, queue execution switch, agent execution switch, and G0-05 restrictions.
- [x] Read-only preflight dispatcher created; it has no executor, subprocess, or write capability.
- [x] Report formatter created with required provenance fields, repository-contained input hashing, validation, and report digest.
- [x] Static configuration/source consistency review completed against the branch files.

## Deferred validation

These checks must not be run while the current G0-05 handoff prohibits them:

- [ ] Python syntax/import validation.
- [ ] Unit tests for allowlist mismatch, task mutation, phase mismatch, unknown operation, disabled switches, and G0-05 hard lock.
- [ ] Report-builder tests for valid reports, malformed manifests, path traversal, and deterministic digests.
- [ ] End-to-end dry-run of the preflight dispatcher.
- [ ] GitHub Actions workflow validation and a manual workflow run.

A static source review is not a substitute for these runtime checks.

## Conditions before any activation

1. The applicable research handoff must explicitly permit the proposed validation and execution scope. Do not infer permission from this checklist.
2. A human reviewer must inspect the exact task definition and approve its SHA-256 hash in the trusted allowlist.
3. The agent execution and queue execution switches must remain disabled until the validation checks above pass.
4. The safety controller must be tested against both allowed and denied cases, including tampered task payloads and missing/malformed policy files.
5. A future workflow must use least-privilege GitHub permissions, explicit branch filters, concurrency protection, bounded artifact retention, and no secrets unless separately justified.
6. Initial automation must be manual-dispatch only and preflight/report-only. Event-driven and scheduled triggers remain disabled until manual operation is independently validated.
7. No automatic commits, merges, canonical research-data changes, VPS deployment, or secret/permission changes.
8. Human authority remains required for gate closure and phase advancement.

## Completion definition

The agent is considered operational only after the permitted runtime checks pass, a manually triggered preflight produces a correct artifact, safety-denial cases are demonstrated, and the human reviewer approves activation. Merely creating these files does not count as success.
