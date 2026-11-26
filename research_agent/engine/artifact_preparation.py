"""Preflight-to-artifact orchestration; deliberately performs no task work or writes."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from .report_builder import (
    build_artifact_bundle,
    build_input_manifest,
    build_preflight_report,
)
from .task_runner import _preflight_task_with_queue, load_queue

EXPECTED_REPOSITORY = "islamomanpk-boop/okxtester"
EXPECTED_BRANCH = "agent/okx-research-agent-v1"


def prepare_task_artifact(
    task_id: str,
    *,
    repository: str,
    branch: str,
    commit_sha: str,
    actual_head_sha: str,
    checkout_clean: bool,
    run_id: str,
    run_attempt: str,
    timestamp_utc: str,
    input_paths: Iterable[str | Path] = (),
) -> dict[str, Any]:
    """Prepare one preflight-only report and in-memory artifact bundle.

    Workflow context arguments must be obtained independently from trusted
    GitHub event/checkout metadata. This function does not authenticate them.
    It never executes a task, launches a process, changes queue state, writes
    files, uploads artifacts, or treats preflight approval as task completion.
    A DENY decision is still reportable as a blocked artifact.
    """
    if repository != EXPECTED_REPOSITORY:
        raise ValueError("Repository does not match the configured research repository.")
    if branch != EXPECTED_BRANCH:
        raise ValueError("Artifact preparation is restricted to the isolated agent branch.")

    queue = load_queue()
    tasks = queue.get("tasks")
    if not isinstance(tasks, list) or not all(isinstance(row, dict) for row in tasks):
        raise ValueError("Trusted task queue is malformed.")
    matches = [row for row in tasks if row.get("task_id") == task_id]
    if len(matches) != 1:
        raise ValueError("Task ID must match exactly one trusted queue entry.")
    task = matches[0]

    preflight = _preflight_task_with_queue(task_id, queue)
    manifest = build_input_manifest(input_paths)
    report = build_preflight_report(
        task,
        preflight,
        repository=repository,
        branch=branch,
        commit_sha=commit_sha,
        run_id=run_id,
        timestamp_utc=timestamp_utc,
        input_manifest=manifest,
    )
    bundle = build_artifact_bundle(
        report,
        task,
        expected_repository=repository,
        expected_branch=branch,
        expected_commit_sha=commit_sha,
        actual_head_sha=actual_head_sha,
        checkout_clean=checkout_clean,
        run_id=run_id,
        run_attempt=run_attempt,
    )
    return {
        "mode": "preflight_artifact_preparation_only",
        "task_id": task_id,
        "preflight": preflight,
        "report_status": report["status"],
        "execution_performed": False,
        "filesystem_writes_performed": False,
        "artifact_upload_performed": False,
        "bundle": bundle,
    }
