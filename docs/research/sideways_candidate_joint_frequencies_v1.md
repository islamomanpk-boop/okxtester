# Sideways Candidate Definitions — Joint Condition Frequencies V1

Date recorded: 2026-11-22  
Project: Price Action V1  
Branch: `price-action-v1`

## Objective

Record the exploratory comparison of 27 candidate 48-hour sideways definitions for each of BTC, ETH, SOL, DOGE, and AVAX. Each definition requires all three conditions:
1. 48H channel width at or below an asset-specific full-sample percentile threshold (P25, P40, or P50).
2. Directional efficiency at or below 0.20, 0.30, or 0.40.
3. Mean adjacent 4H candle overlap at or above 0.50, 0.60, or 0.70.

This is descriptive classification research, not a strategy test. Full-sample percentile thresholds are retrospective and not suitable for live classification.

## Data and calculation

- Common minute observations across five files: 569,125.
- Complete 4H candles per asset: 2,370.
- Valid 48H feature windows per asset: 2,358.
- The three features and formulas are defined in `sideways_market_identification_methodology_v1.md`.
- Channel percentile thresholds were calculated separately for each asset using all 2,358 feature windows.
- Qualifying window = all three conditions true simultaneously.
- The 27 combinations were evaluated for each asset (135 asset/definition comparisons).
- No local files were written or changed.

## Asset-specific channel thresholds

| Asset | P25 width | P40 width | P50 width |
|---|---:|---:|---:|
| BTC | 3.242% | 3.948% | 4.423% |
| ETH | 4.245% | 5.475% | 6.219% |
| SOL | 5.067% | 6.115% | 6.856% |
| DOGE | 5.166% | 6.264% | 7.134% |
| AVAX | 5.705% | 6.916% | 7.758% |

## Complete candidate results

Each cell is qualifying windows (percentage of 2,358 valid windows).

### BTC

| Channel | DE max | Overlap min | Count | % |
|---|---:|---:|---:|---:|
| P25 | 0.20 | 0.50 | 292 | 12.4 |
| P25 | 0.20 | 0.60 | 292 | 12.4 |
| P25 | 0.20 | 0.70 | 275 | 11.7 |
| P25 | 0.30 | 0.50 | 431 | 18.3 |
| P25 | 0.30 | 0.60 | 431 | 18.3 |
| P25 | 0.30 | 0.70 | 401 | 17.0 |
| P25 | 0.40 | 0.50 | 513 | 21.8 |
| P25 | 0.40 | 0.60 | 513 | 21.8 |
| P25 | 0.40 | 0.70 | 476 | 20.2 |
| P40 | 0.20 | 0.50 | 457 | 19.4 |
| P40 | 0.20 | 0.60 | 457 | 19.4 |
| P40 | 0.20 | 0.70 | 431 | 18.3 |
| P40 | 0.30 | 0.50 | 644 | 27.3 |
| P40 | 0.30 | 0.60 | 644 | 27.3 |
| P40 | 0.30 | 0.70 | 601 | 25.5 |
| P40 | 0.40 | 0.50 | 769 | 32.6 |
| P40 | 0.40 | 0.60 | 769 | 32.6 |
| P40 | 0.40 | 0.70 | 712 | 30.2 |
| P50 | 0.20 | 0.50 | 570 | 24.2 |
| P50 | 0.20 | 0.60 | 567 | 24.0 |
| P50 | 0.20 | 0.70 | 520 | 22.1 |
| P50 | 0.30 | 0.50 | 789 | 33.5 |
| P50 | 0.30 | 0.60 | 786 | 33.3 |
| P50 | 0.30 | 0.70 | 717 | 30.4 |
| P50 | 0.40 | 0.50 | 953 | 40.4 |
| P50 | 0.40 | 0.60 | 949 | 40.2 |
| P50 | 0.40 | 0.70 | 858 | 36.4 |

### ETH

| Channel | DE max | Overlap min | Count | % |
|---|---:|---:|---:|---:|
| P25 | 0.20 | 0.50 | 334 | 14.2 |
| P25 | 0.20 | 0.60 | 333 | 14.1 |
| P25 | 0.20 | 0.70 | 315 | 13.4 |
| P25 | 0.30 | 0.50 | 442 | 18.7 |
| P25 | 0.30 | 0.60 | 440 | 18.7 |
| P25 | 0.30 | 0.70 | 415 | 17.6 |
| P25 | 0.40 | 0.50 | 507 | 21.5 |
| P25 | 0.40 | 0.60 | 505 | 21.4 |
| P25 | 0.40 | 0.70 | 480 | 20.4 |
| P40 | 0.20 | 0.50 | 501 | 21.2 |
| P40 | 0.20 | 0.60 | 500 | 21.2 |
| P40 | 0.20 | 0.70 | 461 | 19.6 |
| P40 | 0.30 | 0.50 | 671 | 28.5 |
| P40 | 0.30 | 0.60 | 669 | 28.4 |
| P40 | 0.30 | 0.70 | 620 | 26.3 |
| P40 | 0.40 | 0.50 | 790 | 33.5 |
| P40 | 0.40 | 0.60 | 787 | 33.4 |
| P40 | 0.40 | 0.70 | 737 | 31.3 |
| P50 | 0.20 | 0.50 | 597 | 25.3 |
| P50 | 0.20 | 0.60 | 596 | 25.3 |
| P50 | 0.20 | 0.70 | 543 | 23.0 |
| P50 | 0.30 | 0.50 | 814 | 34.5 |
| P50 | 0.30 | 0.60 | 812 | 34.4 |
| P50 | 0.30 | 0.70 | 741 | 31.4 |
| P50 | 0.40 | 0.50 | 972 | 41.2 |
| P50 | 0.40 | 0.60 | 969 | 41.1 |
| P50 | 0.40 | 0.70 | 891 | 37.8 |

