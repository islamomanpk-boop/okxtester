import unittest
import pandas as pd

from trade_candidate_engine import build_candidates


def make_row():
    ts = pd.Timestamp("2025-01-01T00:00:00Z")
    return {
        "ts": ts,
        "signal_available_at": ts + pd.Timedelta(minutes=15),
        "open": 100.0,
        "high": 102.0,
        "low": 98.0,
        "close": 101.0,
        "atr14": 2.0,
        "pa_direction_permission": "LONG_ONLY",
        "daily_structure": "BULLISH",
        "four_hour_structure": "BULLISH",
        "symbol": "BTC",
        "bullish_engulfing": False,
        "bearish_engulfing": False,
        "bullish_pinbar": False,
        "bearish_pinbar": False,
        "support_rejection": False,
        "resistance_rejection": False,
        "support_zone_touch": False,
        "resistance_zone_touch": False,
        "bullish_ob_first_retest": False,
        "bearish_ob_first_retest": False,
    }


class TradeCandidateTests(unittest.TestCase):
    def candidate(self, row):
        return build_candidates(pd.DataFrame([row]))

    def test_support_rejection_is_priority_three_long(self):
        row = make_row()
        row["support_rejection"] = True
        result = self.candidate(row)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["side"], 1)
        self.assertEqual(result[0]["signal_priority"], 3)
        self.assertEqual(result[0]["signal_type"], "support_rejection")

    def test_bearish_ob_retest_is_short_when_permitted(self):
        row = make_row()
        row["pa_direction_permission"] = "SHORT_ONLY"
        row["bearish_ob_first_retest"] = True
        result = self.candidate(row)
        self.assertEqual(result[0]["side"], -1)
        self.assertEqual(result[0]["signal_priority"], 3)

    def test_bullish_engulfing_at_support_is_priority_two(self):
        row = make_row()
        row["bullish_engulfing"] = True
        row["support_zone_touch"] = True
        result = self.candidate(row)
        self.assertEqual(result[0]["signal_priority"], 2)
        self.assertEqual(
            result[0]["signal_type"], "bullish_engulfing_at_support"
        )

    def test_bullish_pinbar_at_support_is_priority_two(self):
        row = make_row()
        row["bullish_pinbar"] = True
        row["support_zone_touch"] = True
        self.assertEqual(self.candidate(row)[0]["signal_priority"], 2)

    def test_bearish_engulfing_at_resistance_is_priority_two(self):
        row = make_row()
        row["pa_direction_permission"] = "SHORT_ONLY"
        row["bearish_engulfing"] = True
        row["resistance_zone_touch"] = True
        result = self.candidate(row)
        self.assertEqual(result[0]["signal_priority"], 2)
        self.assertEqual(
            result[0]["signal_type"], "bearish_engulfing_at_resistance"
        )

    def test_standalone_engulfing_is_priority_one(self):
        row = make_row()
        row["bullish_engulfing"] = True
        result = self.candidate(row)
        self.assertEqual(result[0]["signal_priority"], 1)
        self.assertEqual(result[0]["signal_type"], "bullish_engulfing")

    def test_zone_touch_without_matching_pattern_is_not_priority_two(self):
        row = make_row()
        row["bullish_engulfing"] = True
        row["resistance_zone_touch"] = True
        result = self.candidate(row)
        self.assertEqual(result[0]["signal_priority"], 1)

    def test_priority_three_wins_over_priority_two(self):
        row = make_row()
        row["support_rejection"] = True
        row["bullish_engulfing"] = True
        row["support_zone_touch"] = True
        result = self.candidate(row)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["signal_priority"], 3)

    def test_daily_four_hour_conflict_blocks_trend_candidate(self):
        row = make_row()
        row["pa_direction_permission"] = "NO_TREND"
        row["bullish_engulfing"] = True
        self.assertEqual(self.candidate(row), [])

    def test_opposite_direction_signal_is_blocked(self):
        row = make_row()
        row["pa_direction_permission"] = "LONG_ONLY"
        row["bearish_engulfing"] = True
        self.assertEqual(self.candidate(row), [])

    def test_long_stop_reference_uses_low_minus_point_one_atr(self):
        row = make_row()
        row["bullish_engulfing"] = True
        result = self.candidate(row)[0]
        self.assertAlmostEqual(result["stop_reference_price"], 97.8)

    def test_short_stop_reference_uses_high_plus_point_one_atr(self):
        row = make_row()
        row["pa_direction_permission"] = "SHORT_ONLY"
        row["bearish_engulfing"] = True
        result = self.candidate(row)[0]
        self.assertAlmostEqual(result["stop_reference_price"], 102.2)

    def test_signal_available_at_is_candle_close(self):
        row = make_row()
        row["bullish_engulfing"] = True
        result = self.candidate(row)[0]
        self.assertEqual(
            result["signal_available_at"] - result["signal_ts"],
            900_000,
        )

    def test_future_availability_time_is_rejected(self):
        row = make_row()
        row["signal_available_at"] += pd.Timedelta(minutes=1)
        with self.assertRaises(ValueError):
            self.candidate(row)

    def test_invalid_boolean_is_rejected(self):
        row = make_row()
        row["bullish_engulfing"] = "maybe"
        with self.assertRaises(ValueError):
            self.candidate(row)

    def test_duplicate_signal_timestamps_are_rejected(self):
        row = make_row()
        with self.assertRaises(ValueError):
            build_candidates(pd.DataFrame([row, row]))


if __name__ == "__main__":
    unittest.main()
