# Master Inherited Workflow Inventory and Execution-Risk Map — 2026-11-27

## Purpose and authority

This document consolidates the static reviews of the inherited `.github/workflows/` directory on `agent/okx-research-agent-v1`. The directory listing returned 39 YAML workflow files.

The controlling Phase 3 G0-05 handoff remains authoritative. This inventory is not an activation plan and does not authorize execution. No workflow, script, test, market-data job, VPS job, artifact operation, or research-branch write was performed.

## 1. Complete 39-file inventory

### A. Phase 3 lifecycle, G0-04/G0-05 and completion (8)

1. `phase3-rejection-lifecycle-v1.yml`
2. `phase3-rejection-lifecycle-v1-1.yml`
3. `phase3-breakout-lifecycle-v1-1.yml`
4. `phase3-completion-validation.yml`
5. `phase3-g0-04-causal-breakout-reconstruction.yml`
6. `phase3-g0-05-source-audit.yml`
7. `phase3-g0-05-independent-minute-verification.yml`
8. `phase3-g0-05-candidate-contract-tests.yml`

These include historical research execution, test execution, artifact download/consumption, completion-string/archive checks, and in some cases permanent research-branch archive writes. The G0-05 handoff explicitly prohibits dispatching these workflows, including read-only jobs.

### B. Funding and Phase 1 (4)

9. `funding-engine-contract-tests.yml`
10. `phase3-funding-coverage-audit.yml`
11. `phase3-funding-mark-price-full-audit.yml`
12. `phase1-uptrend-source-preflight.yml`

The funding-engine workflow compiles and runs broad funding/execution/portfolio/mark-price test suites. The funding coverage workflow runs tests. The full mark-price audit creates and pushes a candidate-proxy snapshot. The Phase 1 preflight runs tests and a five-asset input audit, then permanently archives/pushes reports. Phase 1 remains blocked by the agreed sequence until Phase 3 is complete and authorized.

### C. Sideways historical research and taxonomy (7)

13. `sideways-boundary-interaction-taxonomy-v1.yml`
14. `sideways-rejection-episode-retest-anatomy-v1.yml`
15. `sideways-rejection-early-path-sequence-followthrough-v1.yml`
16. `sideways-rejection-v1-full-study.yml`
17. `sideways-rejection-v1-tests.yml`
18. `sideways-pre-event-matched-controls-v3.yml`
19. `sideways-pre-event-matched-controls-v4.yml`

These run taxonomy, five-asset anatomy/follow-through, bootstrap, matched-control and robustness research, or their tests. Several write generated results permanently to `price-action-v1`; others upload short-retention artifacts. File-existence checks are not provenance or integrity checks.

### D. Matched cohort and V10 sensitivity pipeline (18; includes matched-asset robustness)

21. `sideways-matched-cohort-audit-v7.yml`
22. `sideways-matched-cohort-audit-v8.yml`
23. `sideways-matched-feasibility-audit-v9.yml`
24. `sideways-covariate-correlation-v10-1.yml`
25. `sideways-covariate-audit-v10-2.yml`
26. `sideways-balance-retention-v10-3.yml`
27. `sideways-alternative-matching-v10-4.yml`
28. `sideways-asset-direction-balance-v10-5.yml`
29. `sideways-balance-synthesis-v10-6.yml`
30. `sideways-minimum-sample-sensitivity-v10-7.yml`
31. `sideways-covariate-persistence-v10-8.yml`
32. `sideways-distributional-overlap-v10-9.yml`
33. `sideways-matched-covariate-audit-v10.yml`
34. `sideways-joint-support-v10-10.yml`
35. `sideways-joint-support-percentile-v10-11.yml`
36. `sideways-pre-event-matched-controls-v5.yml`
37. `sideways-pre-event-matched-controls-v6.yml`
38. `sideways-matched-asset-robustness-v1.yml`

This family includes matched-cohort feasibility, covariate balance, matching constraints, support/overlap, subgroup and sensitivity diagnostics. The dependency graph is documented in the detailed V3–V6, V7–V9 and V10 audits. Workflow-local concurrency does not provide a single global lock for the complete chain. Several jobs push generated archives. Input checks such as `test -f` or `test -s` alone do not authenticate provenance, schema, or cross-file lineage.

### E. VPS operations (1)

39. `vps-health-monitor.yml`

Manual-only self-hosted Linux x64 workflow. It collects host/kernel/resource information, downloader process command lines, a tail of a downloader log, and SQLite file names/sizes, then writes these into the GitHub Actions step summary. It is not the cloud research agent and must not be used as a proxy for agent health. No VPS or runner was inspected.

### F. Archive policy (1)

40. `research-archive-policy-check.yml`

Shell-level presence and keyword checks. It is not a provenance, schema, cryptographic-integrity, source-correctness, or gate-authorization verifier.

