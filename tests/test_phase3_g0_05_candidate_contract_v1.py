import unittest
import hashlib
import tempfile
from pathlib import Path

from research.phase3_g0_05_candidate_contract_v1 import (
    MINUTE_MS, FIFTEEN_MIN_MS, FAILURE_HORIZON_MS,
    snapshot_is_valid, rejection_confirmation, first_eligible_minute,
    family_side, complete_15m_confirmation, failed_breakout_confirmation,
    candidate_id, classify_disposition, deterministic_json,
    validate_candidate_identity_links, validate_canonical_candidate_record,
    validate_canonical_candidate_ledger, serialize_source_disposition_ledgers,
    causal_regime_eligible, validate_strict_broad_nesting,
    exact_first_minute_disposition, failed_breakout_horizon_disposition,
    rejection_physical_identity, collapse_rejection_cohort_rows, causal_rejection_disposition,
    exact_threshold_for_snapshot, validate_source_key_join, validate_disposition_reason,
    REJECTED_REASON_CODES, EXPIRED_REASON_CODES, CENSORED_REASON_CODES,
)

from research.phase3_g0_05_source_manifest_audit_v1 import (
    first_eligible_minute_or_blank, validate_module_b_horizons,
    validate_disposition_ledger, grouped_disposition_counts, historical_membership_label,
    assign_interval_graph_clusters, observed_window_bars, consistent_physical_cluster,
    make_repeated_signal_group_id, aggregate_completed_15m_bar, file_manifest_entry, git_blob_sha1,
    failed_breakout_confirmation_timing,
    canonical_failed_breakout_confirmation,
    confirmation_ambiguity_flag, canonical_snapshot_provenance,
    resolve_lagged_feature_reference, canonical_cohort_label,
)


