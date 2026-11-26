"""Assignment-bound worker return review; no dispatch or completion authority."""
from __future__ import annotations

from typing import Any

from .report_builder import task_definition_digest
from .review_pipeline import review_submission_with_verified_evidence


def review_assignment_return(
    trusted_task: dict[str, Any],
    assignment_package: dict[str, Any],
    submission: dict[str, Any],
    *,
    expected_commit_sha: str,
    commit_manifest: dict[str, Any],
    file_contents: dict[str, bytes],
) -> dict[str, Any]:
    """Bind a returned submission to its prepared assignment, then review it.

    This function does not prove that a worker was dispatched or that the
    package was delivered. Blocked packages and any package with altered
    identity, scope, policy, or authority are rejected before submission
    review. Passing remains human-review-only.
    """
    if not isinstance(trusted_task, dict) or not isinstance(assignment_package, dict):
        raise TypeError("Trusted task and assignment package must be objects.")
    if assignment_package.get("schema_version") != 1:
        raise ValueError("Unsupported assignment package schema version.")
    if assignment_package.get("mode") != "worker_assignment_package_only":
        raise ValueError("Assignment package mode is invalid.")
    if assignment_package.get("assignment_status") != "prepared_not_dispatched":
        raise ValueError("Only a prepared, non-blocked assignment package can be reviewed.")
    if assignment_package.get("dispatch_permitted") is not False:
        raise ValueError("Assignment package must not claim dispatch permission.")
    for field in ("execution_performed", "task_completion_approved", "gate_closure_approved"):
        if assignment_package.get(field) is not False:
            raise ValueError(f"Assignment package has an invalid authority flag: {field}.")
    if assignment_package.get("completion_authority") != "human_only":
        raise ValueError("Assignment package must preserve human-only completion authority.")

    digest = task_definition_digest(trusted_task)
    expected = {
        "task_id": trusted_task.get("task_id"),
        "phase": trusted_task.get("phase"),
        "operation": trusted_task.get("operation"),
        "handoff_id": trusted_task.get("handoff_id"),
        "task_definition_sha256": digest,
        "trusted_task": trusted_task,
        "scope": trusted_task.get("scope"),
        "prohibited": trusted_task.get("prohibited"),
        "completion_authority": "human_only",
    }
    for field, value in expected.items():
        if assignment_package.get(field) != value:
            raise ValueError(f"Assignment package does not match trusted task field: {field}.")

    preflight = assignment_package.get("preflight")
    if not isinstance(preflight, dict) or preflight != {
        "decision": "ALLOW_READ_ONLY",
        "authorized": True,
        "reason": preflight.get("reason") if isinstance(preflight, dict) else None,
        "execution_performed": False,
    } or not isinstance(preflight.get("reason"), str) or not preflight["reason"].strip():
        raise ValueError("Assignment package does not contain an exact allowed preflight result.")

    review = review_submission_with_verified_evidence(
        trusted_task,
        submission,
        expected_commit_sha=expected_commit_sha,
        commit_manifest=commit_manifest,
        file_contents=file_contents,
    )
    return {
        "mode": "assignment_bound_return_review_only",
        "assignment_binding_verified": True,
        "dispatch_or_delivery_verified": False,
        "submission_review": review,
        "task_completion_approved": False,
        "gate_closure_approved": False,
        "human_review_required": True,
        "limitations": [
            "Assignment binding does not prove that a worker was dispatched or received the package.",
            "Caller-supplied commit context, manifest, and file bytes remain subject to independent workflow verification.",
            "Evidence integrity does not establish research correctness, completeness, or source truth.",
            "Only a human may accept task completion or close a phase gate.",
        ],
    }
