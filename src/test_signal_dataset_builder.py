"""Tests for causal ATR and 15m-to-4h regime alignment."""

import unittest

import numpy as np
import pandas as pd

from signal_dataset_builder import calculate_atr14, attach_regimes


class TestSignalDatasetBuilder(unittest.TestCase):

    def test_atr_does_not_use_future_candles(self):
        n = 40
        close = np.linspace(100, 120, n)
        df = pd.DataFrame({
            "open": close - 0.5,
            "high": close + 1,
            "low": close - 1,
            "close": close,
        })

        changed = df.copy()
        changed.loc[25:, ["open", "high", "low", "close"]] *= 3

        original_atr = calculate_atr14(df)
        changed_atr = calculate_atr14(changed)

        pd.testing.assert_series_equal(
            original_atr.iloc[:25],
            changed_atr.iloc[:25],
        )

    def test_regime_is_not_used_before_available_at(self):
        signals = pd.DataFrame({
            "ts": pd.to_datetime([
                "2026-01-01 03:45:00+00:00",
                "2026-01-01 04:00:00+00:00",
                "2026-01-01 04:15:00+00:00",
            ], utc=True),
            "signal_available_at": pd.to_datetime([
                "2026-01-01 04:00:00+00:00",
                "2026-01-01 04:15:00+00:00",
                "2026-01-01 04:30:00+00:00",
            ], utc=True),
        })

        regimes = pd.DataFrame({
            "regime_ts": pd.to_datetime([
                "2026-01-01 00:00:00+00:00",
                "2026-01-01 04:00:00+00:00",
            ], utc=True),
            "regime_available_at": pd.to_datetime([
                "2026-01-01 04:00:00+00:00",
                "2026-01-01 08:00:00+00:00",
            ], utc=True),
            "regime": ["SIDEWAYS", "BULLISH"],
        })

        result = attach_regimes(signals, regimes)

        self.assertEqual(result.loc[0, "regime"], "SIDEWAYS")
        self.assertEqual(result.loc[1, "regime"], "SIDEWAYS")
        self.assertEqual(result.loc[2, "regime"], "SIDEWAYS")

        self.assertTrue(
            (
                result["regime_available_at"]
                <= result["signal_available_at"]
            ).all()
        )

    def test_no_regime_before_first_available_time(self):
        signals = pd.DataFrame({
            "signal_available_at": pd.to_datetime([
                "2026-01-01 03:59:00+00:00",
                "2026-01-01 04:00:00+00:00",
            ], utc=True),
        })

        regimes = pd.DataFrame({
            "regime_ts": pd.to_datetime([
                "2026-01-01 00:00:00+00:00",
            ], utc=True),
            "regime_available_at": pd.to_datetime([
                "2026-01-01 04:00:00+00:00",
            ], utc=True),
            "regime": ["BEARISH"],
        })

        result = attach_regimes(signals, regimes)

        self.assertEqual(result.loc[0, "regime"], "NO_REGIME_AVAILABLE")
        self.assertEqual(result.loc[1, "regime"], "BEARISH")


if __name__ == "__main__":
    unittest.main(verbosity=2)
