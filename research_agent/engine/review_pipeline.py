"""Integrated structural and evidence-integrity review pipeline.

This orchestration layer combines existing pure validators. Caller-supplied
checkout context is not authenticated here; no work, filesystem, GitHub, or
network operations are performed.
"""
from __future__ import annotations

from typing import Any

from .evidence_verifier import verify_worker_evidence
from .supervisor_review import review_worker_submission


def review_submission_with_verified_evidence(
    trusted_task: dict[str, Any],
    submission: dict[str, Any],
    *,
    expected_commit_sha: str,
    commit_manifest: dict[str, Any],
    file_contents: dict[str, bytes],
) -> dict[str, Any]:
    """Return structural review plus per-item integrity results, never approval."""
    structural = review_worker_submission(trusted_task, submission)
    result: dict[str, Any] = {
        "mode": "integrated_supervisor_review_only",
        "structural_review": structural,
        "evidence_verification": None,
        "evidence_integrity_passed": False,
        "review_disposition": structural["review_disposition"],
        "task_completion_approved": False,
        "gate_closure_approved": False,
        "human_review_required": True,
        "limitations": [
            "Caller-supplied commit context, manifest, and checkout bytes are not authenticated by this orchestration layer.",
            "Evidence integrity does not establish research correctness, completeness, or source truth.",
            "A human must inspect findings and independently validate workflow provenance before accepting completion.",
        ],
    }

    if not structural["submission_structurally_valid"]:
        result["limitations"].append(
            "Evidence verification was skipped because the worker submission failed structural or safety review."
        )
        return result

    evidence = submission["evidence"]
    try:
        verification = verify_worker_evidence(
            evidence,
            expected_commit_sha=expected_commit_sha,
            commit_manifest=commit_manifest,
            file_contents=file_contents,
        )
    except (TypeError, ValueError) as exc:
        result["evidence_verification"] = {
            "mode": "evidence_verification_only",
            "verification_error": type(exc).__name__,
            "all_evidence_verified": False,
            "task_completion_approved": False,
            "gate_closure_approved": False,
            "human_review_required": True,
        }
        result["review_disposition"] = "return_for_revision"
        result["limitations"].append(
            "Evidence verification could not be completed because its supplied commit context or manifest was invalid."
        )
        return result

    result["evidence_verification"] = verification
    result["evidence_integrity_passed"] = (
        verification["evidence_count"] > 0 and verification["all_evidence_verified"]
    )
    result["review_disposition"] = structural["review_disposition"]
    if verification["rejected_count"] > 0:
        result["review_disposition"] = "return_for_revision"
        result["limitations"].append(
            "One or more evidence references failed integrity verification; the submission must be revised."
        )
    return result
