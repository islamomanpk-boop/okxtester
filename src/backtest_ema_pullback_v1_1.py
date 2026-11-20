import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path.home() / "okx_adaptive_bot"
DATA = BASE / "data" / "indicators"
REPORTS = BASE / "reports"
REPORTS.mkdir(exist_ok=True)

with open(BASE / "config.json") as f:
    base_config = json.load(f)

with open(BASE / "ema_pullback_config.json") as f:
    cfg = json.load(f)

SYMBOLS = base_config["symbols"]
TARGETS_R = [float(x) for x in cfg["targets_r"]]

INITIAL_CAPITAL = float(cfg["initial_capital"])
RISK_PCT = float(cfg["risk"]["risk_per_trade_pct"]) / 100
ATR_MULTIPLE = float(cfg["risk"]["stop_atr_multiple"])

FEE = float(
    cfg["execution_costs"]["taker_fee_pct_per_side"]
) / 100

SLIPPAGE = float(
    cfg["execution_costs"]["slippage_pct_per_side"]
) / 100

MAX_LEVERAGE = 3.0

ALLOWED_REGIMES = {
    "WARMUP", "TRANSITION", "SIDEWAYS",
    "BULLISH", "BEARISH"
}

print("===== EMA PULLBACK V1.1 =====")
print("Mode: BACKTEST ONLY")
print("Initial capital per test:", INITIAL_CAPITAL)
print("Risk per trade:", RISK_PCT * 100, "%")
print("Maximum notional leverage:", MAX_LEVERAGE, "x")
print("Taker fee per side:", FEE * 100, "%")
print("Slippage per side:", SLIPPAGE * 100, "%")
print("Funding: EXCLUDED")
print("Targets:", TARGETS_R)


