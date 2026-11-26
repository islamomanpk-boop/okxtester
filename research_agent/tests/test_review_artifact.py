"""Assignment review artifact integration tests; authored, not executed."""
import hashlib
import unittest
from unittest.mock import patch
from research_agent.engine import review_artifact
from research_agent.engine.assignment_package import assignment_package_digest, prepare_worker_assignment
from research_agent.engine.report_builder import task_definition_digest

class ReviewArtifactTests(unittest.TestCase):
    def setUp(self):
        self.task = {
            "task_id": "P3-G005-RO-001", "phase": "phase3_sideways_range",
            "operation": "evidence_lineage_review", "title": "Read-only reconciliation",
            "status": "queued", "handoff_id": "PHASE3_G0_05_RECONCILIATION_TASK_02",
            "scope": ["Inspect existing evidence only"],
            "prohibited": ["execute_scripts", "execute_tests", "trigger_workflows",
                "modify_code", "modify_research_data", "create_candidates",
                "run_backtests", "make_pnl_claims", "select_strategies", "close_gates"],
            "completion_authority": "human_only",
        }
        digest = task_definition_digest(self.task)
        preflight = {"task_id": self.task["task_id"], "queue_status": "queued",
            "decision": "ALLOW_READ_ONLY", "authorized": True,
            "reason": "Synthetic preflight fixture.", "execution_performed": False,
            "mode": "preflight_only"}
        plan = {"task_id": self.task["task_id"], "phase": self.task["phase"],
            "operation": self.task["operation"], "title": self.task["title"],
            "handoff_id": self.task["handoff_id"], "scope": list(self.task["scope"]),
            "prohibited": list(self.task["prohibited"]), "task_definition_sha256": digest,
            "assignment_status": "preflight_allowed_not_executed", "completion_authority": "human_only"}
        self.package = prepare_worker_assignment(self.task, preflight, planned_assignment=plan)
        self.package_digest = assignment_package_digest(self.package)
        self.commit = "1" * 40
        self.path = "docs/assistant_handoff/source.md"
        self.content = b"Source evidence fixture.\\n"
        file_hash = hashlib.sha256(self.content).hexdigest()
        self.manifest = {"commit_sha": self.commit, "files": {self.path: file_hash}}
        self.submission = {"schema_version": 1, "task_id": self.task["task_id"],
            "phase": self.task["phase"], "operation": self.task["operation"],
            "task_definition_sha256": digest, "status": "completed",
            "summary": "Worker says reconciliation is complete.",
            "findings": ["Worker says source mapping is documented."],
            "evidence": [{"path": self.path, "sha256": file_hash,
                "source_ref": self.commit, "description": "Source fixture"}],
            "actions_performed": ["read_existing_documentation"],
            "limitations": ["Human review remains required."],
            "completion_claimed": True, "gate_closure_claimed": False}
        self.context = {"expected_assignment_package_sha256": self.package_digest,
            "expected_commit_sha": self.commit, "commit_manifest": self.manifest,
            "file_contents": {self.path: self.content},
            "repository": review_artifact.EXPECTED_REPOSITORY,
            "branch": review_artifact.EXPECTED_BRANCH, "commit_sha": self.commit,
            "actual_head_sha": self.commit, "checkout_clean": True, "run_id": "12345",
            "run_attempt": "1", "timestamp_utc": "2026-11-26T12:00:00Z", "input_manifest": []}

    def build(self, submission=None, **overrides):
        context = dict(self.context)
        context.update(overrides)
        captured = {}
        def bundle(report, trusted_task, **kwargs):
            captured["report"] = report
            return {"artifact_name": "fixture", "files": {
                "report.json": "{}", "report.md": "md", "artifact_manifest.json": "{}"}, "manifest": {}}
        with patch.object(review_artifact, "build_artifact_bundle", side_effect=bundle):
            result = review_artifact.build_assignment_review_artifact(
                self.task, self.package, self.submission if submission is None else submission, **context)
        return result, captured["report"]

    def test_worker_completion_claim_remains_not_run_and_human_only(self):
        result, report = self.build()
        self.assertEqual(result["report_status"], "not_run")
        self.assertEqual(report["status"], "not_run")
        self.assertEqual(result["review_disposition"], "ready_for_human_review")
        self.assertFalse(result["task_completion_approved"])
        self.assertFalse(result["gate_closure_approved"])
        self.assertTrue(result["human_review_required"])
        self.assertTrue(any("Worker-declared finding" in item for item in report["findings"]))

    def test_evidence_hash_failure_is_recorded_as_blocker(self):
        bad = dict(self.submission)
        bad["evidence"] = [dict(self.submission["evidence"][0], sha256="0" * 64)]
        result, report = self.build(bad)
        self.assertFalse(result["evidence_integrity_passed"])
        self.assertTrue(any("Evidence integrity issue" in item for item in report["blockers"]))
        self.assertEqual(report["status"], "not_run")

    def test_assignment_scope_tampering_is_rejected_before_bundle(self):
        package = dict(self.package, scope=["Expanded"])
        with patch.object(review_artifact, "build_artifact_bundle") as builder:
            with self.assertRaisesRegex(ValueError, "scope"):
                review_artifact.build_assignment_review_artifact(
                    self.task, package, self.submission, **self.context)
            builder.assert_not_called()

    def test_rejects_wrong_repository_or_branch(self):
        with self.assertRaisesRegex(ValueError, "research repository"):
            self.build(repository="other/repo")
        with self.assertRaisesRegex(ValueError, "isolated agent branch"):
            self.build(branch="price-action-v1")

    def test_rejects_mismatched_evidence_and_report_commit(self):
        with self.assertRaisesRegex(ValueError, "evidence-review commit"):
            self.build(commit_sha="2" * 40)

    def test_never_claims_dispatch_or_upload(self):
        result, _ = self.build()
        self.assertFalse(result["dispatch_or_delivery_verified"])
        self.assertFalse(result["artifact_upload_performed"])
        self.assertFalse(result["task_execution_performed"])

if __name__ == "__main__":
    unittest.main()
