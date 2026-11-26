"""Read-only queue preflight for okx-research-agent.

Despite the historical module name, this scaffold does not execute research
work. It selects a queue entry and asks the safety controller for a decision.
The current disabled execution switches make every task non-runnable.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .safety_controller import authorize_task

ROOT = Path(__file__).resolve().parents[2]
QUEUE_PATH = ROOT / "research_agent" / "config" / "task_queue.json"


def load_queue(path: Path = QUEUE_PATH) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("tasks"), list):
        raise ValueError("Task queue is missing or malformed.")
    return value


def _preflight_result(
    task_id: str | None,
    *,
    queue_status: str = "unknown",
    decision: str = "DENY",
    authorized: bool = False,
    reason: str,
) -> dict[str, Any]:
    """Return one stable, explicitly non-executing preflight result shape."""
    return {
        "task_id": task_id,
        "queue_status": queue_status,
        "decision": decision,
        "authorized": authorized,
        "reason": reason,
        "execution_performed": False,
        "mode": "preflight_only",
    }


def _preflight_task_with_queue(task_id: str, current_queue: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one exact queue entry; never invokes an executor or changes files."""
    if not isinstance(task_id, str) or not task_id.strip():
        return _preflight_result(
            None, reason="A non-empty task ID is required."
        )

    if not isinstance(current_queue, dict):
        return _preflight_result(
            task_id, reason="Task queue must be a JSON object."
        )
    tasks = current_queue.get("tasks")
    if not isinstance(tasks, list):
        return _preflight_result(
            task_id, reason="Task queue entries are malformed."
        )
    # Fail closed on any malformed row rather than silently filtering it out.
    if not all(isinstance(task, dict) for task in tasks):
        return _preflight_result(
            task_id, reason="Every task queue entry must be a JSON object."
        )
    matches = [task for task in tasks if task.get("task_id") == task_id]
    if len(matches) != 1:
        return _preflight_result(
            task_id, reason="Task ID must match exactly one queue entry."
        )

    task = matches[0]
    queue_status = task.get("status")
    if not isinstance(queue_status, str) or not queue_status.strip():
        queue_status = "unknown"
    decision = authorize_task(task)
    if not isinstance(decision, dict):
        return _preflight_result(
            task_id,
            queue_status=queue_status,
            reason="Safety controller returned a malformed decision; denied.",
        )
    valid_reason = decision.get("reason")
    authorized = (
        decision.get("authorized") is True
        and decision.get("decision") == "ALLOW_READ_ONLY"
        and isinstance(valid_reason, str)
        and bool(valid_reason.strip())
    )
    return _preflight_result(
        task_id,
        queue_status=queue_status,
        decision="ALLOW_READ_ONLY" if authorized else "DENY",
        authorized=authorized,
        reason=(
            valid_reason if isinstance(valid_reason, str) and valid_reason.strip()
            else "Safety controller returned no valid reason; denied."
        ),
    )


def preflight_task(task_id: str) -> dict[str, Any]:
    """Runtime preflight against the queue stored in this repository only."""
    try:
        trusted_queue = load_queue()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return {"decision": "DENY", "reason": f"Cannot load task queue: {exc}"}
    return _preflight_task_with_queue(task_id, trusted_queue)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preflight a queued research task. This tool never executes tasks."
    )
    parser.add_argument("--task-id", required=True, help="Exact task ID from task_queue.json.")
    args = parser.parse_args()
    result = preflight_task(args.task_id)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("authorized") else 1


if __name__ == "__main__":
    raise SystemExit(main())
