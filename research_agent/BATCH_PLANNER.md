# Bounded Batch Planner

The `engine.batch_planner` module creates a deterministic, bounded work plan
from the trusted task queue and a complete, non-authorizing per-task preflight
summary. The future runtime must call `build_runtime_batch_plan()`: this entry
point accepts only a batch-size limit and loads both queue and preflight data
from their fixed repository runtime sources. `build_batch_plan()` remains a
pure planning/test seam that accepts explicit inputs and must not be treated as
a trusted dispatch boundary.

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
- Runtime planning loads the trusted queue once and derives every per-task preflight result from that same in-memory snapshot, avoiding a queue reload between planning and preflight. The lower-level planner uses the same rule when it must obtain its own preflight summary.
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

## Batch-cap visibility limitation

When more tasks pass preflight in the earliest queued phase than fit within `max_tasks`, the current implementation selects the first `max_tasks` entries and reports that the batch was capped. It does not enumerate the remaining eligible task IDs in `planned_tasks` or `deferred_tasks`, and it does not return an overflow count or continuation cursor. The current queue does not establish that this limit is reached, but future larger queues need an explicit overflow representation before relying on the plan as a complete inventory. See [the static audit](docs/ORCHESTRATION_BATCH_CAP_VISIBILITY_AUDIT_2026-11-27.md).
