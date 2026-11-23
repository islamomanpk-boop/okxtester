"""Deterministic tests for the rejection outcome calendar-block bootstrap V1."""
import unittest

import numpy as np
import pandas as pd

from research.sideways_rejection_block_bootstrap_v1 import (
    contrast_from_sufficient_stats,
    daily_sufficient_stats,
    sample_day_multiplicities,
)


class TestBlockBootstrapV1(unittest.TestCase):
    def test_calendar_block_sampling_is_reproducible_and_preserves_calendar_length(self):
        first = sample_day_multiplicities(11, 3, np.random.default_rng(123))
        second = sample_day_multiplicities(11, 3, np.random.default_rng(123))
        np.testing.assert_array_equal(first, second)
        self.assertEqual(int(first.sum()), 11)
        self.assertEqual(len(first), 11)
        self.assertTrue(np.all(first >= 0))

    def test_calendar_days_without_events_remain_in_daily_arrays(self):
        calendar = pd.date_range("2026-01-01", periods=5, freq="D", tz="UTC")
        events = pd.DataFrame({
            "calendar_day": [calendar[0], calendar[2], calendar[2], calendar[4]],
            "direction": ["upper", "upper", "lower", "lower"],
            "15m_status": ["complete"] * 4,
            "15m_direction_adjusted_return": [0.02, 0.04, -0.01, 0.03],
        })
        upper_sum, upper_n, lower_sum, lower_n = daily_sufficient_stats(
            events, calendar, "15m"
        )
        self.assertEqual(len(upper_sum), 5)
        self.assertEqual(upper_n[1], 0)
        self.assertEqual(lower_n[3], 0)
        self.assertEqual(upper_n[0], 1)
        self.assertEqual(lower_n[4], 1)

    def test_horizon_censoring_excludes_incomplete_rows(self):
        calendar = pd.date_range("2026-01-01", periods=2, freq="D", tz="UTC")
        events = pd.DataFrame({
            "calendar_day": [calendar[0], calendar[0], calendar[1]],
            "direction": ["upper", "lower", "upper"],
            "1h_status": ["complete", "complete", "incomplete"],
            "1h_direction_adjusted_return": [0.03, -0.02, np.nan],
        })
        upper_sum, upper_n, lower_sum, lower_n = daily_sufficient_stats(
            events, calendar, "1h"
        )
        self.assertEqual(int(upper_n.sum()), 1)
        self.assertEqual(int(lower_n.sum()), 1)
        self.assertAlmostEqual(float(upper_sum.sum()), 0.03)
        self.assertAlmostEqual(float(lower_sum.sum()), -0.02)

    def test_upper_minus_lower_mean_contrast(self):
        weights = np.array([[1, 1], [2, 0]], dtype=float)
        upper_sum = np.array([0.04, 0.02])
        upper_n = np.array([2.0, 1.0])
        lower_sum = np.array([0.00, -0.02])
        lower_n = np.array([0.0, 1.0])
        result = contrast_from_sufficient_stats(
            weights, upper_sum, upper_n, lower_sum, lower_n
        )
        self.assertAlmostEqual(result[0], 0.04)
        self.assertTrue(np.isnan(result[1]))

    def test_one_shared_calendar_weight_vector_can_be_applied_to_all_assets(self):
        # A single sampled day multiplicity vector is the synchronous draw:
        # every asset uses these same date weights, not separate resamples.
        weights = sample_day_multiplicities(7, 2, np.random.default_rng(9))
        btc_daily = np.arange(7, dtype=float)
        eth_daily = np.arange(7, dtype=float) * 10
        self.assertAlmostEqual(float(weights @ eth_daily), 10 * float(weights @ btc_daily))
        self.assertEqual(int(weights.sum()), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
