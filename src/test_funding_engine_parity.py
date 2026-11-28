import unittest

from execution_engine import ExecutionConfig, simulate_trade
from portfolio_backtester import PortfolioBacktestConfig, run_portfolio_backtest


BASE = 1_700_000_000_000
INTERVAL = 120_000


def bars():
    return [
        {"ts": BASE, "open": 100.0, "high": 100.2, "low": 99.8, "close": 100.0},
        {"ts": BASE + 60_000, "open": 100.0, "high": 100.2, "low": 99.8, "close": 100.0},
        {"ts": BASE + INTERVAL, "open": 100.0, "high": 101.2, "low": 99.8, "close": 100.5},
    ]


def contract(mode):
    events = [
        {"funding_time": BASE, "funding_rate": 0.0005},
        {"funding_time": BASE + INTERVAL, "funding_rate": 0.001},
    ]
    if mode == "exact":
        events[0]["mark_price"] = 100.0
        events[1]["mark_price"] = 100.25
    return {
        "events": events,
        "coverage": {
            "instrument_name": "BTC-USDT-SWAP",
            "source_sha256": "a" * 64,
            "coverage_start_ms": BASE,
            "coverage_end_ms": BASE + INTERVAL,
            "schedule_id": "synthetic_parity_schedule_v1",
            "schedule_start_ms": BASE,
            "schedule_interval_ms": INTERVAL,
            "schedule_end_ms": BASE + INTERVAL,
            "event_window_start_ms": BASE,
            "event_window_end_ms": BASE + INTERVAL,
            "mark_price_mode": mode,
        },
    }


def standalone_config():
    return ExecutionConfig(
        risk_fraction=0.005,
        max_gross_leverage=1.0,
        taker_fee_rate=0.0,
        slippage_bps=0.0,
    )


def portfolio_config():
    return PortfolioBacktestConfig(
        initial_equity=1000.0,
        risk_fraction=0.005,
        max_gross_leverage=1.0,
        taker_fee_rate=0.0,
        slippage_bps=0.0,
        record_equity_curve=False,
    )


def portfolio_candidate():
    return {
        "asset": "BTC",
        "side": 1,
        "signal_available_at": BASE,
        "signal_priority": 1,
        "stop_price": 99.0,
        "stop_distance_atr": 1.0,
        "target_pct": 0.01,
        "signal_type": "synthetic_funding_parity",
    }


class FundingEngineParityTests(unittest.TestCase):
    def assert_engine_parity(self, mode):
        source_bars = bars()
        funding_contract = contract(mode)
        single = simulate_trade(
            source_bars,
            entry_index=0,
            side=1,
            stop_price=99.0,
            target_price=101.0,
            equity=1000.0,
            config=standalone_config(),
            funding_contract=funding_contract,
        )
        portfolio = run_portfolio_backtest(
            {"BTC": source_bars},
            [portfolio_candidate()],
            {"BTC": funding_contract},
            portfolio_config(),
        )
        self.assertEqual(portfolio["trade_count"], 1)
        portfolio_trade = portfolio["trades"][0]

        self.assertAlmostEqual(single["funding_pnl"], portfolio_trade["funding_pnl"], places=12)
        self.assertAlmostEqual(single["quantity"], portfolio_trade["quantity"], places=12)
        self.assertEqual(single["funding_settlements_applied"], 1)
        self.assertEqual(portfolio_trade["funding_settlements_applied"], 1)
        self.assertEqual(single["entry_time"], portfolio_trade["entry_time"])
        self.assertEqual(single["exit_time"], portfolio_trade["exit_time"])
        self.assertEqual(single["funding_mark_price_mode"], mode)
        self.assertEqual(portfolio_trade["funding_mark_price_mode"], mode)

        # The settlement at entry time is excluded; the settlement at exit time is included.
        expected_mark = 100.25 if mode == "exact" else 100.5
        expected_funding = -single["quantity"] * expected_mark * 0.001
        self.assertAlmostEqual(single["funding_pnl"], expected_funding, places=12)

    def test_exact_mark_funding_arithmetic_matches_between_engines(self):
        self.assert_engine_parity("exact")

    def test_explicit_candle_close_proxy_funding_matches_between_engines(self):
        self.assert_engine_parity("candle_close_proxy")


if __name__ == "__main__":
    unittest.main()
