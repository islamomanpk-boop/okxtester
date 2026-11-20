import json
import math
from pathlib import Path

import pandas as pd

BASE = Path.home() / "okx_adaptive_bot"
DATA = BASE / "data" / "indicators"
REPORTS = BASE / "reports"
REPORTS.mkdir(exist_ok=True)

with open(BASE / "config.json") as f:
    base_config = json.load(f)

with open(BASE / "ema_pullback_config.json") as f:
    strategy_config = json.load(f)

SYMBOLS = base_config["symbols"]
TARGETS_R = strategy_config["targets_r"]

INITIAL_CAPITAL = float(strategy_config["initial_capital"])
RISK_PCT = float(strategy_config["risk"]["risk_per_trade_pct"]) / 100
ATR_MULTIPLE = float(strategy_config["risk"]["stop_atr_multiple"])
TAKER_FEE = float(
    strategy_config["execution_costs"]["taker_fee_pct_per_side"]
) / 100
SLIPPAGE = float(
    strategy_config["execution_costs"]["slippage_pct_per_side"]
) / 100

print("===== EMA PULLBACK V1 BACKTEST =====")
print("Mode: BACKTEST ONLY")
print("Initial capital per coin/target:", INITIAL_CAPITAL)
print("Risk per trade:", RISK_PCT * 100, "%")
print("Taker fee per side:", TAKER_FEE * 100, "%")
print("Slippage per side:", SLIPPAGE * 100, "%")
print("Funding: EXCLUDED")
print("Targets:", TARGETS_R)


def load_data(symbol):
    path15 = DATA / f"{symbol}_USDT_15m_indicators.csv"
    path4h = REPORTS / f"{symbol}_regimes.csv"

    df = pd.read_csv(path15)
    regime = pd.read_csv(path4h)

    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    regime["available_at"] = pd.to_datetime(
        regime["available_at"], utc=True
    )

    df = df.sort_values("ts").reset_index(drop=True)
    regime = regime.sort_values("available_at").reset_index(drop=True)

    previous_close = df["close"].shift(1)

    true_range = pd.concat([
        df["high"] - df["low"],
        (df["high"] - previous_close).abs(),
        (df["low"] - previous_close).abs()
    ], axis=1).max(axis=1)

    df["atr14"] = true_range.rolling(14).mean()
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
    ).reset_index(drop=True)

    if (
        merged["available_at"].notna()
        & (
            merged["available_at"]
            > merged["signal_available_at"]
        )
    ).any():
        raise RuntimeError(f"{symbol}: future regime data detected")

    return merged


def make_signal(row):
    required = [
        row["atr14"],
        row["ema20"],
        row["ema50"],
        row["open"],
        row["high"],
        row["low"],
        row["close"]
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


def close_trade(position, raw_exit, reason, timestamp, equity):
    side = position["side"]
    qty = position["qty"]

    if side == "LONG":
        exit_fill = raw_exit * (1 - SLIPPAGE)
        gross_pnl = (exit_fill - position["entry_fill"]) * qty
    else:
        exit_fill = raw_exit * (1 + SLIPPAGE)
        gross_pnl = (position["entry_fill"] - exit_fill) * qty

    exit_fee = abs(exit_fill * qty) * TAKER_FEE
    total_fees = position["entry_fee"] + exit_fee
    net_pnl = gross_pnl - total_fees
    new_equity = equity + net_pnl

    trade = {
        "symbol": position["symbol"],
        "target_r": position["target_r"],
        "side": side,
        "entry_time": position["entry_time"],
        "exit_time": timestamp,
        "entry_price": position["entry_fill"],
        "exit_price": exit_fill,
        "stop_price": position["stop"],
        "target_price": position["target"],
        "quantity": qty,
        "exit_reason": reason,
        "gross_pnl": gross_pnl,
        "entry_fee": position["entry_fee"],
        "exit_fee": exit_fee,
        "total_fees": total_fees,
        "net_pnl": net_pnl,
        "equity_after_trade": new_equity
    }

    return trade, new_equity


def run_backtest(df, symbol, target_r):
    equity = INITIAL_CAPITAL
    position = None
    trades = []
    equity_curve = [INITIAL_CAPITAL]

    for i in range(1, len(df)):
        row = df.iloc[i]
        raw_open = float(row["open"])
        raw_high = float(row["high"])
        raw_low = float(row["low"])
        raw_close = float(row["close"])
        timestamp = row["ts"]

        closed_this_bar = False

        # 1. Manage a position that was already open.
        if position is not None:
            side = position["side"]
            stop = position["stop"]
            target = position["target"]

            if side == "LONG":
                if raw_open <= stop:
                    raw_exit = raw_open
                    reason = "STOP_GAP"
                elif raw_open >= target:
                    raw_exit = raw_open
                    reason = "TARGET_GAP"
                elif raw_low <= stop:
                    raw_exit = stop
                    reason = "STOP"
                elif raw_high >= target:
                    raw_exit = target
                    reason = "TARGET"
                else:
                    raw_exit = None
                    reason = None
            else:
                if raw_open >= stop:
                    raw_exit = raw_open
                    reason = "STOP_GAP"
                elif raw_open <= target:
                    raw_exit = raw_open
                    reason = "TARGET_GAP"
                elif raw_high >= stop:
                    raw_exit = stop
                    reason = "STOP"
                elif raw_low <= target:
                    raw_exit = target
                    reason = "TARGET"
                else:
                    raw_exit = None
                    reason = None

            if raw_exit is not None:
                trade, equity = close_trade(
                    position, raw_exit, reason, timestamp, equity
                )
                trades.append(trade)
                equity_curve.append(equity)
                position = None
                closed_this_bar = True

        # 2. If flat, consider the signal from the previous candle.
        # Do not re-enter on a candle where another trade just closed.
        if position is None and not closed_this_bar:
            signal_row = df.iloc[i - 1]
            signal = make_signal(signal_row)

            if signal is not None:
                side = signal["side"]
                stop = signal["stop"]

                if side == "LONG":
                    entry_fill = raw_open * (1 + SLIPPAGE)
                    valid_stop = stop < raw_open and stop < entry_fill
                else:
                    entry_fill = raw_open * (1 - SLIPPAGE)
                    valid_stop = stop > raw_open and stop > entry_fill

                if valid_stop and equity > 0:
                    risk_cash = equity * RISK_PCT
                    stop_distance = abs(entry_fill - stop)

                    if stop_distance > 0 and math.isfinite(stop_distance):
                        qty = risk_cash / stop_distance
                        entry_fee = abs(entry_fill * qty) * TAKER_FEE

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
                            "entry_fee": entry_fee
                        }

                        # 3. Check stop/target on the entry candle too.
                        if side == "LONG":
                            if raw_low <= stop:
                                raw_exit = stop
                                reason = "STOP"
                            elif raw_high >= target:
                                raw_exit = target
                                reason = "TARGET"
                            else:
                                raw_exit = None
                                reason = None
                        else:
                            if raw_high >= stop:
                                raw_exit = stop
                                reason = "STOP"
                            elif raw_low <= target:
                                raw_exit = target
                                reason = "TARGET"
                            else:
                                raw_exit = None
                                reason = None

                        if raw_exit is not None:
                            trade, equity = close_trade(
                                position, raw_exit, reason, timestamp, equity
                            )
                            trades.append(trade)
                            equity_curve.append(equity)
                            position = None

    # 4. Close any remaining position at the final candle close.
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

    return trades, equity_curve, equity


