# Funding Data Collection V1

## Purpose

Collect actual OKX USDT perpetual-swap funding rates for BTC, ETH, SOL,
DOGE and AVAX for the period 2025-10-20 through 2026-11-19 UTC.

## Sources

- Historical monthly ZIP archives provide the older history.
- OKX public `funding-rate-history` API fills the recent period.
- The API's `realizedRate` field is required. Predicted `fundingRate`
  must not be substituted for realized settlement rates.

## Reconciliation

The merger compares every overlapping archive/API timestamp. Conflicting
rates cause a hard failure. Duplicate timestamps with conflicting values
are rejected. The final records are sorted by funding timestamp.

Settlement intervals are measured from observed timestamps. The pipeline
does not assume that every instrument always settles every eight hours.

## Local storage

Raw ZIP files and processed CSVs are stored under:

`~/okx_scalping_data/funding_rates/`

They are intentionally excluded from normal Git history. Code, tests,
documentation, manifests, checksums and audit reports are tracked in Git.

## Running

```bash
python -m unittest discover -s src -p 'test_merge_funding_history.py' -v
python src/merge_funding_history.py
```

A successful run writes the reconciled processed CSVs locally and updates
`reports/funding_data_audit.md`. Do not begin cost-adjusted backtesting if
the reconciliation fails.
