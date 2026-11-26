"""Deterministic assignment recovery classification; no dispatch or state writes.

Inputs are observations that a future trusted adapter must authenticate. This
module does not authenticate them, persist state, retry delivery, or approve
task completion.
"""
from __future__ import annotations

from typing import Any

_DELIVERY_STATES = {
    "not_dispatched",
    "dispatch_started",
    "delivery_confirmed",
    "delivery_uncertain",
}
_REVIEW_STATES = {
    "not_received",
    "submission_received",
    "review_completed",
}
_HUMAN_DISPOSITIONS = {None, "accepted", "rejected", "needs_revision"}


def classify_assignment_recovery(
    *,
    delivery_state: str,
    review_state: str,
    human_disposition: str | None = None,
) -> dict[str, Any]:
    """Return a conservative next-step classification from trusted observations.

    The returned action is guidance only. No branch triggers dispatch, retry,
    review, queue mutation, completion approval, or phase-gate closure.
    """
    if not isinstance(delivery_state, str) or delivery_state not in _DELIVERY_STATES:
        raise ValueError("Unsupported assignment delivery state.")
    if not isinstance(review_state, str) or review_state not in _REVIEW_STATES:
        raise ValueError("Unsupported assignment review state.")
    if human_disposition not in _HUMAN_DISPOSITIONS:
        raise ValueError("Unsupported human disposition.")

    if delivery_state == "not_dispatched":
        if review_state != "not_received" or human_disposition is not None:
            raise ValueError("Undispatched assignment cannot have downstream observations.")
        status, action = "prepared_not_dispatched", "hold_for_explicit_dispatch_authorization"

    elif delivery_state == "dispatch_started":
        if review_state != "not_received" or human_disposition is not None:
            raise ValueError("In-flight dispatch cannot have downstream observations.")
        status, action = "delivery_pending_or_unknown", "reconcile_delivery_before_any_retry"

    elif delivery_state == "delivery_uncertain":
        if review_state != "not_received" or human_disposition is not None:
            raise ValueError("Uncertain delivery cannot have downstream observations.")
        status, action = "delivery_uncertain", "manual_delivery_reconciliation_no_auto_retry"

    else:  # delivery_confirmed
        if review_state == "not_received":
            if human_disposition is not None:
                raise ValueError("Human disposition requires a reviewed submission.")
            status, action = "delivered_awaiting_return", "wait_for_submission_or_human_timeout_review"
        elif review_state == "submission_received":
            if human_disposition is not None:
                raise ValueError("Human disposition requires completed supervisor review.")
            status, action = "submission_awaiting_review", "perform_assignment_bound_supervisor_review"
        else:  # review_completed
            if human_disposition is None:
                status, action = "review_awaiting_human_disposition", "request_human_disposition"
            elif human_disposition == "accepted":
                status, action = "human_accepted_task_only", "record_task_acceptance_keep_phase_gate_separate"
            elif human_disposition == "rejected":
                status, action = "human_rejected_task", "return_to_human_for_replanning"
            else:
                status, action = "revision_requested", "request_worker_revision_under_human_supervision"

    return {
        "recovery_status": status,
        "recommended_next_action": action,
        "automatic_dispatch_permitted": False,
        "automatic_retry_permitted": False,
        "task_completion_approved": False,
        "phase_gate_closure_approved": False,
        "queue_state_changed": False,
        "human_review_required": True,
        "observations_authenticated_by_module": False,
    }
