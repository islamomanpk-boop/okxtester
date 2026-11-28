# G0-03 Funding Contract Integration — 2026-11-28

**Project:** OKX Price Action V1  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** Code-level integration and synthetic parity checks passed; real local-input integration remains pending.  
**Scope:** Funding loader/coverage contract/standalone and portfolio engine integration only. No strategy backtest or real-input trade simulation.

## 1. Existing real funding-file evidence

The user's actual local processed funding CSVs were previously audited in Termux on 2026-11-25:
- Five assets: BTC, ETH, SOL, DOGE, AVAX USDT swaps.
- 1,188 rows per asset; 5,940 total.
- Common timestamp coverage: 2025-10-20 00:00 UTC through 2026-11-19 16:00 UTC.
- 1,187 intervals per asset, each exactly 8 hours.
- Zero missing settlements, gaps, irregular intervals, duplicates, instrument mismatches, invalid rates or cross-asset timestamp differences.
- The exact five SHA-256 hashes are in `reports/sideways_phase3_research_archive_v1/funding_coverage_audit_v1/funding_coverage_manifest.json`.

The CSV files remain local and are not committed. This existing audit proves source coverage/hash integrity for that run; it does not yet prove the production runner loads those exact files into valid funding contracts in the user's local environment.

## 2. Additional code-level checks

Added `src/test_funding_engine_parity.py`:
- Runs the same synthetic one-position scenario through the standalone execution engine and shared-capital portfolio engine.
- Verifies identical funding cashflows under `exact` and `candle_close_proxy` modes.
- Verifies one funding event at entry is excluded and one at exit is included under `entry_time < funding_timestamp <= exit_time`.
- Confirms the settlement count, entry/exit times, and position quantity agree.

Added `src/audit_funding_contract_integration.py`:
- Read-only integration harness that uses the production `load_funding_contract` loader and `validate_funding_contract` contract validator.
- Reads the five actual local CSVs and the committed manifest.
- Verifies file SHA-256, instrument identity, row count, first/last timestamps, exact scheduled settlements, cross-asset timestamp equality and the entry-exclusive/exit-inclusive boundary.
- Reports the current explicit `candle_close_proxy` mode and confirms exact settlement marks are not present in the rate-only CSVs.
- Does not simulate trades, calculate strategy PnL, copy source CSVs, or upload local files.

Added `src/test_funding_contract_integration.py` for deterministic synthetic fixtures, including five-asset timestamp mismatch and manifest failure cases.

## 3. CI evidence

Funding/execution workflow [46150715018](https://github.com/islamomanpk-boop/okxtester/actions/runs/46150715018) completed SUCCESS on commit `bc4be49e3f8aacd2fcd534d3c81381ac2c635202`.

**90/90 tests passed** across:
- full-window mark-price audit helper tests;
- funding coverage contract tests;
- funding manifest loader tests;
- new read-only contract integration harness tests;
- new standalone/portfolio funding arithmetic parity tests;
- standalone execution engine tests;
- portfolio backtester tests;
- portfolio experiment integration tests;
- trailing portfolio integration tests;
- portfolio allocator and safety tests.

These CI tests use synthetic fixtures. They do not replace the real local CSV integration run.

## 4. Required local real-input integration run

The actual CSVs are intentionally not in GitHub and are not available in this ChatGPT session. The remaining G0-03 input-integration step therefore requires the read-only command below to run in the user's Termux environment, from the canonical repository root:

```bash
python src/audit_funding_contract_integration.py \
  --funding-dir "$HOME/okx_scalping_data/funding_rates/processed" \
  --manifest reports/sideways_phase3_research_archive_v1/funding_coverage_audit_v1/funding_coverage_manifest.json \
  --output reports/funding_contract_integration_v1.json
```

Expected successful status: `REAL_FUNDING_INPUT_CONTRACT_INTEGRATION_PASS`.

The resulting JSON report contains only counts, hashes, schedule/coverage metadata and explicit proxy-mode status; it does not include or copy the raw CSV contents. Share or upload that JSON report so its hashes and counts can be reconciled with the archived funding manifest.

## 5. Gate disposition and limitations

**G0-03 remains PARTIALLY CLOSED / ACCEPTANCE OPEN.** Code-level fail-closed funding contracts, both engine integrations, synthetic arithmetic parity and the read-only real-input harness are implemented and CI-tested. The actual local-input harness has not yet been run in Termux.

The current production loader explicitly uses `candle_close_proxy`; exact OKX settlement mark-price fidelity is not established by the realized-rate CSVs. The separately archived 4H mark-price snapshot is a candidate proxy, not exact settlement mark evidence. Keep exact mark-price fidelity and fee/instrument/contract assumptions as separate Gate 0 blockers.

No strategy PnL backtest, execution experiment, order/fill simulation on market data, strategy selection, Gate 2+ or live trading was performed or authorized.
