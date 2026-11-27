# Orchestration Batch-Cap Visibility Audit — 2026-11-27

## Scope

Static inspection of:

- `research_agent/engine/batch_planner.py`
- `research_agent/engine/orchestration_coordinator.py`
- `research_agent/engine/assignment_package.py`
- `research_agent/BATCH_PLANNER.md`
- `research_agent/ORCHESTRATION_COORDINATOR.md`

No tests, scripts, workflows, queue mutations, research data, or runtime operations were performed. The active Phase 3 G0-05 handoff remains controlling.

## Finding ORCH-01 — eligible tasks beyond the batch cap are not enumerated

**Observed code behavior**

In `build_batch_plan()`, the planner constructs the full `ready` list for the earliest queued phase. It then assigns only `ready[:max_tasks]` to `planned_tasks`. If `len(ready) > max_tasks`, it sets `stop_reason` to `"Batch bounded by max_tasks."` and breaks. The remaining eligible task IDs are not added to `deferred_tasks`, and the returned plan has no explicit overflow count or continuation cursor.

The coordinator builds assignment packages only for `plan["planned_tasks"]` and `plan["deferred_tasks"]`. Consequently, eligible tasks beyond the cap are also absent from the coordinator's package list.

**Classification**

This is a bounded-plan visibility/completeness limitation, not an authorization bypass or execution vulnerability. The output does state that the batch was capped, so the truncation is not entirely silent; however, it does not identify which eligible tasks were left out or make their disposition machine-readable.

**Current impact**

The checked-in queue has only a small number of Phase 3 queued tasks, and the default cap is five. This static finding does not establish that the current queue actually overflows the cap. It is a generic behavior when a future or test queue contains more eligible tasks than `max_tasks`.

**Recommended correction before scaling**

Keep the selected batch unchanged, but add an explicit deterministic representation such as:

- `remaining_eligible_tasks` with the exact unselected task IDs and task-definition digests; or
- `eligible_overflow_count` plus a stable continuation cursor bound to the exact queue snapshot and phase.

The coordinator should either preserve this overflow representation or explicitly state that its snapshot is partial. Any continuation must re-load and revalidate the live queue, handoff, allowlist and phase gate; it must not treat an earlier preflight as durable authorization.

Do not mark these tasks as denied or deferred for policy reasons: they passed preflight but were not selected due solely to the batch limit.

## Other integration boundaries confirmed

- `build_runtime_batch_plan()` loads the fixed-path queue once and derives the per-task preflight summary from that same in-memory snapshot.
- `build_orchestration_snapshot()` is an explicit-input composition/test seam; the runtime entry point does not accept caller-supplied queue/preflight inputs.
- The coordinator calculates assignment-package digests but returns `package_digest_stored: false`; no independent trusted digest custody is implemented.
- Recovery observations are caller-supplied and explicitly marked unauthenticated.
- Assignment packages remain non-dispatchable; assignment-return review requires an independently retained expected package digest and does not prove dispatch or delivery.
- Evidence verification compares bytes against a caller-supplied manifest and file map; it does not authenticate those inputs.
- Review-artifact creation is in-memory, records status `not_run`, and preserves human-only task and phase-gate authority.

These are existing documented boundaries, not newly discovered operational capabilities.

## Status and non-actions

This is a source-level static finding only. No tests were executed to reproduce the overflow case. No code change is proposed or made under the current handoff. No worker was dispatched; no task or research script was executed; no workflow, artifact upload, queue mutation, candidate generation, backtest, PnL analysis, strategy selection, G0-05 closure, or phase advancement occurred.

G0-05 remains open. Phase order remains Phase 3, Phase 1, Phase 2, Phase 4, Phase 5.
