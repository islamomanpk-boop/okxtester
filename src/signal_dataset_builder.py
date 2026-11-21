"""Build causal 15m price-action signal datasets with 4h regime context."""

from pathlib import Path

import pandas as pd

from price_action_signals import detect_signals

BASE = Path.home() / "okx_adaptive_bot"
INDICATORS = BASE / "data" / "indicators"
REGIMES = BASE / "reports"
OUTPUT = BASE / "reports" / "price_action_signals"
PROJECT_REPORT = Path(__file__).resolve().parents[1] / "reports" / "signal_dataset_audit.md"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
SIGNAL_DURATION = pd.Timedelta(minutes=15)
REGIME_DURATION = pd.Timedelta(hours=4)

OHLC = ["open", "high", "low", "close"]


def calculate_atr14(df, period=14):
    """Same Wilder-style ATR calculation used by calculate_indicators.py."""
    previous_close = df["close"].shift(1)

    true_range = pd.concat([
        df["high"] - df["low"],
        (df["high"] - previous_close).abs(),
        (df["low"] - previous_close).abs(),
    ], axis=1).max(axis=1)

    return true_range.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()


def load_15m(symbol):
    path = INDICATORS / f"{symbol}_USDT_15m_indicators.csv"
    if not path.is_file():
        raise FileNotFoundError(path)

    df = pd.read_csv(path)

    required = ["ts", *OHLC, "vol"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{symbol} 15m missing columns: {missing}")

    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)

    if df["ts"].duplicated().any():
        raise ValueError(f"{symbol} 15m has duplicate timestamps")

    df = df.sort_values("ts").reset_index(drop=True)

    if not df["ts"].is_monotonic_increasing:
        raise ValueError(f"{symbol} 15m timestamps are not chronological")

    for col in [*OHLC, "vol"]:
        df[col] = pd.to_numeric(df[col], errors="raise")

    values = df[OHLC].to_numpy(dtype=float)
    if not pd.notna(values).all():
        raise ValueError(f"{symbol} 15m has missing OHLC values")

    if (values <= 0).any():
        raise ValueError(f"{symbol} 15m has non-positive prices")

    invalid = (
        (df["high"] < df[["open", "close", "low"]].max(axis=1))
        | (df["low"] > df[["open", "close", "high"]].min(axis=1))
    )
    if invalid.any():
        raise ValueError(f"{symbol} 15m has invalid OHLC structure")

    # Timestamp is candle OPEN. Signals become usable after candle CLOSE.
    df["signal_available_at"] = df["ts"] + SIGNAL_DURATION

    # ATR is calculated only from current and past completed 15m candles.
    df["atr14"] = calculate_atr14(df)

    return df


