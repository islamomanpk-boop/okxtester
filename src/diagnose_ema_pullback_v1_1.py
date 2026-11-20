#!/usr/bin/env python3

import os
import glob
import pandas as pd
import numpy as np

REPORTS = "reports"
OUTPUT = os.path.join(REPORTS, "ema_v1_1_diagnostics")

os.makedirs(OUTPUT, exist_ok=True)

files = sorted(glob.glob(
    os.path.join(
        REPORTS,
        "*_EMA_PULLBACK_V1_1_*R_trades.csv"
    )
))

print("\n===== EMA PULLBACK V1.1 DIAGNOSTICS =====")

if not files:
    raise SystemExit("ERROR: No trade files found.")

frames = []

for file in files:
    df = pd.read_csv(file)

    required = [
        "symbol", "target_r", "side",
        "entry_time", "exit_time",
        "gross_pnl", "total_fees", "net_pnl",
        "exit_reason"
    ]

    missing = [c for c in required if c not in df.columns]

    if missing:
        print("Skipping", file, "Missing:", missing)
        continue

    frames.append(df)

if not frames:
    raise SystemExit("ERROR: No valid trade files.")

trades = pd.concat(frames, ignore_index=True)

# Parse timestamps and derive diagnostic fields.
trades["entry_time"] = pd.to_datetime(
    trades["entry_time"], utc=True, errors="coerce"
)

trades["exit_time"] = pd.to_datetime(
    trades["exit_time"], utc=True, errors="coerce"
)

trades["holding_minutes"] = (
    trades["exit_time"] - trades["entry_time"]
).dt.total_seconds() / 60

trades["entry_hour_utc"] = trades["entry_time"].dt.hour
trades["entry_weekday"] = trades["entry_time"].dt.day_name()
trades["entry_month"] = trades["entry_time"].dt.strftime("%Y-%m")

trades["side"] = trades["side"].astype(str).str.upper()
trades["exit_reason"] = (
    trades["exit_reason"].astype(str).str.upper()
)

# Statistics helper.
def summarize(data, keys):
    result = (
        data.groupby(keys, dropna=False)
        .agg(
            trades=("net_pnl", "size"),
            wins=("net_pnl", lambda x: (x > 0).sum()),
            losses=("net_pnl", lambda x: (x < 0).sum()),
            win_rate_pct=(
                "net_pnl",
                lambda x: (x > 0).mean() * 100
            ),
            gross_pnl=("gross_pnl", "sum"),
            fees=("total_fees", "sum"),
            net_pnl=("net_pnl", "sum"),
            average_net=("net_pnl", "mean"),
            average_win=(
                "net_pnl",
                lambda x: x[x > 0].mean()
            ),
            average_loss=(
                "net_pnl",
                lambda x: x[x < 0].mean()
            ),
            median_holding_minutes=(
                "holding_minutes", "median"
            )
        )
        .reset_index()
    )

    def pf(row):
        # Calculate PF from individual trades below.
        return row

    # Calculate profit factors accurately.
    pf_rows = []

    for name, group in data.groupby(keys, dropna=False):
        if not isinstance(name, tuple):
            name = (name,)

        positive = group.loc[
            group["net_pnl"] > 0, "net_pnl"
        ].sum()

        negative = -group.loc[
            group["net_pnl"] < 0, "net_pnl"
        ].sum()

        gross_positive = group.loc[
            group["gross_pnl"] > 0, "gross_pnl"
        ].sum()

        gross_negative = -group.loc[
            group["gross_pnl"] < 0, "gross_pnl"
        ].sum()

        pf_rows.append({
            **dict(zip(keys, name)),
            "net_profit_factor": (
                positive / negative if negative else np.nan
            ),
            "gross_profit_factor": (
                gross_positive / gross_negative
                if gross_negative else np.nan
            )
        })

    if pf_rows:
        result = result.merge(
            pd.DataFrame(pf_rows),
            on=keys,
            how="left"
        )

    return result


def show(title, data, keys, filename):
    print("\n" + "=" * 75)
    print(title)
    print("=" * 75)

    result = summarize(data, keys)

    print(result.round(3).to_string(index=False))

    result.to_csv(
        os.path.join(OUTPUT, filename),
        index=False
    )

    return result


# 1. Direction performance.
show(
    "1. LONG VS SHORT PERFORMANCE",
    trades,
    ["symbol", "target_r", "side"],
    "by_direction.csv"
)

# 2. Stop versus target performance.
show(
    "2. STOP VS TARGET PERFORMANCE",
    trades,
    ["symbol", "target_r", "exit_reason"],
    "by_exit_reason.csv"
)

# 3. Individual coin and target performance.
show(
    "3. OVERALL CONFIGURATION PERFORMANCE",
    trades,
    ["symbol", "target_r"],
    "by_configuration.csv"
)

# 4. Performance by UTC entry hour.
hour_data = show(
    "4. PERFORMANCE BY ENTRY HOUR (UTC)",
    trades,
    ["symbol", "target_r", "entry_hour_utc"],
    "by_hour.csv"
)

# 5. Performance by weekday.
show(
    "5. PERFORMANCE BY WEEKDAY",
    trades,
    ["symbol", "target_r", "entry_weekday"],
    "by_weekday.csv"
)

# 6. Performance by month.
show(
    "6. PERFORMANCE BY MONTH",
    trades,
    ["symbol", "target_r", "entry_month"],
    "by_month.csv"
)

# 7. Holding-time analysis.
print("\n" + "=" * 75)
print("7. HOLDING TIME")
print("=" * 75)

holding = (
    trades.groupby(["symbol", "target_r"])
    ["holding_minutes"]
    .agg(["count", "mean", "median", "min", "max"])
    .reset_index()
)

print(holding.round(2).to_string(index=False))

holding.to_csv(
    os.path.join(OUTPUT, "holding_time.csv"),
    index=False
)

# 8. Trading cost analysis.
print("\n" + "=" * 75)
print("8. TRADING COST ANALYSIS")
print("=" * 75)

costs = (
    trades.groupby(["symbol", "target_r"])
    .agg(
        trades=("net_pnl", "size"),
        gross_pnl=("gross_pnl", "sum"),
        total_fees=("total_fees", "sum"),
        net_pnl=("net_pnl", "sum")
    )
    .reset_index()
)

costs["fees_pct_of_gross_profit"] = np.where(
    costs["gross_pnl"] > 0,
    costs["total_fees"] / costs["gross_pnl"] * 100,
    np.nan
)

print(costs.round(3).to_string(index=False))

costs.to_csv(
    os.path.join(OUTPUT, "cost_analysis.csv"),
    index=False
)

# 9. Data integrity checks.
print("\n" + "=" * 75)
print("9. DATA INTEGRITY")
print("=" * 75)

print("Files loaded:", len(files))
print("Total trade records:", len(trades))
print("Duplicate rows:", trades.duplicated().sum())
print("Missing entry times:", trades["entry_time"].isna().sum())
print("Missing exit times:", trades["exit_time"].isna().sum())
print("Negative holding times:", (
    trades["holding_minutes"] < 0
).sum())
print("Zero-minute trades:", (
    trades["holding_minutes"] == 0
).sum())
print("Missing PnL:", trades["net_pnl"].isna().sum())

# Save combined enriched trade records.
trades.to_csv(
    os.path.join(OUTPUT, "all_trades_enriched.csv"),
    index=False
)

print("\n===== DIAGNOSTIC COMPLETE =====")
print("Output directory:", OUTPUT)
print("Original trade files were not modified.")
