#!/usr/bin/env python3
"""Read-only diagnostic: exact historical absolute-price directional efficiency.

V2 changed the lookback but retained the archived script's percentage-return ER.
The historical detector instead defines ER as:
    abs(close[i] - close[i-12]) / sum(abs(diff(close[i-12:i+1])))
This diagnostic compares that exact 13-close / 12-price-change formula against
the archived 12-close / 11-percentage-return formula. Overlap is held at the
available-valid-pair implementation; prior V2 showed strict/available overlap
gave identical event counts in this dataset.

No tuning, file writes, controls, forward outcomes, or strategy simulation.
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

def make_bars(one, rule, expected):
    bars=one.resample(rule,origin="epoch",label="left",closed="left").agg(
        {"open":"first","high":"max","low":"min","close":"last"})
    counts=one["close"].resample(rule,origin="epoch",label="left",closed="left").count()
    return bars.loc[counts.eq(expected)].copy()

def load_asset(asset):
    path=BASE/f"{asset}_USDT_USDT_1m.csv"
    d=pd.read_csv(path,usecols=["ts","open","high","low","close"])
    d["ts"]=pd.to_datetime(pd.to_numeric(d["ts"],errors="raise").astype("int64"),
                           unit="ms",utc=True)
    d=d.set_index("ts").sort_index()
    if d.index.has_duplicates:
        raise ValueError(f"{asset}: duplicate timestamps")
    if not d.index.to_series().diff().dropna().eq(pd.Timedelta(minutes=1)).all():
        raise ValueError(f"{asset}: source not continuous")
    return d

def feature_frame(h4, mode):
    upper=h4["high"].rolling(12,min_periods=12).max()
    lower=h4["low"].rolling(12,min_periods=12).min()
    width=(upper/lower-1.0)*100.0
    if mode=="ARCHIVED_ER11_PERCENT":
        net=(h4["close"]/h4["close"].shift(11)-1.0).abs()
        path=h4["close"].pct_change().abs().rolling(11,min_periods=11).sum()
        efficiency=net/path.replace(0.0,np.nan)
    elif mode=="HISTORICAL_ER12_ABSOLUTE_PRICE":
        net=(h4["close"]-h4["close"].shift(12)).abs()
        path=h4["close"].diff().abs().rolling(12,min_periods=12).sum()
        efficiency=net/path.replace(0.0,np.nan)
    else:
        raise ValueError(mode)

    ph,pl=h4["high"].shift(1),h4["low"].shift(1)
    inter=(np.minimum(h4["high"],ph)-np.maximum(h4["low"],pl)).clip(lower=0.0)
    smaller=np.minimum(h4["high"]-h4["low"],ph-pl)
    pair=inter/smaller.replace(0.0,np.nan)
    overlap=pair.rolling(11,min_periods=1).mean()
    f=pd.DataFrame({"upper":upper,"lower":lower,"width":width,
                    "efficiency":efficiency,"overlap":overlap}).dropna()
    f["snapshot_time"]=f.index+pd.Timedelta(hours=4)
    return f

def main():
    raw={a:load_asset(a) for a in ASSETS}
    common=raw[ASSETS[0]].index
    for a in ASSETS[1:]:
        common=common.intersection(raw[a].index)
    common=common.sort_values()
    if len(common)!=EXPECTED_COMMON:
        raise ValueError(f"Common timestamps {len(common)} != {EXPECTED_COMMON}")
    if not common.to_series().diff().dropna().eq(pd.Timedelta(minutes=1)).all():
        raise ValueError("Common timestamp sequence is not continuous")
    print("READ-ONLY HISTORICAL ER FORMULA DIAGNOSTIC V3")
    print(f"Common 1M timestamps: {len(common):,}")
    print("ER formulas compared: archived 11-change percentage vs historical 12-change absolute price.")
    print("Overlap fixed to available valid adjacent-pair mean.")
    rows=[]
    for asset in ASSETS:
        one=raw[asset].loc[common]
        h4=make_bars(one,"4h",240)
        m15=make_bars(one,"15min",15)
        if len(h4)!=2370 or len(m15)!=37941:
            raise ValueError(f"{asset}: unexpected complete 4H/15M count")
        for mode in ["ARCHIVED_ER11_PERCENT","HISTORICAL_ER12_ABSOLUTE_PRICE"]:
            f=feature_frame(h4,mode)
            m=m15.copy()
            m.index.name="bar_start"
            aligned=pd.merge_asof(
                m.reset_index().sort_values("bar_start"),
                f.reset_index(drop=True).sort_values("snapshot_time"),
                left_on="bar_start",right_on="snapshot_time",direction="backward"
            ).set_index("bar_start")
            qs={"P25":float(aligned["width"].quantile(.25)),
                "P40":float(aligned["width"].quantile(.40))}
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
                    rows.append((asset,mode,definition,direction,actual,EXPECTED[key],actual==EXPECTED[key]))
            print(f"{asset} {mode}: feature_rows={len(f):,} "
                  f"P25={qs['P25']:.9f}% P40={qs['P40']:.9f}%")
    out=pd.DataFrame(rows,columns=["asset","er_formula","definition","direction","actual","expected","pass"])
    for mode in ["ARCHIVED_ER11_PERCENT","HISTORICAL_ER12_ABSOLUTE_PRICE"]:
        part=out[out.er_formula.eq(mode)]
        print("\n"+"="*82+"\n"+mode)
        print(part[["asset","definition","direction","actual","expected","pass"]].to_string(index=False))
        print(f"EXACT MATCHES: {int(part['pass'].sum())}/20")
    print("\nNo controls, forward outcomes, matching, or profitability calculations.")
    print("No files were written or modified.")

if __name__=="__main__":
    main()
