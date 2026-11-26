"""Assignment-bound worker return review; no dispatch or completion authority."""
from __future__ import annotations

from typing import Any

import json

from .assignment_package import prepare_worker_assignment
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
    if type(assignment_package.get("schema_version")) is not int or assignment_package.get("schema_version") != 1:
        raise ValueError("Unsupported assignment package schema version.")

    digest = task_definition_digest(trusted_task)
    preflight = assignment_package.get("preflight")
    if not isinstance(preflight, dict):
        raise ValueError("Assignment package preflight record is invalid.")
    reason = preflight.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Assignment package does not contain an exact allowed preflight result.")

    # Rebuild the package from the trusted task and the minimal allowed
    # preflight facts, then compare canonical JSON. String comparison keeps
    # JSON booleans distinct from integers (Python dict equality does not).
    canonical_preflight = {
        "task_id": trusted_task.get("task_id"),
        "queue_status": "queued",
        "decision": "ALLOW_READ_ONLY",
        "authorized": True,
        "reason": reason,
        "execution_performed": False,
        "mode": "preflight_only",
    }
    canonical_plan = {
        "task_id": trusted_task.get("task_id"),
        "phase": trusted_task.get("phase"),
        "operation": trusted_task.get("operation"),
        "title": trusted_task.get("title"),
        "handoff_id": trusted_task.get("handoff_id"),
        "scope": trusted_task.get("scope"),
        "prohibited": trusted_task.get("prohibited"),
        "task_definition_sha256": digest,
        "assignment_status": "preflight_allowed_not_executed",
        "completion_authority": "human_only",
    }
    expected_package = prepare_worker_assignment(
        trusted_task, canonical_preflight, planned_assignment=canonical_plan
    )
    try:
        supplied_canonical = json.dumps(
            assignment_package, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        )
        expected_canonical = json.dumps(
            expected_package, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Assignment package is not strict JSON data.") from exc
    if supplied_canonical != expected_canonical:
        raise ValueError("Assignment package does not exactly match the canonical trusted package.")

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
