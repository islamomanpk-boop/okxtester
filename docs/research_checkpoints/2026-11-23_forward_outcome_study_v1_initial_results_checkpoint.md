# Forward Rejection Outcome Study V1 — Initial Results Checkpoint

Date: 2026-11-23
Branch: `price-action-v1`
Status: **Full historical run completed; initial aggregate results reviewed. Descriptive only; no trading edge or profitability established.**

## Execution and integrity

The user ran:

```bash
python research/sideways_rejection_forward_outcomes_v1.py
```

The script completed successfully and wrote:
- `reports/sideways_rejection_forward_outcomes_v1/event_level_outcomes.csv`
- `reports/sideways_rejection_forward_outcomes_v1/aggregate_summary.csv`
- `reports/sideways_rejection_forward_outcomes_v1/data_validation.csv`

Reconciled population:
- Broad: 1,154 first-strong-rejection events.
- Strict: 838 events, a contained subgroup of broad.
- Output rows: 1,992 because the two labelled cohorts are both represented; do not add or pool broad and strict as independent events.

Source validation across BTC, ETH, SOL, DOGE, AVAX:
- 569,125–569,127 1M rows per asset.
- Zero non-60-second gaps.
- 1,992/1,992 event rows had the exact confirmation-minute candle.
- Zero missing confirmation-minute rows.

Horizon coverage:
- Broad: 15m 1,154/1,154; 1h 1,154/1,154; 4h 1,154/1,154; 24h 1,146/1,154 (8 censored).
- Strict: 15m 838/838; 1h 838/838; 4h 838/838; 24h 836/838 (2 censored).
- Incomplete 24h observations are excluded from that horizon's return denominator.

## Overall aggregate results

Positive direction-adjusted return frequency and median direction-adjusted return:

| Cohort | Horizon | Complete | Positive frequency | Median adjusted return |
|---|---:|---:|---:|---:|
| Broad | 15m | 1,154 | 52.253% | +0.0160% |
| Broad | 1h | 1,154 | 51.127% | +0.0152% |
| Broad | 4h | 1,154 | 52.166% | +0.0451% |
| Broad | 24h | 1,146 | 52.356% | +0.1447% |
| Strict | 15m | 838 | 51.671% | +0.0134% |
| Strict | 1h | 838 | 49.761% | 0.0000% |
| Strict | 4h | 838 | 52.029% | +0.0429% |
| Strict | 24h | 836 | 54.426% | +0.2129% |

## Directional asymmetry — broad cohort

Upper rejection (expected down):
- Positive adjusted frequency: 54.362% (15m), 52.685% (1h), 55.872% (4h), 57.383% (24h).
- Median adjusted return: +0.0260%, +0.0327%, +0.1022%, +0.2898% respectively.

Lower rejection (expected up):
- Positive adjusted frequency: 50.000% (15m), 49.462% (1h), 48.208% (4h), 46.909% (24h).
- Median adjusted return: +0.0005%, 0.0000%, -0.0213%, -0.1269% respectively.

## Directional asymmetry — strict subgroup

Upper rejection:
- Positive adjusted frequency: 53.846% (15m), 51.810% (1h), 55.430% (4h), 60.181% (24h).
- Median adjusted return: +0.0220%, +0.0242%, +0.0732%, +0.3674%.

Lower rejection:
- Positive adjusted frequency: 49.242% (15m), 47.475% (1h), 48.232% (4h), 47.970% (24h).
- Median adjusted return: 0.0000%, -0.0220%, -0.0116%, -0.0739%.

## Initial interpretation

The broad all-event aggregate is weak: positive direction-adjusted frequency is approximately 51–52% across horizons, with small median adjusted returns.

A directional asymmetry is visible in the supplied aggregate output:
- Upper-bound rejection outcomes are more directionally consistent than lower-bound rejection outcomes, particularly at 4h and 24h.
- Broad upper 24h: 57.383% positive frequency and +0.2898% median adjusted return.
- Broad lower 24h: 46.909% positive frequency and -0.1269% median adjusted return.
- The strict subgroup displays the same qualitative split.

This is a hypothesis for further investigation, not evidence of statistical significance, predictive probability, or a robust trading edge. The events may overlap and are not independent. No naive independent-event confidence intervals should be used. The event study excludes fees, spread, slippage, latency, funding, fills, position sizing, stop/target sequencing, and portfolio P&L. Excursions are path statistics, not realized trade returns. Broad and strict must not be pooled.

## Next validation step

Inspect the asset-by-direction aggregate rows and run additional event-level consistency checks before treating this as a finalized empirical result. In particular:
- Check the upper/lower split within each asset (to determine whether the pooled asymmetry is broadly distributed or concentrated in a few assets).
- Verify status counts, unique event identities within each cohort, and finite metrics for complete horizons.
- Keep the analysis descriptive and avoid optimizing definitions/horizons on these same observations.

The full event-level CSVs are local generated outputs; this checkpoint records the user-reported run and aggregate tables, not a claim that the generated CSVs have been uploaded to GitHub.
