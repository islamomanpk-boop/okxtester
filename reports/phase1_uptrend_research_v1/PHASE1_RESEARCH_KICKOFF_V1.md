# Phase 1 — Uptrend / Bullish Research Kickoff V1

**Status:** Source preflight initiated; no trend labels or thresholds frozen yet.  
**Sequence:** Follows the Phase 3 completion decision dated 2026-11-25.

## Objective

Describe how BTC, ETH, SOL, DOGE, and AVAX behave during objectively defined uptrend/bullish environments. This phase is descriptive research, not strategy testing.

## Data foundation

- Frozen source: `data/market_1m/{BTC,ETH,SOL,DOGE,AVAX}_USDT_USDT_1m.csv`.
- Existing audit: each asset has approximately 569k 1-minute candles; individual data-quality checks passed.
- Cross-asset alignment audit: 569,127 union timestamps and 569,125 timestamps common to all five assets; the only differences are trailing observations.
- Phase 1 V1 preflight independently rechecks timestamps, OHLCV integrity, exact 1-minute cadence, per-asset row counts, cross-asset intersection, and source SHA-256 hashes. It does not modify source data.

## Research protocol

1. Lock and archive source hashes and the common timeline.
2. Build higher-timeframe candles/features only from complete source intervals. Do not forward-fill, fabricate candles, or use information before its availability time.
3. Define candidate bullish/uptrend context using price structure and trend-strength measures. Freeze definitions before examining forward outcomes; retain strict and broad definitions only if their rules are explicit and interpretable.
4. Audit label coverage by asset and chronological subperiod, overlap/dependence, timestamp causality, and sensitivity to the frozen definitions.
5. Describe event anatomy and forward paths only after labels pass validation. Report all assets and periods, including weak or contradictory results.
6. Do not select strategies, tune entries/exits, optimize parameters, or infer profitability during this phase.

## Open design items

No numerical trend thresholds, moving-average lengths, or event labels are declared in this kickoff document. They must be justified and frozen in a separate versioned specification before the corresponding labels or outcomes are generated. This prevents silently importing arbitrary settings from the sideways-regime study.

## Phase order

After Phase 1: Phase 2 Downtrend/Bearish, then Phase 4 Choppy/High Volatility, then Phase 5 Transition/Expansion.
