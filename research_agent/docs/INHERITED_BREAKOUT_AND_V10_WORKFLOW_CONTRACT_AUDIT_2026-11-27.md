# Inherited Breakout and V10 Workflow Contract Audit — 2026-11-27

## Scope

Static inspection of selected inherited workflow YAML files on `agent/okx-research-agent-v1`. This is documentation only. No workflow, script, test, package installation, artifact, data operation, or research computation was run. The controlling G0-05 handoff still prohibits all such execution.

## 1. Breakout Lifecycle V1.1 workflow encodes a material archive limitation

File: `.github/workflows/phase3-breakout-lifecycle-v1-1.yml`.

Observed workflow contract:
- Lines 5–13: manual dispatch plus push trigger on `price-action-v1`, watching the V1.1 research script, test, checkpoint amendment, and workflow file.
- Lines 15–16: `contents: write`.
- Lines 27–30: explicitly checks out `price-action-v1`.
- Lines 37–44: installs pinned NumPy/pandas, runs the breakout lifecycle tests, then executes the frozen historical breakout lifecycle script.
- Lines 46–73: asserts a metadata contract including 1,592 primary events, 1,537 primary links, 6,368 horizon rows, 6,368 forward crosscheck rows/passes, 18 fields checked per row, 569,125 common 1m timestamps, zero common 1m gaps, and overlap-cluster conditions.
- Crucially, lines 59–65 assert that `forward_archive_unavailable_lifecycle_fields` is exactly the five retest fields: `outside_retest`, `outside_retest_boundary_crossed`, `outside_retest_minutes`, `outside_retest_depth_pct_of_boundary`, and `outside_retest_hold`.
- Lines 75–81 upload a 90-day artifact.
- Lines 83–90 commit and push generated reports to `price-action-v1`.

Interpretation boundary: the YAML's assertion is a declared expected metadata contract, not proof of the current archive contents or a fresh execution result. It is nevertheless direct static evidence that this workflow expects those five fields to be unavailable in the forward archive. That aligns with the current handoff's descriptive-only status and reinforces that no retest field should be treated as canonical, materialized, or validated by this workflow.

## 2. V10 matched-cohort/covariate workflow family

The following inspected files each declare `workflow_dispatch` and a push trigger on `price-action-v1`, `contents: write`, Ubuntu-hosted execution, checkout of the research branch, Python/dependency setup, tests and/or historical diagnostics, permanent archive writes, and a push back to `price-action-v1`:

- `sideways-matched-covariate-audit-v10.yml`: V10 covariate structure/bottleneck audit; consumes prior anatomy, sequence, V6 pairs, V9 feasibility, feature and minute inputs; writes a V10 archive.
- `sideways-covariate-correlation-v10-1.yml`: V10.1 correlation diagnostic; writes a correlation archive.
- `sideways-covariate-audit-v10-2.yml`: V10.2 redundancy/balance audit; consumes V10.1 correlation and V6 matched pairs; writes a V10.2 archive.
- `sideways-balance-retention-v10-3.yml`: V10.3 balance-retention frontier; research/test execution and permanent archive path.
- `sideways-alternative-matching-v10-4.yml`: V10.4 alternative-matching constraint sensitivity; research/test execution and permanent archive path.
- `sideways-asset-direction-balance-v10-5.yml`: V10.5 asset-direction balance attribution; research/test execution and permanent archive path.
- `sideways-balance-synthesis-v10-6.yml`: V10.6 stable-stratum balance synthesis; research/test execution and permanent archive path.
- `sideways-covariate-persistence-v10-8.yml`: V10.8 imbalance-persistence diagnostic; uses V10.7 output and includes retry/rebase/push logic (up to three push attempts).
- `sideways-distributional-overlap-v10-9.yml`: V10.9 distributional-overlap audit; uses frozen anatomy/sequence/V6 pairs and market/feature inputs; retry/rebase/push archive logic.
- `sideways-joint-support-v10-10.yml`: V10.10 joint common-support retention audit; consumes frozen anatomy/sequence/V6 pairs and market/feature inputs; retry/rebase/push archive logic.
- `sideways-joint-support-percentile-v10-11.yml`: V10.11 joint-support percentile sensitivity; write-capable archive workflow.

These are not isolated read-only diagnostics: the inspected YAMLs explicitly create or update version-controlled archive paths and push the results. Some additionally publish secondary artifacts. Exact per-file path filters and step contracts remain in the workflow source; this summary does not claim every detail is identical.

The V7, V8 and V9 matched-cohort/feasibility workflows were also inspected. Each is manual/push-triggered, declares `contents: write`, checks out `price-action-v1`, executes the respective matching/cohort audit, and has an archive/push step plus artifact publication. They are part of the same unsafe inherited execution family.

## 3. Research archive policy check is a distinct low-write-risk but still executable workflow

File: `.github/workflows/research-archive-policy-check.yml`.

- Push trigger is restricted to `price-action-v1` and archive-policy/Phase 3 archive/workflow paths; manual dispatch is also enabled.
- Declares `contents: read` and uses `ubuntu-latest`.
- Checks out repository contents and runs shell assertions (`test`, `grep`) against the archiving rule and archive directory/README.
- The inspected file does not run a research script or push commits.

This is lower side-effect than the write-capable research workflows, but it is still a workflow execution and remains prohibited by the current handoff. It is not an agent worker workflow.

## 4. Safety conclusions

1. The breakout V1.1 workflow's expected metadata explicitly lists all five retest fields as unavailable in the forward archive. Do not infer canonical field sourceability from this workflow.
2. The V7–V10.11 matched-cohort/covariate family can run from matching pushes to `price-action-v1` and write research archives back to that branch. Keep all of them out of any future agent allowlist.
3. Retry-safe push logic does not make these workflows safe; it can make branch writes more persistent/reliable.
4. A low-write-risk archive-policy check still violates the current no-workflow-execution handoff.
5. These workflows cannot be used to validate G0-05, create canonical candidates, or advance Phase 3 under the current authority state.

## Evidence limits and explicit non-actions

This is a targeted static workflow-source inspection, not an exhaustive audit of every referenced script, dependency, action implementation, runner image, secret, environment, or effective GitHub setting. The metadata assertions above are workflow expectations, not fresh runtime results.

No workflow was executed, dispatched, rerun, cancelled, enabled, or edited. No tests, scripts, packages, research calculations, downloads, artifacts, VPS/self-hosted runners, permissions, secrets, protected research files, or `price-action-v1` state were changed. No G0-05 decision, phase status, candidate status, or agent activation state was changed.