def load_data(symbol):
    path15 = DATA / f"{symbol}_USDT_15m_indicators.csv"
    path4h = REPORTS / f"{symbol}_regimes.csv"

    if not path15.exists():
        raise FileNotFoundError(path15)

    if not path4h.exists():
        raise FileNotFoundError(path4h)

    df = pd.read_csv(path15)
    regime = pd.read_csv(path4h)

    required = {
        "ts", "open", "high", "low", "close",
        "ema20", "ema50"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{symbol}: missing 15M columns {missing}")

    if not {"available_at", "regime"}.issubset(regime.columns):
        raise ValueError(f"{symbol}: missing regime columns")

    # Explicitly require millisecond epoch timestamps.
    ts_numeric = pd.to_numeric(df["ts"], errors="coerce")

    if ts_numeric.isna().any():
        raise ValueError(f"{symbol}: invalid 15M timestamps")

    if not ts_numeric.between(1e11, 1e14).all():
        raise ValueError(
            f"{symbol}: timestamps are not valid millisecond epochs"
        )

    df["ts"] = pd.to_datetime(
        ts_numeric, unit="ms", utc=True, errors="raise"
    )

    regime["available_at"] = pd.to_datetime(
        regime["available_at"], utc=True, errors="coerce"
    )

    if regime["available_at"].isna().any():
        raise ValueError(f"{symbol}: invalid regime timestamps")

    if not regime["regime"].isin(ALLOWED_REGIMES).all():
        bad = regime.loc[
            ~regime["regime"].isin(ALLOWED_REGIMES), "regime"
        ].unique()

        raise ValueError(
            f"{symbol}: unexpected regime labels: {bad}"
        )

    df = df.sort_values("ts").reset_index(drop=True)
    regime = regime.sort_values(
        "available_at"
    ).reset_index(drop=True)

    if df["ts"].duplicated().any():
        raise ValueError(f"{symbol}: duplicate 15M timestamps")

    if regime["available_at"].duplicated().any():
        raise ValueError(f"{symbol}: duplicate regime availability times")

    # Validate OHLC data before any execution.
    ohlc = df[["open", "high", "low", "close"]].apply(
        pd.to_numeric, errors="coerce"
    )

    if not np.isfinite(ohlc.to_numpy(dtype=float)).all():
        raise ValueError(f"{symbol}: missing or non-finite OHLC values")

    if (ohlc <= 0).any().any():
        raise ValueError(f"{symbol}: non-positive OHLC values")

    invalid = (
        (ohlc["high"] < ohlc["low"])
        | (ohlc["high"] < ohlc["open"])
        | (ohlc["high"] < ohlc["close"])
        | (ohlc["low"] > ohlc["open"])
        | (ohlc["low"] > ohlc["close"])
    )

    if invalid.any():
        raise ValueError(
            f"{symbol}: invalid OHLC candles: {int(invalid.sum())}"
        )

    for col in ["open", "high", "low", "close"]:
        df[col] = ohlc[col]

    # ATR14 calculated from completed 15M candles.
    previous_close = df["close"].shift(1)

    true_range = pd.concat([
        df["high"] - df["low"],
        (df["high"] - previous_close).abs(),
        (df["low"] - previous_close).abs()
    ], axis=1).max(axis=1)

    df["atr14"] = true_range.rolling(14).mean()

    # A 15M signal is available only after its candle closes.
    df["signal_available_at"] = (
        df["ts"] + pd.Timedelta(minutes=15)
    )

    merged = pd.merge_asof(
        df.sort_values("signal_available_at"),
        regime[["available_at", "regime"]].sort_values(
            "available_at"
        ),
        left_on="signal_available_at",
        right_on="available_at",
        direction="backward"
    )

    # Explicit chronological sort after merge.
    merged = merged.sort_values("ts").reset_index(drop=True)

    matched = merged["available_at"].notna()

    future_match = (
        matched
        & (
            merged["available_at"]
            > merged["signal_available_at"]
        )
    )

    if future_match.any():
        raise RuntimeError(
            f"{symbol}: future regime match detected"
        )

    return merged


def make_signal(row):
    required = [
        row["atr14"], row["ema20"], row["ema50"],
        row["open"], row["high"], row["low"], row["close"]
    ]

    if any(pd.isna(x) for x in required):
        return None

    if row["regime"] == "BULLISH":
        if (
            row["ema20"] > row["ema50"]
            and row["low"] <= row["ema20"]
            and row["close"] > row["ema20"]
            and row["close"] > row["open"]
        ):
            stop = min(
                row["low"],
                row["close"] - ATR_MULTIPLE * row["atr14"]
            )

            return {"side": "LONG", "stop": float(stop)}

    if row["regime"] == "BEARISH":
        if (
            row["ema20"] < row["ema50"]
            and row["high"] >= row["ema20"]
            and row["close"] < row["ema20"]
            and row["close"] < row["open"]
        ):
            stop = max(
                row["high"],
                row["close"] + ATR_MULTIPLE * row["atr14"]
            )

            return {"side": "SHORT", "stop": float(stop)}

    return None


def mark_to_market(position, adverse_price, equity):
    """Conservative estimated liquidation value at adverse bar extreme."""

    if position["side"] == "LONG":
        exit_fill = adverse_price * (1 - SLIPPAGE)
        unrealized = (
            exit_fill - position["entry_fill"]
        ) * position["qty"]
    else:
        exit_fill = adverse_price * (1 + SLIPPAGE)
        unrealized = (
            position["entry_fill"] - exit_fill
        ) * position["qty"]

    estimated_exit_fee = abs(
        exit_fill * position["qty"]
    ) * FEE

    return (
        equity
        + unrealized
        - position["entry_fee"]
        - estimated_exit_fee
    )


def close_trade(position, raw_exit, reason, timestamp, equity):
    if position["side"] == "LONG":
        exit_fill = raw_exit * (1 - SLIPPAGE)
        gross_pnl = (
            exit_fill - position["entry_fill"]
        ) * position["qty"]
    else:
        exit_fill = raw_exit * (1 + SLIPPAGE)
        gross_pnl = (
            position["entry_fill"] - exit_fill
        ) * position["qty"]

    exit_fee = abs(exit_fill * position["qty"]) * FEE
    total_fees = position["entry_fee"] + exit_fee
    net_pnl = gross_pnl - total_fees
    new_equity = equity + net_pnl

    trade = {
        "symbol": position["symbol"],
        "target_r": position["target_r"],
        "side": position["side"],
        "entry_time": position["entry_time"],
        "exit_time": timestamp,
        "entry_price": position["entry_fill"],
        "exit_price": exit_fill,
        "stop_price": position["stop"],
        "target_price": position["target"],
        "quantity": position["qty"],
        "notional": position["notional"],
        "effective_leverage": position["effective_leverage"],
        "planned_risk_cash": position["planned_risk_cash"],
        "actual_price_risk_cash": position["actual_price_risk_cash"],
        "exit_reason": reason,
        "gross_pnl": gross_pnl,
        "entry_fee": position["entry_fee"],
        "exit_fee": exit_fee,
        "total_fees": total_fees,
        "net_pnl": net_pnl,
        "equity_after_trade": new_equity
    }

    return trade, new_equity


def get_exit(position, raw_open, raw_high, raw_low):
    """Stop-first execution, including opening gaps."""

    stop = position["stop"]
    target = position["target"]

    if position["side"] == "LONG":
        if raw_open <= stop:
            return raw_open, "STOP_GAP"
        if raw_open >= target:
            return raw_open, "TARGET_GAP"
        if raw_low <= stop:
            return stop, "STOP"
        if raw_high >= target:
            return target, "TARGET"

    else:
        if raw_open >= stop:
            return raw_open, "STOP_GAP"
        if raw_open <= target:
            return raw_open, "TARGET_GAP"
        if raw_high >= stop:
            return stop, "STOP"
        if raw_low <= target:
            return target, "TARGET"

    return None, None


def run_backtest(df, symbol, target_r):
    equity = INITIAL_CAPITAL
    position = None
    trades = []

    # Contains realized equity and conservative open-trade marks.
    equity_curve = [INITIAL_CAPITAL]

    skipped_invalid_stop = 0
    capped_positions = 0

    for i in range(1, len(df)):
        row = df.iloc[i]

        # Explicit execution-bar data safety check.
        values = [
            row["open"], row["high"], row["low"], row["close"]
        ]

        if any(not np.isfinite(float(x)) for x in values):
            raise ValueError(
                f"{symbol}: invalid execution OHLC at row {i}"
            )

        raw_open = float(row["open"])
        raw_high = float(row["high"])
        raw_low = float(row["low"])
        raw_close = float(row["close"])
        timestamp = row["ts"]

        closed_this_bar = False

        # 1. Manage a position already open before this candle.
        if position is not None:
            adverse_price = (
                raw_low if position["side"] == "LONG"
                else raw_high
            )

            # Capture the adverse excursion even if the trade later wins.
            equity_curve.append(
                mark_to_market(position, adverse_price, equity)
            )

            raw_exit, reason = get_exit(
                position, raw_open, raw_high, raw_low
            )

            if raw_exit is not None:
                trade, equity = close_trade(
                    position, raw_exit, reason, timestamp, equity
                )

                trades.append(trade)
                equity_curve.append(equity)
                position = None
                closed_this_bar = True
            else:
                # Also record the candle close valuation.
                equity_curve.append(
                    mark_to_market(position, raw_close, equity)
                )

        # 2. If flat, consider the previous completed candle's signal.
        if position is None and not closed_this_bar:
            signal = make_signal(df.iloc[i - 1])

            if signal is not None:
                side = signal["side"]
                stop = signal["stop"]

                if side == "LONG":
                    entry_fill = raw_open * (1 + SLIPPAGE)
                    valid_stop = stop < raw_open and stop < entry_fill
                else:
                    entry_fill = raw_open * (1 - SLIPPAGE)
                    valid_stop = stop > raw_open and stop > entry_fill

                if not valid_stop:
                    skipped_invalid_stop += 1

                elif equity > 0:
                    stop_distance = abs(entry_fill - stop)

                    if stop_distance > 0 and math.isfinite(stop_distance):
                        planned_risk = equity * RISK_PCT
                        uncapped_qty = planned_risk / stop_distance

                        # Maximum 3x notional exposure.
                        max_notional = equity * MAX_LEVERAGE
                        max_qty = max_notional / entry_fill

                        qty = min(uncapped_qty, max_qty)

                        if qty < uncapped_qty:
                            capped_positions += 1

                        notional = qty * entry_fill
                        actual_price_risk = qty * stop_distance
                        effective_leverage = notional / equity

                        entry_fee = notional * FEE

                        if side == "LONG":
                            target = entry_fill + stop_distance * target_r
                        else:
                            target = entry_fill - stop_distance * target_r

                        position = {
                            "symbol": symbol,
                            "target_r": target_r,
                            "side": side,
                            "entry_time": timestamp,
                            "entry_fill": entry_fill,
                            "stop": stop,
                            "target": target,
                            "qty": qty,
                            "notional": notional,
                            "effective_leverage": effective_leverage,
                            "planned_risk_cash": planned_risk,
                            "actual_price_risk_cash": actual_price_risk,
                            "entry_fee": entry_fee
                        }

                        # Include adverse movement on the entry candle.
                        adverse_price = (
                            raw_low if side == "LONG" else raw_high
                        )

                        equity_curve.append(
                            mark_to_market(position, adverse_price, equity)
                        )

                        # Entry candle is also checked for stop/target.
                        raw_exit, reason = get_exit(
                            position, raw_open, raw_high, raw_low
                        )

                        if raw_exit is not None:
                            trade, equity = close_trade(
                                position, raw_exit, reason, timestamp, equity
                            )

                            trades.append(trade)
                            equity_curve.append(equity)
                            position = None
                        else:
                            equity_curve.append(
                                mark_to_market(position, raw_close, equity)
                            )

        if position is None and not closed_this_bar:
            # Keep the curve updated during flat periods.
            equity_curve.append(equity)

    # 3. Close any remaining position at the end of the dataset.
    if position is not None:
        final_row = df.iloc[-1]

        trade, equity = close_trade(
            position,
            float(final_row["close"]),
            "END_OF_DATA",
            final_row["ts"] + pd.Timedelta(minutes=15),
            equity
        )

        trades.append(trade)
        equity_curve.append(equity)
        position = None

    return (
        trades,
        equity_curve,
        equity,
        skipped_invalid_stop,
        capped_positions
    )


def calculate_metrics(
    trades, equity_curve, ending_equity,
    skipped_invalid_stop, capped_positions
):
    results = [t["net_pnl"] for t in trades]
    wins = [x for x in results if x > 0]
    losses = [x for x in results if x < 0]

    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))

    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    elif gross_profit > 0:
        profit_factor = float("inf")
    else:
        profit_factor = 0.0

    peak = INITIAL_CAPITAL
    max_dd = 0.0

    for value in equity_curve:
        peak = max(peak, value)

        if peak > 0:
            drawdown = (peak - value) / peak * 100
            max_dd = max(max_dd, drawdown)

    max_streak = 0
    streak = 0

    for value in results:
        if value < 0:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0

    net_pnl = ending_equity - INITIAL_CAPITAL

    return {
        "trades": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": (
            len(wins) / len(trades) * 100 if trades else 0.0
        ),
        "net_pnl": net_pnl,
        "return_pct": net_pnl / INITIAL_CAPITAL * 100,
        "profit_factor": profit_factor,
        "max_drawdown_pct": max_dd,
        "expectancy": (
            sum(results) / len(results) if results else 0.0
        ),
        "average_win": (
            sum(wins) / len(wins) if wins else 0.0
        ),
        "average_loss": (
            sum(losses) / len(losses) if losses else 0.0
        ),
        "total_fees": sum(
            t["total_fees"] for t in trades
        ),
        "ending_equity": ending_equity,
        "max_consecutive_losses": max_streak,
        "max_effective_leverage": max(
            (t["effective_leverage"] for t in trades),
            default=0.0
        ),
        "max_notional": max(
            (t["notional"] for t in trades),
            default=0.0
        ),
        "capped_positions": capped_positions,
        "skipped_invalid_stop": skipped_invalid_stop
    }


