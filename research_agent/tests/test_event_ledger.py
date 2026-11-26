"""Append-only task event ledger tests; authored but not executed."""
import unittest

from research_agent.engine.event_ledger import append_event, validate_event_ledger


class EventLedgerTests(unittest.TestCase):
    def make_event(self, ledger=None, **overrides):
        values = {
            "event_id": "delivery-001",
            "event_type": "task_observed",
            "task_id": "P3-G005-RO-001",
            "task_definition_sha256": "a" * 64,
            "occurred_at_utc": "2026-11-26T12:00:00Z",
            "source": "github_workflow",
            "source_ref": "workflow-run:123",
            "payload": {"note": "observed"},
        }
        values.update(overrides)
        return append_event(ledger or [], **values)

    def test_appends_and_verifies_genesis_event(self):
        result = self.make_event()
        verified = validate_event_ledger(result["ledger"])
        self.assertTrue(verified["valid"])
        self.assertEqual(verified["event_count"], 1)
        self.assertTrue(result["appended"])
        self.assertFalse(result["authorization_granted"])
        self.assertFalse(result["task_state_changed"])

    def test_appends_hash_linked_second_event(self):
        first = self.make_event()
        second = self.make_event(
            first["ledger"], event_id="delivery-002",
            event_type="assignment_prepared",
        )
        self.assertEqual(
            second["event"]["previous_event_sha256"],
            first["event"]["event_sha256"],
        )
        self.assertEqual(validate_event_ledger(second["ledger"])["event_count"], 2)

    def test_exact_delivery_replay_is_idempotent(self):
        first = self.make_event()
        replay = self.make_event(first["ledger"])
        self.assertFalse(replay["appended"])
        self.assertTrue(replay["duplicate_replay"])
        self.assertEqual(replay["ledger"], first["ledger"])

    def test_event_id_reuse_with_different_facts_is_rejected(self):
        first = self.make_event()
        with self.assertRaisesRegex(ValueError, "reused"):
            self.make_event(first["ledger"], payload={"note": "changed"})

    def test_tampered_payload_is_detected(self):
        first = self.make_event()
        tampered = [dict(first["event"])]
        tampered[0]["payload"] = {"note": "tampered"}
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            validate_event_ledger(tampered)

    def test_broken_chain_link_is_detected(self):
        first = self.make_event()
        second = self.make_event(first["ledger"], event_id="delivery-002")
        broken = [dict(item) for item in second["ledger"]]
        broken[1]["previous_event_sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "Broken previous-event link"):
            validate_event_ledger(broken)

    def test_duplicate_event_id_in_imported_ledger_is_rejected(self):
        first = self.make_event()
        duplicated = first["ledger"] + [dict(first["event"])]
        with self.assertRaisesRegex(ValueError, "Duplicate event ID"):
            validate_event_ledger(duplicated)

    def test_noncanonical_time_and_unsupported_event_type_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "canonical"):
            self.make_event(occurred_at_utc="2026-11-26T12:00:00+00:00")
        with self.assertRaisesRegex(ValueError, "Unsupported ledger event type"):
            self.make_event(event_type="execute_task")

    def test_non_json_payload_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "strict JSON"):
            self.make_event(payload={"bad": object()})

    def test_non_string_event_type_and_source_are_rejected_cleanly(self):
        with self.assertRaisesRegex(ValueError, "Unsupported ledger event type"):
            self.make_event(event_type=["task_observed"])
        with self.assertRaisesRegex(ValueError, "Unsupported event source"):
            self.make_event(source=["github_workflow"])

    def test_python_only_payload_values_and_non_string_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "strict JSON"):
            self.make_event(payload={"bad": (1, 2)})
        with self.assertRaisesRegex(ValueError, "keys must be strings"):
            self.make_event(payload={1: "bad"})

    def test_empty_ledger_is_valid_and_non_authorizing(self):
        result = validate_event_ledger([])
        self.assertTrue(result["valid"])
        self.assertIsNone(result["head_event_sha256"])
        self.assertFalse(result["authorization_granted"])
        self.assertFalse(result["gate_closure_approved"])


if __name__ == "__main__":
    unittest.main()
