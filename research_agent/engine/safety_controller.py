"""Fail-closed authorization for the OKX research operations agent.

This module evaluates permissions only. It never executes a research task.
All missing, malformed, stale, or conflicting policy data results in DENY.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "research_agent" / "config"
AGENT_CONFIG = CONFIG_DIR / "agent_config.json"
PHASE_CONFIG = CONFIG_DIR / "phase_permissions.json"
QUEUE_CONFIG = CONFIG_DIR / "task_queue.json"
ALLOWLIST_CONFIG = CONFIG_DIR / "task_allowlist.json"

READ_ONLY_OPERATIONS = {
    "repository_inspection",
    "evidence_lineage_review",
    "report_generation",
}
DENIED_OPERATIONS = {
    "modify_code",
    "modify_research_data",
    "modify_canonical_definitions",
    "create_candidates",
    "run_backtests",
    "make_pnl_claims",
    "select_strategies",
    "close_gates",
    "deploy_to_vps",
    "change_secrets_or_permissions",
    "trigger_workflows",
    "execute_scripts",
    "execute_tests",
}


class PermissionConfigError(Exception):
    """Raised when trusted permission configuration is missing or malformed."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PermissionConfigError(f"Cannot load configuration: {path.name}") from exc
    if not isinstance(value, dict):
        raise PermissionConfigError(f"Configuration must be a JSON object: {path.name}")
    return value


def _canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _deny(reason: str) -> dict[str, Any]:
    return {"authorized": False, "decision": "DENY", "reason": reason}