def load_regimes(symbol):
    path = REGIMES / f"{symbol}_regimes.csv"
    if not path.is_file():
        raise FileNotFoundError(path)

    df = pd.read_csv(path)

    required = ["ts", "available_at", "regime", "symbol"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{symbol} regime report missing columns: {missing}")

    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df["available_at"] = pd.to_datetime(df["available_at"], utc=True)

    if df["ts"].duplicated().any():
        raise ValueError(f"{symbol} regime report has duplicate timestamps")

    if df["available_at"].duplicated().any():
        raise ValueError(f"{symbol} regime report has duplicate availability times")

    df = df.sort_values("available_at").reset_index(drop=True)

    expected = df["ts"] + REGIME_DURATION
    if not (df["available_at"] == expected).all():
        raise ValueError(f"{symbol} regime available_at is not ts + 4 hours")

    if not (df["symbol"] == symbol).all():
        raise ValueError(f"{symbol} regime report contains another symbol")

    allowed = {"BULLISH", "BEARISH", "SIDEWAYS", "TRANSITION", "WARMUP"}
    unknown = set(df["regime"].dropna().unique()) - allowed
    if unknown:
        raise ValueError(f"{symbol} has unknown regimes: {sorted(unknown)}")

    keep = df[["ts", "available_at", "regime"]].copy()
    return keep.rename(columns={
        "ts": "regime_ts",
        "available_at": "regime_available_at",
    })


def attach_regimes(signals, regimes):
    """Attach only the latest regime already available at signal close."""
    left = signals.sort_values("signal_available_at").copy()
    right = regimes.sort_values("regime_available_at").copy()

    merged = pd.merge_asof(
        left,
        right,
        left_on="signal_available_at",
        right_on="regime_available_at",
        direction="backward",
        allow_exact_matches=True,
    )

    matched = merged["regime_available_at"].notna()
    if (
        merged.loc[matched, "regime_available_at"]
        > merged.loc[matched, "signal_available_at"]
    ).any():
        raise AssertionError("Future 4h regime attached to a 15m signal")

    merged["regime"] = merged["regime"].fillna("NO_REGIME_AVAILABLE")
    return merged


def build_symbol(symbol):
    candles = load_15m(symbol)
    regimes = load_regimes(symbol)

    detected = detect_signals(candles)
    detected["symbol"] = symbol

    result = attach_regimes(detected, regimes)

    # Final independent timing assertion.
    matched = result["regime_available_at"].notna()
    if not (
        result.loc[matched, "regime_available_at"]
        <= result.loc[matched, "signal_available_at"]
    ).all():
        raise AssertionError(f"{symbol}: future regime leakage detected")

    if result["ts"].duplicated().any():
        raise AssertionError(f"{symbol}: duplicate output timestamps")

    if not result["ts"].is_monotonic_increasing:
        raise AssertionError(f"{symbol}: output is not chronological")

    return result


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    PROJECT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    report = [
        "# Price Action Signal Dataset Audit",
        "",
        "Status: generated by `src/signal_dataset_builder.py`.",
        "",
        "Timing rules:",
        "- 15m candle timestamp is its opening time.",
        "- Signal availability is 15m timestamp + 15 minutes.",
        "- 4h regime availability is its 4h timestamp + 4 hours.",
        "- Regimes are attached using backward as-of matching only.",
        "- Exact-time matches are allowed; future regime matches are forbidden.",
        "- ATR14 uses the same Wilder-style calculation as the existing indicator script.",
        "",
        "| Asset | Rows | Regime matched | No regime yet | Signal events | Future matches |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    total_rows = 0
    total_events = 0

    for symbol in SYMBOLS:
        result = build_symbol(symbol)
        output_path = OUTPUT / f"{symbol}_15m_price_action_signals.csv"
        result.to_csv(output_path, index=False)

        matched = result["regime_available_at"].notna()
        future = (
            result.loc[matched, "regime_available_at"]
            > result.loc[matched, "signal_available_at"]
        ).sum()

        event_cols = [
            "bullish_engulfing", "bearish_engulfing",
            "bullish_pinbar", "bearish_pinbar",
            "support_rejection", "resistance_rejection",
            "bullish_ob_created", "bearish_ob_created",
            "bullish_ob_first_retest", "bearish_ob_first_retest",
        ]
        events = int(result[event_cols].to_numpy(dtype=bool).sum())

        total_rows += len(result)
        total_events += events

        report.append(
            f"| {symbol} | {len(result):,} | {int(matched.sum()):,} "
            f"| {int((~matched).sum()):,} | {events:,} | {int(future)} |"
        )

        print(
            f"{symbol}: rows={len(result):,}, "
            f"regime matched={int(matched.sum()):,}, "
            f"signal events={events:,}, future matches={int(future)}"
        )
        print(f"Saved local dataset: {output_path}")

    report.extend([
        "",
        f"Total rows: {total_rows:,}",
        f"Total signal events: {total_events:,}",
        "",
        "All five assets completed. Any future regime match would stop the build.",
        "The per-asset CSV datasets remain local and are not added to Git.",
    ])

    PROJECT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n===== SIGNAL DATASET BUILD COMPLETE =====")
    print("Audit report:", PROJECT_REPORT)
    print("Local datasets:", OUTPUT)


if __name__ == "__main__":
    main()
