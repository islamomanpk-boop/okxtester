"""Safety-controller denial tests. These tests are authored but not yet executed.

Run only after the active research handoff permits test execution.
"""
import hashlib
import json
import unittest

from research_agent.engine.safety_controller import authorize_task


def digest(value):
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def policy_fixture(task, *, phase_order=None, phase_rules=None, lock=False):
    phase_order = phase_order or ["phase3_sideways_range"]
    phase_rules = phase_rules or {
        "phase3_sideways_range": {
            "status": "active_research_phase",
            "execution_override": "allow_read_only",
            "g0_05": {
                "status": "read_only_reconciliation_only",
                "scripts_tests_workflows": "prohibited",
                "data_or_code_changes": "prohibited",
                "candidate_generation": "prohibited",
                "backtesting_and_pnl": "prohibited",
                "gate_closure": "prohibited",
            },
        }
    }
    queued_task = dict(task)
    queue = {
        "queue_policy": {
            "phase_order": phase_order,
            "execution_enabled": True,
            "no_phase_skipping": True,
            "tasks_may_not_override_handoffs": True,
        },
        "tasks": [queued_task],
    }
    agent = {
        "execution": {
            "enabled": True,
            "require_task_allowlist": True,
            "require_phase_permission": True,
            "require_safety_controller": True,
            "current_g0_05_execution_lock": lock,
        },
        "phase_order": phase_order,
    }
    phases = {
        "phase_order": phase_order,
        "global_defaults": {
            "repository_inspection": "allow_read_only",
            "evidence_lineage_review": "allow_read_only",
            "report_generation": "allow_local_or_artifact_only",
        },
        "phases": phase_rules,
    }
    allowlist = {
        "approved_tasks": [
            {"task_id": queued_task["task_id"], "task_sha256": digest(queued_task)}
        ]
    }
    return queued_task, agent, phases, queue, allowlist


class SafetyControllerTests(unittest.TestCase):
    def evaluate(self, task, **kwargs):
        queued, agent, phases, queue, allowlist = policy_fixture(task, **kwargs)
        return authorize_task(
            queued,
            allowlist=allowlist,
            agent_config=agent,
            phase_config=phases,
            queue_config=queue,
        )

    def test_allows_exactly_approved_read_only_task_when_phase_opts_in(self):
        result = self.evaluate({
            "task_id": "P3-RO-TEST",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        })
        self.assertTrue(result["authorized"])

    def test_denies_phase_with_execution_override_deny(self):
        result = self.evaluate(
            {
                "task_id": "P3-RO-DENY",
                "phase": "phase3_sideways_range",
                "operation": "repository_inspection",
                "status": "queued",
            },
            phase_rules={
                "phase3_sideways_range": {
                    "status": "active_research_phase",
                    "execution_override": "deny",
                }
            },
        )
        self.assertFalse(result["authorized"])
        self.assertIn("execution override", result["reason"])

    def test_denies_later_phase_without_human_closed_prior_gate(self):
        result = self.evaluate(
            {
                "task_id": "P1-RO-BLOCK",
                "phase": "phase1_uptrend_bullish",
                "operation": "repository_inspection",
                "status": "queued",
            },
            phase_order=["phase3_sideways_range", "phase1_uptrend_bullish"],
            phase_rules={
                "phase3_sideways_range": {
                    "status": "active_research_phase",
                    "execution_override": "deny",
                },
                "phase1_uptrend_bullish": {
                    "status": "active_research_phase",
                    "execution_override": "allow_read_only",
                },
            },
        )
        self.assertFalse(result["authorized"])
        self.assertIn("human-authorized closed", result["reason"])

    def test_denies_relabelled_phase3_task_while_global_lock_is_active(self):
        result = self.evaluate(
            {
                "task_id": "P3-OTHER-LABEL",
                "phase": "phase3_sideways_range",
                "workstream": "unrelated_label",
                "operation": "repository_inspection",
                "status": "queued",
            },
            lock=True,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("all Phase 3 task authorization", result["reason"])

    def test_denies_duplicate_phase_order_entries(self):
        result = self.evaluate(
            {
                "task_id": "P3-DUPLICATE-PHASE",
                "phase": "phase3_sideways_range",
                "operation": "repository_inspection",
                "status": "queued",
            },
            phase_order=["phase3_sideways_range", "phase3_sideways_range"],
        )
        self.assertFalse(result["authorized"])
        self.assertIn("unique, non-empty phase names", result["reason"])

    def test_denies_g0_05_while_global_lock_is_active(self):
        result = self.evaluate(
            {
                "task_id": "P3-G005-LOCK",
                "phase": "phase3_sideways_range",
                "workstream": "g0_05",
                "handoff_id": "PHASE3_G0_05_RECONCILIATION_TASK_02",
                "operation": "evidence_lineage_review",
                "status": "queued",
            },
            lock=True,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("G0-05 execution lock is active", result["reason"])


if __name__ == "__main__":
    unittest.main()
