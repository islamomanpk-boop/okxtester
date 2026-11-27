# Inherited Phase 3 Lifecycle and G0-04/G0-05 Workflow Boundary Audit — 2026-11-27

## Scope and authority

Static inspection of eight workflow YAML files on `agent/okx-research-agent-v1`:

- `.github/workflows/phase3-rejection-lifecycle-v1.yml`
- `.github/workflows/phase3-rejection-lifecycle-v1-1.yml`
- `.github/workflows/phase3-breakout-lifecycle-v1-1.yml`
- `.github/workflows/phase3-completion-validation.yml`
- `.github/workflows/phase3-g0-04-causal-breakout-reconstruction.yml`
- `.github/workflows/phase3-g0-05-source-audit.yml`
- `.github/workflows/phase3-g0-05-independent-minute-verification.yml`
- `.github/workflows/phase3-g0-05-candidate-contract-tests.yml`

The active G0-05 handoff remains authoritative. This review did not dispatch, run, rerun, cancel, or modify any workflow. No script, test, research data, report, or market input was executed or read by a workflow during this review. The findings below describe YAML declarations, not evidence of actual run outcomes.

## 1. Rejection lifecycle V1 and V1.1

Both workflows declare manual dispatch and push triggers on `price-action-v1`, with path filters covering their research module, tests, checkpoint document, and workflow YAML. Both grant `contents: write`, checkout `price-action-v1`, run synthetic tests, execute a historical lifecycle script, validate fixed output metadata, upload a 90-day artifact, and commit/push generated reports back to the research branch.

The V1.1 result contract additionally asserts overlap-cluster metadata and a fixed episode-row count. These assertions are runtime checks only if the workflow is executed; static inspection does not verify the underlying report or values.

**Boundary:** these are research-execution and protected-branch archive writers, not read-only evidence-inspection workers. Their push triggers mean a matching research-branch change can initiate the job without a manual dispatch.

## 2. Breakout lifecycle V1.1

This workflow also declares manual and matching push triggers, grants `contents: write`, checks out the research branch, installs exact NumPy/pandas versions, runs tests and a historical breakout lifecycle script, validates a metadata contract, uploads a 90-day artifact, and commits/pushes the output archive.

The YAML's metadata assertions include 1,592 primary events, 1,537 primary links, 6,368 horizon rows, 6,368 passing forward cross-check rows, 18 checked fields per row, 569,125 common 1m timestamps, zero common 1m gaps, and an explicit list of five retest lifecycle fields reported unavailable in the forward archive. These are asserted expected values and labels in workflow code; they are not newly verified empirical findings in this audit.

**Boundary:** this workflow is a historical research execution and archive writer. It is not authorized under the current G0-05 no-execution handoff.

## 3. Phase 3 completion archive validation

This workflow declares manual and matching push triggers, `contents: read`, and checks out `price-action-v1`. It checks required archive paths for non-empty files, runs an inline Python comparison between V10.10 and V10.11 central-90 outputs, and uses `grep` to check two closeout-record phrases.

Important distinctions:

- `test -s` proves only that a path exists and has non-zero size. It does not authenticate provenance, establish schema correctness generally, or prove the files correspond to a trusted commit.
- The inline comparison checks selected count columns for matching keys and checks metadata flags/row counts. It is a bounded archive consistency assertion, not a complete research correctness review or a G0-05 authorization.
- The final text checks establish presence of exact phrases, not that all phase gates have been validly satisfied.
- Although the token is read-only, the workflow still executes code and checks while the active handoff prohibits workflow execution.

**Boundary:** read-only permission does not make this workflow permissible during the current no-workflow-execution period. Its name or phrase checks must not be interpreted as independent authority to close a phase gate.

## 4. G0-04 causal reconstruction

The G0-04 workflow declares manual and matching push triggers, `contents: read`, and checks out `price-action-v1` with persisted credentials disabled. It installs pinned NumPy/pandas versions, compiles the reconstruction module, runs its self-test, executes the descriptive reconstruction, and uploads a 14-day artifact (including an upload attempt under `if: always()`).

This is a read-token workflow but it performs script compilation, synthetic self-test, and historical reconstruction. It is prohibited by the current G0-05 handoff, which expressly bars workflow/script/test execution. The YAML does not commit its output back to the research branch.

## 5. G0-05 source-audit artifact dependency

The source-audit workflow declares manual and matching push triggers, `contents: read` and `actions: read`, and checks out the research branch with persisted credentials disabled. It downloads a specifically named G0-04 artifact using a hard-coded run ID, compiles the source-audit module, runs the provenance/identity audit, and uploads a 14-day artifact.

