import unittest

from execution_engine import (
    ExecutionConfig,
    find_next_entry_index,
    simulate_trade as _simulate_trade,
    size_position,
)


def config():
    return ExecutionConfig(
        risk_fraction=0.005,
        max_gross_leverage=1.0,
        taker_fee_rate=0.0005,
        slippage_bps=2,
    )


def bar(ts, o, h, l, c):
    return {
        "ts": ts,
        "open": o,
        "high": h,
        "low": l,
        "close": c,
    }


def funding_contract_for_test(bars, events=None):
    events = list(events or [])
    first_bar = int(bars[0]["ts"])
    last_bar = int(bars[-1]["ts"])
    interval = 28_800_000
    schedule_start = (
        int(events[0]["funding_time"])
        if events else last_bar + interval
    )
    schedule_end = (
        int(events[-1]["funding_time"])
        if events else schedule_start
    )
    return {
        "events": events,
        "coverage": {
            "instrument_name": "BTC-USDT-SWAP",
            "source_sha256": "a" * 64,
            "coverage_start_ms": 0,
            "coverage_end_ms": last_bar,
            "schedule_id": "test_schedule_v1",
            "schedule_start_ms": schedule_start,
            "schedule_interval_ms": interval,
            "schedule_end_ms": schedule_end,
            "event_window_start_ms": 0,
            "event_window_end_ms": last_bar,
            "mark_price_mode": "candle_close_proxy",
        },
    }


def simulate_trade(bars, entry_index, side, stop_price, target_price,
                   equity, execution_config, funding_events=None):
    return _simulate_trade(
        bars, entry_index, side, stop_price, target_price, equity,
        execution_config,
        funding_contract=funding_contract_for_test(bars, funding_events),
    )


