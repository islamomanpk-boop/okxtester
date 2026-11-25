# Phase 3 Past-Only Regime Threshold Diagnostic V1

**Date:** 2026-11-25  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Branch at review:** `price-action-v1`  
**Starting commit:** `8efa81c8a735c730115cb1d257e60a940801300a`  
**Status:** PRELIMINARY EXPLORATORY DIAGNOSTIC — no threshold policy selected; no candidate generation or PnL simulation authorized.

## 1. Question

How do two strictly past-only alternatives for the historical channel-width P25/P40 regime cutoffs behave, compared with the retrospective full-sample cutoffs already used in the descriptive archive?

This diagnostic addresses the look-ahead defect identified in the Phase 3 candidate-availability audit. It does not determine which threshold method is best for trading.

## 2. Inputs and scope

Read-only inputs were the five tracked feature ledgers:

- `reports/sideways_detector_original_v1/BTC_features_original_v1.csv`
- `reports/sideways_detector_original_v1/ETH_features_original_v1.csv`
- `reports/sideways_detector_original_v1/SOL_features_original_v1.csv`
- `reports/sideways_detector_original_v1/DOGE_features_original_v1.csv`
- `reports/sideways_detector_original_v1/AVAX_features_original_v1.csv`

Each ledger contains 2,358 feature rows, spanning availability timestamps from 2025-10-22 16:00 UTC through 2026-11-19 12:00 UTC. The source feature rows record the 12-candle 4H channel, channel width, directional efficiency, mean overlap and snapshot availability time.

The existing full-sample cutoffs, retained only as retrospective reference values, are:

| Asset | Full-sample P25 width % | Full-sample P40 width % |
|---|---:|---:|
| BTC | 3.242203 | 3.947937 |
| ETH | 4.245214 | 5.474563 |
| SOL | 5.067174 | 6.114542 |
| DOGE | 5.165724 | 6.264058 |
| AVAX | 5.704868 | 6.916216 |

## 3. Exploratory methods compared

Both alternatives require 180 prior completed 4H snapshots before the first classification. This is a 30-day warm-up. No current or future row is included in its own threshold calculation. Quantiles use linear interpolation, matching the archived original quantile convention.

1. **Rolling-180:** At each snapshot, calculate P25/P40 from only the immediately preceding 180 completed snapshots for that asset.
2. **Expanding-prior:** At each snapshot, calculate P25/P40 from all prior completed snapshots for that asset, beginning after the same 180-snapshot warm-up.

For each method, classify the current row using its current channel width and the unchanged descriptive filters `directional_efficiency <= 0.30` and `mean_overlap >= 0.70`. Strict uses the past-only P25 width cutoff; broad uses the past-only P40 cutoff. These labels are diagnostic cohort counts only.

The first 180 rows per asset are warm-up rows and are not classified by either method. Each method therefore has 2,178 evaluated rows per asset (10,890 asset-rows across the five ledgers).

## 4. Results

Median past-only thresholds and resulting descriptive cohort rates:

| Asset | Method | Median P25 % | Median P40 % | Strict rows | Strict % | Broad rows | Broad % |
|---|---|---:|---:|---:|---:|---:|---:|
| BTC | Rolling-180 | 3.212831 | 3.868251 | 429 | 19.70 | 630 | 28.93 |
| BTC | Expanding-prior | 3.582697 | 4.332077 | 501 | 23.00 | 688 | 31.59 |
| ETH | Rolling-180 | 4.256086 | 5.150664 | 434 | 19.93 | 605 | 27.78 |
| ETH | Expanding-prior | 4.730012 | 6.203267 | 527 | 24.20 | 733 | 33.65 |
| SOL | Rolling-180 | 5.157966 | 6.101186 | 452 | 20.75 | 655 | 30.07 |
| SOL | Expanding-prior | 5.552892 | 6.723192 | 535 | 24.56 | 704 | 32.32 |
| DOGE | Rolling-180 | 5.162520 | 6.117922 | 441 | 20.25 | 636 | 29.20 |
| DOGE | Expanding-prior | 5.672452 | 6.986551 | 511 | 23.46 | 705 | 32.37 |
| AVAX | Rolling-180 | 6.053944 | 6.948975 | 410 | 18.82 | 607 | 27.87 |
| AVAX | Expanding-prior | 6.053944 | 7.069015 | 493 | 22.64 | 685 | 31.45 |

The past-only threshold values vary through time; they are not constants. Observed minimum-to-maximum threshold ranges:

