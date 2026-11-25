# Phase 3 canonical Git vs VPS OHLCV reconciliation V1

**Recorded:** 2026-11-25  
**Supporting repository:** `islamomanpk-boop/okxtester_private@main`  
**Workflow source commit:** `0b798e4def1bd58ff3dbc1612c53fc0e5a986cd0`  
**Workflow run:** [45657820585](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45657820585) — completed successfully  
**Metadata-only artifact:** `15044456441`, SHA-256 `defe522a466fee197dc36a42cc08889dbc7f16d76468703b5d99771a1e5278e0`  
**Canonical snapshot commit:** `d7502306e89b0b78980eb9e3c8a39570b3b05966`  
**VPS source:** confirmed-only CSV exports plus targeted read-only SQLite lookup

## 1. Scope

The workflow downloaded the five canonical Git CSVs pinned to the exact historical Git commit above, verified each against its recorded SHA-256, verified the current VPS CSV hashes against the preceding VPS snapshot manifest, then performed a streaming timestamp merge and exact decimal comparison of OHLC fields and volume mappings. It also queried SQLite read-only for the one canonical timestamp absent from the confirmed-only VPS SOL export.

No raw market files were committed or uploaded as workflow artifacts. No VPS CSV, SQLite row, service, or downloader was changed. Only the small comparison metadata JSON was uploaded.

## 2. Results

All five canonical Git file hashes matched their pinned values. All five VPS file hashes matched the previously audited VPS snapshot. Both datasets were monotonic in timestamp order.

| Asset | Canonical rows | VPS rows | Matched timestamps | Canonical-only | VPS-only | OHLC mismatches |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 569,125 | 578,022 | 569,125 | 0 | 8,897 | 0 |
| ETH | 569,125 | 578,051 | 569,125 | 0 | 8,926 | 0 |
| SOL | 569,126 | 578,080 | 569,125 | 1 | 8,955 | 0 |
| DOGE | 569,126 | 578,111 | 569,126 | 0 | 8,985 | 0 |
| AVAX | 569,127 | 578,141 | 569,127 | 0 | 9,014 | 0 |

**Every matched timestamp has exact OHLC equality** (Decimal comparison, not rounded display values). No open, high, low, or close mismatch was found.

The canonical snapshot begins at 2025-10-20 08:50 UTC. The VPS snapshot begins earlier, at 2025-10-20 00:00 UTC. The canonical data ends on 2026-11-19 around 14:14–14:16 UTC, while the VPS snapshot extends through 2026-11-25 with staggered asset endpoints. Thus the canonical files are an earlier, narrower overlapping snapshot, not byte-identical copies of the VPS exports.

## 3. Volume-field reconciliation

For every matched timestamp in all five assets, the canonical file's column named `vol` equals the VPS export's `volCcy` value exactly. It does **not** consistently equal the VPS export's `vol` field.

| Asset | Canonical `vol` = VPS `vol` | Canonical `vol` = VPS `volCcy` | Canonical `vol` = VPS `volCcyQuote` |
|---|---:|---:|---:|
| BTC | 0 / 569,125 | 569,125 / 569,125 | 0 / 569,125 |
| ETH | 0 / 569,125 | 569,125 / 569,125 | 0 / 569,125 |
| SOL | 569,125 / 569,125 | 569,125 / 569,125 | 0 / 569,125 |
| DOGE | 4 / 569,126 | 569,126 / 569,126 | 4 / 569,126 |
| AVAX | 569,127 / 569,127 | 569,127 / 569,127 | 626 / 569,127 |

The single canonical SOL-only timestamp was also checked against SQLite. Its OHLC and canonical volume match the database row's OHLC and `volCcy`; the database row has `confirm=0`, matching the current public OKX history-candles response.

### Unit interpretation

The official OKX V5 candlestick schema defines:
- `vol`: contract quantity for derivatives.
- `volCcy`: base-currency quantity for derivatives.
- `volCcyQuote`: quote-currency quantity.

Official documentation: https://app.okx.com/docs-v5/en/ (Market Data → Candlesticks / Historical Candlesticks).

Therefore the canonical Git files' generic `vol` column is, by exact field-value reconciliation, **base-currency volume (`volCcy`)**, not contract count. The VPS export preserves the three fields separately. For future work, do not compare or combine generic `vol` columns without a declared unit mapping. Use explicit names such as `volume_contracts`, `volume_base_ccy`, and `volume_quote_ccy`.

The exact equality identifies the field mapping; it does not establish that raw base-currency volume is directly comparable across different assets. Cross-asset volume comparisons need an explicit normalization or quote-notional policy.

## 4. SOL non-confirmed row

The canonical SOL file contains one timestamp absent from the confirmed-only VPS CSV: 2026-08-28 08:30 UTC (`1787905800000`). It exists in VPS SQLite with `confirm=0`, and the current OKX history-candles endpoint returns the same row with `confirm=0`. Canonical OHLC and canonical volume both match the SQLite row's OHLC and `volCcy`.

This is a source-status difference: the older canonical file retained the row without a confirmation column, while the newer VPS CSV export filters it out. It is not an OHLCV mismatch. Do not relabel it confirmed or silently fill the confirmed-only CSV.

## 5. What this establishes—and what it does not

Established:
1. Exact OHLC agreement on every timestamp common to each canonical/VPS asset pair.
2. Exact mapping of canonical `vol` to VPS `volCcy` on every matched timestamp.
3. Canonical files are contained in the VPS timestamp set for BTC, ETH, DOGE, and AVAX; SOL has one known source-status exception.
4. The VPS snapshot extends both earlier and later than the canonical Git snapshot.
5. The known SOL exception is present in SQLite and currently returned by OKX with `confirm=0`.

Not established:
- Byte identity with the original historical Termux source files, whose contemporaneous hashes were not recorded.
- Full VPS downloader acquisition history or why OKX retains the historical SOL candle with `confirm=0`.
- Funding settlement-price fidelity, fee provenance, or execution-engine acceptance.
- Permission to replace the canonical Git snapshot with the newer VPS snapshot.

Preserve both snapshots separately. Any future canonical refresh must be a new versioned snapshot with a manifest, hashes, row counts, coverage, volume-unit mapping, confirmation policy, and cross-asset timestamp alignment.

## 6. Gate disposition

This closes the current **overlap value-reconciliation** task for the five canonical 1-minute files against the audited VPS snapshot. It resolves the generic-volume-column ambiguity for this dataset pair. It does not close all Gate 0 source provenance, funding, candidate-causality, or engine-acceptance blockers.

Gate 0 remains **CONDITIONAL HOLD**. No candidate generation, Gate 2 execution-resolution comparison, strategy PnL backtest, or Phase 1 handoff is authorized.
