"""Read-only preflight dispatcher tests; authored but not executed."""
import unittest
from unittest.mock import patch

from research_agent.engine import task_runner


class TaskRunnerTests(unittest.TestCase):
    def test_rejects_non_object_queue_without_raising(self):
        result = task_runner._preflight_task_with_queue("P3-RO-001", [])
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("JSON object", result["reason"])

    def test_rejects_malformed_task_list(self):
        result = task_runner._preflight_task_with_queue("P3-RO-001", {"tasks": "not-a-list"})
        self.assertEqual(result["decision"], "DENY")

    def test_rejects_duplicate_task_ids(self):
        task = {"task_id": "P3-RO-001", "status": "queued"}
        result = task_runner._preflight_task_with_queue(
            "P3-RO-001", {"tasks": [task, dict(task)]}
        )
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("exactly one", result["reason"])

    def test_public_preflight_rejects_caller_supplied_queue(self):
        with self.assertRaises(TypeError):
            task_runner.preflight_task("P3-RO-001", queue={"tasks": []})

    def test_every_denial_has_stable_preflight_envelope(self):
        result = task_runner._preflight_task_with_queue("P3-RO-001", {"tasks": "bad"})
        self.assertEqual(
            set(result),
            {"task_id", "queue_status", "decision", "authorized", "reason",
             "execution_performed", "mode"},
        )
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["mode"], "preflight_only")

    def test_rejects_non_object_rows_instead_of_filtering_them(self):
        result = task_runner._preflight_task_with_queue(
            "P3-RO-001", {"tasks": [{"task_id": "P3-RO-001"}, "malformed"]}
        )
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("Every task queue entry", result["reason"])

    def test_rejects_malformed_authorizer_result(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        with patch.object(task_runner, "authorize_task", return_value=None):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])

    def test_does_not_trust_inconsistent_authorizer_decision(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        inconsistent = {
            "decision": "ALLOW_READ_ONLY",
            "authorized": False,
            "reason": "inconsistent test fixture",
        }
        with patch.object(task_runner, "authorize_task", return_value=inconsistent):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])

    def test_preflight_never_invokes_executor(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        with patch.object(
            task_runner, "authorize_task",
            return_value={"decision": "DENY", "authorized": False, "reason": "test"},
        ) as authorize:
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        authorize.assert_called_once()
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["mode"], "preflight_only")


if __name__ == "__main__":
    unittest.main()
