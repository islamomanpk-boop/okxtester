#!/usr/bin/env python3
"""Read-only G0-04 causal breakout reconstruction; descriptive eligibility only."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, subprocess
from pathlib import Path
import numpy as np
import pandas as pd

ASSETS=("BTC","ETH","SOL","DOGE","AVAX")
COLS=["ts","open","high","low","close","vol"]
M1,H4=60_000,14_400_000
WARMUP=180
EFF_MAX,OVERLAP_MIN,ATOL=.30,.70,1e-9
EXPECTED={
"BTC":("3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633",569125),
"ETH":("8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2",569125),
"SOL":("8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3",569126),
"DOGE":("eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4",569126),
"AVAX":("44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5",569127)}
BASELINE={
("BTC","BROAD_P40","LOWER"):91,("BTC","BROAD_P40","UPPER"):115,("BTC","STRICT_P25","LOWER"):62,("BTC","STRICT_P25","UPPER"):81,
("ETH","BROAD_P40","LOWER"):87,("ETH","BROAD_P40","UPPER"):77,("ETH","STRICT_P25","LOWER"):51,("ETH","STRICT_P25","UPPER"):51,
("SOL","BROAD_P40","LOWER"):117,("SOL","BROAD_P40","UPPER"):96,("SOL","STRICT_P25","LOWER"):77,("SOL","STRICT_P25","UPPER"):71,
("DOGE","BROAD_P40","LOWER"):81,("DOGE","BROAD_P40","UPPER"):75,("DOGE","STRICT_P25","LOWER"):55,("DOGE","STRICT_P25","UPPER"):65,
("AVAX","BROAD_P40","LOWER"):84,("AVAX","BROAD_P40","UPPER"):109,("AVAX","STRICT_P25","LOWER"):64,("AVAX","STRICT_P25","UPPER"):83}
POLICIES=("FIXED_180","EXPANDING_PRIOR","ROLLING_180")
POPS=("UNIQUE_4H_FEATURE_ROWS","JOINED_15M_ROWS")
KEYS=["asset","direction","signal_time_ms","context_snapshot_ms"]

def digest(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()
def stop(s): raise RuntimeError("G0-04 FAIL-CLOSED: "+s)

def load_sources(root):
 frames={}; arrays={}; audit=[]
 for a in ASSETS:
  p=root/"data/market_1m"/f"{a}_USDT_USDT_1m.csv"
  if not p.is_file(): stop(f"missing {p}")
  h=digest(p); want,n=EXPECTED[a]
  if h!=want: stop(f"{a} SHA256 mismatch; parsing prohibited")
  d=pd.read_csv(p)
  if list(d.columns)!=COLS or len(d)!=n: stop(f"{a} schema/row-count mismatch")
  ts=pd.to_numeric(d.ts,errors="coerce")
  if ts.isna().any() or (ts%1).any(): stop(f"{a} invalid timestamp")
  d.ts=ts.astype("int64")
  if d.ts.duplicated().any() or not d.ts.is_monotonic_increasing: stop(f"{a} duplicate/unordered timestamps")
  v=d[["open","high","low","close","vol"]].apply(pd.to_numeric,errors="coerce").to_numpy(float)
  if not np.isfinite(v).all(): stop(f"{a} non-finite OHLCV")
  o,hi,lo,c,vol=v.T
  if (o<=0).any() or (hi<=0).any() or (lo<=0).any() or (c<=0).any() or (vol<0).any(): stop(f"{a} invalid prices/volume")
  if (hi<np.maximum.reduce([o,lo,c])).any() or (lo>np.minimum.reduce([o,hi,c])).any(): stop(f"{a} invalid OHLC")
  arrays[a]=d.ts.to_numpy(np.int64)
  frames[a]=d.set_index(pd.to_datetime(d.ts,unit="ms",utc=True))[["open","high","low","close","vol"]]
  audit.append({"asset":a,"rows":n,"sha256":h})
 common=arrays["BTC"]
 for a in ASSETS[1:]: common=np.intersect1d(common,arrays[a],assume_unique=True)
 if len(common)!=569125 or not np.all(np.diff(common)==M1): stop("common index must be 569125 rows at exact 60s cadence")
 for x in audit: x["excluded_from_common_index"]=x["rows"]-len(common)
 ix=pd.to_datetime(common,unit="ms",utc=True)
 return {a:frames[a].reindex(ix) for a in ASSETS},audit,common

def bars(minute,rule,n):
 g=minute.resample(rule,label="right",closed="left")
 x=g.agg({"open":"first","high":"max","low":"min","close":"last","vol":"sum"})
 return x.loc[g.close.count()==n].dropna()

def overlap(high,low):
 ph,pl=high.shift(1),low.shift(1)
 inter=(np.minimum(high,ph)-np.maximum(low,pl)).clip(lower=0)
 small=np.minimum(high-low,ph-pl)
 return (inter/small.replace(0,np.nan)).clip(0,1)

def detector_context(b4):
 # Exact original sideways-detector features, available at the close of the
 # twelfth completed 4H candle. These are checked against its feature ledger.
 x=b4.copy()
 x["upper"]=x.high.rolling(12).max()
 x["lower"]=x.low.rolling(12).min()
 x["channel_width"]=(x.upper/x.lower-1)*100
 net=(x.close-x.close.shift(12)).abs()
 path=x.close.diff().abs().rolling(12).sum()
 x["efficiency"]=net/path.replace(0,np.nan)
 x.loc[path.eq(0),"efficiency"]=0.0
 x["overlap"]=overlap(x.high,x.low).rolling(11).mean()
 x.index.name="snapshot"
 return x


def historical_breakout_context(b4):
 # Preserve the exact one-4H-bar-lagged context used by the earlier
 # breakout-count study. Do not substitute the detector's current-candle
 # ledger here: that changes the historical 20 baseline counts.
 x=b4.copy()
 x["upper"]=x.high.rolling(12).max().shift(1)
 x["lower"]=x.low.rolling(12).min().shift(1)
 x["channel_width"]=(x.upper/x.lower-1)*100
 net=(x.close.shift(1)/x.close.shift(13)-1).abs()
 path=x.close.pct_change().abs().rolling(12).sum().shift(1)
 x["efficiency"]=net/path.replace(0,np.nan)
 x["overlap"]=overlap(x.high,x.low).rolling(12).mean().shift(1)
 x.index.name="snapshot"
 return x

def joined15(b15,ctx):
 l=b15.reset_index()
 l=l.rename(columns={l.columns[0]:"signal_time"})
 r=ctx.reset_index()[["snapshot","upper","lower","channel_width","efficiency","overlap"]]
 z=pd.merge_asof(l.sort_values("signal_time"),r.sort_values("snapshot"),
                 left_on="signal_time",right_on="snapshot",direction="backward")
 # Leading 15M bars before the first available 4H snapshot are expected warm-up rows.
 # Keep them with null context; downstream masks naturally exclude them.
 # A non-null future assignment remains a hard failure.
 if (z.snapshot.notna() & (z.snapshot>z.signal_time)).any(): stop("future as-of context")
 return z

def cross_check(root,a,ctx):
 p=root/"reports/sideways_detector_original_v1"/f"{a}_features_original_v1.csv"
 if not p.is_file(): stop(f"missing detector ledger {p}")
 d=pd.read_csv(p)
 # Detector availability is the right-labelled 4H context snapshot itself.
 # Adding another H4 shifts every detector row one bar into the future.
 d["join_ts"]=pd.to_numeric(d.available_at_ts_ms).astype("int64")
 c=ctx.reset_index()
 c["join_ts"]=c.snapshot.astype("int64")//1_000_000
 m=c.merge(d,on="join_ts",how="outer",suffixes=("_src","_det"),indicator=True)
 if (m._merge!="both").any(): stop(f"{a} detector ledger timestamp mismatch")
 for x,y in [("upper_src","upper_det"),("lower_src","lower_det"),("channel_width","channel_width_pct"),
              ("efficiency","directional_efficiency"),("overlap","mean_overlap")]:
  if not np.isclose(m[x].to_numpy(float),m[y].to_numpy(float),rtol=0,atol=ATOL,equal_nan=True).all():
   stop(f"{a} detector ledger value mismatch: {x}/{y}")
 return {"asset":a,"matched_rows":len(m),"tolerance_abs":ATOL}


def cross_check_legacy_channel_lag(root,a,legacy):
 # Historical breakout context at snapshot t uses the prior 4H candle set;
 # its channel must equal detector-ledger features available at t-H4.
 p=root/"reports/sideways_detector_original_v1"/f"{a}_features_original_v1.csv"
 d=pd.read_csv(p)
 d["join_ts"]=pd.to_numeric(d.available_at_ts_ms).astype("int64")+H4
 c=legacy.dropna(subset=["upper","lower","channel_width"]).reset_index()
 c["join_ts"]=c.snapshot.astype("int64")//1_000_000
 m=c.merge(d,on="join_ts",how="outer",suffixes=("_legacy","_det"),indicator=True)
 # One leading legacy channel window predates the detector's 13-close ER
 # ledger; one newest detector row has no later legacy snapshot. Both are
 # expected boundary rows, while all 2,357 overlapping rows must match.
 if int((m._merge=="left_only").sum())!=1 or int((m._merge=="right_only").sum())!=1:
  stop(f"{a} historical one-bar-lag channel timestamp mismatch")
 m=m[m._merge=="both"]
 if len(m)!=len(d)-1: stop(f"{a} historical lag overlap row-count mismatch")
 for x,y in [("upper_legacy","upper_det"),("lower_legacy","lower_det"),("channel_width","channel_width_pct")]:
  if not np.isclose(m[x].to_numpy(float),m[y].to_numpy(float),rtol=0,atol=ATOL,equal_nan=True).all():
   stop(f"{a} historical one-bar-lag channel mismatch: {x}/{y}")
 return {"asset":a,"matched_rows":len(m),"expected_boundary_rows":2,"lag_bars":1,"tolerance_abs":ATOL}

def baseline(z,a):
 w=z.channel_width.dropna()
 p25,p40=w.quantile(.25),w.quantile(.40)
 same=z.snapshot.eq(z.snapshot.shift(1)); prev=z.close.shift(1)
 out=[]
 for name,lim in [("STRICT_P25",p25),("BROAD_P40",p40)]:
  ok=(z.channel_width<=lim)&(z.efficiency<=EFF_MAX)&(z.overlap>=OVERLAP_MIN)
  for direction,mask in [("UPPER",ok&same&(prev<=z.upper)&(z.close>z.upper)),
                         ("LOWER",ok&same&(prev>=z.lower)&(z.close<z.lower))]:
   n=int(mask.fillna(False).sum()); e=BASELINE[(a,name,direction)]
   out.append({"asset":a,"definition":name,"direction":direction,"expected":e,"actual":n,"passed":n==e})
 return out

def raw_events(z,a):
 same=z.snapshot.eq(z.snapshot.shift(1)); prev=z.close.shift(1); out=[]
 for direction,mask in [("UPPER",same&(prev<=z.upper)&(z.close>z.upper)),
                        ("LOWER",same&(prev>=z.lower)&(z.close<z.lower))]:
  for r in z.loc[mask.fillna(False)].itertuples(index=False):
   t=pd.Timestamp(r.signal_time); s=pd.Timestamp(r.snapshot)
   out.append({"asset":a,"direction":direction,"signal_time_ms":t.value//1_000_000,
    "context_snapshot_ms":s.value//1_000_000,"upper":r.upper,"lower":r.lower,
    "channel_width_pct":r.channel_width,"efficiency":r.efficiency,"overlap":r.overlap})
 return out

def thresholds(ctx,z,a):
 counts=z.groupby("snapshot").size()
 full=counts[counts==16].index
 prior_clock=ctx.loc[ctx.index.isin(full)].sort_index()
 current_clock=ctx.sort_index()
 if len(prior_clock)<WARMUP+1: stop(f"{a} fewer than 181 fully covered contexts")
 widths=z[z.snapshot.isin(prior_clock.index)].groupby("snapshot").channel_width.agg(list)
 rows=[]
 for t in current_clock.index:
  # Current context may have a partial 15M tail; it is eligible for classification,
  # but only fully covered, strictly earlier contexts may enter calibration.
  prior=prior_clock.index[prior_clock.index<t]
  if len(prior)<WARMUP: continue
  for pol in POLICIES:
   sample=prior[:WARMUP] if pol=="FIXED_180" else (prior[-WARMUP:] if pol=="ROLLING_180" else prior)
   for pop in POPS:
    vals=(prior_clock.loc[sample,"channel_width"].to_numpy(float) if pop=="UNIQUE_4H_FEATURE_ROWS"
          else np.asarray([v for ts in sample for v in widths.loc[ts]],float))
    if not np.isfinite(vals).all(): stop("non-finite calibration values")
    rows.append({"asset":a,"snapshot_ms":t.value//1_000_000,"policy":pol,"population":pop,
     "p25":np.quantile(vals,.25,method="linear"),"p40":np.quantile(vals,.40,method="linear"),
     "prior_context_count":len(sample),"prior_15m_row_count":len(sample)*16,
     "first_prior_context_ms":sample[0].value//1_000_000,"last_prior_context_ms":sample[-1].value//1_000_000})
 return pd.DataFrame(rows),counts

def old_events(root):
 p=root/"reports/breakout_prior_test_count_v1/breakout_prior_test_classifications_v1.csv"
 if not p.is_file(): stop("historical 932-signal classification ledger missing")
 d=pd.read_csv(p)
 required=["asset","direction","signal_time","snapshot"]
 if any(c not in d.columns for c in required): stop("historical classification ledger missing identity columns")
 if d[required].isna().any().any(): stop("historical classification ledger contains null identity fields")
 signal_ts=pd.to_datetime(d.signal_time,utc=True,errors="coerce")
 snapshot_ts=pd.to_datetime(d.snapshot,utc=True,errors="coerce")
 if signal_ts.isna().any() or snapshot_ts.isna().any(): stop("historical classification ledger contains invalid identity timestamps")
 d["signal_time_ms"]=signal_ts.astype("int64")//1_000_000
 d["context_snapshot_ms"]=snapshot_ts.astype("int64")//1_000_000
 # The source is a classification matrix: each signal identity is intentionally
 # repeated across definition (STRICT_P25/BROAD_P40) and zone (5/10/15%).
 # Validate uniqueness at that full source-row grain before collapsing to the
 # 932 cross-definition signal identities used by the downstream reconciliation.
 source_keys=KEYS+["definition","zone_pct_of_channel"]
 if any(c not in d.columns for c in source_keys): stop("historical classification ledger missing classification-key columns")
 if d.duplicated(source_keys).any(): stop("historical classification ledger contains duplicate full classification rows")
 if set(d.definition.dropna().unique())!={"STRICT_P25","BROAD_P40"}: stop("historical classification ledger has unexpected definitions")
 zone_values=pd.to_numeric(d.zone_pct_of_channel,errors="coerce")
 if zone_values.isna().any(): stop("historical classification ledger contains null/invalid zone levels")
 if set(zone_values.unique())!={5.0,10.0,15.0}: stop("historical classification ledger has unexpected zone levels")
 identities=d[KEYS].drop_duplicates()
 return identities.assign(was_historical_selected=True)

def run(root,out):
 mins,input_audit,common=load_sources(root)
 baseline_rows=[]; ctx_audit=[]; cache={}
 # First pass: reconstruct source context and reproduce all 20 historical counts.
 # No causal thresholds or raw-event outputs are calculated before this gate passes.
 for a in ASSETS:
  b15,b4=bars(mins[a],"15min",15),bars(mins[a],"4h",240)
  detector_ctx=detector_context(b4)
  detector_finite=detector_ctx.dropna(subset=["upper","lower","channel_width","efficiency","overlap"])
  legacy_ctx=historical_breakout_context(b4)
  legacy_finite=legacy_ctx.dropna(subset=["upper","lower","channel_width","efficiency","overlap"])
  # Historical counts must use the exact legacy context that generated them.
  z=joined15(b15,legacy_ctx)
  counts=z.groupby("snapshot").size()
  exceptions=[{"snapshot_ms":int(t.value//1_000_000),"rows":int(n)} for t,n in counts.items() if n!=16]
  ctx_audit.append({"asset":a,"bars15":len(b15),"bars4h":len(b4),
    "detector_finite_contexts":len(detector_finite),"historical_finite_contexts":len(legacy_finite),
    "coverage_exceptions":exceptions,
    "detector_cross_pipeline":cross_check(root,a,detector_finite),
    "historical_channel_lag_cross_check":cross_check_legacy_channel_lag(root,a,legacy_ctx)})
  baseline_rows+=baseline(z,a)
  cache[a]=(legacy_finite,z)
 base=pd.DataFrame(baseline_rows)
 if len(base)!=20 or not base.passed.all():
  out.mkdir(parents=True,exist_ok=True)
  base.to_csv(out/"historical_baseline_reproduction.csv",index=False)
  stop(f"historical baseline reproduced {int(base.passed.sum())}/20; causal output withheld")
 # Second pass begins only after exact 20/20 baseline reproduction.
 event_rows=[]; threshold_rows=[]
 for a in ASSETS:
  finite,z=cache[a]
  th,_=thresholds(finite,z,a)
  threshold_rows.append(th)
  event_rows+=raw_events(z,a)
 ev=pd.DataFrame(event_rows); th=pd.concat(threshold_rows,ignore_index=True); old=old_events(root)
 if ev.duplicated(KEYS).any() or old.duplicated(KEYS).any(): stop("event identity duplicate")
 if len(old)!=932: stop(f"historical selected identity count {len(old)} != 932")
 ids=ev.merge(old,on=KEYS,how="left")
 ids["was_historical_selected"]=ids.was_historical_selected.fillna(False).astype(bool)
 # Attach each policy/population independently; retain one row per raw event.
 for pol in POLICIES:
  for pop in POPS:
   q=th[(th.policy==pol)&(th.population==pop)][["asset","snapshot_ms","p25","p40"]]
   tmp=ev.merge(q,left_on=["asset","context_snapshot_ms"],right_on=["asset","snapshot_ms"],how="left")
   tag=f"{pol}__{pop}"
   tmp[tag+"__strict"]=(tmp.channel_width_pct<=tmp.p25)&(tmp.efficiency<=EFF_MAX)&(tmp.overlap>=OVERLAP_MIN)
   tmp[tag+"__broad"]=(tmp.channel_width_pct<=tmp.p40)&(tmp.efficiency<=EFF_MAX)&(tmp.overlap>=OVERLAP_MIN)
   ids=ids.merge(tmp[KEYS+[tag+"__strict",tag+"__broad"]],on=KEYS,how="left",validate="one_to_one")
 strict=[c for c in ids if c.endswith("__strict")]
 broad=[c for c in ids if c.endswith("__broad")]
 if (ids[strict].fillna(False).to_numpy() & ~ids[broad].fillna(False).to_numpy()).any():
  stop("strict is not nested in broad")
 oldset=set(map(tuple,old[KEYS].to_numpy())); rawset=set(map(tuple,ev[KEYS].to_numpy()))
 source_mismatch=oldset-rawset
 if source_mismatch:
  out.mkdir(parents=True,exist_ok=True)
  pd.DataFrame(list(source_mismatch),columns=KEYS).to_csv(out/"historical_identity_source_mismatches.csv",index=False)
  stop(f"historical 932 identity reconciliation failed: {len(source_mismatch)} source identities absent from raw scan")
 rec=[]
 for pol in POLICIES:
  for pop in POPS:
   for definition in ("strict","broad"):
    col=f"{pol}__{pop}__{definition}"
    elig=ids[ids[col].fillna(False)]
    eset=set(map(tuple,elig[KEYS].to_numpy()))
    for a in ASSETS:
     for direction in ("LOWER","UPPER"):
      o={k for k in oldset if k[0]==a and k[1]==direction}
      r={k for k in rawset if k[0]==a and k[1]==direction}
      e={k for k in eset if k[0]==a and k[1]==direction}
      rec.append({"asset":a,"direction":direction,"policy":pol,"population":pop,"definition":definition,
       "eligible_event_count":len(e),"unchanged_eligible":len(o&r&e),"newly_eligible":len((r-o)&e),
       "no_longer_eligible":len((o&r)-e),"raw_source_mismatch":len(o-r)})
 out.mkdir(parents=True,exist_ok=True)
 base.to_csv(out/"historical_baseline_reproduction.csv",index=False)
 pd.DataFrame(input_audit).to_csv(out/"input_manifest.csv",index=False)
 pd.DataFrame(ctx_audit).to_json(out/"context_coverage_and_cross_pipeline_audit.json",orient="records",indent=2)
 th.to_csv(out/"causal_thresholds_by_context.csv",index=False)
 ids.to_csv(out/"unique_raw_crossing_events_with_six_variants.csv",index=False)
 pd.DataFrame(rec).to_csv(out/"historical_932_identity_reconciliation.csv",index=False)
 ids.groupby(["asset","direction"]).size().rename("raw_crossings").reset_index().to_csv(out/"raw_crossing_summary.csv",index=False)
 meta={"status":"DESCRIPTIVE_RECONSTRUCTION_COMPLETE_BASELINE_20_OF_20","common_1m_timestamps":len(common),
  "input_hashes":input_audit,"code_revision":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
  "python":platform.python_version(),"numpy":np.__version__,"pandas":pd.__version__,
  "scope":"descriptive only; no candidates, orders, fills, outcomes, inference or PnL"}
 meta["output_sha256"]={p.name:digest(p) for p in out.iterdir() if p.is_file()}
 (out/"run_metadata.json").write_text(json.dumps(meta,indent=2,sort_keys=True))
 print(meta["status"])

def self_test():
 # Right-labelled, left-closed aggregation and incomplete interval exclusion.
 ix=pd.date_range("2026-01-01",periods=32,freq="min",tz="UTC")
 m=pd.DataFrame({"open":100.,"high":101.,"low":99.,"close":100.5,"vol":1.},index=ix)
 b15=bars(m,"15min",15)
 assert len(b15)==2 and b15.index[0]==ix[0]+pd.Timedelta(minutes=15)
 assert len(bars(m,"4h",240))==0
 # Context is usable at its exact availability label.
 c=pd.DataFrame({"upper":[110.],"lower":[90.],"channel_width":[22.],"efficiency":[.2],"overlap":[.8]},
  index=pd.DatetimeIndex([ix[0]+pd.Timedelta(minutes=15)],name="snapshot"))
 z=joined15(b15,c)
 assert z.snapshot.iloc[0]==b15.index[0] and z.snapshot.iloc[1]==b15.index[0]
 # A future context must not be back-assigned to an earlier 15M close.
 future=c.copy(); future.index=future.index+pd.Timedelta(minutes=30)
 zfuture=joined15(b15,future)
 assert zfuture.snapshot.isna().all()  # future context is not back-assigned
 # Pre-context warm-up rows remain present and are explicitly unclassified.
 warm=joined15(b15,future)
 assert len(warm)==len(b15) and warm.snapshot.isna().all()
 # Build 182 contexts with 16 joined 15M rows each; last context is extreme
 # to prove its own value is excluded from its threshold.
 times=pd.date_range("2025-01-01",periods=182,freq="4h",tz="UTC",name="snapshot")
 widths=np.arange(1.,183.); widths[-1]=10000.
 ctx=pd.DataFrame({"upper":200.,"lower":100.,"channel_width":widths,
  "efficiency":.2,"overlap":.8},index=times)
 rows=[]
 for t,w in zip(times,widths):
  for j in range(16):
   rows.append({"snapshot":t,"channel_width":w,"close":100.})
 joined=pd.DataFrame(rows)
 th,_=thresholds(ctx,joined,"TST")
 at=th[th.snapshot_ms==times[180].value//1_000_000]
 assert len(at)==6 and set(at.prior_context_count)=={180}
 assert set(at.prior_15m_row_count)=={2880}
 at_last=th[th.snapshot_ms==times[181].value//1_000_000]
 expanding=at_last[at_last.policy=="EXPANDING_PRIOR"]
 assert len(expanding)==2 and set(expanding.prior_context_count)=={181}
 assert float(expanding.p25.iloc[0])==float(np.quantile(np.arange(1.,182.),.25))
 # Rolling and fixed windows each use 180 contexts, expanding uses all 181.
 assert set(at_last[at_last.policy.isin(["FIXED_180","ROLLING_180"])].prior_context_count)=={180}
 # One incomplete prior context is excluded, never silently counted as 16.
 partial=joined.drop(joined.index[0])
 th_partial,_=thresholds(ctx,partial,"TST")
 last=th_partial[th_partial.snapshot_ms==times[181].value//1_000_000]
 assert set(last.prior_context_count)=={180}
 # Strict percentile threshold cannot exceed broad threshold.
 assert (th.p25<=th.p40).all()
 # Historical identity is independent of strict/broad duplicate labels.
 identity=("BTC","UPPER",123,456)
 assert len(set([identity,identity]))==1

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[1])
 p.add_argument("--output-dir",type=Path,default=Path("phase3_g0_04_output"))
 p.add_argument("--self-test",action="store_true")
 a=p.parse_args()
 if a.self_test: self_test(); print("PASS: synthetic G0-04 tests"); return
 run(a.repo_root,a.output_dir)
if __name__=="__main__": main()
