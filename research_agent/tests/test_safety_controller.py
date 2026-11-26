"""Safety-controller denial tests. These tests are authored but not yet executed.

Run only after the active research handoff permits test execution.
"""
import hashlib
import json
import unittest

from research_agent.engine.report_builder import task_definition_digest
from research_agent.engine.safety_controller import (
    _authorize_task_with_policy,
    _unique_json_object,
    _canonical_hash,
    authorize_task,
)


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
            "task_scope": "follow_current_handoff_and_gate_status",
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
    for index, phase_name in enumerate(phase_order, start=1):
        if phase_name in phase_rules:
            phase_rules[phase_name].setdefault("priority", index)
    if "phase3_sideways_range" in phase_rules:
        phase3 = phase_rules["phase3_sideways_range"]
        phase3.setdefault("task_scope", "follow_current_handoff_and_gate_status")
        phase3.setdefault("g0_05", {
            "status": "read_only_reconciliation_only",
            "scripts_tests_workflows": "prohibited",
            "data_or_code_changes": "prohibited",
            "candidate_generation": "prohibited",
            "backtesting_and_pnl": "prohibited",
            "gate_closure": "prohibited",
            "lock_reason": "Current G0-05 handoff prohibits execution.",
        })
    queued_task = dict(task)
    queued_task.setdefault("title", "Read-only policy fixture task")
    queued_task.setdefault("scope", ["Inspect existing repository evidence only"])
    queued_task.setdefault("prohibited", [
        "execute_scripts", "execute_tests", "trigger_workflows",
        "modify_code", "modify_research_data", "create_candidates",
        "run_backtests", "make_pnl_claims", "select_strategies", "close_gates",
    ])
    queued_task.setdefault("completion_authority", "human_only")
    queue = {
        "schema_version": 1,
        "queue_policy": {
            "phase_order": phase_order,
            "execution_enabled": True,
            "no_phase_skipping": True,
            "advance_only_after_current_phase_gate_is_human_authorized_closed": True,
            "tasks_may_not_override_handoffs": True,
        },
        "tasks": [queued_task],
    }
    agent = {
        "agent_name": "okx-research-agent",
        "version": "1.0.0",
        "operating_mode": "deterministic_research_operations",
        "report_destination": "github_actions_artifacts",
        "cost_policy": "free_only",
        "repository_access": "read_only_by_default",
        "branch_policy": {
            "working_branch": "agent/okx-research-agent-v1",
            "research_branch": "price-action-v1",
            "automatic_merge": False,
            "automatic_commit_to_research_branch": False,
        },
        "scheduling": {
            "mode": "event_driven_with_scheduled_fallback",
            "enabled": False,
            "triggers": ["manual_dispatch"],
            "concurrency_group": "okx-research-agent",
            "cancel_in_progress": False,
        },
        "execution": {
            "enabled": True,
            "require_task_allowlist": True,
            "require_phase_permission": True,
            "require_safety_controller": True,
            "current_g0_05_execution_lock": lock,
        },
        "phase_order": phase_order,
        "prohibitions": ["no_automatic_merge"],
    }
    phases = {
        "schema_version": 1,
        "phase_order": phase_order,
        "global_defaults": {
            "repository_inspection": "allow_read_only",
            "evidence_lineage_review": "allow_read_only",
            "report_generation": "allow_local_or_artifact_only",
            "execute_scripts": "deny_unless_task_and_phase_allowlisted",
            "execute_tests": "deny_unless_task_and_phase_allowlisted",
            "trigger_workflows": "deny",
            "modify_research_data": "deny",
            "modify_canonical_definitions": "deny",
            "create_candidates": "deny",
            "run_backtests": "deny",
            "make_pnl_claims": "deny",
            "select_strategies": "deny",
            "close_gates": "deny",
            "deploy_to_vps": "deny",
            "change_secrets_or_permissions": "deny",
        },
        "phases": phase_rules,
        "approval_required_for": ["closing_a_research_gate"],
    }
    allowlist = {
        "schema_version": 1,
        "description": "Test-only trusted approval fixture.",
        "approved_tasks": [
            {"task_id": queued_task["task_id"], "task_sha256": digest(queued_task)}
        ]
    }
    return queued_task, agent, phases, queue, allowlist


