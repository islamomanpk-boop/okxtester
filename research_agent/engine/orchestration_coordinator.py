"""Pure coordinator for phase-ordered, non-dispatching agent orchestration.

This module composes trusted queue/preflight inputs, batch planning, assignment
packaging, and recovery guidance. It has no filesystem, network, GitHub,
dispatch, persistence, scheduling, or task-execution side effects.
"""
from __future__ import annotations

from typing import Any

from .assignment_package import assignment_package_digest, prepare_worker_assignment
from .batch_planner import build_batch_plan
from .recovery_policy import classify_assignment_recovery
from .task_runner import _preflight_all_tasks_with_queue, load_queue


def build_orchestration_snapshot(
    *,
    queue: dict[str, Any],
    preflight_summary: dict[str, Any],
    max_tasks: int = 5,
    recovery_observations: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compose one exact queue snapshot into reviewable assignment packages.

    Recovery observations are untrusted caller declarations. They are only
    classified; this function does not authenticate or persist them.
    """
    plan = build_batch_plan(
        max_tasks=max_tasks,
        queue=queue,
        preflight_summary=preflight_summary,
    )
    tasks = queue["tasks"]
    task_by_id = {task["task_id"]: task for task in tasks}
    preflight_by_id = {
        row["task_id"]: row for row in preflight_summary["tasks"]
    }

    selected_by_id = {
        row["task_id"]: row for row in plan["planned_tasks"]
    }
    deferred_by_id = {
        row["task_id"]: row for row in plan["deferred_tasks"]
    }
    assignment_packages: list[dict[str, Any]] = []

    # Selected work is packaged but remains explicitly undispatched.
    for task_id, planned in selected_by_id.items():
        package = prepare_worker_assignment(
            task_by_id[task_id],
            preflight_by_id[task_id],
            planned_assignment=planned,
        )
        assignment_packages.append({
            "task_id": task_id,
            "package": package,
            "package_sha256": assignment_package_digest(package),
            "package_digest_stored": False,
        })

    # Denied queued work receives a blocked audit package, never a dispatch.
    for task_id in deferred_by_id:
        task = task_by_id[task_id]
        package = prepare_worker_assignment(task, preflight_by_id[task_id])
        assignment_packages.append({
            "task_id": task_id,
            "package": package,
            "package_sha256": assignment_package_digest(package),
            "package_digest_stored": False,
        })

    recovery: dict[str, dict[str, Any]] = {}
    if recovery_observations is not None:
        if not isinstance(recovery_observations, dict):
            raise TypeError("Recovery observations must be an object keyed by task ID.")
        for task_id, observation in recovery_observations.items():
            if task_id not in task_by_id or not isinstance(observation, dict):
                raise ValueError("Recovery observation must reference a known task and object.")
            if set(observation) != {"delivery_state", "review_state", "human_disposition"}:
                raise ValueError("Recovery observation has missing or unsupported fields.")
            recovery[task_id] = {
                **classify_assignment_recovery(
                    delivery_state=observation["delivery_state"],
                    review_state=observation["review_state"],
                    human_disposition=observation["human_disposition"],
                ),
                "observation_source_authenticated": False,
            }

    return {
        "schema_version": 1,
        "mode": "orchestration_snapshot_only",
        "decision": "SNAPSHOT_ONLY",
        "phase": plan["phase"],
        "queue_task_count": len(tasks),
        "planned_task_count": plan["planned_task_count"],
        "assignment_package_count": len(assignment_packages),
        "plan": plan,
        "assignment_packages": assignment_packages,
        "recovery_guidance": recovery,
        "dispatch_permitted": False,
        "execution_performed": False,
        "queue_state_changed": False,
        "persistence_performed": False,
        "scheduling_enabled": False,
        "human_gate_required": True,
        "task_completion_approved": False,
        "phase_gate_closure_approved": False,
        "limitations": [
            "This is an in-memory orchestration snapshot, not an execution or dispatch.",
            "Package digests are calculated but not stored in an independent trusted channel.",
            "Caller-supplied recovery observations are not authenticated.",
            "A future dispatcher must independently re-check the live handoff, exact task digest, allowlist, phase gate, and current permissions at the operation boundary.",
            "Only a human may approve task completion or close a phase gate.",
        ],
    }


def build_runtime_orchestration_snapshot(*, max_tasks: int = 5) -> dict[str, Any]:
    """Load one fixed-path queue snapshot and derive preflight from that snapshot."""
    trusted_queue = load_queue()
    preflight = _preflight_all_tasks_with_queue(trusted_queue)
    return build_orchestration_snapshot(
        queue=trusted_queue,
        preflight_summary=preflight,
        max_tasks=max_tasks,
    )
