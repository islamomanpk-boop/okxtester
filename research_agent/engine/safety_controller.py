"""Fail-closed permission checks for okx-research-agent.

This module authorizes a task; it does not execute the task. Missing or
ambiguous permission is always a denial. No network access or side effects.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
AGENT_CONFIG = ROOT / "research_agent" / "config" / "agent_config.json"
PHASE_CONFIG = ROOT / "research_agent" / "config" / "phase_permissions.json"

READ_ONLY_OPERATIONS = {
    "repository_inspection",
    "evidence_lineage_review",
    "report_generation",
}

GLOBAL_DENY_OPERATIONS = {
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
    """Raised when permission configuration is missing or malformed."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PermissionConfigError(f"Cannot load configuration: {path.name}") from exc
    if not isinstance(value, dict):
        raise PermissionConfigError(f"Configuration must be a JSON object: {path.name}")
    return value


def _deny(reason: str) -> dict[str, Any]:
    return {"authorized": False, "decision": "DENY", "reason": reason}


def authorize_task(
    task: dict[str, Any],
    *,
    allowlist: dict[str, Any] | None = None,
    agent_config: dict[str, Any] | None = None,
    phase_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Authorize one task without executing it.

    The allowlist must come from a separately reviewed trusted source.
    Expected shape: {"approved_task_ids": ["..."]}. A task cannot approve itself.
    """
    if not isinstance(task, dict):
        return _deny("Task must be a JSON object.")

    try:
        agent = agent_config if agent_config is not None else _load_json(AGENT_CONFIG)
        phases = phase_config if phase_config is not None else _load_json(PHASE_CONFIG)
    except PermissionConfigError as exc:
        return _deny(str(exc))

    if not isinstance(agent, dict):
        return _deny("Agent configuration is malformed.")
    execution = agent.get("execution")
    if not isinstance(execution, dict):
        return _deny("Agent execution configuration is missing or malformed.")
    if execution.get("require_task_allowlist") is not True:
        return _deny("Agent configuration does not require an explicit task allowlist.")
    if execution.get("require_phase_permission") is not True:
        return _deny("Agent configuration does not require phase permissions.")
    if execution.get("require_safety_controller") is not True:
        return _deny("Agent configuration does not require the safety controller.")

    if not isinstance(allowlist, dict):
        return _deny("Trusted task allowlist was not supplied.")
    approved_ids = allowlist.get("approved_task_ids")
    if not isinstance(approved_ids, list) or not all(
        isinstance(item, str) and item.strip() for item in approved_ids
    ):
        return _deny("Task allowlist is missing or malformed.")

    task_id = task.get("task_id")
    phase = task.get("phase")
    operation = task.get("operation")
    if not isinstance(task_id, str) or not task_id.strip():
        return _deny("Task is missing a valid task_id.")
    if task_id not in approved_ids:
        return _deny("Task ID is not present in the trusted allowlist.")
    if not isinstance(phase, str) or not isinstance(operation, str):
        return _deny("Task must specify phase and operation as strings.")

    phase_order = phases.get("phase_order")
    phase_rules = phases.get("phases")
    defaults = phases.get("global_defaults")
    if not isinstance(phase_order, list) or not isinstance(phase_rules, dict) or not isinstance(defaults, dict):
        return _deny("Phase permission configuration is malformed.")
    if phase not in phase_order or phase not in phase_rules:
        return _deny("Unknown phase; no permission is granted.")

    # Global prohibitions override every phase-specific allowance.
    if operation in GLOBAL_DENY_OPERATIONS:
        return _deny(f"Operation is globally prohibited: {operation}")
    if operation not in READ_ONLY_OPERATIONS:
        return _deny(f"Unrecognized or non-read-only operation: {operation}")

    phase_rule = phase_rules[phase]
    if not isinstance(phase_rule, dict):
        return _deny("Phase rule is malformed.")

    # G0-05 permits only read-only reconciliation under its current handoff.
    # The operation allowlist above excludes scripts, tests, workflows, and writes.
    if phase == "phase3_sideways_range":
        g0_05 = phase_rule.get("g0_05")
        if not isinstance(g0_05, dict):
            return _deny("Phase 3 G0-05 lock configuration is missing.")
        targets_g0_05 = (
            task.get("handoff_id") == "PHASE3_G0_05_RECONCILIATION_TASK_02"
            or task.get("workstream") == "g0_05"
        )
        if targets_g0_05 and (
            g0_05.get("status") != "read_only_reconciliation_only"
            or g0_05.get("scripts_tests_workflows") != "prohibited"
            or g0_05.get("data_or_code_changes") != "prohibited"
            or g0_05.get("backtesting_and_pnl") != "prohibited"
            or g0_05.get("gate_closure") != "prohibited"
        ):
            return _deny("G0-05 safety lock is missing, weakened, or malformed.")

    if phase_rule.get("execution_override") == "deny" and operation not in READ_ONLY_OPERATIONS:
        return _deny("Phase execution override denies this operation.")

    default_key = {
        "repository_inspection": "repository_inspection",
        "evidence_lineage_review": "evidence_lineage_review",
        "report_generation": "report_generation",
    }[operation]
    permitted_values = {
        "repository_inspection": {"allow_read_only"},
        "evidence_lineage_review": {"allow_read_only"},
        "report_generation": {"allow_local_or_artifact_only"},
    }
    if defaults.get(default_key) not in permitted_values[operation]:
        return _deny("Global configuration does not explicitly permit this read-only operation.")

    return {
        "authorized": True,
        "decision": "ALLOW_READ_ONLY",
        "reason": "Task is allowlisted and within the configured read-only scope.",
        "task_id": task_id,
        "phase": phase,
        "operation": operation,
        "execution_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check an OKX research task's permissions; this command does not execute it."
    )
    parser.add_argument("task_file", type=Path, help="Path to a JSON task description.")
    parser.add_argument(
        "--allowlist-file",
        type=Path,
        required=True,
        help="Trusted JSON allowlist containing approved_task_ids.",
    )
    args = parser.parse_args()
    try:
        task = json.loads(args.task_file.read_text(encoding="utf-8"))
        allowlist = json.loads(args.allowlist_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps(_deny(f"Cannot read task or allowlist: {exc}"), indent=2))
        return 2
    result = authorize_task(task, allowlist=allowlist)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["authorized"] else 1


if __name__ == "__main__":
    sys.exit(main())
