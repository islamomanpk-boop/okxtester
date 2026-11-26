# Assignment Review Artifact Handoff

`engine/review_artifact.py` connects the exact assignment-bound return review to
the existing deterministic report and artifact builder.

## Flow
1. Bind the package to the exact trusted queue task and digest.
2. Run structural supervisor review.
3. Verify evidence declarations against caller-supplied commit manifest and bytes.
4. Project worker declarations, review disposition, evidence-integrity outcomes,
   blockers, and limitations into the existing strict report schema.
5. Use `report_builder.build_artifact_bundle()` to verify task and checkout
   provenance and construct the three-file bundle in memory.

## Safety boundaries
- Malformed worker values that cannot be represented as strict JSON, including excessively nested values, are rendered as a bounded type marker in the audit report, so malformed declarations remain reviewable instead of crashing report construction.
- Report status is always `not_run`: this reporting layer did not execute the
  research task. Worker status/findings are explicitly labelled declarations.
- Evidence integrity means only that supplied bytes match the supplied manifest.
  The caller/workflow must independently authenticate checkout, exact commit,
  cleanliness, manifest origin, run identifiers, and timestamp.
- Assignment binding requires an expected package SHA-256 retained independently by a trusted dispatcher/channel; a worker-returned digest is not trusted.
- Assignment binding does not prove worker dispatch or delivery.
- A passing review is only eligible for human review. Completion and gate closure
  remain human-only.
- No execution, dispatch, queue mutation, filesystem writes, uploads, workflow
  calls, research-code/data changes, candidates, backtests, PnL analysis,
  strategy selection, or gate closure occurs here.
- This module does not override the active Phase 3 G0-05 handoff.

## Inputs and output
The caller supplies the exact task/package/submission, the independently retained expected assignment-package SHA-256, evidence manifest and
bytes, workflow metadata, and report input manifest. The module restricts
repository and branch, and requires report commit to equal evidence-review
commit. Output includes the supervisor review and an in-memory bundle containing
`report.json`, `report.md`, and `artifact_manifest.json`. No files are
written or uploaded.
