"""Reusable performance metrics for portfolio backtests.

All trade PnL metrics use net_pnl after fees and funding.
Timestamps are Unix milliseconds or ISO-8601 strings.
"""

from collections import defaultdict
from datetime import datetime, timezone
from calendar import monthrange
import math
import statistics


def _number(value, default=0.0):
    if value is None:
        return default
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Metric inputs must be finite")
    return result


def _timestamp(value):
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value) / 1000.0, timezone.utc)
    elif isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
    else:
        raise ValueError("Timestamp must be Unix milliseconds, ISO text, or datetime")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _trade_time(trade, field):
    if field not in trade or trade[field] is None:
        raise ValueError(f"Trade is missing {field}")
    return _timestamp(trade[field])


def _pnl(trade, field):
    return _number(trade.get(field, 0.0))


def summarize_trade_metrics(trades, max_drawdown_amount=0.0):
    """Summarize a trade collection using net PnL for wins/losses and ratios."""
    rows = list(trades)
    net = [_pnl(t, "net_pnl") for t in rows]
    gross = sum(_pnl(t, "gross_pnl") for t in rows)
    fees = sum(_pnl(t, "total_fees") for t in rows)
    funding = sum(_pnl(t, "funding_pnl") for t in rows)
    wins = [v for v in net if v > 0]
    losses = [v for v in net if v < 0]
    breakeven = sum(v == 0 for v in net)
    total_net = sum(net)
    loss_total = abs(sum(losses))
    profit_factor = sum(wins) / loss_total if loss_total > 0 else None
    average_win = statistics.fmean(wins) if wins else None
    average_loss = abs(statistics.fmean(losses)) if losses else None
    payoff = (
        average_win / average_loss
        if average_win is not None and average_loss not in (None, 0)
        else None
    )

    ordered = sorted(
        enumerate(rows),
        key=lambda pair: (_trade_time(pair[1], "exit_time"), pair[0]),
    )
    max_losing_streak = current_streak = 0
    for _, trade in ordered:
        value = _pnl(trade, "net_pnl")
        if value < 0:
            current_streak += 1
            max_losing_streak = max(max_losing_streak, current_streak)
        else:
            current_streak = 0

    durations = []
    for trade in rows:
        minutes = (
            _trade_time(trade, "exit_time") -
            _trade_time(trade, "entry_time")
        ).total_seconds() / 60.0
        if minutes < 0:
            raise ValueError("Trade exit_time cannot precede entry_time")
        durations.append(minutes)

    dd_amount = _number(max_drawdown_amount)
    return {
        "trade_count": len(rows),
        "net_pnl": total_net,
        "gross_pnl": gross,
        "total_fees": fees,
        "funding_pnl": funding,
        "winning_trades": len(wins),
        "losing_trades": len(losses),
        "breakeven_trades": breakeven,
        "win_rate_pct": len(wins) / len(rows) * 100.0 if rows else None,
        "breakeven_rate_pct": breakeven / len(rows) * 100.0 if rows else None,
        "profit_factor": profit_factor,
        "expectancy": total_net / len(rows) if rows else None,
        "average_win": average_win,
        "average_loss": average_loss,
        "payoff_ratio": payoff,
        "largest_win": max(wins) if wins else None,
        "largest_loss": abs(min(losses)) if losses else None,
        "max_consecutive_losses": max_losing_streak,
        "average_duration_minutes": statistics.fmean(durations) if durations else None,
        "median_duration_minutes": statistics.median(durations) if durations else None,
        "max_duration_minutes": max(durations) if durations else None,
        "recovery_factor": total_net / dd_amount if dd_amount > 0 else None,
    }


def _mark_timestamp(mark):
    if "timestamp" in mark:
        return mark["timestamp"]
    if "ts" in mark:
        return mark["ts"]
    raise ValueError("Equity mark must contain timestamp or ts")


def _normalize_marks(marks):
    normalized = []
    for mark in marks:
        dt = _timestamp(_mark_timestamp(mark))
        equity = _number(mark.get("equity"))
        normalized.append((dt, equity, mark))
    normalized.sort(key=lambda item: item[0])
    for index in range(1, len(normalized)):
        if normalized[index][0] == normalized[index - 1][0]:
            normalized[index - 1] = normalized[index]
    return normalized


