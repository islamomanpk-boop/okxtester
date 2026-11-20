import pandas as pd
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
DATA = BASE / "data" / "indicators"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

for symbol in SYMBOLS:
    df = pd.read_csv(
        BASE / "reports" / f"{symbol}_regimes.csv"
    )

    ready = df.dropna(
        subset=[
            "daily_ema50",
            "daily_ema200",
            "ema50",
            "ema200",
            "adx14"
        ]
    ).copy()

    daily_bull = ready["daily_ema50"] > ready["daily_ema200"]
    daily_bear = ready["daily_ema50"] < ready["daily_ema200"]

    four_bull = ready["ema50"] > ready["ema200"]
    four_bear = ready["ema50"] < ready["ema200"]

    low_adx = ready["adx14"] < 20
    high_adx = ready["adx14"] >= 20

    print(f"\n===== {symbol} =====")
    print(f"Ready candles: {len(ready):,}")
    print(f"Daily bullish: {daily_bull.sum():,}")
    print(f"Daily bearish: {daily_bear.sum():,}")
    print(f"4H bullish:    {four_bull.sum():,}")
    print(f"4H bearish:    {four_bear.sum():,}")
    print(f"ADX below 20:  {low_adx.sum():,}")
    print(f"ADX >= 20:     {high_adx.sum():,}")

    print(f"Both bullish:  {(daily_bull & four_bull).sum():,}")
    print(f"Both bearish:  {(daily_bear & four_bear).sum():,}")
    print(f"Trend conflict: {(daily_bull & four_bear | daily_bear & four_bull).sum():,}")

    print(f"Low ADX with aligned trend: {((daily_bull & four_bull | daily_bear & four_bear) & low_adx).sum():,}")

print("\n===== DIAGNOSIS COMPLETE =====")