summary_rows = []

for symbol in SYMBOLS:
    print(f"\nLoading {symbol}...")

    df = load_data(symbol)
    print(f"{symbol}: {len(df)} candles | Data validation passed")

    for target_r in TARGETS_R:
        print(f"Running {symbol} at {target_r}R...")

        (
            trades,
            equity_curve,
            ending_equity,
            skipped_invalid_stop,
            capped_positions
        ) = run_backtest(df, symbol, target_r)

        metrics = calculate_metrics(
            trades,
            equity_curve,
            ending_equity,
            skipped_invalid_stop,
            capped_positions
        )

        metrics["symbol"] = symbol
        metrics["target_r"] = target_r
        metrics["funding_included"] = False
        metrics["max_leverage_limit"] = MAX_LEVERAGE

        summary_rows.append(metrics)

        trade_path = REPORTS / (
            f"{symbol}_EMA_PULLBACK_V1_1_{target_r}R_trades.csv"
        )

        pd.DataFrame(trades).to_csv(trade_path, index=False)

        print(
            f"  Trades: {metrics['trades']} | "
            f"Net PnL: {metrics['net_pnl']:.2f} | "
            f"Return: {metrics['return_pct']:.2f}% | "
            f"MTM Max DD: {metrics['max_drawdown_pct']:.2f}% | "
            f"PF: {metrics['profit_factor']}"
        )