class ExecutionEngineTests(unittest.TestCase):
    def test_next_eligible_minute(self):
        bars = [
            bar(60000, 100, 101, 99, 100),
            bar(120000, 100, 101, 99, 100),
            bar(180000, 100, 101, 99, 100),
        ]
        self.assertEqual(find_next_entry_index(bars, 120000), 1)
        self.assertEqual(find_next_entry_index(bars, 150000), 2)
        self.assertIsNone(find_next_entry_index(bars, 240000))

    def test_missing_execution_minute_rejected(self):
        bars = [
            bar(60000, 100, 101, 99, 100),
            bar(180000, 100, 101, 99, 100),
        ]
        with self.assertRaisesRegex(ValueError, "exactly 1 minute"):
            simulate_trade(
                bars, 0, 1, 90, 110, 1000, config()
            )

    def test_position_risk_and_exposure_cap(self):
        result = size_position(1000, 100, 99, 1, config())
        self.assertAlmostEqual(result["risk_budget"], 5)
        self.assertLessEqual(result["gross_exposure"], 1000.01)
        self.assertLessEqual(
            result["planned_cost_adjusted_risk"],
            result["risk_budget"] + 1e-10,
        )

    def test_standalone_sizing_reserves_entry_exit_fees_and_slippage(self):
        no_costs = ExecutionConfig(
            risk_fraction=0.005,
            max_gross_leverage=1.0,
            taker_fee_rate=0.0,
            slippage_bps=0.0,
        )
        with_costs = config()
        baseline = size_position(1000, 100, 99, 1, no_costs)
        adjusted = size_position(1000, 100, 99, 1, with_costs)
        self.assertLess(adjusted["quantity"], baseline["quantity"])
        expected_stop_fill = 99 * (1 - 2 / 10000)
        expected_risk_per_unit = (
            abs(100 - expected_stop_fill)
            + 0.0005 * (100 + expected_stop_fill)
        )
        self.assertAlmostEqual(
            adjusted["risk_per_unit"], expected_risk_per_unit
        )
        self.assertAlmostEqual(
            adjusted["planned_cost_adjusted_risk"],
            adjusted["quantity"] * expected_risk_per_unit,
        )

    def test_cost_adjusted_sizing_supports_short_stop_slippage(self):
        result = size_position(1000, 100, 101, -1, config())
        expected_stop_fill = 101 * (1 + 2 / 10000)
        expected = (
            abs(100 - expected_stop_fill)
            + 0.0005 * (100 + expected_stop_fill)
        )
        self.assertAlmostEqual(result["risk_per_unit"], expected)
        self.assertLessEqual(
            result["planned_cost_adjusted_risk"],
            result["risk_budget"] + 1e-10,
        )

    def test_long_stop_execution(self):
        bars = [
            bar(60000, 100, 100.5, 99.5, 100),
            bar(120000, 100, 100.2, 98.5, 99),
        ]
        result = simulate_trade(
            bars, 0, 1, 99, 102, 1000, config()
        )
        self.assertEqual(result["exit_reason"], "stop")
        self.assertLess(result["net_pnl"], 0)

    def test_short_target_execution(self):
        bars = [
            bar(60000, 100, 100.5, 99.5, 100),
            bar(120000, 100, 100.2, 97.5, 99),
        ]
        result = simulate_trade(
            bars, 0, -1, 101, 98, 1000, config()
        )
        self.assertEqual(result["exit_reason"], "target")
        self.assertGreater(result["gross_pnl"], 0)

    def test_stop_wins_when_both_hit(self):
        bars = [
            bar(60000, 100, 100.5, 99.5, 100),
            bar(120000, 100, 103, 98, 100),
        ]
        result = simulate_trade(
            bars, 0, 1, 99, 102, 1000, config()
        )
        self.assertEqual(result["exit_reason"], "stop")

    def test_gap_through_long_stop(self):
        bars = [
            bar(60000, 100, 100.5, 99.5, 100),
            bar(120000, 97, 98, 96, 97),
        ]
        result = simulate_trade(
            bars, 0, 1, 99, 102, 1000, config()
        )
        self.assertEqual(result["exit_reason"], "stop_gap")
        self.assertLess(result["exit_price"], 97)

    def test_funding_long_pays_positive_rate(self):
        bars = [
            bar(60000, 100, 100.5, 99.5, 100),
            bar(120000, 100, 100.5, 99.5, 100),
            bar(180000, 100, 100.5, 99.5, 100),
        ]
        result = simulate_trade(
            bars, 0, 1, 90, 110, 1000, config(),
            funding_events=[
                {"funding_time": 120000, "funding_rate": 0.001}
            ],
        )
        self.assertLess(result["funding_pnl"], 0)
        expected = (
            -result["quantity"] * 100.0 * 0.001
        )
        self.assertAlmostEqual(result["funding_pnl"], expected)

    def test_funding_short_receives_positive_rate(self):
        bars = [
            bar(60000, 100, 100.5, 99.5, 100),
            bar(120000, 100, 100.5, 99.5, 100),
            bar(180000, 100, 100.5, 99.5, 100),
        ]
        result = simulate_trade(
            bars, 0, -1, 110, 90, 1000, config(),
            funding_events=[
                {"funding_time": 120000, "funding_rate": 0.001}
            ],
        )
        self.assertGreater(result["funding_pnl"], 0)

    def test_funding_before_entry_not_charged(self):
        bars = [
            bar(60000, 100, 100.5, 99.5, 100),
            bar(120000, 100, 100.5, 99.5, 100),
        ]
        result = simulate_trade(
            bars, 0, 1, 90, 110, 1000, config(),
            funding_events=[
                {"funding_time": 60000, "funding_rate": 0.001}
            ],
        )
        self.assertEqual(result["funding_pnl"], 0)

    def test_omitted_funding_contract_is_rejected(self):
        bars = [bar(60000, 100, 100.5, 99.5, 100)]
        with self.assertRaises(TypeError):
            _simulate_trade(bars, 0, 1, 90, 110, 1000, config())

    def test_trade_outside_funding_coverage_is_rejected(self):
        bars = [
            bar(60000, 100, 100.5, 99.5, 100),
            bar(120000, 100, 100.5, 99.5, 100),
            bar(180000, 100, 100.5, 99.5, 100),
        ]
        contract = funding_contract_for_test(bars)
        contract["coverage"]["coverage_end_ms"] = 120000
        contract["coverage"]["event_window_end_ms"] = 120000
        with self.assertRaisesRegex(ValueError, "exceeds verified funding coverage"):
            _simulate_trade(
                bars, 0, 1, 90, 110, 1000, config(),
                funding_contract=contract,
            )

    def test_fee_and_slippage_are_recorded(self):
        bars = [bar(60000, 100, 100.5, 99.5, 100)]
        result = simulate_trade(
            bars, 0, 1, 90, 110, 1000, config()
        )
        self.assertGreater(result["total_fees"], 0)
        self.assertGreater(result["entry_price"], 100)

    def test_missing_cost_assumptions_rejected(self):
        bad = ExecutionConfig()
        with self.assertRaises(ValueError):
            simulate_trade(
                [bar(60000, 100, 101, 99, 100)],
                0, 1, 90, 110, 1000, bad
            )


if __name__ == "__main__":
    unittest.main()
