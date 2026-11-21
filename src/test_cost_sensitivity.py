import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from run_cost_sensitivity import COST_SCENARIOS, run_scenario
from exit_experiment_config import build_baseline_experiments


class TestCostSensitivity(unittest.TestCase):
    def test_scenario_invokes_detailed_performance_reporting(self):
        bars = {
            "BTC": type("Bars", (), {"timestamps": [1_000_000, 1_060_000]})()
        }
        result = {
            "decisions": [], "trades": [], "trade_count": 0,
            "initial_equity": 1000.0, "final_equity": 1000.0,
            "net_pnl": 0.0, "return_pct": 0.0,
            "max_drawdown_pct": 0.0, "total_gross_pnl": 0.0,
            "total_fees": 0.0, "total_funding_pnl": 0.0,
            "equity_curve": [], "daily_equity_marks": [],
            "max_drawdown_amount": 0.0,
            "start_ts": 1_000_000, "end_ts": 1_060_000,
        }
        with tempfile.TemporaryDirectory() as folder:
            with patch("run_cost_sensitivity.run_portfolio_backtest", return_value=result), patch(
                "run_cost_sensitivity.write_performance_reports"
            ) as report_writer, patch("run_cost_sensitivity.Path.home", return_value=Path(folder)):
                run_scenario(
                    COST_SCENARIOS[0], bars, {"BTC": []}, [],
                    build_baseline_experiments()[0],
                )
        report_writer.assert_called_once()
        metadata = report_writer.call_args.kwargs["metadata"]
        self.assertEqual(metadata["execution_timeframe"], "1m")
        self.assertEqual(metadata["taker_fee_rate_per_side"], 0.0)
        self.assertEqual(metadata["slippage_bps_per_side"], 2.0)
        self.assertIn("cost-aware sizing", metadata["cost_sensitivity_note"])

    def test_three_distinct_cost_scenarios_exist(self):
        self.assertEqual(len(COST_SCENARIOS), 3)
        self.assertEqual(
            len({item["scenario_id"] for item in COST_SCENARIOS}), 3
        )

    def test_zero_fee_scenario_keeps_two_bps_slippage(self):
        scenario = COST_SCENARIOS[0]
        self.assertEqual(scenario["taker_fee_rate"], 0.0)
        self.assertEqual(scenario["slippage_bps"], 2.0)

    def test_zero_slippage_scenario_keeps_baseline_fee(self):
        scenario = COST_SCENARIOS[1]
        self.assertEqual(scenario["taker_fee_rate"], 0.0005)
        self.assertEqual(scenario["slippage_bps"], 0.0)

    def test_high_slippage_scenario_keeps_baseline_fee(self):
        scenario = COST_SCENARIOS[2]
        self.assertEqual(scenario["taker_fee_rate"], 0.0005)
        self.assertEqual(scenario["slippage_bps"], 5.0)


if __name__ == "__main__":
    unittest.main()
