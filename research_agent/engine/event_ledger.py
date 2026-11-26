"""Append-only task event ledger primitives; no persistence or authority.

The ledger records an auditable sequence of task-related observations. It is
not a queue, scheduler, authorization source, task-state mutator, or gate
approval mechanism. Callers must persist returned records through a separately
reviewed trusted channel and authenticate event sources independently.
"""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
import math
import re
from typing import Any

EVENT_TYPES = {
    "task_observed",
    "assignment_prepared",
    "worker_submission_received",
    "review_completed",
    "human_disposition_recorded",
}
EVENT_SOURCES = {"github_workflow", "human_review", "worker_return"}
_EVENT_FIELDS = {
    "event_id", "event_type", "task_id", "task_definition_sha256",
    "occurred_at_utc", "source", "source_ref", "payload",
    "previous_event_sha256", "event_sha256",
}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


def _validate_json_value(value: Any) -> None:
    """Reject Python values that JSON serialization would silently coerce."""
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Ledger values must contain finite JSON numbers.")
        return
    if isinstance(value, list):
        for item in value:
            _validate_json_value(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("Ledger JSON object keys must be strings.")
            _validate_json_value(item)
        return
    raise ValueError("Ledger values must contain strict JSON data.")


def _strict_json_copy(value: Any) -> Any:
    """Round-trip only unambiguous JSON values; reject coercible Python values."""
    _validate_json_value(value)
    try:
        encoded = json.dumps(value, ensure_ascii=False, allow_nan=False)
        return json.loads(encoded)
    except (TypeError, ValueError) as exc:
        raise ValueError("Ledger values must contain strict JSON data.") from exc


def _canonical_bytes(value: dict[str, Any]) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")


def _event_digest(event_without_hash: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(event_without_hash)).hexdigest()


def _validate_timestamp(value: Any) -> None:
    if not isinstance(value, str) or not _TIMESTAMP_RE.fullmatch(value):
        raise ValueError("Event time must be canonical ISO-8601 UTC ending in Z.")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError("Event time is not a valid UTC timestamp.") from exc


def _event_core(event: dict[str, Any]) -> dict[str, Any]:
    return {key: event[key] for key in _EVENT_FIELDS if key not in {
        "previous_event_sha256", "event_sha256"
    }}


def _validate_event_shape(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict) or set(event) != _EVENT_FIELDS:
        raise ValueError("Ledger event has missing or unsupported fields.")
    if not isinstance(event["event_id"], str) or not event["event_id"].strip():
        raise ValueError("Event ID must be a non-empty string.")
    if len(event["event_id"]) > 200:
        raise ValueError("Event ID exceeds the 200-character limit.")
    if not isinstance(event["event_type"], str) or event["event_type"] not in EVENT_TYPES:
        raise ValueError("Unsupported ledger event type.")
    if not isinstance(event["task_id"], str) or not event["task_id"].strip():
        raise ValueError("Event task ID must be a non-empty string.")
    if not isinstance(event["task_definition_sha256"], str) or not _SHA256_RE.fullmatch(
        event["task_definition_sha256"]
    ):
        raise ValueError("Event task-definition digest must be lowercase SHA-256.")
    _validate_timestamp(event["occurred_at_utc"])
    if not isinstance(event["source"], str) or event["source"] not in EVENT_SOURCES:
        raise ValueError("Unsupported event source category.")
    if not isinstance(event["source_ref"], str) or not event["source_ref"].strip():
        raise ValueError("Event source reference must be a non-empty string.")
    if not isinstance(event["payload"], dict):
        raise ValueError("Event payload must be a JSON object.")
    _strict_json_copy(event["payload"])
    previous = event["previous_event_sha256"]
    if previous is not None and (
        not isinstance(previous, str) or not _SHA256_RE.fullmatch(previous)
    ):
        raise ValueError("Previous-event digest must be null or lowercase SHA-256.")
    if not isinstance(event["event_sha256"], str) or not _SHA256_RE.fullmatch(
        event["event_sha256"]
    ):
        raise ValueError("Event digest must be lowercase SHA-256.")
    return event


def validate_event_ledger(ledger: Any) -> dict[str, Any]:
    """Verify schema, unique event IDs, and the complete hash chain."""
    if not isinstance(ledger, list):
        raise ValueError("Event ledger must be a list.")
    seen: dict[str, dict[str, Any]] = {}
    previous_hash = None
    for index, raw_event in enumerate(ledger):
        event = _validate_event_shape(raw_event)
        event_id = event["event_id"]
        if event_id in seen:
            raise ValueError(f"Duplicate event ID at ledger index {index}.")
        if event["previous_event_sha256"] != previous_hash:
            raise ValueError(f"Broken previous-event link at ledger index {index}.")
        unsigned = {key: event[key] for key in event if key != "event_sha256"}
        if _event_digest(unsigned) != event["event_sha256"]:
            raise ValueError(f"Event hash mismatch at ledger index {index}.")
        seen[event_id] = event
        previous_hash = event["event_sha256"]
    return {
        "valid": True,
        "event_count": len(ledger),
        "head_event_sha256": previous_hash,
        "unique_event_ids": len(seen),
        "authorization_granted": False,
        "task_state_changed": False,
        "gate_closure_approved": False,
    }


def append_event(
    ledger: list[dict[str, Any]],
    *,
    event_id: str,
    event_type: str,
    task_id: str,
    task_definition_sha256: str,
    occurred_at_utc: str,
    source: str,
    source_ref: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Return a new ledger with one event, or a no-op for an exact event replay.

    The caller-supplied event ID must come from a stable upstream delivery ID.
    Replays with the same ID and same event facts are idempotent; reuse of an
    ID for different facts is rejected. The function performs no file I/O.
    """
    validate_event_ledger(ledger)
    proposed_core = {
        "event_id": event_id,
        "event_type": event_type,
        "task_id": task_id,
        "task_definition_sha256": task_definition_sha256,
        "occurred_at_utc": occurred_at_utc,
        "source": source,
        "source_ref": source_ref,
        "payload": _strict_json_copy(payload),
    }
    # Validate all caller-controlled fields before considering replay.
    provisional = {
        **proposed_core,
        "previous_event_sha256": None,
        "event_sha256": "0" * 64,
    }
    _validate_event_shape(provisional)
    for existing in ledger:
        if existing["event_id"] == event_id:
            if _event_core(existing) == proposed_core:
                return {
                    "ledger": _strict_json_copy(ledger),
                    "event": _strict_json_copy(existing),
                    "appended": False,
                    "duplicate_replay": True,
                    "authorization_granted": False,
                    "task_state_changed": False,
                }
            raise ValueError("Event ID was reused with different event facts.")

    previous_hash = ledger[-1]["event_sha256"] if ledger else None
    unsigned = {**proposed_core, "previous_event_sha256": previous_hash}
    event = {**unsigned, "event_sha256": _event_digest(unsigned)}
    updated = _strict_json_copy(ledger)
    updated.append(event)
    validate_event_ledger(updated)
    return {
        "ledger": updated,
        "event": _strict_json_copy(event),
        "appended": True,
        "duplicate_replay": False,
        "authorization_granted": False,
        "task_state_changed": False,
    }
