#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(".")
REPORTS = ROOT / "reports"

SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

def profit_factor(values):
    wins = values[values > 0].sum()
    losses = abs(values[values < 0].sum())
    if losses == 0:
        return np.nan if wins == 0 else np.inf
    return wins / losses

def summarize(group):
    net = group["net_pnl"]
    planned_risk = group["planned_risk_cash"].sum()

    return pd.Series({
        "trades": len(group),
        "wins": int((net > 0).sum()),
        "losses": int((net < 0).sum()),
        "win_rate_pct": (net > 0).mean() * 100,
        "gross_pnl": group["gross_pnl"].sum(),
        "total_fees": group["total_fees"].sum(),
        "net_pnl": net.sum(),
        "net_profit_factor": profit_factor(net),
        "average_net_per_trade": net.mean(),
        "average_holding_hours": group["holding_hours"].mean(),
        "average_notional": group["notional"].mean(),
        "fees_pct_of_planned_risk": (
            group["total_fees"].sum() / planned_risk * 100
            if planned_risk else np.nan
        ),
    })

def main():
    all_trades = []
    regime_frames = {}

    print("\n===== LOADING REGIME FILES =====")

    for symbol in SYMBOLS:
        path = REPORTS / f"{symbol}_regimes.csv"

        if not path.exists():
            raise FileNotFoundError(f"Missing regime file: {path}")

        regime = pd.read_csv(path)

        required = {"available_at", "regime", "symbol"}
        missing = required - set(regime.columns)

        if missing:
            raise ValueError(f"{path} missing columns: {missing}")

        regime["available_at"] = pd.to_datetime(
            regime["available_at"], utc=True
        )

        regime = regime.dropna(subset=["available_at"])
        regime = regime.sort_values("available_at")

        if regime["available_at"].duplicated().any():
            raise ValueError(f"Duplicate regime availability timestamps: {symbol}")

        regime_frames[symbol] = regime[
            ["available_at", "regime"]
        ].copy()

        print(
            f"{symbol}: {len(regime)} regime records, "
            f"latest available {regime['available_at'].max()}"
        )

    print("\n===== LOADING UNLIMITED TRADES =====")

    for symbol in SYMBOLS:
        files = sorted(
            REPORTS.glob(
                f"{symbol}_EMA_PULLBACK_V1_1_*R_UNLIMITED_audited_trades.csv"
            )
        )

        if not files:
            raise FileNotFoundError(
                f"No UNLIMITED audited trade files for {symbol}"
            )

        for path in files:
            df = pd.read_csv(path)

            required = {
                "symbol", "target_r", "side", "entry_time",
                "exit_time", "holding_hours", "notional",
                "planned_risk_cash", "exit_reason",
                "gross_pnl", "total_fees", "net_pnl"
            }

            missing = required - set(df.columns)
            if missing:
                raise ValueError(f"{path} missing columns: {missing}")

            df["entry_time"] = pd.to_datetime(
                df["entry_time"], utc=True
            )
            df["exit_time"] = pd.to_datetime(
                df["exit_time"], utc=True
            )

            df["source_file"] = path.name
            all_trades.append(df)

            print(f"{path.name}: {len(df)} trades")

    trades = pd.concat(all_trades, ignore_index=True)

    if trades.empty:
        raise ValueError("No trades found.")

    numeric_columns = [
        "target_r", "holding_hours", "notional",
        "planned_risk_cash", "gross_pnl",
        "total_fees", "net_pnl"
    ]

    for col in numeric_columns:
        trades[col] = pd.to_numeric(trades[col], errors="coerce")

    if trades[numeric_columns].isna().any().any():
        raise ValueError("Missing or invalid numeric trade data detected.")

    print("\n===== MATCHING ENTRY TIMES TO AVAILABLE REGIMES =====")

    enriched = []

    for symbol in SYMBOLS:
        part = trades[trades["symbol"] == symbol].copy()

        if part.empty:
            continue

        regime = regime_frames[symbol]

        part = pd.merge_asof(
            part.sort_values("entry_time"),
            regime.sort_values("available_at"),
            left_on="entry_time",
            right_on="available_at",
            direction="backward",
            allow_exact_matches=True
        )

        matched = part["available_at"].notna()

        future_matches = (
            part.loc[matched, "available_at"]
            > part.loc[matched, "entry_time"]
        ).sum()

        if future_matches:
            raise AssertionError(
                f"Future regime match detected for {symbol}"
            )

        print(
            f"{symbol}: {matched.sum()} matched, "
            f"{(~matched).sum()} unmatched, "
            f"{future_matches} future matches"
        )

        enriched.append(part)

    trades = pd.concat(enriched, ignore_index=True)

    # Basic data-quality checks
    if (trades["total_fees"] < 0).any():
        raise ValueError("Negative fees detected.")

    if (trades["planned_risk_cash"] <= 0).any():
        raise ValueError("Invalid planned risk detected.")

    if not trades["side"].isin(["LONG", "SHORT"]).all():
        raise ValueError("Unexpected trade side found.")

    # Save the joined trade-level data
    enriched_path = REPORTS / "ema_pullback_unlimited_trades_with_regimes.csv"
    trades.to_csv(enriched_path, index=False)

    print("\n===== OVERALL PERFORMANCE =====")

    overall = (
        trades.groupby(["symbol", "target_r"], dropna=False)
        .apply(summarize, include_groups=False)
        .reset_index()
    )

    overall_path = REPORTS / "ema_pullback_diagnostic_overall.csv"
    overall.to_csv(overall_path, index=False)
    print(overall.round(3).to_string(index=False))

    print("\n===== PERFORMANCE BY DIRECTION AND EXIT =====")

    by_side_exit = (
        trades.groupby(
            ["symbol", "target_r", "side", "exit_reason"],
            dropna=False
        )
        .apply(summarize, include_groups=False)
        .reset_index()
    )

    side_path = REPORTS / "ema_pullback_diagnostic_by_side_exit.csv"
    by_side_exit.to_csv(side_path, index=False)
    print(by_side_exit.round(3).to_string(index=False))

    print("\n===== PERFORMANCE BY MARKET REGIME =====")

    by_regime = (
        trades.groupby(
            ["symbol", "target_r", "regime"],
            dropna=False
        )
        .apply(summarize, include_groups=False)
        .reset_index()
    )

    regime_path = REPORTS / "ema_pullback_diagnostic_by_regime.csv"
    by_regime.to_csv(regime_path, index=False)
    print(by_regime.round(3).to_string(index=False))

    print("\n===== EXIT REASON COUNTS =====")

    exits = (
        trades.groupby(
            ["symbol", "target_r", "exit_reason"]
        )
        .size()
        .unstack(fill_value=0)
    )

    print(exits.to_string())

    print("\n===== DATA QUALITY =====")
    print(f"Total trades: {len(trades)}")
    print(f"Unmatched regime trades: {trades['regime'].isna().sum()}")
    print(f"Future regime matches: 0")
    print(f"Symbols: {sorted(trades['symbol'].unique())}")
    print(f"Targets: {sorted(trades['target_r'].unique())}")

    print("\n===== REPORTS CREATED =====")
    print(enriched_path)
    print(overall_path)
    print(side_path)
    print(regime_path)

    print("\nDIAGNOSTIC COMPLETE.")

if __name__ == "__main__":
    main()
