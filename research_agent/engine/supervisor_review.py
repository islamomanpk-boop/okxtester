"""Supervisor review gate for untrusted worker submissions.

This module validates submission structure and policy declarations only. It
does not verify evidence contents, execute tasks, approve completion, or close
research gates. Every passing submission remains subject to human review.
"""
from __future__ import annotations

import re
from typing import Any

from .report_builder import task_definition_digest

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_WORKER_STATUSES = {"completed", "partial", "blocked"}
_EXPECTED_FIELDS = {
    "schema_version", "task_id", "phase", "operation",
    "task_definition_sha256", "status", "summary", "findings",
    "evidence", "actions_performed", "limitations",
    "completion_claimed", "gate_closure_claimed",
}
_EVIDENCE_FIELDS = {"path", "sha256", "source_ref", "description"}
# Worker declarations are deliberately limited to benign, read-only/reporting actions.
# Unknown labels fail closed; they cannot disguise prohibited operations.
_ALLOWED_DECLARED_ACTIONS = {
    "read_existing_documentation",
    "inspect_repository_metadata",
    "compare_documented_values",
    "trace_source_references",
    "hash_evidence_file",
    "prepare_report",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _safe_evidence_path(value: str) -> bool:
    if not value or value.startswith(("/", "\\")) or "\\" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        return False
    parts = value.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def review_worker_submission(
    trusted_task: dict[str, Any],
    submission: dict[str, Any],
) -> dict[str, Any]:
    """Return a conservative review disposition for one worker submission.

    The trusted task must be the exact task object from the repository queue.
    The submission is untrusted data. A ready result means only that the
    package is structurally eligible for human review, never that the research
    is correct or complete.
    """
    if not isinstance(trusted_task, dict):
        raise TypeError("Trusted task must be an object.")
    if not isinstance(submission, dict):
        raise TypeError("Worker submission must be an object.")

    task_id = trusted_task.get("task_id")
    phase = trusted_task.get("phase")
    operation = trusted_task.get("operation")
    expected_digest = task_definition_digest(trusted_task)

    issues: list[str] = []
    safety_violations: list[str] = []

    if set(submission) != _EXPECTED_FIELDS:
        missing = sorted(_EXPECTED_FIELDS - set(submission))
        extra = sorted(set(submission) - _EXPECTED_FIELDS)
        if missing:
            issues.append("Missing required submission fields: " + ", ".join(missing))
        if extra:
            issues.append("Unsupported submission fields: " + ", ".join(extra))

    if type(submission.get("schema_version")) is not int or submission.get("schema_version") != 1:
        issues.append("Unsupported worker submission schema version.")
    if submission.get("task_id") != task_id:
        issues.append("Submission task ID does not match the trusted queue task.")
    if submission.get("phase") != phase:
        issues.append("Submission phase does not match the trusted queue task.")
    if submission.get("operation") != operation:
        issues.append("Submission operation does not match the trusted queue task.")
    if submission.get("task_definition_sha256") != expected_digest:
        issues.append("Submission task-definition digest does not match the trusted queue task.")

    status = submission.get("status")
    if not isinstance(status, str) or status not in _ALLOWED_WORKER_STATUSES:
        issues.append("Worker status must be completed, partial, or blocked.")
    if not _nonempty_string(submission.get("summary")):
        issues.append("Submission summary must be a non-empty string.")

    findings = submission.get("findings")
    if not isinstance(findings, list) or any(not _nonempty_string(item) for item in findings):
        issues.append("Findings must be a list of non-empty strings.")

    evidence = submission.get("evidence")
    if not isinstance(evidence, list):
        issues.append("Evidence must be a list.")
        evidence = []
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict) or set(item) != _EVIDENCE_FIELDS:
                issues.append(f"Evidence item {index} has an invalid schema.")
                continue
            if not all(_nonempty_string(item.get(key)) for key in _EVIDENCE_FIELDS):
                issues.append(f"Evidence item {index} has an empty required field.")
                continue
            if not _safe_evidence_path(item["path"]):
                issues.append(f"Evidence item {index} has an unsafe repository path.")
            if not _SHA256_RE.fullmatch(item["sha256"]):
                issues.append(f"Evidence item {index} has an invalid SHA-256 digest.")

    actions = submission.get("actions_performed")
    if not isinstance(actions, list) or any(not _nonempty_string(item) for item in actions):
        issues.append("actions_performed must be a list of non-empty strings.")
        actions = []
    prohibited = trusted_task.get("prohibited")
    if not isinstance(prohibited, list) or any(not _nonempty_string(item) for item in prohibited):
        issues.append("Trusted task has an invalid prohibited-action list.")
        prohibited = []
    for action in actions:
        if action in prohibited:
            safety_violations.append(action)
        elif action not in _ALLOWED_DECLARED_ACTIONS:
            safety_violations.append("unsupported_action:" + action)

    limitations = submission.get("limitations")
    if not isinstance(limitations, list) or any(not _nonempty_string(item) for item in limitations):
        issues.append("Limitations must be a list of non-empty strings.")
        limitations = []

    if type(submission.get("completion_claimed")) is not bool:
        issues.append("completion_claimed must be Boolean.")
    if type(submission.get("gate_closure_claimed")) is not bool:
        issues.append("gate_closure_claimed must be Boolean.")
    if submission.get("gate_closure_claimed") is True:
        safety_violations.append("gate_closure_claimed")
    if status == "completed" and submission.get("completion_claimed") is not True:
        issues.append("A completed status must explicitly identify itself as a worker completion claim.")
    if status == "completed" and not evidence:
        issues.append("A completed submission requires at least one evidence reference.")
    if status == "completed" and not actions:
        issues.append("A completed submission must declare at least one permitted action.")
    if status != "completed" and submission.get("completion_claimed") is True:
        issues.append("Only a completed status may carry a worker completion claim.")
    if status == "blocked" and not limitations:
        issues.append("A blocked submission must explain its limitations or blocker.")

    if safety_violations:
        disposition = "rejected_safety_violation"
    elif issues:
        disposition = "return_for_revision"
    elif status == "blocked":
        disposition = "blocked_submission_recorded"
    elif status == "partial":
        disposition = "partial_submission_needs_human_review"
    else:
        disposition = "ready_for_human_review"

    return {
        "mode": "supervisor_review_only",
        "task_id": task_id,
        "phase": phase,
        "review_disposition": disposition,
        "submission_structurally_valid": not issues and not safety_violations,
        "evidence_content_verified": False,
        "research_correctness_verified": False,
        "task_execution_authorized": False,
        "task_completion_approved": False,
        "gate_closure_approved": False,
        "human_review_required": True,
        "issues": issues,
        "safety_violations": safety_violations,
        "evidence_count_declared": len(evidence),
        "limitations": [
            "Evidence paths, source references, and hashes are worker declarations until independently checked against the checkout.",
            "A structurally valid submission is not proof that findings are accurate or complete.",
            "Only a human may accept task completion or close a phase gate.",
        ],
    }
