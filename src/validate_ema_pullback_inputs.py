import pandas as pd
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
DATA = BASE / "data" / "indicators"
REPORTS = BASE / "reports"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

print("===== EMA PULLBACK TIMING AND SIGNAL VALIDATION =====")

total_long = 0
total_short = 0

for symbol in SYMBOLS:
    print(f"\n===== {symbol} =====")

    df = pd.read_csv(
        DATA / f"{symbol}_USDT_15m_indicators.csv"
    )
    regime = pd.read_csv(
        REPORTS / f"{symbol}_regimes.csv"
    )

    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    regime["available_at"] = pd.to_datetime(
        regime["available_at"], utc=True
    )

    df = df.sort_values("ts").copy()
    regime = regime.sort_values("available_at").copy()

    previous_close = df["close"].shift(1)

    true_range = pd.concat([
        df["high"] - df["low"],
        (df["high"] - previous_close).abs(),
        (df["low"] - previous_close).abs()
    ], axis=1).max(axis=1)

    df["atr14"] = true_range.rolling(14).mean()

    # The signal becomes available only when its 15M candle closes.
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

    matched = merged["available_at"].notna()

    # Safety check: a matched 4H regime must already be available.
    future_match = (
        matched
        & (
            merged["available_at"]
            > merged["signal_available_at"]
        )
    )

    if future_match.any():
        raise RuntimeError(
            f"{symbol}: LOOKAHEAD ERROR detected!"
        )

    technical_ready = (
        merged["atr14"].notna()
        & merged["ema20"].notna()
        & merged["ema50"].notna()
    )

    active_regime = merged["regime"].isin([
        "BULLISH", "BEARISH", "SIDEWAYS", "TRANSITION"
    ])

    ready = technical_ready & active_regime

    long_signal = (
        ready
        & (merged["regime"] == "BULLISH")
        & (merged["ema20"] > merged["ema50"])
        & (merged["low"] <= merged["ema20"])
        & (merged["close"] > merged["ema20"])
        & (merged["close"] > merged["open"])
    )

    short_signal = (
        ready
        & (merged["regime"] == "BEARISH")
        & (merged["ema20"] < merged["ema50"])
        & (merged["high"] >= merged["ema20"])
        & (merged["close"] < merged["ema20"])
        & (merged["close"] < merged["open"])
    )

    long_count = int(long_signal.sum())
    short_count = int(short_signal.sum())

    total_long += long_count
    total_short += short_count

    print("15M candles:", len(merged))
    print("15M indicator-ready candles:", int(technical_ready.sum()))
    print("Matched 4H regimes:", int(matched.sum()))
    print("Missing 4H matches:", int((~matched).sum()))
    print("WARMUP rows:", int((merged["regime"] == "WARMUP").sum()))
    print("Fully regime-ready candles:", int(ready.sum()))
    print("Future 4H matches:", int(future_match.sum()))
    print("Potential long signals:", long_count)
    print("Potential short signals:", short_count)

    print("\nRegime counts:")
    print(
        merged.loc[ready, "regime"]
        .value_counts()
        .to_string()
    )

    if matched.any():
        print(
            "\nFirst matched 4H availability:",
            merged.loc[matched, "available_at"].min()
        )

print("\n===== TOTALS =====")
print("Potential long signals:", total_long)
print("Potential short signals:", total_short)
print("Total potential signals:", total_long + total_short)
print("\n===== VALIDATION COMPLETE =====")
print("A successful run must show Future 4H matches: 0 for every coin.")
