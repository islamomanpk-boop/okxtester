import unittest

from portfolio_backtester import (
    PortfolioBacktestConfig,
    run_portfolio_backtest as _run_portfolio_backtest,
)

BASE_TS = 1_000_000


def make_bars(rows):
    return [
        {
            "ts": BASE_TS + i * 60_000,
            "open": r[0],
            "high": r[1],
            "low": r[2],
            "close": r[3],
        }
        for i, r in enumerate(rows)
    ]


def candidate(side=1, stop=99, target_pct=0.05, mode="none"):
    return {
        "asset": "BTC",
        "side": side,
        "signal_available_at": BASE_TS + 60_000,
        "signal_priority": 1,
        "stop_price": stop,
        "stop_distance_atr": 1.0,
        "target_pct": target_pct,
        "signal_type": "trailing_test",
        "trailing_mode": mode,
        "trailing_activation_r": 1.0,
        "trailing_distance_r": (
            0.5 if mode == "trailing_take_profit" else 1.0
        ),
        "trailing_activation_at_target": (
            mode == "trailing_take_profit"
        ),
    }


def config():
    return PortfolioBacktestConfig(
        initial_equity=1000,
        taker_fee_rate=0,
        slippage_bps=0,
    )


def funding_contract_for_test(bars, events=None):
    events = list(events or [])
    first_ts = int(bars[0]["ts"])
    last_ts = int(bars[-1]["ts"])
    interval = 28_800_000
    schedule_start = int(events[0]["funding_time"]) if events else last_ts + interval
    schedule_end = int(events[-1]["funding_time"]) if events else schedule_start
    exact = bool(events) and all(event.get("mark_price") is not None for event in events)
    return {
        "events": events,
        "coverage": {
            "instrument_name": "BTC-USDT-SWAP",
            "source_sha256": "a" * 64,
            "coverage_start_ms": first_ts - 1,
            "coverage_end_ms": last_ts,
            "schedule_id": "test_schedule_v1",
            "schedule_start_ms": schedule_start,
            "schedule_interval_ms": interval,
            "schedule_end_ms": schedule_end,
            "event_window_start_ms": first_ts - 1,
            "event_window_end_ms": last_ts,
            "mark_price_mode": "exact" if exact else "candle_close_proxy",
        },
    }


def run_portfolio_backtest(bars_by_asset, candidates, funding_by_asset, config):
    contracts = {
        asset: funding_contract_for_test(bars, funding_by_asset[asset])
        for asset, bars in bars_by_asset.items()
        if asset in funding_by_asset
    }
    return _run_portfolio_backtest(
        bars_by_asset, candidates, contracts, config
    )


class TrailingPortfolioTests(unittest.TestCase):

    def run_trade(self, rows, c):
        return run_portfolio_backtest(
            {"BTC": make_bars(rows)},
            [c],
            {"BTC": []},
            config(),
        )["trades"][0]

    def test_long_trailing_stop_activates_on_next_candle(self):
        trade = self.run_trade([
            (100, 100.2, 99.8, 100),
            (100, 101.5, 99.8, 101),
            (100.4, 100.8, 100.2, 100.5),
        ], candidate(mode="trailing_stop_loss"))

        self.assertEqual(trade["exit_reason"], "stop_gap")
        self.assertAlmostEqual(trade["exit_price"], 100.4)
        self.assertTrue(trade["trailing_sl_active"])
        self.assertEqual(trade["trailing_sl_activation_time"], BASE_TS + 60_000)
        self.assertGreater(trade["trailing_sl_update_count"], 0)
        self.assertAlmostEqual(trade["initial_stop_price"], 99.0)
        self.assertGreater(trade["stop_price"], trade["initial_stop_price"])

    def test_short_trailing_stop_activates_on_next_candle(self):
        trade = self.run_trade([
            (100, 100.2, 99.8, 100),
            (100, 100.2, 98.5, 99),
            (99.6, 99.8, 99.4, 99.5),
        ], candidate(
            side=-1,
            stop=101,
            mode="trailing_stop_loss",
        ))

        self.assertEqual(trade["exit_reason"], "stop_gap")
        self.assertAlmostEqual(trade["exit_price"], 99.6)
        self.assertTrue(trade["trailing_sl_active"])
        self.assertEqual(trade["trailing_sl_activation_time"], BASE_TS + 60_000)
        self.assertGreater(trade["trailing_sl_update_count"], 0)
        self.assertLess(trade["stop_price"], trade["initial_stop_price"])

    def test_long_trailing_take_profit(self):
        trade = self.run_trade([
            (100, 100.2, 99.8, 100),
            (100, 102.5, 99.8, 102),
            (102.1, 102.3, 101.9, 102),
        ], candidate(
            target_pct=0.02,
            mode="trailing_take_profit",
        ))

        self.assertEqual(trade["exit_reason"], "trailing_take_profit")
        self.assertAlmostEqual(trade["exit_price"], 102.0)
        self.assertTrue(trade["trailing_tp_active"])
        self.assertEqual(trade["trailing_tp_activation_time"], BASE_TS + 60_000)
        self.assertGreater(trade["trailing_tp_update_count"], 0)
        self.assertGreater(trade["max_favorable_excursion_r"], 0)

    def test_short_trailing_take_profit(self):
        trade = self.run_trade([
            (100, 100.2, 99.8, 100),
            (100, 100.2, 97.5, 98),
            (97.9, 98.1, 97.7, 98),
        ], candidate(
            side=-1,
            stop=101,
            target_pct=0.02,
            mode="trailing_take_profit",
        ))

        self.assertEqual(trade["exit_reason"], "trailing_take_profit")
        self.assertAlmostEqual(trade["exit_price"], 98.0)
        self.assertTrue(trade["trailing_tp_active"])
        self.assertEqual(trade["trailing_tp_activation_time"], BASE_TS + 60_000)
        self.assertGreater(trade["trailing_tp_update_count"], 0)

    def test_protective_stop_wins_on_trailing_tp_activation_candle(self):
        trade = self.run_trade([
            (100, 100.2, 99.8, 100),
            (100, 102.5, 98.5, 101),
        ], candidate(
            target_pct=0.02,
            mode="trailing_take_profit",
        ))

        self.assertEqual(trade["exit_reason"], "stop")
        self.assertAlmostEqual(trade["exit_price"], 99.0)


if __name__ == "__main__":
    unittest.main()
