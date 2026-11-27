# Inherited Workflow Fleet Risk and Cross-Phase Trigger Audit — 2026-11-27

## Purpose and scope

This documentation-only continuation consolidates a targeted static sample of the 39 workflow files under .github/workflows/ on agent/okx-research-agent-v1. It focuses on push-triggered research execution, branch writes, artifact publication, and cross-phase hazards.

The earlier repository-wide static census recorded 39 workflow files, 38 with workflow_dispatch, 35 with push, four manual-only, and one push-only. It also recorded 26 files with at least one explicit write permission among the inspected GitHub token permission keys. These are inventory-level static counts, not proof of effective permissions or a complete per-step security audit.

No workflow was run, dispatched, rerun, cancelled, enabled, or edited. No matching push was made. No test, script, package installation, data download, research computation, artifact upload/download, or branch write occurred.

The controlling Phase 3 G0-05 handoff remains open and authoritative. It prohibits running scripts, tests, or workflows and prohibits research-code/data changes, candidate generation, backtesting, PnL conclusions, strategy selection, and G0-05 closure. These findings do not grant permission to execute anything.

## 1. Repeated write-capable Phase 3 matching workflow family

The following sampled workflows each statically show a push trigger scoped to price-action-v1, contents: write, research/test execution, and a commit/push step back to price-action-v1. They are not passive checks and must not be treated as safe agent runners.

| Workflow | Observed behavior |
|---|---|
| sideways-pre-event-matched-controls-v3.yml | Compiles/tests and runs V3 matching audit; commits and pushes archive output. |
| sideways-pre-event-matched-controls-v4.yml | Compiles/tests and runs V4 matching audit; commits and pushes archive output. |
| sideways-pre-event-matched-controls-v5.yml | Compiles/tests and runs V5 matching audit; commits and pushes archive output. |
| sideways-pre-event-matched-controls-v6.yml | Compiles/tests and runs V6 matching audit; commits and pushes archive output. |
| sideways-matched-cohort-audit-v7.yml | Compiles/tests and runs V7 cohort audit; commits and pushes archive output. |
| sideways-matched-cohort-audit-v8.yml | Compiles/tests and runs V8 cohort audit; commits and pushes archive output. |
| sideways-matched-feasibility-audit-v9.yml | Compiles/tests and runs V9 feasibility audit; commits and pushes archive output. |
| sideways-covariate-correlation-v10-1.yml | Compiles/tests and runs V10.1 correlation diagnostic; commits and pushes archive output. |
| sideways-covariate-audit-v10-2.yml | Compiles/tests and runs V10.2 covariate/balance audit; commits and pushes archive output. |
| sideways-balance-retention-v10-3.yml | Compiles/tests and runs V10.3 balance-retention audit; commits and pushes archive output. |
| sideways-alternative-matching-v10-4.yml | Compiles/tests and runs V10.4 alternative matching sensitivity; commits and pushes archive output. |
| sideways-asset-direction-balance-v10-5.yml | Compiles/tests and runs V10.5 asset-direction attribution; commits and pushes archive output. |
| sideways-balance-synthesis-v10-6.yml | Compiles/tests and runs V10.6 balance synthesis; commits and pushes archive output. |
| sideways-minimum-sample-sensitivity-v10-7.yml | Compiles/tests and runs V10.7 subgroup-size sensitivity; commits and pushes archive output. |
| sideways-covariate-persistence-v10-8.yml | Compiles/tests and runs V10.8 persistence audit; commits and pushes archive output. |
| sideways-distributional-overlap-v10-9.yml | Compiles/tests and runs V10.9 distributional overlap audit; commits and pushes archive output. |
| sideways-joint-support-v10-10.yml | Compiles/tests and runs V10.10 joint-support audit; commits and pushes archive output. |
| sideways-joint-support-percentile-v10-11.yml | Compiles/tests and runs V10.11 percentile sensitivity; commits and pushes archive output. |
| sideways-matched-asset-robustness-v1.yml | Compiles/tests and runs matched-asset robustness audit; commits and pushes archive output. |

This sample demonstrates a repeated pattern, not that every workflow has identical path filters, dependency pins, outputs, or failure handling. Exact watched paths and complete step behavior must be checked before any future governance change.

### Why the pattern matters

- A documentation or code push to a watched path on price-action-v1 can cause research computation without a separate manual dispatch.
- These workflows have repository write permission and an explicit research-branch push, so their output is not isolated to an artifact.
- A push-triggered run may be initiated by an ordinary branch update; a human need not click the manual dispatch button.
- An artifact upload after failure is not evidence that the research computation or assertions passed.
- Agent task labels, queue state, and branch isolation under research_agent/ do not disable inherited workflows. Their own trigger filters and GitHub Actions policy govern them.

## 2. Other observed cross-phase write path

### Phase 1 source preflight

File: .github/workflows/phase1-uptrend-source-preflight.yml

Static inspection found:
- workflow_dispatch and push trigger restricted to price-action-v1 and selected Phase 1 paths (lines 2–6).
- contents: write and ubuntu-latest (lines 10–17).
- Compiles the Phase 1 preflight and test files, runs the test suite, and executes the preflight script (lines 28–32).
- Commits and pushes the generated archive to price-action-v1 (lines 44–47).
- Uploads an artifact (line 53).

