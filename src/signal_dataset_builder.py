"""Build causal 15m datasets with separate PA and indicator context."""

from pathlib import Path

import numpy as np
import pandas as pd

from price_action_signals import detect_signals
from price_action_structure import detect_structure

BASE = Path.home() / "okx_adaptive_bot"
INDICATORS = BASE / "data" / "indicators"
REGIMES = BASE / "reports"
OUTPUT = BASE / "reports" / "price_action_signals"
PROJECT_REPORT = (
    Path(__file__).resolve().parents[1]
    / "reports" / "signal_dataset_audit.md"
)

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
SIGNAL_DURATION = pd.Timedelta(minutes=15)
REGIME_DURATION = pd.Timedelta(hours=4)

OHLC = ["open", "high", "low", "close"]

STRUCTURE_CONFIG = {
    "1d": {
        "duration_ms": 86_400_000,
        "prefix": "daily",
    },
    "4h": {
        "duration_ms": 14_400_000,
        "prefix": "four_hour",
    },
}


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
    if not np.isfinite(values).all():
        raise ValueError(f"{symbol} 15m has invalid OHLC values")

    if (values <= 0).any():
        raise ValueError(f"{symbol} 15m has non-positive prices")

    invalid = (
        (df["high"] < df[["open", "close", "low"]].max(axis=1))
        | (df["low"] > df[["open", "close", "high"]].min(axis=1))
    )
    if invalid.any():
        raise ValueError(f"{symbol} 15m has invalid OHLC structure")

    # A 15m signal is available only after its candle closes.
    df["signal_available_at"] = df["ts"] + SIGNAL_DURATION

    # ATR uses only current and past completed 15m candles.
    df["atr14"] = calculate_atr14(df)

    return df


def load_regimes(symbol):
    """Load the existing indicator-assisted Model B regime labels."""
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
        raise ValueError(
            f"{symbol} regime report has duplicate availability times"
        )

    df = df.sort_values("available_at").reset_index(drop=True)

    expected = df["ts"] + REGIME_DURATION
    if not (df["available_at"] == expected).all():
        raise ValueError(
            f"{symbol} regime available_at is not ts + 4 hours"
        )

    if not (df["symbol"] == symbol).all():
        raise ValueError(f"{symbol} regime report contains another symbol")

    allowed = {"BULLISH", "BEARISH", "SIDEWAYS", "TRANSITION", "WARMUP"}
    unknown = set(df["regime"].dropna().unique()) - allowed
    if unknown:
        raise ValueError(
            f"{symbol} has unknown regimes: {sorted(unknown)}"
        )

    keep = df[["ts", "available_at", "regime"]].copy()
    return keep.rename(columns={
        "ts": "regime_ts",
        "available_at": "regime_available_at",
    })


def attach_regimes(signals, regimes):
    """Attach only the latest Model B regime available at signal close."""
    left = signals.copy()
    left["_builder_order"] = np.arange(len(left))

    left = left.sort_values("signal_available_at")
    right = regimes.sort_values("regime_available_at")

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

    # Explicit Model B name; keep legacy regime column for compatibility.
    merged["indicator_regime"] = merged["regime"]

    return (
        merged.sort_values("_builder_order")
        .drop(columns="_builder_order")
        .reset_index(drop=True)
    )


