"""Tests for preflight artifact orchestration; authored, not executed."""
import unittest
from unittest.mock import patch

from research_agent.engine import artifact_preparation


class ArtifactPreparationTests(unittest.TestCase):
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
            "prohibited": [
                "execute_scripts", "execute_tests", "trigger_workflows",
                "modify_code", "modify_research_data", "create_candidates",
                "run_backtests", "make_pnl_claims", "select_strategies", "close_gates",
            ],
            "completion_authority": "human_only",
        }
        self.queue = {"tasks": [self.task]}
        self.context = {
            "repository": artifact_preparation.EXPECTED_REPOSITORY,
            "branch": artifact_preparation.EXPECTED_BRANCH,
            "commit_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "checkout_clean": True,
            "run_id": "12345",
            "run_attempt": "1",
            "timestamp_utc": "2026-11-26T12:00:00Z",
        }

    def prepare(self, **overrides):
        context = dict(self.context)
        context.update(overrides)
        with patch.object(artifact_preparation, "load_queue", return_value=self.queue):
            with patch.object(
                artifact_preparation, "_preflight_task_with_queue",
                return_value={
                    "task_id": self.task["task_id"], "queue_status": "queued",
                    "decision": "DENY", "authorized": False,
                    "reason": "Active G0-05 handoff lock; denied.",
                    "execution_performed": False, "mode": "preflight_only",
                },
            ):
                return artifact_preparation.prepare_task_artifact(
                    self.task["task_id"], **context
                )

    def test_prepares_blocked_bundle_without_execution_or_writes(self):
        result = self.prepare()
        self.assertEqual(result["report_status"], "blocked")
        self.assertFalse(result["execution_performed"])
        self.assertFalse(result["filesystem_writes_performed"])
        self.assertFalse(result["artifact_upload_performed"])
        self.assertEqual(
            set(result["bundle"]["files"]),
            {"report.json", "report.md", "artifact_manifest.json"},
        )

    def test_rejects_non_agent_branch(self):
        with self.assertRaisesRegex(ValueError, "isolated agent branch"):
            self.prepare(branch="price-action-v1")

    def test_rejects_wrong_repository(self):
        with self.assertRaisesRegex(ValueError, "research repository"):
            self.prepare(repository="someone/else")

    def test_rejects_dirty_checkout(self):
        with self.assertRaisesRegex(ValueError, "clean"):
            self.prepare(checkout_clean=False)

    def test_rejects_head_commit_mismatch(self):
        with self.assertRaisesRegex(ValueError, "HEAD"):
            self.prepare(actual_head_sha="b" * 40)

    def test_rejects_duplicate_task_identity(self):
        duplicate = dict(self.task)
        with patch.object(
            artifact_preparation, "load_queue",
            return_value={"tasks": [self.task, duplicate]},
        ):
            with self.assertRaisesRegex(ValueError, "exactly one"):
                artifact_preparation.prepare_task_artifact(
                    self.task["task_id"], **self.context
                )

    def test_rejects_unknown_task(self):
        with patch.object(
            artifact_preparation, "load_queue", return_value=self.queue
        ):
            with self.assertRaisesRegex(ValueError, "exactly one"):
                artifact_preparation.prepare_task_artifact(
                    "UNKNOWN", **self.context
                )


if __name__ == "__main__":
    unittest.main()