def build_daily_returns(daily_marks, initial_equity):
    """Return the last available equity mark for each UTC date."""
    initial = _number(initial_equity)
    if initial <= 0:
        raise ValueError("Initial equity must be positive")
    marks = _normalize_marks(daily_marks)
    by_date = {}
    for dt, equity, _ in marks:
        by_date[dt.date().isoformat()] = equity

    output = []
    previous_equity = initial
    for day, ending_equity in sorted(by_date.items()):
        pnl = ending_equity - previous_equity
        daily_return = pnl / previous_equity if previous_equity > 0 else None
        output.append({
            "date_utc": day,
            "ending_equity": ending_equity,
            "daily_pnl": pnl,
            "daily_return": daily_return,
        })
        previous_equity = ending_equity
    return output


def build_monthly_returns(daily_marks, initial_equity, start_ts=None, end_ts=None):
    """Build UTC calendar-month returns and flag partial first/final months."""
    initial = _number(initial_equity)
    if initial <= 0:
        raise ValueError("Initial equity must be positive")
    marks = _normalize_marks(daily_marks)
    if not marks:
        return []

    month_ends = {}
    for dt, equity, _ in marks:
        month_ends[(dt.year, dt.month)] = (dt, equity)

    start = _timestamp(start_ts) if start_ts is not None else None
    end = _timestamp(end_ts) if end_ts is not None else marks[-1][0]
    output = []
    previous_equity = initial
    for (year, month), (dt, ending_equity) in sorted(month_ends.items()):
        month_start = datetime(year, month, 1, tzinfo=timezone.utc)
        last_day = monthrange(year, month)[1]
        final_minute = datetime(year, month, last_day, 23, 59, tzinfo=timezone.utc)
        partial = (
            start is not None
            and (year, month) == (start.year, start.month)
            and start > month_start
        ) or (
            (year, month) == (end.year, end.month)
            and end < final_minute
        )
        pnl = ending_equity - previous_equity
        output.append({
            "month_utc": f"{year:04d}-{month:02d}",
            "starting_equity": previous_equity,
            "ending_equity": ending_equity,
            "net_pnl": pnl,
            "return_pct": (
                pnl / previous_equity * 100.0
                if previous_equity > 0 else None
            ),
            "partial_month": partial,
        })
        previous_equity = ending_equity
    return output


def _drawdown_metrics(curve):
    peak = None
    max_amount = 0.0
    max_pct = 0.0
    for _, equity, _ in curve:
        if peak is None or equity > peak:
            peak = equity
        amount = peak - equity
        pct = amount / peak * 100.0 if peak > 0 else 0.0
        max_amount = max(max_amount, amount)
        max_pct = max(max_pct, pct)
    return max_amount, max_pct