def load_structure(symbol, timeframe):
    """
    Calculate indicator-free structure from one higher timeframe.

    Only ts and OHLC are passed to detect_structure. Any EMA, RSI,
    ADX, or other indicator columns in the source file are ignored.
    """
    if timeframe not in STRUCTURE_CONFIG:
        raise ValueError(f"Unsupported structure timeframe: {timeframe}")

    config = STRUCTURE_CONFIG[timeframe]
    duration_ms = config["duration_ms"]
    prefix = config["prefix"]

    path = INDICATORS / f"{symbol}_USDT_{timeframe}_indicators.csv"
    if not path.is_file():
        raise FileNotFoundError(path)

    source = pd.read_csv(path)

    required = ["ts", *OHLC]
    missing = [c for c in required if c not in source.columns]
    if missing:
        raise ValueError(
            f"{symbol} {timeframe} structure input missing columns: {missing}"
        )

    ts = pd.to_numeric(source["ts"], errors="coerce")
    if ts.isna().any() or not np.isfinite(ts.to_numpy(dtype=float)).all():
        raise ValueError(f"{symbol} {timeframe} has invalid timestamps")

    if not np.equal(ts.to_numpy(dtype=float), np.floor(
        ts.to_numpy(dtype=float)
    )).all():
        raise ValueError(f"{symbol} {timeframe} timestamps must be integers")

    source["ts"] = ts.astype("int64")

    if source["ts"].duplicated().any():
        raise ValueError(f"{symbol} {timeframe} has duplicate timestamps")

    source = source.sort_values("ts").reset_index(drop=True)

    if len(source) > 1:
        differences = source["ts"].diff().dropna()
        if not (differences == duration_ms).all():
            raise ValueError(
                f"{symbol} {timeframe} has missing or irregular candles"
            )

    # Keep only raw price fields. Indicators cannot affect Model A.
    candles = source[["ts", *OHLC]].copy()

    for col in OHLC:
        candles[col] = pd.to_numeric(candles[col], errors="raise")

    detected = detect_structure(
        candles,
        timeframe_ms=duration_ms,
        left=3,
        right=3,
    )

    # Use namespaced columns so daily and 4h fields never collide.
    result = pd.DataFrame({
        f"{prefix}_ts": pd.to_datetime(
            detected["ts"], unit="ms", utc=True
        ),
        f"{prefix}_structure_available_at": pd.to_datetime(
            detected["structure_available_at"], unit="ms", utc=True
        ),
        f"{prefix}_structure": detected["structure"].astype(str),
        f"{prefix}_pivot_high_confirmed": (
            detected["pivot_high_confirmed"].astype(bool)
        ),
        f"{prefix}_pivot_low_confirmed": (
            detected["pivot_low_confirmed"].astype(bool)
        ),
        f"{prefix}_confirmed_pivot_high": (
            detected["confirmed_pivot_high"]
        ),
        f"{prefix}_confirmed_pivot_low": (
            detected["confirmed_pivot_low"]
        ),
        f"{prefix}_bos_bullish": detected["bos_bullish"].astype(bool),
        f"{prefix}_bos_bearish": detected["bos_bearish"].astype(bool),
        f"{prefix}_bos_level": detected["bos_level"],
    })

    return result


def attach_structure(signals, structure, prefix):
    """Backward-align one higher-timeframe structure to 15m signal times."""
    available_col = f"{prefix}_structure_available_at"
    structure_col = f"{prefix}_structure"

    if "signal_available_at" not in signals:
        raise ValueError("Signals missing signal_available_at")

    required = [
        available_col,
        structure_col,
        f"{prefix}_bos_bullish",
        f"{prefix}_bos_bos_placeholder",
    ]
    # Check the actual required columns without requiring a placeholder.
    required = [
        available_col,
        structure_col,
        f"{prefix}_bos_bullish",
        f"{prefix}_bos_bearish",
    ]
    missing = [c for c in required if c not in structure.columns]
    if missing:
        raise ValueError(f"{prefix} structure missing columns: {missing}")

    left = signals.copy()
    left["_builder_order"] = np.arange(len(left))

    left = left.sort_values("signal_available_at")
    right = structure.sort_values(available_col)

    merged = pd.merge_asof(
        left,
        right,
        left_on="signal_available_at",
        right_on=available_col,
        direction="backward",
        allow_exact_matches=True,
    )

    matched = merged[available_col].notna()
    if (
        merged.loc[matched, available_col]
        > merged.loc[matched, "signal_available_at"]
    ).any():
        raise AssertionError(f"Future {prefix} structure attached")

    merged[structure_col] = merged[structure_col].fillna(
        "NO_STRUCTURE_AVAILABLE"
    )

    # Missing structure means no BOS event, not an event with unknown value.
    for col in [
        f"{prefix}_pivot_high_confirmed",
        f"{prefix}_pivot_low_confirmed",
        f"{prefix}_bos_bullish",
        f"{prefix}_bos_bearish",
    ]:
        if col in merged.columns:
            merged[col] = merged[col].fillna(False).astype(bool)

    return (
        merged.sort_values("_builder_order")
        .drop(columns="_builder_order")
        .reset_index(drop=True)
    )


def apply_direction_permission(df):
    """Require daily and 4h price structure to agree for trend permission."""
    daily = df["daily_structure"]
    four_hour = df["four_hour_structure"]

    df = df.copy()
    df["pa_direction_permission"] = "NO_TREND"

    bullish = (daily == "BULLISH") & (four_hour == "BULLISH")
    bearish = (daily == "BEARISH") & (four_hour == "BEARISH")

    df.loc[bullish, "pa_direction_permission"] = "LONG_ONLY"
    df.loc[bearish, "pa_direction_permission"] = "SHORT_ONLY"

    return df


