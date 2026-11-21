"""Run one shared-capital, five-asset exit experiment."""

import argparse
import csv
import math
from bisect import bisect_left, bisect_right
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from compact_bar_series import CompactBarSeries
from exit_experiment_config import build_baseline_experiments
from portfolio_backtester import (
    PortfolioBacktestConfig,
    run_portfolio_backtest,
)
from performance_reporting import write_performance_reports
from trade_candidate_engine import REQUIRED, build_candidates


ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
FEE_RATE = 0.0005
SLIPPAGE_BPS = 2.0


def trim_series_to_window(bars, start_ts, end_ts):
    """Trim compact candles in place to an inclusive common time window."""
    left = bisect_left(bars.timestamps, int(start_ts))
    right = bisect_right(bars.timestamps, int(end_ts))

    if left >= right:
        raise ValueError("Common execution window contains no candles")

    for name in ("timestamps", "opens", "highs", "lows", "closes", "volumes"):
        values = getattr(bars, name)
        del values[right:]
        del values[:left]

    if bars.timestamps[0] != start_ts or bars.timestamps[-1] > end_ts:
        raise ValueError("Execution candles do not align to common window")

    return bars


def load_funding(path, start_ts, end_ts):
    """Load only funding events inside the shared execution window."""
    events = []

    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"funding_time", "funding_rate"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path}: missing funding columns")

        for row in reader:
            ts = int(float(row["funding_time"]))
            rate = float(row["funding_rate"])

            if not math.isfinite(rate):
                raise ValueError(f"{path}: invalid funding rate")

            if start_ts <= ts <= end_ts:
                events.append({
                    "funding_time": ts,
                    "funding_rate": rate,
                })

    events.sort(key=lambda event: event["funding_time"])

    if any(
        events[i]["funding_time"] >= events[i + 1]["funding_time"]
        for i in range(len(events) - 1)
    ):
        raise ValueError(f"{path}: duplicate funding timestamps")

    return events


def load_inputs(home=None):
    """Load five assets, align execution bars, build Model A candidates."""
    home = Path(home) if home else Path.home()

    signal_dir = home / "okx_adaptive_bot/reports/price_action_signals"
    execution_dir = home / "okx_scalping_data"
    funding_dir = execution_dir / "funding_rates/processed"

    bars_by_asset = {}
    for asset in ASSETS:
        path = execution_dir / f"{asset}_USDT_USDT_1m.csv"
        bars_by_asset[asset] = CompactBarSeries.from_csv(path)

    common_start = max(
        bars.timestamps[0] for bars in bars_by_asset.values()
    )
    common_end = min(
        bars.timestamps[-1] for bars in bars_by_asset.values()
    )

    if common_start >= common_end:
        raise ValueError("Assets have no common execution window")

    for asset in ASSETS:
        trim_series_to_window(
            bars_by_asset[asset], common_start, common_end
        )

    expected_count = (
        (common_end - common_start) // 60_000
    ) + 1

    for asset, bars in bars_by_asset.items():
        if len(bars) != expected_count:
            raise ValueError(
                f"{asset}: execution candles do not fully cover common window"
            )

    funding_by_asset = {}
    for asset in ASSETS:
        path = funding_dir / f"{asset}_USDT_SWAP_funding_rates.csv"
        funding_by_asset[asset] = load_funding(
            path, common_start, common_end
        )

    candidates = []
    selected_columns = list(REQUIRED) + [
        "daily_structure", "four_hour_structure"
    ]

    for asset in ASSETS:
        path = signal_dir / f"{asset}_15m_price_action_signals.csv"
        frame = pd.read_csv(path, usecols=selected_columns)

        asset_candidates = build_candidates(frame, asset=asset)
        del frame

        candidates.extend(
            candidate for candidate in asset_candidates
            if common_start <= candidate["signal_available_at"] <= common_end
        )
        del asset_candidates

    candidates.sort(key=lambda item: (
        item["signal_available_at"],
        -item["signal_priority"],
        item["stop_distance_atr"],
        item["asset"],
    ))

    return (
        bars_by_asset,
        funding_by_asset,
        candidates,
        common_start,
        common_end,
    )


