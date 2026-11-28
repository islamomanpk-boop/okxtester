# G0-08 Local Read-Only Account Fee Probe V1 — 2026-11-28

## Purpose and safety

This checkpoint records tooling for obtaining current account-specific OKX fee rates without sharing credentials in chat or running private account requests in GitHub Actions.

The script calls only:
- GET /api/v5/public/time
- GET /api/v5/account/trade-fee

It does not call order placement, order amendment/cancellation, trade history, position, withdrawal or transfer endpoints. It never prints or writes API credentials. The owner must use a dedicated API key with Read permission only and no Trade/Withdraw permissions. The script cannot independently verify the key's configured permissions.

## Code and verification

- Commit: a5ac62831cfba902b2af5dae3b35c13b46a4d333.
- Probe: src/inspect_okx_account_fee_rates_readonly.py.
- Offline tests: src/test_okx_account_fee_rates_readonly.py.
- Successful CI: https://github.com/islamomanpk-boop/okxtester/actions/runs/46159858988.
- 10 offline fee-probe tests passed.
- Current public instrument metadata was re-fetched and uploaded; artifact ID 15269490178, ZIP SHA-256 c789262b49b71841d91afb41fe541155128d93f14c4aa40f96af4f12fbc6a911.

The CI workflow deliberately does not execute the authenticated probe and does not receive secrets.

## Probe behavior

For each of BTC-USDT, ETH-USDT, SOL-USDT, DOGE-USDT and AVAX-USDT instrument families, the probe requests the current account's SWAP fee rates and requires exactly one matching feeGroup with groupId 4. It records the account fee level, raw maker/taker rates and nonnegative commission-cost rates.

OKX fee sign convention: negative rates are commissions; positive rates are rebates. The script maps commission cost to max(0, -raw_rate) and does not count rebates as negative costs.

The JSON report is written locally to reports/g0_08_account_fee_rates_local_v1.json by default. It contains account-specific fee data and is not uploaded by CI. The owner may share the report or only the relevant fee level/rates if comfortable; API credentials must never be shared.

## Termux instructions

From the repository root, after creating a dedicated Read-only API key in OKX:

```bash
read -r -s -p "OKX API key (Read only): " OKX_API_KEY; echo
read -r -s -p "OKX API secret: " OKX_API_SECRET; echo
read -r -s -p "OKX API passphrase: " OKX_API_PASSPHRASE; echo
export OKX_API_KEY OKX_API_SECRET OKX_API_PASSPHRASE
python src/inspect_okx_account_fee_rates_readonly.py --output reports/g0_08_account_fee_rates_local_v1.json
unset OKX_API_KEY OKX_API_SECRET OKX_API_PASSPHRASE
```

The probe uses OKX server time for signature timestamps. It fails closed if an asset response is missing or the fee-group mapping is ambiguous. Do not commit or upload the local fee report unless explicitly intended.

## Remaining G0-08 work

1. Run the local probe with a dedicated Read-only key, or use an account fee-rate statement/export.
2. Reconstruct historical effective instrument metadata for the full 2025-10 to 2026-11 research period; current public metadata and upcoming-change fields do not prove historical values.
3. Document the selected fee assumptions and their effective dates.
4. Complete G0-07 contract conversion and rounding only after the metadata/fee assumptions are verified.

G0-08 remains OPEN. Gate 0 remains CONDITIONAL HOLD. No strategy PnL, execution simulation, orders, fills, Gate 2+ or live trading is authorized.
