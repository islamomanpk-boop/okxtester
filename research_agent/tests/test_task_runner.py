"""Read-only preflight dispatcher tests; authored but not executed."""
import unittest
from unittest.mock import patch

from research_agent.engine import task_runner


class TaskRunnerTests(unittest.TestCase):
    def test_rejects_non_object_queue_without_raising(self):
        result = task_runner.preflight_task("P3-RO-001", queue=[])
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("JSON object", result["reason"])

    def test_rejects_malformed_task_list(self):
        result = task_runner.preflight_task("P3-RO-001", queue={"tasks": "not-a-list"})
        self.assertEqual(result["decision"], "DENY")

    def test_rejects_duplicate_task_ids(self):
        task = {"task_id": "P3-RO-001", "status": "queued"}
        result = task_runner.preflight_task(
            "P3-RO-001", queue={"tasks": [task, dict(task)]}
        )
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("exactly one", result["reason"])

    def test_preflight_never_invokes_executor(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        with patch.object(
            task_runner, "authorize_task",
            return_value={"decision": "DENY", "authorized": False, "reason": "test"},
        ) as authorize:
            result = task_runner.preflight_task("P3-RO-001", queue=queue)
        authorize.assert_called_once()
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["mode"], "preflight_only")


if __name__ == "__main__":
    unittest.main()
