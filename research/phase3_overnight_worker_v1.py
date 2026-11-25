#!/usr/bin/env python3
"""Read-only Phase 3 overnight preflight and gate index."""
from __future__ import annotations
import csv, hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get("PHASE3_OUTPUT_DIR", "phase3_overnight_output"))
OUT.mkdir(parents=True, exist_ok=True)
EXPECTED = {
 "BTC": ("data/market_1m/BTC_USDT_USDT_1m.csv", "3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633", 569125),
 "ETH": ("data/market_1m/ETH_USDT_USDT_1m.csv", "8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2", 569125),
 "SOL": ("data/market_1m/SOL_USDT_USDT_1m.csv", "8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3", 569126),
 "DOGE": ("data/market_1m/DOGE_USDT_USDT_1m.csv", "eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4", 569126),
 "AVAX": ("data/market_1m/AVAX_USDT_USDT_1m.csv", "44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5", 569127),
}
COLS = ["ts", "open", "high", "low", "close", "vol"]
DOCS = [
 "docs/research_checkpoints/2026-11-25_phase3_breakout_causal_reconstruction_preflight_contract_v1.md",
 "docs/research_checkpoints/2026-11-25_phase3_causal_breakout_implementation_architecture_audit_v1.md",
 "docs/research_checkpoints/2026-11-25_phase3_execution_and_backtest_roadmap_v1.md",
 "reports/sideways_phase3_research_archive_v1/GATE0_SOURCE_ENGINE_READINESS_AUDIT_V1.md",
 "reports/sideways_phase3_research_archive_v1/PHASE3_SCOPE_COMPLETENESS_AUDIT_V1.md",
]
def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()

