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

# None means unlimited holding time.
HOLDING_LIMITS_HOURS = [None, 6, 12, 24, 48]

ALLOWED_REGIMES = {
    "WARMUP", "TRANSITION", "SIDEWAYS",
    "BULLISH", "BEARISH"
}

BAR_DURATION = pd.Timedelta(minutes=15)

print("===== EMA PULLBACK V1.1 AUDITED EXPERIMENT =====")
print("Mode: BACKTEST ONLY")
print("Initial capital per independent test:", INITIAL_CAPITAL)
print("Risk per trade:", RISK_PCT * 100, "%")
print("Maximum notional leverage:", MAX_LEVERAGE, "x")
print("Taker fee per side:", FEE * 100, "%")
print("Slippage per side:", SLIPPAGE * 100, "%")
print("Funding: EXCLUDED")
print("Targets:", TARGETS_R)
print("Holding limits:", HOLDING_LIMITS_HOURS)


def holding_label(hours):
    return "UNLIMITED" if hours is None else f"{hours}H"


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
        raise ValueError(
            f"{symbol}: duplicate regime availability times"
        )

    # Check that the execution candles are continuous.
    gaps = df["ts"].diff().dropna()

    if not gaps.eq(BAR_DURATION).all():
        bad_gaps = int((gaps != BAR_DURATION).sum())
        raise ValueError(
            f"{symbol}: {bad_gaps} unexpected 15M timestamp gaps"
        )

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

    previous_close = df["close"].shift(1)

    true_range = pd.concat([
        df["high"] - df["low"],
        (df["high"] - previous_close).abs(),
        (df["low"] - previous_close).abs()
    ], axis=1).max(axis=1)

    df["atr14"] = true_range.rolling(14).mean()

    # A signal is available only when its 15M candle has closed.
    df["signal_available_at"] = df["ts"] + BAR_DURATION

    merged = pd.merge_asof(
        df.sort_values("signal_available_at"),
        regime[["available_at", "regime"]].sort_values(
            "available_at"
        ),
        left_on="signal_available_at",
        right_on="available_at",
        direction="backward"
    )

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


def mark_to_market(position, mark_price, equity):
    if position["side"] == "LONG":
        exit_fill = mark_price * (1 - SLIPPAGE)
        unrealized = (
            exit_fill - position["entry_fill"]
        ) * position["qty"]
    else:
        exit_fill = mark_price * (1 + SLIPPAGE)
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


