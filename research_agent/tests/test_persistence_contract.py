"""Optimistic-concurrency persistence contract tests; authored, not executed."""
import unittest

from research_agent.engine.event_ledger import append_event
from research_agent.engine.persistence_contract import prepare_append


class PersistenceContractTests(unittest.TestCase):
    def event_args(self, **overrides):
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
        return values

    def test_matching_empty_checkpoint_prepares_genesis_append(self):
        result = prepare_append([], expected_head_event_sha256=None, **self.event_args())
        self.assertEqual(result["status"], "append_prepared")
        self.assertTrue(result["appended"])
        self.assertFalse(result["persistence_performed"])
        self.assertFalse(result["authorization_granted"])
        self.assertEqual(len(result["ledger"]), 1)

    def test_matching_current_head_prepares_next_append(self):
        first = append_event([], **self.event_args())["ledger"]
        head = first[-1]["event_sha256"]
        result = prepare_append(
            first, expected_head_event_sha256=head,
            **self.event_args(event_id="delivery-002", event_type="review_completed"),
        )
        self.assertEqual(result["status"], "append_prepared")
        self.assertEqual(result["event"]["previous_event_sha256"], head)

    def test_stale_checkpoint_returns_conflict_without_changing_ledger(self):
        first = append_event([], **self.event_args())["ledger"]
        result = prepare_append(
            first, expected_head_event_sha256=None,
            **self.event_args(event_id="delivery-002"),
        )
        self.assertEqual(result["status"], "stale_checkpoint")
        self.assertTrue(result["conflict"])
        self.assertFalse(result["appended"])
        self.assertEqual(result["ledger"], first)
        self.assertIsNone(result["event"])

    def test_exact_replay_is_idempotent_even_after_head_advanced(self):
        first = append_event([], **self.event_args())
        advanced = append_event(
            first["ledger"], **self.event_args(event_id="delivery-002")
        )["ledger"]
        replay = prepare_append(
            advanced, expected_head_event_sha256=first["event"]["event_sha256"],
            **self.event_args(),
        )
        self.assertEqual(replay["status"], "idempotent_replay")
        self.assertFalse(replay["appended"])
        self.assertEqual(replay["ledger"], advanced)

    def test_reused_event_id_with_different_facts_is_rejected(self):
        first = append_event([], **self.event_args())["ledger"]
        with self.assertRaisesRegex(ValueError, "reused"):
            prepare_append(
                first, expected_head_event_sha256=first[-1]["event_sha256"],
                **self.event_args(payload={"note": "different"}),
            )

    def test_invalid_checkpoint_format_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Expected ledger head"):
            prepare_append([], expected_head_event_sha256="not-a-hash", **self.event_args())

    def test_corrupt_existing_ledger_is_rejected_before_preparation(self):
        first = append_event([], **self.event_args())["ledger"]
        first[0]["payload"] = {"tampered": True}
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            prepare_append(
                first, expected_head_event_sha256="a" * 64,
                **self.event_args(event_id="delivery-002"),
            )

    def test_conflict_never_claims_authority_or_persistence(self):
        first = append_event([], **self.event_args())["ledger"]
        result = prepare_append(
            first, expected_head_event_sha256=None,
            **self.event_args(event_id="delivery-002"),
        )
        self.assertFalse(result["persistence_performed"])
        self.assertFalse(result["authorization_granted"])
        self.assertFalse(result["task_state_changed"])


if __name__ == "__main__":
    unittest.main()
