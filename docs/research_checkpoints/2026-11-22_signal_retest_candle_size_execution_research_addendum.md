# Additional Research Workstreams — Signal Anatomy, Retests, and Execution Resolution

**Project:** OKX Price Action Research V1  
**Branch:** `price-action-v1`  
**Date:** 2026-11-22  
**Status:** Added to roadmap; not yet empirically completed. Research-only.  
**Scope:** Same completed 15M signal cohort; no strategy backtests or local data changes.

## Why this checkpoint exists

A review of the main roadmap and its status audit identified that execution research was mentioned broadly, but the user's requested comparisons and post-signal questions were not explicitly enumerated as dedicated studies. This checkpoint makes them visible and prevents them from being mistaken as completed.

## 1. Execution timeframe comparison

Compare **1M, 3M, 5M, and 15M execution** using the same completed 15M signals. Build 3M/5M/15M execution bars from the common 1M source. Do not regenerate signals on those execution timeframes.

Measure:
- Earliest eligible execution time and delay from completed 15M signal confirmation.
- Entry price and distance from signal close / structural levels.
- Price movement while waiting.
- Immediate entry versus separate pullback, signal-midpoint, retest, and confirmation entry methods.
- Touch, fill-opportunity, missed-entry, expiry, and partial-fill rates under explicit assumptions.
- Post-fill adverse selection and MFE/MAE.
- Differences by asset, side, signal type, signal-candle size, and known regime.

Respect causal timing: no execution before signal confirmation, and no use of a 15M execution candle before its close. Label OHLC touch-based fills as approximations, not verified fills.

## 2. Post-signal path and retest behaviour

For each completed 15M signal, follow the path from the next eligible 1M candle. Measure:
- Immediate continuation versus pullback-first.
- Retests of signal open, midpoint, close, high/low, and relevant breakout/structure levels.
- Retest incidence, time to first retest, depth, penetration, time spent around the level, and post-retest reaction.
- Hold/rejection, clean cross, repeated cross, failure/reversal, continuation, and no-touch outcomes.
- MFE, MAE, directional close movement and threshold timing at 15M, 1H, 4H, 12H and 24H where complete data exists.

Freeze levels at signal confirmation. Never count a pre-confirmation touch as a retest. Define event labels before calculation and report denominators, incomplete windows and overlapping-event dependence.

## 3. Signal-candle size and anatomy

For every signal candle record:
- High-low range, real body, body/range ratio, upper wick, lower wick and close location.
- Range/body relative to prior 15M ATR and recent rolling 15M distributions.
- Signal type, side, asset and contemporaneously known market regime.

Compare subsequent continuation, pullback, retest and failure behaviour across within-asset volatility-normalized size groups. Do not assume larger candles are stronger. Keep retrospective descriptive bins distinct from thresholds that could have been known live.

## 4. Status and sequencing

These three workstreams are **not yet completed**. They are now explicit roadmap requirements.

Recommended sequence:
1. Finish the already-agreed matched breakout-control study.
2. Complete signal-candle anatomy and post-signal path/retest research.
3. Compare 1M/3M/5M/15M execution resolution using the same 15M signal cohort.
4. Only later, and only with explicit authorization, consider cost-integrated strategy experiments.

No strategy backtest, order simulation, local data write, or profitability claim is authorized by this checkpoint.
