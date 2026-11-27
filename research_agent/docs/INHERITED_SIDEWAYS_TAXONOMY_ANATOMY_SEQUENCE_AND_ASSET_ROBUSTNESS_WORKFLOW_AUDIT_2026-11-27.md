# Inherited Sideways Taxonomy, Anatomy, Sequence, and Asset-Robustness Workflow Audit — 2026-11-27

## Scope and authority

Static inspection of four workflow YAML files on `agent/okx-research-agent-v1`:

- `.github/workflows/sideways-boundary-interaction-taxonomy-v1.yml`
- `.github/workflows/sideways-rejection-episode-retest-anatomy-v1.yml`
- `.github/workflows/sideways-rejection-early-path-sequence-followthrough-v1.yml`
- `.github/workflows/sideways-matched-asset-robustness-v1.yml`

The active Phase 3 G0-05 handoff remains controlling. This review is static only. No workflows, scripts, tests, packages, source datasets, artifacts, or reports were executed, downloaded, or modified.

## 1. Boundary interaction and penetration taxonomy V1

- Manual dispatch only; declares `contents: read`; checks out `price-action-v1`.
- Installs NumPy/pandas, compiles the taxonomy module and tests, and runs the synthetic test suite.
- Checks each of five one-minute CSVs for non-empty content and an exact header.
- Reconstructs 15-minute candles inline from the 1-minute data. It checks timestamp uniqueness/order, exact 60,000 ms cadence, and keeps only complete 15-minute buckets; it then requires exactly 37,941 reconstructed bars per asset.
- The step name says "Verify frozen 15-minute source hashes and run historical taxonomy", but the visible YAML command only invokes the taxonomy module with reconstructed data and the feature directory. No explicit hash comparison appears in the shown workflow step. The module may implement additional checks; that requires separate source inspection. Do not infer that a hash was verified merely from the step label.
- Uploads the historical study outputs as a 14-day artifact.
- Although the token is read-only, this is a full historical study and test execution, prohibited by the current no-execution handoff.

## 2. Rejection episode/retest anatomy and early-path historical studies V1

- Manual dispatch plus a push trigger on `price-action-v1` when this workflow YAML path changes.
- Declares `contents: write`; checks out the research branch.
- Compiles six research modules and six test modules, runs six synthetic test suites, and checks existence of the historical boundary event CSV, five feature files, and five 1-minute market files using `test -f`.
- Executes the five-asset episode/retest anatomy study and early-path sequence/follow-through study, then a 10,000-replicate calendar moving-block bootstrap (seed 20261124).
- Executes initial and stricter pre-event matched-control studies, each with 10,000 replicates and seed 20261124; V2 additionally passes max-distance 1.5 and max-absolute-difference 0.75.
- Permanently archives five groups of generated reports and pushes the commit to `price-action-v1`; uploads five secondary artifacts with 14-day retention.
- The input guards establish only file existence, not non-empty content, schema, digest, exact commit provenance, or cross-file consistency.
- The workflow's path-only push filter means a matching edit to the workflow YAML itself can initiate the full historical research and archive-write job.
- This is a broad research execution and protected-branch archive writer, not a read-only agent task.

## 3. Early-path sequence/follow-through standalone workflow

- Manual dispatch plus push trigger when its own workflow YAML changes on `price-action-v1`.
- Declares `contents: read`; checks out the research branch.
- Compiles anatomy/sequence modules and tests, runs two synthetic suites, checks existence of boundary event, five feature, and five 1-minute market files with `test -f`.
- Executes the five-asset early-path sequence/follow-through study and uploads a 14-day artifact.
- No research-branch archive commit is shown in this workflow. However, read-only permissions do not exempt its script/test execution from the active handoff.
- The source guards do not establish data authenticity or provenance.

## 4. Matched-pair asset robustness V1

- Manual dispatch plus push trigger on changes to its own workflow YAML on `price-action-v1`.
- Declares `contents: write`; checks out the research branch.
- Compiles the asset robustness module and test, runs its synthetic tests, then checks that V4 matched-pairs and early-path follow-through archive CSVs exist using `test -f`.
- Runs asset-level and leave-one-asset-out robustness with 10,000 replicates and seed 20261124.
- Permanently archives generated output under the Phase 3 research archive and pushes to `price-action-v1`; uploads a 14-day secondary artifact.
- The workflow consumes a matched-pair artifact and outcome file from different prior study families. The YAML checks only path existence; it does not visibly bind the two files to the same trusted source commit, study run, or authenticated manifest.
- This is a downstream research execution and protected-branch archive writer. It is prohibited under the active handoff.

## 5. Cross-workflow dependency and trigger risks

1. The anatomy/sequence workflow produces several datasets later consumed by matched-control and asset-robustness workflows. The asset robustness job consumes archived V4 matched pairs and follow-through outcomes; the YAML does not establish a cryptographic or run-level lineage binding between them.
2. The anatomy workflow and asset-robustness workflow both have write permissions and commit archive outputs. Their separate concurrency groups do not provide a global lock across the full Phase 3 study chain.
3. The taxonomy workflow is manual-only but still executes a five-asset historical study. Manual-only is not equivalent to authorized.
4. The early-path workflow is read-token only but still compiles, tests, and executes research code.
5. `test -f` checks in the anatomy and asset-robustness workflows are weaker than `test -s` and do not even establish non-empty inputs. Neither form authenticates content or provenance.
6. A push filter that watches only the workflow YAML can make a workflow edit itself the event that starts historical execution. Workflow-file changes must not be used as an implicit activation mechanism.

## 6. Agent and phase-governance implications

- Do not dispatch or repurpose any of these inherited workflows for agent work while G0-05 prohibits workflow/script/test execution.
- Do not classify a workflow as safe merely because it has `contents: read` or lacks a Git push step.
- Keep all work in the agent branch confined to static documentation and repository metadata until the active handoff is formally changed by the owner.
- Future downstream artifact consumers should verify authenticated source run/workflow identity, repository, exact commit, run attempt, artifact identity and digest, plus schema and cross-file lineage before parsing.
- Separate workflow-local concurrency groups do not replace a single global research-pipeline lock.
- No workflow result, artifact, or archive phrase can independently close G0-05 or authorize Phase 1.

## Evidence limits and non-actions

This is a static review of the four listed workflow YAML files. It does not audit the implementation of referenced research modules/tests, actual artifact contents, prior workflow run logs, effective GitHub permissions, action internals, runner images, package integrity, or data correctness. The YAML declares intended behavior, not proof that a workflow ran or passed.

No workflows, scripts, tests, package installations, research calculations, source-data reads, artifact downloads, reports, protected files, permissions, secrets, VPS/self-hosted runners, or research-branch state were touched. G0-05 remains open. No candidate generation, backtesting, PnL analysis, strategy selection, gate closure, phase advancement, or agent activation was authorized.
