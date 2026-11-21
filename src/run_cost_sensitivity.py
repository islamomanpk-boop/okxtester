"""Run controlled fee and slippage sensitivity tests."""

import csv
from pathlib import Path

from exit_experiment_config import build_baseline_experiments
from portfolio_backtester import (
    PortfolioBacktestConfig,
    run_portfolio_backtest,
)
from performance_reporting import write_performance_reports
from run_exit_experiments import ASSETS, load_inputs


COST_SCENARIOS = (
    {
        "scenario_id": "zero_fees_slippage_2bps",
        "taker_fee_rate": 0.0,
        "slippage_bps": 2.0,
    },
    {
        "scenario_id": "fees_0_05pct_zero_slippage",
        "taker_fee_rate": 0.0005,
        "slippage_bps": 0.0,
    },
    {
        "scenario_id": "fees_0_05pct_slippage_5bps",
        "taker_fee_rate": 0.0005,
        "slippage_bps": 5.0,
    },
)


def write_csv(path, rows, fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run_scenario(scenario, bars, funding, candidates, experiment):
    scenario_candidates = []
    for candidate in candidates:
        item = dict(candidate)
        item["exit_experiment"] = experiment
        scenario_candidates.append(item)

    config = PortfolioBacktestConfig(
        initial_equity=1000.0,
        risk_fraction=0.005,
        max_gross_leverage=1.0,
        taker_fee_rate=scenario["taker_fee_rate"],
        slippage_bps=scenario["slippage_bps"],
        record_equity_curve=False,
    )

    result = run_portfolio_backtest(
        bars_by_asset=bars,
        candidates=scenario_candidates,
        funding_by_asset=funding,
        config=config,
    )

    accepted = sum(len(d["accepted"]) for d in result["decisions"])
    rejected = sum(len(d["rejected"]) for d in result["decisions"])

    summary = {
        "scenario_id": scenario["scenario_id"],
        "experiment_id": experiment.experiment_id,
        "taker_fee_rate_per_side": scenario["taker_fee_rate"],
        "slippage_bps_per_side": scenario["slippage_bps"],
        "candidate_count": len(scenario_candidates),
        "accepted_entries": accepted,
        "rejected_entries": rejected,
        "trade_count": result["trade_count"],
        "initial_equity": result["initial_equity"],
        "final_equity": result["final_equity"],
        "net_pnl": result["net_pnl"],
        "return_pct": result["return_pct"],
        "max_drawdown_pct": result["max_drawdown_pct"],
        "gross_pnl": result["total_gross_pnl"],
        "fees": result["total_fees"],
        "funding_pnl": result["total_funding_pnl"],
    }

    output_dir = Path.home() / "okxtester/reports/cost_sensitivity"
    scenario_id = scenario["scenario_id"]

    write_csv(
        output_dir / f"{scenario_id}_summary.csv",
        [summary],
        list(summary),
    )

    trade_rows = [
        {"scenario_id": scenario_id, **trade}
        for trade in result["trades"]
    ]
    trade_fields = ["scenario_id"] + (
        list(result["trades"][0]) if result["trades"] else [
            "asset", "side", "entry_time", "exit_time", "gross_pnl",
            "funding_pnl", "total_fees", "net_pnl", "exit_reason",
        ]
    )
    write_csv(
        output_dir / f"{scenario_id}_trades.csv",
        trade_rows,
        trade_fields,
    )

    report_metadata = {
        "scenario_id": scenario_id,
        "experiment_id": experiment.experiment_id,
        "assets": ",".join(ASSETS),
        "execution_timeframe": "1m",
        "execution_window_start_utc": (
            __import__("datetime").datetime.fromtimestamp(
                bars[next(iter(bars))].timestamps[0] / 1000,
                __import__("datetime").timezone.utc,
            ).isoformat()
        ),
        "execution_window_end_utc": (
            __import__("datetime").datetime.fromtimestamp(
                bars[next(iter(bars))].timestamps[-1] / 1000,
                __import__("datetime").timezone.utc,
            ).isoformat()
        ),
        "taker_fee_rate_per_side": scenario["taker_fee_rate"],
        "slippage_bps_per_side": scenario["slippage_bps"],
        "funding_data": "Historical asset-specific realized funding rates",
        "funding_treatment": "Applied at funding timestamps; mark price when supplied, otherwise candle close proxy",
        "equity_curve_storage": "summary-only",
        "risk_fraction": 0.005,
        "max_gross_leverage": 1.0,
        "cost_sensitivity_note": "Same signals, date window, exit rules, risk fraction, and portfolio constraints; cost-aware sizing means fills, accepted entries, and outcomes can change.",
        "end_of_data_policy": "Open positions forcibly closed at final available candle",
    }
    performance_paths = write_performance_reports(
        result,
        output_dir,
        scenario_id,
        metadata=report_metadata,
    )

    print(f"\n===== {scenario_id} COMPLETE =====")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("Detailed performance files:")
    for path in performance_paths.values():
        print(path)

    return summary


def main():
    print("Loading and aligning five-asset inputs...")
    bars, funding, candidates, start_ts, end_ts = load_inputs()

    experiment = build_baseline_experiments()[0]

    print(f"Candidates: {len(candidates)}")
    print(f"Execution window: {start_ts} to {end_ts}")
    print(f"Baseline exit experiment: {experiment.experiment_id}")

    summaries = []
    for scenario in COST_SCENARIOS:
        summaries.append(
            run_scenario(
                scenario, bars, funding, candidates, experiment
            )
        )

    output_dir = Path.home() / "okxtester/reports/cost_sensitivity"
    fields = list(summaries[0])
    write_csv(output_dir / "cost_sensitivity_comparison.csv", summaries, fields)

    print("\n===== COST SENSITIVITY COMPLETE =====")
    print(f"Comparison saved to: {output_dir / 'cost_sensitivity_comparison.csv'}")


if __name__ == "__main__":
    main()
