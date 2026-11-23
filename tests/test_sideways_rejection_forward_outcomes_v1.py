"""Unit tests for causal historical rejection forward outcomes V1."""
import unittest

import numpy as np

from research.sideways_rejection_forward_outcomes_v1 import (
    MINUTE_MS,
    calculate_horizon,
    direction_adjusted_return,
)


class TestForwardOutcomeV1(unittest.TestCase):
    def make_series(self, count):
        ts = np.arange(count, dtype=np.int64) * MINUTE_MS
        opens = np.full(count, 100.0)
        highs = np.full(count, 102.0)
        lows = np.full(count, 98.0)
        closes = np.full(count, 101.0)
        return ts, opens, highs, lows, closes

    def test_direction_adjusted_return_upper_and_lower(self):
        self.assertAlmostEqual(direction_adjusted_return(0.02, "upper"), -0.02)
        self.assertAlmostEqual(direction_adjusted_return(0.02, "lower"), 0.02)

    def test_exact_15m_horizon_uses_confirmation_through_plus_14m(self):
        ts, opens, highs, lows, closes = self.make_series(20)
        opens[2] = 100.0
        closes[16] = 90.0
        result = calculate_horizon(
            ts, opens, highs, lows, closes, 2 * MINUTE_MS, "upper", 15 * MINUTE_MS
        )
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["expected_bars"], 15)
        self.assertEqual(result["observed_bars"], 15)
        self.assertEqual(result["horizon_end_ts_ms"], 17 * MINUTE_MS)
        self.assertAlmostEqual(result["raw_return"], -0.10)
        self.assertAlmostEqual(result["direction_adjusted_return"], 0.10)

    def test_missing_future_minute_is_censored(self):
        ts, opens, highs, lows, closes = self.make_series(20)
        ts = np.delete(ts, 8)
        opens = np.delete(opens, 8)
        highs = np.delete(highs, 8)
        lows = np.delete(lows, 8)
        closes = np.delete(closes, 8)
        result = calculate_horizon(
            ts, opens, highs, lows, closes, 2 * MINUTE_MS, "lower", 15 * MINUTE_MS
        )
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["censor_reason"], "missing_or_irregular_minute")

    def test_no_lookahead_and_exact_confirmation_minute_required(self):
        ts, opens, highs, lows, closes = self.make_series(20)
        result = calculate_horizon(
            ts, opens, highs, lows, closes, 2 * MINUTE_MS + 30_000,
            "lower", 15 * MINUTE_MS
        )
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["censor_reason"], "missing_confirmation_minute")

    def test_lower_excursions_use_upside_as_favorable(self):
        ts, opens, highs, lows, closes = self.make_series(20)
        highs[2:17] = 110.0
        lows[2:17] = 95.0
        result = calculate_horizon(
            ts, opens, highs, lows, closes, 2 * MINUTE_MS, "lower", 15 * MINUTE_MS
        )
        self.assertAlmostEqual(result["favorable_excursion"], 0.10)
        self.assertAlmostEqual(result["adverse_excursion"], 0.05)


if __name__ == "__main__":
    unittest.main(verbosity=2)
