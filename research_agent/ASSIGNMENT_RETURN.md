# Assignment-Bound Return Review

`engine.assignment_return.review_assignment_return` binds a returned worker
submission to the exact trusted task and prepared assignment package before
calling the existing structural and evidence-integrity review pipeline.

## Checks

- Requires the expected SHA-256 digest of the exact prepared package, retained independently by a trusted dispatcher or handoff channel. The digest must not come from the worker return. This protects all package fields, including the dynamic preflight reason, against alteration. The fingerprint uses strict canonical JSON validation and rejects non-string object keys, tuples, non-finite numbers, and Python-only values.

- Requires a `prepared_not_dispatched` package with no dispatch, execution,
  task-completion, or gate-closure authority.
- Recomputes the trusted task-definition digest.
- Compares task ID, phase, operation, handoff ID, full task object, scope,
  prohibited-action list, and human-only completion authority.
- Requires the exact allowed preflight shape.
- Rejects blocked packages and altered package fields before submission review.
- Passes a valid binding to the existing supervisor/evidence review pipeline.

## Important limits

The result records that the submission matches a prepared package. It does
not prove that a worker was dispatched, received the package, or performed
the declared work. Commit context, manifest and evidence bytes remain
caller-supplied and require independent workflow verification. Even a clean
review is only ready for human review; task completion and phase-gate closure
are never approved by this module.

No worker is launched, no files are read or written, no GitHub/network calls
are made, and no task queue or allowlist is changed. Runtime tests remain
unexecuted under the active G0-05 handoff.


The return reviewer now rebuilds and compares the complete canonical package using strict JSON serialization, including worker action instructions, submission schema, metadata, and authority flags. This prevents altered instructions from being accepted as the original assignment and rejects Boolean schema versions masquerading as integer version 1.
