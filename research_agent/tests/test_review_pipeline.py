"""Integrated review-pipeline tests; authored, not executed."""
import hashlib
import unittest

from research_agent.engine.report_builder import task_definition_digest
from research_agent.engine.review_pipeline import review_submission_with_verified_evidence


class IntegratedReviewPipelineTests(unittest.TestCase):
    def setUp(self):
        self.task = {
            "task_id": "P3-G005-RO-001",
            "phase": "phase3_sideways_range",
            "operation": "evidence_lineage_review",
            "title": "Read-only reconciliation",
            "status": "queued",
            "workstream": "g0_05",
            "handoff_id": "PHASE3_G0_05_RECONCILIATION_TASK_02",
            "scope": ["Inspect existing evidence only"],
            "prohibited": ["execute_scripts", "execute_tests", "trigger_workflows",
                           "modify_code", "modify_research_data", "create_candidates",
                           "run_backtests", "make_pnl_claims", "select_strategies", "close_gates"],
            "completion_authority": "human_only",
        }
        self.commit = "1" * 40
        self.path = "docs/assistant_handoff/evidence.md"
        self.content = b"Evidence bytes from the expected commit.\n"
        self.digest = hashlib.sha256(self.content).hexdigest()
        self.manifest = {"commit_sha": self.commit, "files": {self.path: self.digest}}
        self.submission = {
            "schema_version": 1,
            "task_id": self.task["task_id"],
            "phase": self.task["phase"],
            "operation": self.task["operation"],
            "task_definition_sha256": task_definition_digest(self.task),
            "status": "completed",
            "summary": "Reviewed the evidence lineage.",
            "findings": ["The source reference is documented."],
            "evidence": [{"path": self.path, "sha256": self.digest,
                          "source_ref": self.commit, "description": "Source evidence"}],
            "actions_performed": ["read_existing_documentation"],
            "limitations": ["Integrity does not prove research correctness."],
            "completion_claimed": True,
            "gate_closure_claimed": False,
        }

    def run_review(self, submission=None, manifest=None, contents=None):
        return review_submission_with_verified_evidence(
            self.task, self.submission if submission is None else submission,
            expected_commit_sha=self.commit,
            commit_manifest=self.manifest if manifest is None else manifest,
            file_contents={self.path: self.content} if contents is None else contents,
        )

    def test_valid_submission_and_bytes_remain_human_review_only(self):
        result = self.run_review()
        self.assertTrue(result["evidence_integrity_passed"])
        self.assertEqual(result["review_disposition"], "ready_for_human_review")
        self.assertFalse(result["task_completion_approved"])
        self.assertFalse(result["gate_closure_approved"])
        self.assertTrue(result["human_review_required"])

    def test_hash_mismatch_returns_submission_for_revision(self):
        bad = dict(self.submission)
        bad["evidence"] = [dict(self.submission["evidence"][0], sha256="a" * 64)]
        result = self.run_review(submission=bad)
        self.assertFalse(result["evidence_integrity_passed"])
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_checkout_byte_mismatch_returns_submission_for_revision(self):
        result = self.run_review(contents={self.path: b"tampered"})
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_manifest_commit_mismatch_fails_closed(self):
        result = self.run_review(
            manifest={"commit_sha": "2" * 40, "files": {self.path: self.digest}}
        )
        self.assertEqual(result["review_disposition"], "return_for_revision")
        self.assertFalse(result["evidence_integrity_passed"])
        self.assertIn("verification_error", result["evidence_verification"])
        self.assertFalse(result["task_completion_approved"])

    def test_structural_safety_failure_skips_evidence_verification(self):
        bad = dict(self.submission, gate_closure_claimed=True)
        result = self.run_review(submission=bad)
        self.assertEqual(result["review_disposition"], "rejected_safety_violation")
        self.assertIsNone(result["evidence_verification"])
        self.assertFalse(result["task_completion_approved"])

    def test_empty_evidence_cannot_pass_integrity_gate(self):
        bad = dict(self.submission, status="partial", completion_claimed=False, evidence=[])
        result = self.run_review(submission=bad)
        self.assertFalse(result["evidence_integrity_passed"])
        self.assertEqual(result["evidence_verification"]["evidence_count"], 0)


if __name__ == "__main__":
    unittest.main()