### SOL

| Channel | DE max | Overlap min | Count | % |
|---|---:|---:|---:|---:|
| P25 | 0.20 | 0.50 | 312 | 13.2 |
| P25 | 0.20 | 0.60 | 312 | 13.2 |
| P25 | 0.20 | 0.70 | 289 | 12.3 |
| P25 | 0.30 | 0.50 | 441 | 18.7 |
| P25 | 0.30 | 0.60 | 440 | 18.7 |
| P25 | 0.30 | 0.70 | 409 | 17.3 |
| P25 | 0.40 | 0.50 | 517 | 21.9 |
| P25 | 0.40 | 0.60 | 516 | 21.9 |
| P25 | 0.40 | 0.70 | 477 | 20.2 |
| P40 | 0.20 | 0.50 | 478 | 20.3 |
| P40 | 0.20 | 0.60 | 472 | 20.0 |
| P40 | 0.20 | 0.70 | 428 | 18.2 |
| P40 | 0.30 | 0.50 | 677 | 28.7 |
| P40 | 0.30 | 0.60 | 668 | 28.3 |
| P40 | 0.30 | 0.70 | 607 | 25.7 |
| P40 | 0.40 | 0.50 | 809 | 34.3 |
| P40 | 0.40 | 0.60 | 800 | 33.9 |
| P40 | 0.40 | 0.70 | 726 | 30.8 |
| P50 | 0.20 | 0.50 | 567 | 24.0 |
| P50 | 0.20 | 0.60 | 559 | 23.7 |
| P50 | 0.20 | 0.70 | 499 | 21.2 |
| P50 | 0.30 | 0.50 | 818 | 34.7 |
| P50 | 0.30 | 0.60 | 806 | 34.2 |
| P50 | 0.30 | 0.70 | 725 | 30.7 |
| P50 | 0.40 | 0.50 | 987 | 41.9 |
| P50 | 0.40 | 0.60 | 974 | 41.3 |
| P50 | 0.40 | 0.70 | 873 | 37.0 |

### DOGE

| Channel | DE max | Overlap min | Count | % |
|---|---:|---:|---:|---:|
| P25 | 0.20 | 0.50 | 336 | 14.2 |
| P25 | 0.20 | 0.60 | 335 | 14.2 |
| P25 | 0.20 | 0.70 | 302 | 12.8 |
| P25 | 0.30 | 0.50 | 452 | 19.2 |
| P25 | 0.30 | 0.60 | 449 | 19.0 |
| P25 | 0.30 | 0.70 | 407 | 17.3 |
| P25 | 0.40 | 0.50 | 531 | 22.5 |
| P25 | 0.40 | 0.60 | 528 | 22.4 |
| P25 | 0.40 | 0.70 | 481 | 20.4 |
| P40 | 0.20 | 0.50 | 527 | 22.3 |
| P40 | 0.20 | 0.60 | 522 | 22.1 |
| P40 | 0.20 | 0.70 | 457 | 19.4 |
| P40 | 0.30 | 0.50 | 698 | 29.6 |
| P40 | 0.30 | 0.60 | 690 | 29.3 |
| P40 | 0.30 | 0.70 | 606 | 25.7 |
| P40 | 0.40 | 0.50 | 833 | 35.3 |
| P40 | 0.40 | 0.60 | 825 | 35.0 |
| P40 | 0.40 | 0.70 | 729 | 30.9 |
| P50 | 0.20 | 0.50 | 636 | 27.0 |
| P50 | 0.20 | 0.60 | 630 | 26.7 |
| P50 | 0.20 | 0.70 | 555 | 23.5 |
| P50 | 0.30 | 0.50 | 848 | 36.0 |
| P50 | 0.30 | 0.60 | 839 | 35.6 |
| P50 | 0.30 | 0.70 | 740 | 31.4 |
| P50 | 0.40 | 0.50 | 1,007 | 42.7 |
| P50 | 0.40 | 0.60 | 998 | 42.3 |
| P50 | 0.40 | 0.70 | 885 | 37.5 |

