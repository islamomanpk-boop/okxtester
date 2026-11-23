#!/usr/bin/env python3
"""V5: isolate the archived previous-15M-selected breakout gate.

Uses the exact historical 12-change absolute-price ER formula and compares:
  * quantiles from unique 4H feature rows vs joined 15M rows
  * current+same-snapshot crossing mask vs archived current+previous-selected
    +same-snapshot crossing mask

All other calculations are held fixed. Read-only: no controls, outcomes, PnL,
or file writes. This is a diagnostic, not an accepted event engine.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
BASE = Path.home() / "okx_scalping_data"
EXPECTED_COMMON = 569125
EXPECTED = {
    ("BTC","P25","LOWER"):62,("BTC","P25","UPPER"):81,
    ("BTC","P40","LOWER"):91,("BTC","P40","UPPER"):115,
    ("ETH","P25","LOWER"):51,("ETH","P25","UPPER"):51,
    ("ETH","P40","LOWER"):87,("ETH","P40","UPPER"):77,
    ("SOL","P25","LOWER"):77,("SOL","P25","UPPER"):71,
    ("SOL","P40","LOWER"):117,("SOL","P40","UPPER"):96,
    ("DOGE","P25","LOWER"):55,("DOGE","P25","UPPER"):65,
    ("DOGE","P40","LOWER"):81,("DOGE","P40","UPPER"):75,
    ("AVAX","P25","LOWER"):64,("AVAX","P25","UPPER"):83,
    ("AVAX","P40","LOWER"):84,("AVAX","P40","UPPER"):109,
}

def bars(one, rule, required):
    x = one.resample(rule, origin="epoch", label="left", closed="left").agg(
        {"open":"first","high":"max","low":"min","close":"last"})
    n = one["close"].resample(
        rule, origin="epoch", label="left", closed="left").count()
    return x.loc[n.eq(required)].copy()

def load(asset):
    p = BASE / f"{asset}_USDT_USDT_1m.csv"
    d = pd.read_csv(p, usecols=["ts","open","high","low","close"])
    d["ts"] = pd.to_datetime(
        pd.to_numeric(d["ts"], errors="raise").astype("int64"),
        unit="ms", utc=True)
    d = d.set_index("ts").sort_index()
    if d.index.has_duplicates:
        raise ValueError(f"{asset}: duplicate 1M timestamps")
    if not d.index.to_series().diff().dropna().eq(pd.Timedelta(minutes=1)).all():
        raise ValueError(f"{asset}: 1M source is not continuous")
    return d

def historical_features(h4):
    upper = h4.high.rolling(12, min_periods=12).max()
    lower = h4.low.rolling(12, min_periods=12).min()
    width = (upper / lower - 1.0) * 100.0
    net = (h4.close - h4.close.shift(12)).abs()
    path = h4.close.diff().abs().rolling(12, min_periods=12).sum()
    efficiency = net / path.replace(0.0, np.nan)
    ph, pl = h4.high.shift(1), h4.low.shift(1)
    intersection = (
        np.minimum(h4.high, ph) - np.maximum(h4.low, pl)
    ).clip(lower=0.0)
    smaller = np.minimum(h4.high - h4.low, ph - pl)
    pair = intersection / smaller.replace(0.0, np.nan)
    overlap = pair.rolling(11, min_periods=1).mean()
    f = pd.DataFrame({
        "upper":upper, "lower":lower, "width":width,
        "efficiency":efficiency, "overlap":overlap
    }).dropna()
    f["snapshot_time"] = f.index + pd.Timedelta(hours=4)
    return f

def main():
    raw = {a:load(a) for a in ASSETS}
    common = raw[ASSETS[0]].index
    for a in ASSETS[1:]:
        common = common.intersection(raw[a].index)
    common = common.sort_values()
    if len(common) != EXPECTED_COMMON:
        raise ValueError(f"Common timestamps {len(common)} != {EXPECTED_COMMON}")
    if not common.to_series().diff().dropna().eq(pd.Timedelta(minutes=1)).all():
        raise ValueError("Common 1M timestamps are not continuous")

    print("READ-ONLY PREVIOUS-SELECTED GATE DIAGNOSTIC V5")
    print(f"Common 1M timestamps: {len(common):,}")
    print("ER: exact historical 12-change absolute-price formula.")
    print("Quantile populations: unique 4H feature rows vs joined 15M rows.")
    print("Mask comparison: current+same-snapshot vs archived previous-selected gate.")
    print("No thresholds or masks are tuned to target counts.")
    rows = []

    for asset in ASSETS:
        one = raw[asset].loc[common]
        h4, m15 = bars(one, "4h", 240), bars(one, "15min", 15)
        if len(h4) != 2370 or len(m15) != 37941:
            raise ValueError(f"{asset}: unexpected complete 4H/15M row counts")
        f = historical_features(h4)
        if len(f) != 2358:
            raise ValueError(f"{asset}: expected 2,358 features, got {len(f)}")
        m = m15.copy()
        m.index.name = "bar_start"
        aligned = pd.merge_asof(
            m.reset_index().sort_values("bar_start"),
            f.reset_index(drop=True).sort_values("snapshot_time"),
            left_on="bar_start", right_on="snapshot_time",
            direction="backward"
        ).set_index("bar_start")

        populations = {
            "UNIQUE_4H_FEATURE_ROWS": f.width,
            "JOINED_15M_ROWS": aligned.width,
        }
        same_snapshot = aligned.snapshot_time.eq(aligned.snapshot_time.shift(1))
        previous_close = aligned.close.shift(1)

        for population, width_values in populations.items():
            thresholds = {
                "P25":float(width_values.quantile(.25)),
                "P40":float(width_values.quantile(.40)),
            }
            print(
                f"{asset} {population}: rows={width_values.notna().sum():,} "
                f"P25={thresholds['P25']:.9f}% P40={thresholds['P40']:.9f}%"
            )
            for definition, threshold in thresholds.items():
                selected = (
                    aligned.width.le(threshold)
                    & aligned.efficiency.le(.30)
                    & aligned.overlap.ge(.70)
                )
                # V3/V4 accepted reconstruction: current selected + same snapshot.
                current_gate = selected & same_snapshot
                # Exact archived breakout-script gate:
                # current selected AND immediately previous 15M row selected,
                # with both rows on the same frozen 4H snapshot.
                previous_selected = selected.shift(1).fillna(False).astype(bool)
                archived_gate = selected & previous_selected & same_snapshot

                for gate_name, gate in [
                    ("CURRENT_SELECTED_ONLY", current_gate),
                    ("ARCHIVED_PREVIOUS_SELECTED", archived_gate),
                ]:
                    masks = {
                        "UPPER": gate & previous_close.le(aligned.upper)
                                 & aligned.close.gt(aligned.upper),
                        "LOWER": gate & previous_close.ge(aligned.lower)
                                 & aligned.close.lt(aligned.lower),
                    }
                    for direction, mask in masks.items():
                        actual = int(mask.fillna(False).sum())
                        expected = EXPECTED[(asset,definition,direction)]
                        rows.append({
                            "asset":asset, "population":population,
                            "definition":definition, "gate":gate_name,
                            "direction":direction, "actual":actual,
                            "expected":expected, "pass":actual == expected,
                        })

    out = pd.DataFrame(rows)
    for population in ["UNIQUE_4H_FEATURE_ROWS","JOINED_15M_ROWS"]:
        for gate in ["CURRENT_SELECTED_ONLY","ARCHIVED_PREVIOUS_SELECTED"]:
            part = out[out.population.eq(population) & out.gate.eq(gate)]
            print("\n" + "="*96)
            print(f"{population} | {gate}")
            print(part[["asset","definition","direction","actual","expected","pass"]]
                  .to_string(index=False))
            print(f"EXACT MATCHES: {int(part['pass'].sum())}/20")

    print("\nNo controls, forward outcomes, matching, inference, or profitability calculations.")
    print("No files were written or modified.")

if __name__ == "__main__":
    main()
