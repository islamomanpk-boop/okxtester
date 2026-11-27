# Inherited Phase 3 Workflow Side-Effect and Automation Audit — 2026-11-27

## Scope and method

Read-only static inspection of selected inherited workflow definitions on `agent/okx-research-agent-v1`. The files are inherited from the repository's research branch; none is an `okx-research-agent` workflow. This is a targeted extension to [the earlier G0-05 push-trigger audit](INHERITED_RESEARCH_WORKFLOW_PUSH_TRIGGER_AND_G0_05_HAZARD_AUDIT_2026-11-27.md), not a complete re-audit of every workflow, action, dependency, or repository setting.

No workflow was dispatched, rerun, enabled, cancelled, or edited. No matching push was made. No tests, scripts, package installation, data retrieval, research pipeline, artifact publication, or branch write occurred.

The active G0-05 handoff remains controlling and prohibits execution of scripts, tests, and workflows. These findings are hazards to avoid, not instructions to invoke any workflow.

## High-impact findings

### WF-SIDEWAYS-01 — Matched-cohort V8 workflow can write and push research-branch outputs

File: `.github/workflows/sideways-matched-cohort-audit-v8.yml`

Static facts:
- Triggers on `workflow_dispatch` and pushes to `price-action-v1` matching the workflow, V8 research module, or V8 test file (lines 2–9).
- Declares `contents: write` (line 11); runs on `ubuntu-latest` (lines 15–18).
- Checks out `price-action-v1` (lines 19–24), installs NumPy, pandas, and SciPy (lines 26–27), compiles and runs tests (lines 28–31), verifies frozen archive/data files (lines 32–40), and executes the V8 historical audit (lines 41–49).
- Copies results into the research archive, stages them, commits, and pushes to `price-action-v1` (lines 50–61). It also uploads a secondary artifact with 14-day retention (lines 62–68).

Risk:
- A matching push can launch tests and a historical research computation, then create a commit and push archive outputs to the research branch. This is not a read-only validation workflow.
- Because the workflow file itself is a watched path, changing that workflow on `price-action-v1` is also a trigger.
- Do not edit watched paths or dispatch this workflow while the handoff prohibits workflow execution and research changes.

### WF-FUNDING-01 — Full-window funding/mark-price workflow can publish a candidate-proxy snapshot to the research branch

File: `.github/workflows/phase3-funding-mark-price-full-audit.yml`

Static facts:
- Triggers on matching pushes to `price-action-v1` and `workflow_dispatch` (lines 2–9).
- Declares `contents: write` (line 11), runs on `ubuntu-latest`, and checks out the triggering commit SHA (lines 15–23).
- Compiles/runs helper tests, then executes the full-window public funding and mark-price audit (lines 28–41).
- Verifies a frozen CSV digest, row counts, per-asset counts, and metadata; writes a manifest and README; then stages and pushes a candidate-proxy CSV/manifest/README to `price-action-v1` (lines 42–131).
- Uploads a workflow artifact with 90-day retention (lines 133–139).

The generated manifest explicitly labels the output `CANDIDATE_PROXY_NOT_EXACT_SETTLEMENT_MARK`, sets exact settlement verification and funding policy acceptance to false, and says engine mode was not changed (lines 74–99). This qualification is important: the workflow's own code does not claim the proxy is exact settlement truth.

Risk:
- The workflow is a data-generation and research-branch-write pipeline, not a passive audit. Its existence does not authorize running it under the current handoff.
- Its write permission and embedded git push are independent reasons to keep it out of the agent's permitted execution surface.

### WF-BREAKOUT-01 — Breakout lifecycle workflow executes tests/reconstruction and pushes reports

File: `.github/workflows/phase3-breakout-lifecycle-v1-1.yml`

Static facts:
- Triggers on manual dispatch and matching pushes to `price-action-v1`, including the research module, test file, amendment checkpoint, and workflow itself (lines 5–13).
- Declares `contents: write` (lines 15–16), checks out `price-action-v1` (lines 22–30), installs pinned NumPy/pandas (lines 32–38), runs unit tests and the frozen historical lifecycle script (lines 40–44), and validates fixed output counts/fields (lines 46–73).
- Uploads the report artifact with 90-day retention (lines 75–81), then commits and pushes report outputs to `price-action-v1` (lines 83–93).

The static output assertions include 1,592 primary events, 6,368 horizon rows, and the five unavailable outside-retest lifecycle fields. Those are workflow assertions, not newly verified results in this audit.

Risk:
- This workflow directly intersects the current G0-05 boundary: tests, historical reconstruction, artifact publication, and a research-branch write. It must not be run or used as an alternate validation route.

