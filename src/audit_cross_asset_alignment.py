from pathlib import Path
import sys
import pandas as pd

DATA = Path.home() / "okx_scalping_data"
REPORTS = Path("reports")
SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
INTERVAL_MS = 60_000
REQUIRED = ["ts", "open", "high", "low", "close", "vol"]

REPORTS.mkdir(exist_ok=True)

frames = {}
timestamp_sets = {}
summary = []
issues = []

print("===== CROSS-ASSET AUDIT V2 =====")

for symbol in SYMBOLS:
    path = DATA / f"{symbol}_USDT_USDT_1m.csv"
    print(f"\nChecking {symbol}: {path}")

    try:
        df = pd.read_csv(path)

        missing_columns = [c for c in REQUIRED if c not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")

        ts = pd.to_numeric(df["ts"], errors="coerce")

        if ts.isna().any():
            raise ValueError("Invalid timestamps")
        if (ts % 1 != 0).any():
            raise ValueError("Non-integer timestamps")

        df["ts"] = ts.astype("int64")

        duplicates = int(df["ts"].duplicated().sum())
        out_of_order = int((df["ts"].diff().dropna() <= 0).sum())
        unexpected_intervals = int(
            (df["ts"].diff().dropna() != INTERVAL_MS).sum()
        )

        timestamp_sets[symbol] = set(df["ts"].tolist())

        summary.append({
            "symbol": symbol,
            "rows": len(df),
            "unique_timestamps": len(timestamp_sets[symbol]),
            "first_utc": pd.to_datetime(df["ts"].iloc[0], unit="ms", utc=True),
            "last_utc": pd.to_datetime(df["ts"].iloc[-1], unit="ms", utc=True),
            "duplicates": duplicates,
            "out_of_order": out_of_order,
            "unexpected_intervals": unexpected_intervals,
        })

        if duplicates or out_of_order or unexpected_intervals:
            issues.append(
                f"{symbol}: duplicate={duplicates}, "
                f"out_of_order={out_of_order}, "
                f"unexpected_intervals={unexpected_intervals}"
            )

        frames[symbol] = df[REQUIRED].copy()
        print(f"Rows: {len(df):,}")
        print(f"Duplicates: {duplicates}")
        print(f"Out of order: {out_of_order}")
        print(f"Unexpected intervals: {unexpected_intervals}")

    except Exception as exc:
        issues.append(f"{symbol}: {exc}")
        print(f"ERROR: {exc}")

if len(frames) != len(SYMBOLS):
    print("\nFAIL: Could not load all five datasets.")
    sys.exit(1)

union = set.union(*timestamp_sets.values())
common = set.intersection(*timestamp_sets.values())
common_sorted = sorted(common)

if not common_sorted:
    issues.append("No common timestamps across all assets")
else:
    common_start = common_sorted[0]
    common_end = common_sorted[-1]

    internal_exceptions = [
        ts for ts in union - common
        if common_start <= ts <= common_end
    ]

    if internal_exceptions:
        issues.append(
            f"{len(internal_exceptions)} unmatched timestamps "
            "inside the common time range"
        )

    common_gaps = sum(
        (b - a) != INTERVAL_MS
        for a, b in zip(common_sorted, common_sorted[1:])
    )

    if common_gaps:
        issues.append(
            f"Common timeline contains {common_gaps} unexpected intervals"
        )

trailing_only = not any(
    common_sorted[0] <= ts <= common_sorted[-1]
    for ts in union - common
) if common_sorted else False

# Build a wide dataset using exact timestamp matches only.
combined = None

for symbol in SYMBOLS:
    part = frames[symbol].copy()
    part = part.rename(columns={
        col: f"{symbol}_{col}"
        for col in ["open", "high", "low", "close", "vol"]
    })

    if combined is None:
        combined = part
    else:
        combined = combined.merge(
            part,
            on="ts",
            how="inner",
            validate="one_to_one"
        )

combined = combined.sort_values("ts").reset_index(drop=True)

if len(combined) != len(common):
    issues.append(
        f"Combined dataset has {len(combined)} rows, "
        f"but timestamp intersection has {len(common)}"
    )

if len(combined) > 0:
    combined_gaps = int(
        (combined["ts"].diff().dropna() != INTERVAL_MS).sum()
    )
    if combined_gaps:
        issues.append(
            f"Combined dataset has {combined_gaps} unexpected intervals"
        )

# Save synchronized data locally, not in GitHub.
output_path = DATA / "synchronized_5asset_1m.csv"
combined.to_csv(output_path, index=False)

# Save reports.
summary_df = pd.DataFrame(summary)
summary_df["timestamps_common_to_all"] = len(common)
summary_df["timestamps_not_common"] = [
    len(union - timestamp_sets[symbol])
    + len(timestamp_sets[symbol] - common)
    for symbol in SYMBOLS
]
summary_df.to_csv(
    REPORTS / "cross_asset_timestamp_alignment.csv",
    index=False
)

exception_rows = []
for ts in sorted(union - common):
    exception_rows.append({
        "timestamp_utc": pd.to_datetime(ts, unit="ms", utc=True),
        "missing_symbols": ",".join(
            s for s in SYMBOLS if ts not in timestamp_sets[s]
        )
    })

pd.DataFrame(
    exception_rows,
    columns=["timestamp_utc", "missing_symbols"]
).to_csv(
    REPORTS / "cross_asset_timestamp_exceptions.csv",
    index=False
)

if issues:
    status = "FAIL"
elif union == common:
    status = "PASS"
else:
    status = "PASS_WITH_TRAILING_DIFFERENCES"

lines = [
    "# Cross-Asset Timestamp Alignment Audit",
    "",
    f"Status: **{status}**",
    "",
    f"- Assets: {', '.join(SYMBOLS)}",
    f"- Union timestamps: {len(union):,}",
    f"- Common timestamps: {len(common):,}",
    f"- Combined dataset rows: {len(combined):,}",
    f"- Trailing-only differences: {trailing_only}",
    f"- Synchronized dataset: `{output_path}`",
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
lines += [f"- {x}" for x in issues] if issues else ["None detected."]
lines += [
    "",
    "Only exact common timestamps were retained.",
    "No forward filling or fabricated candles were used.",
    "Original source CSV files were not modified.",
    "",
    "This audit checks data alignment, not strategy profitability.",
]

(REPORTS / "cross_asset_timestamp_alignment.md").write_text(
    "\n".join(lines) + "\n"
)

print("\n===== FINAL RESULT =====")
print("Status:", status)
print("Common timestamps:", f"{len(common):,}")
print("Combined rows:", f"{len(combined):,}")
print("Local dataset:", output_path)

if issues:
    for issue in issues:
        print("-", issue)
    sys.exit(1)

print("\nAudit completed successfully.")