Static concern: the artifact dependency is pinned by a numeric workflow run ID and expected artifact name, but the shown workflow does not itself visibly compare the downloaded artifact's originating run metadata, head SHA, workflow identity, or artifact digest to an independently trusted expected tuple before invoking the audit. Whether the script performs additional checks must be established by a separate source review; this YAML alone does not prove those bindings.

## 6. G0-05 independent exact-minute verification dependency

This workflow declares manual and matching push triggers, `contents: read` and `actions: read`, and checks out the research branch with persisted credentials disabled. It lists up to 20 successful source-audit runs on `price-action-v1`, selects the first whose `headSha` equals a hard-coded commit SHA, downloads an artifact named using that run ID, compiles the independent verifier, runs exact-minute verification, and uploads a 14-day artifact.

Static observations and limitations:

- The run selection is constrained by a hard-coded expected commit SHA and success conclusion, but only the latest 20 matching workflow runs are considered.
- The shell/Python selection shown chooses the first matching row returned by the GitHub CLI; the YAML does not state an explicit ordering guarantee or independently verify uniqueness of matching successful runs.
- The workflow does not visibly verify the downloaded artifact's cryptographic digest, originating workflow identity, or full provenance tuple before using it. A separate verifier-source review would be needed to determine any further checks.
- A missing matching run causes the explicit non-empty run-ID guard to fail closed rather than selecting an arbitrary run.
- The hard-coded expected SHA creates a maintenance-sensitive coupling: a legitimate source-audit rerun at another commit will not satisfy this selector until the expected SHA is intentionally updated and reviewed.

These are static contract observations, not proof that an artifact was incorrectly selected or that a verification result is wrong.

## 7. G0-05 candidate contract tests

This workflow declares manual and matching push triggers, `contents: read`, and checks out the research branch with persisted credentials disabled. It compiles the candidate-contract module and test file, then executes the focused unittest suite. The comment says canonical market data is not loaded, but the workflow still runs tests and therefore remains prohibited under the active handoff.

## 8. Consolidated classification

| Workflow | Trigger | Declared token permissions | Executes scripts/tests | Writes research branch |
|---|---|---|---|---|
| Rejection lifecycle V1/V1.1 | Manual + matching push | contents: write | Yes, tests + historical lifecycle | Yes |
| Breakout lifecycle V1.1 | Manual + matching push | contents: write | Yes, tests + historical lifecycle | Yes |
| Completion validation | Manual + matching push | contents: read | Yes, inline Python + shell checks | No in YAML |
| G0-04 reconstruction | Manual + matching push | contents: read | Yes, compile + self-test + reconstruction | No in YAML |
| G0-05 source audit | Manual + matching push | contents: read, actions: read | Yes, compile + source audit | No in YAML |
| G0-05 independent minute verification | Manual + matching push | contents: read, actions: read | Yes, compile + independent verifier | No in YAML |
| G0-05 candidate contract tests | Manual + matching push | contents: read | Yes, compile + tests | No in YAML |

All seven are prohibited from execution under the current handoff. The write-capable lifecycle workflows additionally have explicit research-branch archive-push behavior. Read-only token scope is not an exemption from a no-execution instruction.

## 9. Implications for the future agent boundary

1. Do not dispatch or reuse any inherited workflow as an agent worker while G0-05 remains open.
2. Do not treat `contents: read`, `persist-credentials: false`, synthetic-only comments, or an audit-oriented workflow name as proof that execution is authorized.
3. A future artifact consumer must bind artifact bytes to an independently trusted workflow run, repository, workflow identity, exact head commit, run attempt, artifact name, and digest; a filename or run ID alone is not sufficient provenance.
4. Where a downstream job selects an upstream run, it should reject ambiguous matches, verify the complete run/attempt/head identity, and verify the downloaded artifact against a trusted digest before parsing it.
5. A successful workflow or phrase-based closeout check cannot grant human gate closure, alter the current handoff, or authorize phase advancement.

## Evidence limits and non-actions

This is a static review of the listed workflow YAML only. It does not audit the full implementation of referenced research modules, test suites, artifact contents, GitHub CLI behavior, effective organization/repository permissions, action internals, runner images, dependency resolution, or actual historical run logs. Assertions and comments in YAML are declarations, not verified outcomes.

No workflows, scripts, tests, package installs, research calculations, artifact downloads, report generation, market-data reads, pushes, permission changes, or VPS/self-hosted runner operations were performed. No protected research files or branch state were changed. G0-05 remains open; no candidate generation, backtesting, PnL analysis, strategy selection, gate closure, phase advancement, or agent activation was authorized.
