# GitHub-First Research Operating Protocol V1

Date: 2026-11-24
Project: OKX Price Action V1
Primary research branch: `price-action-v1`
Status: Active working protocol

## 1. Purpose

This protocol defines how research, code changes, execution, verification, and preservation are carried out for the OKX Price Action V1 project.

The default operating model is GitHub-first. Termux remains available for tasks that require local files, local Git operations, credentials, or execution outside GitHub Actions.

This protocol supplements the frozen research specifications. It does not replace or modify them.

## 2. Research phase order

Complete the phases in this order:

1. Phase 3 — Sideways / Range
2. Phase 1 — Uptrend / Bullish
3. Phase 2 — Downtrend / Bearish
4. Phase 4 — Choppy / High Volatility
5. Phase 5 — Transition / Expansion

Finish and document the current phase before moving to the next. Do not jump to strategy selection before the required regime research is complete.

## 3. GitHub-first responsibilities

Use the connected GitHub repository as the primary workspace whenever the available tools support the task.

Preferred GitHub work includes:

- Inspecting repository files, branches, commits, and existing research.
- Reviewing source code, tests, specifications, logs, and reports.
- Creating new scripts, tests, documentation, and workflow files.
- Making narrowly scoped edits while preserving prior versions and evidence.
- Reviewing commit history and checking exact changed-file lists.
- Inspecting GitHub Actions logs and downloading generated artifacts.
- Auditing generated reports against frozen specifications and previously committed outputs.

Use the existing project branch `price-action-v1` for active research unless a task explicitly requires another branch.

Do not assume a GitHub write succeeded until its returned commit is confirmed and the resulting file is fetched and checked.

## 4. GitHub Actions execution

Use GitHub Actions as the preferred execution environment for repeatable research and tests when:

- Required code and data are committed to the repository.
- Dependencies can be installed within the workflow.
- Runtime, memory, storage, and artifact limits are appropriate.
- The workflow can run without private credentials or unsafe permissions.

Prefer manually triggered workflows for research runs. Workflows should use least-privilege permissions, normally `contents: read`, and should not automatically commit generated results unless a separately approved process requires it.

Write generated output to a fresh temporary directory or a new versioned output directory. Never overwrite a non-empty historical report directory. Preserve prior run logs, failed-run evidence, specifications, and reports.

The assistant may prepare and verify workflow files directly in GitHub. If the available GitHub connection cannot dispatch a workflow, the user must start it through the GitHub Actions interface. Do not claim a workflow was started until GitHub confirms the dispatch.

A green workflow status is not, by itself, research validation. Inspect:

- The exact branch and commit checked out.
- Syntax and unit-test results.
- Dataset presence, schema, row counts, and integrity checks.
- The full study command and its exit status.
- Generated artifact names, sizes, and contents.
- Event counts, duplicate checks, missing data, censoring, and reconciliation against frozen specifications.
- Reproducibility against prior reports where appropriate.

Treat execution success, data validation, and research interpretation as separate conclusions.

## 5. When Termux is still required

Use Termux only when the task materially requires local access or a capability unavailable through the connected GitHub tools, including:

- Uploading large local files or datasets that are not yet in GitHub.
- Local Git fetch, merge, push, authentication, or synchronization.
- Inspecting or processing files that exist only on the user's phone.
- Running experiments that exceed GitHub Actions limits or require local-only resources.
- Troubleshooting a workflow or environment that cannot be diagnosed from GitHub logs and artifacts.

Do not ask the user to run Termux commands merely to inspect a file, read a report, review a commit, or perform work that can be completed directly through GitHub.

When Termux is needed, give one safe, copy-paste-ready step at a time and wait for the result before proceeding. Avoid requiring manual code editing on the phone.

## 6. Git and preservation safety

- Never use `git add .` or broad staging commands.
- Stage only explicitly named files.
- Inspect `git status`, staged file names, and staged diffs before committing.
- Never delete, reset, clean, stash, or overwrite unrelated or untracked user files.
- Do not force-push or rewrite shared research history.
- Before a local push, fetch the remote and inspect branch divergence. Merge or otherwise reconcile safely; do not discard either side's commits.
- When GitHub commits directly to a branch while a local clone exists, expect the local clone to become behind and synchronize it before its next push.
- Preserve original specifications, implementations, tests, provenance, raw data, failed-run logs, and earlier reports. Corrections should be additive and clearly versioned.
- Do not claim a commit, push, execution, or verification occurred unless the relevant tool or user-provided output confirms it.

## 7. Data and repository safety

The repository is public. Treat every committed file as publicly accessible.

Never upload API keys, passwords, access tokens, private account data, or other secrets. Review data contents and provenance before committing new datasets.

Keep large datasets in their established paths and avoid duplicating them unnecessarily. Do not change ignore rules broadly just to add a specific approved data file; if necessary, force-add only the exact approved paths.

## 8. Research integrity

- Follow the frozen specification for each study.
- Preserve causal timing, timestamp, missing-data, and censoring rules.
- Do not bridge missing intervals unless the frozen specification explicitly permits it.
- Distinguish candle-level observations from independent episodes.
- Do not convert descriptive findings into predictive, causal, profitability, or strategy claims without a separate study designed to test those claims.
- Reconcile outputs independently; do not rely solely on a successful process exit or a green Actions badge.
- Record limitations and incomplete observations explicitly.
- Do not change a frozen specification silently. Propose a separately versioned amendment or follow-up study.

## 9. Communication and execution style

The assistant leads the technical workflow and explains decisions in plain language.

- Prefer direct GitHub inspection and execution over asking the user to copy commands.
- Give the user one operational step at a time when their action is required.
- Use copy-paste-ready Termux commands only when local work is necessary.
- Clearly distinguish what was inspected, edited, committed, executed, and independently verified.
- Ask for user action only when required by permissions, workflow dispatch, local files, or another genuine limitation.
- Preserve project continuity and do not ask the user to repeat information already available in the repository or conversation context.

## 10. Current execution baseline

As of 2026-11-24:

- Five one-minute datasets (BTC, ETH, SOL, DOGE, AVAX) are committed under `data/market_1m/` on `price-action-v1`.
- The historical sideways rejection forward-outcome study has 1,992 event rows: 1,154 broad and 838 strict.
- The manual full-study GitHub Actions workflow is available at `.github/workflows/sideways-rejection-v1-full-study.yml`.
- A successful run has produced three reports: `event_level_outcomes.csv`, `aggregate_summary.csv`, and `data_validation.csv`.
- The run's three generated reports were checked against the corresponding committed reports and matched exactly.
- Ten 24-hour event outcomes are censored for insufficient future data (8 broad, 2 strict); these remain incomplete observations, not failures to be silently filled.
- The current research phase remains Phase 3 — Sideways / Range. Complete its remaining research and documentation before proceeding to Phase 1.

This baseline is a dated checkpoint, not a replacement for newer verified repository state.

---

End of protocol.
