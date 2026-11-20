import pandas as pd
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
DATA_DIR = BASE / "data"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

TIMEFRAMES = {
    "15m": "15min",
    "4h": "4h",
    "1d": "24h",
}

REQUIRED = ["ts", "open", "high", "low", "close", "vol"]


def load_data(symbol):
    path = DATA_DIR / f"{symbol}_USDT_USDT_1m.csv"

    if not path.is_file():
        raise FileNotFoundError(f"Missing data file: {path}")

    df = pd.read_csv(path)

    if list(df.columns) != REQUIRED:
        raise ValueError(
            f"Unexpected columns in {path.name}: {list(df.columns)}"
        )

    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)

    for col in ["open", "high", "low", "close", "vol"]:
        df[col] = pd.to_numeric(df[col], errors="raise")

    if df.isna().any().any():
        raise ValueError(f"Missing values found in {path.name}")

    if df["ts"].duplicated().any():
        raise ValueError(f"Duplicate timestamps found in {path.name}")

    df = df.sort_values("ts").set_index("ts")

    differences = df.index.to_series().diff().dropna()
    missing = int(
        (differences != pd.Timedelta(minutes=1)).sum()
    )

    if missing:
        raise ValueError(
            f"{symbol}: found {missing} timestamp gaps. "
            "Stopping rather than silently creating misleading candles."
        )

    if not (
        df["high"] >= df[["open", "close", "low"]].max(axis=1)
    ).all():
        raise ValueError(f"Invalid high prices in {symbol}")

    if not (
        df["low"] <= df[["open", "close", "high"]].min(axis=1)
    ).all():
        raise ValueError(f"Invalid low prices in {symbol}")

    if (df["vol"] < 0).any():
        raise ValueError(f"Negative volume found in {symbol}")

    return df


def make_timeframe(df, rule):
    result = df.resample(
        rule,
        origin="epoch",
        label="left",
        closed="left"
    ).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "vol": "sum",
    })

    result = result.dropna()

    # Exclude the first bucket if source data begins partway through it.
    first_complete_start = df.index[0].ceil(rule)
    result = result[result.index >= first_complete_start]

    # Each 1m timestamp represents the START of its candle.
    # Therefore, the final source candle ends one minute later.
    last_candle_end = df.index[-1] + pd.Timedelta(minutes=1)

    # Keep only higher-timeframe candles that have fully closed.
    duration = pd.Timedelta(rule)
    result = result[
        result.index + duration <= last_candle_end
    ]

    return result


def main():
    print("===== OKX ADAPTIVE BOT DATA PREPARATION =====")

    for symbol in SYMBOLS:
        print(f"\nProcessing {symbol}...")

        df = load_data(symbol)

        print(f"1m candles: {len(df):,}")
        print(f"First candle: {df.index[0]}")
        print(f"Last candle:  {df.index[-1]}")

        for name, rule in TIMEFRAMES.items():
            candles = make_timeframe(df, rule)

            if candles.empty:
                raise ValueError(
                    f"{symbol} {name}: no complete candles produced"
                )

            output = DATA_DIR / f"{symbol}_USDT_{name}.csv"

            save = candles.copy()
            save.insert(
                0,
                "ts",
                save.index.as_unit("ns").asi8 // 10**6
            )
            save.to_csv(output, index=False)

            print(
                f"{name}: {len(candles):,} complete candles saved"
            )
            print(f"  Latest candle: {candles.index[-1]}")

    print("\n===== PREPARATION COMPLETE =====")
    print("Original 1m files were not modified.")
    print("LINK was excluded.")
    print(f"Output folder: {DATA_DIR}")


if __name__ == "__main__":
    main()
