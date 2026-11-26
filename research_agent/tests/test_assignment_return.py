"""Assignment-bound return-review tests; authored, not executed."""
import hashlib
import unittest

from research_agent.engine.assignment_package import assignment_package_digest, prepare_worker_assignment
from research_agent.engine.assignment_return import review_assignment_return
from research_agent.engine.report_builder import task_definition_digest


class AssignmentReturnTests(unittest.TestCase):
    def setUp(self):
        self.task = {
            "task_id": "P3-G005-RO-001",
            "phase": "phase3_sideways_range",
            "operation": "evidence_lineage_review",
            "title": "Read-only reconciliation",
            "status": "queued",
            "handoff_id": "PHASE3_G0_05_RECONCILIATION_TASK_02",
            "scope": ["Inspect existing evidence only"],
            "prohibited": ["execute_scripts", "execute_tests", "trigger_workflows",
                           "modify_code", "modify_research_data", "create_candidates",
                           "run_backtests", "make_pnl_claims", "select_strategies", "close_gates"],
            "completion_authority": "human_only",
        }
        self.preflight = {
            "task_id": self.task["task_id"], "queue_status": "queued",
            "decision": "ALLOW_READ_ONLY", "authorized": True,
            "reason": "Synthetic allowed preflight for unit coverage.",
            "execution_performed": False, "mode": "preflight_only",
        }
        digest = task_definition_digest(self.task)
        plan = {
            "task_id": self.task["task_id"], "phase": self.task["phase"],
            "operation": self.task["operation"], "title": self.task["title"],
            "handoff_id": self.task["handoff_id"], "scope": list(self.task["scope"]),
            "prohibited": list(self.task["prohibited"]),
            "task_definition_sha256": digest,
            "assignment_status": "preflight_allowed_not_executed",
            "completion_authority": "human_only",
        }
        self.package = prepare_worker_assignment(
            self.task, self.preflight, planned_assignment=plan
        )
        self.package_digest = assignment_package_digest(self.package)
        self.commit = "1" * 40
        self.path = "docs/assistant_handoff/evidence.md"
        self.content = b"Evidence bytes from expected commit.\n"
        file_hash = hashlib.sha256(self.content).hexdigest()
        self.manifest = {"commit_sha": self.commit, "files": {self.path: file_hash}}
        self.submission = {
            "schema_version": 1, "task_id": self.task["task_id"],
            "phase": self.task["phase"], "operation": self.task["operation"],
            "task_definition_sha256": digest, "status": "completed",
            "summary": "Reviewed the source lineage.",
            "findings": ["Source mapping is documented."],
            "evidence": [{"path": self.path, "sha256": file_hash,
                          "source_ref": self.commit, "description": "Evidence"}],
            "actions_performed": ["read_existing_documentation"],
            "limitations": ["Human review remains required."],
            "completion_claimed": True, "gate_closure_claimed": False,
        }

    def review(self, package=None, package_digest=None):
        selected_package = self.package if package is None else package
        trusted_digest = self.package_digest if package_digest is None else package_digest
        return review_assignment_return(
            self.task, selected_package, self.submission,
            expected_assignment_package_sha256=trusted_digest,
            expected_commit_sha=self.commit, commit_manifest=self.manifest,
            file_contents={self.path: self.content},
        )

    def test_valid_return_is_bound_but_still_human_review_only(self):
        result = self.review()
        self.assertTrue(result["assignment_binding_verified"])
        self.assertFalse(result["dispatch_or_delivery_verified"])
        self.assertTrue(result["submission_review"]["evidence_integrity_passed"])
        self.assertFalse(result["task_completion_approved"])
        self.assertFalse(result["gate_closure_approved"])

    def test_blocked_preflight_package_cannot_accept_worker_return(self):
        blocked_preflight = dict(self.preflight, decision="DENY", authorized=False)
        blocked = prepare_worker_assignment(self.task, blocked_preflight)
        with self.assertRaisesRegex(ValueError, "prepared, non-blocked"):
            self.review(blocked, package_digest=assignment_package_digest(blocked))

    def test_tampered_preflight_reason_is_rejected_by_trusted_package_digest(self):
        tampered = dict(self.package)
        tampered["preflight"] = dict(self.package["preflight"], reason="Forged reason")
        with self.assertRaisesRegex(ValueError, "trusted prepared-package digest"):
            self.review(tampered)

    def test_tampered_scope_is_rejected_before_submission_review(self):
        tampered = dict(self.package)
        tampered["scope"] = ["Expanded scope"]
        with self.assertRaisesRegex(ValueError, "canonical trusted package"):
            self.review(tampered)

    def test_tampered_digest_is_rejected(self):
        tampered = dict(self.package, task_definition_sha256="0" * 64)
        with self.assertRaisesRegex(ValueError, "canonical trusted package"):
            self.review(tampered)

    def test_tampered_worker_action_allowlist_is_rejected(self):
        tampered = dict(self.package)
        tampered["allowed_declared_actions"] = ["run_backtests"]
        with self.assertRaisesRegex(ValueError, "canonical trusted package"):
            self.review(tampered)

    def test_tampered_submission_schema_is_rejected(self):
        tampered = dict(self.package)
        tampered["worker_submission_schema"] = {"required_fields": []}
        with self.assertRaisesRegex(ValueError, "canonical trusted package"):
            self.review(tampered)

    def test_boolean_schema_version_is_not_accepted_as_integer_one(self):
        tampered = dict(self.package, schema_version=True)
        with self.assertRaisesRegex(ValueError, "schema version"):
            self.review(tampered)

    def test_dispatch_claim_is_rejected(self):
        tampered = dict(self.package, dispatch_permitted=True)
        with self.assertRaisesRegex(ValueError, "dispatch permission"):
            self.review(tampered)


if __name__ == "__main__":
    unittest.main()