def main():
 started=datetime.now(timezone.utc).isoformat()
 run_id=os.environ.get("GITHUB_RUN_ID","local")
 revision=os.environ.get("PHASE3_RESEARCH_SHA",os.environ.get("GITHUB_SHA","unknown"))
 m={"worker":"phase3_overnight_worker_v1","run_id":run_id,"workflow_revision":revision,
    "research_branch":"price-action-v1","started_utc":started,"source_files":[],
    "documents":[],"common_index":{},"status":"RUNNING",
    "scope_boundary":"read-only source preflight and gate-status index only"}
 failures=[]; hashes_ok=True
 for asset,(rel,want,rows) in EXPECTED.items():
  p=ROOT/rel; item={"asset":asset,"path":rel,"expected_sha256":want,
                    "expected_rows":rows,"exists":p.is_file()}
  if not p.is_file():
   item["status"]="MISSING"; failures.append(f"{asset}: missing canonical input {rel}"); hashes_ok=False
  else:
   got=sha256(p); item.update({"actual_sha256":got,"hash_match":got==want,"bytes":p.stat().st_size})
   item["status"]="HASH_PASS" if got==want else "HASH_MISMATCH"
   if got!=want: failures.append(f"{asset}: SHA-256 mismatch; parsing prohibited"); hashes_ok=False
  m["source_files"].append(item)
 for rel in DOCS:
  p=ROOT/rel
  m["documents"].append({"path":rel,"exists":p.is_file(),"bytes":p.stat().st_size if p.is_file() else None})
  if not p.is_file(): failures.append(f"Required governance document missing: {rel}")
 arrays={}
 if hashes_ok:
  for asset,(rel,_,expected_rows) in EXPECTED.items():
   p=ROOT/rel
   try:
    df=pd.read_csv(p)
    if list(df.columns)!=COLS: raise ValueError(f"unexpected columns: {list(df.columns)}")
    if len(df)!=expected_rows: raise ValueError(f"row count {len(df)} != {expected_rows}")
    ts=pd.to_numeric(df["ts"],errors="raise").to_numpy(dtype=np.int64)
    if len(np.unique(ts))!=len(ts): raise ValueError("duplicate timestamps")
    if not np.all(np.diff(ts)>0): raise ValueError("timestamps not strictly increasing")
    vals=df[["open","high","low","close","vol"]].apply(pd.to_numeric,errors="raise").to_numpy(dtype=np.float64)
    if not np.isfinite(vals).all(): raise ValueError("non-finite OHLCV")
    o,h,l,c,v=vals.T
    if np.any(o<=0) or np.any(h<=0) or np.any(l<=0) or np.any(c<=0): raise ValueError("non-positive price")
    if np.any(h<np.maximum.reduce([o,l,c])) or np.any(l>np.minimum.reduce([o,h,c])): raise ValueError("invalid OHLC relationship")
    if np.any(v<0): raise ValueError("negative volume")
    arrays[asset]=ts
    item=next(x for x in m["source_files"] if x["asset"]==asset)
    item.update({"rows_verified":len(df),"timestamp_min":int(ts[0]),"timestamp_max":int(ts[-1]),
                 "ohlcv_valid":True,"status":"PASS"})
   except Exception as exc:
    failures.append(f"{asset}: validation failed: {type(exc).__name__}: {exc}")
    item=next(x for x in m["source_files"] if x["asset"]==asset)
    item.update({"status":"DATA_VALIDATION_FAILED","error":f"{type(exc).__name__}: {exc}"})
 if len(arrays)==5:
  common=arrays["BTC"]
  for a in ["ETH","SOL","DOGE","AVAX"]: common=np.intersect1d(common,arrays[a],assume_unique=True)
  cadence=bool(len(common)>1 and np.all(np.diff(common)==60000))
  m["common_index"]={"count":int(len(common)),"expected_count":569125,
    "count_match":len(common)==569125,"cadence_ms":60000,"cadence_match":cadence,
    "first_ts":int(common[0]) if len(common) else None,"last_ts":int(common[-1]) if len(common) else None}
  if len(common)!=569125: failures.append(f"common index count {len(common)} != 569125")
  if not cadence: failures.append("common index cadence is not exactly 60000 ms")
 else:
  failures.append("common index not computed because one or more assets failed validation")
 gates=[
  ("G0","Source / event / execution readiness","CONDITIONAL_HOLD","This run checks canonical market inputs and governance-file presence only. Causal event availability, three-family candidate generator, funding/fee/mark-price and engine readiness remain separately gated."),
  ("G1","Descriptive lifecycle","PARTIALLY_COMPLETE_REVIEW_REQUIRED","Existing rejection and breakout descriptive archives are preserved; remaining failed-breakout and execution lifecycle scope needs reconciliation."),
  ("G2","Execution-resolution comparison","BLOCKED_PENDING_G0_AND_CAUSAL_COHORT","No 1M/3M/5M/15M comparison before an accepted causal common 15M signal cohort and frozen fill rules."),
  ("G3","Entry-method comparison","BLOCKED_PENDING_G2_AND_FROZEN_ORDER_RULES","No entry variants before activation, fill, expiry, cancellation and adverse-selection rules are frozen."),
  ("G4","Stops / targets / trade management","BLOCKED_PENDING_FROZEN_EVENT_AND_ENTRY_CONTRACTS","No levels are optimized or outcomes calculated before causal events and predeclared hypotheses are accepted."),
  ("G5","Execution-engine acceptance","AUDIT_REQUIRED_NOT_ACCEPTED","Existing engines have known gaps: limit/expiry/partial fills, missing-funding fail-closed behavior, exact fee/contract assumptions and funding mark provenance."),
  ("G6-G7","Strategy backtest and chronological validation","NOT_AUTHORIZED","Out of scope until Gates 0-5 pass; no candidate orders, fills, PnL, inference or strategy backtest."),
 ]
 m["gate_status"]=[{"gate":g,"name":n,"status":s,"reason":why} for g,n,s,why in gates]
 m["failures"]=failures; m["finished_utc"]=datetime.now(timezone.utc).isoformat()
 m["status"]="PASS_READ_ONLY_PREFLIGHT" if not failures else "FAIL_CLOSED_PREFLIGHT"
 (OUT/"input_manifest.json").write_text(json.dumps(m,indent=2,sort_keys=True),encoding="utf-8")
 with (OUT/"gate_status.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.writer(f); w.writerow(["gate","name","status","reason"]); w.writerows(gates)
 lines=["# Phase 3 Overnight Work — Recovery Index","",f"- Run ID: {run_id}",
  f"- Workflow revision: {revision}",f"- Started UTC: {started}",f"- Finished UTC: {m['finished_utc']}",
  f"- Overall result: **{m['status']}**","- Research branch: price-action-v1",
  "- Scope: read-only input integrity preflight and gate-status report.","",
  "## Input integrity","","| Asset | Expected rows | Result | OHLCV |","|---|---:|---|---|"]
 for x in m["source_files"]:
  lines.append(f"| {x['asset']} | {x['expected_rows']} | {x.get('status','NOT_CHECKED')} | {x.get('ohlcv_valid','not run')} |")
 ci=m["common_index"]
 lines += ["",f"- Common timestamps: {ci.get('count','not computed')} (expected 569125).",
  f"- Exact 60000 ms cadence: {ci.get('cadence_match','not computed')}.",
  "","## Gate status","","| Gate | Status |","|---|---|"]
 for g,_,s,_ in gates: lines.append(f"| {g} | {s} |")
 lines += ["","## Work not performed","",
  "- No causal breakout reconstruction or threshold-policy selection.",
  "- No candidates, matched controls, orders, fills, forward outcomes, inference or PnL.",
  "- No Gate 2-7 experiments; dependent gates remain blocked until prerequisites pass.",
  "- No repository, raw-data, VPS, database or service changes.","","## Failures / stop reasons",""]
 lines += [f"- {x}" for x in failures] if failures else ["- None."]
 lines += ["","## Morning continuation","",
  "Start with input_manifest.json and gate_status.csv. If integrity passes, implement and synthetic-test the separate causal event reconstruction module under the frozen preflight contract. Do not bypass Gate 0.",""]
 (OUT/"PHASE3_OVERNIGHT_INDEX.md").write_text("\n".join(lines),encoding="utf-8")
 print("PHASE3_WORKER_STATUS="+m["status"])
 return 0 if not failures else 2
if __name__=="__main__": raise SystemExit(main())