def write_rows(path, rows, fallback_fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fields = list(rows[0]) if rows else list(fallback_fields)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(rows)


def run_one_experiment(experiment, home=None):
    """Load inputs and run one experiment (single-run CLI compatibility)."""
    home = Path(home) if home else Path.home()
    inputs = load_inputs(home)
    return run_one_experiment_with_inputs(experiment, inputs, home=home)


def run_one_experiment_with_inputs(experiment, inputs, home=None):
    """Run one experiment using preloaded shared inputs.

    The batch runner calls this helper so candles, funding, and candidates
    are loaded only once for the complete experiment matrix.
    """
    home = Path(home) if home else Path.home()

    (
        bars_by_asset,
        funding_by_asset,
        candidates,
        start_ts,
        end_ts,
    ) = inputs

    experiment_candidates = []
    for candidate in candidates:
        item = dict(candidate)
        item["exit_experiment"] = experiment
        experiment_candidates.append(item)

    config = PortfolioBacktestConfig(
        initial_equity=1000.0,
        risk_fraction=0.005,
        max_gross_leverage=1.0,
        taker_fee_rate=FEE_RATE,
        slippage_bps=SLIPPAGE_BPS,
        record_equity_curve=False,
    )

    result = run_portfolio_backtest(
        bars_by_asset=bars_by_asset,
        candidates=experiment_candidates,
        funding_by_asset=funding_by_asset,
        config=config,
    )

    accepted = sum(len(d["accepted"]) for d in result["decisions"])
    rejected = sum(len(d["rejected"]) for d in result["decisions"])

    summary = {
        "experiment_id": experiment.experiment_id,
        "stop_model": experiment.stop_model,
        "target_model": experiment.target_model,
        "target_value": experiment.target_value,
        "trailing_mode": experiment.trailing_mode,
        "assets": ",".join(ASSETS),
        "start_utc": datetime.fromtimestamp(
            start_ts / 1000, timezone.utc
        ).isoformat(),
        "end_utc": datetime.fromtimestamp(
            end_ts / 1000, timezone.utc
        ).isoformat(),
        "execution_minutes": len(next(iter(bars_by_asset.values()))),
        "candidate_count": len(experiment_candidates),
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
        "taker_fee_rate_per_side": FEE_RATE,
        "slippage_bps_per_side": SLIPPAGE_BPS,
    }

    output_dir = home / "okxtester/reports/exit_experiments"
    output_dir.mkdir(parents=True, exist_ok=True)
    experiment_id = experiment.experiment_id

    write_rows(
        output_dir / f"{experiment_id}_summary.csv",
        [summary],
        summary.keys(),
    )

    trades = [
        {"experiment_id": experiment_id, **trade}
        for trade in result["trades"]
    ]
    trade_fields = [
        "experiment_id", "asset", "side", "entry_time", "exit_time",
        "entry_price", "exit_price", "quantity", "stop_price",
        "target_price", "signal_priority", "gross_pnl", "funding_pnl",
        "entry_fee", "exit_fee", "total_fees", "net_pnl", "exit_reason",
    ]
    write_rows(
        output_dir / f"{experiment_id}_trades.csv",
        trades,
        trade_fields,
    )

    report_metadata = {
        "experiment_id": experiment_id,
        "stop_model": experiment.stop_model,
        "target_model": experiment.target_model,
        "target_value": experiment.target_value,
        "trailing_mode": experiment.trailing_mode,
        "assets": ",".join(ASSETS),
        "execution_timeframe": "1m",
        "execution_window_start_utc": summary["start_utc"],
        "execution_window_end_utc": summary["end_utc"],
        "taker_fee_rate_per_side": FEE_RATE,
        "slippage_bps_per_side": SLIPPAGE_BPS,
        "funding_data": "Historical asset-specific realized funding rates",
        "funding_treatment": "Applied at funding timestamps; mark price when supplied, otherwise candle close proxy",
        "equity_curve_storage": "summary-only",
        "risk_fraction": 0.005,
        "max_gross_leverage": 1.0,
        "end_of_data_policy": "Open positions forcibly closed at final available candle",
    }
    performance_paths = write_performance_reports(
        result,
        output_dir,
        experiment_id,
        metadata=report_metadata,
    )

    report = [
        f"# Exit experiment: {experiment_id}",
        "",
        "## Configuration",
        f"- Assets: {', '.join(ASSETS)}",
        f"- Execution: synchronized 1-minute candles",
        f"- Starting equity: $1,000",
        f"- Risk budget: 0.5% of current equity per trade",
        f"- Maximum gross exposure: 1.0x equity",
        f"- Taker fee: 0.05% per side",
        f"- Slippage: 2 bps per side",
        f"- Funding: historical asset-specific funding events",
        f"- Equity curve storage: summary-only mode",
        "",
        "## Results",
        f"- Execution window: {summary['start_utc']} to {summary['end_utc']}",
        f"- Candidates: {len(experiment_candidates):,}",
        f"- Accepted entries: {accepted:,}",
        f"- Rejected entries: {rejected:,}",
        f"- Closed trades: {result['trade_count']:,}",
        f"- Final equity: ${result['final_equity']:,.2f}",
        f"- Net PnL: ${result['net_pnl']:,.2f}",
        f"- Return: {result['return_pct']:.2f}%",
        f"- Maximum drawdown: {result['max_drawdown_pct']:.2f}%",
        f"- Gross PnL: ${result['total_gross_pnl']:,.2f}",
        f"- Fees: ${result['total_fees']:,.2f}",
        f"- Funding PnL: ${result['total_funding_pnl']:,.2f}",
        "",
        "## Important",
        "This is a historical simulation, not a live-trading result. "
        "Fees, slippage and funding are modeled assumptions. "
        "No parameter has been selected as optimal from this single run.",
        "",
    ]

    (output_dir / f"{experiment_id}_report.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print("\nEXPERIMENT COMPLETE")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print(f"\nReports saved in: {output_dir}")
    print("Detailed performance files:")
    for path in performance_paths.values():
        print(path)

    return summary


def main():
    experiments = build_baseline_experiments()
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-experiments", action="store_true")
    parser.add_argument("--experiment-id", default=experiments[0].experiment_id)
    args = parser.parse_args()

    if args.list_experiments:
        for experiment in experiments:
            print(experiment.experiment_id)
        return

    selected = {
        experiment.experiment_id: experiment
        for experiment in experiments
    }

    if args.experiment_id not in selected:
        parser.error("Unknown experiment ID. Use --list-experiments.")

    run_one_experiment(selected[args.experiment_id])


if __name__ == "__main__":
    main()
