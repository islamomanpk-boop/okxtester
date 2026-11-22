"""Unit tests for the reconstructed sideways detector v1."""

import unittest
import numpy as np

from research.sideways_detector_v1 import (
    WINDOW,
    directional_efficiency,
    pair_overlap,
    mean_adjacent_overlap,
    linear_quantile,
)


class TestSidewaysDetectorV1(unittest.TestCase):
    def test_directional_efficiency_uses_12_closes_and_11_changes(self):
        closes = np.arange(12, dtype=float)
        self.assertAlmostEqual(directional_efficiency(closes), 1.0)

    def test_zero_path_efficiency_is_zero(self):
        self.assertEqual(directional_efficiency(np.full(WINDOW, 123.0)), 0.0)

    def test_efficiency_rejects_wrong_window_length(self):
        with self.assertRaises(ValueError):
            directional_efficiency(np.arange(13, dtype=float))

    def test_identical_ranges_overlap_one(self):
        self.assertEqual(pair_overlap(10.0, 0.0, 10.0, 0.0), 1.0)

    def test_disjoint_ranges_overlap_zero(self):
        self.assertEqual(pair_overlap(10.0, 0.0, 20.0, 10.0), 0.0)

    def test_partial_overlap_uses_intersection_over_union(self):
        self.assertAlmostEqual(pair_overlap(10.0, 0.0, 15.0, 5.0), 1.0 / 3.0)

    def test_mean_overlap_has_eleven_adjacent_pairs(self):
        highs = np.full(WINDOW, 10.0)
        lows = np.zeros(WINDOW)
        self.assertEqual(mean_adjacent_overlap(highs, lows), 1.0)

    def test_linear_quantile(self):
        self.assertAlmostEqual(
            linear_quantile(np.array([0.0, 10.0, 20.0, 30.0]), 0.25),
            7.5,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
