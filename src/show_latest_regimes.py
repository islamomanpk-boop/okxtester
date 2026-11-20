import pandas as pd
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
REPORTS = BASE / "reports"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

print("===== LATEST COMPLETED MARKET REGIMES =====")

for symbol in SYMBOLS:
    df = pd.read_csv(REPORTS / f"{symbol}_regimes.csv")
    df = df.sort_values("ts")

    latest = df.iloc[-1]

    ts = pd.to_datetime(
        latest["ts"], unit="ms", utc=True
    )

    close_time = ts + pd.Timedelta(hours=4)

    print(f"\n{symbol}")
    print("4H candle opened:", ts)
    print("4H candle closed:", close_time)
    print("Regime:", latest["regime"])
    print("4H close:", latest["close"])
    print("Daily EMA50:", latest["daily_ema50"])
    print("Daily EMA200:", latest["daily_ema200"])
    print("4H EMA50:", latest["ema50"])
    print("4H EMA200:", latest["ema200"])
    print("ADX14:", latest["adx14"])

print("\n===== INSPECTION COMPLETE =====")
