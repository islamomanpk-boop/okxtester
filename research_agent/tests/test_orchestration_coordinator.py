"""Authored tests for the pure orchestration coordinator; not executed."""
import unittest
from unittest.mock import patch

from research_agent.engine.orchestration_coordinator import (
    build_orchestration_snapshot,
    build_runtime_orchestration_snapshot,
)


def fixture(allowed=False):
    task = {
        "task_id": "P3-TEST-001",
        "phase": "phase3_sideways_range",
        "operation": "repository_inspection",
        "handoff_id": "TEST_HANDOFF",
        "title": "Read-only inspection",
        "status": "queued",
        "scope": ["Read existing documentation"],
        "prohibited": ["execute_scripts", "modify_research_data"],
        "completion_authority": "human_only",
    }
    decision = "ALLOW_READ_ONLY" if allowed else "DENY"
    preflight = {
        "mode": "queue_preflight_only",
        "decision": "SUMMARY_ONLY",
        "authorized": False,
        "execution_performed": False,
        "task_count": 1,
        "allow_count": int(allowed),
        "deny_count": int(not allowed),
        "reason": "Per-task preflight results only.",
        "tasks": [{
            "task_id": task["task_id"],
            "queue_status": "queued",
            "decision": decision,
            "authorized": allowed,
            "reason": "Test-only preflight fixture.",
            "execution_performed": False,
            "mode": "preflight_only",
        }],
    }
    queue = {
        "queue_policy": {
            "phase_order": [
                "phase3_sideways_range",
                "phase1_uptrend_bullish",
                "phase2_downtrend_bearish",
                "phase4_choppy_high_volatility",
                "phase5_transition_expansion",
            ],
            "no_phase_skipping": True,
        },
        "tasks": [task],
    }
    return queue, preflight


class OrchestrationCoordinatorTests(unittest.TestCase):
    def test_denied_queued_task_becomes_blocked_package(self):
        queue, preflight = fixture(False)
        result = build_orchestration_snapshot(queue=queue, preflight_summary=preflight)
        self.assertEqual(result["phase"], "phase3_sideways_range")
        self.assertEqual(result["planned_task_count"], 0)
        self.assertEqual(result["assignment_package_count"], 1)
        item = result["assignment_packages"][0]
        self.assertEqual(item["package"]["assignment_status"], "blocked_preflight")
        self.assertFalse(item["package"]["dispatch_permitted"])
        self.assertFalse(item["package_digest_stored"])

    def test_allowed_task_is_packaged_but_never_dispatched(self):
        queue, preflight = fixture(True)
        result = build_orchestration_snapshot(queue=queue, preflight_summary=preflight)
        self.assertEqual(result["planned_task_count"], 1)
        item = result["assignment_packages"][0]
        self.assertEqual(item["package"]["assignment_status"], "prepared_not_dispatched")
        self.assertFalse(result["dispatch_permitted"])
        self.assertFalse(result["execution_performed"])
        self.assertFalse(result["queue_state_changed"])

    def test_recovery_observations_are_never_authenticated(self):
        queue, preflight = fixture(False)
        result = build_orchestration_snapshot(
            queue=queue,
            preflight_summary=preflight,
            recovery_observations={
                "P3-TEST-001": {
                    "delivery_state": "delivery_uncertain",
                    "review_state": "not_received",
                    "human_disposition": None,
                }
            },
        )
        guidance = result["recovery_guidance"]["P3-TEST-001"]
        self.assertEqual(guidance["recovery_status"], "delivery_uncertain")
        self.assertFalse(guidance["automatic_retry_permitted"])
        self.assertFalse(guidance["observation_source_authenticated"])

    @patch("research_agent.engine.orchestration_coordinator._preflight_all_tasks_with_queue")
    @patch("research_agent.engine.orchestration_coordinator.load_queue")
    def test_runtime_uses_one_queue_snapshot_for_preflight_and_planning(self, mock_load, mock_preflight):
        queue, preflight = fixture(False)
        mock_load.return_value = queue
        mock_preflight.return_value = preflight

        result = build_runtime_orchestration_snapshot()

        mock_load.assert_called_once_with()
        mock_preflight.assert_called_once_with(queue)
        self.assertEqual(result["planned_task_count"], 0)
        self.assertFalse(result["dispatch_permitted"])

    def test_rejects_boolean_batch_limit(self):
        queue, preflight = fixture(False)
        with self.assertRaises(ValueError):
            build_orchestration_snapshot(
                queue=queue, preflight_summary=preflight, max_tasks=True
            )

    def test_denied_phase_three_prevents_allowed_phase_one_from_being_packaged(self):
        queue, preflight = fixture(False)
        phase_one = {
            "task_id": "P1-TEST-001",
            "phase": "phase1_uptrend_bullish",
            "operation": "repository_inspection",
            "handoff_id": "P1_HANDOFF",
            "title": "Later phase inspection",
            "status": "queued",
            "scope": ["Read existing documentation"],
            "prohibited": ["execute_scripts", "modify_research_data"],
            "completion_authority": "human_only",
        }
        queue["tasks"].append(phase_one)
        preflight["tasks"].append({
            "task_id": "P1-TEST-001",
            "queue_status": "queued",
            "decision": "ALLOW_READ_ONLY",
            "authorized": True,
            "reason": "Test-only later-phase allowance.",
            "execution_performed": False,
            "mode": "preflight_only",
        })
        preflight["task_count"] = 2
        preflight["allow_count"] = 1
        preflight["deny_count"] = 1

        result = build_orchestration_snapshot(
            queue=queue, preflight_summary=preflight
        )

        self.assertIsNone(result["phase"])
        self.assertEqual(result["planned_task_count"], 0)
        self.assertEqual(
            [item["task_id"] for item in result["assignment_packages"]],
            ["P3-TEST-001"],
        )
        self.assertEqual(
            result["assignment_packages"][0]["package"]["assignment_status"],
            "blocked_preflight",
        )
        self.assertFalse(result["dispatch_permitted"])

    def test_unknown_recovery_task_is_rejected(self):
        queue, preflight = fixture(False)
        with self.assertRaises(ValueError):
            build_orchestration_snapshot(
                queue=queue,
                preflight_summary=preflight,
                recovery_observations={
                    "UNKNOWN": {
                        "delivery_state": "not_dispatched",
                        "review_state": "not_received",
                        "human_disposition": None,
                    }
                },
            )


if __name__ == "__main__":
    unittest.main()