## Additional sampled workflows

### WF-ARCHIVE-01 — Phase 3 completion archive validation

File: `.github/workflows/phase3-completion-validation.yml`

- Manual and matching push trigger on `price-action-v1`; watched paths include its own YAML and selected Phase 3 archive/decision files (lines 2–10).
- Declares `contents: read`, checks out `price-action-v1`, and uses shell/Python assertions to verify archives, compare V10.10/V10.11 fields, and inspect the closeout record (lines 11–67).
- Although it does not declare repository write permission or a report upload in the inspected file, it is still executable workflow validation and prohibited by the active handoff.

### WF-FUNDING-02 — Funding coverage test workflow

File: `.github/workflows/phase3-funding-coverage-audit.yml`

- Matching push trigger on `price-action-v1` and manual dispatch (lines 2–9).
- Declares `contents: read`, checks out the research branch, compiles the audit/test modules, and runs deterministic tests (lines 10–31).
- No artifact upload or explicit research-branch write appears in the inspected workflow. It remains prohibited because it executes tests.

### WF-SIDEWAYS-02 — Full historical rejection study

File: `.github/workflows/sideways-rejection-v1-full-study.yml`

- Manual-dispatch only in the inspected trigger block; `contents: read`; `ubuntu-latest); checks out `price-action-v1).
- Installs Python dependencies, runs a full historical study, and uploads an artifact with 14-day retention.
- No push trigger or repository write permission was visible in the inspected file. Manual-only does not make it permissible under the current handoff.

### WF-SIDEWAYS-03 — Rejection-study test workflow

File: `.github/workflows/sideways-rejection-v1-tests.yml`

- Manual-dispatch only in the inspected trigger block; `contents: read`; `ubuntu-latest); checks out `price-action-v1).
- Installs/upgrades pip and installs NumPy/pandas, then compiles and runs focused tests.
- No push trigger or repository write permission was visible in the inspected file. It is still prohibited test execution.

### WF-SIDEWAYS-04 — Matched-covariate V10 audit

File: `.github/workflows/sideways-matched-covariate-audit-v10.yml`

- Triggers manually and on matching pushes to `price-action-v1`; explicitly declares `contents: write`; runs on `ubuntu-latest), installs NumPy/pandas/SciPy, and uploads a 14-day artifact.
- The static sample captured the trigger, permission, runner, checkout, dependency-install, execution, and artifact-upload sections. The complete terminal write behavior was not established in this targeted excerpt; do not infer that it pushes or does not push without a complete line-level review.

## Cross-cutting interpretation

1. A workflow's `contents: read` permission does not make its computation harmless: it may still execute prohibited scripts/tests, install dependencies, retrieve public data, or publish artifacts.
2. A workflow with `contents: write` plus explicit `git push` is a research-branch mutation path. It must be treated separately from the proposed isolated agent's report-only workflow.
3. Manual-only is not permission to run. The active handoff prohibits these workflow executions regardless of trigger type.
4. Matching push triggers are scoped to `price-action-v1`; documentation-only changes confined to `research_agent/` on `agent/okx-research-agent-v1` do not match the sampled branch/path filters.
5. This is a targeted sample, not proof that all 39 inherited workflows have been exhaustively inspected at every step. The earlier inventory remains the broader trigger/permission census; unknown effective repository/org Actions settings remain UNKNOWN.
6. The sampled workflows use mutable action version tags such as `actions/checkout@v4`, `actions/setup-python@v5`, and `actions/upload-artifact@v4`; this sample did not establish immutable full-SHA pinning.

## Required handling

- Do not dispatch, rerun, or otherwise invoke any sampled workflow while the handoff prohibits workflow execution.
- Do not push to `price-action-v1` or change watched research/workflow paths.
- Keep the agent's future workflow separate from inherited research workflows; do not repurpose these workflows as an agent runner.
- Any future workflow change, permission adjustment, or activation must be a separately reviewed security/governance decision, with exact trigger, checkout SHA, permissions, outputs, and branch-write behavior inspected.
- If a future task requires execution, obtain an explicit handoff update permitting that exact operation first; a general approval does not override a more specific prohibition.

## Explicit non-actions

No workflow was run, dispatched, rerun, cancelled, enabled, or edited. No matching push, test, script, package installation, public-data retrieval, artifact download/upload, research computation, candidate generation, or branch write occurred. No research code/data/tests/manifests/workflows or protected branch were changed. No G0-05 closure, strategy selection, PnL conclusion, or phase advancement occurred.

This document is a static documentation audit only. It does not activate the agent or authorize any workflow execution.
