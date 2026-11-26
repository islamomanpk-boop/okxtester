#!/usr/bin/env python3
"""Pure G0-05 causal candidate contract primitives; no market-data generation."""
from __future__ import annotations
import hashlib
import json

MINUTE_MS = 60_000
FIFTEEN_MIN_MS = 900_000
FOUR_HOUR_MS = 14_400_000
FAILURE_HORIZON_MS = 12 * 60 * MINUTE_MS

FAMILY_SIDE = {
    "SUPPORT_REJECTION": ("LOWER", "LONG"),
    "RESISTANCE_REJECTION": ("UPPER", "SHORT"),
    "BREAKOUT_CONTINUATION_UPPER": ("UPPER", "LONG"),
    "BREAKOUT_CONTINUATION_LOWER": ("LOWER", "SHORT"),
    "FAILED_UPPER_BREAKOUT": ("UPPER", "SHORT"),
    "FAILED_LOWER_BREAKOUT": ("LOWER", "LONG"),
}

REJECTED_REASON_CODES = frozenset({
    "CAUSAL_THRESHOLD_WARMUP",
    "CAUSAL_REGIME_NOT_ELIGIBLE",
    "SNAPSHOT_NOT_AVAILABLE_AT_SIGNAL",
    "SOURCE_HASH_MISMATCH",
    "MISSING_SOURCE_IDENTITY",
    "SOURCE_JOIN_UNMATCHED",
    "DUPLICATE_SOURCE_IDENTITY",
    "DUPLICATE_CANDIDATE_ID",
    "INVALID_SOURCE_SCHEMA",
    "INVALID_FEATURE_VALUES",
    "FUTURE_CONTEXT_ASSIGNED",
    "DIRECTION_MAPPING_MISMATCH",
    "NO_VALID_SOURCE_BREAKOUT",
    "INCOMPLETE_CONFIRMATION_BAR",
})
EXPIRED_REASON_CODES = frozenset({
    "EXPIRED_NO_RETURN_INSIDE_WITHIN_12H",
    "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION",
})
CENSORED_REASON_CODES = frozenset({
    "MISSING_OR_GAPPED_MINUTES",
    "INCOMPLETE_15M_CONFIRMATION",
    "SOURCE_END_BEFORE_RESOLUTION",
    "AMBIGUOUS_CONFIRMATION_UNRESOLVED",
})
DISPOSITION_STATUSES = frozenset({
    "ELIGIBLE_FOR_FURTHER_VALIDATION", "REJECTED", "EXPIRED", "CENSORED",
})


def snapshot_is_valid(snapshot_available_ms: int, snapshot_next_ms: int,
                      confirmation_ms: int) -> bool:
    """Snapshot validity is [available, next_available), through confirmation."""
    if snapshot_next_ms <= snapshot_available_ms:
        raise ValueError("snapshot validity interval must be positive")
    return snapshot_available_ms <= confirmation_ms < snapshot_next_ms


def rejection_confirmation(rejection_bar_open_ms: int) -> int:
    return int(rejection_bar_open_ms) + FIFTEEN_MIN_MS


def first_eligible_minute(signal_available_ms: int, observed_minute_opens: list[int]) -> int:
    """Require exact minute at availability; never shift to a nearby bar."""
    if not observed_minute_opens:
        raise ValueError("no post-confirmation minute bars")
    if observed_minute_opens[0] != signal_available_ms:
        raise ValueError("first post-confirmation minute must open exactly at availability")
    if any(b - a != MINUTE_MS for a, b in zip(observed_minute_opens, observed_minute_opens[1:])):
        raise ValueError("minute bars contain a gap, duplicate, or out-of-order timestamp")
    return observed_minute_opens[0]


def causal_regime_eligible(channel_width_pct: float, threshold_pct: float,
                           efficiency: float, overlap: float) -> bool:
    """Apply the frozen same-snapshot sideways detector conditions."""
    values = (channel_width_pct, threshold_pct, efficiency, overlap)
    if not all(map(lambda x: isinstance(x, (int, float)) and x == x and abs(x) != float("inf"), values)):
        raise ValueError("regime features and threshold must be finite numeric values")
    return channel_width_pct <= threshold_pct and efficiency <= 0.30 and overlap >= 0.70


