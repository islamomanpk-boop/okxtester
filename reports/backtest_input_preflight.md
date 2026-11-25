# Backtest Input Preflight

Sequential CSV validation.
Raw market and funding files remain local.

## BTC
- Signal rows: 37941
- Execution rows: 569125
- Execution first: 1760950200000
- Execution last: 1795097640000
- Funding rows: 1188
- Funding first: 1760918400000
- Funding last: 1795104000000

## ETH
- Signal rows: 37941
- Execution rows: 569125
- Execution first: 1760950200000
- Execution last: 1795097640000
- Funding rows: 1188
- Funding first: 1760918400000
- Funding last: 1795104000000

## SOL
- Signal rows: 37941
- Execution rows: 569126
- Execution first: 1760950200000
- Execution last: 1795097700000
- Funding rows: 1188
- Funding first: 1760918400000
- Funding last: 1795104000000

## DOGE
- Signal rows: 37941
- Execution rows: 569126
- Execution first: 1760950200000
- Execution last: 1795097700000
- Funding rows: 1188
- Funding first: 1760918400000
- Funding last: 1795104000000

## AVAX
- Signal rows: 37941
- Execution rows: 569127
- Execution first: 1760950200000
- Execution last: 1795097760000
- Funding rows: 1188
- Funding first: 1760918400000
- Funding last: 1795104000000

## Shared execution window
- Start: 1760950200000
- End: 1795097640000

## Issues

None detected.

## Result: PASS


## Scope and reproducibility limitations

This PASS is evidence that the five local funding CSVs were available and passed the checks implemented by this script at the time of that run. It does not record SHA-256 checksums, does not prove the files remain available in a later runtime, and does not check for missing expected funding settlements between the first and last timestamps. The separate funding reconciliation report records 1,188 rows and 1,187 observed 480-minute intervals per asset, but the processed files remain outside Git. Before Phase 3 backtesting, rerun a strengthened audit against the exact files and archive their hashes and settlement-gap results. This preflight PASS is not a strategy-backtest approval.
