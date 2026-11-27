# Orchestration Coordinator

The `engine.orchestration_coordinator` module composes the existing queue
preflight, bounded phase planner, assignment package builder, package digest,
and optional recovery classifier into one deterministic in-memory snapshot.

## Runtime entry point

`build_runtime_orchestration_snapshot()` loads the queue once from the fixed
repository path, derives every per-task preflight result from that same queue
snapshot, and passes both to the pure coordinator. It does not accept caller-
supplied queue or preflight data.

`build_orchestration_snapshot()` is the explicit-input composition/test seam.
It delegates phase ordering and eligibility to the batch planner, then builds
packages only for selected tasks and denied queued tasks in the earliest
eligible phase. Selected packages remain `prepared_not_dispatched`; denied
packages remain `blocked_preflight`.

Each package digest is returned with `package_digest_stored: false`. The
coordinator does not claim an independent trusted channel exists. A future
dispatcher must retain the expected digest independently before delivery and
must verify the live handoff and permissions again at the operation boundary.

Optional recovery observations are caller declarations. The coordinator
validates their shape and returns conservative recovery guidance, but marks
their source unauthenticated. Uncertain delivery never triggers automatic
retry.

## Non-capabilities

The coordinator performs no task execution, dispatch, GitHub operation,
filesystem write, persistence, scheduling, queue mutation, workflow trigger,
research-data/code change, candidate generation, backtest, PnL analysis,
strategy selection, or gate closure. All output is snapshot-only and requires
human review. It cannot override the active Phase 3 G0-05 handoff.

Under the current G0-05 lock, the runtime snapshot is expected to stop at
Phase 3, contain no planned assignments, and package queued Phase 3 tasks as
blocked. It must not skip ahead to Phase 1.

## Snapshot completeness limitation

The coordinator packages selected tasks and denied tasks returned by the planner. If the planner has more eligible tasks than the batch cap, eligible overflow tasks are not represented in the package list. The plan's stop reason notes the cap, but does not identify the omitted task IDs. Treat such a snapshot as a bounded partial batch, not a complete inventory of all eligible tasks. See [the static audit](docs/ORCHESTRATION_BATCH_CAP_VISIBILITY_AUDIT_2026-11-27.md).
