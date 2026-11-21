"""Tests for causal, indicator-free market structure."""

import unittest
import numpy as np
import pandas as pd

from price_action_structure import (
    detect_structure,
    align_structure_to_signals,
)


def frame(high, low, close=None):
    n = len(high)
    if close is None:
        close = [(h + l) / 2 for h, l in zip(high, low)]
    return pd.DataFrame({
        "ts": np.arange(n, dtype=np.int64) * 60_000,
        "open": close,
        "high": high,
        "low": low,
        "close": close,
    })


class TestPriceActionStructure(unittest.TestCase):

    def test_pivot_waits_for_three_right_candles(self):
        d = frame(
            [10, 11, 12, 20, 13, 12, 11, 12, 13],
            [8, 9, 10, 11, 9, 8, 7, 8, 9],
        )
        r = detect_structure(d, 60_000)
        self.assertFalse(r.loc[5, "pivot_high_confirmed"])
        self.assertTrue(r.loc[6, "pivot_high_confirmed"])
        self.assertEqual(r.loc[6, "confirmed_pivot_high"], 20)
        self.assertEqual(r.loc[6, "structure_available_at"], 420_000)

    def test_no_pivot_without_three_left_and_right(self):
        d = frame([10, 11, 12, 20, 13], [8, 9, 10, 11, 9])
        r = detect_structure(d, 60_000)
        self.assertFalse(r["pivot_high_confirmed"].any())

    def test_bullish_bos_only_after_confirmed_level(self):
        high = [10, 11, 12, 20, 13, 12, 11, 15, 18, 21, 22]
        low =  [8, 9, 10, 11, 9, 8, 7, 9, 10, 12, 13]
        close = [9, 10, 11, 15, 12, 10, 9, 14, 17, 21, 21]
        d = frame(high, low, close)
        r = detect_structure(d, 60_000)
        self.assertFalse(r.loc[6, "bos_bullish"])
        self.assertTrue(r.loc[9, "bos_bullish"])
        self.assertEqual(r.loc[9, "bos_level"], 20)
        self.assertFalse(r.loc[10, "bos_bullish"])

    def test_indicator_columns_do_not_change_output(self):
        d = frame(
            [10, 11, 12, 20, 13, 12, 11, 12, 13],
            [8, 9, 10, 11, 9, 8, 7, 8, 9],
        )
        a = detect_structure(d, 60_000)
        d["ema200"] = np.arange(len(d)) * 999
        d["rsi14"] = 99
        d["adx14"] = 100
        b = detect_structure(d, 60_000)
        pd.testing.assert_series_equal(a["structure"], b["structure"])
        pd.testing.assert_series_equal(
            a["confirmed_pivot_high"], b["confirmed_pivot_high"]
        )

    def test_future_changes_do_not_change_past_results(self):
        rng = np.random.default_rng(7)
        close = 100 + np.cumsum(rng.normal(0, 1, 150))
        op = np.r_[close[0], close[:-1]]
        d = pd.DataFrame({
            "open": op,
            "high": np.maximum(op, close) + rng.uniform(.1, 1, 150),
            "low": np.minimum(op, close) - rng.uniform(.1, 1, 150),
            "close": close,
        })
        changed = d.copy()
        cutoff = 90
        changed.loc[cutoff+1:, ["open", "high", "low", "close"]] *= 1.7
        a = detect_structure(d, 60_000)
        b = detect_structure(changed, 60_000)
        cols = [
            "pivot_high_confirmed", "pivot_low_confirmed",
            "confirmed_pivot_high", "confirmed_pivot_low",
            "structure", "bos_bullish", "bos_bearish", "bos_level",
        ]
        pd.testing.assert_frame_equal(
            a.loc[:cutoff, cols], b.loc[:cutoff, cols],
            check_dtype=False,
        )

    def test_higher_timeframe_alignment_is_backward_only(self):
        structure = pd.DataFrame({
            "structure_available_at": [100, 200, 300],
            "structure": ["NEUTRAL", "BULLISH", "BEARISH"],
        })
        signals = pd.DataFrame({
            "signal_at": [99, 100, 199, 200, 250, 301]
        })
        r = align_structure_to_signals(
            signals, structure, "signal_at"
        )
        self.assertTrue(pd.isna(r.loc[0, "structure"]))
        self.assertEqual(r.loc[1, "structure"], "NEUTRAL")
        self.assertEqual(r.loc[2, "structure"], "NEUTRAL")
        self.assertEqual(r.loc[3, "structure"], "BULLISH")
        self.assertEqual(r.loc[4, "structure"], "BULLISH")
        self.assertEqual(r.loc[5, "structure"], "BEARISH")

    def test_invalid_timeframe_rejected(self):
        d = frame([10, 11], [8, 9])
        with self.assertRaises(ValueError):
            detect_structure(d, 0)

    def test_duplicate_timestamps_rejected(self):
        d = frame([10, 11, 12], [8, 9, 10])
        d.loc[2, "ts"] = d.loc[1, "ts"]
        with self.assertRaises(ValueError):
            detect_structure(d, 60_000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
