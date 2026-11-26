# Worker Assignment Package

`engine.assignment_package.prepare_worker_assignment` builds a structured,
task-bound handoff for a worker without dispatching that worker.

## Inputs and binding

- The exact trusted task object from `config/task_queue.json`.
- Its exact single-task preflight result.
- For an `ALLOW_READ_ONLY` result, the matching assignment entry produced by
  `engine.batch_planner`.

The builder recomputes the task-definition SHA-256 digest and compares the
planned task ID, phase, operation, title, handoff ID, scope, prohibited-action
list, digest, assignment status, and human-only completion authority against
the trusted task. Unknown preflight fields, non-`queued` queue status, and inconsistent decisions fail
closed. This prevents completed, blocked, or otherwise ineligible tasks from being
repackaged as new worker assignments.

A denied preflight can produce a blocked audit handoff. An allowed preflight
can produce a prepared package only when the planner entry matches exactly.

## Package contents

The package carries the full trusted task, scope, prohibited actions, handoff
identifier, task digest, permitted worker-declared read-only/reporting actions,
and the required supervisor submission/evidence fields.

## Authority boundary

Every output has `dispatch_permitted: false`,
`execution_performed: false`, `task_completion_approved: false`, and
`gate_closure_approved: false`. It cannot change the task queue, create an
allowlist approval, execute commands, contact GitHub, or override the live
research handoff. Even a synthetic or future `ALLOW_READ_ONLY` preflight does
not activate dispatch. A human must separately review and authorize any
future activation, and the worker must re-check the live handoff.

Under the active G0-05 restriction, the expected result is a
`blocked_preflight` package, not an executable assignment.

Regression tests are authored but not executed because the current handoff
prohibits the relevant test execution.
