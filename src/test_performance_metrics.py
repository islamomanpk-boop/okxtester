import unittest
from datetime import datetime, timezone

from performance_metrics import (
    build_daily_returns,
    build_exit_reason_breakdown,
    build_grouped_trade_metrics,
    build_monthly_returns,
    summarize_portfolio_metrics,
    summarize_trade_metrics,
)


def trade(
    net,
    gross=None,
    fee=0.0,
    funding=0.0,
    asset="BTC",
    side="LONG",
    entry=1_000,
    exit=61_000,
    reason="target",
):
    return {
        "asset": asset,
        "side": side,
        "entry_time": entry,
        "exit_time": exit,
        "gross_pnl": net if gross is None else gross,
        "total_fees": fee,
        "funding_pnl": funding,
        "net_pnl": net,
        "exit_reason": reason,
    }


class TradeMetricTests(unittest.TestCase):
    def test_trade_counts_rates_and_pnl(self):
        rows = [
            trade(10, gross=12, fee=2, funding=0),
            trade(-4, gross=-3, fee=1, funding=0, entry=2_000, exit=62_000),
            trade(0, gross=1, fee=1, entry=3_000, exit=63_000),
        ]
        result = summarize_trade_metrics(rows, max_drawdown_amount=5)
        self.assertEqual(result["trade_count"], 3)
        self.assertEqual(result["winning_trades"], 1)
        self.assertEqual(result["losing_trades"], 1)
        self.assertEqual(result["breakeven_trades"], 1)
        self.assertAlmostEqual(result["win_rate_pct"], 100 / 3)
        self.assertAlmostEqual(result["breakeven_rate_pct"], 100 / 3)
        self.assertEqual(result["net_pnl"], 6)
        self.assertEqual(result["gross_pnl"], 10)
        self.assertEqual(result["total_fees"], 4)
        self.assertEqual(result["profit_factor"], 2.5)
        self.assertEqual(result["expectancy"], 2)
        self.assertEqual(result["average_win"], 10)
        self.assertEqual(result["average_loss"], 4)
        self.assertEqual(result["payoff_ratio"], 2.5)
        self.assertEqual(result["largest_win"], 10)
        self.assertEqual(result["largest_loss"], 4)
        self.assertEqual(result["recovery_factor"], 1.2)

    def test_empty_trades_and_undefined_ratios(self):
        result = summarize_trade_metrics([])
        self.assertEqual(result["trade_count"], 0)
        self.assertIsNone(result["win_rate_pct"])
        self.assertIsNone(result["expectancy"])
        self.assertIsNone(result["profit_factor"])
        self.assertIsNone(result["payoff_ratio"])
        self.assertIsNone(result["average_duration_minutes"])
        self.assertEqual(result["max_consecutive_losses"], 0)

    def test_profit_factor_unavailable_without_losses(self):
        result = summarize_trade_metrics([trade(5)])
        self.assertIsNone(result["profit_factor"])
        self.assertIsNone(result["average_loss"])
        self.assertIsNone(result["payoff_ratio"])

    def test_profit_factor_unavailable_without_wins(self):
        result = summarize_trade_metrics([trade(-5)])
        self.assertEqual(result["profit_factor"], 0)
        self.assertIsNone(result["average_win"])
        self.assertIsNone(result["payoff_ratio"])

    def test_losing_streak_is_chronological_and_breakeven_breaks_it(self):
        rows = [
            trade(-1, entry=1_000, exit=181_000),
            trade(-2, entry=2_000, exit=61_000),
            trade(0, entry=3_000, exit=121_000),
            trade(-3, entry=4_000, exit=241_000),
        ]
        result = summarize_trade_metrics(rows)
        self.assertEqual(result["max_consecutive_losses"], 2)

    def test_trade_durations(self):
        rows = [
            trade(1, entry=0, exit=60_000),
            trade(1, entry=0, exit=180_000),
            trade(1, entry=0, exit=300_000),
        ]
        result = summarize_trade_metrics(rows)
        self.assertEqual(result["average_duration_minutes"], 3)
        self.assertEqual(result["median_duration_minutes"], 3)
        self.assertEqual(result["max_duration_minutes"], 5)

    def test_exit_before_entry_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot precede"):
            summarize_trade_metrics([trade(1, entry=120_000, exit=60_000)])