summary = pd.DataFrame(summary_rows)

columns = [
    "symbol", "target_r", "trades", "wins", "losses",
    "win_rate_pct", "net_pnl", "return_pct",
    "profit_factor", "max_drawdown_pct", "expectancy",
    "average_win", "average_loss", "total_fees",
    "ending_equity", "max_consecutive_losses",
    "max_effective_leverage", "max_notional",
    "capped_positions", "skipped_invalid_stop",
    "max_leverage_limit", "funding_included"
]

summary = summary[columns]

summary_path = REPORTS / "ema_pullback_v1_1_summary.csv"
summary.to_csv(summary_path, index=False)

print("\n===== V1.1 FINAL SUMMARY =====")
print(summary.to_string(index=False))

print("\nSummary saved:", summary_path)
print("Trade files saved in:", REPORTS)

print("\nIMPORTANT LIMITATIONS:")
print("- Each coin/target starts with an independent $1,000.")
print("- Maximum position notional is capped at 3x current equity.")
print("- Drawdown uses conservative bar-extreme mark-to-market estimates.")
print("- Intrabar price path is unknown; adverse extremes may overstate DD.")
print("- This is not a liquidation or exchange margin simulator.")
print("- Funding is excluded.")
print("- Fees and slippage are assumptions from the config.")
print("- Research only; no live orders.")
