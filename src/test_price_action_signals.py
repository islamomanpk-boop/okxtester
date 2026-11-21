"""Automated tests for causal Price Action V1 signal detectors."""

import unittest
import numpy as np
import pandas as pd

from price_action_signals import detect_signals


def make_data(n=40):
    close = np.full(n, 100.0)
    return pd.DataFrame({
        "open": close.copy(),
        "high": close + 5,
        "low": close - 5,
        "close": close.copy(),
        "atr14": np.ones(n) * 10,
    })


class TestPriceActionSignals(unittest.TestCase):

    def test_engulfing(self):
        d = make_data(5)
        d.loc[0, ["open", "close"]] = [102, 98]
        d.loc[1, ["open", "close"]] = [97, 103]

        result = detect_signals(d)
        self.assertTrue(result.loc[1, "bullish_engulfing"])

    def test_bearish_engulfing(self):
        d = make_data(5)
        d.loc[0, ["open", "close"]] = [98, 102]
        d.loc[1, ["open", "close"]] = [103, 97]

        result = detect_signals(d)
        self.assertTrue(result.loc[1, "bearish_engulfing"])

    def test_bullish_pinbar(self):
        d = make_data(5)
        d.loc[2, ["open", "close", "high", "low"]] = [
            99, 100, 100.5, 96
        ]

        result = detect_signals(d)
        self.assertTrue(result.loc[2, "bullish_pinbar"])

    def test_bearish_pinbar(self):
        d = make_data(5)
        d.loc[2, ["open", "close", "high", "low"]] = [
            100, 99, 104, 98.5
        ]

        result = detect_signals(d)
        self.assertTrue(result.loc[2, "bearish_pinbar"])

    def test_pivot_confirmation_delay(self):
        d = make_data(15)
        d.loc[3, "high"] = 120

        result = detect_signals(d)

        # Pivot at candle 3 is not usable until candle 6 closes.
        self.assertFalse(result.loc[5, "pivot_high_confirmed"])
        self.assertTrue(result.loc[6, "pivot_high_confirmed"])
        self.assertEqual(result.loc[6, "confirmed_pivot_high"], 120)

    def test_support_requires_two_confirmed_pivots(self):
        d = make_data(20)

        # Two distinct pivot lows at the same price.
        d.loc[3, "low"] = 90
        d.loc[10, "low"] = 90

        # A rejection after the second pivot has been confirmed.
        d.loc[15, ["open", "high", "low", "close"]] = [
            91, 94, 89, 93
        ]

        result = detect_signals(d)
        self.assertTrue(result.loc[6, "pivot_low_confirmed"])
        self.assertTrue(result.loc[13, "pivot_low_confirmed"])
        self.assertTrue(result.loc[15, "support_rejection"])
        self.assertTrue(result.loc[15, "support_zone_touch"])

    def test_support_zone_touch_without_rejection(self):
        d = make_data(20)
        d.loc[3, "low"] = 90
        d.loc[10, "low"] = 90

        # Price enters the confirmed zone but closes inside it.
        d.loc[15, ["open", "high", "low", "close"]] = [
            92, 93, 89, 91
        ]

        result = detect_signals(d)
        self.assertTrue(result.loc[15, "support_zone_touch"])
        self.assertFalse(result.loc[15, "support_rejection"])

    def test_resistance_zone_touch_without_rejection(self):
        d = make_data(20)
        d.loc[3, "high"] = 110
        d.loc[10, "high"] = 110

        # Price enters the confirmed zone but closes inside it.
        d.loc[15, ["open", "high", "low", "close"]] = [
            109, 111, 108, 109
        ]

        result = detect_signals(d)
        self.assertTrue(result.loc[15, "resistance_zone_touch"])
        self.assertFalse(result.loc[15, "resistance_rejection"])

    def test_bullish_order_block_and_first_retest(self):
        d = make_data(15)

        # Last bearish candle among the five preceding candles.
        d.loc[4, ["open", "close", "high", "low"]] = [
            100, 98, 101, 97
        ]

        # Large bullish displacement above previous five highs.
        d.loc[5, ["open", "close", "high", "low"]] = [
            100, 120, 121, 99
        ]

        # First retest of the order-block range.
        d.loc[6, ["open", "close", "high", "low"]] = [
            99, 100, 101, 98
        ]

        # A later revisit must not count as a second first retest.
        d.loc[7, ["open", "close", "high", "low"]] = [
            99, 100, 101, 98
        ]

        result = detect_signals(d)
        self.assertTrue(result.loc[5, "bullish_ob_created"])
        self.assertEqual(result.loc[5, "bullish_ob_low"], 97)
        self.assertEqual(result.loc[5, "bullish_ob_high"], 101)
        self.assertTrue(result.loc[6, "bullish_ob_first_retest"])
        self.assertFalse(result.loc[7, "bullish_ob_first_retest"])

    def test_future_changes_do_not_change_past_signals(self):
        rng = np.random.default_rng(42)
        n = 100
        close = 100 + np.cumsum(rng.normal(0, 1, n))
        open_ = np.r_[close[0], close[:-1]]

        d = pd.DataFrame({
            "open": open_,
            "high": np.maximum(open_, close) + rng.uniform(0.1, 2, n),
            "low": np.minimum(open_, close) - rng.uniform(0.1, 2, n),
            "close": close,
            "atr14": np.ones(n) * 2,
        })

        changed = d.copy()
        cutoff = 60

        # Alter only candles strictly after the cutoff.
        changed.loc[cutoff + 1:, "open"] *= 1.5
        changed.loc[cutoff + 1:, "high"] *= 1.5
        changed.loc[cutoff + 1:, "low"] *= 1.5
        changed.loc[cutoff + 1:, "close"] *= 1.5

        original_result = detect_signals(d)
        changed_result = detect_signals(changed)

        columns = [
            c for c in original_result.columns
            if c in changed_result.columns
        ]

        pd.testing.assert_frame_equal(
            original_result.loc[:cutoff, columns],
            changed_result.loc[:cutoff, columns],
            check_dtype=False,
        )

    def test_invalid_ohlc_is_rejected(self):
        d = make_data(5)
        d.loc[2, "high"] = 1

        with self.assertRaises(ValueError):
            detect_signals(d)


if __name__ == "__main__":
    unittest.main(verbosity=2)
