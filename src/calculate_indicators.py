import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
DATA = BASE / "data"
OUT = DATA / "indicators"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

def atr(df, period=14):
    previous_close = df["close"].shift(1)

    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - previous_close).abs(),
        (df["low"] - previous_close).abs()
    ], axis=1).max(axis=1)

    return tr.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()


def rsi(series, period=14):
    change = series.diff()
    gain = change.clip(lower=0)
    loss = -change.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    rs = avg_gain / avg_loss
    result = 100 - (100 / (1 + rs))

    result = result.mask((avg_loss == 0) & (avg_gain > 0), 100)
    result = result.mask((avg_loss == 0) & (avg_gain == 0), 50)

    return result


def adx(df, period=14):
    up_move = df["high"].diff()
    down_move = -df["low"].diff()

    plus_dm = pd.Series(
        np.where((up_move > down_move) & (up_move > 0), up_move, 0),
        index=df.index
    )

    minus_dm = pd.Series(
        np.where((down_move > up_move) & (down_move > 0), down_move, 0),
        index=df.index
    )

    average_tr = atr(df, period)

    smoothed_plus = plus_dm.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    smoothed_minus = minus_dm.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    plus_di = 100 * smoothed_plus / average_tr
    minus_di = 100 * smoothed_minus / average_tr

    denominator = plus_di + minus_di
    dx = 100 * (plus_di - minus_di).abs() / denominator
    dx = dx.mask(denominator == 0)

    return dx.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()


def calculate(df, timeframe):
    df = df.copy()

    if timeframe in ("1d", "4h"):
        df["ema50"] = df["close"].ewm(
            span=50, adjust=False, min_periods=50
        ).mean()

        df["ema200"] = df["close"].ewm(
            span=200, adjust=False, min_periods=200
        ).mean()

        df["atr14"] = atr(df, 14)

    if timeframe == "4h":
        df["adx14"] = adx(df, 14)

    if timeframe == "15m":
        df["ema20"] = df["close"].ewm(
            span=20, adjust=False, min_periods=20
        ).mean()

        df["ema50"] = df["close"].ewm(
            span=50, adjust=False, min_periods=50
        ).mean()

        df["rsi14"] = rsi(df["close"], 14)

        middle = df["close"].rolling(20).mean()
        deviation = df["close"].rolling(20).std(ddof=0)

        df["bb_middle"] = middle
        df["bb_upper"] = middle + 2 * deviation
        df["bb_lower"] = middle - 2 * deviation

        df["volume_sma20"] = df["vol"].rolling(20).mean()

    return df


def main():
    print("===== INDICATOR CALCULATION =====")

    for symbol in SYMBOLS:
        for timeframe in ["1d", "4h", "15m"]:
            source = DATA / f"{symbol}_USDT_{timeframe}.csv"
            df = pd.read_csv(source)

            result = calculate(df, timeframe)

            output = OUT / f"{symbol}_USDT_{timeframe}_indicators.csv"
            result.to_csv(output, index=False)

            indicator_columns = [
                c for c in result.columns
                if c not in ["ts", "open", "high", "low", "close", "vol"]
            ]

            ready = result[indicator_columns].notna().all(axis=1).sum()

            print(
                f"{symbol:5} {timeframe:3} | "
                f"Rows: {len(result):,} | "
                f"Indicator-ready rows: {ready:,} | "
                f"Saved: {output.name}"
            )

    print("\n===== INDICATORS COMPLETE =====")
    print("Original candle files were not modified.")


if __name__ == "__main__":
    main()
