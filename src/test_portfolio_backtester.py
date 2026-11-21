import unittest

from portfolio_backtester import (
    PortfolioBacktestConfig,
    run_portfolio_backtest,
)


BASE_TS = 1_000_000


def make_bars(rows):
    return [
        {
            "ts": BASE_TS + i * 60_000,
            "open": row[0],
            "high": row[1],
            "low": row[2],
            "close": row[3],
        }
        for i, row in enumerate(rows)
    ]


def candidate(
    asset="BTC",
    side=1,
    available=BASE_TS + 60_000,
    stop=99,
    priority=1,
    target_pct=0.01,
):
    return {
        "asset": asset,
        "side": side,
        "signal_available_at": available,
        "signal_priority": priority,
        "stop_price": stop,
        "stop_distance_atr": 1.0,
        "target_pct": target_pct,
        "signal_type": "test",
    }


def config(fee=0.0, slippage=0.0):
    return PortfolioBacktestConfig(
        initial_equity=1000,
        taker_fee_rate=fee,
        slippage_bps=slippage,
    )


class PortfolioBacktesterTests(unittest.TestCase):
    def test_market_entry_and_target_exit(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 100.5, 99.8, 100.2),
                (100.2, 102, 100.1, 101.5),
                (101.5, 101.7, 101.2, 101.4),
            ])
        }
        result = run_portfolio_backtest(
            bars, [candidate()], {"BTC": []}, config()
        )
        self.assertEqual(result["trade_count"], 1)
        trade = result["trades"][0]
        self.assertEqual(trade["exit_reason"], "target")
        self.assertEqual(trade["entry_time"], BASE_TS + 60_000)
        self.assertAlmostEqual(trade["exit_price"], 101.0)

    def test_stop_wins_when_stop_and_target_hit_same_minute(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 102, 98, 100),
                (100, 100.2, 99.8, 100),
            ])
        }
        result = run_portfolio_backtest(
            bars, [candidate()], {"BTC": []}, config()
        )
        self.assertEqual(result["trades"][0]["exit_reason"], "stop")

    def test_simultaneous_assets_share_one_exposure_cap(self):
        rows = [
            (100, 100.2, 99.8, 100),
            (100, 100.5, 99.8, 100),
            (100, 100.5, 99.8, 100),
        ]
        bars = {"BTC": make_bars(rows), "ETH": make_bars(rows)}
        result = run_portfolio_backtest(
            bars,
            [
                candidate("BTC", priority=3),
                candidate("ETH", priority=2),
            ],
            {"BTC": [], "ETH": []},
            config(),
        )
        accepted = result["decisions"][0]["accepted"]
        self.assertEqual(len(accepted), 2)
        self.assertLessEqual(
            sum(p["gross_exposure"] for p in accepted),
            1000.0 + 1e-8,
        )

    def test_priority_controls_limited_shared_exposure(self):
        rows = [
            (100, 100.2, 99.8, 100),
            (100, 100.5, 99.8, 100),
            (100, 100.5, 99.8, 100),
        ]
        bars = {
            asset: make_bars(rows)
            for asset in ("BTC", "ETH", "SOL")
        }
        result = run_portfolio_backtest(
            bars,
            [
                candidate("BTC", priority=1),
                candidate("ETH", priority=2),
                candidate("SOL", priority=3),
            ],
            {"BTC": [], "ETH": [], "SOL": []},
            config(),
        )
        accepted = result["decisions"][0]["accepted"]
        self.assertEqual([p["asset"] for p in accepted], ["SOL", "ETH"])

    def test_signal_uses_first_minute_at_or_after_availability(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
            ])
        }
        c = candidate(available=BASE_TS + 90_000)
        result = run_portfolio_backtest(
            bars, [c], {"BTC": []}, config()
        )
        self.assertEqual(
            result["trades"][0]["entry_time"],
            BASE_TS + 120_000,
        )

    def test_long_pays_positive_funding(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
            ])
        }
        funding = {
            "BTC": [{
                "funding_time": BASE_TS + 120_000,
                "funding_rate": 0.001,
                "mark_price": 100,
            }]
        }
        result = run_portfolio_backtest(
            bars, [candidate()], funding, config()
        )
        self.assertLess(result["total_funding_pnl"], 0)

    def test_short_receives_positive_funding(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
            ])
        }
        funding = {
            "BTC": [{
                "funding_time": BASE_TS + 120_000,
                "funding_rate": 0.001,
                "mark_price": 100,
            }]
        }
        result = run_portfolio_backtest(
            bars,
            [candidate(side=-1, stop=101)],
            funding,
            config(),
        )
        self.assertGreater(result["total_funding_pnl"], 0)

    def test_entry_and_exit_fees_are_counted(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 100.5, 99.8, 100.2),
                (100.2, 102, 100.1, 101.5),
            ])
        }
        result = run_portfolio_backtest(
            bars, [candidate()], {"BTC": []}, config(fee=0.001)
        )
        self.assertGreater(result["total_fees"], 0)
        self.assertAlmostEqual(
            result["total_fees"],
            result["trades"][0]["total_fees"],
        )

    def test_slippage_is_applied_to_entry_and_exit(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 100.5, 99.8, 100.2),
                (100.2, 102, 100.1, 101.5),
            ])
        }
        result = run_portfolio_backtest(
            bars, [candidate()], {"BTC": []}, config(slippage=10)
        )
        self.assertGreater(result["trades"][0]["entry_price"], 100)
        self.assertLess(result["trades"][0]["exit_price"], 101)

    def test_missing_funding_asset_is_rejected(self):
        bars = {"BTC": make_bars([(100, 100.2, 99.8, 100)] * 2)}
        with self.assertRaisesRegex(ValueError, "Funding data key missing"):
            run_portfolio_backtest(bars, [], {}, config())

    def test_unsynchronized_asset_timestamps_are_rejected(self):
        bars = {
            "BTC": make_bars([(100, 100.2, 99.8, 100)] * 3),
            "ETH": [
                {"ts": BASE_TS, "open": 100, "high": 100.2, "low": 99.8, "close": 100},
                {"ts": BASE_TS + 120_000, "open": 100, "high": 100.2, "low": 99.8, "close": 100},
            ],
        }
        with self.assertRaisesRegex(ValueError, "exactly one minute"):
            run_portfolio_backtest(
                bars, [], {"BTC": [], "ETH": []}, config()
            )

    def test_final_open_position_closes_at_end_of_data(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100.1),
                (100.1, 100.2, 100, 100.15),
            ])
        }
        result = run_portfolio_backtest(
            bars, [candidate()], {"BTC": []}, config()
        )
        self.assertEqual(result["trades"][0]["exit_reason"], "end_of_data")
        self.assertEqual(result["equity_curve"][-1]["open_positions"], 0)

    def test_equity_curve_and_summary_are_returned(self):
        bars = {
            "BTC": make_bars([
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
                (100, 100.2, 99.8, 100),
            ])
        }
        result = run_portfolio_backtest(
            bars, [], {"BTC": []}, config()
        )
        self.assertEqual(result["final_equity"], 1000)
        self.assertEqual(len(result["equity_curve"]), 3)
        self.assertEqual(result["trade_count"], 0)


if __name__ == "__main__":
    unittest.main()
