# Inherited Funding, Phase 1, VPS, and Archive Workflow Boundary Audit — 2026-11-27

## Scope and authority

Static inspection of six workflow YAML files on `agent/okx-research-agent-v1`:

- `.github/workflows/funding-engine-contract-tests.yml`
- `.github/workflows/phase3-funding-coverage-audit.yml`
- `.github/workflows/phase3-funding-mark-price-full-audit.yml`
- `.github/workflows/phase1-uptrend-source-preflight.yml`
- `.github/workflows/vps-health-monitor.yml`
- `.github/workflows/research-archive-policy-check.yml`

The active G0-05 handoff remains controlling. This is a static YAML review only. No workflow was dispatched or executed; no tests, scripts, packages, market data, VPS host, SQLite files, logs, artifacts, or research outputs were accessed or modified.

## 1. Funding/execution-engine contract tests

- Push-triggered on `price-action-v1` for a broad set of funding, execution, portfolio, experiment, mark-price and test paths; no manual dispatch trigger is declared.
- Declares `contents: read`, checks out the triggering commit SHA, installs unpinned NumPy/pandas (and upgrades pip), compiles many source/test modules, and executes multiple unittest suites.
- The workflow name understates its scope: it includes funding, execution engine, portfolio backtester, exit experiments, trailing portfolio, portfolio safety, and mark-price audit helper tests.
- A matching push can execute a substantial test fleet automatically. Read-only token permission does not make this execution compatible with the active no-tests/no-workflows handoff.
- Runtime dependency resolution is not hash-locked in this YAML.

## 2. Phase 3 funding coverage tests

- Push-triggered on research-branch changes to the funding audit module, test module, or workflow; also manually dispatchable.
- Declares `contents: read`, checks out `price-action-v1`, compiles the audit/test modules and runs the deterministic funding coverage tests.
- No explicit artifact upload or protected-branch write appears in the inspected YAML.
- Still prohibited during the current handoff because it compiles and executes tests.

## 3. Phase 3 full-window funding mark-price audit

- Push-triggered on the full-window audit module, its test module, or workflow; also manually dispatchable.
- Declares `contents: write`, checks out the triggering commit SHA, compiles/runs helper tests, and executes a public funding/mark-price coverage audit.
- It validates a generated mark-price CSV against a hard-coded SHA-256 and fixed row counts (5,940 total; 1,188 per each of five assets), then prepares a manifest and README.
- It labels the dataset as a candidate proxy, explicitly says exact settlement mark is not verified, funding proxy policy is not accepted, and engine mode is unchanged.
- It fetches the research branch and requires the checkout HEAD to equal the current remote branch HEAD before committing/pushing a candidate-proxy snapshot.
- Uploads a 90-day artifact.
- The workflow includes an explicit VPS reproduction run ID and digest in the manifest. YAML-level equality to a hard-coded digest is a reproducibility check; it does not independently authenticate the VPS runner, workflow run, or source artifact.
- This is a data-producing, write-capable workflow, not a read-only audit worker. It is prohibited under the current handoff.

## 4. Phase 1 uptrend source preflight

- Manual and matching push triggers on `price-action-v1`, including changes to the workflow itself.
- Declares `contents: write`, checks out the research branch, installs unpinned pandas/NumPy, compiles/runs tests, and executes a five-asset Phase 1 input audit.
- Copies outputs into a permanent report archive and pushes commits to the research branch, with up to three pull/rebase/push attempts.
- Although named a preflight, this is active code/test execution and a permanent archive writer. It does not authorize Phase 1 advancement, and the agreed sequence requires Phase 3 completion first.
- It must not be used to bypass the current G0-05 gate or the agreed phase order.

## 5. VPS health monitor

- Manual dispatch only; declares `contents: read`.
- Runs on labels `self-hosted, linux, x64` and explicitly expects a runner installed on the VPS.
- Collects hostname, kernel, memory, root filesystem capacity, load, matching downloader process command lines, the last 40 lines of a downloader log, and names/sizes of SQLite files under a fixed home-directory path.
- Writes the report into the GitHub Actions step summary. It does not upload an artifact in the inspected YAML.
- The report can expose infrastructure details, process arguments, log contents, local paths, database filenames, and operational state into GitHub workflow logs/summaries. Repository visibility and access controls therefore matter; public repo outputs should be treated as public.
- The workflow is not part of the cloud-agent architecture and is not evidence that a VPS runner exists or is active. Do not dispatch it as an agent health check.
- No VPS, self-hosted runner, process, log, database, or host resource was inspected in this audit.

## 6. Research archive policy check

- Manual and matching push triggers for archive-policy documentation, Phase 3 archive paths, and the workflow itself.
- Declares `contents: read`, checks out the triggering ref, and performs shell presence/keyword checks.
- It verifies selected paths and text markers only. It does not validate archive provenance, schema, row counts, cryptographic integrity, source correctness, or phase-gate authorization.
- It executes shell commands and is therefore also prohibited by the current handoff despite read-only permissions.

## 7. Consolidated classification

| Workflow | Trigger | Permission | Executes code/tests | Data/branch side effect |
|---|---|---|---|---|
| Funding/execution-engine tests | Matching push | contents: read | Yes, compile + many test suites | No write shown |
| Funding coverage tests | Manual + matching push | contents: read | Yes, compile + tests | No write shown |
| Funding mark-price full audit | Manual + matching push | contents: write | Yes, tests + public data audit | Candidate dataset commit/push + artifact |
| Phase 1 source preflight | Manual + matching push | contents: write | Yes, tests + input audit | Permanent report commit/push + artifact |
| VPS health monitor | Manual only | contents: read | Yes, host inspection shell | Step summary may expose host/log details |
| Archive policy check | Manual + matching push | contents: read | Yes, shell checks | No write shown |

## 8. Implications for agent isolation and phase governance

1. Do not treat read-only permissions as permission to execute during a no-execution handoff.
2. Do not dispatch inherited workflows to validate the agent architecture; they are not agent workflows and several perform research, tests, data creation, or protected-branch writes.
3. Keep all Phase 1 workflows blocked until Phase 3 is fully completed and the owner-authorized phase transition is recorded.
4. Do not use the VPS health monitor as a proxy for cloud-agent status. It targets a self-hosted host and emits operational details into GitHub summaries.
5. Future health telemetry should be purpose-built, privacy-minimized, access-controlled, and should not disclose raw logs, process arguments, local paths, or database identifiers by default.
6. Future artifact/manifest checks need independent source-run identity and digest verification; hard-coded digests and declared reproduction IDs alone do not authenticate the producing workflow or host.
7. Workflow push triggers that include the workflow YAML itself can cause execution as a consequence of changing that workflow on the protected research branch. Never use such changes as a deployment or activation mechanism without explicit review and authorization.

## Evidence limits and non-actions

This is static inspection of the six listed YAML files only. It does not audit referenced source modules, test implementations, actual GitHub run history, effective organization/repository permissions, action implementations, package resolution, VPS installation, runner registration, host security, secrets, or artifact bytes. YAML declares intended behavior; it is not evidence that a job has run or passed.

No workflow, script, test, package installation, research calculation, data download, artifact operation, VPS/self-hosted runner, report, protected file, permission, secret, or branch outside the agent documentation scope was touched. G0-05 remains open; no candidate generation, backtesting, PnL analysis, strategy selection, gate closure, Phase 1 start, or agent activation was authorized.
