"""Assignment recovery policy tests; authored, not executed."""
import unittest

from research_agent.engine.recovery_policy import classify_assignment_recovery


class RecoveryPolicyTests(unittest.TestCase):
    def classify(self, **kwargs):
        return classify_assignment_recovery(**kwargs)

    def test_not_dispatched_never_dispatches_automatically(self):
        result = self.classify(delivery_state="not_dispatched", review_state="not_received")
        self.assertEqual(result["recovery_status"], "prepared_not_dispatched")
        self.assertFalse(result["automatic_dispatch_permitted"])

    def test_dispatch_started_requires_delivery_reconciliation(self):
        result = self.classify(delivery_state="dispatch_started", review_state="not_received")
        self.assertEqual(result["recommended_next_action"], "reconcile_delivery_before_any_retry")
        self.assertFalse(result["automatic_retry_permitted"])

    def test_uncertain_delivery_never_triggers_automatic_retry(self):
        result = self.classify(delivery_state="delivery_uncertain", review_state="not_received")
        self.assertEqual(result["recovery_status"], "delivery_uncertain")
        self.assertEqual(result["recommended_next_action"], "manual_delivery_reconciliation_no_auto_retry")
        self.assertFalse(result["automatic_retry_permitted"])

    def test_confirmed_delivery_waits_for_worker_return(self):
        result = self.classify(delivery_state="delivery_confirmed", review_state="not_received")
        self.assertEqual(result["recovery_status"], "delivered_awaiting_return")

    def test_received_submission_requires_assignment_bound_review(self):
        result = self.classify(delivery_state="delivery_confirmed", review_state="submission_received")
        self.assertEqual(result["recommended_next_action"], "perform_assignment_bound_supervisor_review")

    def test_reviewed_submission_requires_human_disposition(self):
        result = self.classify(delivery_state="delivery_confirmed", review_state="review_completed")
        self.assertEqual(result["recovery_status"], "review_awaiting_human_disposition")
        self.assertTrue(result["human_review_required"])

    def test_human_acceptance_does_not_close_phase_gate(self):
        result = self.classify(
            delivery_state="delivery_confirmed",
            review_state="review_completed",
            human_disposition="accepted",
        )
        self.assertEqual(result["recovery_status"], "human_accepted_task_only")
        self.assertFalse(result["task_completion_approved"])
        self.assertFalse(result["phase_gate_closure_approved"])

    def test_rejection_and_revision_remain_human_controlled(self):
        rejected = self.classify(
            delivery_state="delivery_confirmed",
            review_state="review_completed",
            human_disposition="rejected",
        )
        revision = self.classify(
            delivery_state="delivery_confirmed",
            review_state="review_completed",
            human_disposition="needs_revision",
        )
        self.assertEqual(rejected["recommended_next_action"], "return_to_human_for_replanning")
        self.assertEqual(revision["recommended_next_action"], "request_worker_revision_under_human_supervision")

    def test_impossible_state_combinations_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Undispatched"):
            self.classify(delivery_state="not_dispatched", review_state="submission_received")
        with self.assertRaisesRegex(ValueError, "in-flight"):
            self.classify(delivery_state="dispatch_started", review_state="review_completed")
        with self.assertRaisesRegex(ValueError, "Human disposition"):
            self.classify(
                delivery_state="delivery_confirmed",
                review_state="submission_received",
                human_disposition="accepted",
            )

    def test_unknown_observations_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "delivery state"):
            self.classify(delivery_state="sent_maybe", review_state="not_received")
        with self.assertRaisesRegex(ValueError, "review state"):
            self.classify(delivery_state="delivery_confirmed", review_state="done-ish")

    def test_no_outcome_claims_or_side_effects(self):
        result = self.classify(
            delivery_state="delivery_confirmed",
            review_state="review_completed",
            human_disposition="accepted",
        )
        self.assertFalse(result["automatic_dispatch_permitted"])
        self.assertFalse(result["automatic_retry_permitted"])
        self.assertFalse(result["queue_state_changed"])
        self.assertFalse(result["observations_authenticated_by_module"])


if __name__ == "__main__":
    unittest.main()
