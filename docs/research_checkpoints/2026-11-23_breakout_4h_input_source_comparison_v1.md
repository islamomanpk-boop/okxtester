# 4H input source comparison V1 — methodology and run instructions

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Script:** `research/validation/breakout_4h_input_source_comparison_v1.py`  
**Status:** Ready to run; no runtime result yet.

## Research question

Are the standalone 4H candles used by the historical sideways-detector workflow identical to 4H candles resampled from the 1M research files used by the archived breakout/retest script?

This is a source-provenance check, not an event-count reconstruction.

## Inputs

For each of BTC, ETH, SOL, DOGE, AVAX:

- 1M: `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv`
- Standalone 4H: `~/okx_adaptive_bot/data/{ASSET}_USDT_4h.csv`

## Method

The script recreates the archived breakout script's 4H aggregation exactly:
- pandas resample rule `4h`;
- `origin="epoch"`;
- `label="left"`;
- `closed="left"`;
- keep only bins containing exactly 240 1M close observations.

It then aligns standalone and resampled bars by 4H bar-start timestamp and reports:
- source row counts;
- incomplete resampling-bin count;
- common timestamps and timestamps unique to either source;
- exact OHLC row equality;
- equality within `rtol=1e-10, atol=1e-10`;
- per-column maximum and mean absolute differences;
- first five rows differing beyond tolerance.

If any required file is missing, the script prints the missing path(s) and stops without substituting another source.

## Safety and scope

- Read-only; no input or output files are written.
- Does not calculate sideways classifications, event masks, controls, forward outcomes, or profitability.
- A mismatch would establish that the source series differ, but would not by itself prove which series generated the historical accepted event counts.
- Equality would rule out OHLC source differences on common timestamps for these two files, but would not resolve other alignment or event-mask questions.

## Run in Termux

```bash
cd ~/okxtester || exit 1
git pull --ff-only origin price-action-v1
python research/validation/breakout_4h_input_source_comparison_v1.py
```

Paste the complete output. Do not run matched controls or forward-outcome calculations until the event gate is resolved.
