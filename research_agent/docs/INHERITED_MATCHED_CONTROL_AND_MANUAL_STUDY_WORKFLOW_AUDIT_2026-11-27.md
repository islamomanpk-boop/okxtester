# Inherited Matched-Control and Manual Study Workflow Audit — 2026-11-27

## Scope and authority

Static inspection of eight additional workflow files on `agent/okx-research-agent-v1`. This is a documentation-only audit. The active G0-05 handoff remains controlling and prohibits workflow, script, test, and research execution. No inspected workflow was run or dispatched.

## 1. V3–V6 matched-control sensitivity workflows

Files:
- `.github/workflows/sideways-pre-event-matched-controls-v3.yml`
- `.github/workflows/sideways-pre-event-matched-controls-v4.yml`
- `.github/workflows/sideways-pre-event-matched-controls-v5.yml`
- `.github/workflows/sideways-pre-event-matched-controls-v6.yml`

Static observations:
- All declare `workflow_dispatch` and a push trigger on `price-action-v1`.
- All declare `contents: write`, use `ubuntu-latest`, and explicitly checkout `price-action-v1`.
- All install Python research dependencies, compile and run their version-specific tests, and execute historical matching sensitivity research.
- V3/V4 specify 10,000 replicates and fixed seed 20261124, with distinct matching constraints; V5 executes an outcome-blind caliper grid; V6 executes optimal-assignment sensitivity.
- All copy generated outputs into version-controlled `reports/sideways_phase3_research_archive_v1/` subdirectories, commit, and push to `price-action-v1`.
- All upload secondary artifacts with 14-day retention.

These are protected-branch research writers, not reusable read-only agent workers.

## 2. V10.7 minimum-sample sensitivity

File: `.github/workflows/sideways-minimum-sample-sensitivity-v10-7.yml`.

- Manual and matching push triggers on `price-action-v1`.
- `contents: write`; checkout of `price-action-v1`.
- Compiles/runs tests and a subgroup-size sensitivity diagnostic using frozen V10.5 and V10.6 outputs.
- Copies the result into the permanent V10.7 archive.
- Uses up to three pull/rebase/push attempts to publish the archive, then uploads a 14-day secondary artifact.

Retry/rebase logic is not a safety boundary. It is an explicit mechanism to keep attempting a protected-branch write after concurrent changes.

## 3. Matched-asset robustness workflow

File: `.github/workflows/sideways-matched-asset-robustness-v1.yml`.

- Manual dispatch plus a push trigger on `price-action-v1` when this workflow file changes.
- `contents: write`; checks out the research branch.
- Installs NumPy/pandas, compiles and runs tests, then executes asset-level and leave-one-asset-out robustness with 10,000 replicates and fixed seed 20261124.
- Archives results in Git, commits/pushes to `price-action-v1`, and uploads a 14-day artifact.

The workflow-file-only push filter is notable: editing that workflow on the research branch can itself trigger a historical research job.

## 4. Manual-only full study and test workflows

### `sideways-rejection-v1-full-study.yml`

- Manual dispatch only; `contents: read`; Ubuntu runner; explicitly checks out `price-action-v1`.
- Installs Python dependencies, compiles/runs focused tests, validates five historical market datasets, then executes a five-asset historical forward-outcome study.
- Uploads generated research reports as a 14-day artifact.
- The inspected YAML does not commit/push generated reports.

### `sideways-rejection-v1-tests.yml`

- Manual dispatch only; `contents: read`; Ubuntu runner; explicitly checks out `price-action-v1`.
- Installs dependencies, compiles the forward-outcome and episode/retest-anatomy modules, and executes two test suites.
- The inspected YAML does not run the full historical study, upload artifacts, or commit/push outputs.

Both workflows are still prohibited under the current G0-05 handoff. Manual-only and read-only token permissions do not override a no-execution instruction.

## 5. Classification and controls

| Workflow group | Trigger | Token permission | Executes code | Protected-branch write |
|---|---|---|---|---|
| V3–V6 matching | Manual + matching push | contents: write | Tests + research | Yes |
| V10.7 sensitivity | Manual + matching push | contents: write | Tests + research | Yes, retry/rebase |
| Matched-asset robustness | Manual + workflow-file push | contents: write | Tests + research | Yes |
| Full historical study | Manual only | contents: read | Tests + historical study | No in inspected YAML |
| Read-only tests | Manual only | contents: read | Compile + tests | No in inspected YAML |

These categories must remain outside any future agent allowlist while the current handoff applies. A future agent workflow must be independently designed, reviewed, authorized, and isolated; inherited workflows are not a substitute.

## Evidence limits and non-actions

This is a static review of the listed YAML files, not a complete audit of referenced scripts, dependency supply chain, runner images, effective repository/organization settings, secrets, environments, or action implementations. YAML declarations describe intended workflow behavior; they are not evidence that a workflow ran or that a result passed.

No workflow was executed, dispatched, rerun, cancelled, enabled, or modified. No tests, scripts, packages, research calculations, data downloads, artifact operations, VPS/self-hosted runners, permissions, secrets, protected research files, or `price-action-v1` state were touched. No G0-05 decision, phase status, candidate status, or agent activation state changed.
