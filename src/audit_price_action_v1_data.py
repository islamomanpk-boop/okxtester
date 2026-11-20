from pathlib import Path
import pandas as pd
import numpy as np
import sys

BASE = Path.home() / "okx_adaptive_bot" / "data"
SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

def audit(path, interval_ms=None):
    df = pd.read_csv(path)

    required = ["ts", "open", "high", "low", "close", "vol"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    ts = pd.to_numeric(df["ts"], errors="coerce")
    if ts.isna().any():
        raise ValueError("Invalid timestamps")
    if ts.duplicated().any():
        raise ValueError("Duplicate timestamps")

    delta = ts.diff().dropna()
    if (delta <= 0).any():
        raise ValueError("Timestamps out of order")

    if interval_ms and (delta != interval_ms).any():
        raise ValueError(
            f"Unexpected intervals: {(delta != interval_ms).sum()}"
        )

    prices = df[["open", "high", "low", "close", "vol"]].apply(
        pd.to_numeric, errors="coerce"
    )

    if not np.isfinite(prices.to_numpy(dtype=float)).all():
        raise ValueError("Invalid or missing OHLCV values")

    if (prices[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("Non-positive prices")

    invalid = (
        (prices.high < prices[["open", "close", "low"]].max(axis=1))
        | (prices.low > prices[["open", "close", "high"]].min(axis=1))
        | (prices.vol < 0)
    )

    if invalid.any():
        raise ValueError(f"Invalid OHLCV rows: {invalid.sum()}")

    first = pd.to_datetime(ts.iloc[0], unit="ms", utc=True)
    last = pd.to_datetime(ts.iloc[-1], unit="ms", utc=True)

    return len(df), first, last

def main():
    intervals = {
        "1m": 60_000,
        "15m": 900_000,
        "4h": 14_400_000,
        "1d": 86_400_000,
    }

    failures = []

    print("===== PRICE ACTION V1 DATA AUDIT =====")

    for symbol in SYMBOLS:
        print(f"\n--- {symbol} ---")

        for tf, interval in intervals.items():
            suffix = "_USDT_USDT_1m.csv" if tf == "1m" else f"_USDT_{tf}.csv"
            path = BASE / f"{symbol}{suffix}"

            try:
                rows, first, last = audit(path, interval)
                print(f"PASS {tf}: {rows:,} rows")
                print(f"  {first} -> {last}")
            except Exception as e:
                failures.append(f"{symbol} {tf}: {e}")
                print(f"FAIL {tf}: {e}")

        indicator_specs = {
            "15m": ["ema20", "ema50", "rsi14"],
            "4h": ["ema50", "ema200", "atr14", "adx14"],
            "1d": ["ema50", "ema200", "atr14"],
        }

        for tf, columns in indicator_specs.items():
            path = BASE / "indicators" / f"{symbol}_USDT_{tf}_indicators.csv"

            try:
                df = pd.read_csv(path)
                missing = [c for c in columns if c not in df.columns]
                if missing:
                    raise ValueError(f"Missing indicators: {missing}")

                if df["ts"].duplicated().any():
                    raise ValueError("Duplicate timestamps")

                ready = int(df[columns].notna().all(axis=1).sum())
                print(f"PASS {tf} indicators: {ready:,}/{len(df):,} ready")
            except Exception as e:
                failures.append(f"{symbol} {tf} indicators: {e}")
                print(f"FAIL {tf} indicators: {e}")

    print("\n===== FINAL RESULT =====")

    if failures:
        print(f"FAILED: {len(failures)} issue(s)")
        for item in failures:
            print("-", item)
        sys.exit(1)

    print("PASS: all required files passed structural checks.")
    print("This audit does not test strategy profitability or funding.")

if __name__ == "__main__":
    main()
