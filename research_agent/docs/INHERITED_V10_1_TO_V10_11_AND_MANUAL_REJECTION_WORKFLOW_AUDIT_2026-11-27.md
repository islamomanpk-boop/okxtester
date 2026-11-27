# Inherited V10.1–V10.11 and Manual Rejection Workflow Audit — 2026-11-27

## Scope and method

Static inspection only of these workflow files on `agent/okx-research-agent-v1`:

- `.github/workflows/sideways-rejection-v1-full-study.yml`
- `.github/workflows/sideways-rejection-v1-tests.yml`
- `.github/workflows/sideways-covariate-correlation-v10-1.yml`
- `.github/workflows/sideways-covariate-audit-v10-2.yml`
- `.github/workflows/sideways-balance-retention-v10-3.yml`
- `.github/workflows/sideways-alternative-matching-v10-4.yml`
- `.github/workflows/sideways-asset-direction-balance-v10-5.yml`
- `.github/workflows/sideways-balance-synthesis-v10-6.yml`
- `.github/workflows/sideways-minimum-sample-sensitivity-v10-7.yml`
- `.github/workflows/sideways-covariate-persistence-v10-8.yml`
- `.github/workflows/sideways-distributional-overlap-v10-9.yml`
- `.github/workflows/sideways-joint-support-v10-10.yml`
- `.github/workflows/sideways-joint-support-percentile-v10-11.yml`

No workflow was dispatched, no script or test was run, no artifact was downloaded, and no research code, test, workflow, dataset, report, branch protection, or repository setting was changed. This is a workflow-contract review, not evidence that any listed run occurred.

## Findings

### 1. V10.1–V10.11 are push-triggered research execution and archive writers

All eleven V10.1–V10.11 workflows declare both `workflow_dispatch` and a `push` trigger scoped to `price-action-v1` and matching workflow/research/test paths. A qualifying push can therefore launch research work without a manual dispatch.

All eleven declare `permissions: contents: write`, check out `price-action-v1`, use `ubuntu-latest` and Python 3.11, compile/run version-specific tests, execute a research diagnostic or sensitivity, and contain a step that copies generated outputs into a versioned directory under `reports/sideways_phase3_research_archive_v1/`, configures the GitHub Actions bot, commits the archive, and pushes `HEAD:price-action-v1`. They also upload a secondary artifact with 14-day retention.

The family is an ordered dependency chain, not eleven interchangeable independent checks:

| Workflow | Principal role / upstream dependency |
|---|---|
| V10.1 | Covariate-correlation diagnostic; consumes episode anatomy, early-path sequence, detector features, and minute data. |
| V10.2 | Covariate redundancy/balance attribution; additionally consumes V6 matched pairs and V10.1 correlation output. |
| V10.3 | Balance-retention frontier; consumes V10.2 stratum balance, V6 pairs, and V9 feasibility summary. |
| V10.4 | Alternative matching-constraint sensitivity; consumes anatomy, sequence, features, and minute data. |
| V10.5 | Asset-direction balance attribution; consumes anatomy, sequence, features, and minute data. |
| V10.6 | Stable-stratum balance synthesis; consumes V10.5 balance output. |
| V10.7 | Minimum subgroup-size sensitivity; consumes V10.5 and V10.6 archived outputs. |
| V10.8 | Covariate-imbalance persistence; consumes V10.7 detail output. |
| V10.9 | Empirical distributional-overlap audit; consumes anatomy, sequence, V6 matched pairs, features, and minute data. |
| V10.10 | Joint common-support retention; consumes anatomy, sequence, V6 matched pairs, features, and minute data. |
| V10.11 | Joint-support percentile sensitivity; consumes anatomy, sequence, V6 matched pairs, features, and minute data. |

The exact workflow files should be consulted for each output path and command-line input contract. This table summarizes declared dependencies; it does not validate the underlying research methods or results.

### 2. Write-capable workflow details and operational implications

- V10.1 and V10.2 install NumPy, pandas, and SciPy; V10.3 uses pandas; V10.4 and V10.5 install NumPy, pandas, and SciPy; V10.6–V10.8 use pandas; V10.9–V10.11 install NumPy, pandas, and SciPy.
- V10.1–V10.5 push archive commits directly when staged changes exist. V10.6 performs a pull/rebase before pushing. V10.7–V10.11 include bounded retry loops around pull/rebase and push.
- V10.1–V10.11 use action references such as `actions/checkout@v4`, `actions/setup-python@v5`, and `actions/upload-artifact@v4`; these are version tags, not immutable full commit SHA pins.
- The push filters are limited to each workflow file and its corresponding research/test files. This reduces unrelated triggers but does not make the workflow manual-only.
- The declared write permission and explicit Git push commands make these workflows materially different from read-only analysis jobs. A workflow-file or matching research/test change on `price-action-v1` can itself trigger execution, so changes to those paths are not a safe route for agent activation or review.
- The static YAML does not establish effective repository/org policy settings, whether a particular push event will be permitted by all GitHub rules, or whether any workflow run completed.

### 3. Manual rejection V1 full-study workflow

`sideways-rejection-v1-full-study.yml` is manual-only (`workflow_dispatch`) and declares `contents: read`. It checks out `price-action-v1`, compiles and runs the focused forward-outcome test, verifies nonempty 1-minute BTC/ETH/SOL/DOGE/AVAX CSVs and their expected header, then runs the frozen five-asset historical forward-outcome study. It uploads generated reports as a 14-day artifact and contains no explicit Git commit/push step.

Although it is read-only with respect to repository contents, it still executes research code and tests and reads historical market datasets. The current G0-05 handoff prohibits dispatching it.

### 4. Manual rejection V1 test workflow

`sideways-rejection-v1-tests.yml` is manual-only and declares `contents: read`. It checks out `price-action-v1`, compiles the forward-outcome module/test and episode-retest anatomy module/test, and runs both focused unit-test suites. It contains no research dataset study, artifact upload, or Git push.

This is still test execution, which the active G0-05 handoff prohibits. Read-only token permission does not make prohibited execution permissible.

### 5. Shared supply-chain and output observations

All thirteen inspected workflows use hosted `ubuntu-latest` runners and mutable major-version action tags. Python package installation is performed at runtime without a checked-in hash-locked dependency set visible in these workflow definitions. The V10 family publishes both a Git-archived report set and a shorter-lived Actions artifact; the manual full-study workflow publishes an Actions artifact only. This audit does not establish the repository's artifact visibility/retention settings beyond the YAML declarations.

These are supply-chain, provenance, and public-output review items for a future separately authorized workflow-security gate. They are not instructions to alter inherited workflows during the current handoff.

## Binding G0-05 disposition

The active Phase 3 G0-05 handoff remains controlling. None of these workflows may be used as a shortcut for agent activation, evidence generation, or gate closure. Do not dispatch, push matching workflow/research/test paths, run scripts/tests, invoke Actions by API, or route work through another agent/workflow while the handoff prohibits execution.

The future agent workflow must remain isolated from this inherited fleet. A separate agent repository or an explicitly reviewed manual-only caller/reusable-workflow arrangement is still a separate activation decision; neither is authorized by this audit.

## Evidence limits

- The evidence is static YAML content fetched from the agent branch; no workflow run logs, artifacts, live repository Actions settings, or runtime results were inspected here.
- A declared workflow command is not evidence it ran or passed.
- A GitHub Actions `contents: write` declaration plus a push command describes a potential write path; actual effective permissions and branch-policy enforcement require separate live settings review.
- No inference is made that the V10 diagnostics are statistically valid, that their archived inputs exist or are correct, or that any G0-05 requirement is satisfied.
