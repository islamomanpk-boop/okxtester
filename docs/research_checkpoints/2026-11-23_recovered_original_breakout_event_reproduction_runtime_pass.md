# Original breakout/retest source — runtime reproduction PASS

Date: 2026-11-23
Branch: `price-action-v1`

## Source

Recovered verbatim from the original conversation titled **FINAL TIMING-CORRECTED BREAKOUT AND RETEST RESEARCH** and archived as:

`research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`

The source was committed and read back from GitHub before execution. The local file was verified to match `HEAD` with `git diff --exit-code`. The user ran this exact archived file unchanged in Termux.

## Runtime integrity

- Common 1-minute timestamps: **569,125**
- Per asset: **37,941** complete 15-minute candles
- Per asset: **2,370** complete 4-hour candles
- Five assets: BTC, ETH, SOL, DOGE, AVAX
- No script changes were made for this run.
- Script states read-only and performs no file writes.
- This run reproduced all 20 accepted historical event counts exactly.

## Exact event-count reproduction

Counts are shown as lower / upper for each threshold definition.

| Asset | Broad P40 lower / upper | Strict P25 lower / upper |
|---|---:|---:|
| BTC | 91 / 115 | 62 / 81 |
| ETH | 87 / 77 | 51 / 51 |
| SOL | 117 / 96 | 77 / 71 |
| DOGE | 81 / 75 | 55 / 65 |
| AVAX | 84 / 109 | 64 / 83 |

**Result: 20/20 exact matches** against the historical accepted event-count table recorded in `docs/research_checkpoints/2026-11-22_original_breakout_event_reproduction_pass.md`.

## Runtime thresholds

Percent channel width, dynamically calculated by the original script from joined 15-minute observations:

| Asset | P25 strict | P40 broad |
|---|---:|---:|
| BTC | 3.2422% | 3.9486% |
| ETH | 4.2423% | 5.4819% |
| SOL | 5.0670% | 6.1145% |
| DOGE | 5.1657% | 6.2641% |
| AVAX | 5.7036% | 6.9162% |

These are retrospective full-sample quantiles and remain exploratory, not live-calibrated thresholds.

## Method identity confirmed from source inspection

- Resamples complete 15-minute and 4-hour bars from the common 1-minute intersection, with right-edge labels and left-closed intervals.
- 4-hour channel uses the previous 12 completed 4-hour candles.
- Efficiency and overlap are shifted to use completed prior context.
- Threshold quantiles are computed from joined 15-minute channel-width observations, separately by asset.
- Uses sideways width, efficiency <= 0.30, overlap >= 0.70, and same frozen 4-hour snapshot.
- Upper/lower crossing uses prior 15-minute close at/below upper then current close above upper; lower is the inverse.
- No previous-sideways/previous-selected gate and no cooldown/de-clustering.
- Signal time is the 15-minute close label; final signal minute opens one minute before that label; follow-up begins at the next 1-minute candle open.
- Counts each signal once, not once per outcome horizon.

## Interpretation and scope

This resolves the prior independent event-count reproduction HOLD for this specific recovered source and dataset: the exact original source now reproduces the 20 accepted counts without parameter tuning or code changes.

The script also printed descriptive retest and follow-up summaries for 15-minute, 1-hour, 4-hour and 12-hour horizons. Those are descriptive event-conditioned outcomes only.

This is **not** evidence of profitability, causal effects, executable fills, or live-trading performance. The script does not model fees, slippage, funding, orders, stops, or fills.

## Research gate

The event-count reproduction gate is now **PASS for this recovered source/runtime**. Before matched-control work resumes, retain the existing pre-registered matched-control plan and independently audit the control implementation, outcome conventions, continuous-minute follow-up, matching and inference requirements. Do not treat earlier failed diagnostic scripts or their outputs as accepted findings.
