"""Bounded phase-ordered batch planner; never executes or authorizes work."""
from __future__ import annotations

from typing import Any

from .report_builder import task_definition_digest
from .task_runner import load_queue, preflight_all_tasks

MAX_BATCH_SIZE = 10
EXPECTED_PHASE_ORDER = [
    "phase3_sideways_range",
    "phase1_uptrend_bullish",
    "phase2_downtrend_bearish",
    "phase4_choppy_high_volatility",
    "phase5_transition_expansion",
]


def build_runtime_batch_plan(*, max_tasks: int = 5) -> dict[str, Any]:
    """Build a plan only from the repository's fixed runtime queue and preflight.

    Unlike the pure planning/test seam below, this entry point accepts no
    caller-supplied queue or preflight summary. It remains non-authorizing.
    """
    if type(max_tasks) is not int or not 1 <= max_tasks <= MAX_BATCH_SIZE:
        raise ValueError(f"max_tasks must be an integer from 1 to {MAX_BATCH_SIZE}.")
    trusted_queue = load_queue()
    trusted_preflight = preflight_all_tasks()
    return build_batch_plan(
        max_tasks=max_tasks,
        queue=trusted_queue,
        preflight_summary=trusted_preflight,
    )


def build_batch_plan(
    *,
    max_tasks: int = 5,
    queue: dict[str, Any] | None = None,
    preflight_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a reviewable work plan from trusted queue and preflight results.

    This is planning only. It does not grant permission, change queue state,
    run tasks, or infer that a queued task is safe. A task enters the proposed
    batch only when its exact preflight result is ALLOW_READ_ONLY. Blocked and
    denied tasks are reported separately. Processing stops at the first phase
    with no eligible work; later phases are never pulled forward.
    """
    if type(max_tasks) is not int or not 1 <= max_tasks <= MAX_BATCH_SIZE:
        raise ValueError(f"max_tasks must be an integer from 1 to {MAX_BATCH_SIZE}.")

    if queue is None:
        queue = load_queue()
    if not isinstance(queue, dict) or not isinstance(queue.get("tasks"), list):
        raise ValueError("Trusted task queue is malformed.")
    tasks = queue["tasks"]
    if not all(isinstance(task, dict) for task in tasks):
        raise ValueError("Every task queue entry must be an object.")

    policy = queue.get("queue_policy")
    if not isinstance(policy, dict):
        raise ValueError("Queue policy is missing.")
    phase_order = policy.get("phase_order")
    if phase_order != EXPECTED_PHASE_ORDER:
        raise ValueError("Queue phase order does not match the approved project sequence.")
    if policy.get("no_phase_skipping") is not True:
        raise ValueError("Queue must explicitly prohibit phase skipping.")

    ids = [task.get("task_id") for task in tasks]
    if any(not isinstance(value, str) or not value.strip() for value in ids):
        raise ValueError("Every task must have a non-empty task ID.")
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate task IDs are not permitted.")

    if preflight_summary is None:
        preflight_summary = preflight_all_tasks()
    if not isinstance(preflight_summary, dict):
        raise ValueError("Preflight summary is malformed.")
    if (
        preflight_summary.get("mode") != "queue_preflight_only"
        or preflight_summary.get("execution_performed") is not False
        or preflight_summary.get("authorized") is not False
        or preflight_summary.get("decision") != "SUMMARY_ONLY"
        or not isinstance(preflight_summary.get("tasks"), list)
    ):
        raise ValueError("Only a non-authorizing queue preflight summary is accepted.")

    preflight_rows = preflight_summary["tasks"]
    if not all(isinstance(row, dict) for row in preflight_rows):
        raise ValueError("Preflight rows are malformed.")
    preflight_ids = [row.get("task_id") for row in preflight_rows]
    if len(preflight_ids) != len(set(preflight_ids)) or set(preflight_ids) != set(ids):
        raise ValueError("Preflight results must match every trusted queue task exactly once.")
    preflight_by_id = {row["task_id"]: row for row in preflight_rows}

    plan: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    selected_phase: str | None = None
    stop_reason = "No task is currently eligible for a worker."

    for phase in phase_order:
        phase_tasks = [task for task in tasks if task.get("phase") == phase]
        if not phase_tasks:
            continue
        queued = [task for task in phase_tasks if task.get("status") == "queued"]
        if not queued:
            continue

        ready = []
        for task in queued:
            result = preflight_by_id[task["task_id"]]
            allowed = (
                result.get("authorized") is True
                and result.get("decision") == "ALLOW_READ_ONLY"
                and result.get("execution_performed") is False
                and result.get("mode") == "preflight_only"
                and result.get("task_id") == task["task_id"]
                and isinstance(result.get("reason"), str)
                and bool(result["reason"].strip())
            )
            if allowed:
                ready.append({
                    "task_id": task["task_id"],
                    "phase": phase,
                    "operation": task.get("operation"),
                    "title": task.get("title"),
                    "handoff_id": task.get("handoff_id"),
                    "scope": list(task.get("scope", [])),
                    "prohibited": list(task.get("prohibited", [])),
                    "task_definition_sha256": task_definition_digest(task),
                    "assignment_status": "preflight_allowed_not_executed",
                    "completion_authority": "human_only",
                })
            else:
                deferred.append({
                    "task_id": task["task_id"],
                    "phase": phase,
                    "assignment_status": "blocked_pending_authorization",
                    "reason": result.get("reason", "Missing or inconsistent preflight result."),
                })

        if ready:
            selected_phase = phase
            plan = ready[:max_tasks]
            stop_reason = (
                "Batch bounded by max_tasks."
                if len(ready) > max_tasks
                else "Selected only tasks explicitly allowed by exact single-task preflight."
            )
            break

        # Do not search a later phase when the earliest phase containing
        # queued work has no preflight-approved task.
        stop_reason = "Stopped at the earliest queued phase because no task passed preflight."
        break

    return {
        "mode": "batch_plan_only",
        "decision": "PLAN_ONLY",
        "authorized": False,
        "execution_performed": False,
        "queue_state_changed": False,
        "phase": selected_phase,
        "max_tasks": max_tasks,
        "planned_task_count": len(plan),
        "planned_tasks": plan,
        "deferred_tasks": deferred,
        "stop_reason": stop_reason,
        "limitations": [
            "Planning is not task execution or task authorization.",
            "Preflight approval is not research completion or human gate approval.",
            "A human must review the plan and applicable handoff before any worker runs.",
            "No task status, queue file, research file, or artifact is written.",
        ],
    }