def summarize_portfolio_metrics(result, daily_marks=None):
    """Calculate portfolio risk/return metrics from a backtest result."""
    initial = _number(result.get("initial_equity"))
    final = _number(result.get("final_equity"))
    if initial <= 0:
        raise ValueError("Initial equity must be positive")
    curve = _normalize_marks(result.get("equity_curve", []))
    if daily_marks is None:
        daily_marks = result.get("daily_equity_marks")
    if daily_marks is None:
        daily_marks = [
            {"timestamp": int(dt.timestamp() * 1000), "equity": equity}
            for dt, equity, _ in curve
        ]
    daily = build_daily_returns(daily_marks, initial)
    returns = [row["daily_return"] for row in daily if row["daily_return"] is not None]

    std = statistics.pstdev(returns) if len(returns) >= 2 else 0.0
    sharpe = (
        statistics.fmean(returns) / std * math.sqrt(365.0)
        if len(returns) >= 2 and std > 0 else None
    )
    downside = math.sqrt(
        sum(min(value, 0.0) ** 2 for value in returns) / len(returns)
    ) if returns else 0.0
    sortino = (
        statistics.fmean(returns) / downside * math.sqrt(365.0)
        if returns and downside > 0 else None
    )

    if result.get("start_ts") is not None and result.get("end_ts") is not None:
        elapsed_days = (
            _timestamp(result["end_ts"]) - _timestamp(result["start_ts"])
        ).total_seconds() / 86400.0
    elif curve:
        elapsed_days = (curve[-1][0] - curve[0][0]).total_seconds() / 86400.0
    else:
        # Daily marks do not preserve exact intraday test boundaries.
        elapsed_days = 0.0
    cagr = (
        (final / initial) ** (365.0 / elapsed_days) - 1.0
        if elapsed_days > 0 and final > 0 else None
    )

    if curve:
        dd_amount, dd_pct = _drawdown_metrics(curve)
    else:
        dd_amount = dd_pct = None
    if "max_drawdown_amount" in result:
        dd_amount = max(dd_amount or 0.0, _number(result["max_drawdown_amount"]))
    if "max_drawdown_pct" in result:
        dd_pct = max(dd_pct or 0.0, _number(result["max_drawdown_pct"]))
    dd_fraction = dd_pct / 100.0 if dd_pct is not None else None
    calmar = (
        cagr / dd_fraction
        if cagr is not None and dd_fraction is not None and dd_fraction > 0
        else None
    )

    worst = min(daily, key=lambda row: row["daily_pnl"]) if daily else None
    worst_start_equity = (
        worst["ending_equity"] - worst["daily_pnl"] if worst else None
    )
    worst_pct = (
        worst["daily_pnl"] / worst_start_equity * 100.0
        if worst and worst_start_equity > 0 else None
    )

    exposure_values = []
    max_positions = int(result.get("max_concurrent_positions", 0))
    max_gross = _number(result.get("max_gross_exposure", 0.0))
    max_utilization = (
        _number(result.get("max_capital_utilization_pct", 0.0)) / 100.0
    )
    max_gross_multiple = _number(
        result.get("max_gross_exposure_equity_multiple", 0.0)
    )
    for _, equity, mark in curve:
        gross = _number(mark.get("gross_exposure", 0.0))
        positions = int(mark.get("open_positions", 0))
        max_positions = max(max_positions, positions)
        max_gross = max(max_gross, gross)
        utilization = gross / equity if equity > 0 else 0.0
        exposure_values.append(utilization)
        max_utilization = max(max_utilization, utilization)
        if equity > 0:
            max_gross_multiple = max(max_gross_multiple, utilization)
    average_utilization_pct = (
        _number(result["average_capital_utilization_pct"])
        if result.get("average_capital_utilization_pct") is not None
        else (
            statistics.fmean(exposure_values) * 100.0
            if exposure_values else None
        )
    )

    return {
        "initial_equity": initial,
        "final_equity": final,
        "net_pnl": final - initial,
        "total_return_pct": (final / initial - 1.0) * 100.0,
        "max_drawdown_amount": dd_amount,
        "max_drawdown_pct": dd_pct,
        "recovery_factor": (
            (final - initial) / dd_amount
            if dd_amount is not None and dd_amount > 0 else None
        ),
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "cagr_pct": cagr * 100.0 if cagr is not None else None,
        "calmar_ratio": calmar,
        "daily_returns": daily,
        "worst_daily_loss": worst["daily_pnl"] if worst else None,
        "worst_daily_loss_pct": worst_pct,
        "worst_daily_loss_date_utc": worst["date_utc"] if worst else None,
        "max_concurrent_positions": max_positions,
        "average_capital_utilization_pct": average_utilization_pct,
        "max_capital_utilization_pct": (
            max_utilization * 100.0
            if exposure_values or "max_capital_utilization_pct" in result
            else None
        ),
        "max_gross_exposure": max_gross,
        "max_gross_exposure_equity_multiple": max_gross_multiple,
    }


def build_grouped_trade_metrics(trades, group_fields=("asset",), max_drawdown_amount=0.0):
    """Return one trade-metric row for every observed field combination."""
    groups = defaultdict(list)
    fields = tuple(group_fields)
    for trade in trades:
        key = tuple(trade.get(field) for field in fields)
        groups[key].append(trade)
    output = []
    for key in sorted(groups, key=lambda item: tuple("" if v is None else str(v) for v in item)):
        row = {field: value for field, value in zip(fields, key)}
        row.update(summarize_trade_metrics(groups[key], max_drawdown_amount=0.0))
        output.append(row)
    return output


def build_exit_reason_breakdown(trades):
    """Summarize trade count and PnL by exit reason."""
    groups = defaultdict(list)
    for trade in trades:
        groups[str(trade.get("exit_reason") or "unknown")].append(trade)
    output = []
    for reason in sorted(groups):
        rows = groups[reason]
        output.append({
            "exit_reason": reason,
            "trade_count": len(rows),
            "gross_pnl": sum(_pnl(t, "gross_pnl") for t in rows),
            "total_fees": sum(_pnl(t, "total_fees") for t in rows),
            "funding_pnl": sum(_pnl(t, "funding_pnl") for t in rows),
            "net_pnl": sum(_pnl(t, "net_pnl") for t in rows),
        })
    return output
