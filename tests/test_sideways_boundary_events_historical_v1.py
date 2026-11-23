"""Unit tests for historical 4H-to-15M boundary event reconstruction V1."""

import unittest

import pandas as pd

from research.sideways_boundary_events_historical_v1 import (
    FIFTEEN_MIN_MS,
    process_snapshot,
)


def feature():
    return pd.Series({
        "available_at_ts_ms": 0,
        "upper": 110.0,
        "lower": 100.0,
    })


def bars(rows):
    return pd.DataFrame([
        {
            "ts": ts, "open": close, "high": high,
            "low": low, "close": close, "vol": 1.0,
        }
        for ts, high, low, close in rows
    ])


class TestHistoricalBoundaryEventsV1(unittest.TestCase):
    def test_repeated_touches_need_separation_before_new_test(self):
        data = bars([
            (0, 109.5, 108.0, 108.8),                 # first upper touch + rejection
            (FIFTEEN_MIN_MS, 110.0, 109.0, 109.5),    # same test
            (2 * FIFTEEN_MIN_MS, 108.5, 106.0, 107.5),# separation; not a touch
            (3 * FIFTEEN_MIN_MS, 109.5, 108.5, 109.2),# second test
        ])
        tests, audit = process_snapshot(
            data, feature(), "TST", "strict", 0, 4 * FIFTEEN_MIN_MS, True
        )
        upper = [x for x in tests if x["direction"] == "upper"]
        self.assertEqual(len(upper), 2)
        self.assertEqual([x["test_rank"] for x in upper], [1, 2])
        self.assertEqual(upper[0]["first_strong_rejection_ts_ms"], 0)
        self.assertEqual(upper[0]["closure_reason"], "separated")
        self.assertEqual(upper[1]["test_start_ts_ms"], 3 * FIFTEEN_MIN_MS)
        self.assertEqual(audit["processed_eligible_bars"], 4)

    def test_separation_candle_cannot_start_next_test(self):
        data = bars([
            (0, 109.5, 108.0, 108.8),
            (FIFTEEN_MIN_MS, 109.8, 107.0, 107.5),  # wick touch + separation close
            (2 * FIFTEEN_MIN_MS, 109.6, 108.0, 109.2),
        ])
        tests, _ = process_snapshot(
            data, feature(), "TST", "strict", 0, 4 * FIFTEEN_MIN_MS, True
        )
        upper = [x for x in tests if x["direction"] == "upper"]
        self.assertEqual(len(upper), 2)
        self.assertEqual(upper[0]["test_end_ts_ms"], FIFTEEN_MIN_MS)
        self.assertEqual(upper[1]["test_start_ts_ms"], 2 * FIFTEEN_MIN_MS)

    def test_gap_closes_test_and_resets_rank(self):
        data = bars([
            (0, 109.5, 108.0, 109.2),
            (2 * FIFTEEN_MIN_MS, 109.6, 108.0, 109.2),
        ])
        tests, audit = process_snapshot(
            data, feature(), "TST", "broad", 0, 4 * FIFTEEN_MIN_MS, True
        )
        upper = [x for x in tests if x["direction"] == "upper"]
        self.assertEqual(len(upper), 2)
        self.assertEqual([x["test_rank"] for x in upper], [1, 1])
        self.assertEqual(upper[0]["closure_reason"], "15m_gap")
        self.assertEqual(audit["15m_gaps_within_snapshot"], 1)
        self.assertEqual(audit["continuity_segments"], 2)

    def test_lower_rejection_is_recorded_once(self):
        data = bars([
            (0, 102.0, 100.5, 101.2),
            (FIFTEEN_MIN_MS, 101.0, 100.2, 100.8),
            (2 * FIFTEEN_MIN_MS, 103.0, 102.5, 102.5),
        ])
        tests, _ = process_snapshot(
            data, feature(), "TST", "strict", 0, 4 * FIFTEEN_MIN_MS, True
        )
        lower = [x for x in tests if x["direction"] == "lower"]
        self.assertEqual(len(lower), 1)
        self.assertEqual(lower[0]["first_strong_rejection_ts_ms"], 0)
        self.assertEqual(lower[0]["closure_reason"], "separated")


if __name__ == "__main__":
    unittest.main(verbosity=2)
