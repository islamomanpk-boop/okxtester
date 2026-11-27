# Inherited Research Workflow Push-Trigger and G0-05 Hazard Audit — 2026-11-27

## Scope

Read-only static inspection of four inherited workflow files in `.github/workflows/` on `agent/okx-research-agent-v1`. These workflow files were inherited from the research branch baseline; they are not agent-specific workflow files. No workflow was dispatched, no matching push was made, and no code or research data was executed or modified.

The current authoritative G0-05 handoff prohibits scripts, tests, workflows, and research-code/data changes. That restriction remains controlling.

## Findings

### WF-G0-01 — G0-05 candidate contract workflow has a push trigger

File: `.github/workflows/phase3-g0-05-candidate-contract-tests.yml`

- Triggers: `workflow_dispatch` and `push` to `price-action-v1` when one of these paths changes:
  - `research/phase3_g0_05_candidate_contract_v1.py`
  - `tests/test_phase3_g0_05_candidate_contract_v1.py`
  - this workflow file.
- Explicit permission: `contents: read`.
- Runner: `ubuntu-latest`.
- Checkout: `price-action-v1`, with persisted credentials disabled.
- Steps compile the candidate-contract module/tests and run the corresponding unittest discovery command.

**Risk:** a matching push to `price-action-v1` can run tests without a manual dispatch. Those tests are prohibited by the current handoff. Do not change any matching path or push to the research branch while this restriction is active.

### WF-G0-02 — G0-05 independent minute verification has a push trigger

File: `.github/workflows/phase3-g0-05-independent-minute-verification.yml`

- Triggers: `workflow_dispatch` and `push` to `price-action-v1` when the verifier script or this workflow file changes.
- Explicit permissions: `contents: read`, `actions: read`.
- Runner: `ubuntu-latest`.
- Checks out `price-action-v1` with persisted credentials disabled.
- Uses the GitHub CLI and `github.token` to locate/download a successful source-audit artifact tied to an expected commit SHA.
- Compiles and executes `research/phase3_g0_05_independent_minute_verification_v1.py`.
- Uploads an artifact, including on an `always()` condition, with a 14-day retention setting.

**Risk:** a matching push can launch an executable research-evidence verification and artifact-publication workflow. The `actions: read` permission is still a read capability; the artifact upload is an external publication side effect. The current handoff prohibits this workflow execution.

### WF-G0-03 — G0-05 source audit has a push trigger

File: `.github/workflows/phase3-g0-05-source-audit.yml`

- Triggers: `workflow_dispatch` and `push` to `price-action-v1` when the source-audit script or this workflow file changes.
- Explicit permissions: `contents: read`, `actions: read`.
- Runner: `ubuntu-latest`.
- Checks out `price-action-v1` with persisted credentials disabled.
- Uses `github.token` and GitHub CLI to download a fixed G0-04 artifact.
- Compiles and executes `research/phase3_g0_05_source_manifest_audit_v1.py`.
- Uploads the resulting source-audit evidence artifact, including on an `always()` condition, with a 14-day retention setting.

**Risk:** a matching push can run the G0-05 source audit and publish an artifact without manual dispatch. This is prohibited by the current handoff.

### WF-G0-04 — G0-04 causal reconstruction has a push trigger

File: `.github/workflows/phase3-g0-04-causal-breakout-reconstruction.yml`

- Triggers: `workflow_dispatch` and `push` to `price-action-v1` when the reconstruction script or this workflow file changes.
- Explicit permission: `contents: read`.
- Runner: `ubuntu-latest`.
- Checks out `price-action-v1` with persisted credentials disabled.
- Installs pinned NumPy and pandas versions.
- Compiles the reconstruction module, runs its self-test, executes the descriptive reconstruction, and uploads an artifact with a 14-day retention setting.

**Risk:** a matching push can install dependencies, execute self-tests and a research reconstruction, and publish artifacts. Do not use this workflow as an alternate validation path; the active handoff prohibits execution.

## Cross-cutting observations

1. All four workflows are scoped to pushes on `price-action-v1`, not pushes to the isolated agent branch. A documentation-only commit confined to `research_agent/` on `agent/okx-research-agent-v1` does not match these declared push filters.
2. The workflow YAML files are inherited repository workflows, not the proposed `okx-research-agent` workflow. Their presence does not mean the agent is active.
3. The workflows explicitly declare read-oriented GitHub token permissions, but compilation, script execution, artifact download/upload, and external package installation remain real actions. “Read-only repository permission” does not mean “no execution” or “no external side effects.”
4. `if: always()` on artifact upload means a failed preceding step can still reach the artifact-upload step; the output path may be empty or partial. This is not evidence that the artifact is valid.
5. Action references use version tags (`actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4`), not immutable full commit SHAs.
6. The repository branches were reported unprotected and the rulesets endpoint returned an empty list in the companion governance audit. Thus there is no observed GitHub branch-protection control preventing an accidental matching push.

## Required handling while G0-05 is open

- Do not dispatch, rerun, or otherwise invoke any of these workflows.
- Do not push changes to `price-action-v1`.
- Do not modify the listed watched paths on `price-action-v1`.
- Continue any permitted documentation work only on `agent/okx-research-agent-v1` and under `research_agent/`.
- Before any future validation, obtain an explicit handoff update that permits the exact operation, and separately verify the workflow trigger and target commit. A general statement that “testing is allowed” is insufficient if the specific workflow still performs prohibited reconstruction or publication.
- If the owner later approves a change to workflow triggers, review it as a separate security/governance change. Do not silently remove or alter inherited triggers under this audit.

## Explicit non-actions

No workflow was run, dispatched, rerun, cancelled, enabled, or edited. No matching push was made. No tests, scripts, notebooks, research pipelines, dependency installation, artifact download, or artifact upload occurred. No research code, tests, data, manifests, or protected branch were changed. No G0-05 closure, candidate generation, backtest, PnL conclusion, strategy selection, or phase advancement occurred.

This audit is documentation only. It does not authorize workflow execution or override the active G0-05 handoff.