def calculate_metrics(trades, equity_curve, ending_equity):
    if not trades:
        return {
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate_pct": 0.0,
            "net_pnl": 0.0,
            "return_pct": 0.0,
            "profit_factor": None,
            "max_drawdown_pct": 0.0,
            "expectancy": 0.0,
            "average_win": 0.0,
            "average_loss": 0.0,
            "total_fees": 0.0,
            "ending_equity": ending_equity,
            "max_consecutive_losses": 0
        }

    results = [t["net_pnl"] for t in trades]
    wins = [x for x in results if x > 0]
    losses = [x for x in results if x < 0]

    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))

    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    elif gross_profit > 0:
        profit_factor = None
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
        "win_rate_pct": len(wins) / len(trades) * 100,
        "net_pnl": net_pnl,
        "return_pct": net_pnl / INITIAL_CAPITAL * 100,
        "profit_factor": profit_factor,
        "max_drawdown_pct": max_dd,
        "expectancy": sum(results) / len(results),
        "average_win": sum(wins) / len(wins) if wins else 0.0,
        "average_loss": sum(losses) / len(losses) if losses else 0.0,
        "total_fees": sum(t["total_fees"] for t in trades),
        "ending_equity": ending_equity,
        "max_consecutive_losses": max_streak
    }


summary_rows = []

for symbol in SYMBOLS:
    print(f"\nLoading {symbol} data...")
    df = load_data(symbol)

    print(f"{symbol}: {len(df)} candles")

    for target_r in TARGETS_R:
        print(f"Running {symbol} at {target_r}R...")

        trades, equity_curve, ending_equity = run_backtest(
            df, symbol, float(target_r)
        )

        metrics = calculate_metrics(
            trades, equity_curve, ending_equity
        )

        metrics["symbol"] = symbol
        metrics["target_r"] = float(target_r)
        metrics["funding_included"] = False
        summary_rows.append(metrics)

        trade_path = REPORTS / (
            f"{symbol}_EMA_PULLBACK_{target_r}R_trades.csv"
        )
        pd.DataFrame(trades).to_csv(trade_path, index=False)

        print(
            f"  Trades: {metrics['trades']} | "
            f"Net PnL: {metrics['net_pnl']:.2f} | "
            f"Return: {metrics['return_pct']:.2f}% | "
            f"Max DD: {metrics['max_drawdown_pct']:.2f}%"
        )

summary = pd.DataFrame(summary_rows)

columns = [
    "symbol", "target_r", "trades", "wins", "losses",
    "win_rate_pct", "net_pnl", "return_pct", "profit_factor",
    "max_drawdown_pct", "expectancy", "average_win",
    "average_loss", "total_fees", "ending_equity",
    "max_consecutive_losses", "funding_included"
]

summary = summary[columns]
summary_path = REPORTS / "ema_pullback_v1_summary.csv"
summary.to_csv(summary_path, index=False)

print("\n===== FINAL SUMMARY =====")
print(summary.to_string(index=False))

print("\nSummary saved to:")
print(summary_path)

print("\nIndividual trade files saved in:")
print(REPORTS)

print("\nIMPORTANT:")
print("- Each coin/target test starts with its own $1,000.")
print("- Funding is excluded.")
print("- Fees and slippage are estimates from the config.")
print("- This is a historical research test, not a live trading signal.")
