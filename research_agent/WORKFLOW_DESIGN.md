# GitHub Actions Workflow Boundary — OKX Research Agent

## Status

**Design only. No agent workflow is installed, enabled, or authorized to run.**

This document defines the proposed boundary for the first agent workflow. It does not grant permission to execute research scripts, tests, or workflows. The active Phase 3 G0-05 handoff remains controlling.

## Current static findings

The inherited workflow inventory on this branch contains 39 workflow files. Two G0-05 workflows were inspected directly:

- `.github/workflows/phase3-g0-05-candidate-contract-tests.yml`
- `.github/workflows/phase3-g0-05-independent-minute-verification.yml`

Both include `workflow_dispatch` and push triggers restricted to `price-action-v1`. Both explicitly check out `price-action-v1`, rather than the agent branch. The first compiles and runs the G0-05 candidate-contract test; the second downloads a source-audit artifact, runs the independent minute verifier, and uploads verification output.

These workflows are not agent workflows. They must not be dispatched or otherwise used to bypass the current G0-05 handoff. The two-file review is not a complete audit of all 39 inherited workflow trigger definitions.

## Inherited workflow inventory — complete filename census

A read-only inventory of all 39 YAML workflow files in `.github/workflows/` on the agent branch was completed. This was a static text inspection only; no workflow was dispatched.

- 39 workflows total.
- 38 declare `workflow_dispatch`.
- 35 declare `push`.
- 4 are manual-dispatch-only in the inspected trigger declarations.
- 1 is push-only in the inspected trigger declarations.
- 26 contain at least one explicit write permission among repository contents, Actions, pull requests, or issues.
- 13 do not contain those explicit write permissions.
- All 39 contain workflow YAML files inherited from the research branch; none is an agent-specific workflow.

The four dispatch-only workflows are:
- `sideways-boundary-interaction-taxonomy-v1.yml`
- `sideways-rejection-v1-full-study.yml`
- `sideways-rejection-v1-tests.yml`
- `vps-health-monitor.yml`

The push-only workflow is `funding-engine-contract-tests.yml`.

**Important interpretation:** a workflow being present on the agent branch does not mean it is safe to dispatch. Many workflows explicitly check out `price-action-v1`; some have write permissions and run research scripts or tests. Manual dispatch can therefore still reach protected research code. The current G0-05 handoff prohibits using these workflows for G0-05 work, and the agent must not dispatch any inherited workflow as a workaround.

The 26 write-permission findings are a static regex census of explicit permission declarations, not a proof of the effective token permission after repository/org policy. The complete workflow YAML files were not all reviewed line-by-line for every command, action pin, artifact path, or checkout behavior. The inventory is sufficient to establish a broad isolation risk, not to certify individual workflows.

## First-workflow design (future, subject to authorization)

### Trigger and scope

- Use `workflow_dispatch` only.
- Do not add `push`, `pull_request`, `pull_request_target`, `workflow_run`, `schedule`, or `workflow_call` triggers.
- Require an explicit input selecting one fixed, pre-reviewed operation; reject unknown values.
- Pin the workflow to the agent branch and explicitly check out `agent/okx-research-agent-v1`.
- Do not check out or execute code from `price-action-v1` while the G0-05 handoff prohibits execution.
- Do not let task-queue fields become shell commands, paths outside the repository, action references, or workflow inputs.

### Permissions and credentials

- Set workflow-level `permissions: contents: read`; set job-level permissions explicitly and no broader than required.
- Do not grant `contents: write`, `actions: write`, `pull-requests: write`, `issues: write`, or deployment permissions.
- Do not create, expose, or pass repository secrets to the job.
- Disable persisted checkout credentials (`persist-credentials: false`).
- Avoid third-party actions. When an action is essential, pin it to a reviewed full commit SHA, not a mutable tag.

### Execution containment

- The initial authorized job must be preflight/report-only.
- No shell command may be constructed from queue or artifact content.
- Use a fixed working directory and validate all input paths against a repository-contained allowlist.
- Reject symlinks, path traversal, duplicate manifest paths, malformed hashes, and unexpected files.
- Use a bounded job timeout and a single concurrency group with `cancel-in-progress: false`.
- Do not use self-hosted runners, persistent caches, VPS access, or external services.
- No research scripts, tests, backtests, data downloads, candidate generation, or research-data writes until the applicable handoff explicitly permits each activity.

### Artifact handling

- Upload only the deterministic report output and its provenance manifest.
- Use a unique artifact name containing the workflow run ID.
- Set a short, explicit retention period (initial proposal: 7 days).
- Fail if the expected report is missing; do not silently upload an empty or partial directory.
- Never execute, source, or trust files recovered from an artifact.
- Record repository, branch, commit SHA, task ID, exact task-definition hash, UTC generation time, and input-manifest hashes in the report.
- Artifact output is evidence for review, not authorization to advance a gate.

## Pre-installation review checklist

- [ ] Current handoff explicitly permits the exact proposed validation and execution scope.
- [ ] Complete static audit of inherited workflow triggers and checkout refs is finished.
- [ ] Workflow YAML is reviewed independently before installation.
- [ ] Workflow has only manual dispatch and fixed allowlisted inputs.
- [ ] Branch and checkout refs are explicit and agent-only.
- [ ] Permissions are least-privilege and no secrets are available.
- [ ] Actions are pinned to full commit SHAs or avoided.
- [ ] Timeout, concurrency, path validation, and artifact retention are bounded.
- [ ] Artifact content is deterministic and provenance-complete.
- [ ] Runtime safety tests are permitted and pass.
- [ ] A human reviewer authorizes the exact workflow and task scope.

## Explicit non-goals

This workflow must not merge branches, commit to the research branch, alter canonical definitions or data, close gates, advance phases, select strategies, make PnL claims, deploy to a VPS, or change secrets or repository permissions.

**Activation rule:** until every applicable checklist item is satisfied and the required human authorization is recorded, no agent workflow is to be created or run.
