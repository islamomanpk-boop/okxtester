"""Non-dispatching worker assignment package builder.

This module packages a trusted task and its preflight outcome for review. It
never dispatches a worker, authorizes execution, changes queue state, or
overrides an active research handoff.
"""
from __future__ import annotations

from typing import Any
import hashlib
import json

from .report_builder import task_definition_digest

_ALLOWED_ACTIONS = [
    "read_existing_documentation",
    "inspect_repository_metadata",
    "compare_documented_values",
    "trace_source_references",
    "hash_evidence_file",
    "prepare_report",
]
_PREFLIGHT_FIELDS = {
    "task_id", "queue_status", "decision", "authorized", "reason",
    "execution_performed", "mode",
}
def assignment_package_digest(package: dict[str, Any]) -> str:
    """Hash a canonical package; caller must retain this digest in a trusted channel."""
    if not isinstance(package, dict):
        raise TypeError("Assignment package must be an object.")
    try:
        canonical = json.dumps(package, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("Assignment package is not strict JSON data.") from exc
    return hashlib.sha256(canonical).hexdigest()


_PLAN_FIELDS = {
    "task_id", "phase", "operation", "title", "handoff_id", "scope",
    "prohibited", "task_definition_sha256", "assignment_status",
    "completion_authority",
}


def prepare_worker_assignment(
    trusted_task: dict[str, Any],
    preflight_result: dict[str, Any],
    *,
    planned_assignment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a non-dispatchable package bound to one exact trusted task.

    A DENY result produces a blocked handoff package. An ALLOW_READ_ONLY
    result may produce a prepared package only when accompanied by the exact
    assignment entry from the batch planner. Even then dispatch remains
    disabled and a separate human activation decision is required.
    """
    if not isinstance(trusted_task, dict) or not trusted_task:
        raise TypeError("Trusted task must be a non-empty object.")
    if not isinstance(preflight_result, dict) or set(preflight_result) != _PREFLIGHT_FIELDS:
        raise ValueError("Preflight result has missing or unsupported fields.")

    task_id = trusted_task.get("task_id")
    phase = trusted_task.get("phase")
    operation = trusted_task.get("operation")
    handoff_id = trusted_task.get("handoff_id")
    scope = trusted_task.get("scope")
    prohibited = trusted_task.get("prohibited")
    if not all(isinstance(value, str) and value.strip()
               for value in (task_id, phase, operation, handoff_id)):
        raise ValueError("Trusted task identity and handoff fields must be non-empty strings.")
    if not isinstance(scope, list) or not scope or not all(
        isinstance(item, str) and item.strip() for item in scope
    ):
        raise ValueError("Trusted task scope must be a list of non-empty strings.")
    if not isinstance(prohibited, list) or not prohibited or not all(
        isinstance(item, str) and item.strip() for item in prohibited
    ):
        raise ValueError("Trusted task prohibited list must be a list of non-empty strings.")
    if trusted_task.get("completion_authority") != "human_only":
        raise ValueError("Worker assignment requires human-only completion authority.")

    if (
        preflight_result.get("task_id") != task_id
        or preflight_result.get("mode") != "preflight_only"
        or not isinstance(preflight_result.get("queue_status"), str)
        or not preflight_result["queue_status"].strip()
        or preflight_result.get("execution_performed") is not False
        or type(preflight_result.get("authorized")) is not bool
        or not isinstance(preflight_result.get("reason"), str)
        or not preflight_result["reason"].strip()
    ):
        raise ValueError("Preflight result does not match the exact task or required safe shape.")

    allowed = preflight_result["authorized"] is True
    expected_decision = "ALLOW_READ_ONLY" if allowed else "DENY"
    if preflight_result.get("decision") != expected_decision:
        raise ValueError("Preflight decision and authorization flag are inconsistent.")

    digest = task_definition_digest(trusted_task)
    if allowed:
        if not isinstance(planned_assignment, dict) or set(planned_assignment) != _PLAN_FIELDS:
            raise ValueError("An allowed preflight requires one exact batch-planner assignment.")
        expected_plan = {
            "task_id": task_id,
            "phase": phase,
            "operation": operation,
            "title": trusted_task.get("title"),
            "handoff_id": handoff_id,
            "scope": list(scope),
            "prohibited": list(prohibited),
            "task_definition_sha256": digest,
            "assignment_status": "preflight_allowed_not_executed",
            "completion_authority": "human_only",
        }
        if planned_assignment != expected_plan:
            raise ValueError("Planned assignment does not exactly match the trusted task.")
    elif planned_assignment is not None:
        raise ValueError("A denied preflight cannot be paired with a planned assignment.")

    task_copy = json.loads(json.dumps(trusted_task, allow_nan=False))
    status = "prepared_not_dispatched" if allowed else "blocked_preflight"
    return {
        "schema_version": 1,
        "mode": "worker_assignment_package_only",
        "assignment_status": status,
        "task_id": task_id,
        "phase": phase,
        "operation": operation,
        "handoff_id": handoff_id,
        "task_definition_sha256": digest,
        "trusted_task": task_copy,
        "scope": list(scope),
        "prohibited": list(prohibited),
        "allowed_declared_actions": list(_ALLOWED_ACTIONS),
        "worker_submission_schema": {
            "required_fields": [
                "schema_version", "task_id", "phase", "operation",
                "task_definition_sha256", "status", "summary", "findings",
                "evidence", "actions_performed", "limitations",
                "completion_claimed", "gate_closure_claimed",
            ],
            "evidence_fields": ["path", "sha256", "source_ref", "description"],
            "supervisor": "engine.review_pipeline.review_submission_with_verified_evidence",
        },
        "preflight": {
            "decision": expected_decision,
            "authorized": allowed,
            "reason": preflight_result["reason"],
            "execution_performed": False,
        },
        "dispatch_permitted": False,
        "execution_performed": False,
        "task_completion_approved": False,
        "gate_closure_approved": False,
        "completion_authority": "human_only",
        "human_review_required": True,
        "limitations": [
            "This is a handoff package only; no worker was dispatched and no task was executed.",
            "The package does not create or modify a trusted allowlist approval.",
            "A preflight allowance does not override the live research handoff or authorize prohibited actions.",
            "The worker must re-check the exact task and current handoff before any future permitted operation.",
            "Only a human may approve task completion or close a phase gate.",
        ],
    }
