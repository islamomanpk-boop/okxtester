"""Build complete, consistent performance reports from portfolio backtests."""

import csv
from pathlib import Path

from performance_metrics import (
    build_exit_reason_breakdown,
    build_grouped_trade_metrics,
    build_monthly_returns,
    summarize_portfolio_metrics,
    summarize_trade_metrics,
)


GROUP_FIELDS = {
    "per_asset": ("asset",),
    "per_direction": ("side",),
    "per_asset_direction": ("asset", "side"),
}

BREAKDOWN_FIELDS = (
    "trade_count",
    "net_pnl",
    "gross_pnl",
    "total_fees",
    "funding_pnl",
    "win_rate_pct",
    "profit_factor",
    "expectancy",
    "average_win",
    "average_loss",
    "payoff_ratio",
)


def _write_csv(path, rows, fallback_fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else list(fallback_fields)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(rows)


def _overall_metrics_row(result):
    trades = result.get("trades", [])
    portfolio = summarize_portfolio_metrics(result)
    trade = summarize_trade_metrics(
        trades,
        max_drawdown_amount=portfolio["max_drawdown_amount"] or 0.0,
    )
    row = {
        "trade_" + key: value
        for key, value in trade.items()
    }
    row.update({
        "portfolio_" + key: value
        for key, value in portfolio.items()
        if key != "daily_returns"
    })
    return row


def build_performance_report_data(result):
    """Return all report tables without writing files or mutating result."""
    trades = list(result.get("trades", []))
    portfolio = summarize_portfolio_metrics(result)
    drawdown = portfolio["max_drawdown_amount"] or 0.0

    overall = _overall_metrics_row(result)
    breakdowns = {
        name: build_grouped_trade_metrics(trades, group_fields=fields)
        for name, fields in GROUP_FIELDS.items()
    }
    monthly = build_monthly_returns(
        result.get("daily_equity_marks", []),
        result["initial_equity"],
        start_ts=result.get("start_ts"),
        end_ts=result.get("end_ts"),
    )
    daily = portfolio["daily_returns"]
    exit_reasons = build_exit_reason_breakdown(trades)

    return {
        "overall_metrics": [overall],
        "per_asset_metrics": breakdowns["per_asset"],
        "per_direction_metrics": breakdowns["per_direction"],
        "per_asset_direction_metrics": breakdowns["per_asset_direction"],
        "daily_returns": daily,
        "monthly_returns": monthly,
        "exit_reason_breakdown": exit_reasons,
    }


def _format_value(value):
    if value is None:
        return "unavailable"
    if isinstance(value, float):
        return f"{value:,.6f}"
    return str(value)


def _markdown_table(rows, fields):
    if not rows:
        return "_No closed trades._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(_format_value(row.get(field)) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, separator] + body)


def _build_markdown_report(report_id, data, metadata):
    overall = data["overall_metrics"][0]
    portfolio_fields = (
        "portfolio_initial_equity",
        "portfolio_final_equity",
        "portfolio_net_pnl",
        "portfolio_total_return_pct",
        "portfolio_max_drawdown_amount",
        "portfolio_max_drawdown_pct",
        "portfolio_recovery_factor",
        "portfolio_sharpe_ratio",
        "portfolio_sortino_ratio",
        "portfolio_cagr_pct",
        "portfolio_calmar_ratio",
        "portfolio_worst_daily_loss",
        "portfolio_worst_daily_loss_pct",
        "portfolio_worst_daily_loss_date_utc",
        "portfolio_max_concurrent_positions",
        "portfolio_average_capital_utilization_pct",
        "portfolio_max_capital_utilization_pct",
        "portfolio_max_gross_exposure",
        "portfolio_max_gross_exposure_equity_multiple",
    )
    trade_fields = (
        "trade_trade_count",
        "trade_net_pnl",
        "trade_gross_pnl",
        "trade_total_fees",
        "trade_funding_pnl",
        "trade_winning_trades",
        "trade_losing_trades",
        "trade_breakeven_trades",
        "trade_win_rate_pct",
        "trade_profit_factor",
        "trade_expectancy",
        "trade_average_win",
        "trade_average_loss",
        "trade_payoff_ratio",
        "trade_max_consecutive_losses",
        "trade_average_duration_minutes",
        "trade_median_duration_minutes",
        "trade_max_duration_minutes",
        "trade_recovery_factor",
    )
    lines = [
        f"# Performance report: {report_id}",
        "",
        "## Run metadata",
    ]
    for key, value in metadata.items():
        lines.append(f"- {key.replace('_', ' ').title()}: {_format_value(value)}")
    if not metadata:
        lines.append("- No run metadata supplied.")
    lines.extend(["", "## Portfolio risk and return", ""])
    lines.extend(
        f"- {field.removeprefix('portfolio_').replace('_', ' ').title()}: "
        f"{_format_value(overall.get(field))}"
        for field in portfolio_fields
    )
    lines.extend(["", "## Trade performance", ""])
    lines.extend(
        f"- {field.removeprefix('trade_').replace('_', ' ').title()}: "
        f"{_format_value(overall.get(field))}"
        for field in trade_fields
    )
    lines.extend([
        "",
        "## Per-asset performance",
        "",
        _markdown_table(
            data["per_asset_metrics"],
            ("asset",) + BREAKDOWN_FIELDS,
        ),
        "",
        "## LONG versus SHORT",
        "",
        _markdown_table(
            data["per_direction_metrics"],
            ("side",) + BREAKDOWN_FIELDS,
        ),
        "",
        "## Asset and direction",
        "",
        _markdown_table(
            data["per_asset_direction_metrics"],
            ("asset", "side") + BREAKDOWN_FIELDS,
        ),
        "",
        "## Exit reasons",
        "",
        _markdown_table(
            data["exit_reason_breakdown"],
            ("exit_reason", "trade_count", "gross_pnl", "total_fees",
             "funding_pnl", "net_pnl"),
        ),
        "",
        "## Monthly UTC returns",
        "",
        _markdown_table(
            data["monthly_returns"],
            ("month_utc", "starting_equity", "ending_equity",
             "net_pnl", "return_pct", "partial_month"),
        ),
        "",
        "## Important simulation limitations",
        "",
        "- End-of-data closures are forced simulation closures, not ordinary strategy exits.",
        "- Exchange liquidation is not simulated: maintenance-margin rules and liquidation fees are not modeled.",
        "- Fees, slippage, and funding are modeled assumptions; slippage is reflected in fills and is not reported as a separately measured cost.",
        "- Historical backtest results do not establish a predictive edge or guarantee future performance.",
        "",
    ])
    return "\n".join(lines)


def write_performance_reports(
    result,
    output_dir,
    report_id,
    metadata=None,
):
    """Write all breakdown CSVs and a human-readable Markdown report."""
    if not isinstance(report_id, str) or not report_id.strip():
        raise ValueError("report_id must be a non-empty string")
    if Path(report_id).name != report_id or report_id in (".", ".."):
        raise ValueError("report_id must be a filename-safe identifier")
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be a dictionary")

    data = build_performance_report_data(result)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "overall_metrics": f"{report_id}_overall_metrics.csv",
        "per_asset_metrics": f"{report_id}_per_asset_metrics.csv",
        "per_direction_metrics": f"{report_id}_per_direction_metrics.csv",
        "per_asset_direction_metrics": f"{report_id}_per_asset_direction_metrics.csv",
        "daily_returns": f"{report_id}_daily_returns.csv",
        "monthly_returns": f"{report_id}_monthly_returns.csv",
        "exit_reason_breakdown": f"{report_id}_exit_reason_breakdown.csv",
        "markdown_report": f"{report_id}_performance_report.md",
    }
    fallback_fields = {
        "per_asset_metrics": ("asset",) + BREAKDOWN_FIELDS,
        "per_direction_metrics": ("side",) + BREAKDOWN_FIELDS,
        "per_asset_direction_metrics": ("asset", "side") + BREAKDOWN_FIELDS,
        "daily_returns": ("date_utc", "ending_equity", "daily_pnl", "daily_return"),
        "monthly_returns": (
            "month_utc", "starting_equity", "ending_equity",
            "net_pnl", "return_pct", "partial_month",
        ),
        "exit_reason_breakdown": (
            "exit_reason", "trade_count", "gross_pnl",
            "total_fees", "funding_pnl", "net_pnl",
        ),
    }

    for key, filename in files.items():
        if key == "markdown_report":
            continue
        rows = data[key]
        fields = fallback_fields.get(key, tuple(data[key][0]) if rows else ())
        _write_csv(output_dir / filename, rows, fields)

    markdown = _build_markdown_report(report_id, data, metadata)
    (output_dir / files["markdown_report"]).write_text(
        markdown, encoding="utf-8"
    )
    return {key: output_dir / filename for key, filename in files.items()}
