# Breakout Event Quantile-Population Diagnostic V4 — Runtime Results

Date: 2026-11-23  
Script: `research/validation/breakout_event_quantile_population_diagnostic_v4.py`  
Status: **DIAGNOSTIC ONLY — EVENT GATE REMAINS ON HOLD**

## Question

Does calculating the sideways-width P25/P40 thresholds on unique 4H feature rows, rather than on joined 15M rows, explain the discrepancy between reconstructed breakout event counts and the historical accepted 20-count table?

## Runtime output

```text
READ-ONLY BREAKOUT QUANTILE-POPULATION DIAGNOSTIC V4
Common 1M timestamps: 569,125
ER: exact historical 12-change absolute-price formula.
Comparison: quantiles on unique 4H feature rows vs joined 15M rows.
Other feature formulas, alignment, and accepted event mask held fixed.
BTC UNIQUE_4H_FEATURE_ROWS: source_rows=2,358 P25=3.242203251% P40=3.947937289%
BTC JOINED_15M_ROWS: source_rows=37,721 P25=3.242203251% P40=3.948630141%
ETH UNIQUE_4H_FEATURE_ROWS: source_rows=2,358 P25=4.245214260% P40=5.474563343%
ETH JOINED_15M_ROWS: source_rows=37,721 P25=4.242326420% P40=5.481886231%
SOL UNIQUE_4H_FEATURE_ROWS: source_rows=2,358 P25=5.067174178% P40=6.114541712%
SOL JOINED_15M_ROWS: source_rows=37,721 P25=5.067043049% P40=6.114541712%
DOGE UNIQUE_4H_FEATURE_ROWS: source_rows=2,358 P25=5.165724421% P40=6.264057580%
DOGE JOINED_15M_ROWS: source_rows=37,721 P25=5.165724421% P40=6.264057580%
AVAX UNIQUE_4H_FEATURE_ROWS: source_rows=2,358 P25=5.704867571% P40=6.916215821%
AVAX JOINED_15M_ROWS: source_rows=37,721 P25=5.703624733% P40=6.916215821%

========================================================================================
UNIQUE_4H_FEATURE_ROWS
asset definition direction  actual  expected  pass
  BTC        P25     UPPER      60        81 False
  BTC        P25     LOWER      54        62 False
  BTC        P40     UPPER      84       115 False
  BTC        P40     LOWER      69        91 False
  ETH        P25     UPPER      47        51 False
  ETH        P25     LOWER      46        51 False
  ETH        P40     UPPER      67        77 False
  ETH        P40     LOWER      75        87 False
  SOL        P25     UPPER      53        71 False
  SOL        P25     LOWER      76        77 False
  SOL        P40     UPPER      74        96 False
  SOL        P40     LOWER     102       117 False
 DOGE        P25     UPPER      62        65 False
 DOGE        P25     LOWER      52        55 False
 DOGE        P40     UPPER      73        75 False
 DOGE        P40     LOWER      71        81 False
 AVAX        P25     UPPER      66        83 False
 AVAX        P25     LOWER      63        64 False
 AVAX        P40     UPPER      77       109 False
 AVAX        P40     LOWER      79        84 False
EXACT MATCHES: 0/20

========================================================================================
JOINED_15M_ROWS
asset definition direction  actual  expected  pass
  BTC        P25     UPPER      60        81 False
  BTC        P25     LOWER      54        62 False
  BTC        P40     UPPER      84       115 False
  BTC        P40     LOWER      69        91 False
  ETH        P25     UPPER      47        51 False
  ETH        P25     LOWER      46        51 False
  ETH        P40     UPPER      67        77 False
  ETH        P40     LOWER      75        87 False
  SOL        P25     UPPER      53        71 False
  SOL        P25     LOWER      76        77 False
  SOL        P40     UPPER      74        96 False
  SOL        P40     LOWER     102       117 False
 DOGE        P25     UPPER      62        65 False
 DOGE        P25     LOWER      52        55 False
 DOGE        P40     UPPER      73        75 False
 DOGE        P40     LOWER      71        81 False
 AVAX        P25     UPPER      66        83 False
 AVAX        P25     LOWER      63        64 False
 AVAX        P40     UPPER      77       109 False
 AVAX        P40     LOWER      79        84 False
EXACT MATCHES: 0/20

No controls, forward outcomes, matching, or profitability calculations.
No files were written or modified.
```

## Interpretation

1. Both threshold populations produced exactly the same reconstructed event counts in all 20 asset/definition/direction cells.
2. Neither population reproduced any of the 20 historical accepted counts (0/20 exact matches).
3. The threshold values differ slightly for some asset/definition combinations, but those differences did not change the event counts in this run.
4. Therefore, this tested quantile-population choice does **not** explain the event-count discrepancy.
5. The previous source comparison found the standalone 4H OHLC inputs and 1M-resampled 4H OHLC values identical across all 2,370 common 4H timestamps per asset. That tested source-value distinction also does not explain the discrepancy.

## Research decision

**Keep the breakout event gate on HOLD.** The historical 20-count table remains a record of previously reported counts, not an independently reproduced accepted baseline. Do not create matched controls, run forward-outcome comparisons, conduct inference, or calculate profitability until the exact historical event-producing script/command and its contemporaneous output are recovered, or a newly versioned event engine is transparently established and validated.

## Scope and limitations

- This is a read-only diagnostic.
- It compares only the two stated quantile populations while holding the other V4 implementation choices fixed.
- It does not establish that every possible historical implementation detail has been tested.
- It does not validate the historical accepted counts.
- No controls, forward outcomes, matching, inference, trades, or PnL were calculated.
- The user-provided runtime output is preserved above.
