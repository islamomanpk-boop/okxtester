"""Assignment-return to audit-artifact handoff; never grants completion authority."""
from __future__ import annotations
import json
from typing import Any
from .assignment_return import review_assignment_return
from .report_builder import build_artifact_bundle, task_definition_digest

EXPECTED_REPOSITORY = "islamomanpk-boop/okxtester"
EXPECTED_BRANCH = "agent/okx-research-agent-v1"

def _as_text(value: Any) -> str:
    rendered = value if isinstance(value, str) else json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    rendered = " ".join(rendered.split())
    return rendered if len(rendered) <= 2000 else rendered[:1997] + "..."

def build_assignment_review_artifact(
    trusted_task: dict[str, Any], assignment_package: dict[str, Any], submission: dict[str, Any], *,
    expected_commit_sha: str, commit_manifest: dict[str, Any], file_contents: dict[str, bytes],
    repository: str, branch: str, commit_sha: str, actual_head_sha: str, checkout_clean: bool,
    run_id: str, run_attempt: str, timestamp_utc: str, input_manifest: list[dict[str, str]],
) -> dict[str, Any]:
    """Review one exact assignment return and create a provenance-checked in-memory bundle.

    Workflow metadata, commit manifest, and file bytes must be obtained independently
    by the caller. No execution, dispatch, filesystem write, upload, or network occurs.
    """
    if repository != EXPECTED_REPOSITORY:
        raise ValueError("Repository does not match the configured research repository.")
    if branch != EXPECTED_BRANCH:
        raise ValueError("Review artifacts are restricted to the isolated agent branch.")
    if commit_sha != expected_commit_sha:
        raise ValueError("Report commit SHA must match the evidence-review commit SHA.")

    review = review_assignment_return(
        trusted_task, assignment_package, submission,
        expected_commit_sha=expected_commit_sha, commit_manifest=commit_manifest,
        file_contents=file_contents,
    )
    if review.get("assignment_binding_verified") is not True:
        raise ValueError("Assignment binding was not verified.")
    if review.get("dispatch_or_delivery_verified") is not False:
        raise ValueError("Review result has an invalid dispatch/delivery boundary.")
    if review.get("task_completion_approved") is not False or review.get("gate_closure_approved") is not False:
        raise ValueError("Review result must preserve human-only completion authority.")

    supervisor = review["submission_review"]
    structural = supervisor["structural_review"]
    evidence = supervisor.get("evidence_verification")
    findings = [
        "This artifact records an assignment-bound worker return and supervisor review only; it does not certify task completion.",
        "Supervisor disposition: " + _as_text(supervisor["review_disposition"]),
        "Worker-declared status: " + _as_text(submission.get("status")),
        "Worker-declared summary (not independently assessed): " + _as_text(submission.get("summary")),
        "Structural submission validity: " + str(structural.get("submission_structurally_valid") is True),
        "Evidence integrity passed against the caller-supplied commit manifest and bytes: " + str(supervisor.get("evidence_integrity_passed") is True),
    ]
    worker_findings = submission.get("findings", [])
    if isinstance(worker_findings, list):
        findings.extend("Worker-declared finding (not independently assessed): " + _as_text(item) for item in worker_findings)
    evidence_results = evidence.get("results", []) if isinstance(evidence, dict) else []
    declared_evidence = submission.get("evidence", [])
    if isinstance(declared_evidence, list):
        for index, item in enumerate(declared_evidence):
            if not isinstance(item, dict):
                findings.append("Evidence reference " + str(index) + ": malformed worker declaration.")
                continue
            result = evidence_results[index] if index < len(evidence_results) and isinstance(evidence_results[index], dict) else {}
            findings.append(
                "Evidence reference " + str(index) + ": path=" + _as_text(item.get("path"))
                + "; source_ref=" + _as_text(item.get("source_ref"))
                + "; declared_sha256=" + _as_text(item.get("sha256"))
                + "; integrity_status=" + _as_text(result.get("status", "not_verified"))
            )

    blockers = []
    for item in structural.get("issues", []):
        blockers.append("Structural issue: " + _as_text(item))
    for item in structural.get("safety_violations", []):
        blockers.append("Safety violation: " + _as_text(item))
    if supervisor["review_disposition"] in {"return_for_revision", "rejected_safety_violation", "blocked_submission_recorded"}:
        blockers.append("Supervisor disposition requires correction or further review: " + _as_text(supervisor["review_disposition"]))
    if isinstance(evidence, dict):
        for row in evidence.get("results", []):
            if isinstance(row, dict) and row.get("status") != "verified":
                blockers.append("Evidence integrity issue for " + _as_text(row.get("path")) + ": " + _as_text(row.get("reasons", [])))
        if evidence.get("verification_error"):
            blockers.append("Evidence verification error: " + _as_text(evidence["verification_error"]))

    limitations = [
        "Report status is not_run because this reporting layer did not execute the research task; worker status is retained only as an unverified declaration.",
        "Assignment binding does not prove that a worker was dispatched or received the package.",
        "Evidence integrity means only that supplied bytes match the supplied commit manifest; the caller must independently authenticate checkout, commit, and manifest.",
        "Evidence integrity does not establish research correctness, completeness, source truth, or whether findings support a research conclusion.",
        "Repository, branch, commit, run ID, timestamp, input manifest, and checkout-clean assertion are caller-supplied until independently authenticated by the workflow.",
        "Only a human may accept task completion or close a phase gate.",
    ]
    limitations.extend(_as_text(item) for item in review.get("limitations", []))
    limitations.extend(_as_text(item) for item in supervisor.get("limitations", []))
    skipped_checks = [
        "No task execution, dispatch, delivery, queue mutation, filesystem write, artifact upload, or workflow operation was performed by this module.",
        "No research correctness assessment, candidate generation, backtest, PnL analysis, strategy selection, or gate-closure decision was performed.",
        "Human review and independent workflow-provenance verification remain outstanding.",
    ]
    report = {
        "schema_version": 1, "agent_name": "okx-research-agent",
        "task_id": trusted_task["task_id"], "phase": trusted_task["phase"],
        "status": "not_run", "repository": repository, "branch": branch,
        "commit_sha": commit_sha, "task_definition_sha256": task_definition_digest(trusted_task),
        "run_id": run_id, "timestamp_utc": timestamp_utc, "input_manifest": input_manifest,
        "findings": findings, "blockers": blockers, "skipped_checks": skipped_checks,
        "limitations": list(dict.fromkeys(limitations)),
    }
    bundle = build_artifact_bundle(
        report, trusted_task, expected_repository=repository, expected_branch=branch,
        expected_commit_sha=commit_sha, actual_head_sha=actual_head_sha,
        checkout_clean=checkout_clean, run_id=run_id, run_attempt=run_attempt,
    )
    return {
        "mode": "assignment_review_artifact_only", "task_id": trusted_task["task_id"],
        "assignment_binding_verified": True, "dispatch_or_delivery_verified": False,
        "review_disposition": supervisor["review_disposition"],
        "evidence_integrity_passed": supervisor.get("evidence_integrity_passed") is True,
        "report_status": report["status"], "task_completion_approved": False,
        "gate_closure_approved": False, "human_review_required": True,
        "task_execution_performed": False, "filesystem_writes_performed": False,
        "artifact_upload_performed": False, "review": review, "bundle": bundle,
    }
