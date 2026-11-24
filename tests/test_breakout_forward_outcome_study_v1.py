"""Unit tests for breakout forward-outcome measurements V1."""

import unittest
import pandas as pd

from research.breakout_forward_outcomes.breakout_forward_outcome_study_v1 import (
    classification_group,
    measure_horizon,
    build_event_rows,
)


class TestBreakoutForwardOutcomeV1(unittest.TestCase):

    def make_window(self, rows):
        start = pd.Timestamp("2025-01-01T00:00:00Z")
        index = pd.date_range(start, periods=len(rows), freq="1min")
        return pd.DataFrame(
            rows, columns=["open", "high", "low", "close"], index=index
        )

    def test_entry_uses_first_minute_after_signal_close(self):
        signal_time = pd.Timestamp("2025-01-01T00:15:00Z")
        index = pd.date_range(
            "2025-01-01T00:00:00Z", periods=735, freq="1min"
        )

        minute = pd.DataFrame({
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.0,
            "vol": 1.0,
        }, index=index)

        # Distinguish the final signal minute from the actual entry minute.
        minute.loc[signal_time - pd.Timedelta(minutes=1), "open"] = 110.0
        minute.loc[signal_time, ["open", "high", "low", "close"]] = [
            200.0, 202.0, 199.0, 201.0
        ]

        classification = pd.DataFrame([{
            "asset": "BTC",
            "definition": "BROAD_P40",
            "direction": "UPPER",
            "signal_time": signal_time,
            "zone_pct_of_channel": 10.0,
            "snapshot": signal_time - pd.Timedelta(hours=1),
            "boundary": 150.0,
            "upper": 150.0,
            "lower": 140.0,
            "channel_width_price": 10.0,
            "channel_width_pct": 5.0,
            "prior_touch_test_count": 0,
            "prior_confirmed_rejection_count": 0,
            "prior_contact_only_test_count": 0,
            "pre_breakout_group": "DIRECT",
        }])

        result = build_event_rows(
            classification,
            {"BTC": minute},
        )

        self.assertEqual(len(result), 4)
        self.assertTrue((result["entry_time"] == signal_time).all())
        self.assertTrue((result["entry_open"] == 200.0).all())
        self.assertTrue((result["entry_price"] == 200.0).all())
        self.assertTrue((result["horizon_status"] == "COMPLETE").all())

    def test_upper_mfe_mae(self):
        w = self.make_window([
            (101, 103, 99, 102),
            (102, 105, 100, 104),
            (104, 104, 98, 100),
        ])
        r = measure_horizon(w, "UPPER", 100, 102, 10, w.index[0])
        self.assertAlmostEqual(r["mfe_pct"], 5)
        self.assertAlmostEqual(r["mae_pct"], 2)
        self.assertEqual(r["time_to_mfe_minutes"], 1)
        self.assertEqual(r["time_to_mae_minutes"], 2)

    def test_lower_mfe_mae(self):
        w = self.make_window([
            (99, 101, 97, 98),
            (98, 100, 95, 96),
            (96, 102, 96, 100),
        ])
        r = measure_horizon(w, "LOWER", 100, 98, 10, w.index[0])
        self.assertAlmostEqual(r["mfe_pct"], 5)
        self.assertAlmostEqual(r["mae_pct"], 2)
        self.assertEqual(r["time_to_mfe_minutes"], 1)
        self.assertEqual(r["time_to_mae_minutes"], 2)

    def test_first_extreme_tie(self):
        w = self.make_window([
            (100, 105, 99, 101),
            (101, 105, 98, 100),
            (100, 104, 98, 100),
        ])
        r = measure_horizon(w, "UPPER", 100, 102, 10, w.index[0])
        self.assertEqual(r["time_to_mfe_minutes"], 0)
        self.assertEqual(r["time_to_mae_minutes"], 1)

    def test_upper_boundary_failure(self):
        w = self.make_window([
            (100, 103, 99, 100),
            (100, 104, 100, 103),
        ])
        r = measure_horizon(w, "UPPER", 100, 100, 10, w.index[0])
        self.assertTrue(r["entry_open_already_through_boundary"])
        self.assertTrue(r["boundary_failure"])
        self.assertEqual(r["minutes_to_boundary_failure"], 0)

    def test_lower_boundary_failure(self):
        w = self.make_window([
            (100, 102, 98, 99),
            (99, 101, 97, 100),
        ])
        r = measure_horizon(w, "LOWER", 100, 100, 10, w.index[0])
        self.assertTrue(r["entry_open_already_through_boundary"])
        self.assertTrue(r["boundary_failure"])

    def test_no_boundary_failure(self):
        w = self.make_window([
            (100, 105, 100, 104),
            (104, 106, 103, 105),
        ])
        r = measure_horizon(w, "UPPER", 100, 99, 10, w.index[0])
        self.assertFalse(r["boundary_failure"])
        self.assertTrue(pd.isna(r["boundary_failure_time"]))

    def test_excursions_nonnegative(self):
        w = self.make_window([
            (100, 99, 95, 96),
            (96, 98, 94, 95),
        ])
        r = measure_horizon(w, "UPPER", 100, 90, 10, w.index[0])
        self.assertEqual(r["mfe_pct"], 0)
        self.assertGreaterEqual(r["mae_pct"], 0)

    def test_group_mapping(self):
        self.assertEqual(classification_group(0, 0), "DIRECT")
        self.assertEqual(classification_group(2, 0), "CONTACT_ONLY")
        self.assertEqual(classification_group(1, 1), "ONE_REJECTION")
        self.assertEqual(classification_group(2, 2), "TWO_REJECTIONS")
        self.assertEqual(classification_group(4, 3), "THREE_PLUS_REJECTIONS")

    def test_invalid_group_counts(self):
        with self.assertRaises(ValueError):
            classification_group(1, 2)

    def test_invalid_direction(self):
        w = self.make_window([(100, 101, 99, 100)])
        with self.assertRaises(ValueError):
            measure_horizon(w, "SIDEWAYS", 100, 100, 10, w.index[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
