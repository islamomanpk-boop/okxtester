import unittest
from audit_stop_gap_risk import analyze_bars

def bar(ts, o, h, low, close):
    return {"ts": ts, "open": o, "high": h, "low": low, "close": close, "vol": 1.0}

class StopGapRiskAuditTests(unittest.TestCase):
    def test_long_gap_loss_multiple_and_overshoot(self):
        result = analyze_bars([bar(60000,100,100.2,99.8,100),bar(120000,98.5,99,98,98.7)],[1.0])
        item = next(x for x in result["scenarios"] if x["side"] == "LONG")
        self.assertEqual(item["gap_events"],1)
        self.assertAlmostEqual(item["gap_loss_multiple"]["p50"],1.5)
        self.assertAlmostEqual(item["stop_overshoot_bps"]["p50"],(99-98.5)/99*10000)
        self.assertEqual(item["eligible_minute_transitions"],1)
    def test_short_gap_loss_multiple(self):
        result = analyze_bars([bar(60000,100,100.2,99.8,100),bar(120000,101.5,102,101,101.8)],[1.0])
        item = next(x for x in result["scenarios"] if x["side"] == "SHORT")
        self.assertEqual(item["gap_events"],1)
        self.assertAlmostEqual(item["gap_loss_multiple"]["p50"],1.5)
    def test_exact_stop_open_is_counted_as_gap(self):
        result = analyze_bars([bar(60000,100,100.2,99.8,100),bar(120000,99,99.2,98.8,99)],[1.0])
        item = next(x for x in result["scenarios"] if x["side"] == "LONG")
        self.assertEqual(item["gap_events"],1)
        self.assertAlmostEqual(item["gap_loss_multiple"]["p50"],1.0)
        self.assertAlmostEqual(item["stop_overshoot_bps"]["p50"],0.0)
    def test_nonconsecutive_transition_is_skipped_not_counted_as_market_gap(self):
        result = analyze_bars([bar(60000,100,100.2,99.8,100),bar(180000,90,91,89,90),bar(240000,90,90.2,89.8,90)],[1.0])
        self.assertEqual(result["eligible_minute_transitions"],1)
        self.assertEqual(result["skipped_nonconsecutive_transitions"],1)
        self.assertEqual(next(x for x in result["scenarios"] if x["side"]=="LONG")["gap_events"],0)
    def test_duplicate_timestamps_rejected(self):
        with self.assertRaisesRegex(ValueError,"strictly increasing"):
            analyze_bars([bar(60000,100,100.2,99.8,100),bar(60000,99,99.2,98.8,99)],[1.0])
    def test_invalid_ohlc_rejected(self):
        with self.assertRaisesRegex(ValueError,"Inconsistent high"):
            analyze_bars([bar(60000,100,99,99.8,100),bar(120000,100,100.2,99.8,100)],[1.0])
    def test_invalid_stop_distance_rejected(self):
        with self.assertRaisesRegex(ValueError,"Stop distances"):
            analyze_bars([bar(60000,100,100.2,99.8,100),bar(120000,100,100.2,99.8,100)],[0,100])

    def test_open_jump_distribution_includes_adverse_direction_and_max(self):
        result = analyze_bars([
            bar(60000, 100, 100.2, 99.8, 100),
            bar(120000, 99.8, 100, 99.7, 100.0),
            bar(180000, 100.1, 100.2, 100, 100.15),
        ], [0.2])
        jumps = result["open_jump_distributions_bps"]
        self.assertAlmostEqual(jumps["absolute_open_jump"]["max"], 20.0)
        self.assertAlmostEqual(jumps["long_adverse_open_jump"]["max"], 20.0)
        self.assertAlmostEqual(jumps["short_adverse_open_jump"]["max"], 10.0)
        self.assertEqual(result["first_utc"], "1970-01-01T00:01:00+00:00")

    def test_zero_volume_rows_are_bridged_to_next_traded_open(self):
        rows = [
            bar(60000, 100, 100.2, 99.8, 100),
            {**bar(120000, 100, 100, 100, 100), "vol": 0.0},
            bar(180000, 99.5, 99.7, 99.4, 99.6),
        ]
        result = analyze_bars(rows, [0.25])
        self.assertEqual(result["zero_volume_rows"], 1)
        self.assertEqual(result["positive_volume_rows"], 2)
        self.assertEqual(result["active_trade_transitions"], 1)
        self.assertEqual(result["active_trade_open_jump_distributions_bps"]["elapsed_minutes_between_active_bars"]["max"], 2.0)
        item = next(x for x in result["scenarios"] if x["side"] == "LONG")
        self.assertEqual(item["gap_events"], 1)
        self.assertEqual(item["eligible_active_trade_transitions"], 1)

    def test_negative_volume_is_rejected(self):
        rows = [bar(60000, 100, 100.2, 99.8, 100), {**bar(120000, 100, 100.2, 99.8, 100), "vol": -1.0}]
        with self.assertRaisesRegex(ValueError, "volume"):
            analyze_bars(rows, [1.0])

if __name__ == "__main__":
    unittest.main()
