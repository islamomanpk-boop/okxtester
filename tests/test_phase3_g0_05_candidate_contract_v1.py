import unittest

from research.phase3_g0_05_candidate_contract_v1 import (
    MINUTE_MS, FIFTEEN_MIN_MS, FAILURE_HORIZON_MS,
    snapshot_is_valid, rejection_confirmation, first_eligible_minute,
    family_side, complete_15m_confirmation, failed_breakout_confirmation,
    candidate_id, classify_disposition, deterministic_json,
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

    def test_deterministic_serialization(self):
        rows = [{"b": 2, "a": 1}]
        self.assertEqual(deterministic_json(rows), deterministic_json([{"a": 1, "b": 2}]))


if __name__ == "__main__":
    unittest.main()