def _authorize_task_impl(
    task: dict[str, Any],
    *,
    allowlist: dict[str, Any] | None = None,
    agent_config: dict[str, Any] | None = None,
    phase_config: dict[str, Any] | None = None,
    queue_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate an exact queued task against a separately trusted hash allowlist.

    Allowlist shape: {"approved_tasks": [{"task_id": "...", "task_sha256": "..."}]}.
    A task cannot approve itself, change its own operation, or change its phase.
    """
    if not isinstance(task, dict):
        return _deny("Task must be a JSON object.")

    try:
        agent = agent_config if agent_config is not None else _load_json(AGENT_CONFIG)
        phases = phase_config if phase_config is not None else _load_json(PHASE_CONFIG)
        queue = queue_config if queue_config is not None else _load_json(QUEUE_CONFIG)
        trusted_allowlist = allowlist if allowlist is not None else _load_json(ALLOWLIST_CONFIG)
    except PermissionConfigError as exc:
        return _deny(str(exc))

    if not all(isinstance(item, dict) for item in (agent, phases, queue, trusted_allowlist)):
        return _deny("One or more policy documents are malformed.")

    execution = agent.get("execution")
    if not isinstance(execution, dict):
        return _deny("Agent execution configuration is missing or malformed.")
    if execution.get("enabled") is not True:
        return _deny("Agent execution is disabled; no task can execute.")
    for required_flag in (
        "require_task_allowlist",
        "require_phase_permission",
        "require_safety_controller",
    ):
        if execution.get(required_flag) is not True:
            return _deny(f"Required safety setting is not enabled: {required_flag}")

    queue_policy = queue.get("queue_policy")
    queue_tasks = queue.get("tasks")
    if not isinstance(queue_policy, dict) or not isinstance(queue_tasks, list):
        return _deny("Task queue policy is missing or malformed.")
    if queue_policy.get("execution_enabled") is not True:
        return _deny("Task queue execution is disabled.")
    if queue_policy.get("no_phase_skipping") is not True:
        return _deny("Queue does not enforce sequential phase order.")
    if queue_policy.get("tasks_may_not_override_handoffs") is not True:
        return _deny("Queue does not preserve handoff restrictions.")

    approved = trusted_allowlist.get("approved_tasks")
    if not isinstance(approved, list):
        return _deny("Trusted allowlist must contain an approved_tasks list.")
    if not all(
        isinstance(row, dict)
        and isinstance(row.get("task_id"), str)
        and isinstance(row.get("task_sha256"), str)
        for row in approved
    ):
        return _deny("Trusted allowlist entries are malformed.")

    task_id = task.get("task_id")
    if not isinstance(task_id, str) or not task_id.strip():
        return _deny("Task is missing a valid task_id.")

    queued_matches = [row for row in queue_tasks if isinstance(row, dict) and row.get("task_id") == task_id]
    if len(queued_matches) != 1:
        return _deny("Task ID must match exactly one queue entry.")
    queued_task = queued_matches[0]
    if task != queued_task:
        return _deny("Submitted task differs from its trusted queue definition.")
    if queued_task.get("status") != "queued":
        return _deny("Task is not in queued status.")

    allow_matches = [row for row in approved if row["task_id"] == task_id]
    if len(allow_matches) != 1:
        return _deny("Task is not uniquely approved in the trusted allowlist.")
    if allow_matches[0]["task_sha256"] != _canonical_hash(queued_task):
        return _deny("Task definition hash does not match the trusted approval.")

    phase = queued_task.get("phase")
    operation = queued_task.get("operation")
    phase_order = phases.get("phase_order")
    phase_rules = phases.get("phases")
    defaults = phases.get("global_defaults")
    if not isinstance(phase_order, list) or not phase_order or not all(
        isinstance(item, str) and item.strip() for item in phase_order
    ) or len(set(phase_order)) != len(phase_order):
        return _deny("Phase order must contain unique, non-empty phase names.")
    if not isinstance(phase_rules, dict) or not isinstance(defaults, dict):
        return _deny("Phase permission configuration is malformed.")
    if phase not in phase_order or phase not in phase_rules:
        return _deny("Unknown phase; no permission is granted.")
    if agent.get("phase_order") != phase_order or queue_policy.get("phase_order") != phase_order:
        return _deny("Agent, queue, and phase permission order do not agree.")

    phase_rule = phase_rules[phase]
    if not isinstance(phase_rule, dict):
        return _deny("Phase permission entry is malformed.")
    if phase_rule.get("status") != "active_research_phase":
        return _deny("Task belongs to a phase that is not currently active.")

    # Require an explicit read-only opt-in; missing, deny, and unknown values fail closed.
    if phase_rule.get("execution_override") != "allow_read_only":
        return _deny("Phase execution override does not explicitly allow read-only work.")

    # A later phase cannot become executable by changing its status alone.
    phase_index = phase_order.index(phase)
    for prior_phase in phase_order[:phase_index]:
        prior_rule = phase_rules.get(prior_phase)
        if not isinstance(prior_rule, dict):
            return _deny(f"Prior phase permission is missing or malformed: {prior_phase}")
        if prior_rule.get("gate_status") != "human_authorized_closed":
            return _deny(
                f"Prior phase gate is not explicitly human-authorized closed: {prior_phase}"
            )

    if not isinstance(operation, str) or not operation.strip():
        return _deny("Task operation must be a non-empty string.")
    if operation in DENIED_OPERATIONS:
        return _deny(f"Operation is prohibited: {operation}")
    if operation not in READ_ONLY_OPERATIONS:
        return _deny(f"Unknown or non-read-only operation: {operation}")

    if phase == "phase3_sideways_range":
        g0_05 = phase_rule.get("g0_05")
        if not isinstance(g0_05, dict):
            return _deny("Phase 3 G0-05 lock configuration is missing.")
        global_g0_05_lock = execution.get("current_g0_05_execution_lock")
        if not isinstance(global_g0_05_lock, bool):
            return _deny("Global G0-05 lock must be explicitly true or false.")
        # While the current G0-05 handoff is active, do not rely on task labels:
        # every Phase 3 task is denied, preventing a relabelled task bypass.
        if global_g0_05_lock is True:
            return _deny("G0-05 execution lock is active; all Phase 3 task authorization is prohibited.")
        if queued_task.get("workstream") == "g0_05" or queued_task.get(
            "handoff_id"
        ) == "PHASE3_G0_05_RECONCILIATION_TASK_02":
            required_lock_values = {
                "status": "read_only_reconciliation_only",
                "scripts_tests_workflows": "prohibited",
                "data_or_code_changes": "prohibited",
                "candidate_generation": "prohibited",
                "backtesting_and_pnl": "prohibited",
                "gate_closure": "prohibited",
            }
            if any(g0_05.get(key) != value for key, value in required_lock_values.items()):
                return _deny("G0-05 safety lock is missing, weakened, or malformed.")

    default_values = {
        "repository_inspection": ("repository_inspection", "allow_read_only"),
        "evidence_lineage_review": ("evidence_lineage_review", "allow_read_only"),
        "report_generation": ("report_generation", "allow_local_or_artifact_only"),
    }
    config_key, required_value = default_values[operation]
    if defaults.get(config_key) != required_value:
        return _deny("Global configuration does not explicitly permit this operation.")

    return {
        "authorized": True,
        "decision": "ALLOW_READ_ONLY",
        "reason": "Exact queued task, trusted hash approval, phase, and read-only policy all match.",
        "task_id": task_id,
        "phase": phase,
        "operation": operation,
        "execution_performed": False,
    }


def _authorize_task_with_policy(
    task: dict[str, Any],
    *,
    allowlist: dict[str, Any] | None = None,
    agent_config: dict[str, Any] | None = None,
    phase_config: dict[str, Any] | None = None,
    queue_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Test seam: evaluate against explicitly supplied policy fixtures only."""
    try:
        return _authorize_task_impl(
            task,
            allowlist=allowlist,
            agent_config=agent_config,
            phase_config=phase_config,
            queue_config=queue_config,
        )
    except Exception as exc:
        # Do not leak configuration contents or allow malformed inputs to crash
        # the authorization boundary. Runtime tests should still expose bugs.
        return _deny(
            "Malformed task or policy input; authorization denied "
            f"({type(exc).__name__})."
        )


def authorize_task(task: dict[str, Any]) -> dict[str, Any]:
    """Runtime authorization using only policy files fixed in this checkout."""
    return _authorize_task_with_policy(task)


def authorize_trusted_task(task: dict[str, Any]) -> dict[str, Any]:
    """Explicit alias for the trusted, non-injectable runtime boundary."""
    return authorize_task(task)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate an OKX research task's permissions; does not execute it."
    )
    parser.add_argument("task_file", type=Path, help="JSON task copied exactly from the queue.")
    args = parser.parse_args()
    try:
        task = json.loads(args.task_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = _deny(f"Cannot read task file: {exc}")
    else:
        result = authorize_task(task)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["authorized"] else 1


if __name__ == "__main__":
    sys.exit(main())
