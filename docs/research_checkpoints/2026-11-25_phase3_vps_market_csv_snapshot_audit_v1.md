# Phase 3 VPS market CSV snapshot and SQLite reconciliation V1

**Recorded:** 2026-11-25  
**Supporting repository:** `islamomanpk-boop/okxtester_private@main`  
**Workflow source commit:** `01110f9a8e9e5e61d0db4271a3220a6aa2fa8250`  
**Workflow run:** [45655914596](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45655914596) — completed successfully  
**Metadata-only artifact:** `15042212515`, SHA-256 `3fe4e98476f906435ef3a6e383a0fdea5389d1a29222cdfdd9102d9c578bfd45`  
**Read-only sources:** `$HOME/okx_market_data_v1/csv/*.csv` and `$HOME/okx_market_data_v1/raw/okx_swap_1m.sqlite3`

## 1. Scope and safety

The audit streamed the five exported CSV files to calculate SHA-256, file size, header, row count, timestamp bounds, continuity, OHLC and volume validity, and confirmation status. It then opened the SQLite database in read-only URI mode and queried instrument row counts plus non-confirmed rows. A targeted lookup checked the SOL timestamp responsible for the internal CSV gap.

No source CSV or SQLite row was changed. The downloader was not executed, no API request was made, no files were deleted or overwritten, and no VPS service was changed. Only a small metadata JSON manifest was uploaded as a workflow artifact; raw market data was not uploaded.

## 2. Current VPS CSV snapshot

All five files were found under the downloader's configured CSV directory. Every file had the exact nine-column header:

```text
ts,open,high,low,close,vol,volCcy,volCcyQuote,confirm
```

All five began at the downloader's configured boundary, 2025-10-20 00:00:00 UTC. All exported rows had `confirm=1`. There were no malformed rows, invalid timestamps, duplicate timestamps, out-of-order timestamps, invalid OHLC rows, or invalid volume fields. The only continuity issue was one SOL interval.

| Asset | Rows exported | Bytes | Last exported candle (UTC) | SHA-256 |
|---|---:|---:|---|---|
| BTC | 578,022 | 44,562,372 | 2026-11-25 09:41 | `749b80d0ff37203d4408c914542a7e6495c8077f25f4a5e69d40b035a744e0d9` |
| ETH | 578,051 | 45,380,792 | 2026-11-25 10:10 | `5df4d33682a95bf08af81994d9d05eebb0de49032048e708dbe3f8247bc7aaac` |
| SOL | 578,080 | 40,373,398 | 2026-11-25 10:40 | `307ea6fe4c9ce978b397e7ad0b4e0438da436cc498f23aeda859e5b955fb012e` |
| DOGE | 578,111 | 43,418,273 | 2026-11-25 11:10 | `68296bf9f7bf55d2360ba71d96207f6af7429c9c15c4a9e796e8f5c9ac665f50` |
| AVAX | 578,141 | 37,500,264 | 2026-11-25 11:40 | `215424b685594e6e3016e5351375b3611334daa3aa8f1e9a46a1a130f8fb91d2` |

The five exports share the same start but have different final confirmed timestamps, spanning 09:41–11:40 UTC. This is a staggered per-asset snapshot, not yet a fully reconciled common cross-asset dataset. The common time range cannot be treated as gap-free until the explicit cross-asset timestamp-set comparison is completed.

## 3. SQLite-to-CSV row reconciliation

The read-only database query returned 2,890,411 total rows. For every instrument, the CSV row count exactly matched the database count where `confirm=1`.

| Instrument | SQLite rows | Confirmed rows | Non-confirmed rows | CSV rows | CSV = confirmed count |
|---|---:|---:|---:|---:|---|
| BTC-USDT-SWAP | 578,023 | 578,022 | 1 | 578,022 | Yes |
| ETH-USDT-SWAP | 578,052 | 578,051 | 1 | 578,051 | Yes |
| SOL-USDT-SWAP | 578,082 | 578,080 | 2 | 578,080 | Yes |
| DOGE-USDT-SWAP | 578,112 | 578,111 | 1 | 578,111 | Yes |
| AVAX-USDT-SWAP | 578,142 | 578,141 | 1 | 578,141 | Yes |
| **Total** | **2,890,411** | **2,890,405** | **6** | **2,890,405** | **Yes** |

The six database rows with `confirm=0` were:

