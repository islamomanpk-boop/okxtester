# Historical Directional-Efficiency Formula Audit — V3 Diagnostic

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** code prepared; runtime results pending  
**Research gate:** matched-control study remains HOLD.

## Important correction to V2 interpretation

A closer line-by-line comparison identified that V2's `ER12` variant changed the number of close changes but did **not** reproduce the historical detector's exact directional-efficiency formula.

Archived breakout script:
- `abs(close[i] / close[i-11] - 1)`
- divided by the sum of 11 absolute percentage close changes.

Historical sideways detector:
- `abs(close[i] - close[i-12])`
- divided by the sum of 12 absolute price changes.

These formulas are not interchangeable. Therefore V2 did not test the historical detector's exact ER definition, and its ER12 results must not be described as having ruled out the historical ER formula.

## V3 diagnostic

Added:
- `research/validation/breakout_event_historical_er_formula_diagnostic_v3.py`
- Commit: `8dd6d1e5e1f7ce8a29a015731aea70a7d9a22186`

It compares:
1. Archived ER11 percentage-return formula.
2. Historical ER12 absolute-price formula, exactly as implemented in `research/sideways_detector_original_v1.py`.

To isolate this formula difference, overlap is held to the available-valid-pair mean. V2 showed that strict versus available overlap produced identical event counts for the tested dataset and both tested ER lookbacks.

The diagnostic otherwise retains:
- five-asset common 1M intersection and continuity check;
- complete epoch-aligned 15M and 4H candles;
- 12-bar channel;
- full-sample joined-15M P25/P40 width quantiles;
- feature snapshot available at 4H candle completion;
- backward as-of alignment to 15M bar starts;
- same-snapshot breakout crossing;
- no previous-sideways filter, de-clustering, or cooldown.

It prints all 20 counts and feature-row counts for each ER formula. It performs no controls, forward outcomes, matching, or profitability analysis and writes no local files.

## Run in Termux

```bash
cd ~/okxtester || exit 1
git pull --ff-only origin price-action-v1
python research/validation/breakout_event_historical_er_formula_diagnostic_v3.py
```

Preserve the full output. Even if one formula produces 20/20, it must be justified by the historical source method, not chosen merely for count agreement.

## Current interpretation and hold

- V2 produced 0/20 in all four variants, but did not exactly test the historical detector's ER formula.
- V2 strict and available overlap versions produced identical counts on this dataset/implementation.
- The historical ER formula remains untested in the event-count reconstruction until V3 is run.
- The historical 20-count PASS remains unverified as an independent reproduction.
- No matched controls or forward outcomes may be calculated until the event gate is resolved.