def validate_strict_broad_nesting(strict_flags: list[bool], broad_flags: list[bool]) -> None:
    if len(strict_flags) != len(broad_flags):
        raise ValueError("strict and broad populations must have equal lengths")
    if any(strict and not broad for strict, broad in zip(strict_flags, broad_flags)):
        raise ValueError("strict cohort is not nested within broad cohort")


def rejection_physical_identity(row: dict) -> str:
    """Underlying boundary test identity; historical definition is cohort membership."""
    required = ("asset", "direction", "snapshot_index", "segment_id", "test_rank", "test_start_ts_ms")
    if any(key not in row or row[key] is None for key in required):
        raise ValueError("rejection physical identity is incomplete")
    return "|".join((str(row["asset"]), str(row["direction"]).upper(),
                     str(int(row["snapshot_index"])), str(int(row["segment_id"])),
                     str(int(row["test_rank"])), str(int(row["test_start_ts_ms"]))))


def collapse_rejection_cohort_rows(rows: list[dict]) -> list[dict]:
    """Collapse strict/broad duplicate source rows to one physical event without losing row IDs."""
    grouped = {}
    for row in rows:
        definition = str(row.get("definition", "")).upper()
        if definition not in ("BROAD_P40", "STRICT_P25"):
            raise ValueError("unknown historical cohort definition")
        row_id = row.get("event_id")
        if not row_id:
            raise ValueError("missing immutable source event_id")
        identity = rejection_physical_identity(row)
        item = grouped.setdefault(identity, {})
        if definition in item:
            raise ValueError("duplicate physical event cohort membership")
        item[definition] = str(row_id)
    collapsed = []
    for identity, memberships in sorted(grouped.items()):
        if "BROAD_P40" not in memberships:
            raise ValueError("strict historical cohort is not nested within broad")
        collapsed.append({
            "source_event_id": identity,
            "source_event_row_ids": [memberships[k] for k in ("BROAD_P40", "STRICT_P25") if k in memberships],
            "historical_cohort_memberships": [k for k in ("BROAD_P40", "STRICT_P25") if k in memberships],
        })
    return collapsed


def causal_rejection_disposition(snapshot_available_ms: int, snapshot_next_ms: int,
                                 rejection_bar_open_ms: int, confirmation_ms: int,
                                 threshold_p25: float | None, threshold_p40: float | None,
                                 channel_width_pct: float, efficiency: float,
                                 overlap: float) -> str:
    """Return source-only causal disposition; no candidate or order is created."""
    if snapshot_next_ms <= snapshot_available_ms:
        raise ValueError("snapshot validity interval must be positive")
    if snapshot_available_ms > rejection_bar_open_ms:
        raise ValueError("snapshot was not available at rejection bar open")
    if confirmation_ms != rejection_bar_open_ms + FIFTEEN_MIN_MS:
        raise ValueError("rejection confirmation must be completed 15-minute close")
    if confirmation_ms >= snapshot_next_ms:
        return "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION"
    if threshold_p25 is None and threshold_p40 is None:
        return "CAUSAL_THRESHOLD_WARMUP"
    if threshold_p25 is None or threshold_p40 is None:
        raise ValueError("both causal threshold quantiles must be present")
    values = (threshold_p25, threshold_p40, channel_width_pct, efficiency, overlap)
    if not all(map(lambda x: isinstance(x, (int, float)) and x == x and abs(x) != float("inf"), values)):
        raise ValueError("causal threshold and detector values must be finite")
    if threshold_p25 > threshold_p40:
        raise ValueError("P25 threshold cannot exceed P40")
    if efficiency > 0.30 or overlap < 0.70:
        return "CAUSAL_REGIME_NOT_ELIGIBLE"
    if channel_width_pct <= threshold_p25:
        return "CAUSAL_STRICT_ELIGIBLE"
    if channel_width_pct <= threshold_p40:
        return "CAUSAL_BROAD_ONLY_ELIGIBLE"
    return "CAUSAL_REGIME_NOT_ELIGIBLE"


def family_side(family: str) -> tuple[str, str]:
    try:
        return FAMILY_SIDE[family]
    except KeyError as exc:
        raise ValueError(f"unknown candidate family: {family}") from exc


def complete_15m_confirmation(minute_open_timestamps: list[int], bar_open_ms: int) -> int:
    """Return close-availability time only for exactly 15 consecutive minute opens."""
    expected = [bar_open_ms + i * MINUTE_MS for i in range(15)]
    if minute_open_timestamps != expected:
        raise ValueError("15-minute confirmation requires exactly 15 consecutive component minutes")
    return bar_open_ms + FIFTEEN_MIN_MS


