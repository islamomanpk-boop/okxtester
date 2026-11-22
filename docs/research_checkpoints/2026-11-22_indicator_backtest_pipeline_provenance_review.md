# Indicator and Backtest Input Provenance Review

Date: 2026-11-22
Project branch: `price-action-v1`

## Scope

Read-only source inspection of:
- `~/okx_scalp/2_indicators.py`
- `~/okx_scalp/2_indicadors.py`
- input/output references in `backtest.py`, `3_backtest.py`, and `4_report.py`

No scripts were executed.

## Findings

1. Both indicator scripts read gzip CSV files from `~/okx_scalp/data/*.csv.gz`, excluding files ending in `_ind.csv.gz`.
2. Both write indicator-enriched gzip CSV files to the same directory, named `<coin>_ind.csv.gz`.
3. Neither indicator script contains a 1-minute resampling operation or a reference to `~/okx_scalping_data` or the five `*_USDT_USDT_1m.csv` files.
4. The two indicator scripts are nearly identical, but differ in VWAP grouping:
   - `2_indicators.py` groups timestamps using `dt.floor('D')` (UTC calendar-day grouping if timestamps are UTC-aware).
   - `2_indicadors.py` groups using `dt.floor('12H')`.
   This difference is unrelated to proving the origin of the 1-minute CSVs, but should be reconciled if that older project is ever reused.
5. `backtest.py` and `3_backtest.py` read `*_ind.csv.gz` files from `~/okx_scalp/data` and write results to `~/okx_scalp/results.csv`. Their displayed resampling calls calculate daily aggregates; they do not demonstrate conversion of the investigated 1-minute files.
6. `4_report.py` reads `~/okx_scalp/results.csv`.
7. The inspected older project therefore appears to be a separate 15-minute OKX-perpetual workflow: 15m source candles -> indicator-enriched 15m gzip files -> backtest results. No evidence links this pipeline to the five 1-minute CSVs in `~/okx_scalping_data`.

## Conclusion

The five 1-minute CSVs remain of **unverified provenance**. The older `okx_scalp` scripts do not currently explain their creation.

## Caution

- The indicator scripts' volume-derived calculations depend on the source `vol` field. Their results cannot validate volume units.
- The two indicator scripts differ in VWAP reset interval, so their outputs should not be treated as interchangeable without review.
- No script was executed and no data or existing report was modified.
- All Price Action V1 experiments remain paused.

## Next step

Search the remaining local project source/documentation files for exact references to the five 1-minute filenames, the `~/okx_scalping_data` directory, and OKX candle endpoints. Limit the search to source/config/documentation files and avoid running scripts or scanning large CSV datasets.