def build_symbol(symbol):
    candles = load_15m(symbol)
    regimes = load_regimes(symbol)

    detected = detect_signals(candles)
    detected["symbol"] = symbol

    # Model B: existing indicator-assisted regime, kept separate.
    result = attach_regimes(detected, regimes)

    # Model A: independent OHLC-only daily and 4h structure.
    daily = load_structure(symbol, "1d")
    four_hour = load_structure(symbol, "4h")

    result = attach_structure(result, daily, "daily")
    result = attach_structure(result, four_hour, "four_hour")
    result = apply_direction_permission(result)

    # Independent timing assertions for every higher timeframe.
    for prefix in ("daily", "four_hour"):
        available = result[f"{prefix}_structure_available_at"]
        matched = available.notna()

        if not (
            available.loc[matched]
            <= result.loc[matched, "signal_available_at"]
        ).all():
            raise AssertionError(
                f"{symbol}: future {prefix} structure leakage detected"
            )

    matched_regime = result["regime_available_at"].notna()
    if not (
        result.loc[matched_regime, "regime_available_at"]
        <= result.loc[matched_regime, "signal_available_at"]
    ).all():
        raise AssertionError(f"{symbol}: future indicator regime leakage")

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
        "## Causal timing",
        "",
        "- 15m signal availability = 15m candle open + 15 minutes.",
        "- Daily structure availability = daily candle open + 24 hours.",
        "- 4h structure availability = 4h candle open + 4 hours.",
        "- Indicator regime availability comes from the existing regime report.",
        "- All higher-timeframe joins use backward as-of matching.",
        "- Exact availability-time matches are allowed.",
        "- Future structure and regime matches are forbidden.",
        "",
        "## Model separation",
        "",
        "- Model A uses OHLC-only daily and 4h market structure.",
        "- Model B retains the existing indicator-assisted `indicator_regime`.",
        "- The legacy `regime` column is retained as a compatibility alias.",
        "- Direction permission requires daily and 4h structure agreement.",
        "",
        "| Asset | Rows | Daily matched | 4h matched | Model B matched | Long only | Short only | No trend | Future matches |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    total_rows = 0
    total_events = 0
    total_future = 0

    event_cols = [
        "bullish_engulfing", "bearish_engulfing",
        "bullish_pinbar", "bearish_pinbar",
        "support_rejection", "resistance_rejection",
        "bullish_ob_created", "bearish_ob_created",
        "bullish_ob_first_retest", "bearish_ob_first_retest",
    ]

    for symbol in SYMBOLS:
        result = build_symbol(symbol)
        output_path = OUTPUT / f"{symbol}_15m_price_action_signals.csv"
        result.to_csv(output_path, index=False)

        daily_matched = result["daily_structure_available_at"].notna()
        four_hour_matched = result["four_hour_structure_available_at"].notna()
        regime_matched = result["regime_available_at"].notna()

        future_daily = (
            result.loc[daily_matched, "daily_structure_available_at"]
            > result.loc[daily_matched, "signal_available_at"]
        ).sum()
        future_four_hour = (
            result.loc[four_hour_matched, "four_hour_structure_available_at"]
            > result.loc[four_hour_matched, "signal_available_at"]
        ).sum()
        future_regime = (
            result.loc[regime_matched, "regime_available_at"]
            > result.loc[regime_matched, "signal_available_at"]
        ).sum()

        future = int(future_daily + future_four_hour + future_regime)
        events = int(result[event_cols].to_numpy(dtype=bool).sum())

        permissions = result["pa_direction_permission"].value_counts()

        total_rows += len(result)
        total_events += events
        total_future += future

        report.append(
            f"| {symbol} | {len(result):,} "
            f"| {int(daily_matched.sum()):,} "
            f"| {int(four_hour_matched.sum()):,} "
            f"| {int(regime_matched.sum()):,} "
            f"| {int(permissions.get('LONG_ONLY', 0)):,} "
            f"| {int(permissions.get('SHORT_ONLY', 0)):,} "
            f"| {int(permissions.get('NO_TREND', 0)):,} "
            f"| {future} |"
        )

        print(
            f"{symbol}: rows={len(result):,}, "
            f"daily matched={int(daily_matched.sum()):,}, "
            f"4h matched={int(four_hour_matched.sum()):,}, "
            f"Model B matched={int(regime_matched.sum()):,}"
        )
        print(
            "  PA permission:",
            f"LONG_ONLY={int(permissions.get('LONG_ONLY', 0)):,},",
            f"SHORT_ONLY={int(permissions.get('SHORT_ONLY', 0)):,},",
            f"NO_TREND={int(permissions.get('NO_TREND', 0)):,}",
        )
        print(f"  Future matches: {future}")
        print(f"  Saved local dataset: {output_path}")

    report.extend([
        "",
        f"Total rows: {total_rows:,}",
        f"Total 15m signal events: {total_events:,}",
        f"Total future matches: {total_future:,}",
        "",
        "A successful audit requires zero future matches.",
        "The daily and 4h structure labels use OHLC only.",
        "The indicator-assisted regime remains a separate Model B field.",
        "Per-asset CSV datasets remain local and are not committed to Git.",
    ])

    if total_future:
        raise AssertionError(
            f"Dataset audit failed: {total_future} future matches"
        )

    PROJECT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n===== SIGNAL DATASET BUILD COMPLETE =====")
    print("Audit report:", PROJECT_REPORT)
    print("Local datasets:", OUTPUT)


if __name__ == "__main__":
    main()