### AVAX

| Channel | DE max | Overlap min | Count | % |
|---|---:|---:|---:|---:|
| P25 | 0.20 | 0.50 | 365 | 15.5 |
| P25 | 0.20 | 0.60 | 362 | 15.4 |
| P25 | 0.20 | 0.70 | 323 | 13.7 |
| P25 | 0.30 | 0.50 | 478 | 20.3 |
| P25 | 0.30 | 0.60 | 475 | 20.1 |
| P25 | 0.30 | 0.70 | 430 | 18.2 |
| P25 | 0.40 | 0.50 | 549 | 23.3 |
| P25 | 0.40 | 0.60 | 546 | 23.2 |
| P25 | 0.40 | 0.70 | 495 | 21.0 |
| P40 | 0.20 | 0.50 | 527 | 22.3 |
| P40 | 0.20 | 0.60 | 522 | 22.1 |
| P40 | 0.20 | 0.70 | 458 | 19.4 |
| P40 | 0.30 | 0.50 | 703 | 29.8 |
| P40 | 0.30 | 0.60 | 698 | 29.6 |
| P40 | 0.30 | 0.70 | 624 | 26.5 |
| P40 | 0.40 | 0.50 | 828 | 35.1 |
| P40 | 0.40 | 0.60 | 823 | 34.9 |
| P40 | 0.40 | 0.70 | 739 | 31.3 |
| P50 | 0.20 | 0.50 | 639 | 27.1 |
| P50 | 0.20 | 0.60 | 630 | 26.7 |
| P50 | 0.20 | 0.70 | 550 | 23.3 |
| P50 | 0.30 | 0.50 | 857 | 36.3 |
| P50 | 0.30 | 0.60 | 848 | 36.0 |
| P50 | 0.30 | 0.70 | 748 | 31.7 |
| P50 | 0.40 | 0.50 | 1,006 | 42.7 |
| P50 | 0.40 | 0.60 | 997 | 42.3 |
| P50 | 0.40 | 0.70 | 883 | 37.4 |

## Cross-asset comparison of selected definitions

| Candidate definition | BTC | ETH | SOL | DOGE | AVAX |
|---|---:|---:|---:|---:|---:|
| P25 / DE ≤0.30 / overlap ≥0.70 | 17.0% | 17.6% | 17.3% | 17.3% | 18.2% |
| P40 / DE ≤0.30 / overlap ≥0.70 | 25.5% | 26.3% | 25.7% | 25.7% | 26.5% |
| P50 / DE ≤0.30 / overlap ≥0.70 | 30.4% | 31.4% | 30.7% | 31.4% | 31.7% |

## Observations and interpretation

1. P25 / DE ≤0.30 / overlap ≥0.70 labels approximately 17.0–18.2% of windows across the five coins.
2. P40 / DE ≤0.30 / overlap ≥0.70 labels approximately 25.5–26.5%.
3. P50 / DE ≤0.30 / overlap ≥0.70 labels approximately 30.4–31.7%.
4. The similar cross-asset frequencies are encouraging for a common regime framework, while the channel-width threshold remains asset-relative.
5. Increasing the overlap threshold from 0.50 to 0.60 often has little effect; increasing it to 0.70 reduces qualifying windows more noticeably. This suggests overlap ≥0.50 or ≥0.60 is not very selective in many combinations.
6. Increasing the directional-efficiency ceiling and widening the channel percentile generally increases qualifying windows, as expected.
7. These are rolling windows, not independent episodes. A 48H window advances by 4H, so adjacent windows share 11 of 12 candles. The qualifying percentages must not be interpreted as the fraction of independent market regimes or independent hours.

## Research decision: retain candidates, do not finalize

Retain P25 / DE ≤0.30 / overlap ≥0.70 as a stricter candidate and P40 / DE ≤0.30 / overlap ≥0.70 as a broader candidate for episode-persistence analysis. P50 can remain a sensitivity benchmark. This is not a final production classifier.

Next:
- Convert consecutive qualifying rolling windows into episodes using an explicit run rule.
- Report episode counts, median duration, distribution, and longest duration for the retained candidates.
- Check whether a one-window gap should split or bridge an episode, and report sensitivity rather than silently smoothing.
- Once 4H state confirmation is respected, measure subsequent 15M activity within those states.

## Limitations

- Full-sample asset-specific channel percentiles are retrospective and introduce lookahead if used as if known in real time.
- Window overlap mechanically creates persistence; duration of consecutive rolling labels is not the same as an independently observed regime duration.
- The classifier is a descriptive proxy and has not been validated against human-labelled ranges or future breakout outcomes.
- No trading strategy, execution simulation, or profitability calculation was performed.
- Original 1M candle API provenance and exact instrument identifiers remain incompletely verified.
