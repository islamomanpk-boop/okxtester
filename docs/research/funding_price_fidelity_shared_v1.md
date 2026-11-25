# Shared Funding Price Fidelity Research V1

**Scope:** Shared infrastructure research for every market-regime phase in OKX Price Action V1 (Phase 3, Phase 1, Phase 2, Phase 4, and Phase 5). This is not a Phase-3-only result.
**Status:** OPEN — source reconnaissance completed; exact settlement-price policy not yet validated.
**Last updated:** 2026-11-25

## Why this document is shared

Funding costs affect every strategy and regime whenever a position crosses a funding settlement. This research therefore belongs to the common data/execution layer. Every phase must use the same approved funding contract and price-fidelity policy; phase-specific work must not independently redefine funding marks or silently bypass the funding gate.

## Current implementation and safeguards

- Shared validator: `src/funding_coverage.py`.
- Trade-level funding application: `src/execution_engine.py`.
- Portfolio funding application: `src/portfolio_backtester.py`.
- Experiment loader and provenance: `src/run_exit_experiments.py`.
- Historical mark-price reconnaissance probe: `src/inspect_okx_mark_price_history.py`.
- Funding contracts are explicit and fail closed; `exact` mode requires a supplied mark price. Current exploratory contract remains explicitly labelled `candle_close_proxy`.
- The engine records funding source/mode provenance. Do not weaken these requirements to unblock a phase.

## Evidence recorded so far

### Public historical mark-price candle endpoint

Official endpoint:
`GET /api/v5/market/history-mark-price-candles`

The probe sampled 12 evenly spaced funding timestamps for each of BTC, ETH, SOL, DOGE, and AVAX:
- 60 requests; 60 exact-timestamp mark candles found.
- 0 API errors, missing mark candles, duplicate extra rows, or incomplete candles.
- All returned candles had `confirm=1`.
- 50 trade-close comparisons were possible; 10 boundary comparisons were excluded because local trade candles did not cover those timestamps.
- Across the 50 comparisons, 41 differences printed as zero at six decimal places; pooled range was -1.217730 to +1.012818 bps. Every asset's reported median was zero at displayed precision.

Interpretation: useful evidence of endpoint availability at the selected timestamps and close agreement between two one-minute candle closes. It does **not** establish full historical coverage or identify the exact funding settlement snapshot. Mark OHLC remains a candle-derived proxy.

### OKX account bills: candidate recorded funding mark

The official OKX V5 account-bills documentation describes `px` as the mark price for funding-fee expense/income bill subtypes `173` and `174`. This is a high-priority candidate for validating actual account funding settlements.

Limitations:
- Account bills are private and account-specific.
- Bill `ts` is the balance-update completion time, so it must not automatically be equated to the public funding timestamp.
- A user's realized bill records cannot alone provide a universal mark-price history for hypothetical positions that were never held.
- The mapping of bill rows to positions/settlements and the relationship among `px`, `sz`, `pnl`, funding rate, and contract specifications still require empirical reconciliation.

## Source checkpoint and reproducibility

Detailed evidence, live probe output, boundary analysis, official documentation findings, and next steps are preserved in:
[`docs/research_checkpoints/2026-11-25_okx_historical_mark_price_source_recon_v1.md`](../research_checkpoints/2026-11-25_okx_historical_mark_price_source_recon_v1.md)

Probe command from repository root:
```bash
PYTHONPATH=src python -m py_compile src/inspect_okx_mark_price_history.py
PYTHONPATH=src python src/inspect_okx_mark_price_history.py
```

The 60-sample probe and focused funding/execution CI workflow passed on commit `90668a27a2b3a5eb0b82328a6f22435e5fc8be5f`, workflow run #25. CI validates compilation and focused tests, not settlement-price equivalence.

## Required next validation

1. If the user elects to use account records, retrieve a small read-only sample of their own funding bills. Credentials must remain local, outside chat, source control, logs, and reports.
2. Verify subtype, instrument, bill timestamp, `px`, `sz`, `pnl`, balance change, and currency fields.
3. Reconcile bill records with public funding events while accounting for balance-update timing.
4. Test the correct contract-specific funding formula; do not infer it solely from field names.
5. Determine whether the bill price is consistently populated and whether records are per settlement/position or aggregated.
6. Search for a documented universal source or exchange confirmation for exact historical settlement marks.
7. If no universal source exists, propose a clearly labelled proxy policy and stress-test its effect before authorizing exploratory PnL work.

## Cross-phase rules and current gate

- This shared research applies to all five phases and all assets.
- Keep `candle_close_proxy` explicitly approximate.
- Never label public mark-candle open/close as the exact settlement mark without independent evidence.
- Do not change `exact` mode or claim exact funding from candle timestamp alignment.
- Gate 0 / G0-03 remains **OPEN**. Authoritative strategy PnL backtests remain blocked pending a documented funding-price fidelity decision.
- Any future change must update this shared document, the detailed checkpoint, relevant tests, and the common engine contract before any phase consumes it.


## Additional settlement-timing and contract-formula findings (2026-11-25)

A review of the current OKX funding-fee mechanism explanation adds two important constraints to the account-bill reconciliation:

- Funding assessment is performed within milliseconds; OKX says the actual assessment may take up to a minute. A position opened shortly after the nominal clock time can still be assessed if the assessment process has not finished.
- The funding rate applied during assessment is the most recent rate calculated in the previous minute. Therefore, the public funding-history timestamp, the rate record timestamp, and the account-bill balance-update timestamp must not be assumed to be the same instant.
- OKX describes funding fee as position value multiplied by the funding rate. For USDT/USDC-margined contracts, position value is contracts × contract size × contract multiplier × mark price. For crypto-margined contracts, position value is contracts × contract size × contract multiplier ÷ mark price. Contract metadata and settlement currency are therefore essential to any reconciliation.

Official mechanism reference: https://www.okx.com/help/perps-funding-fee-mechanism. These published formulas are a reconciliation starting point, not proof that a particular account bill's `pnl` can be reconstructed without considering the account's actual position/leg structure and bill semantics.

### Consequence for validation

Do not join account bills to funding history on exact timestamp equality. Build a bounded candidate window around each public settlement, retain original timestamps, and inspect the bill's `instId`, `subType`, `px`, `sz`, `pnl`, `balChg`, `posBalChg`, `ccy`, and `mgnMode`. Reconcile sign, amount, and currency using the contract's `ctVal`, `ctMult`, `ctType`, and settlement currency. Preserve ambiguous or aggregated rows as unresolved rather than forcing a one-to-one mapping.


## Demo API access boundary (2026-11-25)

The user currently has demo-only OKX API access. This is suitable for testing authentication, the demo request header, read-only permissions, response parsing, and safe local handling. It cannot validate historical funding settlements from the user's real account, and demo bills may contain no funding events or may not represent production accounting behavior.

Any demo test must:
- Use a demo API key with **Read** permission only; do not enable Trade or Withdraw.
- Send `x-simulated-trading: 1` on demo private REST requests.
- Make read-only GET requests only; do not place orders or modify demo balances for this source-validation task.
- Keep API key, secret, and passphrase on the user's device; never paste them into chat, commit them, or include them in logs/reports.
- Treat a successful demo response strictly as an integration/authentication test, not as evidence that actual account funding bill `px` records are available or validated.

The next meaningful production-settlement validation still requires a separate read-only real-account key or another independently sourced real account bill sample. Until then, the account-bill route remains a promising but unvalidated candidate and G0-03 remains OPEN.
