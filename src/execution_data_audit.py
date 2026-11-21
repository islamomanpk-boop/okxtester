"""Audit 1-minute execution candles and funding-data availability."""

from pathlib import Path
import pandas as pd

DATA = Path.home() / "okx_scalping_data"
REPORT = Path("reports/execution_data_audit.md")
SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
REQUIRED = ["ts", "open", "high", "low", "close", "vol"]
INTERVAL_MS = 60_000


def audit_frame(df, symbol):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"{symbol}: missing columns {missing}")
    if df.empty:
        raise ValueError(f"{symbol}: empty dataset")

    result = df[REQUIRED].copy()
    ts = pd.to_numeric(result["ts"], errors="coerce")

    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{symbol}: invalid timestamps")

    result["ts"] = ts.astype("int64")

    if result["ts"].duplicated().any():
        raise ValueError(f"{symbol}: duplicate timestamps")

    if not result["ts"].is_monotonic_increasing:
        raise ValueError(f"{symbol}: timestamps not chronological")

    gaps = result["ts"].diff().dropna()
    unexpected = int((gaps != INTERVAL_MS).sum())

    for col in REQUIRED[1:]:
        result[col] = pd.to_numeric(result[col], errors="coerce")

    if result[REQUIRED[1:]].isna().any().any():
        raise ValueError(f"{symbol}: missing or invalid OHLCV values")

    prices = result[["open", "high", "low", "close"]]
    if (prices <= 0).any().any():
        raise ValueError(f"{symbol}: non-positive prices")

    if (result["vol"] < 0).any():
        raise ValueError(f"{symbol}: negative volume")

    invalid = (
        (result["high"] < prices[["open", "close", "low"]].max(axis=1))
        | (result["low"] > prices[["open", "close", "high"]].min(axis=1))
    )
    if invalid.any():
        raise ValueError(f"{symbol}: invalid OHLC structure")

    return {
        "symbol": symbol,
        "rows": len(result),
        "first_utc": pd.to_datetime(result["ts"].iloc[0], unit="ms", utc=True),
        "last_utc": pd.to_datetime(result["ts"].iloc[-1], unit="ms", utc=True),
        "duplicates": int(result["ts"].duplicated().sum()),
        "unexpected_intervals": unexpected,
        "missing_minutes": unexpected,
        "first_ts": int(result["ts"].iloc[0]),
        "last_ts": int(result["ts"].iloc[-1]),
    }


def main():
    results = []
    issues = []

    print("===== EXECUTION DATA AUDIT =====")

    for symbol in SYMBOLS:
        path = DATA / f"{symbol}_USDT_USDT_1m.csv"
        if not path.is_file():
            issues.append(f"{symbol}: file missing: {path}")
            continue

        try:
            df = pd.read_csv(path)
            result = audit_frame(df, symbol)
            results.append(result)

            print(
                f"{symbol}: rows={result['rows']:,}, "
                f"unexpected intervals={result['unexpected_intervals']}, "
                f"first={result['first_utc']}, "
                f"last={result['last_utc']}"
            )

            if result["unexpected_intervals"]:
                issues.append(
                    f"{symbol}: {result['unexpected_intervals']} "
                    "unexpected one-minute intervals"
                )

        except Exception as exc:
            issues.append(f"{symbol}: {exc}")
            print(f"{symbol}: ERROR: {exc}")

    if len(results) != len(SYMBOLS):
        issues.append("Not all five execution datasets passed loading.")

    funding_files = sorted(
        p for p in DATA.rglob("*")
        if p.is_file() and "funding" in p.name.lower()
    )

    funding_status = (
        "FOUND — requires schema and coverage validation"
        if funding_files else
        "NOT FOUND — funding costs must not be assumed to be zero"
    )

    REPORT.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# 1-Minute Execution Data and Funding Audit",
        "",
        f"Funding data status: **{funding_status}**",
        "",
        "## Execution candle results",
        "",
        "| Asset | Rows | First UTC | Last UTC | Unexpected intervals |",
        "|---|---:|---|---|---:|",
    ]

    for r in results:
        lines.append(
            f"| {r['symbol']} | {r['rows']:,} | {r['first_utc']} "
            f"| {r['last_utc']} | {r['unexpected_intervals']} |"
        )

    lines.extend([
        "",
        "## Funding data",
        "",
    ])

    if funding_files:
        lines.extend(f"- `{p}`" for p in funding_files)
    else:
        lines.append(
            "No funding-related files were found in the local data directory."
        )

    lines.extend([
        "",
        "Funding must be obtained and validated separately before claiming "
        "fully cost-adjusted perpetual-swap backtest results.",
        "",
        "## Execution assumptions required by the backtester",
        "",
        "- 15-minute signals become executable only after candle close.",
        "- Market-style entries use the next eligible 1-minute open.",
        "- Limit fills must be checked using 1-minute OHLCV.",
        "- Stop-loss takes priority if stop and target are both touched "
        "within one 1-minute candle.",
        "- Maker/taker fees and slippage must be explicit configuration.",
        "- Missing funding data must be reported, never silently set to zero.",
        "",
        "## Issues",
        "",
    ])

    lines.extend(
        [f"- {issue}" for issue in issues] if issues else ["None detected."]
    )

    lines.extend([
        "",
        "Raw execution CSV files remain local and are not committed to Git.",
        "",
    ])

    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("\n===== AUDIT RESULT =====")
    print("Execution datasets checked:", len(results))
    print("Funding files found:", len(funding_files))
    print("Issues:", len(issues))
    print("Report:", REPORT)

    if issues:
        for issue in issues:
            print("-", issue)
        raise SystemExit(1)

    print("Execution data audit completed successfully.")


if __name__ == "__main__":
    main()
