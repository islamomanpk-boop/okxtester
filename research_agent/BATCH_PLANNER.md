# Bounded Batch Planner

The `engine.batch_planner` module creates a deterministic, bounded work plan
from the trusted task queue and a complete, non-authorizing per-task preflight
summary.

## Behavior

- Enforces the canonical phase sequence: Phase 3, Phase 1, Phase 2, Phase 4,
  Phase 5.
- Stops at the earliest phase containing queued work if no task in that phase
  passes exact single-task preflight. It never skips ahead to a later phase.
- Carries each selected task's exact handoff ID, scope, prohibited-action list, and canonical task-definition digest into the assignment so a future worker receives the complete task boundary.
- Selects only task IDs whose preflight result is explicitly
  `ALLOW_READ_ONLY`, matches the exact task ID, has the expected preflight-only
  shape, and asserts that no execution occurred.
- Caps each proposed batch at 10 tasks (default 5).
- Reports denied queued tasks separately with their reason.
- Leaves blocked later-phase tasks untouched.
- Returns `PLAN_ONLY`, `authorized: false`, and
  `execution_performed: false` unconditionally.

## Non-capabilities

The planner does not execute assignments, call Copilot, create task definitions,
change queue status, write files, upload artifacts, schedule work, authorize a
queue, close gates, or advance phases. A proposed assignment is not completion
evidence. The worker must independently re-check the live handoff and exact
task authorization immediately before any future permitted operation.

Under the current G0-05 lock, Phase 3 tasks are expected to be denied, so the
planner should return an empty batch and stop at Phase 3. This is intentional:
it protects the phase sequence instead of using Phase 1 work as a shortcut.
