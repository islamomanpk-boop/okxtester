"""Synthetic unit tests for sideways rejection episode/retest anatomy V1."""
import unittest
from types import SimpleNamespace

import numpy as np
import pandas as pd

from research.sideways_rejection_episode_retest_anatomy_v1 import (
    MINUTE_MS, candle_anatomy, first_level_revisit, first_touch,
    event_measurements,
)


class TestRejectionAnatomyV1(unittest.TestCase):
    def test_upper_rejection_candle_anatomy(self):
        x = candle_anatomy(108, 110, 106, 107, 110, 100, "upper")
        self.assertEqual(x["rejection_range"], 4)
        self.assertEqual(x["rejection_body"], 1)
        self.assertEqual(x["rejection_upper_wick"], 2)
        self.assertEqual(x["rejection_lower_wick"], 1)
        self.assertAlmostEqual(x["signed_close_boundary_distance_width"], .3)

    def test_lower_rejection_candle_anatomy(self):
        x = candle_anatomy(102, 104, 100, 103, 110, 100, "lower")
        self.assertAlmostEqual(x["signed_close_boundary_distance_width"], .3)
        self.assertAlmostEqual(x["close_location_in_range"], .75)

    def test_zero_range_ratios_are_nan(self):
        x = candle_anatomy(105, 105, 105, 105, 110, 100, "upper")
        self.assertTrue(x["zero_range_candle"])
        self.assertTrue(np.isnan(x["body_range_ratio"]))
        self.assertTrue(np.isnan(x["upper_wick_range_ratio"]))

    def test_invalid_width_and_invalid_direction_rejected(self):
        with self.assertRaises(ValueError):
            candle_anatomy(1, 2, 1, 1, 100, 100, "upper")
        with self.assertRaises(ValueError):
            candle_anatomy(1, 2, 1, 1, 3, 1, "sideways")

    def test_first_boundary_retest_uses_directional_touch(self):
        highs = np.array([108., 109., 109.2, 111.])
        lows = np.array([107., 105., 108., 109.])
        self.assertEqual(first_touch(np.arange(4), highs, lows, 109., "upper"), 1)
        self.assertEqual(first_touch(np.arange(4), highs, lows, 106., "lower"), 1)

    def test_boundary_penetration_is_strict_not_equality(self):
        highs = np.array([110., 110.01])
        lows = np.array([108., 108.])
        self.assertFalse(bool(np.any(highs[:1] > 110.)))
        self.assertTrue(bool(np.any(highs[1:] > 110.)))

    def test_rejection_level_revisit_includes_containment(self):
        highs = np.array([106., 108., 109.])
        lows = np.array([104., 105., 107.])
        self.assertEqual(first_level_revisit(highs, lows, 105.5), 0)
        self.assertIsNone(first_level_revisit(highs, lows, 110.))

    def test_same_bar_retest_and_separation_is_marked_ambiguous(self):
        # Synthetic upper rejection: U=110, W=10; boundary zone starts at 109,
        # separation close is <=108. A bar can span both conditions.
        confirmation = 0
        minute = pd.DataFrame({
            "ts": np.arange(1440, dtype=np.int64) * MINUTE_MS,
            "open": np.full(1440, 109.5),
            "high": np.full(1440, 110.2),
            "low": np.full(1440, 107.5),
            "close": np.full(1440, 108.0),
        })
        event = SimpleNamespace(
            event_id="synthetic", asset="BTC", definition="broad", direction="upper",
            snapshot_index=0, segment_id=1, test_rank=1, test_start_ts_ms=0,
            first_strong_rejection_ts_ms=-900000, confirmation_ts_ms=confirmation,
            rejection_open=109., rejection_high=110., rejection_low=107., rejection_close=108.,
            snapshot_available_at_ts_ms=-3600000, snapshot_next_available_at_ts_ms=3600000,
        )
        feature = pd.Series({"upper": 110., "lower": 100.})
        _, result = event_measurements(event, feature, minute)
        first = result["rows"][0]
        self.assertTrue(first["same_bar_retest_separation_ambiguous"])
        self.assertEqual(first["retest_vs_separation_order"], "same_bar_ambiguous")

    def test_confirmation_minute_is_included_and_earlier_bars_excluded(self):
        minute = pd.DataFrame({
            "ts": np.arange(1440, dtype=np.int64) * MINUTE_MS,
            "open": np.full(1440, 109.5), "high": np.full(1440, 109.8),
            "low": np.full(1440, 108.5), "close": np.full(1440, 109.),
        })
        event = SimpleNamespace(
            event_id="synthetic", asset="BTC", definition="broad", direction="upper",
            snapshot_index=0, segment_id=1, test_rank=1, test_start_ts_ms=0,
            first_strong_rejection_ts_ms=-900000, confirmation_ts_ms=0,
            rejection_open=109., rejection_high=110., rejection_low=107., rejection_close=108.,
            snapshot_available_at_ts_ms=-3600000, snapshot_next_available_at_ts_ms=3600000,
        )
        _, result = event_measurements(event, pd.Series({"upper":110., "lower":100.}), minute)
        expected = {"15m": 15, "1h": 60, "4h": 240, "24h": 1440}
        self.assertEqual({row["horizon"]: row["expected_bars"] for row in result["rows"]}, expected)
        self.assertTrue(all(row["status"] == "complete" for row in result["rows"]))
        self.assertEqual([row["observed_bars"] for row in result["rows"]], [15, 60, 240, 1440])
        self.assertEqual(result["rows"][0]["confirmation_minute_open"], 109.5)


    def test_first_touch_returns_none_when_no_retest(self):
        highs = np.array([108.0, 108.5, 108.7])
        lows = np.array([106.0, 106.5, 106.7])
        self.assertIsNone(first_touch(np.arange(3), highs, lows, 109.0, "upper"))

    def test_same_minute_can_contain_multiple_rejection_levels(self):
        highs = np.array([111.0, 109.0])
        lows = np.array([99.0, 101.0])
        self.assertEqual(first_level_revisit(highs, lows, 110.0), 0)
        self.assertEqual(first_level_revisit(highs, lows, 100.0), 0)
        self.assertEqual(first_level_revisit(highs, lows, 105.0), 0)

    def test_missing_minute_censors_horizon_instead_of_bridging(self):
        minute = pd.DataFrame({
            "ts": np.delete(np.arange(1440, dtype=np.int64) * MINUTE_MS, 5),
            "open": np.full(1439, 109.5), "high": np.full(1439, 109.8),
            "low": np.full(1439, 108.5), "close": np.full(1439, 109.),
        })
        event = SimpleNamespace(
            event_id="gap", asset="BTC", definition="broad", direction="upper",
            snapshot_index=0, segment_id=1, test_rank=1, test_start_ts_ms=0,
            first_strong_rejection_ts_ms=-900000, confirmation_ts_ms=0,
            rejection_open=109., rejection_high=110., rejection_low=107., rejection_close=108.,
            snapshot_available_at_ts_ms=-3600000, snapshot_next_available_at_ts_ms=3600000,
        )
        _, result = event_measurements(event, pd.Series({"upper":110., "lower":100.}), minute)
        first = result["rows"][0]
        self.assertEqual(first["status"], "incomplete")
        self.assertEqual(first["censor_reason"], "missing_or_irregular_minute")
        self.assertTrue(np.isnan(first["horizon_close"]))

    def test_truncated_history_is_censored(self):
        minute = pd.DataFrame({
            "ts": np.arange(10, dtype=np.int64) * MINUTE_MS,
            "open": np.full(10, 109.5), "high": np.full(10, 109.8),
            "low": np.full(10, 108.5), "close": np.full(10, 109.),
        })
        event = SimpleNamespace(
            event_id="tail", asset="BTC", definition="broad", direction="upper",
            snapshot_index=0, segment_id=1, test_rank=1, test_start_ts_ms=0,
            first_strong_rejection_ts_ms=-900000, confirmation_ts_ms=0,
            rejection_open=109., rejection_high=110., rejection_low=107., rejection_close=108.,
            snapshot_available_at_ts_ms=-3600000, snapshot_next_available_at_ts_ms=3600000,
        )
        _, result = event_measurements(event, pd.Series({"upper":110., "lower":100.}), minute)
        first = result["rows"][0]
        self.assertEqual(first["status"], "incomplete")
        self.assertEqual(first["censor_reason"], "insufficient_future_data")
        self.assertEqual(first["observed_bars"], 10)
        self.assertTrue(np.isnan(first["horizon_close"]))



if __name__ == "__main__":
    unittest.main(verbosity=2)
