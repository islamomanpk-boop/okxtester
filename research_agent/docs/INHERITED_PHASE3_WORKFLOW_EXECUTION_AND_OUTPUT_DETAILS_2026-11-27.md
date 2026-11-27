# Inherited Phase 3 Workflow Execution and Output Details — 2026-11-27

## Scope and method

This is a documentation-only continuation of the inherited workflow fleet audit. It records exact behaviors visible in nine workflow YAML files on `agent/okx-research-agent-v1`. The review is static: no workflow, script, test, package installation, artifact operation, research computation, or branch write was executed.

The controlling `price-action-v1` G0-05 reconciliation handoff remains authoritative. Every workflow listed here remains prohibited while that handoff prohibits script, test, and workflow execution. Read-only token permissions do not create an exception.

## 1. Write-capable lifecycle workflows

### `phase3-rejection-lifecycle-v1.yml`

Static facts:
- Triggers on `workflow_dispatch` and matching pushes to `price-action-v1`; watched paths include the lifecycle research script, its test, a checkpoint document, and the workflow itself.
- Declares `contents: write`; runs on `ubuntu-latest`; checks out `price-action-v1`; installs Python 3.11.
- Executes the synthetic lifecycle test, then the historical lifecycle script.
- Runs inline assertions against archived metadata: 1,992 eligible events, 1,992 event-level rows, 7,968 horizon rows, broad/strict counts of 1,154/838, and zero market-source gaps.
- Uploads a 90-day artifact and then commits/pushes generated reports to `price-action-v1`.

### `phase3-rejection-lifecycle-v1-1.yml`

Static facts:
- Same trigger shape and `contents: write` permission, with watched paths for the V1.1 script/test, overlap-cluster checkpoint, and workflow file.
- Executes V1.1 synthetic lifecycle/overlap tests and historical lifecycle script.
- Inline metadata assertions include 1,992 eligible events, 1,992 event-level rows, 3,028 episode rows, 7,968 horizon rows, broad/strict counts 1,154/838, zero market-source gaps, and nonzero overlap-cluster checks.
- Uploads a 90-day artifact and commits/pushes generated reports to `price-action-v1`.

These hard-coded archive contracts are workflow assertions, not independent validation performed in this audit. The workflows are not safe agent runners because they execute research and write the protected research branch.

## 2. Multi-study archive workflow

### `sideways-rejection-episode-retest-anatomy-v1.yml`

Static facts:
- Has `workflow_dispatch` and a push trigger on `price-action-v1`; the only listed push path is the workflow YAML itself.
- Declares `contents: write`, runs on `ubuntu-latest`, checks out `price-action-v1`, and installs/upgrades pip plus NumPy and pandas.
- Compiles multiple research modules/tests and executes six test groups.
- Requires existing frozen event, feature, and one-minute market files for BTC, ETH, SOL, DOGE, and AVAX.
- Executes episode/retest anatomy, early-path follow-through, a 10,000-replicate calendar block bootstrap, and two pre-event matched-control sensitivity studies.
- Copies outputs into a version-controlled Phase 3 archive, writes an archive README, then commits/pushes that archive to `price-action-v1`.
- Uploads five separate artifacts with 14-day retention.

The narrow push path means a change to this workflow file itself can trigger a multi-study research run on the canonical branch. The branch write and research execution make it categorically unsuitable for agent reuse.

## 3. Funding/mark-price candidate-proxy write path

### `phase3-funding-mark-price-full-audit.yml`

Static facts:
- Push/manual triggers; push paths include the funding/mark-price script, its test, and the workflow.
- Declares `contents: write`; uses `ubuntu-latest`; checks out the triggering SHA.
- Compiles and runs helper tests, then runs a full-window funding/mark-price coverage audit.
- The next step is explicitly named as committing an immutable mark-price proxy candidate snapshot. Its environment contains fixed expected SHA-256 values and a prior VPS reproduction run ID.
- The visible workflow code checks the generated CSV digest and metadata before creating the candidate-proxy data/manifest output. The workflow's later archive/push behavior is not exhaustively reproduced in this summary; the static classification as a write-capable candidate-proxy path is based on the inspected workflow.
  
This is especially sensitive: a proxy-labelled dataset or manifest is not equivalent to a canonical G0-05 candidate, and the existence of a workflow step does not authorize candidate creation or change the current handoff.

## 4. Read-only permission does not mean non-executing

The following workflows declare `contents: read`, but their YAML still executes code and therefore remains prohibited by the current handoff:

- `sideways-rejection-early-path-sequence-followthrough-v1.yml`: runs a historical research script and uploads an artifact.
- `sideways-boundary-interaction-taxonomy-v1.yml`: reconstructs 15-minute bars in an inline Python block, invokes a historical taxonomy script, and uploads an artifact.
- `phase3-completion-validation.yml`: checks archived files and runs inline Python comparisons/assertions over archived V10.10/V10.11 outputs, then checks closeout-record text.
- `phase3-funding-coverage-audit.yml`: compiles the funding coverage audit/test and executes the deterministic test suite.
- `funding-engine-contract-tests.yml`: installs/upgrades pip and installs NumPy/pandas; compiles execution/funding modules and executes multiple funding, execution-engine, portfolio, and integration test suites.

The first two publish artifacts; the completion validator and test workflows are still execution, even where no report commit or artifact upload is present in the inspected YAML. Their read-only permission block constrains token writes; it does not make Python execution, test execution, data reads, or workflow side effects disappear.

## 5. Operational conclusions

1. Do not dispatch, rerun, enable, edit, or otherwise trigger any inherited workflow while the active G0-05 handoff prohibits it.
2. Do not use a matching push as an alternative to manual dispatch. Push-triggered workflows can execute automatically when their watched paths change on `price-action-v1`.
3. Do not treat `contents: read` as a blanket safe-execution label.
4. Keep inherited research workflows outside any future agent dispatch allowlist. A future agent workflow must be separately designed and reviewed, with exact immutable source pinning, explicit minimal permissions, an isolated execution surface, and a public-output policy.
5. The Phase 1 workflow remains out of scope until Phase 3 is fully completed and the next handoff authorizes Phase 1.

## Evidence limits and non-actions

This is a targeted static sample, not a complete workflow/action/script/dependency/runner/secret/environment or repository-settings audit. The repository/organization Actions settings remain unknown where not returned by the read connection. The review does not establish that any workflow has run recently or that its archived assertions pass.

No workflow was executed, dispatched, rerun, cancelled, enabled, or modified. No scripts, tests, packages, data downloads, research calculations, artifact operations, VPS/self-hosted runners, permissions, secrets, research files, or protected branch state were touched. No G0-05 status, phase, candidate, strategy, or agent activation state was changed.
