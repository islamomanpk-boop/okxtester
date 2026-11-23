#!/usr/bin/env python3
"""Read-only diagnostic for remaining breakout feature-formula alternatives.

Tests only source-grounded differences between the archived breakout script and
research/sideways_detector_original_v1.py:
  - ER over 11 close changes (12 closes) vs 12 changes (13 closes)
  - overlap requiring all 11 valid adjacent pairs vs averaging available pairs

Uses joined-15M width quantiles, same-snapshot crossing masks, and no
previous-sideways filter. Does not tune parameters, write files, or calculate
forward outcomes.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
BASE = Path.home() / "okx_scalping_data"
EXPECTED_COMMON = 569125
EXPECTED = {
    ("BTC", "P25", "LOWER"): 62, ("BTC", "P25", "UPPER"): 81,
    ("BTC", "P40", "LOWER"): 91, ("BTC", "P40", "UPPER"): 115,
    ("ETH", "P25", "LOWER"): 51, ("ETH", "P25", "UPPER"): 51,
    ("ETH", "P40", "LOWER"): 87, ("ETH", "P40", "UPPER"): 77,
    ("SOL", "P25", "LOWER"): 77, ("SOL", "P25", "UPPER"): 71,
    ("SOL", "P40", "LOWER"): 117, ("SOL", "P40", "UPPER"): 96,
    ("DOGE", "P25", "LOWER"): 55, ("DOGE", "P25", "UPPER"): 65,
    ("DOGE", "P40", "LOWER"): 81, ("DOGE", "P40", "UPPER"): 75,
    ("AVAX", "P25", "LOWER"): 64, ("AVAX", "P25", "UPPER"): 83,
    ("AVAX", "P40", "LOWER"): 84, ("AVAX", "P40", "UPPER"): 109,
}

def make_bars(one, rule, expected):
    bars = one.resample(rule, origin="epoch", label="left", closed="left").agg(
        {"open":"first","high":"max","low":"min","close":"last"}
    )
    counts = one["close"].resample(
        rule, origin="epoch", label="left", closed="left"
    ).count()
    return bars.loc[counts.eq(expected)].copy()

def load_asset(asset):
    path = BASE / f"{asset}_USDT_USDT_1m.csv"
    if not path.is_file():
        raise FileNotFoundError(path)
    d = pd.read_csv(path, usecols=["ts","open","high","low","close"])
    d["ts"] = pd.to_numeric(d["ts"], errors="raise").astype("int64")
    d["ts"] = pd.to_datetime(d["ts"], unit="ms", utc=True)
    d = d.set_index("ts").sort_index()
    if d.index.has_duplicates:
        raise ValueError(f"{asset}: duplicate timestamps")
    if not d.index.to_series().diff().dropna().eq(pd.Timedelta(minutes=1)).all():
        raise ValueError(f"{asset}: source is not continuous 1M")
    return d

def build_features(h4, er_changes, overlap_mode):
    upper = h4["high"].rolling(12, min_periods=12).max()
    lower = h4["low"].rolling(12, min_periods=12).min()
    width = (upper / lower - 1.0) * 100.0

    net = (h4["close"] / h4["close"].shift(er_changes) - 1.0).abs()
    path = h4["close"].pct_change().abs().rolling(
        er_changes, min_periods=er_changes
    ).sum()
    efficiency = net / path.replace(0.0, np.nan)

    ph, pl = h4["high"].shift(1), h4["low"].shift(1)
    intersection = (np.minimum(h4["high"], ph) - np.maximum(h4["low"], pl)).clip(lower=0.0)
    smaller = np.minimum(h4["high"] - h4["low"], ph - pl)
    pair = intersection / smaller.replace(0.0, np.nan)
    if overlap_mode == "ALL_11_PAIRS_REQUIRED":
        overlap = pair.rolling(11, min_periods=11).mean()
    elif overlap_mode == "MEAN_AVAILABLE_VALID_PAIRS":
        overlap = pair.rolling(11, min_periods=1).mean()
    else:
        raise ValueError(overlap_mode)

    f = pd.DataFrame({
        "upper":upper, "lower":lower, "width":width,
        "efficiency":efficiency, "overlap":overlap
    }).dropna()
    f["snapshot_time"] = f.index + pd.Timedelta(hours=4)
    return f

def main():
    raw = {a:load_asset(a) for a in ASSETS}
    common = raw[ASSETS[0]].index
    for a in ASSETS[1:]:
        common = common.intersection(raw[a].index)
    common = common.sort_values()
    if len(common) != EXPECTED_COMMON:
        raise ValueError(f"Common timestamps {len(common)} != {EXPECTED_COMMON}")
    if not common.to_series().diff().dropna().eq(pd.Timedelta(minutes=1)).all():
        raise ValueError("Common timestamp index has a gap")
    print("READ-ONLY FEATURE FORMULA DIAGNOSTIC V2")
    print(f"Common 1M timestamps: {len(common):,}")
    print("Variants are evidence-led, not selected by count matching.")
    variants = [
        ("ER11_OVERLAP_STRICT", 11, "ALL_11_PAIRS_REQUIRED"),
        ("ER11_OVERLAP_VALID_MEAN", 11, "MEAN_AVAILABLE_VALID_PAIRS"),
        ("ER12_OVERLAP_STRICT", 12, "ALL_11_PAIRS_REQUIRED"),
        ("ER12_OVERLAP_VALID_MEAN", 12, "MEAN_AVAILABLE_VALID_PAIRS"),
    ]
    for variant, er_changes, overlap_mode in variants:
        rows=[]
        thresholds_seen=[]
        for asset in ASSETS:
            one=raw[asset].loc[common]
            h4=make_bars(one,"4h",240)
            m15=make_bars(one,"15min",15)
            if len(h4)!=2370 or len(m15)!=37941:
                raise ValueError(f"{asset}: unexpected 4H/15M bar counts")
            f=build_features(h4,er_changes,overlap_mode)
            m15x=m15.copy()
            m15x.index.name="bar_start"
            aligned=pd.merge_asof(
                m15x.reset_index().sort_values("bar_start"),
                f.reset_index(drop=True).sort_values("snapshot_time"),
                left_on="bar_start",right_on="snapshot_time",direction="backward"
            ).set_index("bar_start")
            qs={"P25":float(aligned["width"].quantile(.25)),
                "P40":float(aligned["width"].quantile(.40))}
            thresholds_seen.append((asset,len(f),qs["P25"],qs["P40"]))
            same=aligned["snapshot_time"].eq(aligned["snapshot_time"].shift(1))
            prev=aligned["close"].shift(1)
            for definition,threshold in qs.items():
                selected=(aligned["width"].le(threshold)
                    & aligned["efficiency"].le(.30)
                    & aligned["overlap"].ge(.70))
                valid=selected & same
                masks={
                    "UPPER":valid & prev.le(aligned["upper"]) & aligned["close"].gt(aligned["upper"]),
                    "LOWER":valid & prev.ge(aligned["lower"]) & aligned["close"].lt(aligned["lower"]),
                }
                for direction,mask in masks.items():
                    key=(asset,definition,direction)
                    actual=int(mask.fillna(False).sum())
                    rows.append((asset,definition,direction,actual,EXPECTED[key],actual==EXPECTED[key]))
        result=pd.DataFrame(rows,columns=["asset","definition","direction","actual","expected","pass"])
        print("\n"+"="*82)
        print(variant, f"| ER changes={er_changes} | overlap={overlap_mode}")
        print("Features / joined thresholds:")
        for asset,n,p25,p40 in thresholds_seen:
            print(f"  {asset}: feature_rows={n:,} P25={p25:.9f}% P40={p40:.9f}%")
        print(result.to_string(index=False))
        print(f"EXACT MATCHES: {int(result['pass'].sum())}/20")
    print("\nNo controls, forward outcomes, matching, or profitability calculations.")
    print("No files were written or modified.")

if __name__=="__main__":
    main()