def failed_breakout_confirmation(direction: str, close: float, boundary: float,
                                 confirmation_ms: int, signal_ms: int,
                                 source_candidate_valid: bool) -> dict:
    if not source_candidate_valid:
        raise ValueError("failed-breakout reversal requires a valid linked source breakout")
    if direction not in ("UPPER", "LOWER"):
        raise ValueError("direction must be UPPER or LOWER")
    if confirmation_ms <= signal_ms:
        raise ValueError("failure confirmation must follow source breakout availability")
    if confirmation_ms > signal_ms + FAILURE_HORIZON_MS:
        raise ValueError("failed-breakout confirmation is outside the 12-hour observation horizon")
    returned_inside = close <= boundary if direction == "UPPER" else close >= boundary
    if not returned_inside:
        raise ValueError("completed 15-minute close has not returned inside the original range")
    family = "FAILED_UPPER_BREAKOUT" if direction == "UPPER" else "FAILED_LOWER_BREAKOUT"
    boundary_side, side = family_side(family)
    return {"family": "FAILED_BREAKOUT_REVERSAL", "boundary_side": boundary_side,
            "side": side, "signal_available_at_ts_ms": confirmation_ms,
            "source_breakout_signal_ts_ms": signal_ms}


def candidate_id(source_identity: str, family: str, rule_version: str) -> str:
    if not source_identity or not family or not rule_version:
        raise ValueError("candidate identity inputs must be non-empty")
    payload = "\x1f".join((source_identity, family, rule_version)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_candidate_identity_links(records: list[dict]) -> dict:
    """Validate deterministic candidate IDs and failed-breakout source-candidate links."""
    if not records:
        raise ValueError("candidate ledger must not be empty")
    candidate_ids = set()
    family_source_ids = set()
    versions = set()
    family_counts = {}
    for row in records:
        source_identity = str(row.get("source_event_id", "")).strip()
        family = str(row.get("family", "")).strip()
        rule_version = str(row.get("candidate_rule_version", "")).strip()
        supplied_id = str(row.get("candidate_id", "")).strip()
        if not source_identity or not family or not rule_version or not supplied_id:
            raise ValueError("candidate identity record is missing a required field")
        if supplied_id in candidate_ids:
            raise ValueError("duplicate candidate_id")
        expected_id = candidate_id(source_identity, family, rule_version)
        if supplied_id != expected_id:
            raise ValueError("candidate_id does not match its deterministic source identity")
        source_key = (family, source_identity)
        if source_key in family_source_ids:
            raise ValueError("duplicate family/source_event_id")
        candidate_ids.add(supplied_id)
        family_source_ids.add(source_key)
        versions.add(rule_version)
        family_counts[family] = family_counts.get(family, 0) + 1
    if len(versions) != 1:
        raise ValueError("candidate ledger mixes candidate_rule_version values")

    for row in records:
        family = row["family"]
        linked = row.get("source_breakout_candidate_id")
        if family == "FAILED_BREAKOUT_REVERSAL":
            source_breakout_identity = str(row.get("source_breakout_source_event_id", "")).strip()
            if not source_breakout_identity or not linked:
                raise ValueError("failed-breakout row is missing its source breakout link")
            expected_link = candidate_id(
                source_breakout_identity, "BREAKOUT_CONTINUATION", row["candidate_rule_version"])
            if linked != expected_link:
                raise ValueError("source_breakout_candidate_id does not match the exact source breakout identity")
            if expected_link not in candidate_ids:
                raise ValueError("source_breakout_candidate_id does not resolve to a source breakout candidate row")
            confirmation_ts = str(row.get("signal_available_at_ts_ms") or "NO_CONFIRMATION")
            expected_failed_identity = (
                f"{linked}|{confirmation_ts}|{row['candidate_rule_version']}")
            if row["source_event_id"] != expected_failed_identity:
                raise ValueError("failed-breakout source_event_id does not match linked candidate, confirmation and rule version")
        elif linked not in (None, "", "NOT_APPLICABLE"):
            raise ValueError("non-failed-breakout row must not carry a source breakout candidate link")

    return {
        "candidate_rows": len(records),
        "candidate_ids_unique": True,
        "source_event_ids_unique_within_family": True,
        "candidate_rule_version": next(iter(versions)),
        "family_counts": dict(sorted(family_counts.items())),
        "failed_breakout_source_links_validated": sum(
            1 for row in records if row["family"] == "FAILED_BREAKOUT_REVERSAL"),
    }


def classify_disposition(snapshot_available_ms: int, snapshot_next_ms: int,
                         confirmation_ms: int) -> str:
    return ("ELIGIBLE_FOR_FURTHER_VALIDATION"
            if snapshot_is_valid(snapshot_available_ms, snapshot_next_ms, confirmation_ms)
            else "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION")


def exact_threshold_for_snapshot(threshold_by_key: dict, asset: str,
                                 snapshot_ms: int, policy: str,
                                 population: str) -> dict | None:
    """Return only the exact asset/snapshot/policy/population threshold; never use a neighbor."""
    snapshot = int(snapshot_ms)
    row = threshold_by_key.get((asset, snapshot, policy, population))
    if row is None:
        return None
    if int(row["last_prior_context_ms"]) >= snapshot:
        raise ValueError("threshold calibration must end strictly before snapshot")
    if int(row["prior_context_count"]) < 180:
        raise ValueError("threshold requires at least 180 prior contexts")
    return row


def validate_source_key_join(expected_keys: list, observed_keys: list,
                             exact: bool = True) -> bool:
    """Require unique keys and either exact equality or expected-key subset coverage."""
    expected = list(expected_keys)
    observed = list(observed_keys)
    if len(expected) != len(set(expected)):
        raise ValueError("duplicate expected source identity")
    if len(observed) != len(set(observed)):
        raise ValueError("duplicate observed source identity")
    missing = set(expected) - set(observed)
    extra = set(observed) - set(expected)
    if missing or (exact and extra):
        raise ValueError(
            f"source identity reconciliation mismatch: missing={len(missing)}, extra={len(extra)}"
        )
    return True


def validate_disposition_reason(status: str, exclusion_reason: str,
                                censoring_reason: str = "") -> bool:
    """Enforce the frozen candidate status/reason-code contract."""
    reason = (exclusion_reason or "").strip()
    censor = (censoring_reason or "").strip()
    if status not in DISPOSITION_STATUSES:
        raise ValueError(f"unknown candidate status: {status}")
    if status == "ELIGIBLE_FOR_FURTHER_VALIDATION":
        if reason != "NONE" or censor:
            raise ValueError("eligible rows require exclusion_reason=NONE and no censoring_reason")
    elif status == "REJECTED":
        if reason not in REJECTED_REASON_CODES or censor:
            raise ValueError("rejected row has invalid exclusion or censoring reason")
    elif status == "EXPIRED":
        if reason not in EXPIRED_REASON_CODES or censor:
            raise ValueError("expired row has invalid exclusion or censoring reason")
    elif status == "CENSORED":
        if reason not in CENSORED_REASON_CODES or censor != reason:
            raise ValueError("censored row requires matching non-empty exclusion and censoring reasons")
    return True


def deterministic_json(rows: list[dict]) -> str:
    """Stable serialization helper for substantive output comparisons."""
    return json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def exact_first_minute_disposition(availability_ms: int, observed_minute_opens: set[int]) -> str:
    """Require the exact 1m bar open at availability; never shift to a neighbor."""
    if availability_ms % MINUTE_MS:
        raise ValueError("availability must align to an exact minute boundary")
    return ("EXACT_FIRST_MINUTE_AVAILABLE" if availability_ms in observed_minute_opens
            else "MISSING_OR_GAPPED_MINUTES")


def failed_breakout_horizon_disposition(signal_ms: int, confirmation_ms: int | None,
                                        complete_12h: bool) -> str:
    """Classify the observed 12h source horizon without inventing a failure."""
    if confirmation_ms is None:
        return ("EXPIRED_NO_RETURN_INSIDE_WITHIN_12H" if complete_12h
                else "CENSORED_SOURCE_END_BEFORE_RESOLUTION")
    if confirmation_ms <= signal_ms:
        raise ValueError("failure confirmation must follow source breakout")
    if confirmation_ms > signal_ms + FAILURE_HORIZON_MS:
        raise ValueError("failure confirmation is outside the 12-hour horizon")
    return "CONFIRMED_WITHIN_12H"
