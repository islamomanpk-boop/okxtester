# Breakout event quantile-population diagnostic V4 — methodology

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Script:** `research/validation/breakout_event_quantile_population_diagnostic_v4.py`  
**Status:** Ready to run; no runtime result yet.

## Why V4

V3 tested the exact historical 12-change absolute-price efficiency-ratio formula, but calculated P25/P40 from the joined 15-minute rows. The historical sideways detector computes width quantiles from its unique 4H feature rows before those features are mapped to 15-minute observations.

V1's earlier unique-4H-versus-joined-15M diagnostic used the archived ER11 percentage formula, not the exact historical ER12 formula. V4 isolates this remaining combination.

## Fixed methodology

For each asset:
- Use the synchronized common 1M timestamp index (expected 569,125 rows).
- Resample complete 4H bars using epoch origin, left labels/left closure, exactly 240 1M observations.
- Resample complete 15M bars using the same convention, exactly 15 1M observations.
- Require 2,370 complete 4H bars, 37,941 complete 15M bars, and 2,358 historical feature rows.
- Use the historical detector's 12-bar channel.
- Use the exact historical ER: absolute price change over 12 4H close changes divided by the sum of absolute 12 close-to-close price changes.
- Use available-valid adjacent-pair overlap over the 11 pairs within the 12-bar channel.
- Make each 4H feature snapshot available at the 4H candle close (bar-start timestamp plus four hours).
- Map snapshots backward-as-of to 15M bar-start timestamps.
- Keep the accepted same-snapshot crossing mask, with no previous-sideways requirement and no cooldown/de-clustering.

## Only variable under test

Calculate P25/P40 using two populations:
1. `UNIQUE_4H_FEATURE_ROWS`: quantiles on the 2,358 unique 4H feature rows, matching the historical detector's documented population.
2. `JOINED_15M_ROWS`: quantiles on the feature values after backward-as-of joining to 15M bars, matching the V3 population.

For each population, report all 20 actual event counts against the historical reference table. No other parameter or formula is tuned.

## Scope and safety

Read-only. No files are written or modified. No controls, matching, forward outcomes, inference, entries/exits, costs, or profitability calculations.

A count match would still need to be consistent with the historical source methodology; it must not be selected merely because it matches. If neither population matches, the event gate remains on hold.

## Run in Termux

```bash
cd ~/okxtester || exit 1
git pull --ff-only origin price-action-v1
python research/validation/breakout_event_quantile_population_diagnostic_v4.py
```

Paste the complete output. Do not run matched controls or forward outcomes.
