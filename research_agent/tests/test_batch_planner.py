"""Batch planner tests; authored but not executed under the active handoff."""
import unittest
from unittest.mock import patch

from research_agent.engine.batch_planner import build_batch_plan, build_runtime_batch_plan, EXPECTED_PHASE_ORDER


def make_queue():
    return {
        "queue_policy": {
            "phase_order": list(EXPECTED_PHASE_ORDER),
            "no_phase_skipping": True,
        },
        "tasks": [
            {"task_id": "P3-A", "phase": EXPECTED_PHASE_ORDER[0],
             "operation": "repository_inspection", "title": "Phase 3 A", "status": "queued",
             "completion_authority": "human_only"},
            {"task_id": "P3-B", "phase": EXPECTED_PHASE_ORDER[0],
             "operation": "evidence_lineage_review", "title": "Phase 3 B", "status": "queued",
             "completion_authority": "human_only"},
            {"task_id": "P1-A", "phase": EXPECTED_PHASE_ORDER[1],
             "operation": "repository_inspection", "title": "Phase 1 A",
             "status": "blocked_until_prior_phases_complete",
             "completion_authority": "human_only"},
        ],
    }


def make_summary(queue, allowed_ids=()):
    rows = []
    for task in queue["tasks"]:
        allowed = task["task_id"] in allowed_ids
        rows.append({
            "task_id": task["task_id"],
            "authorized": allowed,
            "decision": "ALLOW_READ_ONLY" if allowed else "DENY",
            "execution_performed": False,
            "mode": "preflight_only",
            "reason": "Exact preflight decision.",
        })
    return {
        "mode": "queue_preflight_only",
        "decision": "SUMMARY_ONLY",
        "authorized": False,
        "execution_performed": False,
        "tasks": rows,
    }


class BatchPlannerTests(unittest.TestCase):
    @patch("research_agent.engine.batch_planner._preflight_all_tasks_with_queue")
    @patch("research_agent.engine.batch_planner.load_queue")
    def test_runtime_planner_uses_fixed_queue_and_preflight_sources(self, mock_load, mock_preflight):
        queue = make_queue()
        summary = make_summary(queue)
        mock_load.return_value = queue
        mock_preflight.return_value = summary

        result = build_runtime_batch_plan()

        mock_load.assert_called_once_with()
        mock_preflight.assert_called_once_with(queue)
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["planned_task_count"], 0)

    def test_runtime_planner_rejects_invalid_batch_size_before_loading(self):
        with patch("research_agent.engine.batch_planner.load_queue") as mock_load:
            with self.assertRaises(ValueError):
                build_runtime_batch_plan(max_tasks=0)
            mock_load.assert_not_called()

    def test_denied_earliest_phase_stops_without_skipping_to_phase_one(self):
        queue = make_queue()
        result = build_batch_plan(queue=queue, preflight_summary=make_summary(queue))
        self.assertEqual(result["mode"], "batch_plan_only")
        self.assertFalse(result["authorized"])
        self.assertFalse(result["execution_performed"])
        self.assertEqual(result["planned_tasks"], [])
        self.assertEqual(len(result["deferred_tasks"]), 2)
        self.assertIsNone(result["phase"])

    def test_selects_only_exactly_preflight_allowed_tasks(self):
        queue = make_queue()
        result = build_batch_plan(
            queue=queue, preflight_summary=make_summary(queue, {"P3-A"})
        )
        self.assertEqual([x["task_id"] for x in result["planned_tasks"]], ["P3-A"])
        self.assertEqual(result["phase"], EXPECTED_PHASE_ORDER[0])
        self.assertEqual(result["planned_tasks"][0]["assignment_status"],
                         "preflight_allowed_not_executed")

    def test_respects_batch_limit(self):
        queue = make_queue()
        result = build_batch_plan(
            max_tasks=1, queue=queue,
            preflight_summary=make_summary(queue, {"P3-A", "P3-B"})
        )
        self.assertEqual(result["planned_task_count"], 1)
        self.assertEqual(result["max_tasks"], 1)

    def test_rejects_boolean_batch_limit(self):
        with self.assertRaises(ValueError):
            build_batch_plan(max_tasks=True, queue=make_queue(),
                             preflight_summary=make_summary(make_queue()))

    def test_rejects_phase_order_drift(self):
        queue = make_queue()
        queue["queue_policy"]["phase_order"] = list(reversed(EXPECTED_PHASE_ORDER))
        with self.assertRaisesRegex(ValueError, "phase order"):
            build_batch_plan(queue=queue, preflight_summary=make_summary(queue))

    def test_rejects_duplicate_queue_ids(self):
        queue = make_queue()
        queue["tasks"].append(dict(queue["tasks"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate task IDs"):
            build_batch_plan(queue=queue, preflight_summary=make_summary(queue))

    def test_rejects_incomplete_or_duplicate_preflight_rows(self):
        queue = make_queue()
        summary = make_summary(queue)
        summary["tasks"].pop()
        with self.assertRaisesRegex(ValueError, "match every"):
            build_batch_plan(queue=queue, preflight_summary=summary)

    def test_rejects_queue_wide_authorization_claim(self):
        queue = make_queue()
        summary = make_summary(queue)
        summary["authorized"] = True
        with self.assertRaisesRegex(ValueError, "non-authorizing"):
            build_batch_plan(queue=queue, preflight_summary=summary)

    def test_never_changes_queue_status(self):
        queue = make_queue()
        before = [task["status"] for task in queue["tasks"]]
        build_batch_plan(queue=queue, preflight_summary=make_summary(queue, {"P3-A"}))
        self.assertEqual([task["status"] for task in queue["tasks"]], before)


if __name__ == "__main__":
    unittest.main()
