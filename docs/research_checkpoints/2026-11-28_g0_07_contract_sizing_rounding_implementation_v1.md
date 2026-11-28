# G0-07 Contract Sizing and Rounding Implementation V1 — 2026-11-28

## Purpose and disposition

This checkpoint adds a pure, fail-closed sizing adapter for current OKX linear USDT perpetual instrument metadata. It addresses the code-level contract conversion, lot/minimum-size handling, price-tick rounding and post-rounding risk recalculation requirement.

This is an isolated helper only. It is not wired into `execution_engine.py` or `portfolio_backtester.py`, does not alter historical backtests, and does not place orders. G0-07 and Gate 0 remain OPEN / CONDITIONAL HOLD pending the remaining evidence and policy decisions below.

## Contract and rounding rules

- Convert base-asset quantity to exchange contracts using `contracts × ctVal × ctMult = base units`.
- Use decimal arithmetic for tick and lot increments.
- Floor contract quantity to `lotSz`; never round quantity upward.
- Reject a result below `minSz`; never round it up to the minimum.
- Enforce the applicable `maxMktSz`, `maxStopSz` or `maxTriggerSz` for the requested order category. Reject over-limit quantities rather than silently splitting an order.
- For risk budgeting, round a LONG stop down to the tick and a SHORT stop up to the tick. This deliberately rounds away from entry so the modeled stop distance is not understated. It is a risk-budgeting convention, not a claim about earliest trigger timing.
- Recalculate cost-adjusted risk after stop-price rounding and contract flooring, using explicit taker-fee and slippage inputs. The helper rejects if the resulting risk exceeds the configured budget.
- Fee and slippage values have no defaults. Callers must supply the assumptions applicable to the account and modeled period.

## Instrument metadata boundary

The parser requires an exact, live, linear SWAP record settled in USDT, with contract value denominated in the asset and positive `ctVal`, `ctMult`, `tickSz`, `lotSz`, `minSz`, `maxMktSz`, `maxStopSz` and `maxTriggerSz`. It validates that `minSz` is an integer multiple of `lotSz`.

The 2026-11-28 public snapshot reports the following current contract increments:

| Asset | Base units per contract | Tick | Lot | Minimum |
|---|---:|---:|---:|---:|
| BTC | 0.01 BTC | 0.1 USDT | 0.01 contracts | 0.01 contracts |
| ETH | 0.1 ETH | 0.01 USDT | 0.01 contracts | 0.01 contracts |
| SOL | 1 SOL | 0.01 USDT | 0.01 contracts | 0.01 contracts |
| DOGE | 1,000 DOGE | 0.00001 USDT | 0.01 contracts | 0.01 contracts |
| AVAX | 1 AVAX | 0.001 USDT | 0.1 contracts | 0.1 contracts |

These are current-only values. The helper accepts metadata as an input and does not embed this table as a historical truth. Do not use the current snapshot retroactively across 2025-10 to 2026-11 until effective-dated parameter history is established.

## Stop trigger reference and execution-cost boundary

The available historical OHLCV files are last-trade candles. The existing candle stop logic therefore represents a last-price research model, but the engine has no explicit trigger-reference setting and is not a verified OKX algo-order emulator. For consistency with the available data, the working research-scope recommendation is to label the current candle model as `last`-price based. This is not a recommendation for live order configuration. A mark/index-triggered model requires matching historical mark/index candles and a separately validated stop path; it must not be approximated using last-trade OHLC.

Historical order-book depth, spread, queue position, latency and market impact remain unavailable. A required slippage input is a stress/model assumption, not a measured historical fill cost. Keep those limitations explicit.

## Fee evidence privacy

The current Demo account fee endpoint was successfully queried locally for all five instrument families on 2026-11-28. The authenticated response returned account fee data for each asset. The account-specific numeric report is retained locally and intentionally excluded from this public repository. The helper accepts a caller-supplied fee rate and does not embed any private account data. This current Demo snapshot does not establish historical or live-account fee rates.

## Files and verification

- Helper: `src/okx_contract_sizing.py`
- Unit tests: `src/test_okx_contract_sizing.py`
- Workflow: `.github/workflows/g0-07-contract-sizing-tests.yml`
- Scope: deterministic synthetic fixtures, including the five current contract increment patterns; no exchange credentials or network requests.
- No changes to existing execution engines, portfolio backtester, datasets or historical reports.

## Remaining G0-07 / Gate 0 work

1. Run and inspect the dedicated GitHub Actions test workflow; tests are synthetic unit tests, not exchange execution evidence.
2. Decide/approve the explicit last-price research trigger scope; do not treat it as a live-order recommendation.
3. Preserve the full-file OHLCV provenance limitation: 35/35 OKX samples matched, but no full-file acquisition/normalization manifest or row-by-row certification exists.
4. Establish evidence-backed slippage/spread/depth stress assumptions; do not claim current order-book snapshots prove historical execution cost.
5. Integrate the helper only after historical effective metadata is available and the standalone/portfolio sizing paths are reconciled.
6. Keep G0-08 open for historical fee/instrument effective dates and G0-09 open for exact settlement-mark fidelity.

No strategy PnL, execution simulation, order placement, fills, Gate 2+ or live trading was run or authorized.

