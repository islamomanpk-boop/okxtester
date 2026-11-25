import unittest

import numpy as np
import pandas as pd

from research.phase3_breakout_lifecycle_v1_1 import (
    assign_overlap_clusters,
    build_complete_15m,
    find_inside_retest,
    find_outside_retest,
    first_1m_return_inside,
    first_15m_failure_and_reclaim,
    _first_15m_close_after,
    compare_with_forward_archive,
    FORWARD_ARCHIVE_METRIC_PAIRS,
    FORWARD_ARCHIVE_UNAVAILABLE_FIELDS,
)


def bar(ts, o, h, low, close):
    return {"ts_ms": ts, "open": o, "high": h, "low": low, "close": close}


class BreakoutLifecycleTests(unittest.TestCase):
    def test_upper_outside_retest_uses_point_one_percent_of_boundary(self):
        result = find_outside_retest(
            "UPPER", 100.0, 100.2,
            [bar(0, 100.15, 100.2, 100.1, 100.12)],
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["elapsed_minutes"], 1)
        self.assertFalse(result["boundary_crossed"])
        self.assertAlmostEqual(result["depth_pct_of_boundary"], 0.0)

    def test_lower_outside_retest_is_symmetric(self):
        result = find_outside_retest(
            "LOWER", 90.0, 89.8,
            [bar(0, 89.85, 89.91, 89.8, 89.86)],
        )
        self.assertIsNotNone(result)
        self.assertFalse(result["boundary_crossed"])
        self.assertAlmostEqual(result["depth_pct_of_boundary"], 0.0)

    def test_exact_outer_band_equality_counts_as_retest(self):
        result = find_outside_retest(
            "UPPER", 100.0, 100.2,
            [bar(0, 100.15, 100.2, 100.1, 100.1)],
        )
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result["bar_low"], 100.1)

    def test_one_minute_return_inside_includes_boundary_equality(self):
        upper = first_1m_return_inside("UPPER", 100.0, [bar(0, 100.2, 100.3, 99.9, 100.0)])
        lower = first_1m_return_inside("LOWER", 90.0, [bar(0, 89.8, 90.1, 89.7, 90.0)])
        self.assertEqual(upper["available_ts_ms"], 60_000)
        self.assertEqual(lower["available_ts_ms"], 60_000)

    def test_retest_hold_requires_a_strictly_later_fifteen_minute_close(self):
        bars15 = pd.DataFrame(
            {"close": [100.2, 100.3]},
            index=pd.to_datetime([
                "2026-01-01T00:15:00Z",
                "2026-01-01T00:30:00Z",
            ]),
        )
        result = _first_15m_close_after(
            bars15, pd.Timestamp("2026-01-01T00:15:00Z")
        )
        self.assertEqual(result["close_ts_ms"], 1767227400000)
        self.assertAlmostEqual(result["close"], 100.3)

    def test_completed_fifteen_minute_failure_then_reclaim(self):
        rows = [(900_000, 100.2), (1_800_000, 99.9), (2_700_000, 100.1)]
        failure, reclaim = first_15m_failure_and_reclaim("UPPER", 100.0, rows)
        self.assertEqual(failure["close_ts_ms"], 1_800_000)
        self.assertEqual(reclaim["close_ts_ms"], 2_700_000)

    def test_lower_fifteen_minute_failure_then_reclaim(self):
        rows = [(900_000, 89.8), (1_800_000, 90.1), (2_700_000, 89.9)]
        failure, reclaim = first_15m_failure_and_reclaim("LOWER", 90.0, rows)
        self.assertEqual(failure["close_ts_ms"], 1_800_000)
        self.assertEqual(reclaim["close_ts_ms"], 2_700_000)

    def test_inside_retest_after_failure_moves_away_then_returns(self):
        bars = [
            bar(0, 99.8, 99.85, 99.7, 99.8),
            bar(60_000, 99.82, 99.95, 99.8, 99.92),
        ]
        result = find_inside_retest("UPPER", 100.0, 99.8, bars)
        self.assertEqual(result["status"], "RETEST_AFTER_MOVING_AWAY")
        self.assertFalse(result["initially_in_band"])
        self.assertEqual(result["bar_open_ts_ms"], 60_000)
        self.assertFalse(result["boundary_crossed"])

    def test_already_in_band_at_failure_is_not_immediately_called_a_retest(self):
        bars = [
            bar(0, 99.95, 99.98, 99.92, 99.94),
            bar(60_000, 99.94, 99.96, 99.9, 99.91),
        ]
        result = find_inside_retest("UPPER", 100.0, 99.95, bars)
        self.assertEqual(result["status"], "ALREADY_IN_BAND_AT_FAILURE_CONFIRMATION")
        self.assertTrue(result["initially_in_band"])
        self.assertNotIn("bar_open_ts_ms", result)

    def test_already_in_band_then_move_away_and_retest(self):
        bars = [
            bar(0, 99.95, 99.89, 99.8, 99.85),
            bar(60_000, 99.85, 99.95, 99.8, 99.92),
        ]
        result = find_inside_retest("UPPER", 100.0, 99.95, bars)
        self.assertEqual(result["status"], "RETEST_AFTER_MOVING_AWAY")
        self.assertTrue(result["initially_in_band"])
        self.assertEqual(result["bar_open_ts_ms"], 60_000)

    def test_same_bar_move_away_and_retest_is_ambiguous_upper(self):
        result = find_inside_retest(
            "UPPER", 100.0, 99.95,
            [bar(0, 99.95, 99.96, 99.8, 99.85)],
        )
        self.assertEqual(result["status"], "SAME_BAR_AMBIGUOUS")
        self.assertEqual(result["bar_open_ts_ms"], 0)
        self.assertTrue(result["initially_in_band"])

    def test_same_bar_move_away_and_retest_is_ambiguous_lower(self):
        result = find_inside_retest(
            "LOWER", 90.0, 90.05,
            [bar(0, 90.05, 90.2, 90.04, 90.15)],
        )
        self.assertEqual(result["status"], "SAME_BAR_AMBIGUOUS")
        self.assertEqual(result["bar_open_ts_ms"], 0)
        self.assertTrue(result["initially_in_band"])

    def test_lower_inside_retest_is_symmetric(self):
        bars = [
            bar(0, 90.2, 90.25, 90.15, 90.2),
            bar(60_000, 90.2, 90.25, 90.05, 90.08),
        ]
        result = find_inside_retest("LOWER", 90.0, 90.2, bars)
        self.assertEqual(result["status"], "RETEST_AFTER_MOVING_AWAY")
        self.assertEqual(result["bar_open_ts_ms"], 60_000)

    def test_only_complete_fifteen_minute_bars_are_retained(self):
        idx = pd.date_range("2026-01-01T00:00:00Z", periods=15, freq="min")
        frame = pd.DataFrame({
            "open": np.arange(15) + 100.0,
            "high": np.arange(15) + 101.0,
            "low": np.arange(15) + 99.0,
            "close": np.arange(15) + 100.5,
        }, index=idx)
        bars15 = build_complete_15m(frame)
        self.assertEqual(len(bars15), 1)
        self.assertEqual(bars15.index[0], pd.Timestamp("2026-01-01T00:15:00Z"))
        self.assertEqual(bars15.iloc[0]["open"], 100.0)
        self.assertEqual(bars15.iloc[0]["close"], 114.5)

    def test_missing_minute_does_not_create_complete_fifteen_minute_bar(self):
        idx = pd.date_range("2026-01-01T00:00:00Z", periods=15, freq="min").delete(7)
        frame = pd.DataFrame({
            "open": np.arange(len(idx)) + 100.0,
            "high": np.arange(len(idx)) + 101.0,
            "low": np.arange(len(idx)) + 99.0,
            "close": np.arange(len(idx)) + 100.5,
        }, index=idx)
        self.assertTrue(build_complete_15m(frame).empty)

    def test_forward_archive_crosscheck_uses_only_archived_fields(self):
        signal = pd.Timestamp("2025-01-01T00:00:00Z")
        signal_ms = int(signal.value // 1_000_000)
        row = {
            "event_id": "event-1", "asset": "BTC", "definition": "STRICT_P25",
            "direction": "UPPER", "entry_time_ms": signal_ms, "horizon": "15M",
            "directional_close_return_pct": 0.1, "mfe_pct": 0.2, "mae_pct": 0.3,
            "mfe_channel_width_pct": 4.0, "mae_channel_width_pct": 5.0,
            "favourable_extreme_price": 101.0, "adverse_extreme_price": 99.0,
            "time_to_mfe_minutes": 2, "time_to_mae_minutes": 3,
            "entry_open": 100.0, "entry_open_already_through_boundary": False,
            "horizon_status": "COMPLETE",
            "favourable_extreme_time_ms": signal_ms + 120_000,
            "adverse_extreme_time_ms": signal_ms + 180_000,
            "boundary_failure_time_ms": signal_ms + 60_000,
            "boundary_failure": True, "minutes_to_boundary_failure": 1,
            "outside_retest_hold": "",
        }
        reference = pd.DataFrame([{
            "asset": "BTC", "definition": "STRICT_P25", "direction": "UPPER",
            "signal_time": signal, "horizon": "15M", "entry_time": signal,
            "directional_close_return_pct": 0.1, "mfe_pct": 0.2, "mae_pct": 0.3,
            "mfe_channel_width_pct": 4.0, "mae_channel_width_pct": 5.0,
            "favourable_extreme_price": 101.0, "adverse_extreme_price": 99.0,
            "time_to_mfe_minutes": 2, "time_to_mae_minutes": 3,
            "entry_open": 100.0, "entry_open_already_through_boundary": False,
            "horizon_status": "COMPLETE",
            "favourable_extreme_time": signal + pd.Timedelta(minutes=2),
            "adverse_extreme_time": signal + pd.Timedelta(minutes=3),
            "boundary_failure_time": signal + pd.Timedelta(minutes=1),
            "boundary_failure": True, "minutes_to_boundary_failure": 1,
        }])
        result = compare_with_forward_archive([row], reference)
        self.assertTrue(result[0]["reference_match"])
        self.assertEqual(result[0]["reference_fields_checked"], len(FORWARD_ARCHIVE_METRIC_PAIRS))
        self.assertIn("outside_retest", FORWARD_ARCHIVE_UNAVAILABLE_FIELDS)
        self.assertIn("outside_retest_hold", FORWARD_ARCHIVE_UNAVAILABLE_FIELDS)

    def test_overlap_clusters_are_transitive_and_asset_scoped(self):
        rows = [
            {"event_id": "a", "asset": "BTC", "signal_time_ms": 0, "observed_bars_12h": 10},
            {"event_id": "b", "asset": "BTC", "signal_time_ms": 300_000, "observed_bars_12h": 10},
            {"event_id": "c", "asset": "BTC", "signal_time_ms": 800_000, "observed_bars_12h": 10},
            {"event_id": "d", "asset": "BTC", "signal_time_ms": 1_400_000, "observed_bars_12h": 5},
            {"event_id": "e", "asset": "ETH", "signal_time_ms": 0, "observed_bars_12h": 10},
        ]
        mapping, summary = assign_overlap_clusters(rows)
        self.assertEqual(mapping["a"]["overlap_cluster_id"], mapping["b"]["overlap_cluster_id"])
        self.assertEqual(mapping["b"]["overlap_cluster_id"], mapping["c"]["overlap_cluster_id"])
        self.assertNotEqual(mapping["c"]["overlap_cluster_id"], mapping["d"]["overlap_cluster_id"])
        self.assertNotEqual(mapping["a"]["overlap_cluster_id"], mapping["e"]["overlap_cluster_id"])
        self.assertEqual(mapping["a"]["overlap_cluster_size"], 3)
        self.assertEqual(summary["total"], 3)
        self.assertEqual(summary["largest_cluster_size"], 3)

    def test_touching_half_open_windows_do_not_overlap(self):
        rows = [
            {"event_id": "a", "asset": "BTC", "signal_time_ms": 0, "observed_bars_12h": 10},
            {"event_id": "b", "asset": "BTC", "signal_time_ms": 600_000, "observed_bars_12h": 10},
        ]
        mapping, summary = assign_overlap_clusters(rows)
        self.assertNotEqual(mapping["a"]["overlap_cluster_id"], mapping["b"]["overlap_cluster_id"])
        self.assertEqual(summary["total"], 2)


if __name__ == "__main__":
    unittest.main()
