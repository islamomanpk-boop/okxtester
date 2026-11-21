"""Unit tests for execution data audit."""

import unittest
import pandas as pd

from execution_data_audit import audit_frame


def sample():
    return pd.DataFrame({
        "ts": [1760950200000, 1760950260000, 1760950320000],
        "open": [100.0, 101.0, 100.5],
        "high": [102.0, 102.0, 101.0],
        "low": [99.0, 100.0, 99.5],
        "close": [101.0, 100.5, 100.0],
        "vol": [10.0, 12.0, 8.0],
    })


class TestExecutionAudit(unittest.TestCase):

    def test_valid_data(self):
        result = audit_frame(sample(), "BTC")
        self.assertEqual(result["rows"], 3)
        self.assertEqual(result["unexpected_intervals"], 0)

    def test_duplicate_timestamps(self):
        df = sample()
        df.loc[1, "ts"] = df.loc[0, "ts"]
        with self.assertRaises(ValueError):
            audit_frame(df, "BTC")

    def test_invalid_ohlc(self):
        df = sample()
        df.loc[0, "high"] = 98.0
        with self.assertRaises(ValueError):
            audit_frame(df, "BTC")

    def test_negative_volume(self):
        df = sample()
        df.loc[0, "vol"] = -1
        with self.assertRaises(ValueError):
            audit_frame(df, "BTC")

    def test_missing_column(self):
        df = sample().drop(columns=["close"])
        with self.assertRaises(ValueError):
            audit_frame(df, "BTC")

    def test_missing_interval_detected(self):
        df = sample().drop(index=1).reset_index(drop=True)
        result = audit_frame(df, "BTC")
        self.assertEqual(result["unexpected_intervals"], 1)


if __name__ == "__main__":
    unittest.main()
