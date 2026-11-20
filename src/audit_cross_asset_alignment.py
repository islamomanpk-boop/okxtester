from pathlib import Path
import pandas as pd
import sys

DATA = Path.home() / "okx_scalping_data"
REPORTS = Path("reports")
SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
INTERVAL_MS = 60_000

REPORTS.mkdir(exist_ok=True)

timestamps = {}
issues = []
summary = []

print("===== CROSS-ASSET TIMESTAMP AUDIT =====")

for symbol in SYMBOLS:
    path = DATA / f"{symbol}_USDT_USDT_1m.csv"
    print(f"\nChecking {symbol}...")

    try:
        df = pd.read_csv(path, usecols=["ts"])
        ts = pd.to_numeric(df["ts"], errors="coerce")

        if ts.isna().any():
            raise ValueError("Invalid timestamps found")

        if (ts % 1 != 0).any():
            raise ValueError("Non-integer timestamps found")

        values = ts.astype("int64")

        duplicates = int(values.duplicated().sum())
        out_of_order = int((values.diff().dropna() <= 0).sum())
        gaps = int((values.diff().dropna() != INTERVAL_MS).sum())

        timestamps[symbol] = set(values.tolist())

        first = int(values.iloc[0])
        last = int(values.iloc[-1])

        summary.append({
            "symbol": symbol,
            "rows": len(values),
            "unique_timestamps": len(timestamps[symbol]),
            "first_utc": pd.to_datetime(first, unit="ms", utc=True),
            "last_utc": pd.to_datetime(last, unit="ms", utc=True),
            "duplicates": duplicates,
            "out_of_order": out_of_order,
            "unexpected_intervals": gaps,
        })

        print(f"Rows: {len(values):,}")
        print(f"Duplicates: {duplicates}")
        print(f"Out of order: {out_of_order}")
        print(f"Unexpected intervals: {gaps}")

        if duplicates or out_of_order or gaps:
            issues.append(f"{symbol}: timestamp integrity problem")

    except Exception as e:
        issues.append(f"{symbol}: {e}")
        print(f"FAIL: {e}")

if len(timestamps) != len(SYMBOLS):
    print("\nFAIL: Not all five datasets could be checked.")
    sys.exit(1)

union = set.union(*timestamps.values())
intersection = set.intersection(*timestamps.values())

print("\n===== CROSS-ASSET ALIGNMENT =====")
print(f"Union timestamps: {len(union):,}")
print(f"Common timestamps: {len(intersection):,}")

for symbol in SYMBOLS:
    missing = union - timestamps[symbol]
    extra = timestamps[symbol] - intersection

    print(
        f"{symbol}: missing from union timeline={len(missing):,}, "
        f"not common to all={len(extra):,}"
    )

    if missing:
        issues.append(f"{symbol}: missing timestamps")

alignment_rows = []
for item in summary:
    item["timestamps_common_to_all"] = len(intersection)
    item["timestamps_not_common"] = (
        len(union - timestamps[item["symbol"]])
        + len(timestamps[item["symbol"]] - intersection)
    )
    alignment_rows.append(item)

pd.DataFrame(alignment_rows).to_csv(
    REPORTS / "cross_asset_timestamp_alignment.csv",
    index=False
)

exception_rows = []
for value in sorted(union - intersection):
    missing_symbols = [
        symbol for symbol in SYMBOLS
        if value not in timestamps[symbol]
    ]
    exception_rows.append({
        "timestamp_utc": pd.to_datetime(value, unit="ms", utc=True),
        "missing_symbols": ",".join(missing_symbols),
    })

pd.DataFrame(
    exception_rows,
    columns=["timestamp_utc", "missing_symbols"]
).to_csv(
    REPORTS / "cross_asset_timestamp_exceptions.csv",
    index=False
)

same = all(timestamps[s] == timestamps[SYMBOLS[0]] for s in SYMBOLS)

if not same:
    issues.append("The five timestamp sets are not identical")

status = "PASS" if not issues else "FAIL"

lines = [
    "# Cross-Asset Timestamp Alignment Audit",
    "",
    f"Status: **{status}**",
    "",
    f"- Assets checked: {', '.join(SYMBOLS)}",
    f"- Union timestamps: {len(union):,}",
    f"- Common timestamps: {len(intersection):,}",
    f"- Identical timestamp sets: {same}",
    "",
    "## Per-asset results",
    "",
    "| Asset | Rows | Duplicates | Out of order | Unexpected intervals |",
    "|---|---:|---:|---:|---:|",
]

for item in summary:
    lines.append(
        f"| {item['symbol']} | {item['rows']} | "
        f"{item['duplicates']} | {item['out_of_order']} | "
        f"{item['unexpected_intervals']} |"
    )

lines += ["", "## Issues", ""]
lines += [f"- {issue}" for issue in issues] if issues else ["None detected."]
lines += [
    "",
    "No missing candles were fabricated or forward-filled.",
    "",
    "This audit checks timestamp alignment, not strategy profitability.",
]

(REPORTS / "cross_asset_timestamp_alignment.md").write_text(
    "\n".join(lines) + "\n"
)

print("\n===== FINAL RESULT =====")
print(status)

if issues:
    for issue in issues:
        print("-", issue)
    sys.exit(1)

print("All five assets have identical, continuous timestamps.")
