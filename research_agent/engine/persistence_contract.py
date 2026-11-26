"""Optimistic-concurrency contract for a future trusted event-ledger store.

This module prepares append decisions only. It performs no persistence,
locking, source authentication, dispatch, authorization, or task-state change.
A future adapter must obtain the expected head from independently protected
storage and atomically compare-and-append against that same head.
"""
from __future__ import annotations

from typing import Any

from research_agent.engine.event_ledger import (
    _SHA256_RE,
    _strict_json_copy,
    append_event,
    validate_event_ledger,
)


def prepare_append(
    ledger: list[dict[str, Any]],
    *,
    expected_head_event_sha256: str | None,
    event_id: str,
    event_type: str,
    task_id: str,
    task_definition_sha256: str,
    occurred_at_utc: str,
    source: str,
    source_ref: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Prepare one append if the caller's independently trusted head is current.

    Exact delivery replays are idempotent even when the original append has
    already advanced the head. A new event with a stale checkpoint returns a
    conflict and an unchanged ledger. This is a decision primitive, not an
    atomic compare-and-swap: only a future trusted persistence adapter can
    provide that guarantee.
    """
    current = validate_event_ledger(ledger)
    if expected_head_event_sha256 is not None and (
        not isinstance(expected_head_event_sha256, str)
        or not _SHA256_RE.fullmatch(expected_head_event_sha256)
    ):
        raise ValueError("Expected ledger head must be null or lowercase SHA-256.")

    proposed = append_event(
        ledger,
        event_id=event_id,
        event_type=event_type,
        task_id=task_id,
        task_definition_sha256=task_definition_sha256,
        occurred_at_utc=occurred_at_utc,
        source=source,
        source_ref=source_ref,
        payload=payload,
    )

    if proposed["duplicate_replay"]:
        return {
            "status": "idempotent_replay",
            "ledger": proposed["ledger"],
            "event": proposed["event"],
            "appended": False,
            "conflict": False,
            "expected_head_event_sha256": expected_head_event_sha256,
            "actual_head_event_sha256": current["head_event_sha256"],
            "persistence_performed": False,
            "authorization_granted": False,
            "task_state_changed": False,
        }

    actual_head = current["head_event_sha256"]
    if expected_head_event_sha256 != actual_head:
        return {
            "status": "stale_checkpoint",
            "ledger": _strict_json_copy(ledger),
            "event": None,
            "appended": False,
            "conflict": True,
            "expected_head_event_sha256": expected_head_event_sha256,
            "actual_head_event_sha256": actual_head,
            "persistence_performed": False,
            "authorization_granted": False,
            "task_state_changed": False,
        }

    return {
        "status": "append_prepared",
        "ledger": proposed["ledger"],
        "event": proposed["event"],
        "appended": True,
        "conflict": False,
        "expected_head_event_sha256": expected_head_event_sha256,
        "actual_head_event_sha256": actual_head,
        "persistence_performed": False,
        "authorization_granted": False,
        "task_state_changed": False,
    }
