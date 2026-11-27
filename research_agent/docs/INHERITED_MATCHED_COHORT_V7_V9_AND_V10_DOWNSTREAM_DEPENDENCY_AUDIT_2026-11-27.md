# Inherited Matched-Cohort V7–V9 and V10 Downstream Dependency Audit — 2026-11-27

## Scope and method

Static inspection of these workflow definitions on `agent/okx-research-agent-v1`:

- `.github/workflows/sideways-matched-cohort-audit-v7.yml`
- `.github/workflows/sideways-matched-cohort-audit-v8.yml`
- `.github/workflows/sideways-matched-feasibility-audit-v9.yml`
- `.github/workflows/sideways-minimum-sample-sensitivity-v10-7.yml`
- `.github/workflows/sideways-covariate-persistence-v10-8.yml`
- `.github/workflows/sideways-distributional-overlap-v10-9.yml`
- `.github/workflows/sideways-joint-support-v10-10.yml`
- `.github/workflows/sideways-joint-support-percentile-v10-11.yml`

No workflow, script, or test was run. No artifacts or research datasets were read. No files outside `research_agent/` were changed.

## Findings

### 1. V7, V8 and V9 are push-triggered, write-capable research workflows

Each declares both manual `workflow_dispatch` and a `push` trigger on `price-action-v1`, filtered to its own workflow, research module and test file. Each declares `contents: write`, checks out `price-action-v1`, installs NumPy/pandas/SciPy, compiles and runs a version-specific test suite, executes the corresponding historical audit, archives output under `reports/sideways_phase3_research_archive_v1/`, pushes a bot-authored commit to `price-action-v1` when output changes, and uploads a 14-day secondary artifact.

Their declared roles are:
- V7: matched-cohort quality/dependence audit, using the V6 optimal matched-pairs archive plus episode anatomy, early-path sequence, five asset feature files and five 1-minute market files.
- V8: matched-cohort common-support audit, using the same V6 and frozen Phase 3 inputs.
- V9: matching-feasibility audit, using V6 pairs, the frozen Phase 3 inputs and an additional V5 research module during compilation.

The V7/V8/V9 workflow definitions use `test -f` for the listed frozen inputs. That proves only path existence at runtime, not nonempty content, expected schema, file digest, immutable source commit, or semantic correctness. This is a code-contract observation, not evidence that any file is missing or malformed.

### 2. Downstream V10.7–V10.8 form a chained dependency

V10.7 is also manual-plus-push, declares `contents: write`, runs tests and subgroup-size sensitivity, and archives/pushes its output. It checks that two upstream V10.5/V10.6 CSVs are nonempty (`test -s`).

V10.8 consumes the V10.7 detail CSV, runs the persistence diagnostic, and archives/pushes its result. It checks the input with `test -s`.

This creates an explicit V10.5 → V10.6/V10.7 → V10.8 evidence dependency. The workflow definitions establish intended file-path dependencies only; they do not by themselves establish that the artifacts are complete, authentic, generated from the intended commit, or methodologically valid.

### 3. V10.9–V10.11 require the V6 matched-pairs archive

V10.9, V10.10 and V10.11 each declare manual-plus-push triggers, `contents: write`, a version-specific test run, historical analysis, permanent archive commits to `price-action-v1`, and a 14-day secondary artifact.

Each requires the episode anatomy archive, early-path sequence archive, V6 optimal matched-pairs CSV, five detector feature files and five 1-minute market CSVs. V10.10 and V10.11 use `test -s` for these inputs; V7–V9 use `test -f`. Nonempty checks are stronger than existence-only checks but still do not authenticate or validate the contents.

The three versions consume the same named V6 matched-pairs archive, but their analyses differ:
- V10.9: empirical distributional overlap.
- V10.10: joint common-support retention.
- V10.11: joint-support percentile sensitivity.

### 4. Shared workflow supply-chain and write-boundary risks

Across these eight workflows:
- Push triggers mean matching path changes on `price-action-v1` may launch code/test execution without a manual dispatch.
- Explicit `contents: write` plus Git add/commit/push steps create an automated write path to the research branch.
- Action references are mutable major-version tags (for example, checkout/setup-python/upload-artifact tags), not immutable full commit SHA pins.
- Dependencies are installed during the run; these YAMLs do not show a hash-locked dependency file or package-hash verification.
- Versioned archive paths and Git commits improve persistence, but do not alone prove source-data identity, complete input lineage, independent reproducibility, or research validity.
- Concurrency groups are per workflow; they do not establish one global lock across the whole V7–V10 chain. V10.7–V10.11 retry push/rebase; retries address Git transport conflicts, not stale or semantically incompatible upstream research inputs.

### 5. Difference between file presence and evidence provenance

The input guards illustrate three different assurance levels:
1. `test -f`: path exists.
2. `test -s`: path exists and has nonzero size.
3. A trusted provenance verifier: recomputes bytes against a manifest bound to an independently verified source commit and checks the expected schema/lineage.

The inspected workflows implement levels 1 or 2 for several frozen files; these checks must not be described as level 3. No conclusion is made about the research scripts' internal validations because this review is limited to workflow YAML.

## Binding G0-05 disposition

The active Phase 3 G0-05 handoff remains authoritative. Do not dispatch these workflows, push matching watched paths on `price-action-v1`, run scripts/tests, use Actions as an alternate execution route, or treat their potential outputs as permission to close G0-05. The workflow audit is static documentation only and does not change the phase sequence or gate status.

## Evidence limits

This document describes declared YAML triggers, permissions, commands, path guards, archive operations, and artifact retention. It does not claim any workflow ran, any output exists, any tests passed, any repository/org permission setting is effective, or any research result is valid. No runtime, Actions logs, artifacts, data rows, or code-level research methods were inspected in this audit.