class G005ContractTests(unittest.TestCase):
    def test_snapshot_valid_before_endpoint(self):
        self.assertTrue(snapshot_is_valid(100, 1000, 999))

    def test_snapshot_confirmation_at_endpoint_is_expired(self):
        self.assertFalse(snapshot_is_valid(100, 1000, 1000))

    def test_snapshot_confirmation_after_endpoint_is_expired(self):
        self.assertFalse(snapshot_is_valid(100, 1000, 1001))

    def test_snapshot_confirmation_before_availability_is_invalid(self):
        self.assertFalse(snapshot_is_valid(100, 1000, 99))

    def test_invalid_snapshot_interval_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            snapshot_is_valid(100, 100, 100)

    def test_rejection_confirmation_is_completed_15m_close(self):
        self.assertEqual(rejection_confirmation(10_000), 10_000 + FIFTEEN_MIN_MS)

    def test_first_eligible_minute_must_equal_availability(self):
        t = 50_000
        self.assertEqual(first_eligible_minute(t, [t, t + MINUTE_MS]), t)

    def test_no_preconfirmation_minute_is_accepted(self):
        with self.assertRaisesRegex(ValueError, "exactly"):
            first_eligible_minute(50_000, [50_000 - MINUTE_MS, 50_000])

    def test_minute_gap_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "gap"):
            first_eligible_minute(0, [0, 2 * MINUTE_MS])

    def test_support_resistance_direction_mapping(self):
        self.assertEqual(family_side("SUPPORT_REJECTION"), ("LOWER", "LONG"))
        self.assertEqual(family_side("RESISTANCE_REJECTION"), ("UPPER", "SHORT"))

    def test_breakout_direction_mapping(self):
        self.assertEqual(family_side("BREAKOUT_CONTINUATION_UPPER"), ("UPPER", "LONG"))
        self.assertEqual(family_side("BREAKOUT_CONTINUATION_LOWER"), ("LOWER", "SHORT"))

    def test_failed_breakout_direction_mapping(self):
        self.assertEqual(family_side("FAILED_UPPER_BREAKOUT"), ("UPPER", "SHORT"))
        self.assertEqual(family_side("FAILED_LOWER_BREAKOUT"), ("LOWER", "LONG"))

    def test_complete_15m_bar_accepted(self):
        opens = [i * MINUTE_MS for i in range(15)]
        self.assertEqual(complete_15m_confirmation(opens, 0), FIFTEEN_MIN_MS)

    def test_incomplete_15m_bar_rejected(self):
        opens = [i * MINUTE_MS for i in range(14)]
        with self.assertRaisesRegex(ValueError, "15 consecutive"):
            complete_15m_confirmation(opens, 0)

    def test_nonconsecutive_15m_components_rejected(self):
        opens = [i * MINUTE_MS for i in range(15)]
        opens[7] += 1
        with self.assertRaisesRegex(ValueError, "15 consecutive"):
            complete_15m_confirmation(opens, 0)

    def test_failed_upper_breakout_confirms_short_on_close_inside(self):
        result = failed_breakout_confirmation("UPPER", 99.0, 100.0, 900_000, 0, True)
        self.assertEqual(result["side"], "SHORT")

    def test_failed_lower_breakout_confirms_long_on_close_inside(self):
        result = failed_breakout_confirmation("LOWER", 101.0, 100.0, 900_000, 0, True)
        self.assertEqual(result["side"], "LONG")

    def test_failed_breakout_without_source_link_rejected(self):
        with self.assertRaisesRegex(ValueError, "linked source breakout"):
            failed_breakout_confirmation("UPPER", 99.0, 100.0, 900_000, 0, False)

    def test_failed_breakout_close_not_inside_rejected(self):
        with self.assertRaisesRegex(ValueError, "not returned inside"):
            failed_breakout_confirmation("UPPER", 101.0, 100.0, 900_000, 0, True)

    def test_failed_breakout_just_before_12h_endpoint_is_accepted(self):
        result = failed_breakout_confirmation("UPPER", 99.0, 100.0,
                                               FAILURE_HORIZON_MS - 1, 0, True)
        self.assertEqual(result["side"], "SHORT")

    def test_failed_breakout_exact_12h_endpoint_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "half-open 12-hour"):
            failed_breakout_confirmation("UPPER", 99.0, 100.0,
                                          FAILURE_HORIZON_MS, 0, True)

    def test_failed_breakout_after_12h_rejected(self):
        with self.assertRaisesRegex(ValueError, "12-hour"):
            failed_breakout_confirmation("UPPER", 99.0, 100.0,
                                          FAILURE_HORIZON_MS + 1, 0, True)

    def _source_only_fixture_from_canonical(self, record, provisional_source_event_id=None,
                                             source_breakout_source_event_id=None):
        return {
            "source_event_id": provisional_source_event_id or record["source_event_id"],
            "source_breakout_source_event_id": source_breakout_source_event_id or "",
            "family": record["family"],
            "instrument_id": record["instrument_id"],
            "asset": record["asset"],
            "side": record["side"],
            "boundary_side": record["boundary_side"],
            "regime_definition_version": record["regime_definition_version"],
            "source_pipeline_version": record["source_pipeline_version"],
            "source_event_row_ids": ";".join(record["source_event_row_ids"]),
            "historical_cohort_memberships": ";".join(record["historical_cohort_memberships"]),
            "causal_cohort_label": record["causal_cohort_label"],
            "overlap_cluster_id": record["overlap_cluster_id"],
            "overlap_cluster_size": str(record["overlap_cluster_size"]),
            "overlap_cluster_start_ts_ms": str(record["overlap_window_start_ts_ms"]),
            "overlap_cluster_end_exclusive_ts_ms": str(record["overlap_window_end_ts_ms"]),
            "repeated_signal_group_id": record["repeated_signal_group_id"],
            "snapshot_id": record["snapshot_id"],
            "snapshot_available_at_ts_ms": str(record["snapshot_available_at_ts_ms"]),
            "snapshot_valid_from_ts_ms": str(record["snapshot_valid_from_ts_ms"]),
            "snapshot_valid_until_ts_ms": str(record["snapshot_valid_until_ts_ms"]),
            "frozen_upper_boundary": str(record["frozen_upper_boundary"]),
            "frozen_lower_boundary": str(record["frozen_lower_boundary"]),
            "channel_width_pct": str(record["channel_width_pct"]),
            "threshold_policy_id": record["threshold_policy_id"],
            "threshold_population_id": record["threshold_population_id"],
            "threshold_value": "" if record["threshold_value"] is None else str(record["threshold_value"]),
            "threshold_percentile": "" if record["threshold_percentile"] is None else str(record["threshold_percentile"]),
            "threshold_calibration_start_ts_ms": "" if record["threshold_calibration_start_ts_ms"] is None else str(record["threshold_calibration_start_ts_ms"]),
            "threshold_calibration_end_ts_ms": "" if record["threshold_calibration_end_ts_ms"] is None else str(record["threshold_calibration_end_ts_ms"]),
            "threshold_prior_observation_count": "" if record["threshold_prior_observation_count"] is None else str(record["threshold_prior_observation_count"]),
            "efficiency_value": "" if record["efficiency_value"] is None else str(record["efficiency_value"]),
            "efficiency_limit": str(record["efficiency_limit"]),
            "overlap_value": "" if record["overlap_value"] is None else str(record["overlap_value"]),
            "overlap_minimum": str(record["overlap_minimum"]),
            "source_file_paths": ";".join(record["source_file_paths"]),
            "source_git_blob_ids": ";".join(record["source_git_blob_ids"]),
            "source_sha256_manifest_id": record["source_sha256_manifest_id"],
            "signal_candle_open_ts_ms": "" if record["signal_candle_open_ts_ms"] is None else str(record["signal_candle_open_ts_ms"]),
            "signal_candle_close_ts_ms": "" if record["signal_candle_close_ts_ms"] is None else str(record["signal_candle_close_ts_ms"]),
            "signal_available_at_ts_ms": "" if record["signal_available_at_ts_ms"] is None else str(record["signal_available_at_ts_ms"]),
            "confirmation_rule_id": record["confirmation_rule_id"],
            "confirmation_bar_interval_ms": str(record["confirmation_bar_interval_ms"]),
            "confirmation_status": record["confirmation_status"],
            "first_eligible_1m_open_ts_ms": "" if record["first_eligible_execution_bar_open_ts_ms"] is None else str(record["first_eligible_execution_bar_open_ts_ms"]),
            "event_observed_at_ts_ms": str(record["event_observed_at_ts_ms"]),
            "ambiguity_flags": ";".join(record["ambiguity_flags"]),
            "decluster_policy_id": record["decluster_policy_id"],
            "disposition": record["candidate_status"],
            "reason_code": record["exclusion_reason"],
            "censoring_reason": record["censoring_reason"] or "",
            "invalidation_reference_type": record["invalidation_reference_type"],
            "invalidation_reference_value": record["invalidation_reference_value"],
            "invalidation_reference_ts_ms": record["invalidation_reference_ts_ms"],
            "expiry_rule_id": record["expiry_rule_id"],
            "expiry_ts_ms": str(record["expiry_ts_ms"]),
            "source_reconciliation_status": record["source_reconciliation_status"],
            "source_join_cardinality": record["source_join_cardinality"],
        }

    def test_source_disposition_serializer_builds_valid_canonical_ledger(self):
        rejection_identity = "BTC|LOWER|rejection|1761287400000"
        rejection = self._canonical_candidate_fixture(
            "SUPPORT_REJECTION", rejection_identity, 1761287400000, "LOWER", "LONG")
        rejection["source_reconciliation_status"] = "EXACT_PHYSICAL_EVENT_COLLAPSE"
        rejection["source_join_cardinality"] = "ONE_PHYSICAL_EVENT_TO_ONE_OR_TWO_COHORT_ROWS"
        rejection_source = self._source_only_fixture_from_canonical(rejection)

        breakout_identity = "BTC|UPPER|1761287400000|1761278400000"
        breakout = self._canonical_candidate_fixture(
            "BREAKOUT_CONTINUATION", breakout_identity, 1761287400000, "UPPER", "LONG")
        breakout_source = self._source_only_fixture_from_canonical(breakout)

        confirmation = 1761291000000
        source_breakout_id = breakout["candidate_id"]
        failed_identity = f"{source_breakout_id}|{confirmation}|G0_05_CANDIDATE_RULE_V1"
        failed = self._canonical_candidate_fixture(
            "FAILED_BREAKOUT_REVERSAL", failed_identity, confirmation, "UPPER", "SHORT",
            source_breakout_candidate_id=source_breakout_id,
            source_breakout_signal_available=breakout["signal_available_at_ts_ms"])
        failed["source_reconciliation_status"] = "EXACT_LINKED_SOURCE_BREAKOUT"
        failed["source_join_cardinality"] = "ONE_FAILED_BREAKOUT_TO_ONE_SOURCE_BREAKOUT"
        failed_source = self._source_only_fixture_from_canonical(
            failed, provisional_source_event_id="PROVISIONAL|FAILED",
            source_breakout_source_event_id=breakout_identity)

        records = serialize_source_disposition_ledgers(
            [rejection_source], [breakout_source], [failed_source])
        self.assertEqual(len(records), 3)
        failed_record = next(x for x in records if x["family"] == "FAILED_BREAKOUT_REVERSAL")
        self.assertEqual(failed_record["source_breakout_candidate_id"], source_breakout_id)
        self.assertEqual(failed_record["source_event_id"], failed_identity)

    def _canonical_candidate_fixture(self, family, source_event_id, signal_available,
                                      boundary_side, side, source_breakout_candidate_id="NOT_APPLICABLE",
                                      source_breakout_signal_available=None):
        snapshot = 1761278400000
        rule_version = "G0_05_CANDIDATE_RULE_V1"
        regime = ("SIDEWAYS_DETECTOR_ORIGINAL_V1"
                  if family in {"SUPPORT_REJECTION", "RESISTANCE_REJECTION"}
                  else "HISTORICAL_BREAKOUT_CONTEXT_V1")
        confirmation_rule = {
            "SUPPORT_REJECTION": "STRONG_REJECTION_15M_CLOSE_V1",
            "RESISTANCE_REJECTION": "STRONG_REJECTION_15M_CLOSE_V1",
            "BREAKOUT_CONTINUATION": "BOUNDARY_CROSSING_15M_CLOSE_V1",
            "FAILED_BREAKOUT_REVERSAL": "RETURN_INSIDE_15M_CLOSE_V1",
        }[family]
        failed = family == "FAILED_BREAKOUT_REVERSAL"
        source_signal = source_breakout_signal_available or signal_available
        record = {
            "source_event_id": source_event_id,
            "family": family,
            "candidate_rule_version": rule_version,
            "instrument_id": "BTC-USDT-SWAP",
            "asset": "BTC",
            "side": side,
            "boundary_side": boundary_side,
            "regime_definition_version": regime,
            "source_pipeline_version": "G0_04_CAUSAL_RECONSTRUCTION_V1+MODULE_A_V1_1+MODULE_B_V1_1",
            "source_event_row_ids": ["source-row-1"],
            "historical_cohort_memberships": ["BROAD_P40"],
            "causal_cohort_label": "STRICT_P25",
            "overlap_cluster_id": "cluster-btc-1",
            "overlap_cluster_size": 1,
            "overlap_window_start_ts_ms": snapshot,
            "overlap_window_end_ts_ms": snapshot + 43200000,
            "repeated_signal_group_id": "group-btc-1",
            "snapshot_id": f"BTC|{snapshot}",
            "snapshot_available_at_ts_ms": snapshot,
            "snapshot_valid_from_ts_ms": snapshot,
            "snapshot_valid_until_ts_ms": snapshot + 14400000,
            "frozen_upper_boundary": 110.0,
            "frozen_lower_boundary": 90.0,
            "channel_width_pct": 9.0,
            "threshold_policy_id": "EXPANDING_PRIOR",
            "threshold_population_id": "UNIQUE_4H_FEATURE_ROWS",
            "threshold_value": 9.5,
            "threshold_percentile": 25,
            "threshold_calibration_start_ts_ms": 1760000000000,
            "threshold_calibration_end_ts_ms": 1761000000000,
            "threshold_prior_observation_count": 200,
            "efficiency_value": 0.2,
            "efficiency_limit": 0.30,
            "overlap_value": 0.8,
            "overlap_minimum": 0.70,
            "source_file_paths": ["data/market_1m/BTC_USDT_USDT_1m.csv",
                                  "G0-04-artifact/unique_raw_crossing_events_with_six_variants.csv"],
            "source_git_blob_ids": ["a" * 40],
            "source_sha256_manifest_id": "b" * 64,
            "signal_candle_open_ts_ms": signal_available - FIFTEEN_MIN_MS,
            "signal_candle_close_ts_ms": signal_available,
            "signal_available_at_ts_ms": signal_available,
            "confirmation_rule_id": confirmation_rule,
            "confirmation_bar_interval_ms": FIFTEEN_MIN_MS,
            "confirmation_status": "CONFIRMED",
            "first_eligible_execution_bar_open_ts_ms": signal_available,
            "event_observed_at_ts_ms": signal_available,
            "ambiguity_flags": ["NONE"],
            "decluster_policy_id": "G0_05_INTERVAL_GRAPH_METADATA_V1",
            "candidate_status": "ELIGIBLE_FOR_FURTHER_VALIDATION",
            "exclusion_reason": "NONE",
            "censoring_reason": None,
            "invalidation_reference_type": "NOT_APPLICABLE",
            "invalidation_reference_value": "NOT_APPLICABLE",
            "invalidation_reference_ts_ms": "NOT_APPLICABLE",
            "expiry_rule_id": "SOURCE_BREAKOUT_12H_RETURN_INSIDE_V1" if failed else "NOT_APPLICABLE",
            "expiry_ts_ms": source_signal + FAILURE_HORIZON_MS if failed else "NOT_APPLICABLE",
            "source_breakout_candidate_id": source_breakout_candidate_id,
            "source_reconciliation_status": "EXACT_LINKED_SOURCE_BREAKOUT" if failed else "EXACT_SOURCE_MATCH",
            "source_join_cardinality": "ONE_FAILED_BREAKOUT_TO_ONE_SOURCE_BREAKOUT" if failed else "ONE_RAW_CROSSING_TO_ONE_DISPOSITION",
        }
        record["candidate_id"] = candidate_id(source_event_id, family, rule_version)
        return record

    def test_full_canonical_candidate_ledger_accepts_exact_breakout_link(self):
        breakout_identity = "BTC|UPPER|1761287400000|1761278400000"
        breakout = self._canonical_candidate_fixture(
            "BREAKOUT_CONTINUATION", breakout_identity, 1761287400000, "UPPER", "LONG")
        confirmation = 1761291000000
        failed_identity = (
            f"{breakout['candidate_id']}|{confirmation}|G0_05_CANDIDATE_RULE_V1")
        failed = self._canonical_candidate_fixture(
            "FAILED_BREAKOUT_REVERSAL", failed_identity, confirmation, "UPPER", "SHORT",
            source_breakout_candidate_id=breakout["candidate_id"],
            source_breakout_signal_available=breakout["signal_available_at_ts_ms"])
        result = validate_canonical_candidate_ledger([breakout, failed])
        self.assertEqual(result["candidate_rows"], 2)
        self.assertEqual(result["failed_breakout_source_links_validated"], 1)

    def test_canonical_record_rejects_wrong_family_side(self):
        record = self._canonical_candidate_fixture(
            "BREAKOUT_CONTINUATION", "BTC|UPPER|1|2", 1761287400000, "UPPER", "LONG")
        record["side"] = "SHORT"
        with self.assertRaisesRegex(ValueError, "family, boundary_side and side"):
            validate_canonical_candidate_record(record)

    def test_canonical_record_rejects_future_threshold_calibration(self):
        record = self._canonical_candidate_fixture(
            "BREAKOUT_CONTINUATION", "BTC|UPPER|1|2", 1761287400000, "UPPER", "LONG")
        record["threshold_calibration_end_ts_ms"] = record["snapshot_available_at_ts_ms"]
        with self.assertRaisesRegex(ValueError, "must end before snapshot"):
            validate_canonical_candidate_record(record)

    def test_canonical_record_rejects_missing_required_lineage(self):
        record = self._canonical_candidate_fixture(
            "BREAKOUT_CONTINUATION", "BTC|UPPER|1|2", 1761287400000, "UPPER", "LONG")
        del record["source_file_paths"]
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            validate_canonical_candidate_record(record)

    def test_canonical_ledger_rejects_failed_breakout_expiry_mismatch(self):
        breakout_identity = "BTC|UPPER|1761287400000|1761278400000"
        breakout = self._canonical_candidate_fixture(
            "BREAKOUT_CONTINUATION", breakout_identity, 1761287400000, "UPPER", "LONG")
        confirmation = 1761291000000
        failed_identity = (
            f"{breakout['candidate_id']}|{confirmation}|G0_05_CANDIDATE_RULE_V1")
        failed = self._canonical_candidate_fixture(
            "FAILED_BREAKOUT_REVERSAL", failed_identity, confirmation, "UPPER", "SHORT",
            source_breakout_candidate_id=breakout["candidate_id"],
            source_breakout_signal_available=breakout["signal_available_at_ts_ms"])
        failed["expiry_ts_ms"] += 1
        with self.assertRaisesRegex(ValueError, "expiry does not match"):
            validate_canonical_candidate_ledger([breakout, failed])

    def _synthetic_candidate_identity_rows(self):
        version = "G0_05_CANDIDATE_RULE_V1"
        source_breakout_id = "BTC|UPPER|1761287400000|1761278400000"
        breakout_id = candidate_id(source_breakout_id, "BREAKOUT_CONTINUATION", version)
        confirmation_ts = "1761300000000"
        failed_source_id = f"{breakout_id}|{confirmation_ts}|{version}"
        failed_id = candidate_id(failed_source_id, "FAILED_BREAKOUT_REVERSAL", version)
        return [
            {
                "candidate_id": breakout_id,
                "source_event_id": source_breakout_id,
                "family": "BREAKOUT_CONTINUATION",
                "candidate_rule_version": version,
                "signal_available_at_ts_ms": 1761287400000,
                "source_breakout_candidate_id": "NOT_APPLICABLE",
            },
            {
                "candidate_id": failed_id,
                "source_event_id": failed_source_id,
                "family": "FAILED_BREAKOUT_REVERSAL",
                "candidate_rule_version": version,
                "source_breakout_source_event_id": source_breakout_id,
                "source_breakout_candidate_id": breakout_id,
                "signal_available_at_ts_ms": confirmation_ts,
                "expiry_ts_ms": 1761287400000 + FAILURE_HORIZON_MS,
            },
        ]

    def test_candidate_identity_validator_accepts_exact_failed_breakout_link(self):
        result = validate_candidate_identity_links(self._synthetic_candidate_identity_rows())
        self.assertEqual(result["candidate_rows"], 2)
        self.assertEqual(result["failed_breakout_source_links_validated"], 1)
        self.assertTrue(result["candidate_ids_unique"])

    def test_candidate_identity_validator_rejects_wrong_candidate_hash(self):
        rows = self._synthetic_candidate_identity_rows()
        rows[0]["candidate_id"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate_candidate_identity_links(rows)

    def test_candidate_identity_validator_rejects_duplicate_candidate_ids(self):
        rows = self._synthetic_candidate_identity_rows()
        rows[1]["candidate_id"] = rows[0]["candidate_id"]
        with self.assertRaisesRegex(ValueError, "duplicate candidate_id"):
            validate_candidate_identity_links(rows)

    def test_candidate_identity_validator_rejects_failed_source_identity_mismatch(self):
        rows = self._synthetic_candidate_identity_rows()
        rows[1]["source_event_id"] += "|wrong"
        rows[1]["candidate_id"] = candidate_id(
            rows[1]["source_event_id"], rows[1]["family"], rows[1]["candidate_rule_version"])
        with self.assertRaisesRegex(ValueError, "failed-breakout source_event_id"):
            validate_candidate_identity_links(rows)

    def test_candidate_identity_validator_supports_no_confirmation_sentinel(self):
        rows = self._synthetic_candidate_identity_rows()
        version = rows[0]["candidate_rule_version"]
        linked = rows[0]["candidate_id"]
        rows[1]["signal_available_at_ts_ms"] = ""
        rows[1]["source_event_id"] = f"{linked}|NO_CONFIRMATION|{version}"
        rows[1]["candidate_id"] = candidate_id(
            rows[1]["source_event_id"], rows[1]["family"], version)
        result = validate_candidate_identity_links(rows)
        self.assertEqual(result["failed_breakout_source_links_validated"], 1)

    def test_candidate_identity_validator_rejects_broken_source_breakout_link(self):
        rows = self._synthetic_candidate_identity_rows()
        rows[1]["source_breakout_candidate_id"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "does not resolve"):
            validate_candidate_identity_links(rows)

    def test_candidate_identity_validator_requires_source_breakout_row(self):
        rows = self._synthetic_candidate_identity_rows()[1:]
        with self.assertRaisesRegex(ValueError, "does not resolve"):
            validate_candidate_identity_links(rows)

    def test_candidate_identity_validator_rejects_source_link_on_other_families(self):
        rows = self._synthetic_candidate_identity_rows()
        rows[0]["source_breakout_candidate_id"] = rows[1]["source_breakout_candidate_id"]
        with self.assertRaisesRegex(ValueError, "non-failed-breakout"):
            validate_candidate_identity_links(rows)

    def test_candidate_id_is_deterministic_and_rule_versioned(self):
        a = candidate_id("BTC|UPPER|1000", "BREAKOUT_CONTINUATION", "v1")
        self.assertEqual(a, candidate_id("BTC|UPPER|1000", "BREAKOUT_CONTINUATION", "v1"))
        self.assertNotEqual(a, candidate_id("BTC|UPPER|1000", "BREAKOUT_CONTINUATION", "v2"))

    def test_disposition_is_explicit(self):
        self.assertEqual(classify_disposition(0, 100, 99), "ELIGIBLE_FOR_FURTHER_VALIDATION")
        self.assertEqual(classify_disposition(0, 100, 100), "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION")

    def test_causal_regime_conditions_accept_boundary_values(self):
        self.assertTrue(causal_regime_eligible(2.0, 2.0, 0.30, 0.70))

    def test_causal_regime_rejects_width_above_threshold(self):
        self.assertFalse(causal_regime_eligible(2.0001, 2.0, 0.20, 0.80))

    def test_causal_regime_rejects_efficiency_above_limit(self):
        self.assertFalse(causal_regime_eligible(1.0, 2.0, 0.3001, 0.80))

    def test_causal_regime_rejects_overlap_below_limit(self):
        self.assertFalse(causal_regime_eligible(1.0, 2.0, 0.20, 0.6999))

    def test_causal_regime_rejects_nonfinite_inputs(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            causal_regime_eligible(float("nan"), 2.0, 0.20, 0.80)

    def test_strict_cohort_must_be_nested_in_broad(self):
        validate_strict_broad_nesting([True, False], [True, True])
        with self.assertRaisesRegex(ValueError, "not nested"):
            validate_strict_broad_nesting([True, True], [True, False])

    def test_strict_broad_cohort_length_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, "equal lengths"):
            validate_strict_broad_nesting([True], [True, False])

    def test_rejection_physical_identity_ignores_historical_definition(self):
        broad = {"asset": "BTC", "direction": "upper", "snapshot_index": 7,
                 "segment_id": 3, "test_rank": 2, "test_start_ts_ms": 9000,
                 "definition": "BROAD_P40"}
        strict = dict(broad, definition="STRICT_P25")
        self.assertEqual(rejection_physical_identity(broad), rejection_physical_identity(strict))

    def test_collapse_preserves_both_historical_cohort_source_ids(self):
        base = {"asset": "BTC", "direction": "upper", "snapshot_index": 7,
                "segment_id": 3, "test_rank": 2, "test_start_ts_ms": 9000}
        rows = [dict(base, definition="BROAD_P40", event_id="broad-row"),
                dict(base, definition="STRICT_P25", event_id="strict-row")]
        result = collapse_rejection_cohort_rows(rows)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["source_event_row_ids"], ["broad-row", "strict-row"])
        self.assertEqual(result[0]["historical_cohort_memberships"], ["BROAD_P40", "STRICT_P25"])

    def test_broad_only_rejection_remains_one_physical_event(self):
        row = {"asset": "ETH", "direction": "lower", "snapshot_index": 8,
               "segment_id": 1, "test_rank": 1, "test_start_ts_ms": 10000,
               "definition": "BROAD_P40", "event_id": "broad-only"}
        result = collapse_rejection_cohort_rows([row])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["historical_cohort_memberships"], ["BROAD_P40"])

    def test_strict_without_broad_membership_fails_closed(self):
        row = {"asset": "ETH", "direction": "lower", "snapshot_index": 8,
               "segment_id": 1, "test_rank": 1, "test_start_ts_ms": 10000,
               "definition": "STRICT_P25", "event_id": "strict-only"}
        with self.assertRaisesRegex(ValueError, "not nested"):
            collapse_rejection_cohort_rows([row])

    def test_duplicate_definition_membership_fails_closed(self):
        row = {"asset": "BTC", "direction": "upper", "snapshot_index": 7,
               "segment_id": 3, "test_rank": 2, "test_start_ts_ms": 9000,
               "definition": "BROAD_P40", "event_id": "broad-row"}
        with self.assertRaisesRegex(ValueError, "duplicate physical"):
            collapse_rejection_cohort_rows([row, dict(row, event_id="duplicate")])

    def test_causal_rejection_disposition_strict(self):
        result = causal_rejection_disposition(0, 2_000_000, 100_000, 1_000_000,
                                              2.0, 3.0, 2.0, 0.30, 0.70)
        self.assertEqual(result, "CAUSAL_STRICT_ELIGIBLE")

    def test_causal_rejection_disposition_broad_only(self):
        result = causal_rejection_disposition(0, 2_000_000, 100_000, 1_000_000,
                                              2.0, 3.0, 2.5, 0.20, 0.80)
        self.assertEqual(result, "CAUSAL_BROAD_ONLY_ELIGIBLE")

    def test_causal_rejection_disposition_not_regime_eligible(self):
        result = causal_rejection_disposition(0, 2_000_000, 100_000, 1_000_000,
                                              2.0, 3.0, 2.5, 0.31, 0.80)
        self.assertEqual(result, "CAUSAL_REGIME_NOT_ELIGIBLE")

    def test_causal_rejection_disposition_warmup(self):
        result = causal_rejection_disposition(0, 2_000_000, 100_000, 1_000_000,
                                              None, None, 2.5, 0.20, 0.80)
        self.assertEqual(result, "CAUSAL_THRESHOLD_WARMUP")

    def test_causal_rejection_snapshot_endpoint_expires(self):
        result = causal_rejection_disposition(0, 1_000_000, 100_000, 1_000_000,
                                              2.0, 3.0, 2.0, 0.20, 0.80)
        self.assertEqual(result, "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION")

    def test_causal_rejection_requires_confirmation_at_15m_close(self):
        with self.assertRaisesRegex(ValueError, "completed 15-minute"):
            causal_rejection_disposition(0, 2_000_000, 100_000, 999_999,
                                         2.0, 3.0, 2.0, 0.20, 0.80)

    def test_causal_rejection_requires_snapshot_available_at_bar_open(self):
        with self.assertRaisesRegex(ValueError, "not available"):
            causal_rejection_disposition(200_000, 2_000_000, 100_000, 1_000_000,
                                         2.0, 3.0, 2.0, 0.20, 0.80)


    def test_exact_first_minute_requires_timestamp_match(self):
        t = 60_000
        self.assertEqual(exact_first_minute_disposition(t, {t, t + MINUTE_MS}),
                         "EXACT_FIRST_MINUTE_AVAILABLE")
        self.assertEqual(exact_first_minute_disposition(t, {t + MINUTE_MS}),
                         "MISSING_OR_GAPPED_MINUTES")

    def test_exact_first_minute_rejects_nonminute_availability(self):
        with self.assertRaisesRegex(ValueError, "minute boundary"):
            exact_first_minute_disposition(60_001, {60_001})

    def test_failed_breakout_complete_horizon_without_confirmation_expires(self):
        self.assertEqual(failed_breakout_horizon_disposition(0, None, True),
                         "EXPIRED_NO_RETURN_INSIDE_WITHIN_12H")

    def test_failed_breakout_incomplete_horizon_without_confirmation_is_censored(self):
        self.assertEqual(failed_breakout_horizon_disposition(0, None, False),
                         "CENSORED_SOURCE_END_BEFORE_RESOLUTION")

    def test_failed_breakout_confirmation_at_12h_boundary_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "half-open 12-hour"):
            failed_breakout_horizon_disposition(0, FAILURE_HORIZON_MS, True)

    def test_failed_breakout_confirmation_after_12h_fails(self):
        with self.assertRaisesRegex(ValueError, "12-hour"):
            failed_breakout_horizon_disposition(0, FAILURE_HORIZON_MS + 1, True)

    def test_deterministic_serialization(self):
        rows = [{"b": 2, "a": 1}]
        self.assertEqual(deterministic_json(rows), deterministic_json([{"a": 1, "b": 2}]))



