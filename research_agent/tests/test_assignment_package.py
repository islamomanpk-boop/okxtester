"""Worker assignment package tests; authored but not executed."""
import unittest

from research_agent.engine.assignment_package import prepare_worker_assignment
from research_agent.engine.batch_planner import build_batch_plan, EXPECTED_PHASE_ORDER
from research_agent.engine.report_builder import task_definition_digest


def make_task():
    return {
        "task_id": "P3-G005-RO-001",
        "phase": EXPECTED_PHASE_ORDER[0],
        "operation": "evidence_lineage_review",
        "title": "Read-only lineage review",
        "status": "queued",
        "handoff_id": "PHASE3_G0_05_RECONCILIATION_TASK_02",
        "scope": ["Inspect existing evidence only", "Record unresolved mappings"],
        "prohibited": ["execute_scripts", "execute_tests", "trigger_workflows",
                       "modify_code", "modify_research_data", "create_candidates",
                       "run_backtests", "make_pnl_claims", "select_strategies", "close_gates"],
        "completion_authority": "human_only",
    }


def preflight(task, allowed=False):
    return {
        "task_id": task["task_id"],
        "queue_status": "queued",
        "decision": "ALLOW_READ_ONLY" if allowed else "DENY",
        "authorized": allowed,
        "reason": "Synthetic test preflight outcome.",
        "execution_performed": False,
        "mode": "preflight_only",
    }


def plan_entry(task):
    return {
        "task_id": task["task_id"],
        "phase": task["phase"],
        "operation": task["operation"],
        "title": task["title"],
        "handoff_id": task["handoff_id"],
        "scope": list(task["scope"]),
        "prohibited": list(task["prohibited"]),
        "task_definition_sha256": task_definition_digest(task),
        "assignment_status": "preflight_allowed_not_executed",
        "completion_authority": "human_only",
    }


class WorkerAssignmentPackageTests(unittest.TestCase):
    def test_denied_g005_preflight_creates_blocked_non_dispatchable_package(self):
        task = make_task()
        result = prepare_worker_assignment(task, preflight(task))
        self.assertEqual(result["assignment_status"], "blocked_preflight")
        self.assertFalse(result["dispatch_permitted"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["handoff_id"], task["handoff_id"])

    def test_allowed_preflight_still_does_not_dispatch(self):
        task = make_task()
        result = prepare_worker_assignment(
            task, preflight(task, True), planned_assignment=plan_entry(task)
        )
        self.assertEqual(result["assignment_status"], "prepared_not_dispatched")
        self.assertFalse(result["dispatch_permitted"])
        self.assertFalse(result["task_completion_approved"])

    def test_rejects_task_digest_mismatch_in_plan(self):
        task = make_task()
        entry = plan_entry(task)
        entry["task_definition_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "exactly match"):
            prepare_worker_assignment(task, preflight(task, True), planned_assignment=entry)

    def test_rejects_wrong_task_identity(self):
        task = make_task()
        result = preflight(task)
        result["task_id"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "exact task"):
            prepare_worker_assignment(task, result)

    def test_rejects_modified_scope_or_prohibitions(self):
        task = make_task()
        entry = plan_entry(task)
        entry["scope"] = ["Expanded scope"]
        with self.assertRaisesRegex(ValueError, "exactly match"):
            prepare_worker_assignment(task, preflight(task, True), planned_assignment=entry)
        entry = plan_entry(task)
        entry["prohibited"] = []
        with self.assertRaisesRegex(ValueError, "exactly match"):
            prepare_worker_assignment(task, preflight(task, True), planned_assignment=entry)

    def test_rejects_unknown_preflight_fields(self):
        task = make_task()
        result = preflight(task)
        result["dispatch"] = True
        with self.assertRaisesRegex(ValueError, "unsupported fields"):
            prepare_worker_assignment(task, result)

    def test_rejects_non_queued_preflight_status(self):
        task = make_task()
        result = preflight(task, True)
        result["queue_status"] = "completed"
        with self.assertRaisesRegex(ValueError, "exact task"):
            prepare_worker_assignment(
                task, result, planned_assignment=plan_entry(task)
            )

    def test_rejects_allow_without_planner_entry(self):
        task = make_task()
        with self.assertRaisesRegex(ValueError, "requires one exact"):
            prepare_worker_assignment(task, preflight(task, True))

    def test_rejects_human_authority_weakening(self):
        task = make_task()
        task["completion_authority"] = "worker"
        with self.assertRaisesRegex(ValueError, "human-only"):
            prepare_worker_assignment(task, preflight(task))

    def test_rejects_empty_scope_or_prohibited_list(self):
        task = make_task()
        task["scope"] = []
        with self.assertRaisesRegex(ValueError, "scope"):
            prepare_worker_assignment(task, preflight(task))
        task = make_task()
        task["prohibited"] = []
        with self.assertRaisesRegex(ValueError, "prohibited"):
            prepare_worker_assignment(task, preflight(task))


if __name__ == "__main__":
    unittest.main()