**Unique total:** 8 + 4 + 7 + 18 + 1 + 1 = 39 workflow files. The matched-asset robustness workflow is grouped only in section D.

## 2. Directory-level trigger and permission observations

Prior static inventory recorded:

- 39 workflow YAML files.
- 38 declare `workflow_dispatch`.
- 35 declare a push trigger.
- Four are manual-only and one is push-only.
- 26 contain at least one explicit write permission among contents, Actions, pull requests, or issues; 13 do not.

These are YAML-level observations, not proof of effective token permissions or actual run history. Organization/repository defaults, event context, reusable-workflow caller grants, and GitHub policy may affect effective permissions. A read-only permission block does not make code execution permissible under the current handoff.

## 3. Cross-cutting risk register

| Risk | Static observation | Required future control |
|---|---|---|
| Accidental execution | Many inherited workflows have push triggers, sometimes watching their own YAML file | No inherited dispatch; separately reviewed agent-only entrypoint |
| Protected-branch mutation | Multiple workflows declare contents write and commit/push reports or datasets | Separate artifact-only agent branch; explicit review for any research-branch write |
| Phase-order bypass | Phase 1 preflight exists as a runnable workflow | Phase gate enforced independently; no Phase 1 until Phase 3 owner-authorized closeout |
| G0-05 bypass | G0-05 workflows exist and can run audits/tests | Active handoff remains hard lock across every route |
| Untrusted artifact lineage | Some workflows select/download artifacts by run IDs, names, or hard-coded head SHA | Verify repository, workflow identity, exact commit, run attempt, artifact identity/digest and schema |
| Weak input guards | `test -f` / `test -s` establish only existence/non-empty bytes | Strict schema, content digest, source identity, completeness and cross-file lineage |
| Dependency drift | Many workflows use mutable action tags and/or runtime package installation without lock hashes | Immutable action SHA pins, hash-locked dependencies, reviewed build provenance |
| Pipeline races | Concurrency groups are often workflow-specific | One protected global pipeline lock and transactional state transitions |
| Public output exposure | Logs, artifacts, summaries and annotations may contain research or infrastructure details | Data classification, redaction, least-privilege access, retention and privacy review |
| VPS coupling | One workflow requires self-hosted VPS runner | Exclude VPS/self-hosted infrastructure from the cloud-agent execution boundary |

## 4. Agent-specific activation decision

No inherited workflow is an acceptable activation mechanism for `okx-research-agent`. The current branch's workflow inventory is inherited research automation, not an agent controller. No agent-specific workflow has been installed or activated.

The previously documented activation alternatives remain:

- Separate repository with its own default branch and a directly dispatchable, narrowly scoped workflow; or
- Same repository with an explicitly approved manual-only caller on `main` and a reusable callee on the agent branch, pinned to an immutable full commit SHA, with exact same-SHA checkout and caller-bounded permissions.

Neither alternative is authorized or implemented. The existing G0-05 handoff blocks even preparatory workflow execution. Any future workflow design must be reviewed as one caller/callee security boundary, including immutable code identity, permissions, inputs, artifact provenance, secret handling and branch isolation.

## 5. Audit index

Detailed supporting documents:

- `INHERITED_V10_1_TO_V10_11_AND_MANUAL_REJECTION_WORKFLOW_AUDIT_2026-11-27.md`
- `INHERITED_MATCHED_COHORT_V7_V9_AND_V10_DOWNSTREAM_DEPENDENCY_AUDIT_2026-11-27.md`
- `INHERITED_MATCHED_CONTROL_AND_MANUAL_STUDY_WORKFLOW_AUDIT_2026-11-27.md`
- `INHERITED_PHASE3_LIFECYCLE_AND_G0_04_G0_05_WORKFLOW_BOUNDARY_AUDIT_2026-11-27.md`
- `INHERITED_FUNDING_PHASE1_VPS_AND_ARCHIVE_WORKFLOW_BOUNDARY_AUDIT_2026-11-27.md`
- `INHERITED_SIDEWAYS_TAXONOMY_ANATOMY_SEQUENCE_AND_ASSET_ROBUSTNESS_WORKFLOW_AUDIT_2026-11-27.md`

## 6. Evidence limits and non-actions

The directory count is based on a GitHub contents listing for `.github/workflows/` at the audited branch. Trigger and permission counts are based on prior static YAML inspection. This document does not independently re-open and re-parse every YAML file, resolve every action implementation, inspect every referenced script/test, establish effective permissions, or prove any workflow has executed successfully.

No workflow, script, test, package installation, research calculation, data download, artifact download, VPS operation, permission/secret change, or research-branch mutation was performed. All conclusions are static and bounded. G0-05 remains open; no candidate generation, backtesting, PnL analysis, strategy selection, phase advancement, gate closure, or agent activation is authorized.
