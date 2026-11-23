"""Tests for the historical-formula sideways detector reproduction V1."""

import unittest

import numpy as np
import pandas as pd

from research.sideways_detector_original_v1 import (
    FOUR_HOURS_MS,
    build_features,
    channel_width_pct,
    directional_efficiency,
    linear_quantile,
    mean_adjacent_overlap,
    pair_overlap_smaller_range,
)


class TestHistoricalSidewaysDetectorV1(unittest.TestCase):
    def test_channel_width_uses_upper_over_lower(self):
        highs = np.full(12, 110.0)
        lows = np.full(12, 100.0)
        self.assertAlmostEqual(channel_width_pct(highs, lows), 10.0)

    def test_channel_width_rejects_wrong_window_size(self):
        with self.assertRaises(ValueError):
            channel_width_pct(np.ones(11), np.zeros(11))

    def test_directional_efficiency_uses_13_closes_12_changes(self):
        self.assertAlmostEqual(directional_efficiency(np.arange(13, dtype=float)), 1.0)

    def test_directional_efficiency_rejects_12_closes(self):
        with self.assertRaises(ValueError):
            directional_efficiency(np.arange(12, dtype=float))

    def test_zero_path_efficiency_is_zero(self):
        self.assertEqual(directional_efficiency(np.full(13, 42.0)), 0.0)

    def test_overlap_is_intersection_over_smaller_range(self):
        # [0,10] and [5,15] share 5; smaller range is 10 => 0.5.
        self.assertAlmostEqual(
            pair_overlap_smaller_range(10.0, 0.0, 15.0, 5.0), 0.5
        )

    def test_nested_ranges_overlap_one(self):
        self.assertEqual(
            pair_overlap_smaller_range(15.0, 0.0, 10.0, 5.0), 1.0
        )

    def test_disjoint_ranges_overlap_zero(self):
        self.assertEqual(
            pair_overlap_smaller_range(10.0, 0.0, 20.0, 10.0), 0.0
        )

    def test_zero_width_pair_is_missing(self):
        self.assertTrue(np.isnan(
            pair_overlap_smaller_range(10.0, 10.0, 12.0, 8.0)
        ))

    def test_mean_overlap_skips_missing_pairs(self):
        highs = np.full(12, 10.0)
        lows = np.zeros(12)
        highs[0] = 1.0
        lows[0] = 1.0
        # The first adjacent pair is missing; the remaining ten are identical.
        self.assertEqual(mean_adjacent_overlap(highs, lows), 1.0)

    def test_mean_overlap_is_missing_when_all_pairs_are_missing(self):
        highs = np.ones(12)
        lows = np.ones(12)
        self.assertTrue(np.isnan(mean_adjacent_overlap(highs, lows)))

    def test_mean_overlap_all_equal_positive_ranges_is_one(self):
        self.assertEqual(
            mean_adjacent_overlap(np.full(12, 10.0), np.zeros(12)), 1.0
        )

    def test_mean_overlap_rejects_bad_shapes(self):
        with self.assertRaises(ValueError):
            mean_adjacent_overlap(np.ones(11), np.zeros(11))

    def test_linear_quantile(self):
        self.assertAlmostEqual(
            linear_quantile(np.array([0.0, 10.0, 20.0, 30.0]), 0.25), 7.5
        )

    def test_feature_alignment_uses_12_channel_bars_and_13_er_closes(self):
        rows = []
        for i in range(13):
            rows.append({
                "ts": i * FOUR_HOURS_MS,
                "open": 100.0 + i,
                "high": 102.0 + i,
                "low": 99.0 + i,
                "close": 101.0 + i,
                "vol": 1.0,
            })
        features = build_features(pd.DataFrame(rows), "TST")
        self.assertEqual(len(features), 1)
        first = features.iloc[0]
        self.assertEqual(first["channel_start_ts_ms"], FOUR_HOURS_MS)
        self.assertEqual(first["channel_end_candle_ts_ms"], 12 * FOUR_HOURS_MS)
        self.assertEqual(first["er_lookback_start_close_ts_ms"], 0)
        self.assertEqual(first["channel_window_candles"], 12)
        self.assertEqual(first["er_close_observations"], 13)
        self.assertEqual(first["er_close_changes"], 12)

    def test_2370_bars_produce_2358_feature_rows(self):
        rows = []
        for i in range(2370):
            base = 100.0 + (i % 17)
            rows.append({
                "ts": i * FOUR_HOURS_MS,
                "open": base,
                "high": base + 2.0,
                "low": base - 2.0,
                "close": base + 0.5,
                "vol": 1.0,
            })
        features = build_features(pd.DataFrame(rows), "TST")
        self.assertEqual(len(features), 2358)


if __name__ == "__main__":
    unittest.main(verbosity=2)
