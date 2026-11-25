import unittest

from research.phase3_rejection_lifecycle_v1 import analyze_event_path


def event(direction="upper"):
    return {
        "event_id": "TEST|broad|upper|0|1|1|0",
        "asset": "BTC",
        "definition": "broad",
        "direction": direction,
        "test_rank_group": "1",
        "confirmation_ts_ms": 0,
        "upper": 100.0,
        "lower": 90.0,
        "channel_width": 10.0,
        "rejection_close": 99.5 if direction == "upper" else 90.5,
    }


def bar(ts, o, h, low, close):
    return {"ts": ts, "open": o, "high": h, "low": low, "close": close}


class RejectionLifecycleTests(unittest.TestCase):
    def test_upper_retest_then_inward_separation(self):
        bars = [
            bar(0, 98.5, 98.8, 98.0, 98.4),
            bar(60_000, 98.7, 99.2, 98.1, 98.5),
            bar(120_000, 98.0, 98.8, 97.0, 97.8),
        ]
        result, episodes, horizons = analyze_event_path(event(), bars)
        self.assertEqual(result["first_retest_ts_ms"], 60_000)
        self.assertEqual(result["first_inward_separation_ts_ms"], 120_000)
        self.assertEqual(result["retest_episode_count"], 1)
        self.assertEqual(episodes[0]["resolution"], "INWARD_SEPARATION")
        self.assertFalse(episodes[0]["same_bar_ambiguous"])
        self.assertEqual(len(horizons), 4)
        self.assertFalse(horizons[0]["complete"])

    def test_distinct_retest_requires_separation_then_reentry(self):
        bars = [
            bar(0, 98.5, 98.8, 98.0, 98.4),
            bar(60_000, 98.7, 99.2, 98.1, 98.5),
            bar(120_000, 98.0, 98.8, 97.0, 97.8),
            bar(180_000, 98.8, 99.2, 98.1, 99.0),
            bar(240_000, 98.0, 98.8, 97.0, 97.7),
        ]
        result, episodes, _ = analyze_event_path(event(), bars)
        self.assertEqual(result["retest_episode_count"], 2)
        self.assertEqual([x["episode_index"] for x in episodes], [1, 2])
        self.assertEqual(episodes[1]["start_ts_ms"], 180_000)

    def test_same_bar_retest_and_separation_is_ambiguous(self):
        bars = [bar(0, 99.0, 99.6, 97.0, 97.8)]
        _, episodes, _ = analyze_event_path(event(), bars)
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["resolution"], "INWARD_SEPARATION")
        self.assertTrue(episodes[0]["same_bar_ambiguous"])

    def test_same_bar_retest_and_close_through_is_ambiguous_failure(self):
        bars = [
            bar(0, 99.8, 100.5, 99.0, 100.2),
            bar(60_000, 100.2, 100.4, 99.7, 99.8),
        ]
        result, episodes, _ = analyze_event_path(event(), bars)
        self.assertEqual(episodes[0]["resolution"], "CLOSE_THROUGH_BOUNDARY")
        self.assertTrue(episodes[0]["same_bar_ambiguous"])
        self.assertEqual(result["first_close_through_ts_ms"], 0)
        self.assertEqual(result["first_reclaim_ts_ms"], 60_000)
        self.assertEqual(result["inside_to_outside_close_cross_count"], 1)
        self.assertEqual(result["outside_to_inside_close_cross_count"], 1)
        self.assertEqual(result["retest_episode_count"], 1)

    def test_lower_boundary_symmetry(self):
        bars = [bar(0, 91.2, 92.5, 90.8, 92.2)]
        _, episodes, _ = analyze_event_path(event("lower"), bars)
        self.assertEqual(episodes[0]["resolution"], "INWARD_SEPARATION")
        self.assertTrue(episodes[0]["same_bar_ambiguous"])


    def test_exact_boundary_close_is_not_close_through(self):
        bars = [bar(0, 99.5, 100.0, 99.0, 100.0)]
        result, episodes, _ = analyze_event_path(event(), bars)
        self.assertIsNone(result["first_close_through_ts_ms"])
        self.assertEqual(result["inside_to_outside_close_cross_count"], 0)
        self.assertEqual(result["retest_episode_count"], 1)

    def test_source_end_censors_incomplete_horizons(self):
        bars = [
            bar(0, 98.5, 98.8, 98.0, 98.4),
            bar(60_000, 98.4, 98.7, 97.9, 98.3),
        ]
        result, _, horizons = analyze_event_path(event(), bars)
        self.assertEqual(result["status"], "CENSORED_SOURCE_END")
        self.assertEqual(result["censor_reason"], "SOURCE_END")
        self.assertEqual([x["complete"] for x in horizons], [False, False, False, False])

    def test_gap_is_not_bridged(self):
        bars = [
            bar(0, 98.5, 98.8, 98.0, 98.4),
            bar(60_000, 98.4, 98.7, 97.9, 98.3),
        ]
        result, _, _ = analyze_event_path(event(), bars, gap_after=True)
        self.assertEqual(result["status"], "CENSORED_GAP")
        self.assertEqual(result["censor_reason"], "GAP")

    def test_confirmation_timestamp_must_be_first_bar(self):
        bars = [bar(60_000, 98.5, 98.8, 98.0, 98.4)]
        with self.assertRaisesRegex(ValueError, "exactly at confirmation"):
            analyze_event_path(event(), bars)

    def test_gap_inside_supplied_window_is_rejected(self):
        bars = [
            bar(0, 98.5, 98.8, 98.0, 98.4),
            bar(120_000, 98.4, 98.7, 97.9, 98.3),
        ]
        with self.assertRaisesRegex(ValueError, "consecutive"):
            analyze_event_path(event(), bars)


if __name__ == "__main__":
    unittest.main()
