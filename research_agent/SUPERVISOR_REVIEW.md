# Supervisor Review Gate

The `engine.supervisor_review` module validates one untrusted worker submission
against the exact trusted queue task. It is a review gate, not a worker or
completion authority.

## Submission contract

A worker submission must include the exact task ID, phase, operation, and
SHA-256 digest of the complete trusted task definition. It must provide a
status, summary, findings, evidence references (repository-relative path,
SHA-256, source reference, description), declared actions performed, and
limitations. Unknown fields are rejected. Declared actions must use the small
allowlist of benign read-only/reporting action identifiers; unknown action
labels fail closed as safety violations rather than being trusted as free text.
Repository-relative evidence paths reject traversal, absolute paths, Windows
drive prefixes, and backslashes.

## Review dispositions

- `ready_for_human_review`: structurally valid completed submission with at
  least one declared evidence reference; correctness and evidence bytes remain
  unverified.
- `partial_submission_needs_human_review`: structurally valid partial work.
- `blocked_submission_recorded`: worker reports a blocker and explains
  limitations.
- `return_for_revision`: malformed, incomplete, mismatched, or unsafe
  submission.
- `rejected_safety_violation`: worker declares a prohibited action or claims
  phase-gate closure.

## Authority boundary

Every result has `human_review_required: true`,
`task_completion_approved: false`, and `gate_closure_approved: false`.
The module does not inspect evidence file bytes, verify source truth, execute
work, alter task state, or approve phase advancement. A later trusted review
stage must independently verify artifact contents and provenance before a
human considers the findings.