class G005ExpandedGateTests(unittest.TestCase):
    def test_exact_threshold_lookup_uses_exact_snapshot_only(self):
        row = {"last_prior_context_ms": 900, "prior_context_count": 180}
        index = {("BTC", 1000, "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS"): row}
        self.assertIs(exact_threshold_for_snapshot(
            index, "BTC", 1000, "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS"), row)
        self.assertIsNone(exact_threshold_for_snapshot(
            index, "BTC", 1001, "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS"))

    def test_exact_threshold_lookup_rejects_current_or_future_calibration(self):
        index = {("BTC", 1000, "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS"):
                 {"last_prior_context_ms": 1000, "prior_context_count": 180}}
        with self.assertRaisesRegex(ValueError, "strictly before"):
            exact_threshold_for_snapshot(
                index, "BTC", 1000, "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS")

    def test_exact_threshold_lookup_requires_180_prior_contexts(self):
        index = {("BTC", 1000, "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS"):
                 {"last_prior_context_ms": 900, "prior_context_count": 179}}
        with self.assertRaisesRegex(ValueError, "180 prior"):
            exact_threshold_for_snapshot(
                index, "BTC", 1000, "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS")

    def test_exact_source_key_join_accepts_exact_match(self):
        self.assertTrue(validate_source_key_join(["a", "b"], ["b", "a"], exact=True))

    def test_exact_source_key_join_rejects_missing_key(self):
        with self.assertRaisesRegex(ValueError, "missing=1"):
            validate_source_key_join(["a", "b"], ["a"], exact=True)

    def test_exact_source_key_join_rejects_extra_key(self):
        with self.assertRaisesRegex(ValueError, "extra=1"):
            validate_source_key_join(["a"], ["a", "b"], exact=True)

    def test_source_key_subset_join_allows_unrelated_raw_events(self):
        self.assertTrue(validate_source_key_join(["selected"], ["selected", "other"], exact=False))

    def test_source_key_subset_join_rejects_unmatched_source(self):
        with self.assertRaisesRegex(ValueError, "missing=1"):
            validate_source_key_join(["selected", "missing"], ["selected", "other"], exact=False)

    def test_source_key_join_rejects_duplicate_expected_or_observed_keys(self):
        with self.assertRaisesRegex(ValueError, "duplicate expected"):
            validate_source_key_join(["a", "a"], ["a"], exact=True)
        with self.assertRaisesRegex(ValueError, "duplicate observed"):
            validate_source_key_join(["a"], ["a", "a"], exact=True)

    def test_all_frozen_disposition_reason_codes_are_classified(self):
        self.assertEqual(REJECTED_REASON_CODES, frozenset({
            "CAUSAL_THRESHOLD_WARMUP", "CAUSAL_REGIME_NOT_ELIGIBLE",
            "SNAPSHOT_NOT_AVAILABLE_AT_SIGNAL", "SOURCE_HASH_MISMATCH",
            "MISSING_SOURCE_IDENTITY", "SOURCE_JOIN_UNMATCHED",
            "DUPLICATE_SOURCE_IDENTITY", "DUPLICATE_CANDIDATE_ID",
            "INVALID_SOURCE_SCHEMA", "INVALID_FEATURE_VALUES",
            "FUTURE_CONTEXT_ASSIGNED", "DIRECTION_MAPPING_MISMATCH",
            "NO_VALID_SOURCE_BREAKOUT", "INCOMPLETE_CONFIRMATION_BAR",
        }))
        self.assertEqual(EXPIRED_REASON_CODES, frozenset({
            "EXPIRED_NO_RETURN_INSIDE_WITHIN_12H", "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION",
        }))
        self.assertEqual(CENSORED_REASON_CODES, frozenset({
            "MISSING_OR_GAPPED_MINUTES", "INCOMPLETE_15M_CONFIRMATION",
            "SOURCE_END_BEFORE_RESOLUTION", "AMBIGUOUS_CONFIRMATION_UNRESOLVED",
        }))
        for reason in REJECTED_REASON_CODES:
            self.assertTrue(validate_disposition_reason("REJECTED", reason))
        for reason in EXPIRED_REASON_CODES:
            self.assertTrue(validate_disposition_reason("EXPIRED", reason))
        for reason in CENSORED_REASON_CODES:
            self.assertTrue(validate_disposition_reason("CENSORED", reason, reason))

    def test_snapshot_expiry_reason_is_expired_not_rejected(self):
        self.assertTrue(validate_disposition_reason(
            "EXPIRED", "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION"))
        with self.assertRaisesRegex(ValueError, "rejected row"):
            validate_disposition_reason("REJECTED", "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION")

    def test_eligible_disposition_requires_none_reason(self):
        self.assertTrue(validate_disposition_reason(
            "ELIGIBLE_FOR_FURTHER_VALIDATION", "NONE"))
        with self.assertRaisesRegex(ValueError, "exclusion_reason=NONE"):
            validate_disposition_reason("ELIGIBLE_FOR_FURTHER_VALIDATION", "")

    def test_censored_disposition_requires_matching_censoring_reason(self):
        with self.assertRaisesRegex(ValueError, "matching"):
            validate_disposition_reason("CENSORED", "SOURCE_END_BEFORE_RESOLUTION", "")

    def test_disposition_ledger_requires_exact_population_and_unique_ids(self):
        rows = [
            {"source_event_key": "a", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION",
             "reason_code": "NONE", "censoring_reason": ""},
            {"source_event_key": "b", "disposition": "REJECTED",
             "reason_code": "CAUSAL_THRESHOLD_WARMUP", "censoring_reason": ""},
        ]
        result = validate_disposition_ledger(rows, "source_event_key", 2)
        self.assertEqual(result["rows"], 2)
        self.assertEqual(sum(result["dispositions"].values()), 2)

    def test_disposition_ledger_rejects_missing_source_rows(self):
        rows = [{"source_event_key": "a", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION"}]
        with self.assertRaisesRegex(RuntimeError, "row count"):
            validate_disposition_ledger(rows, "source_event_key", 2)

    def test_disposition_ledger_rejects_duplicate_source_identity(self):
        rows = [
            {"source_event_key": "a", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION"},
            {"source_event_key": "a", "disposition": "REJECTED"},
        ]
        with self.assertRaisesRegex(RuntimeError, "duplicate"):
            validate_disposition_ledger(rows, "source_event_key", 2)

    def test_disposition_ledger_rejects_unknown_status(self):
        rows = [{"source_event_key": "a", "disposition": "MAYBE"}]
        with self.assertRaisesRegex(RuntimeError, "invalid status"):
            validate_disposition_ledger(rows, "source_event_key", 1)


class G005SourceAuditTests(unittest.TestCase):
    def sample_horizons(self):
        events = [{
            "event_id": "BTC|broad_p40|upper|1000|zone10",
            "signal_time_ms": "1000",
            "complete_12h": "True",
            "first_15m_return_inside_close_ts_ms": "901000",
        }]
        horizons = []
        for label in ("15M", "1H", "4H", "12H"):
            horizons.append({
                "event_id": events[0]["event_id"],
                "horizon": label,
                "complete": "True",
                "first_15m_return_inside_close_ts_ms": "901000" if label == "12H" else "",
            })
        return events, horizons

    def test_module_b_horizons_reconcile_four_rows_per_event(self):
        events, horizons = self.sample_horizons()
        result = validate_module_b_horizons(events, horizons)
        self.assertEqual(result["events_reconciled"], 1)
        self.assertEqual(result["horizon_rows_reconciled"], 4)
        self.assertEqual(result["twelve_hour_confirmations"], 1)

    def test_module_b_horizons_reject_missing_horizon(self):
        events, horizons = self.sample_horizons()
        with self.assertRaisesRegex(RuntimeError, "exactly 15M/1H/4H/12H"):
            validate_module_b_horizons(events, horizons[:-1])

    def test_module_b_horizons_reject_duplicate_horizon(self):
        events, horizons = self.sample_horizons()
        horizons[-1] = dict(horizons[-2])
        with self.assertRaisesRegex(RuntimeError, "duplicate Module B horizon"):
            validate_module_b_horizons(events, horizons)

    def test_module_b_horizons_reject_unknown_event_id(self):
        events, horizons = self.sample_horizons()
        horizons[-1]["event_id"] = "unexpected-event"
        with self.assertRaisesRegex(RuntimeError, "unknown event_id"):
            validate_module_b_horizons(events, horizons)

    def test_module_b_horizons_reject_completion_mismatch(self):
        events, horizons = self.sample_horizons()
        horizons[-1]["complete"] = "False"
        with self.assertRaisesRegex(RuntimeError, "completion flag mismatch"):
            validate_module_b_horizons(events, horizons)

    def test_module_b_horizons_reject_confirmation_mismatch(self):
        events, horizons = self.sample_horizons()
        horizons[-1]["first_15m_return_inside_close_ts_ms"] = "900000"
        with self.assertRaisesRegex(RuntimeError, "confirmation timestamp mismatch"):
            validate_module_b_horizons(events, horizons)

    def test_module_b_horizons_accept_confirmation_just_before_12h_endpoint(self):
        events, horizons = self.sample_horizons()
        events[0]["first_15m_return_inside_close_ts_ms"] = "43200999"
        horizons[-1]["first_15m_return_inside_close_ts_ms"] = "43200999"
        result = validate_module_b_horizons(events, horizons)
        self.assertEqual(result["twelve_hour_confirmations"], 1)

    def test_module_b_horizons_retain_exact_endpoint_as_descriptive_only(self):
        events, horizons = self.sample_horizons()
        events[0]["first_15m_return_inside_close_ts_ms"] = "43201000"
        horizons[-1]["first_15m_return_inside_close_ts_ms"] = "43201000"
        result = validate_module_b_horizons(events, horizons)
        self.assertEqual(result["twelve_hour_confirmations"], 0)
        self.assertEqual(result["twelve_hour_endpoint_observations_excluded"], 1)

    def test_module_b_horizons_reject_confirmation_after_12h(self):
        events, horizons = self.sample_horizons()
        events[0]["first_15m_return_inside_close_ts_ms"] = "43201001"
        horizons[-1]["first_15m_return_inside_close_ts_ms"] = "43201001"
        with self.assertRaisesRegex(RuntimeError, "outside the 12-hour descriptive horizon"):
            validate_module_b_horizons(events, horizons)

    def test_canonical_confirmation_excludes_exact_12h_endpoint(self):
        self.assertIsNone(canonical_failed_breakout_confirmation(1000, 43201000))

    def test_canonical_confirmation_accepts_just_before_12h_endpoint(self):
        self.assertEqual(canonical_failed_breakout_confirmation(1000, 43200999), 43200999)

    def test_canonical_confirmation_rejects_after_descriptive_horizon(self):
        with self.assertRaisesRegex(ValueError, "descriptive horizon"):
            canonical_failed_breakout_confirmation(1000, 43201001)

    def test_failed_breakout_horizon_disposition_accepts_before_endpoint(self):
        self.assertEqual(
            failed_breakout_horizon_disposition(1000, 43200999, True),
            "CONFIRMED_WITHIN_12H")

    def test_failed_breakout_horizon_disposition_rejects_exact_endpoint(self):
        with self.assertRaisesRegex(ValueError, "half-open 12-hour"):
            failed_breakout_horizon_disposition(1000, 43201000, True)

    def test_incomplete_failed_breakout_confirmation_keeps_observation_but_no_candle(self):
        timing = failed_breakout_confirmation_timing(
            1000, 901000, None, True, 720)
        self.assertEqual(timing["confirmation_status"], "CENSORED")
        self.assertEqual(timing["event_observed_at_ts_ms"], 901000)
        self.assertEqual(timing["confirmation_open"], "")
        self.assertEqual(timing["signal_candle_close_ts_ms"], "")
        self.assertEqual(timing["signal_available_at_ts_ms"], "")

    def test_completed_failed_breakout_confirmation_exposes_completed_candle(self):
        timing = failed_breakout_confirmation_timing(
            1000, 901000, {"close": 99.0}, True, 720)
        self.assertEqual(timing["confirmation_status"], "CONFIRMED")
        self.assertEqual(timing["confirmation_open"], 1000)
        self.assertEqual(timing["signal_candle_close_ts_ms"], 901000)
        self.assertEqual(timing["signal_available_at_ts_ms"], 901000)
        self.assertEqual(timing["event_observed_at_ts_ms"], 901000)

    def test_only_eligible_failed_breakout_exposes_first_eligible_minute(self):
        self.assertEqual(first_eligible_minute_or_blank(
            "ELIGIBLE_FOR_FURTHER_VALIDATION", 123000), 123000)
        self.assertEqual(first_eligible_minute_or_blank("REJECTED", 123000), "")
        self.assertEqual(first_eligible_minute_or_blank("EXPIRED", None), "")
        self.assertEqual(first_eligible_minute_or_blank("CENSORED", 123000), "")

    def test_lagged_feature_reference_matches_exact_prior_4h_snapshot(self):
        features = {"BTC": {14400000: {"available_at_ts_ms": "14400000"}}}
        ts, row, status = resolve_lagged_feature_reference(features, "BTC", 28800000)
        self.assertEqual(ts, 14400000)
        self.assertEqual(row["available_at_ts_ms"], "14400000")
        self.assertEqual(status, "MATCHED_ONE_4H_LAG")

    def test_lagged_feature_reference_allows_only_expected_leading_boundary(self):
        features = {"BTC": {14400000: {"available_at_ts_ms": "14400000"}}}
        ts, row, status = resolve_lagged_feature_reference(features, "BTC", 14400000)
        self.assertEqual(ts, 0)
        self.assertIsNone(row)
        self.assertEqual(status, "EXPECTED_LEADING_LEGACY_BOUNDARY")

    def test_lagged_feature_reference_rejects_internal_missing_snapshot(self):
        features = {"BTC": {
            14400000: {"available_at_ts_ms": "14400000"},
            43200000: {"available_at_ts_ms": "43200000"},
        }}
        with self.assertRaisesRegex(ValueError, "missing non-leading"):
            resolve_lagged_feature_reference(features, "BTC", 72000000)

    def test_canonical_cohort_labels_match_frozen_schema_enum(self):
        cases = {
            "CAUSAL_STRICT": "STRICT_P25",
            "CAUSAL_BROAD_ONLY": "BROAD_ONLY",
            "CAUSAL_REGIME_NOT_ELIGIBLE": "NOT_ELIGIBLE",
            "CAUSAL_THRESHOLD_WARMUP": "WARMUP",
            "NOT_EVALUATED": "NOT_APPLICABLE",
        }
        for source, expected in cases.items():
            self.assertEqual(canonical_cohort_label(source), expected)
        with self.assertRaisesRegex(ValueError, "unknown causal cohort"):
            canonical_cohort_label("UNRECOGNIZED")

    def test_canonical_snapshot_provenance_uses_exact_prior_threshold(self):
        feature = {
            "available_at_ts_ms": "1000000", "upper": "110", "lower": "90",
            "channel_width_pct": "20", "directional_efficiency": "0.2",
            "mean_overlap": "0.8",
        }
        threshold = {
            "p25": "18", "p40": "22", "first_prior_context_ms": "1000",
            "last_prior_context_ms": "900000", "prior_context_count": "200",
        }
        strict = canonical_snapshot_provenance("BTC", 1000000, 2000000,
                                               feature, threshold, "CAUSAL_STRICT")
        broad = canonical_snapshot_provenance("BTC", 1000000, 2000000,
                                              feature, threshold, "CAUSAL_BROAD_ONLY")
        self.assertEqual(strict["threshold_value"], 18.0)
        self.assertEqual(strict["threshold_percentile"], 25)
        self.assertEqual(broad["threshold_value"], 22.0)
        self.assertEqual(broad["threshold_percentile"], 40)
        self.assertEqual(strict["instrument_id"], "BTC-USDT-SWAP")
        self.assertEqual(strict["snapshot_valid_until_ts_ms"], 2000000)
        self.assertEqual(strict["threshold_prior_observation_count"], 200)

    def test_canonical_snapshot_provenance_preserves_historical_lagged_context_version(self):
        feature = {
            "available_at_ts_ms": "1000000", "upper": "110", "lower": "90",
            "channel_width_pct": "20", "directional_efficiency": "0.4",
            "mean_overlap": "0.6",
        }
        threshold = {
            "p25": "18", "p40": "22", "first_prior_context_ms": "1000",
            "last_prior_context_ms": "900000", "prior_context_count": "200",
        }
        result = canonical_snapshot_provenance(
            "BTC", 1000000, 15000000, feature, threshold,
            "CAUSAL_REGIME_NOT_ELIGIBLE",
            regime_definition_version="HISTORICAL_BREAKOUT_CONTEXT_V1")
        self.assertEqual(result["regime_definition_version"],
                         "HISTORICAL_BREAKOUT_CONTEXT_V1")
        self.assertEqual(result["efficiency_value"], 0.4)
        self.assertEqual(result["overlap_value"], 0.6)

    def test_canonical_snapshot_provenance_preserves_unavailable_warmup_metrics(self):
        feature = {
            "available_at_ts_ms": "1000000", "upper": "110", "lower": "90",
            "channel_width_pct": "20", "directional_efficiency": "",
            "mean_overlap": "",
        }
        result = canonical_snapshot_provenance(
            "BTC", 1000000, 15000000, feature, None,
            "CAUSAL_THRESHOLD_WARMUP",
            regime_definition_version="HISTORICAL_BREAKOUT_CONTEXT_V1")
        self.assertEqual(result["efficiency_value"], "")
        self.assertEqual(result["overlap_value"], "")
        self.assertEqual(result["threshold_value"], "")
        self.assertEqual(result["threshold_percentile"], "")

    def test_canonical_snapshot_provenance_rejects_nonexact_snapshot(self):
        feature = {
            "available_at_ts_ms": "1000001", "upper": "110", "lower": "90",
            "channel_width_pct": "20", "directional_efficiency": "0.2",
            "mean_overlap": "0.8",
        }
        with self.assertRaisesRegex(ValueError, "exact match"):
            canonical_snapshot_provenance("BTC", 1000000, 2000000,
                                           feature, None, "WARMUP")

    def test_canonical_snapshot_provenance_rejects_future_calibration(self):
        feature = {
            "available_at_ts_ms": "1000000", "upper": "110", "lower": "90",
            "channel_width_pct": "20", "directional_efficiency": "0.2",
            "mean_overlap": "0.8",
        }
        threshold = {
            "p25": "18", "p40": "22", "first_prior_context_ms": "1000",
            "last_prior_context_ms": "1000000", "prior_context_count": "200",
        }
        with self.assertRaisesRegex(ValueError, "prior-only"):
            canonical_snapshot_provenance("BTC", 1000000, 2000000,
                                           feature, threshold, "CAUSAL_STRICT")

    def test_streaming_file_manifest_matches_git_blob_and_sha256(self):
        data = b"frozen source bytes\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "sample.csv"
            path.write_bytes(data)
            info = file_manifest_entry(path, root)
        self.assertEqual(info["path"], "sample.csv")
        self.assertEqual(info["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(info["git_blob_sha1"], git_blob_sha1(data))
        self.assertEqual(info["bytes"], len(data))

    def test_completed_15m_bar_requires_all_15_exact_minute_components(self):
        minute_bars = {
            i * 60000: (100.0, 101.0, 99.0, 100.0)
            for i in range(15)
        }
        bar = aggregate_completed_15m_bar(minute_bars, 900000)
        self.assertEqual(bar["component_minute_count"], 15)
        self.assertEqual(bar["bar_open_ts_ms"], 0)
        self.assertEqual(bar["bar_close_ts_ms"], 900000)
        self.assertEqual(bar["high"], 101.0)
        self.assertEqual(bar["low"], 99.0)
        del minute_bars[7 * 60000]
        self.assertIsNone(aggregate_completed_15m_bar(minute_bars, 900000))

    def test_completed_15m_bar_rejects_non_quarter_hour_close(self):
        with self.assertRaisesRegex(ValueError, "quarter-hour aligned"):
            aggregate_completed_15m_bar({}, 901000)

    def test_completed_15m_bar_rejects_invalid_component_ohlc(self):
        minute_bars = {
            i * 60000: (100.0, 99.0, 101.0, 100.0)
            for i in range(15)
        }
        with self.assertRaisesRegex(ValueError, "invalid 1m OHLC"):
            aggregate_completed_15m_bar(minute_bars, 900000)

    def test_confirmation_ambiguity_rejects_unknown_direction(self):
        with self.assertRaisesRegex(ValueError, "unknown breakout direction"):
            confirmation_ambiguity_flag("SIDEWAYS", 100.0,
                                         {"high": 101.0, "low": 99.0, "close": 100.0})

    def test_failed_breakout_confirmation_open_and_wick_ambiguity(self):
        upper_open = {"open": 101.0, "high": 102.0, "low": 98.0, "close": 99.0}
        lower_open = {"open": 99.0, "high": 102.0, "low": 98.0, "close": 101.0}
        upper_wick = {"open": 100.0, "high": 101.0, "low": 98.0, "close": 99.0}
        lower_wick = {"open": 100.0, "high": 102.0, "low": 99.0, "close": 101.0}
        ordinary_bar = {"open": 100.0, "high": 100.0, "low": 98.0, "close": 99.0}
        self.assertEqual(
            confirmation_ambiguity_flag("UPPER", 100.0, upper_open),
            "CONFIRMATION_CANDLE_OPEN_OUTSIDE_CLOSE_INSIDE")
        self.assertEqual(
            confirmation_ambiguity_flag("LOWER", 100.0, lower_open),
            "CONFIRMATION_CANDLE_OPEN_OUTSIDE_CLOSE_INSIDE")
        self.assertEqual(
            confirmation_ambiguity_flag("UPPER", 100.0, upper_wick),
            "CONFIRMATION_CANDLE_WICK_OUTSIDE_CLOSE_INSIDE")
        self.assertEqual(
            confirmation_ambiguity_flag("LOWER", 100.0, lower_wick),
            "CONFIRMATION_CANDLE_WICK_OUTSIDE_CLOSE_INSIDE")
        self.assertEqual(
            confirmation_ambiguity_flag("UPPER", 100.0, ordinary_bar), "NONE")

    def test_rejection_repeated_signal_group_uses_snapshot_and_segment(self):
        first = make_repeated_signal_group_id(
            "SUPPORT_REJECTION", "BTC", "lower", 12, segment_id=4)
        repeated = make_repeated_signal_group_id(
            "SUPPORT_REJECTION", "BTC", "lower", 12, segment_id=4)
        different_segment = make_repeated_signal_group_id(
            "SUPPORT_REJECTION", "BTC", "lower", 12, segment_id=5)
        different_snapshot = make_repeated_signal_group_id(
            "SUPPORT_REJECTION", "BTC", "lower", 13, segment_id=4)
        self.assertEqual(first, repeated)
        self.assertNotEqual(first, different_segment)
        self.assertNotEqual(first, different_snapshot)

    def test_breakout_repeated_signal_group_uses_context_and_direction(self):
        first = make_repeated_signal_group_id(
            "BREAKOUT_CONTINUATION", "BTC", "UPPER", 1761278400000)
        repeated = make_repeated_signal_group_id(
            "BREAKOUT_CONTINUATION", "BTC", "UPPER", 1761278400000)
        other_side = make_repeated_signal_group_id(
            "BREAKOUT_CONTINUATION", "BTC", "LOWER", 1761278400000)
        other_snapshot = make_repeated_signal_group_id(
            "BREAKOUT_CONTINUATION", "BTC", "UPPER", 1761292800000)
        self.assertEqual(first, repeated)
        self.assertNotEqual(first, other_side)
        self.assertNotEqual(first, other_snapshot)

    def test_failed_breakout_inherits_source_repeated_signal_group(self):
        source = "BTC|breakout|UPPER|snapshot_1761278400000"
        child = make_repeated_signal_group_id(
            "FAILED_BREAKOUT_REVERSAL", "BTC", "UPPER", 1761278400000,
            source_group_id=source)
        self.assertEqual(child, source)

    def test_repeated_signal_group_requires_frozen_source_context(self):
        with self.assertRaisesRegex(ValueError, "segment_id"):
            make_repeated_signal_group_id("SUPPORT_REJECTION", "BTC", "lower", 12)
        with self.assertRaisesRegex(ValueError, "snapshot"):
            make_repeated_signal_group_id("BREAKOUT_CONTINUATION", "BTC", "UPPER", "")
        with self.assertRaisesRegex(ValueError, "inherit"):
            make_repeated_signal_group_id("FAILED_BREAKOUT_REVERSAL", "BTC", "UPPER", 12)

    def test_observed_window_bars_requires_exact_start_and_stops_at_gap(self):
        minute_index = [0, 60000, 120000, 240000, 300000]
        self.assertEqual(observed_window_bars(minute_index, 60000, 10), 2)
        with self.assertRaisesRegex(ValueError, "missing exact"):
            observed_window_bars(minute_index, 180000, 10)

    def test_physical_cluster_requires_matching_cohort_rows(self):
        cluster = ("BTC|overlap|0001", 2, 1000, 2000)
        self.assertEqual(
            consistent_physical_cluster(["broad", "strict"],
                                         {"broad": cluster, "strict": cluster}),
            cluster,
        )

    def test_physical_cluster_rejects_cohort_cluster_mismatch(self):
        with self.assertRaisesRegex(ValueError, "disagree"):
            consistent_physical_cluster(
                ["broad", "strict"],
                {"broad": ("BTC|overlap|0001", 2, 1000, 2000),
                 "strict": ("BTC|overlap|0002", 1, 1000, 2000)},
            )

    def test_interval_graph_clusters_use_transitive_half_open_overlap(self):
        events = [
            {"asset": "BTC", "event_id": "a", "start": 0, "bars": 10},
            {"asset": "BTC", "event_id": "b", "start": 9 * MINUTE_MS, "bars": 11},
            {"asset": "BTC", "event_id": "c", "start": 19 * MINUTE_MS, "bars": 11},
            {"asset": "BTC", "event_id": "d", "start": 30 * MINUTE_MS, "bars": 1},
            {"asset": "ETH", "event_id": "e", "start": 0, "bars": 1},
        ]
        mapping, summary = assign_interval_graph_clusters(
            events, asset_field="asset", event_id_field="event_id",
            start_field="start", observed_bars_field="bars",
            cluster_prefix="g0_05_raw_overlap")
        self.assertEqual(mapping["a"]["overlap_cluster_id"], mapping["b"]["overlap_cluster_id"])
        self.assertEqual(mapping["b"]["overlap_cluster_id"], mapping["c"]["overlap_cluster_id"])
        self.assertNotEqual(mapping["c"]["overlap_cluster_id"], mapping["d"]["overlap_cluster_id"])
        self.assertEqual(mapping["a"]["overlap_cluster_size"], 3)
        self.assertEqual(mapping["d"]["overlap_cluster_size"], 1)
        self.assertEqual(mapping["e"]["overlap_cluster_size"], 1)
        self.assertEqual(summary["total"], 3)

    def test_interval_graph_cluster_results_are_input_order_independent(self):
        events = [
            {"asset": "BTC", "event_id": "b", "start": 9, "bars": 11},
            {"asset": "BTC", "event_id": "a", "start": 0, "bars": 10},
        ]
        args = dict(asset_field="asset", event_id_field="event_id",
                    start_field="start", observed_bars_field="bars",
                    cluster_prefix="g0_05_raw_overlap")
        first = assign_interval_graph_clusters(events, **args)
        second = assign_interval_graph_clusters(list(reversed(events)), **args)
        self.assertEqual(first, second)

    def test_interval_graph_clusters_reject_nonpositive_windows(self):
        events = [{"asset": "BTC", "event_id": "a", "start": 0, "bars": 0}]
        with self.assertRaisesRegex(ValueError, "at least one"):
            assign_interval_graph_clusters(
                events, asset_field="asset", event_id_field="event_id",
                start_field="start", observed_bars_field="bars",
                cluster_prefix="g0_05_raw_overlap")

    def test_interval_graph_clusters_reject_duplicate_event_ids(self):
        events = [
            {"asset": "BTC", "event_id": "a", "start": 0, "bars": 2},
            {"asset": "ETH", "event_id": "a", "start": 0, "bars": 2},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            assign_interval_graph_clusters(
                events, asset_field="asset", event_id_field="event_id",
                start_field="start", observed_bars_field="bars",
                cluster_prefix="g0_05_raw_overlap")

    def test_historical_breakout_membership_maps_both_nested_cohorts(self):
        self.assertEqual(
            historical_membership_label("true", {"BROAD_P40", "STRICT_P25"}),
            "BROAD_P40;STRICT_P25",
        )

    def test_historical_breakout_membership_maps_broad_only(self):
        self.assertEqual(
            historical_membership_label("true", {"BROAD_P40"}),
            "BROAD_P40",
        )

    def test_unselected_breakout_has_no_historical_cohort_membership(self):
        self.assertEqual(historical_membership_label("false", set()), "NONE")

    def test_historical_selected_flag_must_match_cohort_membership(self):
        with self.assertRaisesRegex(RuntimeError, "disagrees"):
            historical_membership_label("true", set())
        with self.assertRaisesRegex(RuntimeError, "disagrees"):
            historical_membership_label("false", {"BROAD_P40"})

    def test_historical_strict_membership_requires_broad(self):
        with self.assertRaisesRegex(RuntimeError, "not nested"):
            historical_membership_label("true", {"STRICT_P25"})

    def test_grouped_disposition_counts_are_deterministic_and_reconcile(self):
        rows = [
            {"asset": "BTC", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION"},
            {"asset": "BTC", "disposition": "REJECTED"},
            {"asset": "ETH", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION"},
        ]
        first = grouped_disposition_counts(rows, ("asset", "disposition"))
        second = grouped_disposition_counts(list(reversed(rows)), ("asset", "disposition"))
        self.assertEqual(first, second)
        self.assertEqual(sum(item["rows"] for item in first), len(rows))
        self.assertEqual(first, [
            {"asset": "BTC", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION", "rows": 1},
            {"asset": "BTC", "disposition": "REJECTED", "rows": 1},
            {"asset": "ETH", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION", "rows": 1},
        ])

    def test_disposition_ledger_enforces_frozen_reason_codes(self):
        rows = [
            {"id": "a", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION",
             "reason_code": "NONE", "censoring_reason": ""},
            {"id": "b", "disposition": "REJECTED",
             "reason_code": "CAUSAL_THRESHOLD_WARMUP", "censoring_reason": ""},
            {"id": "c", "disposition": "EXPIRED",
             "reason_code": "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION", "censoring_reason": ""},
            {"id": "d", "disposition": "CENSORED",
             "reason_code": "MISSING_OR_GAPPED_MINUTES",
             "censoring_reason": "MISSING_OR_GAPPED_MINUTES"},
        ]
        result = validate_disposition_ledger(rows, "id", 4)
        self.assertEqual(result["rows"], 4)

    def test_disposition_ledger_rejects_non_enum_broad_only_reason(self):
        rows = [{"id": "a", "disposition": "ELIGIBLE_FOR_FURTHER_VALIDATION",
                 "reason_code": "CAUSAL_BROAD_ONLY", "censoring_reason": ""}]
        with self.assertRaisesRegex(RuntimeError, "reason contract violation"):
            validate_disposition_ledger(rows, "id", 1)

    def test_disposition_ledger_rejects_unfrozen_failed_breakout_reason(self):
        rows = [{"id": "a", "disposition": "REJECTED",
                 "reason_code": "SOURCE_BREAKOUT_NOT_CAUSALLY_ELIGIBLE",
                 "censoring_reason": ""}]
        with self.assertRaisesRegex(RuntimeError, "reason contract violation"):
            validate_disposition_ledger(rows, "id", 1)

    def test_disposition_ledger_rejects_censor_reason_mismatch(self):
        rows = [{"id": "a", "disposition": "CENSORED",
                 "reason_code": "MISSING_OR_GAPPED_MINUTES",
                 "censoring_reason": "SOURCE_END_BEFORE_RESOLUTION"}]
        with self.assertRaisesRegex(RuntimeError, "reason contract violation"):
            validate_disposition_ledger(rows, "id", 1)

    def test_eligible_failed_breakout_requires_confirmation_minute(self):
        with self.assertRaisesRegex(RuntimeError, "missing its confirmation minute"):
            first_eligible_minute_or_blank("ELIGIBLE_FOR_FURTHER_VALIDATION", None)


if __name__ == "__main__":
    unittest.main()
