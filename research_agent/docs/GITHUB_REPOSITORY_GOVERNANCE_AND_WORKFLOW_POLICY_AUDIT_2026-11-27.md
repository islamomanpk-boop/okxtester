# GitHub Repository Governance and Workflow Policy Audit — 2026-11-27

## Scope and method

Read-only inspection of GitHub repository metadata, branch metadata, repository rulesets, default-branch workflow files, and Actions run metadata. No settings, secrets, workflows, branch refs, or repository files were changed during the inspection. No workflow was dispatched and no project code was executed.

Repository: `islamomanpk-boop/okxtester`.

## Confirmed repository and branch facts

- Repository visibility is **public**.
- Default branch is `main`.
- The repository metadata endpoint reports the linked account has administrative access; this is metadata, not evidence of configured governance controls.
- GitHub branch metadata reports `protected: false` for each of:
  - `main`
  - `price-action-v1`
  - `agent/okx-research-agent-v1`
- The branch metadata for `main` and `price-action-v1` reports protection disabled and required status-check enforcement off.
- The repository rulesets endpoint returned an empty list (`[]`).

**Finding GOV-01 — No branch-level protection was observed.** The three relevant branches are reported unprotected, and no repository rulesets were returned. Therefore the current repository state does not demonstrate enforced pull-request review, required status checks, or branch update restrictions. Do not assume that review or CI gates protect these branches.

## Default-branch workflow inventory

The current `main` tree contains six workflow files under `.github/workflows/`. Static inspection of all six found the same high-level pattern:

- Trigger: `workflow_dispatch` only.
- Explicit workflow permission: `contents: read`.
- Runner: `ubuntu-latest`.
- Checkout target: `price-action-v1`.
- Referenced actions use version tags such as `actions/checkout@v4`, `actions/setup-python@v5`, and, where artifacts are uploaded, `actions/upload-artifact@v4`; these are not immutable full commit-SHA pins.

The six default-branch files are:

1. `phase3-g0-04-causal-breakout-reconstruction.yml`
2. `phase3-overnight-research.yml`
3. `sideways-rejection-early-path-sequence-followthrough-v1.yml`
4. `sideways-rejection-episode-retest-anatomy-v1.yml`
5. `sideways-rejection-v1-full-study.yml`
6. `sideways-rejection-v1-tests.yml`

This inventory is specifically the current default-branch directory, not a complete inventory of workflow files on every branch. The `price-action-v1` branch contains additional inherited research workflows and is subject to its own workflow-trigger risks. The six default-branch files are not the `okx-research-agent` workflow and do not implement its task queue, assignment package, supervisor review, or branch-isolated execution.

**Finding GOV-02 — Action references are mutable tags.** The default-branch workflows inspected do not pin third-party actions to immutable full commit SHAs. Before any future agent workflow is activated, every action and reusable workflow reference should be reviewed and pinned to a verified full SHA, with update governance documented.

**Finding GOV-03 — Default-branch manual workflows still execute research-branch code.** Although the six default-branch workflow files are manual-dispatch-only and declare `contents: read`, they check out `price-action-v1` and execute research tasks. Their existence is not agent activation and they must not be dispatched while the controlling G0-05 handoff prohibits workflow/script execution.

## Workflow run-history check against the G0-05 handoff

The controlling G0-05 issue/handoff was in place by 2026-11-26 17:13 UTC. A read-only Actions run query filtered to runs created after that timestamp returned **zero runs** at the time of this audit. The most recent G0-05 runs visible in the recent run listing were push-triggered runs from 2026-11-26 around 11:03–11:32 UTC, before the handoff timestamp.

This is a bounded API observation, not proof that no execution could occur outside GitHub Actions or that no later run can occur. Continue checking before any future authorization decision.

## Settings that remain UNKNOWN

The available read-only GitHub fetch connection rejected the repository Actions-permissions endpoints as unsupported. Therefore the following were **not verified**:

- Repository/org Actions allowlist and policy restrictions.
- Default `GITHUB_TOKEN` permission setting and fork pull-request workflow policy.
- Whether approval is required for outside collaborators or first-time contributors.
- Environment protection rules and deployment reviewers.
- Artifact/log retention settings and any organization-level overrides.
- Whether secrets are available to any particular workflow/environment (secrets were not inspected).
- Self-hosted runner registration, runner-group policy, or repository access controls.

A failed or unsupported read endpoint is not evidence that a setting is absent or permissive. These items remain UNKNOWN pending owner-side settings inspection.

## Activation and governance consequences

1. **Do not activate the agent yet.** The G0-05 handoff remains controlling; no workflow dispatch, test, script, task execution, or workaround is authorized.
2. **Do not use the public repository for confidential reports or worker returns.** Workflow logs, summaries, artifacts, and metadata must be treated as public outputs unless a separate private storage boundary is proven.
3. Before any future activation, establish and independently verify branch protection/rulesets for `main`, `price-action-v1`, and the agent branch. At minimum, evaluate required pull-request review, required status checks, stale-review dismissal, restricted force-push/deletion, and narrowly scoped bypass actors.
4. Inspect Actions settings and environment policies through the GitHub owner UI or an authorized administration connection. Record actual values and effective scope; do not infer them from workflow YAML.
5. Pin actions and reusable workflows to immutable full commit SHAs, review permissions and checkout identities, and validate the complete caller/callee boundary before any run.
6. Keep the agent's future workflow manual-only and report/preflight-only until the G0-05 handoff permits the relevant operation and the separate activation gates are met.

## Explicit non-actions

- No repository settings, branch protection, rulesets, secrets, environments, permissions, retention, runners, or workflow files were changed.
- No workflow was dispatched, rerun, cancelled, or enabled.
- No scripts, tests, notebooks, research pipelines, or project commands were executed.
- No research data, candidate generation, backtests, PnL analysis, strategy selection, gate closure, or phase advancement occurred.
- This audit is documentation only and does not grant activation authority or override the controlling handoff.