class SafetyControllerTests(unittest.TestCase):
    def test_safety_and_report_builders_share_identical_task_digest(self):
        task = {
            "task_id": "P3-RO-CROSS-CHECK",
            "phase": "phase3_sideways_range",
            "scope": ["read-only", "lineage"],
            "policy": {"enabled": False, "thresholds": [1, 2.5, None]},
        }
        self.assertEqual(_canonical_hash(task), task_definition_digest(task))

    def evaluate(self, task, **kwargs):
        queued, agent, phases, queue, allowlist = policy_fixture(task, **kwargs)
        return _authorize_task_with_policy(
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
                    "status": "queued",
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

    def test_denies_malformed_non_string_operation_without_raising(self):
        result = self.evaluate(
            {
                "task_id": "P3-BAD-OP",
                "phase": "phase3_sideways_range",
                "operation": ["repository_inspection"],
                "status": "queued",
            }
        )
        self.assertFalse(result["authorized"])
        self.assertIn("operation must be a non-empty string", result["reason"])

    def test_denies_malformed_nested_policy_without_raising(self):
        task = {
            "task_id": "P3-BAD-POLICY",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        result = _authorize_task_with_policy(
            task,
            allowlist={"approved_tasks": []},
            agent_config={"execution": []},
            phase_config={"phase_order": [], "phases": [], "global_defaults": []},
            queue_config={"queue_policy": [], "tasks": []},
        )
        self.assertFalse(result["authorized"])
        self.assertEqual(result["decision"], "DENY")

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

    def test_rejects_duplicate_keys_in_policy_json_objects(self):
        with self.assertRaisesRegex(Exception, "Duplicate JSON object key"):
            json.loads('{"execution":{"enabled":false,"enabled":true}}',
                       object_pairs_hook=_unique_json_object)

    def test_denies_malformed_unrelated_queue_entry(self):
        task = {
            "task_id": "P3-QUEUE-CHECK",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        queue["tasks"].append("not-an-object")
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("Every task queue entry", result["reason"])

    def test_denies_phase_priority_mismatch(self):
        result = self.evaluate(
            {
                "task_id": "P3-PRIORITY-MISMATCH",
                "phase": "phase3_sideways_range",
                "operation": "repository_inspection",
                "status": "queued",
            },
            phase_rules={
                "phase3_sideways_range": {
                    "priority": 2,
                    "status": "active_research_phase",
                    "execution_override": "allow_read_only",
                }
            },
        )
        self.assertFalse(result["authorized"])
        self.assertIn("priorities", result["reason"])

    def test_denies_queue_without_human_gate_advancement_rule(self):
        task = {
            "task_id": "P3-NO-GATE-RULE",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        queue["queue_policy"].pop(
            "advance_only_after_current_phase_gate_is_human_authorized_closed"
        )
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("human-authorized gate closure", result["reason"])

    def test_denies_duplicate_ids_in_trusted_allowlist(self):
        task = {
            "task_id": "P3-DUPLICATE-ALLOW",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        allowlist["approved_tasks"].append(dict(allowlist["approved_tasks"][0]))
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("duplicate task IDs", result["reason"])


    def test_public_runtime_authorizer_rejects_policy_injection(self):
        task = {
            "task_id": "P3-INJECT",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        with self.assertRaises(TypeError):
            authorize_task(task, allowlist={"approved_tasks": []})

    def test_denies_task_missing_mandatory_prohibition_even_if_rehashed(self):
        task = {
            "task_id": "P3-MISSING-PROHIBITION",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        queued["prohibited"].remove("execute_tests")
        allowlist["approved_tasks"][0]["task_sha256"] = digest(queued)
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("mandatory safety restrictions", result["reason"])

    def test_denies_task_with_unsupported_contract_field_even_if_rehashed(self):
        task = {
            "task_id": "P3-EXTRA-FIELD",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        queued["shell_command"] = "unsafe"
        allowlist["approved_tasks"][0]["task_sha256"] = digest(queued)
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("unsupported contract fields", result["reason"])

    def test_denies_non_human_task_completion_authority_even_if_rehashed(self):
        task = {
            "task_id": "P3-AUTO-COMPLETE",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        queued["completion_authority"] = "agent"
        allowlist["approved_tasks"][0]["task_sha256"] = digest(queued)
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("human_only", result["reason"])

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


    def test_denies_unrelated_queue_task_with_incomplete_contract(self):
        task = {
            "task_id": "P3-QUEUE-CONTRACT",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        unrelated = dict(queued)
        unrelated["task_id"] = "P3-UNRELATED"
        unrelated.pop("title")
        queue["tasks"].append(unrelated)
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("invalid contract", result["reason"])

    def test_denies_duplicate_prohibited_entries_even_if_rehashed(self):
        task = {
            "task_id": "P3-DUPLICATE-PROHIBITION",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        queued["prohibited"].append("execute_tests")
        allowlist["approved_tasks"][0]["task_sha256"] = digest(queued)
        queue["tasks"][0] = queued
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("duplicate entries", result["reason"])


    def test_denies_enabled_scheduling(self):
        task = {
            "task_id": "P3-SCHEDULE-ON",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        agent["scheduling"]["enabled"] = True
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("Scheduling must remain explicitly disabled", result["reason"])

    def test_denies_branch_policy_drift(self):
        task = {
            "task_id": "P3-BRANCH-DRIFT",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        agent["branch_policy"]["automatic_merge"] = True
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("Branch policy differs", result["reason"])

    def test_denies_integer_zero_instead_of_boolean_false_in_branch_policy(self):
        task = {
            "task_id": "P3-BRANCH-BOOL-TYPE",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        agent["branch_policy"]["automatic_merge"] = 0
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("Branch policy differs", result["reason"])

    def test_denies_boolean_phase_priority_instead_of_integer(self):
        task = {
            "task_id": "P3-PRIORITY-BOOL-TYPE",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        phases["phases"]["phase3_sideways_range"]["priority"] = True
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("priorities", result["reason"])


    def test_denies_unsupported_top_level_policy_fields(self):
        task = {
            "task_id": "P3-EXTRA-POLICY-KEY",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        agent["unreviewed_override"] = True
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("unsupported top-level fields", result["reason"])

    def test_denies_unsupported_phase_rule_fields(self):
        task = {
            "task_id": "P3-EXTRA-PHASE-KEY",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        phases["phases"]["phase3_sideways_range"]["unreviewed_override"] = True
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("Phase 3 rule", result["reason"])

    def test_denies_unsupported_queue_policy_fields(self):
        task = {
            "task_id": "P3-EXTRA-QUEUE-KEY",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        queue["queue_policy"]["allow_anything"] = True
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("Queue policy", result["reason"])

    def test_denies_integer_one_for_boolean_execution_flag(self):
        task = {
            "task_id": "P3-INT-BOOL",
            "phase": "phase3_sideways_range",
            "operation": "repository_inspection",
            "status": "queued",
        }
        queued, agent, phases, queue, allowlist = policy_fixture(task)
        agent["execution"]["require_task_allowlist"] = 1
        result = _authorize_task_with_policy(
            queued, allowlist=allowlist, agent_config=agent,
            phase_config=phases, queue_config=queue,
        )
        self.assertFalse(result["authorized"])
        self.assertIn("strict JSON booleans", result["reason"])


if __name__ == "__main__":
    unittest.main()
