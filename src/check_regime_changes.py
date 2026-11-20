import pandas as pd
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
REPORTS = BASE / "reports"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

print("===== REGIME CHANGE ANALYSIS =====")

for symbol in SYMBOLS:
    df = pd.read_csv(REPORTS / f"{symbol}_regimes.csv")

    df["ts"] = pd.to_datetime(
        df["ts"], unit="ms", utc=True
    )

    df = df.sort_values("ts")

    # Exclude warm-up candles from market regime statistics.
    ready = df[df["regime"] != "WARMUP"].copy()

    ready["previous_regime"] = ready["regime"].shift(1)

    changes = ready[
        ready["regime"] != ready["previous_regime"]
    ]

    print(f"\n===== {symbol} =====")
    print("Ready candles:", len(ready))
    print("Regime changes:", max(len(changes) - 1, 0))

    print("\nRegime distribution:")
    print(ready["regime"].value_counts().to_string())

    print("\nChange counts:")
    print(
        ready.loc[
            ready["previous_regime"].notna()
            & (ready["regime"] != ready["previous_regime"]),
            ["previous_regime", "regime"]
        ].value_counts().to_string()
    )

print("\n===== ANALYSIS COMPLETE =====")
