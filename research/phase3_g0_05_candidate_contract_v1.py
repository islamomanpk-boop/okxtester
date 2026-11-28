#!/usr/bin/env python3
"""Pure G0-05 causal candidate contract primitives; no market-data generation."""
from __future__ import annotations
import hashlib
import math
import re
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

CANONICAL_REQUIRED_FIELDS = frozenset({
    "candidate_id", "source_event_id", "source_event_row_ids", "family",
    "instrument_id", "asset", "side", "boundary_side",
    "regime_definition_version", "candidate_rule_version", "source_pipeline_version",
    "historical_cohort_memberships", "causal_cohort_label",
    "overlap_cluster_id", "overlap_cluster_size", "overlap_window_start_ts_ms",
    "overlap_window_end_ts_ms", "repeated_signal_group_id",
    "snapshot_id", "snapshot_available_at_ts_ms", "snapshot_valid_from_ts_ms",
    "snapshot_valid_until_ts_ms", "frozen_upper_boundary", "frozen_lower_boundary",
    "channel_width_pct", "threshold_policy_id", "threshold_population_id",
    "threshold_value", "threshold_percentile", "threshold_calibration_start_ts_ms",
    "threshold_calibration_end_ts_ms", "threshold_prior_observation_count",
    "efficiency_value", "efficiency_limit", "overlap_value", "overlap_minimum",
    "source_file_paths", "source_git_blob_ids", "source_sha256_manifest_id",
    "signal_candle_open_ts_ms", "signal_candle_close_ts_ms",
    "signal_available_at_ts_ms", "confirmation_rule_id",
    "confirmation_bar_interval_ms", "confirmation_status",
    "first_eligible_execution_bar_open_ts_ms", "event_observed_at_ts_ms",
    "ambiguity_flags", "decluster_policy_id", "candidate_status",
    "exclusion_reason", "censoring_reason", "invalidation_reference_type",
    "invalidation_reference_value", "invalidation_reference_ts_ms",
    "expiry_rule_id", "expiry_ts_ms", "source_breakout_candidate_id",
    "source_reconciliation_status", "source_join_cardinality",
})