| Instrument | Timestamp (UTC) | Interpretation |
|---|---|---|
| BTC-USDT-SWAP | 2026-11-25 09:42 | Latest database row; one minute after CSV end |
| ETH-USDT-SWAP | 2026-11-25 10:11 | Latest database row; one minute after CSV end |
| SOL-USDT-SWAP | 2026-08-28 08:30 | Historical internal row; not a latest-candle boundary |
| SOL-USDT-SWAP | 2026-11-25 10:41 | Latest database row; one minute after CSV end |
| DOGE-USDT-SWAP | 2026-11-25 11:11 | Latest database row; one minute after CSV end |
| AVAX-USDT-SWAP | 2026-11-25 11:41 | Latest database row; one minute after CSV end |

The five latest non-confirmed rows are consistent with the export policy excluding the current/incomplete final minute for each asset. The sixth row is different: SOL's 2026-08-28 08:30 UTC record is an old, non-confirmed row inside the historical range.

## 4. SOL internal gap disposition

The confirmed-only SOL CSV jumps from 2026-08-28 08:29 UTC to 08:31 UTC. The missing timestamp is exactly **2026-08-28 08:30:00 UTC** (`1787905800000` ms).

A read-only SQLite lookup found the SOL row at that exact timestamp with `confirm=0`. Therefore:

- The candle row is **present in SQLite**.
- It is **excluded from the CSV** by the documented `confirm=1` export predicate.
- The one-minute CSV gap is not evidence that the OHLCV row is absent from the database.
- Its historical `confirm=0` status is anomalous enough to investigate; it must not be silently relabelled confirmed, filled, or imputed.

The source uses an upsert that can update a row if that timestamp is fetched again. However, this audit does not establish why this old row remains unconfirmed or whether the current OKX history endpoint now returns a corrected confirmation flag. That is the next narrow read-only check.

## 5. Downloader completion context

The earlier VPS monitor workflow [45647566750](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45647566750) completed successfully at 2026-11-25 15:39 UTC. Its log reported:
- 5/5 assets had a finished marker.
- Downloader process was not running.
- Runner service was active.
- The latest download-log tail showed AVAX at 578,141 confirmed CSV rows, first timestamp 2025-10-20 00:00 UTC, last timestamp 2026-11-25 11:40 UTC, zero gaps and zero invalid OHLC rows.

This supports treating the inspected CSVs as a completed download snapshot, not a live stream. The per-asset end times differ because each instrument's export ended at a different timestamp; the monitor's last-asset tail alone did not reveal the historical SOL confirmation anomaly.

## 6. Relationship to canonical Git market data

The VPS exports are a distinct current snapshot:
- They contain nine columns, including `volCcy`, `volCcyQuote`, and `confirm`.
- They contain approximately 578k confirmed rows per asset and extend through 2026-11-25.
- The canonical Git market files are an earlier, separately hashed research snapshot with a narrower six-column market-data contract and approximately 569k rows in the accepted Module B run metadata.

Do not compare the file hashes as if the schemas and snapshot windows were identical. Do not overwrite the canonical Git data. If the VPS snapshot is to be used in later research, preserve it as a separately versioned source with its own manifest and complete cross-asset alignment review.

## 7. Gate disposition and next checks

This audit establishes the current VPS CSV file identities, exact headers, coverage bounds, per-file continuity, and exact reconciliation of CSV row counts to SQLite's confirmed-row counts. It also isolates one historical unconfirmed SOL row.

Still open:
1. Query the OKX historical-candle endpoint for SOL 2026-08-28 08:30 UTC and compare the returned confirmation flag and OHLCV with the read-only SQLite row.
2. Decide how any stale historical `confirm=0` row should be handled. Do not alter the VPS database or CSV until an explicit, versioned correction policy is approved.
3. Run the explicit five-asset timestamp-set alignment audit on this VPS snapshot, including the SOL internal timestamp and the differing asset end times.
4. Compare the canonical and VPS datasets at the OHLCV-field level only after aligning schema, source window, and instrument identity.

Gate 0 remains **CONDITIONAL HOLD**. This snapshot audit does not establish source acquisition lineage, exact volume-unit suitability, funding mark-price fidelity, or execution-engine readiness. No candidate generation, Gate 2 execution comparison, strategy PnL backtest, or Phase 1 handoff is authorized.
