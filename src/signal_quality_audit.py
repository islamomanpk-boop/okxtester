"""Audit price-action signal frequency and distribution by asset and regime."""

from pathlib import Path

import pandas as pd

BASE = Path.home() / "okx_adaptive_bot"
DATA_DIR = BASE / "reports" / "price_action_signals"
REPORT = Path(__file__).resolve().parents[1] / "reports" / "signal_quality_audit.md"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

REGIMES = [
    "BULLISH", "BEARISH", "SIDEWAYS", "TRANSITION",
    "WARMUP", "NO_REGIME_AVAILABLE",
]

# These are the ten event signals. Pivot confirmations are structural
# information and are reported separately, not counted as entry signals.
SIGNALS = [
    "bullish_engulfing",
    "bearish_engulfing",
    "bullish_pinbar",
    "bearish_pinbar",
    "support_rejection",
    "resistance_rejection",
    "bullish_ob_created",
    "bearish_ob_created",
    "bullish_ob_first_retest",
    "bearish_ob_first_retest",
]

PIVOTS = ["pivot_high_confirmed", "pivot_low_confirmed"]

REQUIRED = ["ts", "regime", *SIGNALS, *PIVOTS]


def boolean_series(series, label):
    """Convert CSV boolean values safely; reject ambiguous values."""
    if series.isna().any():
        raise ValueError(f"{label} contains missing boolean values")

    if pd.api.types.is_bool_dtype(series):
        return series.astype(bool)

    mapped = series.astype(str).str.strip().str.lower().map({
        "true": True, "false": False, "1": True, "0": False,
    })

    if mapped.isna().any():
        bad = series[mapped.isna()].unique().tolist()[:5]
        raise ValueError(f"{label} has invalid boolean values: {bad}")

    return mapped.astype(bool)


def audit_frame(df, symbol):
    """Return deterministic descriptive statistics for one asset."""
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"{symbol}: missing columns: {missing}")

    if df.empty:
        raise ValueError(f"{symbol}: dataset is empty")

    if df["ts"].duplicated().any():
        raise ValueError(f"{symbol}: duplicate timestamps")

    timestamps = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    if timestamps.isna().any() or not timestamps.is_monotonic_increasing:
        raise ValueError(f"{symbol}: invalid or non-chronological timestamps")

    if df["regime"].isna().any():
        raise ValueError(f"{symbol}: missing regime labels")

    unknown = set(df["regime"].unique()) - set(REGIMES)
    if unknown:
        raise ValueError(f"{symbol}: unknown regimes: {sorted(unknown)}")

    flags = pd.DataFrame(index=df.index)
    for col in SIGNALS + PIVOTS:
        flags[col] = boolean_series(df[col], f"{symbol}.{col}")

    event_count = flags[SIGNALS].sum(axis=1)
    pivot_count = flags[PIVOTS].sum(axis=1)

    result = {
        "symbol": symbol,
        "rows": len(df),
        "signal_counts": flags[SIGNALS].sum().astype(int).to_dict(),
        "pivot_counts": flags[PIVOTS].sum().astype(int).to_dict(),
        "regime_rows": df["regime"].value_counts().to_dict(),
        "regime_signal_counts": {},
        "event_rows": int(event_count.gt(0).sum()),
        "total_events": int(event_count.sum()),
        "multi_signal_rows": int(event_count.gt(1).sum()),
        "max_signals_per_candle": int(event_count.max()),
        "overlap_distribution": {
            str(k): int((event_count == k).sum())
            for k in range(4)
        },
        "overlap_distribution": {
            "0": int(event_count.eq(0).sum()),
            "1": int(event_count.eq(1).sum()),
            "2": int(event_count.eq(2).sum()),
            "3+": int(event_count.ge(3).sum()),
        },
        "pivot_event_rows": int(pivot_count.gt(0).sum()),
    }

    for regime in REGIMES:
        mask = df["regime"].eq(regime)
        result["regime_signal_counts"][regime] = {
            col: int(flags.loc[mask, col].sum())
            for col in SIGNALS
        }

    return result


def load_and_audit(symbol):
    path = DATA_DIR / f"{symbol}_15m_price_action_signals.csv"
    if not path.is_file():
        raise FileNotFoundError(path)

    df = pd.read_csv(path)
    return audit_frame(df, symbol)


