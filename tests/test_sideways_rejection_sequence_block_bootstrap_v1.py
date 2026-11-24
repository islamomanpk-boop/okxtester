"""Synthetic tests for calendar moving-block bootstrap V1."""
import unittest
import numpy as np
import pandas as pd
from research.sideways_rejection_sequence_block_bootstrap_v1 import moving_block_contrast, CLASSES


class BlockBootstrapTests(unittest.TestCase):
    def make_data(self):
        rows = []
        start = pd.Timestamp("2025-01-01", tz="UTC")
        for day in range(30):
            for label, value in ((CLASSES[0], 2.0 + day * 0.01), (CLASSES[1], 1.0 + day * 0.01)):
                rows.append({"confirmation_ts_ms": int((start + pd.Timedelta(days=day)).timestamp() * 1000),
                             "sequence_class": label, "metric": value})
        return pd.DataFrame(rows)

    def test_observed_difference_and_deterministic_ci(self):
        data = self.make_data()
        a = moving_block_contrast(data, block_days=3, replicates=300,
                                  rng=np.random.default_rng(7))
        b = moving_block_contrast(data, block_days=3, replicates=300,
                                  rng=np.random.default_rng(7))
        self.assertAlmostEqual(a["observed_difference"], 1.0)
        self.assertEqual(a, b)
        self.assertEqual(a["valid_replicates"], 300)
        self.assertLess(a["ci_2_5"], a["ci_97_5"])

    def test_block_length_is_capped_to_calendar_span(self):
        data = self.make_data().iloc[:4].copy()
        result = moving_block_contrast(data, block_days=100, replicates=50,
                                       rng=np.random.default_rng(1))
        self.assertTrue(np.isfinite(result["observed_difference"]))

    def test_rejects_invalid_bootstrap_settings(self):
        with self.assertRaises(ValueError):
            moving_block_contrast(self.make_data(), block_days=0, replicates=10,
                                  rng=np.random.default_rng(1))


if __name__ == "__main__":
    unittest.main()
