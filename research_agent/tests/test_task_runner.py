"""Read-only preflight dispatcher tests; authored but not executed."""
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from research_agent.engine import task_runner


class TaskRunnerTests(unittest.TestCase):
    def test_load_queue_rejects_duplicate_json_object_keys(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "queue.json"
            path.write_text(
                '{"schema_version":1,"schema_version":1,"tasks":[]}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Duplicate JSON object key"):
                task_runner.load_queue(path)

    def test_load_queue_rejects_nonstandard_json_constants(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "queue.json"
            path.write_text(
                '{"schema_version":NaN,"tasks":[]}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Non-standard JSON"):
                task_runner.load_queue(path)

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

    def test_rejects_allow_result_without_a_reason(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        incomplete = {"decision": "ALLOW_READ_ONLY", "authorized": True, "reason": ""}
        with patch.object(task_runner, "authorize_task", return_value=incomplete):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])

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

    def test_rejects_authorizer_response_with_extra_fields(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        response = {
            "decision": "ALLOW_READ_ONLY", "authorized": True,
            "reason": "looks valid", "execution_performed": True,
        }
        with patch.object(task_runner, "authorize_task", return_value=response):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])

    def test_rejects_authorizer_response_with_missing_fields(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        response = {"decision": "ALLOW_READ_ONLY", "authorized": True}
        with patch.object(task_runner, "authorize_task", return_value=response):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")

    def test_rejects_non_boolean_authorized_flag(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        response = {"decision": "ALLOW_READ_ONLY", "authorized": 1, "reason": "truthy"}
        with patch.object(task_runner, "authorize_task", return_value=response):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")

    def test_rejects_non_string_authorizer_decision_without_raising(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        response = {"decision": ["ALLOW_READ_ONLY"], "authorized": True, "reason": "bad type"}
        with patch.object(task_runner, "authorize_task", return_value=response):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])

    def test_rejects_unknown_authorizer_decision(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        response = {"decision": "ALLOW", "authorized": True, "reason": "unknown"}
        with patch.object(task_runner, "authorize_task", return_value=response):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")

    def test_rejects_authorized_flag_conflicting_with_deny_code(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        response = {"decision": "DENY", "authorized": True, "reason": "conflict"}
        with patch.object(task_runner, "authorize_task", return_value=response):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])

    def test_accepts_exact_identity_bound_allow_response(self):
        task = {
            "task_id": "P3-RO-001", "status": "queued",
            "phase": "phase3_sideways_range", "operation": "repository_inspection",
        }
        response = {
            "authorized": True, "decision": "ALLOW_READ_ONLY",
            "reason": "exact approved task", "task_id": task["task_id"],
            "phase": task["phase"], "operation": task["operation"],
            "execution_performed": False,
        }
        with patch.object(task_runner, "authorize_task", return_value=response):
            result = task_runner._preflight_task_with_queue("P3-RO-001", {"tasks": [task]})
        self.assertEqual(result["decision"], "ALLOW_READ_ONLY")
        self.assertTrue(result["authorized"])
        self.assertFalse(result["execution_performed"])

    def test_rejects_allow_response_with_wrong_task_identity(self):
        task = {
            "task_id": "P3-RO-001", "status": "queued",
            "phase": "phase3_sideways_range", "operation": "repository_inspection",
        }
        response = {
            "authorized": True, "decision": "ALLOW_READ_ONLY",
            "reason": "wrong task", "task_id": "P3-RO-999",
            "phase": task["phase"], "operation": task["operation"],
            "execution_performed": False,
        }
        with patch.object(task_runner, "authorize_task", return_value=response):
            result = task_runner._preflight_task_with_queue("P3-RO-001", {"tasks": [task]})
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


    def test_queue_load_failure_returns_stable_preflight_envelope(self):
        with patch.object(task_runner, "load_queue", side_effect=ValueError("bad queue")):
            result = task_runner.preflight_task("P3-RO-001")
        self.assertEqual(
            set(result),
            {"task_id", "queue_status", "decision", "authorized", "reason",
             "execution_performed", "mode"},
        )
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["mode"], "preflight_only")

    def test_authorizer_exception_returns_stable_denial(self):
        queue = {"tasks": [{"task_id": "P3-RO-001", "status": "queued"}]}
        with patch.object(task_runner, "authorize_task", side_effect=RuntimeError("boom")):
            result = task_runner._preflight_task_with_queue("P3-RO-001", queue)
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertIn("failed unexpectedly", result["reason"])


    def test_preflight_all_tasks_with_queue_uses_one_supplied_snapshot(self):
        queue = {
            "tasks": [
                {"task_id": "P3-RO-001", "status": "queued"},
                {"task_id": "P1-RO-001", "status": "blocked"},
            ]
        }
        per_task = [
            {"task_id": "P3-RO-001", "authorized": False, "execution_performed": False},
            {"task_id": "P1-RO-001", "authorized": False, "execution_performed": False},
        ]
        with patch.object(task_runner, "load_queue", side_effect=AssertionError("must not reload")), patch.object(
            task_runner, "_preflight_task_with_queue", side_effect=per_task
        ) as preflight:
            result = task_runner._preflight_all_tasks_with_queue(queue)
        self.assertEqual(result["decision"], "SUMMARY_ONLY")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["task_count"], 2)
        self.assertEqual(preflight.call_count, 2)
        self.assertIs(preflight.call_args_list[0].args[1], queue)
        self.assertIs(preflight.call_args_list[1].args[1], queue)

    def test_preflight_all_tasks_is_summary_only_and_never_authorizes_queue(self):
        queue = {
            "tasks": [
                {"task_id": "P3-RO-001", "status": "queued"},
                {"task_id": "P1-RO-001", "status": "blocked"},
            ]
        }
        per_task = [
            {"task_id": "P3-RO-001", "authorized": False, "execution_performed": False},
            {"task_id": "P1-RO-001", "authorized": False, "execution_performed": False},
        ]
        with patch.object(task_runner, "load_queue", return_value=queue), patch.object(
            task_runner, "_preflight_task_with_queue", side_effect=per_task
        ) as preflight:
            result = task_runner.preflight_all_tasks()
        self.assertEqual(result["decision"], "SUMMARY_ONLY")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["task_count"], 2)
        self.assertEqual(result["allow_count"], 0)
        self.assertEqual(result["deny_count"], 2)
        self.assertEqual(len(result["tasks"]), 2)
        self.assertEqual(preflight.call_count, 2)

    def test_preflight_all_tasks_fails_closed_on_malformed_rows(self):
        with patch.object(
            task_runner, "load_queue",
            return_value={"tasks": [{"task_id": "P3-RO-001"}, "malformed"]},
        ):
            result = task_runner.preflight_all_tasks()
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["tasks"], [])

    def test_preflight_all_tasks_reports_queue_load_failure(self):
        with patch.object(task_runner, "load_queue", side_effect=OSError("missing")):
            result = task_runner.preflight_all_tasks()
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["task_count"], 0)
        self.assertEqual(result["tasks"], [])



    def test_cli_all_mode_emits_summary_without_authorizing_queue(self):
        summary = {
            "decision": "SUMMARY_ONLY", "authorized": False,
            "execution_performed": False, "tasks": [],
        }
        with patch("sys.argv", ["task_runner", "--all"]), patch.object(
            task_runner, "preflight_all_tasks", return_value=summary
        ) as preflight, patch("builtins.print"):
            exit_code = task_runner.main()
        self.assertEqual(exit_code, 0)
        preflight.assert_called_once_with()

    def test_cli_requires_exactly_one_selection_mode(self):
        with patch("sys.argv", ["task_runner"]), self.assertRaises(SystemExit):
            task_runner.main()
        with patch("sys.argv", ["task_runner", "--all", "--task-id", "P3-RO-001"]), self.assertRaises(SystemExit):
            task_runner.main()


if __name__ == "__main__":
    unittest.main()