def build_report(results):
    lines = [
        "# Price Action V1 — Signal Quality and Distribution Audit",
        "",
        "Purpose: descriptive analysis of signal frequency and overlap.",
        "",
        "This report does not measure trade profitability or predict future returns.",
        "Pivot confirmations are structural events, not entry signals.",
        "",
        "## 1. Asset summary",
        "",
        "| Asset | Rows | Candles with signals | Total signal events | Multi-signal candles | Max signals on one candle | Pivot-event candles |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for r in results:
        lines.append(
            f"| {r['symbol']} | {r['rows']:,} | {r['event_rows']:,} "
            f"| {r['total_events']:,} | {r['multi_signal_rows']:,} "
            f"| {r['max_signals_per_candle']} | {r['pivot_event_rows']:,} |"
        )

    lines.extend([
        "",
        "## 2. Signal counts by asset",
        "",
        "| Asset | " + " | ".join(SIGNALS) + " |",
        "|---|" + "|".join(["---:"] * len(SIGNALS)) + "|",
    ])

    for r in results:
        values = [f"{r['signal_counts'][s]:,}" for s in SIGNALS]
        lines.append("| " + r["symbol"] + " | " + " | ".join(values) + " |")

    lines.extend([
        "",
        "## 3. Pivot confirmations by asset",
        "",
        "| Asset | Confirmed pivot highs | Confirmed pivot lows |",
        "|---|---:|---:|",
    ])

    for r in results:
        lines.append(
            f"| {r['symbol']} | {r['pivot_counts']['pivot_high_confirmed']:,} "
            f"| {r['pivot_counts']['pivot_low_confirmed']:,} |"
        )

    lines.extend([
        "",
        "## 4. Signal counts by market regime",
        "",
        "Counts below are event counts, not unique candles.",
        "",
    ])

    for regime in REGIMES:
        lines.extend([
            f"### {regime}",
            "",
            "| Asset | " + " | ".join(SIGNALS) + " |",
            "|---|" + "|".join(["---:"] * len(SIGNALS)) + "|",
        ])
        for r in results:
            values = [
                f"{r['regime_signal_counts'][regime][s]:,}"
                for s in SIGNALS
            ]
            lines.append(
                "| " + r["symbol"] + " | " + " | ".join(values) + " |"
            )
        lines.append("")

    lines.extend([
        "## 5. Signal overlap",
        "",
        "| Asset | No signals | Exactly 1 | Exactly 2 | 3 or more |",
        "|---|---:|---:|---:|---:|",
    ])

    for r in results:
        d = r["overlap_distribution"]
        lines.append(
            f"| {r['symbol']} | {d['0']:,} | {d['1']:,} "
            f"| {d['2']:,} | {d['3+']:,} |"
        )

    lines.extend([
        "",
        "## 6. Regime candle coverage",
        "",
        "| Asset | " + " | ".join(REGIMES) + " |",
        "|---|" + "|".join(["---:"] * len(REGIMES)) + "|",
    ])

    for r in results:
        values = [
            f"{r['regime_rows'].get(regime, 0):,}"
            for regime in REGIMES
        ]
        lines.append("| " + r["symbol"] + " | " + " | ".join(values) + " |")

    lines.extend([
        "",
        "## Interpretation and limitations",
        "",
        "- High signal frequency does not imply profitability.",
        "- Multiple signals on one candle are counted separately as events.",
        "- Multi-signal candle counts identify overlap, not independent opportunities.",
        "- Regime counts depend on the available historical regime labels.",
        "- WARMUP and NO_REGIME_AVAILABLE observations are reported separately.",
        "- This audit does not evaluate entries, stops, targets, fees, slippage, or funding.",
        "- No strategy selection or parameter optimization is performed.",
        "",
        "The five input CSVs remain local and are not committed to Git.",
        "",
    ])

    return "\n".join(lines)


def main():
    results = []

    for symbol in SYMBOLS:
        result = load_and_audit(symbol)
        results.append(result)
        print(
            f"{symbol}: rows={result['rows']:,}, "
            f"events={result['total_events']:,}, "
            f"signal candles={result['event_rows']:,}, "
            f"overlap candles={result['multi_signal_rows']:,}, "
            f"max signals/candle={result['max_signals_per_candle']}"
        )

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build_report(results), encoding="utf-8")

    print("\n===== SIGNAL QUALITY AUDIT COMPLETE =====")
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