class DailyAndMonthlyTests(unittest.TestCase):
    def test_daily_marks_use_last_mark_per_utc_day(self):
        marks = [
            {"timestamp": 1_735_689_600_000, "equity": 1010},
            {"timestamp": 1_735_732_800_000, "equity": 1020},
            {"timestamp": 1_735_776_000_000, "equity": 1010},
        ]
        rows = build_daily_returns(marks, 1000)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["daily_pnl"], 10)
        self.assertAlmostEqual(rows[0]["daily_return"], 0.01)
        self.assertEqual(rows[1]["daily_pnl"], 10)
        self.assertEqual(rows[2]["daily_pnl"], -10)

    def test_daily_marks_accept_iso_utc_timestamps(self):
        marks = [
            {"timestamp": "2026-01-01T12:00:00Z", "equity": 1010},
            {"timestamp": "2026-01-01T23:59:00Z", "equity": 1020},
        ]
        rows = build_daily_returns(marks, 1000)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["ending_equity"], 1020)

    def test_daily_returns_reject_nonpositive_initial_equity(self):
        with self.assertRaises(ValueError):
            build_daily_returns([], 0)

    def test_monthly_returns_chain_starting_equity_and_flag_partials(self):
        marks = [
            {"timestamp": "2026-01-15T23:59:00Z", "equity": 1100},
            {"timestamp": "2026-02-28T23:59:00Z", "equity": 1000},
            {"timestamp": "2026-03-10T12:00:00Z", "equity": 1200},
        ]
        rows = build_monthly_returns(marks, 1000)
        self.assertEqual([row["month_utc"] for row in rows], [
            "2026-01", "2026-02", "2026-03"
        ])
        self.assertEqual(rows[0]["starting_equity"], 1000)
        self.assertEqual(rows[1]["starting_equity"], 1100)
        self.assertEqual(rows[2]["starting_equity"], 1000)
        self.assertTrue(rows[0]["partial_month"])
        self.assertFalse(rows[1]["partial_month"])
        self.assertTrue(rows[2]["partial_month"])
        self.assertEqual(rows[2]["net_pnl"], 200)

    def test_empty_monthly_marks(self):
        self.assertEqual(build_monthly_returns([], 1000), [])


class GroupingTests(unittest.TestCase):
    def test_grouped_metrics_include_each_asset_and_direction(self):
        rows = [
            trade(10, asset="BTC", side="LONG"),
            trade(-3, asset="BTC", side="SHORT"),
            trade(-2, asset="ETH", side="SHORT"),
        ]
        by_asset = build_grouped_trade_metrics(rows, ("asset",))
        self.assertEqual([row["asset"] for row in by_asset], ["BTC", "ETH"])
        self.assertEqual(by_asset[0]["trade_count"], 2)
        by_asset_side = build_grouped_trade_metrics(rows, ("asset", "side"))
        self.assertEqual(len(by_asset_side), 3)
        self.assertEqual(
            {(row["asset"], row["side"]) for row in by_asset_side},
            {("BTC", "LONG"), ("BTC", "SHORT"), ("ETH", "SHORT")},
        )

    def test_exit_reason_breakdown(self):
        rows = [
            trade(4, reason="target"),
            trade(-2, reason="stop", fee=0.5),
            trade(-1, reason="stop", fee=0.25),
        ]
        result = build_exit_reason_breakdown(rows)
        self.assertEqual([row["exit_reason"] for row in result], ["stop", "target"])
        stop = result[0]
        self.assertEqual(stop["trade_count"], 2)
        self.assertEqual(stop["net_pnl"], -3)
        self.assertEqual(stop["total_fees"], 0.75)


class PortfolioMetricTests(unittest.TestCase):
    def test_portfolio_metrics_and_exposure(self):
        curve = [
            {"timestamp": 1_735_689_600_000, "equity": 1000,
             "gross_exposure": 500, "open_positions": 1},
            {"timestamp": 1_735_776_000_000, "equity": 900,
             "gross_exposure": 900, "open_positions": 2},
            {"timestamp": 1_735_862_400_000, "equity": 1100,
             "gross_exposure": 0, "open_positions": 0},
        ]
        result = summarize_portfolio_metrics({
            "initial_equity": 1000,
            "final_equity": 1100,
            "equity_curve": curve,
        })
        self.assertAlmostEqual(result["total_return_pct"], 10)
        self.assertAlmostEqual(result["max_drawdown_amount"], 100)
        self.assertAlmostEqual(result["max_drawdown_pct"], 10)
        self.assertEqual(result["max_concurrent_positions"], 2)
        self.assertEqual(result["max_gross_exposure"], 900)
        self.assertEqual(result["max_gross_exposure_equity_multiple"], 1)
        self.assertAlmostEqual(result["average_capital_utilization_pct"], 50)
        self.assertEqual(result["worst_daily_loss"], -100)
        self.assertIsNotNone(result["sharpe_ratio"])
        self.assertIsNotNone(result["sortino_ratio"])
        self.assertIsNotNone(result["cagr_pct"])
        self.assertIsNotNone(result["calmar_ratio"])

    def test_undefined_portfolio_ratios_are_none(self):
        result = summarize_portfolio_metrics({
            "initial_equity": 1000,
            "final_equity": 1000,
            "equity_curve": [
                {"timestamp": 1_735_689_600_000, "equity": 1000,
                 "gross_exposure": 0, "open_positions": 0},
            ],
        })
        self.assertIsNone(result["sharpe_ratio"])
        self.assertIsNone(result["sortino_ratio"])
        self.assertIsNone(result["cagr_pct"])
        self.assertIsNone(result["calmar_ratio"])
        self.assertIsNone(result["recovery_factor"])

    def test_portfolio_metrics_can_use_daily_marks_without_full_curve(self):
        marks = [
            {"timestamp": "2026-01-01T23:59:00Z", "equity": 990},
            {"timestamp": "2026-01-02T23:59:00Z", "equity": 1010},
        ]
        result = summarize_portfolio_metrics({
            "initial_equity": 1000,
            "final_equity": 1010,
            "equity_curve": [],
            "daily_equity_marks": marks,
        })
        self.assertEqual(len(result["daily_returns"]), 2)
        self.assertEqual(result["max_drawdown_amount"], 0)
        self.assertEqual(result["max_concurrent_positions"], 0)


if __name__ == "__main__":
    unittest.main()
