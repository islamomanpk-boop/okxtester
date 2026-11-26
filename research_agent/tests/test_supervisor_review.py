"""Supervisor review gate tests; authored, not executed."""
import unittest

from research_agent.engine.report_builder import task_definition_digest
from research_agent.engine.supervisor_review import review_worker_submission


class SupervisorReviewTests(unittest.TestCase):
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
        self.submission = {
            "schema_version": 1,
            "task_id": self.task["task_id"],
            "phase": self.task["phase"],
            "operation": self.task["operation"],
            "task_definition_sha256": task_definition_digest(self.task),
            "status": "completed",
            "summary": "Inspected source mapping and recorded the unresolved edge case.",
            "findings": ["Canonical confirmation status requires additional reconciliation."],
            "evidence": [{
                "path": "docs/assistant_handoff/PHASE3_G0_05_RECONCILIATION_TASK_02.md",
                "sha256": "a" * 64,
                "source_ref": "1e37eabee8dd17a206e4e848c421096d89482ddd",
                "description": "Authoritative handoff",
            }],
            "actions_performed": ["read_existing_documentation"],
            "limitations": ["Evidence bytes require independent verification."],
            "completion_claimed": True,
            "gate_closure_claimed": False,
        }

    def test_valid_submission_is_only_ready_for_human_review(self):
        result = review_worker_submission(self.task, self.submission)
        self.assertEqual(result["review_disposition"], "ready_for_human_review")
        self.assertTrue(result["human_review_required"])
        self.assertFalse(result["task_completion_approved"])
        self.assertFalse(result["evidence_content_verified"])

    def test_rejects_prohibited_action_declaration(self):
        submission = dict(self.submission, actions_performed=["execute_tests"])
        result = review_worker_submission(self.task, submission)
        self.assertEqual(result["review_disposition"], "rejected_safety_violation")
        self.assertIn("execute_tests", result["safety_violations"])

    def test_rejects_gate_closure_claim(self):
        submission = dict(self.submission, gate_closure_claimed=True)
        result = review_worker_submission(self.task, submission)
        self.assertEqual(result["review_disposition"], "rejected_safety_violation")

    def test_returns_submission_with_missing_evidence_for_revision(self):
        submission = dict(self.submission, evidence=[])
        result = review_worker_submission(self.task, submission)
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_rejects_task_digest_mismatch(self):
        submission = dict(self.submission, task_definition_sha256="b" * 64)
        result = review_worker_submission(self.task, submission)
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_rejects_unsafe_evidence_path(self):
        evidence = [dict(self.submission["evidence"][0], path="../outside.txt")]
        result = review_worker_submission(self.task, dict(self.submission, evidence=evidence))
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_rejects_invalid_evidence_digest(self):
        evidence = [dict(self.submission["evidence"][0], sha256="not-a-hash")]
        result = review_worker_submission(self.task, dict(self.submission, evidence=evidence))
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_blocks_without_explained_limitations(self):
        submission = dict(self.submission, status="blocked", completion_claimed=False,
                          limitations=[])
        result = review_worker_submission(self.task, submission)
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_does_not_accept_unknown_fields(self):
        submission = dict(self.submission, automatic_approval=True)
        result = review_worker_submission(self.task, submission)
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_task_identity_must_match(self):
        submission = dict(self.submission, task_id="P1-RO-001")
        result = review_worker_submission(self.task, submission)
        self.assertEqual(result["review_disposition"], "return_for_revision")

    def test_unhashable_status_is_rejected_without_exception(self):
        submission = dict(self.submission, status=["completed"])
        result = review_worker_submission(self.task, submission)
        self.assertEqual(result["review_disposition"], "return_for_revision")


if __name__ == "__main__":
    unittest.main()
