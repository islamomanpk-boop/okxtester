import pandas as pd
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
DATA = BASE / "data" / "indicators"
OUT = BASE / "reports"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
ADX_THRESHOLD = 20


def classify(symbol):
    daily_path = DATA / f"{symbol}_USDT_1d_indicators.csv"
    four_hour_path = DATA / f"{symbol}_USDT_4h_indicators.csv"

    daily = pd.read_csv(daily_path)
    four_hour = pd.read_csv(four_hour_path)

    daily["ts"] = pd.to_datetime(daily["ts"], unit="ms", utc=True)
    four_hour["ts"] = pd.to_datetime(
        four_hour["ts"], unit="ms", utc=True
    )

    daily = daily.sort_values("ts")
    four_hour = four_hour.sort_values("ts")

    # A daily candle is available only after its 24-hour interval closes.
    daily["available_at"] = daily["ts"] + pd.Timedelta(hours=24)

    daily = daily.rename(columns={
        "ema50": "daily_ema50",
        "ema200": "daily_ema200",
        "close": "daily_close"
    })

    daily_columns = [
        "available_at",
        "daily_close",
        "daily_ema50",
        "daily_ema200"
    ]

    # A 4H candle is classified only after its interval closes.
    four_hour["available_at"] = (
        four_hour["ts"] + pd.Timedelta(hours=4)
    )

    merged = pd.merge_asof(
        four_hour.sort_values("available_at"),
        daily[daily_columns].sort_values("available_at"),
        on="available_at",
        direction="backward"
    )

    ready = (
        merged["daily_ema50"].notna()
        & merged["daily_ema200"].notna()
        & merged["ema50"].notna()
        & merged["ema200"].notna()
        & merged["adx14"].notna()
    )

    # Missing indicator history is WARMUP, not market TRANSITION.
    merged["regime"] = "WARMUP"

    # Preserve the original market classification rules.
    merged.loc[ready, "regime"] = "TRANSITION"

    bullish = (
        ready
        & (merged["daily_ema50"] > merged["daily_ema200"])
        & (merged["ema50"] > merged["ema200"])
        & (merged["adx14"] >= ADX_THRESHOLD)
    )

    bearish = (
        ready
        & (merged["daily_ema50"] < merged["daily_ema200"])
        & (merged["ema50"] < merged["ema200"])
        & (merged["adx14"] >= ADX_THRESHOLD)
    )

    sideways = ready & (merged["adx14"] < ADX_THRESHOLD)

    merged.loc[bullish, "regime"] = "BULLISH"
    merged.loc[bearish, "regime"] = "BEARISH"
    merged.loc[sideways, "regime"] = "SIDEWAYS"

    merged["symbol"] = symbol

    return merged


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    all_results = []

    print("===== MARKET REGIME CLASSIFICATION =====")

    for symbol in SYMBOLS:
        result = classify(symbol)

        output = OUT / f"{symbol}_regimes.csv"
        result.to_csv(output, index=False)

        counts = result["regime"].value_counts()

        print(f"\n{symbol}")

        for regime in [
            "BULLISH", "BEARISH", "SIDEWAYS", "TRANSITION", "WARMUP"
        ]:
            count = int(counts.get(regime, 0))
            percentage = count / len(result) * 100

            print(
                f"{regime:10}: {count:5,} "
                f"({percentage:5.1f}%)"
            )

        all_results.append(result)

    combined = pd.concat(all_results, ignore_index=True)

    combined.to_csv(
        OUT / "all_symbols_regimes.csv",
        index=False
    )

    print("\n===== ALL COINS COMBINED =====")

    counts = combined["regime"].value_counts()

    for regime in [
        "BULLISH", "BEARISH", "SIDEWAYS", "TRANSITION", "WARMUP"
    ]:
        count = int(counts.get(regime, 0))
        percentage = count / len(combined) * 100

        print(
            f"{regime:10}: {count:6,} "
            f"({percentage:5.1f}%)"
        )

    print("\nRegime files saved in:", OUT)


if __name__ == "__main__":
    main()
