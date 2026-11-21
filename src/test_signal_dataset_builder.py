"""Tests for causal ATR, regimes, and multi-timeframe PA alignment."""

import unittest

import numpy as np
import pandas as pd

from signal_dataset_builder import (
    calculate_atr14,
    attach_regimes,
    attach_structure,
    apply_direction_permission,
)


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
        self.assertEqual(
            result.loc[0, "indicator_regime"], "SIDEWAYS"
        )

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

    def test_structure_is_not_used_before_availability(self):
        signals = pd.DataFrame({
            "signal_available_at": pd.to_datetime([
                "2026-01-01 07:59:00+00:00",
                "2026-01-01 08:00:00+00:00",
                "2026-01-01 08:15:00+00:00",
            ], utc=True),
        })

        structure = pd.DataFrame({
            "daily_ts": pd.to_datetime([
                "2026-01-01 00:00:00+00:00",
            ], utc=True),
            "daily_structure_available_at": pd.to_datetime([
                "2026-01-01 08:00:00+00:00",
            ], utc=True),
            "daily_structure": ["BULLISH"],
            "daily_bos_bullish": [True],
            "daily_bos_bearish": [False],
        })

        result = attach_structure(signals, structure, "daily")

        self.assertEqual(
            result.loc[0, "daily_structure"],
            "NO_STRUCTURE_AVAILABLE",
        )
        self.assertEqual(result.loc[1, "daily_structure"], "BULLISH")
        self.assertEqual(result.loc[2, "daily_structure"], "BULLISH")
        self.assertFalse(result.loc[0, "daily_bos_bullish"])
        self.assertTrue(result.loc[1, "daily_bos_bullish"])

        matched = result["daily_structure_available_at"].notna()
        self.assertTrue(
            (
                result.loc[matched, "daily_structure_available_at"]
                <= result.loc[matched, "signal_available_at"]
            ).all()
        )

    def test_exact_availability_time_is_allowed(self):
        signals = pd.DataFrame({
            "signal_available_at": pd.to_datetime([
                "2026-01-01 04:00:00+00:00",
            ], utc=True),
        })
        structure = pd.DataFrame({
            "four_hour_ts": pd.to_datetime([
                "2026-01-01 00:00:00+00:00",
            ], utc=True),
            "four_hour_structure_available_at": pd.to_datetime([
                "2026-01-01 04:00:00+00:00",
            ], utc=True),
            "four_hour_structure": ["BEARISH"],
            "four_hour_bos_bullish": [False],
            "four_hour_bos_bearish": [True],
        })

        result = attach_structure(signals, structure, "four_hour")
        self.assertEqual(result.loc[0, "four_hour_structure"], "BEARISH")
        self.assertTrue(result.loc[0, "four_hour_bos_bearish"])

    def test_direction_permission_requires_timeframe_agreement(self):
        df = pd.DataFrame({
            "daily_structure": [
                "BULLISH", "BEARISH", "BULLISH",
                "BEARISH", "NEUTRAL", "NO_STRUCTURE_AVAILABLE",
            ],
            "four_hour_structure": [
                "BULLISH", "BEARISH", "BEARISH",
                "NEUTRAL", "BULLISH", "BULLISH",
            ],
        })

        result = apply_direction_permission(df)

        self.assertEqual(
            result["pa_direction_permission"].tolist(),
            [
                "LONG_ONLY",
                "SHORT_ONLY",
                "NO_TREND",
                "NO_TREND",
                "NO_TREND",
                "NO_TREND",
            ],
        )

    def test_structure_attachment_preserves_signal_order(self):
        signals = pd.DataFrame({
            "signal_id": [1, 2, 3],
            "signal_available_at": pd.to_datetime([
                "2026-01-01 08:15:00+00:00",
                "2026-01-01 04:15:00+00:00",
                "2026-01-01 12:15:00+00:00",
            ], utc=True),
        })

        structure = pd.DataFrame({
            "daily_structure_available_at": pd.to_datetime([
                "2026-01-01 00:00:00+00:00",
                "2026-01-01 08:00:00+00:00",
            ], utc=True),
            "daily_structure": ["NEUTRAL", "BULLISH"],
            "daily_bos_bullish": [False, True],
            "daily_bos_bearish": [False, False],
        })

        result = attach_structure(signals, structure, "daily")

        self.assertEqual(result["signal_id"].tolist(), [1, 2, 3])
        self.assertEqual(
            result["daily_structure"].tolist(),
            ["BULLISH", "NEUTRAL", "BULLISH"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
