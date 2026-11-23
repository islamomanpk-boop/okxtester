#!/usr/bin/env python3
"""Read-only comparison of standalone 4H CSVs vs 4H bars resampled from 1M.

Standalone source:
  ~/okx_adaptive_bot/data/{ASSET}_USDT_4h.csv

1M source:
  ~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv

Uses the archived breakout script's exact 4H resampling convention:
  4h, origin=epoch, label=left, closed=left, exactly 240 1M closes.

No files are written or modified. Missing source files cause a clear stop.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
ONE_MINUTE_DIR = Path.home() / "okx_scalping_data"
STANDALONE_4H_DIR = Path.home() / "okx_adaptive_bot" / "data"
FOUR_HOURS_MS = 4 * 60 * 60 * 1000
OHLC = ["open", "high", "low", "close"]


def load_one_minute(asset: str) -> pd.DataFrame:
    path = ONE_MINUTE_DIR / f"{asset}_USDT_USDT_1m.csv"
    d = pd.read_csv(path, usecols=["ts", *OHLC])
    ts = pd.to_numeric(d["ts"], errors="coerce")
    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{asset}: invalid 1M timestamps in {path}")
    d["ts"] = ts.astype("int64")
    for col in OHLC:
        d[col] = pd.to_numeric(d[col], errors="coerce")
    if not np.isfinite(d[["ts", *OHLC]].to_numpy(dtype=float)).all():
        raise ValueError(f"{asset}: non-finite 1M timestamp/OHLC value")
    if d["ts"].duplicated().any():
        raise ValueError(f"{asset}: duplicate 1M timestamps")
    d["ts"] = pd.to_datetime(d["ts"], unit="ms", utc=True)
    return d.set_index("ts").sort_index()


def resample_4h(one: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    bars = one.resample(
        "4h", origin="epoch", label="left", closed="left"
    ).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
    })
    counts = one["close"].resample(
        "4h", origin="epoch", label="left", closed="left"
    ).count()
    complete = bars.loc[counts.eq(240)].copy()
    return complete, int((~counts.eq(240)).sum())


def load_standalone_4h(asset: str) -> pd.DataFrame:
    path = STANDALONE_4H_DIR / f"{asset}_USDT_4h.csv"
    d = pd.read_csv(path, usecols=["ts", *OHLC])
    ts = pd.to_numeric(d["ts"], errors="coerce")
    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{asset}: invalid standalone 4H timestamps in {path}")
    d["ts"] = ts.astype("int64")
    if (d["ts"] % FOUR_HOURS_MS != 0).any():
        raise ValueError(f"{asset}: standalone 4H timestamps are not epoch-aligned")
    for col in OHLC:
        d[col] = pd.to_numeric(d[col], errors="coerce")
    if not np.isfinite(d[["ts", *OHLC]].to_numpy(dtype=float)).all():
        raise ValueError(f"{asset}: non-finite standalone 4H timestamp/OHLC value")
    if d["ts"].duplicated().any():
        raise ValueError(f"{asset}: duplicate standalone 4H timestamps")
    d["ts"] = pd.to_datetime(d["ts"], unit="ms", utc=True)
    return d.set_index("ts").sort_index()


def main() -> None:
    missing = []
    for asset in ASSETS:
        p1 = ONE_MINUTE_DIR / f"{asset}_USDT_USDT_1m.csv"
        p4 = STANDALONE_4H_DIR / f"{asset}_USDT_4h.csv"
        if not p1.is_file():
            missing.append(str(p1))
        if not p4.is_file():
            missing.append(str(p4))
    if missing:
        print("STOP: required source file(s) are missing. No comparison performed.")
        for path in missing:
            print("MISSING:", path)
        return

    print("READ-ONLY 4H SOURCE PROVENANCE COMPARISON")
    print("Standalone 4H vs 4H resampled from 1M.")
    print("Resampling: epoch-aligned, left-labeled/left-closed, exactly 240 1M rows.")
    print("No files will be written or modified.")
    print("")

    for asset in ASSETS:
        one = load_one_minute(asset)
        resampled, incomplete_bins = resample_4h(one)
        standalone = load_standalone_4h(asset)

        common = standalone.index.intersection(resampled.index).sort_values()
        standalone_only = standalone.index.difference(resampled.index)
        resampled_only = resampled.index.difference(standalone.index)

        print("=" * 88)
        print(f"{asset}")
        print(f"1M rows: {len(one):,}")
        print(f"Resampled complete 4H rows: {len(resampled):,}")
        print(f"Resampling bins not containing exactly 240 rows: {incomplete_bins:,}")
        print(f"Standalone 4H rows: {len(standalone):,}")
        print(f"Common 4H timestamps: {len(common):,}")
        print(f"Standalone-only timestamps: {len(standalone_only):,}")
        print(f"Resampled-only timestamps: {len(resampled_only):,}")

        if len(common) == 0:
            print("NO COMMON 4H TIMESTAMPS — OHLC comparison unavailable.")
            continue

        left = standalone.loc[common, OHLC].astype(float)
        right = resampled.loc[common, OHLC].astype(float)
        diff = left - right
        exact_row = left.eq(right).all(axis=1)
        close_row = np.isclose(
            left.to_numpy(), right.to_numpy(), rtol=1e-10, atol=1e-10
        ).all(axis=1)
        mismatch = ~close_row

        print(f"Exact OHLC-identical rows: {int(exact_row.sum()):,}/{len(common):,}")
        print(f"OHLC rows equal within rtol=1e-10, atol=1e-10: {int(close_row.sum()):,}/{len(common):,}")
        print(f"Rows differing beyond tolerance: {int(mismatch.sum()):,}")

        for col in OHLC:
            values = diff[col].abs().to_numpy()
            max_abs = float(values.max()) if len(values) else 0.0
            mean_abs = float(values.mean()) if len(values) else 0.0
            print(f"{col.upper()} max_abs_diff={max_abs:.12g} mean_abs_diff={mean_abs:.12g}")

        if mismatch.any():
            sample_times = common[np.flatnonzero(mismatch)[:5]]
            print("First differing rows (standalone | resampled):")
            for ts in sample_times:
                a = left.loc[ts]
                b = right.loc[ts]
                print(
                    f"  {ts}: "
                    + " ".join(
                        f"{c}={a[c]:.12g}|{b[c]:.12g}" for c in OHLC
                    )
                )
        else:
            print("No OHLC differences beyond tolerance on common timestamps.")

        if len(standalone_only):
            print("First standalone-only timestamps:", list(standalone_only[:5]))
        if len(resampled_only):
            print("First resampled-only timestamps:", list(resampled_only[:5]))

    print("")
    print("END: source comparison only; no event masks, controls, forward outcomes, or PnL.")


if __name__ == "__main__":
    main()
