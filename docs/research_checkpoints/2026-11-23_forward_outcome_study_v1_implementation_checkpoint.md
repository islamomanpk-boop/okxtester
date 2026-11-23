# Forward Rejection Outcome Study V1 — Implementation Checkpoint

Date: 2026-11-23
Branch: `price-action-v1`
Status: **Implementation committed; local execution and tests pending. No outcomes have been calculated.**

## Input inspection

The user's read-only Termux inspection confirmed:
- Event ledger exists at `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`.
- Event columns include asset, definition, direction, snapshot index, segment, rank, test boundaries, first strong rejection timestamp, rejection OHLC, and closure reason.
- Original 1M file exists at `~/okx_scalping_data/BTC_USDT_USDT_1m.csv` with `ts, open, high, low, close, vol`.
- New output directory `reports/sideways_rejection_forward_outcomes_v1` did not exist and was empty at inspection.
- The event CSV was not found as a tracked GitHub file at the expected repository path; it is a local generated research output. Do not assume it is committed or alter it.

## Implementation files

- `research/sideways_rejection_forward_outcomes_v1.py`
- `tests/test_sideways_rejection_forward_outcomes_v1.py`
- Frozen methodology: `docs/research_checkpoints/2026-11-23_historical_rejection_forward_outcome_study_spec_v1.md`

The script:
- Uses the existing event ledger and original five 1M files; it does not alter either.
- Filters to events with a first strong rejection and requires 1,154 broad plus 838 strict events.
- Derives confirmation as rejection 15M open timestamp + 900,000 ms.
- Uses the exact confirmation-minute OPEN as a descriptive reference entry.
- Calculates 15m, 1h, 4h, and 24h outcomes from forward 1M bars only.
- Requires exact timestamp coverage for each horizon; incomplete horizons are censored and do not contribute returns.
- Calculates raw return, direction-adjusted return, favorable/adverse excursion, and preserves horizon high/low/close.
- Produces broad and strict summaries separately, including overall, asset, direction, and asset-direction breakdowns, medians and quantiles, and censored counts.
- Does not include fees, spread, slippage, latency, funding, fills, sizing, or portfolio P&L.
- Refuses to write into a non-empty output directory.

Timestamp gaps are not globally fatal: they remain visible in the validation audit and any horizon containing a gap is censored by exact timestamp comparison. No missing minute is filled or bridged.

## Unit tests

Five tests cover:
1. Upper/lower direction-adjusted return signs.
2. Exact 15-minute horizon boundary and ending close.
3. Missing-minute horizon censoring.
4. Exact confirmation timestamp requirement (no look-ahead).
5. Lower-side favorable/adverse excursion direction.

## Expected local command

After syncing branch `price-action-v1` in Termux:

```bash
python -m unittest tests.test_sideways_rejection_forward_outcomes_v1 -v
python research/sideways_rejection_forward_outcomes_v1.py
```

Default inputs:
- `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv`
- `~/okx_scalping_data/{BTC,ETH,SOL,DOGE,AVAX}_USDT_USDT_1m.csv`

Default new output:
- `reports/sideways_rejection_forward_outcomes_v1/event_level_outcomes.csv`
- `reports/sideways_rejection_forward_outcomes_v1/aggregate_summary.csv`
- `reports/sideways_rejection_forward_outcomes_v1/data_validation.csv`

## Execution status and interpretation

Implementation and tests are committed to GitHub. They have not yet been executed in the user's Termux environment. Do not claim tests passed or outcomes exist until the user runs the commands and supplies the result. The next action is local test execution, followed by the study run only if tests pass.
