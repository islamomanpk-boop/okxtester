import pandas as pd
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
REPORTS = BASE / "reports"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

print("===== REGIME DURATION ANALYSIS =====")

for symbol in SYMBOLS:
    df = pd.read_csv(REPORTS / f"{symbol}_regimes.csv")
    df = df.sort_values("ts").copy()

    df = df[df["regime"] != "WARMUP"].copy()

    # Identify consecutive runs of the same regime.
    df["run_id"] = (
        df["regime"] != df["regime"].shift()
    ).cumsum()

    runs = (
        df.groupby(["run_id", "regime"])
        .size()
        .reset_index(name="candles")
    )

    runs["hours"] = runs["candles"] * 4

    print(f"\n===== {symbol} =====")

    summary = (
        runs.groupby("regime")["hours"]
        .agg(["count", "median", "mean", "min", "max"])
        .round(1)
    )

    print(summary.to_string())

    print("\nAll regime runs:", len(runs))

print("\n===== ANALYSIS COMPLETE =====")
