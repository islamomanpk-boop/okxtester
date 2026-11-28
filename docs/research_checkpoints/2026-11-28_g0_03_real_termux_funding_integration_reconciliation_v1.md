# G0-03 real Termux funding integration reconciliation — 2026-11-28

## Result

**Real-input funding contract integration: PASS.** The user ran `src/audit_funding_contract_integration.py` locally in Termux against the five actual funding CSVs and the archived funding coverage manifest. The script returned `REAL_FUNDING_INPUT_CONTRACT_INTEGRATION_PASS`.

- Scope: read-only real local funding CSV → production loader → fail-closed funding contract validation.
- Assets: AVAX, BTC, DOGE, ETH, SOL.
- Rows: 1,188 per asset; 5,940 total.
- Common timestamps: 1,188, identical across all five assets.
- Per-asset schedule count: 1,188.
- Trade-window boundary: entry timestamp excluded; exit timestamp included.
- Source CSVs copied/uploaded: false.
- Strategy PnL calculated: false.
- Trade simulation performed: false.

The user verified the saved local JSON report at `reports/funding_contract_integration_v1.json`. SHA-256: `557f59fd4c2aa1588ef0716aca4ed3411c6bc1f19b6702a93336a6ace2067e70`.

The report explicitly records `mark_price_mode=candle_close_proxy`, `exact_mark_price_available=false` for every asset, and `exact_settlement_mark_price_verified=false`.

## Interpretation and gate boundary

This completes the previously outstanding **local real-input execution/reconciliation subtask** of the G0-03 funding contract integration harness. The harness exercised the production loader and fail-closed funding contract against the user's real local inputs and verified the manifest-backed source/schedule/timestamp/boundary contract.

It does **not** establish that candle-close proxy prices equal the exact mark prices used for OKX funding settlement. Exact settlement-mark fidelity remains unverified and is tracked separately under G0-09. Do not change the production funding price mode based on this result.

No strategy PnL, trade simulation, execution simulation, orders or fills were performed. The local funding CSVs and JSON report remain on the user's Termux device; neither the source CSVs nor the JSON report were uploaded to GitHub. Only this evidence summary and the user-reported report checksum are recorded in the repository.

**Gate decision:** G0-03 real-input funding contract integration subtask = PASS. Overall G0-03 gate acceptance remains OPEN pending exact settlement-mark/funding-policy resolution and any remaining gate-level reconciliation. Gate 0 remains **CONDITIONAL HOLD**. G0-07, G0-08 and G0-09 remain open. No Gate 2+, strategy PnL backtest, execution simulation, orders, fills or live trading is authorized.

## Reproduction

```bash
python src/audit_funding_contract_integration.py \
  --funding-dir "$HOME/okx_scalping_data/funding_rates/processed" \
  --manifest reports/sideways_phase3_research_archive_v1/funding_coverage_audit_v1/funding_coverage_manifest.json \
  --output reports/funding_contract_integration_v1.json
```
