# Inherited Breakout, Completion, Archive-Policy and Phase-1 Workflow Audit — 2026-11-27

## Scope and authority

Static inspection of five workflow YAML files on `agent/okx-research-agent-v1`. The controlling G0-05 handoff prohibits workflow, script, test, and research execution. The agreed phase order remains Phase 3 complete before Phase 1. This audit makes no gate or phase decision.

## 1. Breakout lifecycle V1.1

File: `.github/workflows/phase3-breakout-lifecycle-v1-1.yml`.

- Manual dispatch and push trigger on protected `price-action-v1` paths.
- Declares `contents: write`, checks out `price-action-v1`, installs pinned NumPy/pandas, runs synthetic tests and the historical breakout lifecycle script.
- Asserts 1,592 primary events, 1,537 primary links, 6,368 horizon rows, full forward crosscheck, 569,125 common 1-minute timestamps, zero gaps, and overlap-cluster conditions.
- Critically, its result contract explicitly expects `forward_archive_unavailable_lifecycle_fields` to contain exactly the five descriptive retest fields: `outside_retest`, `outside_retest_boundary_crossed`, `outside_retest_minutes`, `outside_retest_depth_pct_of_boundary`, and `outside_retest_hold`.
- Uploads a 90-day artifact and commits/pushes reports to `price-action-v1`.

This independently reinforces the documented limitation: those five fields are explicitly marked unavailable in the forward archive contract. It does not prove their real-row sourceability or authorize filling them. The workflow is a protected-branch research writer and is prohibited by the current handoff.

## 2. Phase 3 completion archive validation

File: `.github/workflows/phase3-completion-validation.yml`.

- Manual dispatch and push trigger on selected Phase 3 archive/decision files.
- Declares `contents: read`, checks out `price-action-v1`.
- Checks existence of selected source archives and validates that V10.11 central-90 rows reproduce V10.10 baseline counts.
- Asserts V10.11 metadata says outcomes were not loaded/compared and checks summary/detail row counts.
- Finally greps the closeout decision for text saying to stop the V6 matched-controls branch and mentioning Phase 1.

The YAML describes an archive-presence and selected consistency validator, not an independent G0-05 sourceability review, full research-quality review, or authorization engine. Presence of a closeout text marker is not itself proof that all governing gates are closed. The workflow remains prohibited by the handoff despite read-only permissions.

## 3. Research archive policy check

File: `.github/workflows/research-archive-policy-check.yml`.

- Push trigger on `price-action-v1` for archive policy, Phase 3 archive, or workflow changes; also manual dispatch.
- Declares `contents: read`; checks out the triggering ref (no explicit `ref` override).
- Performs shell existence/keyword checks for the archiving rule and archive README.
- No research script, Python test, artifact upload, or Git write step appears in the inspected YAML.

This is a comparatively narrow policy-presence check, but it still executes a workflow on the protected research branch and is not an authorized exception to the handoff.

## 4. Funding/execution engine contract test workflow

File: `.github/workflows/funding-engine-contract-tests.yml`.

- Push-only trigger on `price-action-v1` changes across funding, execution, portfolio, experiment, verification, and mark-price audit modules/tests.
- Declares `contents: read`, checks out the triggering commit SHA.
- Installs NumPy/pandas, compiles a broad set of modules, and runs focused funding, loader, execution engine, portfolio, experiment, trailing, allocator, and safety test suites.
- No artifact upload or Git write step appears in the inspected YAML.

Although no manual dispatch is declared and token permissions are read-only, this is still an executable test workflow. It is not part of the isolated agent and cannot be used to validate the agent under the current handoff.

## 5. Phase 1 Uptrend source preflight

File: `.github/workflows/phase1-uptrend-source-preflight.yml`.

- Manual dispatch and push trigger on `price-action-v1`.
- Declares `contents: write`, checks out the protected research branch, installs dependencies, compiles/runs Phase 1 tests, and executes a five-asset source-input audit.
- Permanently archives the output under `reports/phase1_uptrend_research_v1/data_preflight_v1`, commits/pushes to `price-action-v1` with pull/rebase retry logic, and uploads a 14-day secondary artifact.

This is a concrete cross-phase execution hazard: its manual trigger makes it technically dispatchable, but the agreed research order requires Phase 3 to be fully completed before Phase 1 begins. The current G0-05 handoff independently prohibits execution. Do not dispatch it, and do not treat its existence as permission to advance phases.

## 6. Classification

| Workflow | Trigger | Permission | Declared activity | Git write in YAML |
|---|---|---|---|---|
| Breakout lifecycle V1.1 | Manual + push | contents: write | Tests + historical lifecycle + archive assertions | Yes |
| Phase 3 completion validator | Manual + push | contents: read | Archive existence + V10.10/V10.11 consistency + closeout text checks | No |
| Archive policy check | Manual + push | contents: read | Shell presence/keyword checks | No |
| Funding/execution contract tests | Push only | contents: read | Compile + broad focused test suites | No |
| Phase 1 source preflight | Manual + push | contents: write | Tests + source audit + permanent archive | Yes |

## Evidence limits and non-actions

Static YAML review only. It does not inspect or execute referenced scripts/tests, validate archived outputs, prove G0-05 closure, assess Phase 3 completeness, or inspect effective repository/organization permissions and workflow-run history. The workflow's assertions and grep checks are recorded as source contracts, not as test results.

No workflow was executed, dispatched, rerun, cancelled, enabled, or modified. No tests, scripts, packages, research calculations, data downloads, artifacts, VPS/self-hosted runners, permissions, secrets, protected research files, or `price-action-v1` state were touched. No phase advanced, gate closed, or candidate/strategy decision changed.
