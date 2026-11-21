"""Tests for complete performance report generation."""

import csv
from pathlib import Path
import tempfile
import unittest

from performance_reporting import (
    build_performance_report_data,
    write_performance_reports,
)


def sample_result():
    start = 1704067200000  # 2024-01-01 00:00 UTC
    end = 1704283200000    # 2024-01-03 12:00 UTC
    trades = [
        {
            "asset": "BTC", "side": "LONG",
            "entry_time": start, "exit_time": start + 60_000,
            "gross_pnl": 12.0, "total_fees": 2.0,
            "funding_pnl": 0.0, "net_pnl": 10.0,
            "exit_reason": "target",
        },
        {
            "asset": "ETH", "side": "SHORT",
            "entry_time": start + 60_000, "exit_time": start + 120_000,
            "gross_pnl": -27.0, "total_fees": 2.0,
            "funding_pnl": -1.0, "net_pnl": -30.0,
            "exit_reason": "stop",
        },
        {
            "asset": "BTC", "side": "SHORT",
            "entry_time": start + 120_000, "exit_time": start + 180_000,
            "gross_pnl": 2.0, "total_fees": 2.0,
            "funding_pnl": 0.0, "net_pnl": 0.0,
            "exit_reason": "end_of_data",
        },
    ]
    return {
        "initial_equity": 1000.0,
        "final_equity": 980.0,
        "net_pnl": -20.0,
        "return_pct": -2.0,
        "max_drawdown_amount": 50.0,
        "max_drawdown_pct": 5.0,
        "start_ts": start,
        "end_ts": end,
        "daily_equity_marks": [
            {"timestamp": start, "equity": 1000.0},
            {"timestamp": start + 86_400_000, "equity": 980.0},
        ],
        "max_concurrent_positions": 2,
        "average_capital_utilization_pct": 25.0,
        "max_capital_utilization_pct": 50.0,
        "max_gross_exposure": 500.0,
        "max_gross_exposure_equity_multiple": 0.5,
        "trades": trades,
        "equity_curve": [],
    }


class PerformanceReportingTests(unittest.TestCase):
    def test_builds_all_required_breakdown_tables(self):
        data = build_performance_report_data(sample_result())
        self.assertEqual(len(data["overall_metrics"]), 1)
        self.assertEqual(
            {row["asset"] for row in data["per_asset_metrics"]},
            {"BTC", "ETH"},
        )
        self.assertEqual(
            {row["side"] for row in data["per_direction_metrics"]},
            {"LONG", "SHORT"},
        )
        self.assertEqual(
            {(row["asset"], row["side"])
             for row in data["per_asset_direction_metrics"]},
            {("BTC", "LONG"), ("BTC", "SHORT"), ("ETH", "SHORT")},
        )
        self.assertEqual(
            {row["exit_reason"] for row in data["exit_reason_breakdown"]},
            {"target", "stop", "end_of_data"},
        )

    def test_losing_asset_and_direction_are_not_omitted(self):
        data = build_performance_report_data(sample_result())
        eth = next(row for row in data["per_asset_metrics"] if row["asset"] == "ETH")
        short = next(row for row in data["per_direction_metrics"] if row["side"] == "SHORT")
        self.assertEqual(eth["net_pnl"], -30.0)
        self.assertEqual(short["net_pnl"], -30.0)

    def test_overall_metrics_include_trade_and_portfolio_fields(self):
        row = build_performance_report_data(sample_result())["overall_metrics"][0]
        self.assertEqual(row["trade_trade_count"], 3)
        self.assertEqual(row["trade_net_pnl"], -20.0)
        self.assertEqual(row["portfolio_net_pnl"], -20.0)
        self.assertEqual(row["portfolio_max_drawdown_amount"], 50.0)
        self.assertEqual(row["portfolio_max_concurrent_positions"], 2)

    def test_daily_and_monthly_returns_are_included(self):
        data = build_performance_report_data(sample_result())
        self.assertEqual(len(data["daily_returns"]), 2)
        self.assertEqual(data["daily_returns"][1]["daily_pnl"], -20.0)
        self.assertEqual(len(data["monthly_returns"]), 1)
        self.assertEqual(data["monthly_returns"][0]["month_utc"], "2024-01")
        self.assertTrue(data["monthly_returns"][0]["partial_month"])

    def test_writes_all_csvs_and_markdown_report(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = write_performance_reports(
                sample_result(),
                directory,
                "test_run",
                metadata={
                    "execution_timeframe": "1m",
                    "equity_curve_storage": "summary-only",
                    "taker_fee_rate_per_side": 0.0005,
                },
            )
            self.assertEqual(len(paths), 8)
            for path in paths.values():
                self.assertTrue(Path(path).is_file(), path)

            with Path(paths["per_asset_metrics"]).open(
                newline="", encoding="utf-8"
            ) as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual({row["asset"] for row in rows}, {"BTC", "ETH"})

            report = Path(paths["markdown_report"]).read_text(encoding="utf-8")
            self.assertIn("summary-only", report)
            self.assertIn("Exchange liquidation is not simulated", report)
            self.assertIn("forced simulation closures", report)
            self.assertIn("Per-asset performance", report)
            self.assertIn("LONG versus SHORT", report)

    def test_empty_trade_set_still_writes_header_only_breakdowns(self):
        result = sample_result()
        result["trades"] = []
        with tempfile.TemporaryDirectory() as directory:
            paths = write_performance_reports(result, directory, "empty")
            with Path(paths["per_asset_metrics"]).open(
                newline="", encoding="utf-8"
            ) as handle:
                self.assertEqual(list(csv.reader(handle)), [
                    ["asset"] + [
                        "trade_count", "net_pnl", "gross_pnl", "total_fees",
                        "funding_pnl", "win_rate_pct", "profit_factor",
                        "expectancy", "average_win", "average_loss",
                        "payoff_ratio",
                    ]
                ])
            with Path(paths["exit_reason_breakdown"]).open(
                newline="", encoding="utf-8"
            ) as handle:
                self.assertEqual(len(list(csv.reader(handle))), 1)

    def test_rejects_unsafe_report_identifier(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                write_performance_reports(sample_result(), directory, "../bad")

    def test_does_not_mutate_backtest_result(self):
        result = sample_result()
        before = [dict(trade) for trade in result["trades"]]
        build_performance_report_data(result)
        self.assertEqual(result["trades"], before)


if __name__ == "__main__":
    unittest.main()
