# Inherited Sideways Anatomy, Follow-Through and Taxonomy Workflow Audit — 2026-11-27

## Scope and authority

Static inspection of four additional workflow YAML files. The active G0-05 handoff prohibits workflow, script, test, and research execution. No workflow was run or dispatched.

## 1. Boundary interaction and penetration taxonomy

File: `.github/workflows/sideways-boundary-interaction-taxonomy-v1.yml`.

- Manual dispatch only; declares `contents: read`; checks out `price-action-v1`.
- Installs NumPy/pandas, compiles the taxonomy module/tests, and runs synthetic tests.
- Reconstructs 15-minute bars from five frozen 1-minute market datasets inside the runner.
- The inline reconstruction rejects duplicate/unordered timestamps and non-continuous one-minute cadence; retains complete epoch-aligned 15-minute bars and asserts exactly 37,941 rows per asset.
- Runs the historical taxonomy and uploads a 14-day artifact.
- No Git commit/push step appears in the inspected YAML.

Manual-only/read-only does not make it permissible under the active no-execution handoff. The 37,941 assertion is a workflow contract, not a result independently verified here.

## 2. Early-path sequence and follow-through

File: `.github/workflows/sideways-rejection-early-path-sequence-followthrough-v1.yml`.

- Manual dispatch plus push trigger on `price-action-v1`, but the push path filter is only this workflow file.
- Declares `contents: read`; checks out `price-action-v1`.
- Compiles two research modules and tests, runs both test suites, checks frozen source inputs, executes the five-asset historical sequence/follow-through study, and uploads a 14-day artifact.
- No Git commit/push step appears in the inspected YAML.

Although token permissions are read-only, it is still a historical research execution surface. The workflow-file-only push filter means a workflow edit can trigger the job on the protected branch.

## 3. Episode/retest anatomy and early-path multi-study workflow

File: `.github/workflows/sideways-rejection-episode-retest-anatomy-v1.yml`.

- Manual dispatch plus push trigger on `price-action-v1`, filtered to this workflow file.
- Declares `contents: write`; checks out `price-action-v1`.
- Compiles six research modules and six corresponding test modules, then runs multiple focused test suites.
- Runs five-asset episode/retest anatomy and early-path studies, a 10,000-replicate sequence block bootstrap, and two 10,000-replicate matched-control sensitivities.
- Permanently archives multiple result families and a README under `reports/sideways_phase3_research_archive_v1/`, then commits/pushes to `price-action-v1`.
- Uploads five secondary artifacts, each with 14-day retention.

This is a broad research execution and protected-branch write workflow, not a safe agent runner. Its archive README itself characterizes bootstrap contrasts as descriptive observational comparisons rather than causal estimates or proof of a profitable strategy.

## 4. V10 matched covariate audit

File: `.github/workflows/sideways-matched-covariate-audit-v10.yml`.

- Manual dispatch plus matching push trigger on `price-action-v1`.
- Declares `contents: write`; checks out the protected branch.
- Compiles/runs tests and an outcome-blind covariate audit using frozen V6 matched pairs and V9 feasibility outputs.
- Archives the result in Git, commits/pushes to `price-action-v1`, and uploads a 14-day secondary artifact.

This is another inherited research writer and should remain outside any future agent allowlist under the current handoff.

## 5. Classification

| Workflow | Trigger | Permission | Declared activity | Git write in YAML |
|---|---|---|---|---|
| Boundary taxonomy | Manual only | contents: read | Tests + 1m-to-15m reconstruction + historical taxonomy | No |
| Early-path follow-through | Manual + workflow-file push | contents: read | Tests + five-asset historical study | No |
| Episode/retest multi-study | Manual + workflow-file push | contents: write | Multiple tests + historical studies + bootstrap/matching | Yes |
| V10 covariate audit | Manual + matching push | contents: write | Tests + covariate audit | Yes |

## Evidence limits and non-actions

This is static YAML inspection only. It does not validate referenced source code, frozen data, generated outputs, artifact contents, effective repository/organization permissions, or actual workflow-run history. Workflow assertions and descriptions are not runtime evidence.

No workflow was executed, dispatched, rerun, cancelled, enabled, or modified. No tests, scripts, packages, research calculations, data downloads, artifacts, VPS/self-hosted runners, permissions, secrets, protected research files, or `price-action-v1` state were touched. No G0-05 decision, phase status, candidate status, or agent activation state changed.
