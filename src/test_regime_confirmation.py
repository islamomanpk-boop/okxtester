import pandas as pd
from pathlib import Path

BASE = Path.home() / "okx_adaptive_bot"
REPORTS = BASE / "reports"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

print("===== TWO-CANDLE CONFIRMATION TEST =====")

total_original = 0
total_confirmed = 0

for symbol in SYMBOLS:
    df = pd.read_csv(REPORTS / f"{symbol}_regimes.csv")
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df = df.sort_values("ts").copy()

    ready = df["regime"] != "WARMUP"
    original = df.loc[ready, "regime"]

    # A new regime is accepted only after two consecutive
    # closed candles show the same new regime.
    confirmed = []
    current = None
    candidate = None
    candidate_count = 0

    for regime in original:
        if current is None:
            current = regime
            candidate = None
            candidate_count = 0

        elif regime == current:
            candidate = None
            candidate_count = 0

        elif regime == candidate:
            candidate_count += 1

            if candidate_count >= 2:
                current = candidate
                candidate = None
                candidate_count = 0

        else:
            candidate = regime
            candidate_count = 1

        confirmed.append(current)

    original_changes = int(
        (original != original.shift(1)).sum() - 1
    )

    confirmed_series = pd.Series(confirmed, index=original.index)

    confirmed_changes = int(
        (confirmed_series != confirmed_series.shift(1)).sum() - 1
    )

    filtered = original_changes - confirmed_changes

    total_original += original_changes
    total_confirmed += confirmed_changes

    print(f"\n===== {symbol} =====")
    print("Original regime changes:", original_changes)
    print("Confirmed regime changes:", confirmed_changes)
    print("Changes filtered:", filtered)

    print("\nConfirmed regime distribution:")
    print(confirmed_series.value_counts().to_string())

print("\n===== COMBINED =====")
print("Original changes:", total_original)
print("Confirmed changes:", total_confirmed)
print("Changes filtered:", total_original - total_confirmed)

print("\nNo original regime files were modified.")
