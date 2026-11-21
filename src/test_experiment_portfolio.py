import unittest

from exit_experiment_config import build_baseline_experiments
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


def get_experiment(stop_model, target_model):
    for exp in build_baseline_experiments():
        if (
            exp.stop_model == stop_model
            and exp.target_model == target_model
            and exp.trailing_mode == "none"
        ):
            return exp
    raise AssertionError("Requested experiment was not found")


def make_candidate(experiment):
    return {
        "asset": "BTC",
        "side": 1,
        "signal_available_at": BASE_TS + 60_000,
        "signal_priority": 1,
        "stop_distance_atr": 1.0,
        "stop_reference_price": 99.75,
        "signal_high": 100.2,
        "signal_low": 99.8,
        "signal_atr14": 0.5,
        "exit_experiment": experiment,
    }


def make_config(slippage_bps=0):
    return PortfolioBacktestConfig(
        initial_equity=1000,
        taker_fee_rate=0,
        slippage_bps=slippage_bps,
    )


class ExperimentPortfolioTests(unittest.TestCase):

    def test_fixed_stop_and_target_use_slippage_adjusted_entry(self):
        exp = get_experiment(
            "fixed_stop_0_50pct",
            "fixed_target_0_75pct",
        )
        bars = make_bars([
            (100.0, 100.2, 99.8, 100.0),
            (100.0, 100.5, 99.9, 100.3),
            (100.3, 101.0, 100.2, 100.8),
        ])

        result = run_portfolio_backtest(
            candidates=[make_candidate(exp)],
            bars_by_asset={"BTC": bars},
            funding_by_asset={"BTC": []},
            config=make_config(slippage_bps=10),
        )

        self.assertEqual(len(result["trades"]), 1)
        trade = result["trades"][0]

        expected_entry = 100.0 * 1.001
        self.assertAlmostEqual(trade["entry_price"], expected_entry)
        self.assertAlmostEqual(
            trade["stop_price"], expected_entry * (1 - 0.005)
        )
        self.assertAlmostEqual(
            trade["target_price"], expected_entry * (1 + 0.0075)
        )
        self.assertEqual(trade["exit_reason"], "target")

    def test_exact_candle_stop_and_one_r_target(self):
        exp = get_experiment(
            "signal_extreme_exact",
            "target_1R",
        )
        bars = make_bars([
            (100.0, 100.2, 99.8, 100.0),
            (100.0, 100.2, 99.9, 100.1),
            (100.1, 100.6, 100.0, 100.5),
        ])

        result = run_portfolio_backtest(
            candidates=[make_candidate(exp)],
            bars_by_asset={"BTC": bars},
            funding_by_asset={"BTC": []},
            config=make_config(slippage_bps=10),
        )

        self.assertEqual(len(result["trades"]), 1)
        trade = result["trades"][0]

        expected_entry = 100.1
        expected_stop = 99.8
        expected_target = expected_entry + (
            expected_entry - expected_stop
        )

        self.assertAlmostEqual(trade["entry_price"], expected_entry)
        self.assertAlmostEqual(trade["stop_price"], expected_stop)
        self.assertAlmostEqual(trade["target_price"], expected_target)

    def test_gap_past_candle_stop_rejects_candidate_without_crashing(self):
        exp = get_experiment(
            "signal_extreme_exact",
            "target_1R",
        )
        bars = make_bars([
            (100.0, 100.2, 99.8, 100.0),
            (99.7, 100.0, 99.5, 99.8),
            (99.8, 100.0, 99.6, 99.9),
        ])

        result = run_portfolio_backtest(
            candidates=[make_candidate(exp)],
            bars_by_asset={"BTC": bars},
            funding_by_asset={"BTC": []},
            config=make_config(slippage_bps=10),
        )

        self.assertEqual(result["trades"], [])

        rejected = [
            item
            for decision in result["decisions"]
            for item in decision["rejected"]
        ]
        self.assertTrue(
            any(
                item["reason"].startswith("invalid_experiment_entry:")
                for item in rejected
            ),
            "Expected the invalid candle-stop entry to be rejected",
        )


if __name__ == "__main__":
    unittest.main()