This is a future-phase workflow, not authorization to begin Phase 1. The agreed sequence requires Phase 3 to be fully completed first, then Phase 1, and the current G0-05 handoff still prohibits workflow execution. Do not invoke this workflow as a way to progress the phase order.

## 3. G0-05-specific workflows remain prohibited

The three inherited G0-05 workflows previously inspected are particularly sensitive:
- phase3-g0-05-candidate-contract-tests.yml: push/manual triggers; compiles and executes candidate-contract tests.
- phase3-g0-05-independent-minute-verification.yml: push/manual triggers; reads a prior Actions artifact, runs the independent minute verifier, and uploads an artifact.
- phase3-g0-05-source-audit.yml: push/manual triggers; downloads a fixed G0-04 artifact, executes source-audit code, and uploads an artifact.

The G0-04 causal reconstruction workflow is also push/manual triggered and runs the reconstruction/self-test before uploading output. These are all prohibited by the current handoff even when their workflow permission block is read-only.

## 4. Other workflow patterns observed in the sample

- phase3-rejection-lifecycle-v1.yml and phase3-rejection-lifecycle-v1-1.yml: matching push/manual workflows with contents: write; run tests and lifecycle research scripts, upload artifacts, and push report outputs.
- sideways-rejection-episode-retest-anatomy-v1.yml: matching push/manual workflow with contents: write; runs multiple tests and research scripts, uploads multiple artifacts, and pushes outputs.
- phase3-funding-mark-price-full-audit.yml: matching push/manual workflow with contents: write; runs helper tests and full-window funding/mark-price research, then pushes a clearly labelled candidate-proxy snapshot and manifest.
- sideways-rejection-early-path-sequence-followthrough-v1.yml: read-only permission in the inspected file, but runs tests and a historical research script and uploads an artifact.
- sideways-boundary-interaction-taxonomy-v1.yml: read-only permission in the inspected file, but runs compilation, tests, and a historical research script and uploads an artifact.
- phase3-completion-validation.yml: read-only permission; validates archived Phase 3 files and compares archived sensitivity outputs. Still prohibited workflow execution.
- phase3-funding-coverage-audit.yml and funding-engine-contract-tests.yml: read-only permission; compile and execute test suites. Still prohibited test execution.
- sideways-rejection-v1-full-study.yml and sideways-rejection-v1-tests.yml: manual-only workflows in the prior static sample; manual-only does not override the handoff prohibition.
- vps-health-monitor.yml: self-hosted runner workflow; outside the agent's allowed execution surface and must not be invoked.

This list is descriptive, not exhaustive. A complete audit would require reviewing every workflow's entire YAML, referenced scripts/actions, all branch/path filters, token permissions, runner configuration, secrets/environment access, and effective repository/organization settings.

## 5. Agent isolation implications

1. The proposed agent must never reuse or dispatch inherited research workflows as a worker execution mechanism.
2. The agent's future workflow must be distinct, with a separately reviewed security boundary, exact immutable checkout SHA, explicit least-privilege permissions, no inherited research-branch write, and public-output classification.
3. Documentation-only changes under research_agent/ on agent/okx-research-agent-v1 do not match the sampled push filters that specify price-action-v1. This is a bounded static conclusion about inspected filters, not a universal guarantee against all triggers.
4. The agent branch's existence does not make it safe to merge, push, or dispatch against price-action-v1.
5. Repository and organization Actions settings unavailable through the read connection remain UNKNOWN. Do not assume permissive or restrictive values.
6. Sampled action references use version tags (for example actions/checkout@v4, actions/setup-python@v5, actions/upload-artifact@v4) rather than immutable full commit SHAs. This is a future supply-chain hardening requirement, not permission to modify existing workflows now.
7. Because the repository is public, logs, annotations, step summaries, artifacts, and failure output must be treated as public outputs.

## 6. Required controls and stop conditions

- Keep all inherited research workflows out of the agent's dispatch allowlist.
- Do not dispatch, rerun, enable, or edit these workflows while the active handoff prohibits workflow execution.
- Do not push to price-action-v1, modify watched research files, or change inherited workflow YAML.
- Do not use Phase 1 workflow execution to bypass the agreed Phase 3-first order.
- Do not treat read-only token permission as evidence that running the workflow is authorized.
- Do not interpret artifact existence, upload success, or a workflow's green status as approval to close a research gate.
- Any future workflow activation or settings change requires a separate explicit owner decision and a complete security review; it cannot override the current research handoff.

## Explicit non-actions

No workflow was executed, dispatched, rerun, cancelled, enabled, or modified. No tests, scripts, data retrieval, package installation, research computations, artifact operations, or branch writes occurred. No VPS or self-hosted runner was accessed. No research code, tests, data, reports, manifests, workflow files, protected branch state, permissions, or secrets were changed.

This is a static documentation audit only. It does not activate the agent, authorize Phase 1, close G0-05, or advance any phase.
