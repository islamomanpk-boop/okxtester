import unittest

from research.phase3_g0_05_candidate_contract_v1 import (
    MINUTE_MS, FIFTEEN_MIN_MS, FAILURE_HORIZON_MS,
    snapshot_is_valid, rejection_confirmation, first_eligible_minute,
    family_side, complete_15m_confirmation, failed_breakout_confirmation,
    candidate_id, classify_disposition, deterministic_json,
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

    def test_failed_breakout_at_12h_boundary_accepted(self):
        result = failed_breakout_confirmation("UPPER", 99.0, 100.0,
                                               FAILURE_HORIZON_MS, 0, True)
        self.assertEqual(result["side"], "SHORT")

    def test_failed_breakout_after_12h_rejected(self):
        with self.assertRaisesRegex(ValueError, "12-hour"):
            failed_breakout_confirmation("UPPER", 99.0, 100.0,
                                          FAILURE_HORIZON_MS + 1, 0, True)

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

    def test_failed_breakout_confirmation_at_12h_boundary_is_valid(self):
        self.assertEqual(failed_breakout_horizon_disposition(0, FAILURE_HORIZON_MS, True),
                         "CONFIRMED_WITHIN_12H")

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

    def test_module_b_horizons_allow_exact_12h_confirmation(self):
        events, horizons = self.sample_horizons()
        events[0]["first_15m_return_inside_close_ts_ms"] = "43201000"
        horizons[-1]["first_15m_return_inside_close_ts_ms"] = "43201000"
        result = validate_module_b_horizons(events, horizons)
        self.assertEqual(result["twelve_hour_confirmations"], 1)

    def test_module_b_horizons_reject_confirmation_after_12h(self):
        events, horizons = self.sample_horizons()
        events[0]["first_15m_return_inside_close_ts_ms"] = "43201001"
        horizons[-1]["first_15m_return_inside_close_ts_ms"] = "43201001"
        with self.assertRaisesRegex(RuntimeError, "outside 12-hour horizon"):
            validate_module_b_horizons(events, horizons)

    def test_only_eligible_failed_breakout_exposes_first_eligible_minute(self):
        self.assertEqual(first_eligible_minute_or_blank(
            "ELIGIBLE_FOR_FURTHER_VALIDATION", 123000), 123000)
        self.assertEqual(first_eligible_minute_or_blank("REJECTED", 123000), "")
        self.assertEqual(first_eligible_minute_or_blank("EXPIRED", None), "")
        self.assertEqual(first_eligible_minute_or_blank("CENSORED", 123000), "")

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
