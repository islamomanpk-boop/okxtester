#!/usr/bin/env python3
"""Freeze and independently re-audit the five-asset 1M source inputs for Phase 1."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import pandas as pd
ASSETS=("BTC","ETH","SOL","DOGE","AVAX")
EXPECTED_ROWS={"BTC":569125,"ETH":569125,"SOL":569126,"DOGE":569126,"AVAX":569127}
REQUIRED=("ts","open","high","low","close","vol")
def audit_frame(df:pd.DataFrame,asset:str)->tuple[dict,set[int]]:
 missing=set(REQUIRED)-set(df.columns)
 if missing: raise ValueError(f"{asset}: missing columns {sorted(missing)}")
 d=df[list(REQUIRED)].copy()
 ts=pd.to_numeric(d.ts,errors="coerce")
 if ts.isna().any() or (ts%1!=0).any(): raise ValueError(f"{asset}: invalid millisecond timestamps")
 ts=ts.astype("int64")
 if ts.duplicated().any(): raise ValueError(f"{asset}: duplicate timestamps")
 if not ts.is_monotonic_increasing: raise ValueError(f"{asset}: timestamps out of order")
 gaps=ts.diff().dropna()
 if not (gaps==60_000).all(): raise ValueError(f"{asset}: missing or irregular 1M intervals")
 for c in REQUIRED[1:]: d[c]=pd.to_numeric(d[c],errors="coerce")
 vals=d[list(REQUIRED[1:])].to_numpy(dtype=float)
 if not __import__("numpy").isfinite(vals).all(): raise ValueError(f"{asset}: non-finite OHLCV")
 if (d[["open","high","low","close"]]<=0).any().any() or (d.vol<0).any(): raise ValueError(f"{asset}: invalid price or volume")
 if (d.high<d[["open","low","close"]].max(axis=1)).any() or (d.low>d[["open","high","close"]].min(axis=1)).any(): raise ValueError(f"{asset}: inconsistent OHLC")
 if len(d)!=EXPECTED_ROWS[asset]: raise ValueError(f"{asset}: expected {EXPECTED_ROWS[asset]} rows, got {len(d)}")
 info={"asset":asset,"rows":len(d),"first_ts_ms":int(ts.iloc[0]),"last_ts_ms":int(ts.iloc[-1]),"duplicates":0,"unexpected_intervals":0,"ohlcv_valid":True}
 return info,set(ts.tolist())
def sha256(path:Path)->str:
 h=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def run(data_dir:Path,output:Path)->None:
 records=[]; timelines={}
 for asset in ASSETS:
  p=data_dir/f"{asset}_USDT_USDT_1m.csv"
  if not p.is_file(): raise FileNotFoundError(p)
  info,times=audit_frame(pd.read_csv(p),asset);info["sha256"]=sha256(p)
  records.append(info);timelines[asset]=times
 union=set.union(*timelines.values());common=set.intersection(*timelines.values())
 if len(union)!=569127 or len(common)!=569125: raise ValueError(f"Cross-asset alignment changed: union={len(union)}, common={len(common)}")
 if any(len(t)!=EXPECTED_ROWS[a] for a,t in timelines.items()):raise ValueError("Unexpected per-asset row count")
 output.mkdir(parents=True,exist_ok=True)
 pd.DataFrame(records).to_csv(output/"phase1_source_input_audit_v1.csv",index=False)
 meta={"study":"Phase 1 Uptrend/Bullish source-input preflight V1","assets":list(ASSETS),"timeframe":"1 minute","expected_rows":EXPECTED_ROWS,"union_timestamps":len(union),"timestamps_common_to_all_assets":len(common),"cross_asset_alignment":"PASS_WITH_TRAILING_DIFFERENCES","aggregation_policy":"Future timeframe bars must be built from complete, timestamp-aligned source candles; never forward-fill or fabricate missing bars.","phase1_scope":"descriptive uptrend/bullish research only; regime and event definitions must be pre-registered before outcome analysis","strategy_optimization_started":False,"outcome_comparison_started":False,"source_files":records}
 (output/"run_metadata_v1.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"assets":records,"union_timestamps":len(union),"common_timestamps":len(common)},indent=2))
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--data-dir",required=True);p.add_argument("--output",required=True);a=p.parse_args();run(Path(a.data_dir),Path(a.output))
if __name__=="__main__":main()
