# Inherited G0-04/G0-05 and Lifecycle Workflow Boundary Audit — 2026-11-27

## Scope and authority

Static inspection of eight workflow YAML files on `agent/okx-research-agent-v1`. The active G0-05 handoff remains controlling: no workflow, script, test, or research execution. This document records declared workflow behavior only; it does not assert any run occurred or passed.

## 1. G0-04 causal reconstruction workflow

File: `.github/workflows/phase3-g0-04-causal-breakout-reconstruction.yml`.

- Manual dispatch and push trigger scoped to `price-action-v1` changes in the G0-04 script/workflow.
- Declares `contents: read`; checks out `price-action-v1` with `persist-credentials: false`.
- Installs pinned NumPy/pandas, compiles the script, runs its self-test, then runs descriptive reconstruction.
- Uploads output artifact with 14-day retention.
- No commit/push step is present in the inspected YAML.

The workflow is still an execution surface and is prohibited by the current handoff, despite read-only token permission and no persistent Git write step.

## 2. G0-05 source audit and independent minute verification

### Source audit

File: `.github/workflows/phase3-g0-05-source-audit.yml`.

- Manual dispatch and push trigger on `price-action-v1` changes to its script/workflow.
- Declares `contents: read` and `actions: read`; checks out the protected research branch with persisted credentials disabled.
- Downloads a specifically named G0-04 artifact using fixed workflow run ID `45756061179`.
- Compiles and runs the read-only source/provenance audit; uploads a 14-day artifact.
- No Git commit/push step is present in the inspected YAML.

### Independent exact-minute verification

File: `.github/workflows/phase3-g0-05-independent-minute-verification.yml`.

- Manual dispatch and push trigger on `price-action-v1` changes to its script/workflow.
- Declares `contents: read` and `actions: read`; checks out the protected branch with persisted credentials disabled.
- Queries successful source-audit workflow runs, filters for an exact hard-coded source commit SHA, then downloads the named source-audit artifact.
- Compiles and runs independent raw-file re-hashing and exact-minute membership verification; uploads a 14-day artifact.
- No Git commit/push step is present in the inspected YAML.

These are chained evidence-producing executions, not harmless configuration checks. Their artifact lineage, fixed run/commit selectors, retention, and actual outputs require evidence review; this static YAML inspection does not validate the referenced historical artifacts or prove that the chain completed.

## 3. G0-05 candidate contract synthetic tests

File: `.github/workflows/phase3-g0-05-candidate-contract-tests.yml`.

- Manual dispatch and push trigger on protected-branch changes to candidate-contract script/test/workflow.
- Declares `contents: read`; checkout uses `persist-credentials: false`.
- Compiles the contract module and test, then runs synthetic contract tests.
- No canonical market data load, artifact upload, or Git write is declared in the inspected YAML.

The workflow comment says contract-only, but it remains code execution and is prohibited by the current handoff. Static review cannot substitute for test results.

## 4. Rejection lifecycle V1 and V1.1 workflows

Files:
- `.github/workflows/phase3-rejection-lifecycle-v1.yml`
- `.github/workflows/phase3-rejection-lifecycle-v1-1.yml`

Both:
- Have manual and push triggers on `price-action-v1`.
- Declare `contents: write`, checkout the canonical research branch, run synthetic tests and historical lifecycle scripts.
- Assert hard-coded output counts and market-gap/overlap conditions.
- Upload 90-day artifacts and commit/push generated reports back to `price-action-v1`.

V1 asserts 1,992 eligible/event rows, 7,968 horizon rows, and broad/strict cohort counts 1,154/838. V1.1 additionally asserts 3,028 episode rows and overlap-cluster conditions. These are workflow acceptance assertions, not new validation performed by this audit.

These are direct protected-branch research writers. They are not agent workflows and must not be dispatched under the current handoff.

## 5. Funding workflow boundary

### Funding coverage tests

File: `.github/workflows/phase3-funding-coverage-audit.yml`.

- Manual and matching push triggers; `contents: read`; checks out `price-action-v1`.
- Compiles and runs deterministic funding coverage tests.
- No artifact upload or Git write step is present.

Still prohibited because tests execute.

### Full-window funding/mark-price audit

File: `.github/workflows/phase3-funding-mark-price-full-audit.yml`.

- Manual and matching push triggers; declares `contents: write`.
- Checks out the triggering commit SHA, compiles/runs tests, and performs a public funding/mark-price coverage audit.
- Generates a mark-price snapshot, verifies a hard-coded digest and row-count contract, records a manifest, and pushes a versioned dataset under `data/funding_mark_price_proxy_candidate_v1/` to `price-action-v1`.
- The generated manifest explicitly labels the data `CANDIDATE_PROXY_NOT_EXACT_SETTLEMENT_MARK`, with `exact_settlement_mark_verified: false`, `funding_proxy_policy_accepted: false`, and `engine_mode_changed: false`.
- Uploads a 90-day artifact.

The workflow's own metadata distinguishes a candle-derived proxy from exact settlement mark data. This audit does not validate the underlying dataset or the embedded digest; it records only the workflow's declared assertions and output behavior.

## 6. Classification

| Workflow | Trigger | Permission | Declared activity | Git write in YAML |
|---|---|---|---|---|
| G0-04 reconstruction | Manual + push | contents: read | Self-test + descriptive reconstruction | No |
| G0-05 source audit | Manual + push | contents/actions: read | Artifact download + source audit | No |
| G0-05 minute verification | Manual + push | contents/actions: read | Run lookup + artifact download + independent verifier | No |
| G0-05 contract tests | Manual + push | contents: read | Compile + synthetic tests | No |
| Rejection lifecycle V1/V1.1 | Manual + push | contents: write | Tests + historical research + archive | Yes |
| Funding coverage tests | Manual + push | contents: read | Compile + tests | No |
| Funding/mark-price full audit | Manual + push | contents: write | Tests + data audit + candidate-proxy dataset | Yes |

## Evidence limits and non-actions

This is a static review of eight workflow YAML files. It does not inspect or execute every referenced script, authenticate artifact provenance, validate fixed historical run IDs, inspect effective repository/organization permissions, or establish workflow-run history. The hard-coded SHA/run selectors and YAML assertions are recorded as source facts only.

No workflow was executed, dispatched, rerun, cancelled, enabled, or modified. No tests, scripts, packages, research calculations, market-data retrieval, artifacts, VPS/self-hosted runners, permissions, secrets, protected research files, or `price-action-v1` state were touched. No G0-05 decision, phase status, candidate status, or agent activation state changed.
