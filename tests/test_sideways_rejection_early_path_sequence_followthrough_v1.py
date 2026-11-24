"""Synthetic tests for early-path sequence and post-landmark follow-through V1."""
import unittest
from types import SimpleNamespace
import numpy as np
import pandas as pd

from research.sideways_rejection_early_path_sequence_followthrough_v1 import (
    classify_sequence, analyze_event,
)


class SequenceTests(unittest.TestCase):
    def upper_arrays(self):
        ts = np.arange(15, dtype=np.int64) * 60_000
        op = np.full(15, 109.5)
        hi = np.full(15, 108.8)
        lo = np.full(15, 108.4)
        cl = np.full(15, 108.6)
        return ts, op, hi, lo, cl

    def test_four_upper_sequence_classes(self):
        ts, op, hi, lo, cl = self.upper_arrays()
        hi[2] = 109.2
        cl[5] = 107.8
        self.assertEqual(classify_sequence(ts, op, hi, lo, cl, 110, 100, "upper"),
                         ("RETEST_FIRST", 2, 5))

        ts, op, hi, lo, cl = self.upper_arrays()
        cl[2] = 107.8
        hi[5] = 109.2
        self.assertEqual(classify_sequence(ts, op, hi, lo, cl, 110, 100, "upper"),
                         ("SEPARATION_FIRST", 5, 2))

        ts, op, hi, lo, cl = self.upper_arrays()
        self.assertEqual(classify_sequence(ts, op, hi, lo, cl, 110, 100, "upper"),
                         ("NEITHER_WITHIN_15M", None, None))

        ts, op, hi, lo, cl = self.upper_arrays()
        hi[4] = 109.2
        cl[4] = 108.0
        self.assertEqual(classify_sequence(ts, op, hi, lo, cl, 110, 100, "upper"),
                         ("SAME_BAR_AMBIGUOUS", 4, 4))

    def test_lower_direction_symmetry(self):
        ts = np.arange(15, dtype=np.int64) * 60_000
        op = np.full(15, 100.5)
        hi = np.full(15, 101.6)
        lo = np.full(15, 101.2)
        cl = np.full(15, 101.4)
        lo[3] = 100.8
        cl[7] = 102.2
        self.assertEqual(classify_sequence(ts, op, hi, lo, cl, 110, 100, "lower"),
                         ("RETEST_FIRST", 3, 7))

    def test_classification_requires_exactly_15_bars(self):
        with self.assertRaises(ValueError):
            classify_sequence(np.arange(14), np.ones(14), np.ones(14),
                              np.ones(14), np.ones(14), 110, 100, "upper")

    def test_outcomes_start_after_classification_window(self):
        ts = np.arange(15 + 60, dtype=np.int64) * 60_000
        op = np.full(len(ts), 109.5)
        hi = np.full(len(ts), 108.8)
        lo = np.full(len(ts), 108.5)
        cl = np.full(len(ts), 109.2)
        hi[14] = 150.0  # Classification-window extreme must not leak forward.
        hi[18] = 109.2  # First future retest is three minutes after landmark.
        minutes = pd.DataFrame({"ts": ts, "open": op, "high": hi, "low": lo, "close": cl})
        event = SimpleNamespace(
            event_id="e1", asset="BTC", definition="broad", direction="upper",
            snapshot_index=0, segment_id=1, test_rank=1, test_start_ts_ms=0,
            first_strong_rejection_ts_ms=-900_000, confirmation_ts_ms=0,
        )
        seq, rows = analyze_event(event, pd.Series({"upper": 110.0, "lower": 100.0}), minutes)
        self.assertEqual(seq["classification_status"], "complete")
        self.assertEqual(seq["landmark_ts_ms"], 900_000)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["status"], "complete")
        self.assertGreaterEqual(rows[0]["landmark_ts_ms"], 900_000)
        self.assertLess(rows[0]["max_high"], 150.0)
        self.assertEqual(rows[0]["first_future_retest_elapsed_min"], 3.0)
        self.assertEqual(rows[1]["status"], "incomplete")
        self.assertEqual(rows[1]["censor_reason"], "insufficient_future_data")
        self.assertTrue(np.isnan(rows[1]["max_high"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