def close_trade(
    position,
    raw_exit,
    reason,
    exit_time,
    exit_time_type,
    equity
):
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

    holding_minutes = (
        exit_time - position["entry_time"]
    ).total_seconds() / 60

    trade = {
        "symbol": position["symbol"],
        "target_r": position["target_r"],
        "max_hold_hours": position["max_hold_hours"],
        "side": position["side"],
        "entry_time": position["entry_time"],
        "exit_time": exit_time,
        "exit_time_type": exit_time_type,
        "holding_minutes": holding_minutes,
        "holding_hours": holding_minutes / 60,
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


def get_exit(
    position,
    raw_open,
    raw_high,
    raw_low,
    candle_time,
    max_hold_hours
):
    """
    Priority:
    1. Opening gap through stop or target.
    2. Time stop at the candle open.
    3. Intrabar stop/target, with stop-first ambiguity handling.

    Intrabar exits are timestamped at candle close because exact
    event time cannot be known from 15M OHLC data.
    """

    stop = position["stop"]
    target = position["target"]

    if position["side"] == "LONG":
        if raw_open <= stop:
            return raw_open, "STOP_GAP", "OPEN"

        if raw_open >= target:
            return raw_open, "TARGET_GAP", "OPEN"

    else:
        if raw_open >= stop:
            return raw_open, "STOP_GAP", "OPEN"

        if raw_open <= target:
            return raw_open, "TARGET_GAP", "OPEN"

    # Time stop is checked at the first available candle open
    # at or after the holding deadline.
    if max_hold_hours is not None:
        deadline = (
            position["entry_time"]
            + pd.Timedelta(hours=max_hold_hours)
        )

        if candle_time >= deadline:
            return raw_open, "TIME_STOP", "OPEN"

    if position["side"] == "LONG":
        if raw_low <= stop:
            return stop, "STOP", "INTRABAR"

        if raw_high >= target:
            return target, "TARGET", "INTRABAR"

    else:
        if raw_high >= stop:
            return stop, "STOP", "INTRABAR"

        if raw_low <= target:
            return target, "TARGET", "INTRABAR"

    return None, None, None


def run_backtest(df, symbol, target_r, max_hold_hours):
    equity = INITIAL_CAPITAL
    position = None
    trades = []

    equity_curve = [INITIAL_CAPITAL]

    skipped_invalid_stop = 0
    capped_positions = 0

    for i in range(1, len(df)):
        row = df.iloc[i]

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
        candle_close_time = timestamp + BAR_DURATION

        closed_this_bar = False

        # 1. Manage an existing position.
        if position is not None:
            raw_exit, reason, timing = get_exit(
                position,
                raw_open,
                raw_high,
                raw_low,
                timestamp,
                max_hold_hours
            )

            if raw_exit is not None:
                # Opening exits are valued at the open.
                # Intrabar exits use the adverse bar extreme
                # for conservative drawdown measurement.
                if timing == "OPEN":
                    mark_price = raw_open
                    exit_time = timestamp
                else:
                    mark_price = (
                        raw_low if position["side"] == "LONG"
                        else raw_high
                    )
                    exit_time = candle_close_time

                equity_curve.append(
                    mark_to_market(position, mark_price, equity)
                )

                trade, equity = close_trade(
                    position,
                    raw_exit,
                    reason,
                    exit_time,
                    timing,
                    equity
                )

                trades.append(trade)
                equity_curve.append(equity)
                position = None
                closed_this_bar = True

            else:
                adverse_price = (
                    raw_low if position["side"] == "LONG"
                    else raw_high
                )

                equity_curve.append(
                    mark_to_market(position, adverse_price, equity)
                )

                equity_curve.append(
                    mark_to_market(position, raw_close, equity)
                )

        # 2. If flat, consider the previous completed candle signal.
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
                            target = (
                                entry_fill + stop_distance * target_r
                            )
                        else:
                            target = (
                                entry_fill - stop_distance * target_r
                            )

                        position = {
                            "symbol": symbol,
                            "target_r": target_r,
                            "max_hold_hours": max_hold_hours,
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

                        # Check the entry candle too.
                        raw_exit, reason, timing = get_exit(
                            position,
                            raw_open,
                            raw_high,
                            raw_low,
                            timestamp,
                            None
                        )

                        if raw_exit is not None:
                            mark_price = (
                                raw_low if side == "LONG" else raw_high
                            )

                            equity_curve.append(
                                mark_to_market(
                                    position, mark_price, equity
                                )
                            )

                            exit_time = candle_close_time

                            trade, equity = close_trade(
                                position,
                                raw_exit,
                                reason,
                                exit_time,
                                "INTRABAR",
                                equity
                            )

                            trades.append(trade)
                            equity_curve.append(equity)
                            position = None

                        else:
                            adverse_price = (
                                raw_low if side == "LONG" else raw_high
                            )

                            equity_curve.append(
                                mark_to_market(
                                    position, adverse_price, equity
                                )
                            )

                            equity_curve.append(
                                mark_to_market(
                                    position, raw_close, equity
                                )
                            )

        if position is None and not closed_this_bar:
            equity_curve.append(equity)

    # 3. Close any remaining position at the final candle close.
    if position is not None:
        final_row = df.iloc[-1]
        final_close_time = final_row["ts"] + BAR_DURATION

        trade, equity = close_trade(
            position,
            float(final_row["close"]),
            "END_OF_DATA",
            final_close_time,
            "CANDLE_CLOSE",
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
    trades,
    equity_curve,
    ending_equity,
    skipped_invalid_stop,
    capped_positions,
    max_hold_hours
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

    durations = [t["holding_hours"] for t in trades]
    time_stop_count = sum(
        t["exit_reason"] == "TIME_STOP" for t in trades
    )

    over_24h = sum(x > 24 for x in durations)

    return {
        "symbol": None,
        "target_r": None,
        "max_hold_hours": (
            "UNLIMITED" if max_hold_hours is None else max_hold_hours
        ),
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
        "total_fees": sum(t["total_fees"] for t in trades),
        "ending_equity": ending_equity,
        "max_consecutive_losses": max_streak,
        "average_holding_hours": (
            float(np.mean(durations)) if durations else 0.0
        ),
        "median_holding_hours": (
            float(np.median(durations)) if durations else 0.0
        ),
        "max_holding_hours_observed": (
            max(durations) if durations else 0.0
        ),
        "trades_over_24h": over_24h,
        "time_stop_count": time_stop_count,
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
    print(f"{symbol}: {len(df)} candles | Validation passed")

    for target_r in TARGETS_R:
        for max_hold_hours in HOLDING_LIMITS_HOURS:
            label = holding_label(max_hold_hours)

            print(
                f"Running {symbol} | {target_r}R | {label}..."
            )

            (
                trades,
                equity_curve,
                ending_equity,
                skipped_invalid_stop,
                capped_positions
            ) = run_backtest(
                df,
                symbol,
                target_r,
                max_hold_hours
            )

            metrics = calculate_metrics(
                trades,
                equity_curve,
                ending_equity,
                skipped_invalid_stop,
                capped_positions,
                max_hold_hours
            )

            metrics["symbol"] = symbol
            metrics["target_r"] = target_r
            metrics["funding_included"] = False
            metrics["max_leverage_limit"] = MAX_LEVERAGE

            summary_rows.append(metrics)

            trade_path = REPORTS / (
                f"{symbol}_EMA_PULLBACK_V1_1_"
                f"{target_r}R_{label}_audited_trades.csv"
            )

            pd.DataFrame(trades).to_csv(
                trade_path,
                index=False
            )

            print(
                f"  Trades: {metrics['trades']} | "
                f"Net PnL: {metrics['net_pnl']:.2f} | "
                f"Win rate: {metrics['win_rate_pct']:.2f}% | "
                f"PF: {metrics['profit_factor']} | "
                f"Max DD: {metrics['max_drawdown_pct']:.2f}% | "
                f"Avg hold: {metrics['average_holding_hours']:.2f}h | "
                f"Time stops: {metrics['time_stop_count']}"
            )


summary = pd.DataFrame(summary_rows)

columns = [
    "symbol",
    "target_r",
    "max_hold_hours",
    "trades",
    "wins",
    "losses",
    "win_rate_pct",
    "net_pnl",
    "return_pct",
    "profit_factor",
    "max_drawdown_pct",
    "expectancy",
    "average_win",
    "average_loss",
    "total_fees",
    "ending_equity",
    "max_consecutive_losses",
    "average_holding_hours",
    "median_holding_hours",
    "max_holding_hours_observed",
    "trades_over_24h",
    "time_stop_count",
    "max_effective_leverage",
    "max_notional",
    "capped_positions",
    "skipped_invalid_stop",
    "max_leverage_limit",
    "funding_included"
]

summary = summary[columns]

summary_path = (
    REPORTS / "ema_pullback_v1_1_holding_period_experiment.csv"
)

summary.to_csv(summary_path, index=False)

print("\n===== HOLDING PERIOD EXPERIMENT COMPLETE =====")
print(summary.to_string(index=False))

print("\nSummary saved:", summary_path)
print("Audited trade files saved in:", REPORTS)

print("\nIMPORTANT LIMITATIONS:")
print("- Each symbol/target/holding test starts with independent $1,000.")
print("- Maximum position notional is capped at 3x current equity.")
print("- Funding remains excluded.")
print("- Fees and slippage use the existing config assumptions.")
print("- Intrabar exit timestamps represent candle close, not exact event time.")
print("- Opening-gap and time-stop exits use the candle open.")
print("- Time stops execute at the first available 15M open at or after expiry.")
print("- Same-candle stop/target ambiguity is resolved stop-first.")
print("- This is not an exchange liquidation or margin simulator.")
print("- Research only; no live orders.")