| Asset | Rolling P25 range % | Rolling P40 range % | Expanding P25 range % | Expanding P40 range % |
|---|---:|---:|---:|---:|
| BTC | 2.0761–5.5826 | 2.5154–6.6330 | 3.2136–4.6117 | 3.9338–5.1062 |
| ETH | 2.6761–7.5473 | 3.4681–9.0516 | 4.2057–7.1690 | 5.3150–8.2433 |
| SOL | 3.0574–8.1438 | 3.4241–10.5073 | 4.9956–7.6087 | 6.0633–9.4671 |
| DOGE | 2.8419–7.9058 | 3.4747–9.0620 | 5.0000–7.6745 | 6.2041–8.9226 |
| AVAX | 3.8071–8.4902 | 4.9891–9.9418 | 5.6296–8.4534 | 6.6760–9.1727 |

Compared with the retrospective full-sample classifications on the same 2,178 evaluated rows, the expanding-prior method disagreed on 4.04–6.24% of strict labels and 3.40–5.60% of broad labels, depending on asset. Rolling-180 disagreed on 6.52–9.55% of strict labels and 7.21–10.24% of broad labels. This is expected evidence that retrospective full-sample labels are not interchangeable with labels available at the time.

## 5. Interpretation

- Both alternatives remove the specific future-information leak from the width quantile: each threshold uses only prior completed 4H snapshots.
- Rolling-180 responds more quickly to recent volatility changes, but its threshold range is wider and more variable in these ledgers.
- Expanding-prior is generally more stable in this sample, but it can adapt more slowly when the distribution changes.
- The cohort percentages are not evidence of predictive power, causal market structure, executable fills or profitability.
- Similarity to the old full-sample cutoffs is not a valid selection criterion; the old labels contain future information and are only a retrospective reference.
- The different cohort counts demonstrate that threshold policy materially changes which historical events would be eligible. This must be resolved before candidate generation.

## 6. Decision

**No threshold policy is selected by this diagnostic.** Both Rolling-180 and Expanding-prior remain candidate calibration policies for a separately specified, predeclared follow-up comparison. Do not silently replace the archived P25/P40 labels, overwrite historical outputs, or pass the descriptive full-sample labels into a live candidate generator.

Before selection, freeze a protocol that compares the two methods on threshold stability, warm-up coverage, regime-label persistence/turnover, asset comparability and the number/timing of eligible source events. Do not inspect forward returns, MFE/MAE, trade PnL or strategy outcomes to select the calibration method. Any later predictive or trading evaluation must use chronological development/validation/test separation and a threshold policy frozen without using the test period.

## 7. Explicit limitations

- This was a read-only calculation over the committed feature ledgers; no source data, VPS files, databases, workflows or existing research outputs were modified.
- The diagnostic did not independently rebuild the feature ledgers from canonical 1M candles.
- It did not validate the source 4H files, raw 15M inputs or full boundary snapshot provenance.
- The 180-snapshot warm-up and the two candidate policies are exploratory comparison settings, not approved production parameters.
- No rejection, breakout or failed-breakout candidate records were generated.
- No strategy, order, fill, fee, funding, PnL or backtest result was produced.

## 8. Next action

Write and review a formal threshold-selection protocol before implementing a reusable diagnostic script. The next comparison should measure time-series stability and event-eligibility consequences for both methods, preserving the three Phase 3 families separately. G0-04 and G0-05 remain OPEN / CRITICAL; Gate 0 remains CONDITIONAL HOLD; Gate 2 and strategy backtesting remain closed.


## 10. Scope amendment — breakout calibration is a separate source pipeline

A subsequent source-code inspection identified an important scope boundary. The calculations in this checkpoint use the five `sideways_detector_original_v1/*_features_original_v1.csv` ledgers. They directly describe the reconstructed sideways detector feature pipeline and are relevant to the rejection source chain, which joins events to those feature rows by asset and snapshot index.

They must **not** be assumed to reproduce the breakout pipeline's historical threshold population. The recovered breakout source independently builds complete 4H bars from the canonical common 1M data, constructs a lagged 12-candle context, backward-as-of joins that context to completed 15M bars, and calculates its historical P25/P40 quantiles over the joined 15M channel-width series. Its `snapshot` field is the right-labelled 4H context timestamp. That source-specific context/threshold population must be reconstructed and audited separately before applying a past-only breakout threshold.

Accordingly:
- The rolling-180 and expanding-prior results above are preliminary detector-feature diagnostics, not a universal Phase 3 threshold decision.
- Do not apply those numerical thresholds directly to breakout events.
- Rebuild the breakout 4H context from the exact canonical 1M source hashes recorded in its accepted metadata; verify complete 4H/15M bars, right-label timestamps, context lag and the event's snapshot timestamp.
- Define a past-only breakout threshold using only earlier available context snapshots, with a clearly stated unique-snapshot versus repeated-15M-row calibration population. Do not silently mix the two.
- Compare the breakout source's unique 4H context widths to the rejection detector feature ledger and explain any timestamp/value differences before candidate generation.

This amendment narrows the interpretation of the original diagnostic; it does not invalidate the detector-feature calculations or change any accepted historical archive.