COHORT_LABELS = frozenset({
    "STRICT_P25", "BROAD_ONLY", "NOT_ELIGIBLE", "WARMUP", "NOT_APPLICABLE",
})
CONFIRMATION_STATUSES = frozenset({
    "CONFIRMED", "NOT_CONFIRMED", "CENSORED", "NOT_APPLICABLE",
})
SOURCE_RECONCILIATION_STATUSES = frozenset({
    "EXACT_SOURCE_MATCH", "EXACT_PHYSICAL_EVENT_COLLAPSE",
    "DECLARED_SUBSET_MATCH", "EXACT_LINKED_SOURCE_BREAKOUT",
})
SOURCE_JOIN_CARDINALITIES = frozenset({
    "ONE_RAW_CROSSING_TO_ONE_DISPOSITION",
    "ONE_PHYSICAL_EVENT_TO_ONE_OR_TWO_COHORT_ROWS",
    "ONE_FAILED_BREAKOUT_TO_ONE_SOURCE_BREAKOUT",
})
AMBIGUITY_FLAGS = frozenset({
    "NONE", "CONFIRMATION_CANDLE_OPEN_OUTSIDE_CLOSE_INSIDE",
    "CONFIRMATION_CANDLE_WICK_OUTSIDE_CLOSE_INSIDE",
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
    if confirmation_ms >= signal_ms + FAILURE_HORIZON_MS:
        raise ValueError("failed-breakout confirmation is outside the half-open 12-hour observation horizon")
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


def _finite_number(value, field: str, allow_none: bool = False) -> bool:
    if value is None and allow_none:
        return True
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValueError(f"{field} must be a finite number")
    return True


def validate_canonical_candidate_record(row: dict) -> None:
    """Validate one fully serialized canonical G0-05 candidate/disposition record."""
    missing = CANONICAL_REQUIRED_FIELDS - set(row)
    if missing:
        raise ValueError(f"canonical candidate missing required fields: {sorted(missing)}")
    family = row["family"]
    family_sides = {
        "SUPPORT_REJECTION": ("LOWER", "LONG"),
        "RESISTANCE_REJECTION": ("UPPER", "SHORT"),
        "BREAKOUT_CONTINUATION": None,
        "FAILED_BREAKOUT_REVERSAL": None,
    }
    if family not in family_sides:
        raise ValueError("unknown canonical candidate family")
    asset = row["asset"]
    if asset not in {"BTC", "ETH", "SOL", "DOGE", "AVAX"}:
        raise ValueError("unknown candidate asset")
    if row["instrument_id"] != f"{asset}-USDT-SWAP":
        raise ValueError("instrument_id does not match frozen OKX asset mapping")
    side = row["side"]
    boundary = row["boundary_side"]
    expected_pairs = {
        "SUPPORT_REJECTION": {("LOWER", "LONG")},
        "RESISTANCE_REJECTION": {("UPPER", "SHORT")},
        "BREAKOUT_CONTINUATION": {("UPPER", "LONG"), ("LOWER", "SHORT")},
        "FAILED_BREAKOUT_REVERSAL": {("UPPER", "SHORT"), ("LOWER", "LONG")},
    }
    if (boundary, side) not in expected_pairs[family]:
        raise ValueError("family, boundary_side and side mapping mismatch")
    expected_regime = (
        "SIDEWAYS_DETECTOR_ORIGINAL_V1"
        if family in {"SUPPORT_REJECTION", "RESISTANCE_REJECTION"}
        else "HISTORICAL_BREAKOUT_CONTEXT_V1"
    )
    if row["regime_definition_version"] != expected_regime:
        raise ValueError("regime_definition_version does not match family")
    if row["candidate_rule_version"] != "G0_05_CANDIDATE_RULE_V1":
        raise ValueError("candidate_rule_version mismatch")
    if row["source_pipeline_version"] != "G0_04_CAUSAL_RECONSTRUCTION_V1+MODULE_A_V1_1+MODULE_B_V1_1":
        raise ValueError("source_pipeline_version mismatch")
    if row["causal_cohort_label"] not in COHORT_LABELS:
        raise ValueError("invalid causal_cohort_label")
    source_row_ids = row["source_event_row_ids"]
    if (not isinstance(source_row_ids, list) or not source_row_ids
            or any(not isinstance(value, str) or not value.strip() for value in source_row_ids)):
        raise ValueError("source_event_row_ids must be a non-empty list of non-empty strings")
    if len(set(source_row_ids)) != len(source_row_ids):
        raise ValueError("source_event_row_ids contain duplicates")
    memberships = row["historical_cohort_memberships"]
    if not isinstance(memberships, list):
        raise ValueError("historical_cohort_memberships must be a list")
    if any(not isinstance(value, str) or not value.strip() for value in memberships):
        raise ValueError("historical_cohort_memberships must contain non-empty strings")
    if not set(memberships).issubset({"BROAD_P40", "STRICT_P25"}):
        raise ValueError("invalid historical_cohort_memberships")
    if len(set(memberships)) != len(memberships):
        raise ValueError("historical_cohort_memberships contain duplicates")
    if not isinstance(row["source_event_id"], str) or not row["source_event_id"] or not isinstance(row["candidate_id"], str):
        raise ValueError("candidate/source event identity is blank")
    if not re.fullmatch(r"[0-9a-f]{64}", row["candidate_id"]):
        raise ValueError("candidate_id must be a SHA-256 hex digest")
    if row["candidate_id"] != candidate_id(
        row["source_event_id"], family, row["candidate_rule_version"]):
        raise ValueError("candidate_id does not match deterministic identity")
    if row["snapshot_id"] != f"{asset}|{int(row['snapshot_available_at_ts_ms'])}":
        raise ValueError("snapshot_id does not match asset and availability timestamp")
    for field in ("snapshot_available_at_ts_ms", "snapshot_valid_from_ts_ms",
                  "snapshot_valid_until_ts_ms", "signal_candle_open_ts_ms",
                  "signal_candle_close_ts_ms", "signal_available_at_ts_ms",
                  "event_observed_at_ts_ms", "overlap_window_start_ts_ms",
                  "overlap_window_end_ts_ms"):
        value = row[field]
        if value is not None and (isinstance(value, bool) or not isinstance(value, int)):
            raise ValueError(f"{field} must be an integer timestamp or null")
    if any(row[field] is None for field in ("snapshot_available_at_ts_ms", "snapshot_valid_from_ts_ms",
                                             "snapshot_valid_until_ts_ms", "event_observed_at_ts_ms",
                                             "overlap_window_start_ts_ms", "overlap_window_end_ts_ms")):
        raise ValueError("snapshot, event and overlap-window timestamps cannot be null")
    if row["snapshot_valid_from_ts_ms"] != row["snapshot_available_at_ts_ms"]:
        raise ValueError("snapshot_valid_from must equal snapshot availability")
    if row["snapshot_valid_until_ts_ms"] <= row["snapshot_available_at_ts_ms"]:
        raise ValueError("snapshot validity interval must be positive")
    for field in ("frozen_upper_boundary", "frozen_lower_boundary", "channel_width_pct",
                  "efficiency_limit", "overlap_minimum"):
        _finite_number(row[field], field)
    if row["frozen_upper_boundary"] <= row["frozen_lower_boundary"]:
        raise ValueError("frozen upper boundary must exceed lower boundary")
    if row["channel_width_pct"] < 0 or row["efficiency_limit"] != 0.30 or row["overlap_minimum"] != 0.70:
        raise ValueError("invalid frozen feature limits")
    _finite_number(row["efficiency_value"], "efficiency_value", allow_none=True)
    _finite_number(row["overlap_value"], "overlap_value", allow_none=True)
    if row["threshold_policy_id"] != "EXPANDING_PRIOR" or row["threshold_population_id"] != "UNIQUE_4H_FEATURE_ROWS":
        raise ValueError("threshold policy/population mismatch")
    threshold_fields = (
        row["threshold_value"], row["threshold_percentile"],
        row["threshold_calibration_start_ts_ms"], row["threshold_calibration_end_ts_ms"],
        row["threshold_prior_observation_count"],
    )
    if row["threshold_value"] is None:
        if any(value is not None for value in threshold_fields[1:]):
            raise ValueError("null threshold value requires all threshold metadata null")
    else:
        _finite_number(row["threshold_value"], "threshold_value")
        if row["causal_cohort_label"] == "WARMUP":
            raise ValueError("WARMUP candidates must not carry threshold metadata")
        if type(row["threshold_percentile"]) is not int or row["threshold_percentile"] not in (25, 40):
            raise ValueError("threshold_percentile must be 25 or 40")
        if type(row["threshold_calibration_start_ts_ms"]) is not int or type(row["threshold_calibration_end_ts_ms"]) is not int:
            raise ValueError("threshold calibration bounds must be integer timestamps")
        if row["threshold_calibration_start_ts_ms"] >= row["threshold_calibration_end_ts_ms"]:
            raise ValueError("threshold calibration start must precede end")
        if row["threshold_calibration_end_ts_ms"] >= row["snapshot_available_at_ts_ms"]:
            raise ValueError("threshold calibration must end before snapshot")
        if type(row["threshold_prior_observation_count"]) is not int or row["threshold_prior_observation_count"] < 180:
            raise ValueError("threshold prior observation count must be at least 180")
        expected_percentile = 25 if row["causal_cohort_label"] == "STRICT_P25" else 40
        if row["threshold_percentile"] != expected_percentile:
            raise ValueError("threshold percentile does not match causal cohort label")
    if "STRICT_P25" in memberships and "BROAD_P40" not in memberships:
        raise ValueError("strict historical cohort membership requires broad historical membership")
    label = row["causal_cohort_label"]
    if label in {"STRICT_P25", "BROAD_ONLY", "NOT_ELIGIBLE"}:
        if row["threshold_value"] is None:
            raise ValueError("evaluated causal cohort label requires threshold provenance")
        if row["efficiency_value"] is None or row["overlap_value"] is None:
            raise ValueError("evaluated causal cohort label requires efficiency and overlap measurements")
        width_passes = row["channel_width_pct"] <= row["threshold_value"]
        efficiency_passes = row["efficiency_value"] <= row["efficiency_limit"]
        overlap_passes = row["overlap_value"] >= row["overlap_minimum"]
        if label == "STRICT_P25" and not (width_passes and efficiency_passes and overlap_passes):
            raise ValueError("STRICT_P25 label conflicts with canonical regime feature thresholds")
        if label == "BROAD_ONLY" and not (width_passes and efficiency_passes and overlap_passes):
            raise ValueError("BROAD_ONLY label conflicts with canonical broad regime thresholds")
        if label == "NOT_ELIGIBLE" and (width_passes and efficiency_passes and overlap_passes):
            raise ValueError("NOT_ELIGIBLE label has no failing broad regime condition")
    # BROAD_ONLY cannot be proven to exceed P25 from this row alone: only the selected P40 is serialized.
    # Rejection rows use the sideways detector regime; breakout families use historical breakout context.
    for field in ("source_file_paths", "source_git_blob_ids"):
        values = row[field]
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v for v in values):
            raise ValueError(f"{field} must be a non-empty list of strings")
        if len(set(values)) != len(values):
            raise ValueError(f"{field} contains duplicates")
    if any(not re.fullmatch(r"[0-9a-f]{40}", value) for value in row["source_git_blob_ids"]):
        raise ValueError("source_git_blob_ids must contain Git SHA-1 blob IDs")
    if not re.fullmatch(r"[0-9a-f]{64}", str(row["source_sha256_manifest_id"])):
        raise ValueError("source_sha256_manifest_id must be a SHA-256 hex digest")
    if row["confirmation_bar_interval_ms"] != FIFTEEN_MIN_MS:
        raise ValueError("confirmation bar interval must be 15 minutes")
    if row["confirmation_status"] not in CONFIRMATION_STATUSES:
        raise ValueError("invalid confirmation_status")
    expected_confirmation_rule = {
        "SUPPORT_REJECTION": "STRONG_REJECTION_15M_CLOSE_V1",
        "RESISTANCE_REJECTION": "STRONG_REJECTION_15M_CLOSE_V1",
        "BREAKOUT_CONTINUATION": "BOUNDARY_CROSSING_15M_CLOSE_V1",
        "FAILED_BREAKOUT_REVERSAL": "RETURN_INSIDE_15M_CLOSE_V1",
    }[family]
    if row["confirmation_rule_id"] != expected_confirmation_rule:
        raise ValueError("confirmation_rule_id does not match family")
    if row["signal_candle_open_ts_ms"] is None:
        if family != "FAILED_BREAKOUT_REVERSAL" or row["confirmation_status"] not in {"NOT_CONFIRMED", "CENSORED"}:
            raise ValueError("only unresolved failed-breakout rows may omit confirmation candle timestamps")
        if row["signal_candle_close_ts_ms"] is not None or row["signal_available_at_ts_ms"] is not None:
            raise ValueError("unconfirmed failed-breakout row must omit all signal candle timestamps")
    else:
        if row["signal_candle_close_ts_ms"] is None or row["signal_available_at_ts_ms"] is None:
            raise ValueError("completed signal candle requires close and availability timestamps")
        if row["signal_candle_close_ts_ms"] - row["signal_candle_open_ts_ms"] != FIFTEEN_MIN_MS:
            raise ValueError("signal candle must be exactly 15 minutes")
        if (row["signal_candle_open_ts_ms"] % FIFTEEN_MIN_MS != 0
                or row["signal_candle_close_ts_ms"] % FIFTEEN_MIN_MS != 0):
            raise ValueError("completed 15m candle timestamps must be quarter-hour aligned")
        if row["signal_available_at_ts_ms"] != row["signal_candle_close_ts_ms"]:
            raise ValueError("signal availability must equal completed 15m close")
        if row["event_observed_at_ts_ms"] != row["signal_available_at_ts_ms"]:
            raise ValueError("confirmed event observation must equal completed signal availability")
    ambiguity_flags = row["ambiguity_flags"]
    if not isinstance(ambiguity_flags, list):
        raise ValueError("ambiguity_flags must be a list")
    if any(not isinstance(value, str) or not value.strip() for value in ambiguity_flags):
        raise ValueError("ambiguity_flags must contain non-empty strings")
    if not set(ambiguity_flags).issubset(AMBIGUITY_FLAGS):
        raise ValueError("invalid ambiguity_flags")
    if len(set(ambiguity_flags)) != len(ambiguity_flags):
        raise ValueError("ambiguity_flags contain duplicates")
    if "NONE" in ambiguity_flags and len(ambiguity_flags) != 1:
        raise ValueError("NONE cannot be combined with ambiguity flags")
    if type(row["overlap_cluster_size"]) is not int or row["overlap_cluster_size"] < 1:
        raise ValueError("overlap_cluster_size must be a positive integer")
    if row["overlap_window_end_ts_ms"] <= row["overlap_window_start_ts_ms"]:
        raise ValueError("overlap cluster window must have positive duration")
    if not row["overlap_cluster_id"] or not row["repeated_signal_group_id"]:
        raise ValueError("dependence metadata IDs must be non-empty")
    if row["decluster_policy_id"] != "G0_05_INTERVAL_GRAPH_METADATA_V1":
        raise ValueError("decluster_policy_id mismatch")
    if row["signal_candle_open_ts_ms"] is None and row["confirmation_status"] == "CONFIRMED":
        raise ValueError("confirmed event must carry its completed confirmation candle")
    if row["signal_candle_open_ts_ms"] is not None and row["confirmation_status"] != "CONFIRMED":
        raise ValueError("observed confirmation candle must have CONFIRMED status")
    status = row["candidate_status"]
    reason = row["exclusion_reason"]
    if status not in DISPOSITION_STATUSES:
        raise ValueError("invalid candidate_status")
    if status == "ELIGIBLE_FOR_FURTHER_VALIDATION":
        if (reason != "NONE" or type(row["first_eligible_execution_bar_open_ts_ms"]) is not int
                or row["first_eligible_execution_bar_open_ts_ms"] != row["signal_available_at_ts_ms"]):
            raise ValueError("eligible candidate requires NONE reason and exact first eligible minute")
        if (family != "FAILED_BREAKOUT_REVERSAL"
                and not snapshot_is_valid(
                    row["snapshot_available_at_ts_ms"], row["snapshot_valid_until_ts_ms"],
                    row["signal_available_at_ts_ms"])):
            raise ValueError("eligible rejection/breakout signal must fall inside snapshot validity")
    else:
        if row["first_eligible_execution_bar_open_ts_ms"] is not None:
            raise ValueError("non-eligible candidate must not expose a first eligible minute")
    if status != "ELIGIBLE_FOR_FURTHER_VALIDATION" and (reason == "NONE" or reason not in REJECTED_REASON_CODES | EXPIRED_REASON_CODES | CENSORED_REASON_CODES):
        raise ValueError("non-eligible candidate requires a controlled exclusion reason")
    censor = row["censoring_reason"]
    if status == "CENSORED":
        if censor != reason or censor not in CENSORED_REASON_CODES:
            raise ValueError("censored candidate requires matching controlled censoring reason")
    elif censor not in (None, ""):
        raise ValueError("censoring_reason must be blank unless status is CENSORED")
    if row["invalidation_reference_type"] != "NOT_APPLICABLE" or row["invalidation_reference_value"] != "NOT_APPLICABLE" or row["invalidation_reference_ts_ms"] != "NOT_APPLICABLE":
        raise ValueError("G0-05 point events must not invent invalidation references")
    if family == "FAILED_BREAKOUT_REVERSAL":
        if row["expiry_rule_id"] != "SOURCE_BREAKOUT_12H_RETURN_INSIDE_V1" or type(row["expiry_ts_ms"]) is not int:
            raise ValueError("failed-breakout row requires its source 12-hour expiry")
        if not re.fullmatch(r"[0-9a-f]{64}", str(row["source_breakout_candidate_id"])):
            raise ValueError("failed-breakout row requires a SHA-256 source_breakout_candidate_id")
    elif row["expiry_rule_id"] != "NOT_APPLICABLE" or row["expiry_ts_ms"] != "NOT_APPLICABLE":
        raise ValueError("rejection/continuation expiry fields must be NOT_APPLICABLE")
    if family != "FAILED_BREAKOUT_REVERSAL" and row["source_breakout_candidate_id"] != "NOT_APPLICABLE":
        raise ValueError("non-failed-breakout row must not link a source breakout candidate")
    if row["source_reconciliation_status"] not in SOURCE_RECONCILIATION_STATUSES:
        raise ValueError("invalid source_reconciliation_status")
    if row["source_join_cardinality"] not in SOURCE_JOIN_CARDINALITIES:
        raise ValueError("invalid source_join_cardinality")


def validate_canonical_candidate_ledger(records: list[dict]) -> dict:
    """Validate all canonical records and cross-row source-breakout identity links."""
    if not records:
        raise ValueError("canonical candidate ledger must not be empty")
    for row in records:
        validate_canonical_candidate_record(row)
    return validate_candidate_identity_links(records)


def _failed_breakout_confirmation_identity_timestamp(row: dict) -> str:
    """Use the completed confirmation time, or a censored observed time when no candle completed."""
    available = row.get("signal_available_at_ts_ms")
    if available not in (None, ""):
        return str(int(available))
    if (row.get("confirmation_status") == "CENSORED"
            and row.get("exclusion_reason", row.get("reason_code")) == "INCOMPLETE_15M_CONFIRMATION"):
        observed = row.get("event_observed_at_ts_ms")
        if observed in (None, ""):
            raise ValueError("incomplete confirmation identity lacks its observed timestamp")
        return str(int(observed))
    return "NO_CONFIRMATION"


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

    records_by_id = {row["candidate_id"]: row for row in records}
    for row in records:
        family = row["family"]
        linked = row.get("source_breakout_candidate_id")
        if family == "FAILED_BREAKOUT_REVERSAL":
            if not linked:
                raise ValueError("failed-breakout row is missing its source breakout link")
            source_breakout_row = records_by_id.get(linked)
            if source_breakout_row is None or source_breakout_row.get("family") != "BREAKOUT_CONTINUATION":
                raise ValueError("source_breakout_candidate_id does not resolve to a source breakout candidate row")
            confirmation_ts = _failed_breakout_confirmation_identity_timestamp(row)
            expected_failed_identity = (
                f"{linked}|{confirmation_ts}|{row['candidate_rule_version']}")
            if row["source_event_id"] != expected_failed_identity:
                raise ValueError("failed-breakout source_event_id does not match linked candidate, confirmation and rule version")
            source_signal_available = source_breakout_row.get("signal_available_at_ts_ms")
            if not isinstance(source_signal_available, int):
                raise ValueError("linked source breakout lacks a completed signal availability timestamp")
            if row.get("expiry_ts_ms") != source_signal_available + FAILURE_HORIZON_MS:
                raise ValueError("failed-breakout expiry does not match linked source breakout 12-hour horizon")
            expiry = source_signal_available + FAILURE_HORIZON_MS
            confirmation_status = row.get("confirmation_status")
            observed_at = row.get("event_observed_at_ts_ms")
            if confirmation_status == "CONFIRMED":
                confirmation_at = row.get("signal_available_at_ts_ms")
                if (type(confirmation_at) is not int
                        or not source_signal_available < confirmation_at < expiry
                        or observed_at != confirmation_at):
                    raise ValueError("failed-breakout confirmation must be observed strictly inside its source 12-hour horizon")
            elif confirmation_status == "NOT_CONFIRMED":
                if observed_at != expiry:
                    raise ValueError("unconfirmed failed-breakout must be observed at its 12-hour expiry")
            elif confirmation_status == "CENSORED":
                if not source_signal_available < observed_at < expiry:
                    raise ValueError("censored failed-breakout observation must fall strictly inside its source 12-hour horizon")
            else:
                raise ValueError("failed-breakout requires confirmed, not-confirmed or censored confirmation status")
            inherited_fields = (
                "asset", "instrument_id", "boundary_side", "regime_definition_version",
                "source_pipeline_version", "historical_cohort_memberships", "causal_cohort_label",
                "snapshot_id", "snapshot_available_at_ts_ms", "snapshot_valid_from_ts_ms",
                "snapshot_valid_until_ts_ms", "frozen_upper_boundary", "frozen_lower_boundary",
                "channel_width_pct", "threshold_policy_id", "threshold_population_id",
                "threshold_value", "threshold_percentile", "threshold_calibration_start_ts_ms",
                "threshold_calibration_end_ts_ms", "threshold_prior_observation_count",
                "efficiency_value", "efficiency_limit", "overlap_value", "overlap_minimum",
                "source_sha256_manifest_id", "repeated_signal_group_id", "overlap_cluster_id",
                "overlap_cluster_size", "overlap_window_start_ts_ms", "overlap_window_end_ts_ms",
            )
            for field in inherited_fields:
                if row.get(field) != source_breakout_row.get(field):
                    raise ValueError(f"failed-breakout candidate does not inherit source breakout {field}")
            opposite_side = {"LONG": "SHORT", "SHORT": "LONG"}.get(source_breakout_row.get("side"))
            if row.get("side") != opposite_side:
                raise ValueError("failed-breakout side must reverse the linked breakout side")
            if (source_breakout_row.get("candidate_status") != "ELIGIBLE_FOR_FURTHER_VALIDATION"
                    and row.get("candidate_status") == "ELIGIBLE_FOR_FURTHER_VALIDATION"):
                raise ValueError("failed-breakout candidate cannot be eligible when its source breakout is not eligible")
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


def _split_semicolon(value) -> list[str]:
    if value is None or str(value).strip() == "":
        return []
    return [part for part in str(value).split(";") if part != ""]


def _int_or_none(value):
    if value is None or str(value).strip() == "":
        return None
    return int(value)


def _float_or_none(value):
    if value is None or str(value).strip() == "":
        return None
    return float(value)


def _int_or_na(value):
    if value is None or str(value).strip() in {"", "NOT_APPLICABLE"}:
        return "NOT_APPLICABLE"
    return int(value)


def serialize_source_disposition_ledgers(rejection_rows: list[dict],
                                          breakout_rows: list[dict],
                                          failed_breakout_rows: list[dict]) -> list[dict]:
    """Serialize source-only rows into canonical records; caller must authorize invocation."""
    rule_version = "G0_05_CANDIDATE_RULE_V1"
    breakout_candidate_ids = {}
    for row in breakout_rows:
        source_identity = str(row.get("source_event_id", "")).strip()
        if not source_identity:
            raise ValueError("breakout source-only row has no source_event_id")
        if source_identity in breakout_candidate_ids:
            raise ValueError("duplicate breakout source_event_id in source-only ledger")
        breakout_candidate_ids[source_identity] = candidate_id(
            source_identity, "BREAKOUT_CONTINUATION", rule_version)

    def serialize(row: dict, failed: bool = False) -> dict:
        family = row["family"]
        source_breakout_candidate = "NOT_APPLICABLE"
        if failed:
            source_breakout_identity = str(row.get("source_breakout_source_event_id", "")).strip()
            source_breakout_candidate = breakout_candidate_ids.get(source_breakout_identity)
            if source_breakout_candidate is None:
                raise ValueError("failed-breakout row has no exact source breakout source-event row")
            confirmation = _failed_breakout_confirmation_identity_timestamp({
                "signal_available_at_ts_ms": row.get("signal_available_at_ts_ms"),
                "confirmation_status": row.get("confirmation_status"),
                "reason_code": row.get("reason_code"),
                "event_observed_at_ts_ms": row.get("event_observed_at_ts_ms"),
            })
            source_identity = f"{source_breakout_candidate}|{confirmation}|{rule_version}"
        else:
            source_identity = str(row["source_event_id"])
        status = row["disposition"]
        reason = "NONE" if status == "ELIGIBLE_FOR_FURTHER_VALIDATION" else row.get("reason_code") or ""
        censoring_reason = (row.get("censoring_reason") or reason) if status == "CENSORED" else None
        record = {
            "source_event_id": source_identity,
            "family": family,
            "candidate_rule_version": rule_version,
            "candidate_id": candidate_id(source_identity, family, rule_version),
            "source_event_row_ids": _split_semicolon(row.get("source_event_row_ids")),
            "instrument_id": row["instrument_id"],
            "asset": row["asset"],
            "side": row["side"],
            "boundary_side": row["boundary_side"],
            "regime_definition_version": row["regime_definition_version"],
            "source_pipeline_version": row["source_pipeline_version"],
            "historical_cohort_memberships": _split_semicolon(row.get("historical_cohort_memberships")),
            "causal_cohort_label": row["causal_cohort_label"],
            "overlap_cluster_id": row["overlap_cluster_id"],
            "overlap_cluster_size": int(row["overlap_cluster_size"]),
            "overlap_window_start_ts_ms": int(row["overlap_cluster_start_ts_ms"]),
            "overlap_window_end_ts_ms": int(row["overlap_cluster_end_exclusive_ts_ms"]),
            "repeated_signal_group_id": row["repeated_signal_group_id"],
            "snapshot_id": row["snapshot_id"],
            "snapshot_available_at_ts_ms": int(row["snapshot_available_at_ts_ms"]),
            "snapshot_valid_from_ts_ms": int(row["snapshot_valid_from_ts_ms"]),
            "snapshot_valid_until_ts_ms": int(row["snapshot_valid_until_ts_ms"]),
            "frozen_upper_boundary": float(row["frozen_upper_boundary"]),
            "frozen_lower_boundary": float(row["frozen_lower_boundary"]),
            "channel_width_pct": float(row["channel_width_pct"]),
            "threshold_policy_id": row["threshold_policy_id"],
            "threshold_population_id": row["threshold_population_id"],
            "threshold_value": _float_or_none(row.get("threshold_value")),
            "threshold_percentile": _int_or_none(row.get("threshold_percentile")),
            "threshold_calibration_start_ts_ms": _int_or_none(row.get("threshold_calibration_start_ts_ms")),
            "threshold_calibration_end_ts_ms": _int_or_none(row.get("threshold_calibration_end_ts_ms")),
            "threshold_prior_observation_count": _int_or_none(row.get("threshold_prior_observation_count")),
            "efficiency_value": _float_or_none(row.get("efficiency_value")),
            "efficiency_limit": float(row["efficiency_limit"]),
            "overlap_value": _float_or_none(row.get("overlap_value")),
            "overlap_minimum": float(row["overlap_minimum"]),
            "source_file_paths": _split_semicolon(row.get("source_file_paths")),
            "source_git_blob_ids": _split_semicolon(row.get("source_git_blob_ids")),
            "source_sha256_manifest_id": row["source_sha256_manifest_id"],
            "signal_candle_open_ts_ms": _int_or_none(row.get("signal_candle_open_ts_ms")),
            "signal_candle_close_ts_ms": _int_or_none(row.get("signal_candle_close_ts_ms")),
            "signal_available_at_ts_ms": _int_or_none(row.get("signal_available_at_ts_ms")),
            "confirmation_rule_id": row["confirmation_rule_id"],
            "confirmation_bar_interval_ms": int(row["confirmation_bar_interval_ms"]),
            "confirmation_status": row["confirmation_status"],
            "first_eligible_execution_bar_open_ts_ms": _int_or_none(row.get("first_eligible_1m_open_ts_ms")),
            "event_observed_at_ts_ms": int(row["event_observed_at_ts_ms"]),
            "ambiguity_flags": _split_semicolon(row.get("ambiguity_flags")),
            "decluster_policy_id": row["decluster_policy_id"],
            "candidate_status": status,
            "exclusion_reason": reason,
            "censoring_reason": censoring_reason,
            "invalidation_reference_type": row["invalidation_reference_type"],
            "invalidation_reference_value": row["invalidation_reference_value"],
            "invalidation_reference_ts_ms": row["invalidation_reference_ts_ms"],
            "expiry_rule_id": row["expiry_rule_id"],
            "expiry_ts_ms": _int_or_na(row.get("expiry_ts_ms")),
            "source_breakout_candidate_id": source_breakout_candidate,
            "source_reconciliation_status": row["source_reconciliation_status"],
            "source_join_cardinality": row["source_join_cardinality"],
        }
        return record

    canonical = (
        [serialize(row) for row in rejection_rows]
        + [serialize(row) for row in breakout_rows]
        + [serialize(row, failed=True) for row in failed_breakout_rows]
    )
    validate_canonical_candidate_ledger(canonical)
    return canonical


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
    if confirmation_ms >= signal_ms + FAILURE_HORIZON_MS:
        raise ValueError("failure confirmation is outside the half-open 12-hour horizon")
    return "CONFIRMED_WITHIN_12H"
