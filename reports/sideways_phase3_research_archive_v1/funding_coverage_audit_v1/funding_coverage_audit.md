# OKX Realized Funding Coverage Audit

**Result: PASS**  
**Execution:** user's Termux environment, actual processed local CSVs  
**Audit scope:** 2025-10-20 00:00 UTC through 2026-11-19 16:00 UTC  
**Expected settlement interval:** 8 hours (28,800,000 ms)  
**Source:** processed OKX realized-rate CSVs; no missing settlements imputed or treated as zero.

| Asset | Instrument | Rows | Missing | First UTC | Last UTC | SHA-256 |
|---|---|---:|---:|---|---|---|
| BTC | BTC-USDT-SWAP | 1,188 | 0 | 2025-10-20 00:00 | 2026-11-19 16:00 | `44c1c9c219adb2f1808612a492f451b995d27d3a258d5bbd5ef8ff1a4ccf5642` |
| ETH | ETH-USDT-SWAP | 1,188 | 0 | 2025-10-20 00:00 | 2026-11-19 16:00 | `146a3b8310eb0f361d014c61aeb3cd311e19964faf4a231f98881d228fdbe903` |
| SOL | SOL-USDT-SWAP | 1,188 | 0 | 2025-10-20 00:00 | 2026-11-19 16:00 | `fe473ac103c549853fd0ca044d8607776fe07bdfd95f1fcf303d6df35fee3041` |
| DOGE | DOGE-USDT-SWAP | 1,188 | 0 | 2025-10-20 00:00 | 2026-11-19 16:00 | `c00d261ba97e2d64fbb173e4d4c28c01970b3ee3ea4ff1e8e7d32c1ac4113749` |
| AVAX | AVAX-USDT-SWAP | 1,188 | 0 | 2025-10-20 00:00 | 2026-11-19 16:00 | `c3e84c3271dd233f65e9cf61393f49109b3f155c6f0cd7d44bd1eab805c444a9` |

**Totals:** 5,940 rows; zero missing settlements. Every asset had 1,187 intervals, all exactly 8 hours. No duplicate timestamps, gaps, irregular intervals, instrument mismatches, invalid rates, or cross-asset timestamp differences were reported. Audit failures: none.

## Provenance

The exact absolute Termux source paths are recorded in the accompanying JSON manifest. The processed CSVs remain local and are intentionally not committed to Git. The SHA-256 values above identify the exact files audited.

## Interpretation and limitations

This confirms current local funding-file availability, schema/instrument validation, timestamp ordering, expected cadence, coverage endpoints, and cross-asset timestamp equality for this run. It does not validate funding cashflow calculations in the backtester, mark-price availability/accuracy, or engine fail-closed behaviour when funding is missing. It is a data-coverage audit, not a strategy backtest or profitability result. Gate 0 therefore remains CONDITIONAL HOLD.
