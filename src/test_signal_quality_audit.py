"""Tests for signal quality and distribution audit."""

import unittest

import pandas as pd

from signal_quality_audit import (
    REQUIRED, SIGNALS, PIVOTS, audit_frame, boolean_series,
)


def sample_frame():
    rows = []
    for i in range(4):
        row = {
            "ts": f"2026-01-01T00:{i:02d}:00Z",
            "regime": ["BULLISH", "BEARISH", "SIDEWAYS",
                       "NO_REGIME_AVAILABLE"][i],
        }
        row.update({col: False for col in SIGNALS + PIVOTS})
        rows.append(row)

    df = pd.DataFrame(rows)
    df.loc[0, "bullish_engulfing"] = True
    df.loc[0, "bullish_pinbar"] = True
    df.loc[1, "bearish_engulfing"] = True
    df.loc[2, "support_rejection"] = True
    df.loc[0, "pivot_high_confirmed"] = True
    df.loc[2, "pivot_low_confirmed"] = True
    return df


class TestSignalQualityAudit(unittest.TestCase):

    def test_counts_and_overlap(self):
        result = audit_frame(sample_frame(), "BTC")
        self.assertEqual(result["rows"], 4)
        self.assertEqual(result["total_events"], 4)
        self.assertEqual(result["event_rows"], 3)
        self.assertEqual(result["multi_signal_rows"], 1)
        self.assertEqual(result["max_signals_per_candle"], 2)
        self.assertEqual(result["overlap_distribution"]["2"], 1)
        self.assertEqual(result["overlap_distribution"]["1"], 2)
        self.assertEqual(result["pivot_event_rows"], 2)

    def test_regime_counts(self):
        result = audit_frame(sample_frame(), "BTC")
        self.assertEqual(
            result["regime_signal_counts"]["BULLISH"]["bullish_engulfing"],
            1,
        )
        self.assertEqual(
            result["regime_signal_counts"]["BEARISH"]["bearish_engulfing"],
            1,
        )

    def test_missing_columns_rejected(self):
        df = sample_frame().drop(columns=["bullish_pinbar"])
        with self.assertRaises(ValueError):
            audit_frame(df, "BTC")

    def test_duplicate_timestamps_rejected(self):
        df = sample_frame()
        df.loc[1, "ts"] = df.loc[0, "ts"]
        with self.assertRaises(ValueError):
            audit_frame(df, "BTC")

    def test_unknown_regime_rejected(self):
        df = sample_frame()
        df.loc[0, "regime"] = "UNKNOWN"
        with self.assertRaises(ValueError):
            audit_frame(df, "BTC")

    def test_invalid_boolean_rejected(self):
        values = pd.Series(["yes", "no"])
        with self.assertRaises(ValueError):
            boolean_series(values, "test")


if __name__ == "__main__":
    unittest.main()
