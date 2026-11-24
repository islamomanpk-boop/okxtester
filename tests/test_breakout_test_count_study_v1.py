"""Unit tests for causal breakout prior-test classification V1."""

import unittest

import pandas as pd

from research.breakout_test_count.breakout_test_count_study_v1 import (
    classify_events,
    group_summary,
)

STEP = pd.Timedelta(minutes=15)


def joined(rows, snapshots=None, times=None):
    start = pd.Timestamp("2025-01-01T00:00:00Z")
    if times is None:
        times = [start + i * STEP for i in range(len(rows))]
    if snapshots is None:
        snapshots = [start - pd.Timedelta(hours=4)] * len(rows)
    frame = pd.DataFrame(rows, columns=["open", "high", "low", "close"])
    frame["snapshot"] = snapshots
    frame["upper"] = 103.0
    frame["lower"] = 100.0
    frame["channel_width"] = 3.0
    frame["efficiency"] = 0.10
    frame["overlap"] = 0.80
    frame.index = pd.DatetimeIndex(times, name="time")
    return frame


def event(time, direction="UPPER"):
    return {
        "asset": "BTC",
        "definition": "STRICT_P25",
        "direction": direction,
        "signal_time": time,
        "snapshot": pd.Timestamp("2024-12-31T20:00:00Z"),
        "boundary": 103.0 if direction == "UPPER" else 100.0,
        "upper": 103.0,
        "lower": 100.0,
        "channel_width_price": 3.0,
        "channel_width_pct": 3.0,
        "efficiency": 0.10,
        "overlap": 0.80,
        "minute_signal_pos": 0,
    }


class TestBreakoutPriorTestCountV1(unittest.TestCase):
    def classify(self, frame, signal_event, zone=0.10):
        return classify_events(
            frame, [signal_event], "BTC", "STRICT_P25", zone, 3.2
        )

    def test_counts_distinct_tests_and_confirmed_rejections(self):
        frame = joined([
            (102.0, 102.8, 101.8, 102.5),  # touch + confirmed rejection
            (102.2, 102.5, 101.9, 102.3),  # non-touch 20% separation
            (102.2, 102.8, 102.0, 102.9),  # second test, contact only
            (103.0, 103.3, 102.8, 103.2),  # breakout; excluded from count
        ])
        c, links = self.classify(frame, event(frame.index[-1]))
        row = c.iloc[0]
        self.assertEqual(row["prior_touch_test_count"], 2)
        self.assertEqual(row["prior_confirmed_rejection_count"], 1)
        self.assertEqual(row["prior_contact_only_test_count"], 1)
        self.assertEqual(row["prior_rejection_group"], "1")
        self.assertEqual(len(links), 2)
        self.assertEqual(
            set(links["test_status_at_breakout"]),
            {"confirmed_rejection", "contact_only"},
        )

    def test_breakout_candle_does_not_count_as_prior_touch(self):
        frame = joined([(102.0, 103.4, 101.8, 103.2)])
        c, links = self.classify(frame, event(frame.index[0]))
        self.assertEqual(c.iloc[0]["prior_touch_test_count"], 0)
        self.assertEqual(c.iloc[0]["prior_confirmed_rejection_count"], 0)
        self.assertTrue(links.empty)

    def test_timestamp_gap_resets_prior_test_state_before_event(self):
        start = pd.Timestamp("2025-01-01T00:00:00Z")
        frame = joined(
            [
                (102.0, 102.8, 101.8, 102.5),
                (103.0, 103.3, 102.8, 103.2),
            ],
            times=[start, start + 2 * STEP],
        )
        c, links = self.classify(frame, event(frame.index[-1]))
        self.assertEqual(c.iloc[0]["prior_touch_test_count"], 0)
        self.assertTrue(links.empty)

    def test_snapshot_change_resets_prior_test_state_before_event(self):
        start = pd.Timestamp("2025-01-01T00:00:00Z")
        snapshots = [
            start - pd.Timedelta(hours=4),
            start + STEP - pd.Timedelta(hours=4),
        ]
        frame = joined(
            [
                (102.0, 102.8, 101.8, 102.5),
                (103.0, 103.3, 102.8, 103.2),
            ],
            snapshots=snapshots,
        )
        c, links = self.classify(frame, event(frame.index[-1]))
        self.assertEqual(c.iloc[0]["prior_touch_test_count"], 0)
        self.assertTrue(links.empty)

    def test_lower_boundary_rejection_is_counted(self):
        frame = joined([
            (100.8, 101.2, 100.2, 100.5),  # lower touch + rejection
            (100.0, 100.2, 99.7, 99.8),    # lower breakout
        ])
        c, links = self.classify(frame, event(frame.index[-1], "LOWER"))
        self.assertEqual(c.iloc[0]["prior_touch_test_count"], 1)
        self.assertEqual(c.iloc[0]["prior_confirmed_rejection_count"], 1)
        self.assertEqual(c.iloc[0]["prior_rejection_group"], "1")
        self.assertEqual(len(links), 1)

    def test_separation_candle_arms_next_test_but_is_not_a_test(self):
        frame = joined([
            (102.0, 102.8, 101.8, 102.5),  # first test/rejection
            (102.2, 102.5, 101.9, 102.3),  # separation only
            (102.2, 102.8, 102.0, 102.9),  # second test
            (103.0, 103.3, 102.8, 103.2),  # breakout
        ])
        c, links = self.classify(frame, event(frame.index[-1]))
        self.assertEqual(
            list(links["test_start_time"]),
            [frame.index[0], frame.index[2]],
        )



    def test_group_summary_includes_zero_count_categories(self):
        sample = pd.DataFrame([{
            "asset": "BTC",
            "definition": "STRICT_P25",
            "direction": "UPPER",
            "zone_pct_of_channel": 10.0,
            "prior_rejection_group": "1",
        }])
        summary = group_summary(sample)
        counts = dict(zip(summary["prior_rejection_group"], summary["event_count"]))
        self.assertEqual(counts, {"0": 0, "1": 1, "2": 0, "3+": 0})


if __name__ == "__main__":
    unittest.main(verbosity=2)
