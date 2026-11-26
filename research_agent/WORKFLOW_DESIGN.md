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

- Use the report builder's in-memory artifact bundle, which returns exactly `report.json`, `report.md`, and `artifact_manifest.json` only after task, checkout, commit, and input-manifest provenance checks pass.
- The artifact manifest contains the fixed artifact name (run ID plus run attempt), task/phase/repository/branch/task-definition-hash/commit identifiers, and SHA-256 hashes for the JSON and Markdown report bytes. It deliberately does not self-hash. `verify_artifact_files()` checks the actual downloaded artifact name and manifest run ID/attempt against independently supplied trusted workflow run ID/attempt, requires exactly the three expected filenames, rejects duplicate JSON keys and non-standard NaN/Infinity constants, matches the embedded manifest to the supplied manifest, checks both report-file hashes, requires canonical JSON/Markdown renderings to agree, and checks report task, phase, repository, branch, task-definition hash, run ID, and commit identity against the manifest. The workflow must obtain expected run ID/attempt from trusted GitHub context, not from the artifact.
- Upload the three expected files together as one artifact. Do not upload a partial directory; fail if any file is missing, unexpected files are present, or uploaded bytes do not match the artifact manifest.
- Use the exact artifact name returned by the bundle builder; it includes the trusted workflow run ID and run attempt. Never use task/report-supplied values to construct the artifact name.
- Set a short, explicit retention period (initial proposal: 7 days).
- Fail if the expected report is missing; do not silently upload an empty or partial directory.
- Never execute, source, or trust files recovered from an artifact.
- Record repository, branch, commit SHA, task ID, canonical task-definition SHA-256 (computed from the exact trusted queue object), UTC generation time, and input-manifest hashes in the report. The report schema checks hash format; provenance still requires the workflow to compute it from the trusted queue entry and bind it to the checked-out commit/run.
- The workflow must derive expected repository/ref/commit from trusted GitHub workflow context (never dispatch inputs or report fields), verify actual checked-out `HEAD` equals the expected commit, and independently confirm a clean working tree before calling the report provenance verifier. It must check out the exact event commit SHA, not a moving branch name.
- The provenance verifier checks report repository, branch, and commit against those trusted runtime values; checks `HEAD == expected commit`; requires the caller's clean-checkout assertion to be exactly `True`; binds the report to the exact trusted task; and rechecks every manifest file against current checkout bytes. The function does not itself query Git or authenticate its caller, so the workflow is responsible for obtaining these runtime facts safely.
- The bundle builder only creates in-memory strings; it does not write or upload files. Upload completeness and artifact-service behavior remain the workflow's responsibility.
- Artifact SHA-256 values detect byte changes but do not authenticate the uploader or GitHub artifact service.
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
- [ ] The workflow uploads exactly `report.json`, `report.md`, and `artifact_manifest.json` as one artifact, validates each uploaded file hash, and fails closed on missing or unexpected files.
- [ ] Workflow checks out the exact event commit SHA; derives expected repository/ref/SHA only from trusted workflow context; independently verifies `HEAD` equality and a clean working tree; then invokes `verify_report_provenance()` with those facts.
- [ ] Runtime safety tests are permitted and pass.
- [ ] A human reviewer authorizes the exact workflow and task scope.

## Explicit non-goals

This workflow must not merge branches, commit to the research branch, alter canonical definitions or data, close gates, advance phases, select strategies, make PnL claims, deploy to a VPS, or change secrets or repository permissions.

**Activation rule:** until every applicable checklist item is satisfied and the required human authorization is recorded, no agent workflow is to be created or run.


## Deep static workflow review — actions, writes, checkout, and VPS boundary

A second read-only pass fetched the full text of all 39 workflow files in batches. This pass inspected action references, explicit permission declarations, checkout refs, secret references, and shell-command indicators. No workflow was run.

### Confirmed high-risk inherited patterns

- Action references are tag-based, including `actions/checkout@v4`, `actions/setup-python@v5`, and `actions/upload-artifact@v4`; these are not immutable full-SHA pins. This is an inventory observation, not a claim that these first-party actions are malicious.
- The Phase 1 source-preflight workflow grants `contents: write`, checks out `price-action-v1`, permanently archives outputs into the research tree, commits, and pushes to `price-action-v1`.
- The Phase 3 breakout-lifecycle workflow grants `contents: write`, checks out `price-action-v1`, runs tests and a historical research script, archives reports, and pushes to `price-action-v1`. Its output-contract assertions explicitly include the five outside-retest fields, so it is especially unsuitable as an agent-side shortcut under the current G0-05 handoff.
- The Phase 3 funding mark-price audit grants `contents: write`, creates a candidate-proxy snapshot and manifest, then commits and pushes data to `price-action-v1`. It also embeds a prior VPS reproduction run ID and digest in its workflow environment; this is provenance metadata, not evidence of live SSH access.
- Multiple other inherited Phase 3 and sideways workflows likewise declare `contents: write` and archive outputs into Git. They are not agent-safe merely because they can be manually dispatched.
- The G0-05 source-audit and independent-minute-verification workflows explicitly check out `price-action-v1`, use the GitHub token to retrieve/download the relevant source artifact, and execute G0-05 scripts. They remain prohibited by the controlling handoff.
- The VPS health-monitor workflow is materially different: it uses a `self-hosted, linux, x64` runner, with read-only repository permission and no explicit named secret reference. Its shell commands inspect host/memory/disk/load, the OKX downloader process, a download log, and SQLite filenames under the runner user's home directory, then write the report to the GitHub step summary. This is direct VPS-side execution and can expose operational metadata/log content to the workflow run; it must never be repurposed for the research agent. The agent design therefore explicitly excludes self-hosted runners and all VPS access.

### What the scan did and did not establish

- The scan found no explicit `secrets.NAME` references and no literal SSH/SCP/rsync deployment commands in the 39 workflow files. It did find the self-hosted VPS health workflow described above.
- This does not rule out credentials supplied implicitly by GitHub, runner environment variables, actions, scripts, or repository settings. Static workflow text cannot establish effective token permissions or runner isolation.
- Shell/network indicators were treated as triage signals only; a false result is not a security certification.
- Several workflows do not explicitly declare permissions. Their effective permissions must be evaluated against repository and organization defaults before any future use.
- The inventory is complete at the workflow-file level for this branch snapshot, but it is not a line-by-line audit of every invoked Python script, dependency, action implementation, or runner configuration.

### Agent boundary decision

The agent must run only on a fresh GitHub-hosted runner, with an explicit agent-branch checkout, no inherited workflow invocation, no self-hosted labels, no repository secrets, no write token, and no dynamic action or shell selection. The first future workflow remains manual-dispatch and report-only, and cannot be installed or run until the G0-05 handoff permits the exact validation scope and a human authorizes it.
