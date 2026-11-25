# Phase 3 VPS downloader SQL, export, and update semantics V1

**Recorded:** 2026-11-25  
**Repository:** `islamomanpk-boop/okxtester_private`  
**Supporting workflow commit:** `7cbd0b171affbaa31dd4f437f35ccb114e5597ad`  
**Workflow run:** [45654166874](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45654166874) — completed successfully  
**Artifact:** `15042235920`, SHA-256 `a09bba18e44e5e48c52bde379ba92d39cd0714703ee4d0f7c7646ddda63f3e3a`  
**Inspected VPS source:** `$HOME/okx_market_data_v1/download_okx.py`  
**Source SHA-256:** `b2cd563b373ca613e8e26a6a08e628f76a88ad3f927e10000a084279c4f28a01`

## 1. Inspection method and scope

This is a static Python AST review of the exact VPS downloader source fingerprinted in the prior provenance checkpoint. The workflow did not import or execute the downloader, issue an OKX request, query or modify SQLite, export CSVs, or change VPS files/services. The sanitized AST report preserved SQL structure and placeholders while redacting arbitrary string literals and keeping bound parameter values out of the SQL output.

The source hash exactly matches the earlier downloader fingerprint and semantic review. This is a source-level description, not a runtime/database snapshot or proof that the file has not changed since the recorded inspection time.

## 2. SQLite schema and write policy

The downloader creates a `candles` table with:

- `inst_id TEXT NOT NULL`
- `ts INTEGER NOT NULL`
- `open, high, low, close, vol, vol_ccy, vol_ccy_quote TEXT`
- `confirm INTEGER NOT NULL`
- primary key `(inst_id, ts)`

SQLite is configured with `journal_mode=WAL` and `synchronous=NORMAL`.

The exact write statement is:

```sql
INSERT INTO candles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(inst_id, ts) DO UPDATE SET
  open=excluded.open,
  high=excluded.high,
  low=excluded.low,
  close=excluded.close,
  vol=excluded.vol,
  vol_ccy=excluded.vol_ccy,
  vol_ccy_quote=excluded.vol_ccy_quote,
  confirm=excluded.confirm
```

The downloader therefore **updates an existing instrument/timestamp row on conflict**; it does not preserve every version of that row. This can correctly replace an initially unconfirmed candle with a later confirmed response, but it can also replace historical OHLCV values if the API returns revised values. The SQLite table is a mutable latest-state store, not an immutable acquisition log. A reproducible historical snapshot must be exported separately and identified by file hashes and a timestamped manifest.

## 3. Retrieval and pagination implications

The source constructs instrument IDs as `{asset}-USDT-SWAP` for BTC, ETH, SOL, DOGE, and AVAX. The request uses the OKX history-candles endpoint with `instId`, `bar`, and `limit`; the interval is `1m`. When supplied, the `after` cursor is added as a string parameter.

The downloader first fetches the latest page and saves those records, then uses the earliest stored timestamp (`SELECT MIN(ts)`) as the cursor for backward history retrieval. It moves the cursor to the oldest timestamp returned by each page, rejects a non-advancing cursor, and applies a start boundary named `START_MS`. Each response row must contain exactly nine fields. The source casts row[0] to integer and retains the three volume fields and integer confirmation flag separately.

The request layer has up to eight attempts, a 30-second request timeout, exponential retry delay capped at 30 seconds, and checks the OKX response code before returning response data. These behaviours were established by the static source review and are not a measurement of live API reliability.

## 4. Exact CSV export projection and filter

The export query is:

```sql
SELECT ts, open, high, low, close, vol, vol_ccy, vol_ccy_quote, confirm
FROM candles
WHERE inst_id=? AND confirm=1 AND ts>=?
ORDER BY ts ASC
```

Consequences:

1. Only the selected instrument is exported.
2. Only rows with `confirm=1` are exported.
3. Rows before `START_MS` are excluded.
4. Rows are ordered by ascending timestamp.
5. The export retains all three source volume fields separately and includes the confirmation field.
6. The audit separately counts all database rows for the instrument; that raw count is not the same as the confirmed, start-bounded CSV row count.

The export code casts the timestamp field to integer for its gap checks and checks timestamp differences greater than 60,000 as missing one-minute intervals. It does not convert the timestamp to seconds before writing the CSV row. The source therefore preserves the API timestamp integer in the CSV; its millisecond interpretation is consistent with the `START_MS` naming and 60,000-ms interval logic, but the full external timestamp contract still depends on the OKX API specification and should be recorded alongside the source manifest.

The export audit also checks OHLC ordering/consistency. It does not establish volume units, exact upstream instrument provenance beyond the configured IDs, or immutable history of revisions.

## 5. Research and data-governance implications

- Treat the VPS SQLite database as a mutable operational store, not the canonical frozen research dataset.
- Do not use its present contents as a historical snapshot without exporting them, hashing each file, recording row counts and coverage, and preserving the exact source-code fingerprint.
- Preserve raw API fields `vol`, `vol_ccy`, and `vol_ccy_quote` separately; do not substitute one for another or infer units from renamed CSV columns alone.
- Record the timestamp unit and candle-open semantics explicitly in each future data manifest.
- If a source refresh is required, create a separately versioned snapshot; do not overwrite the canonical Git market files.
- This static review does not prove that current VPS CSV exports are byte-identical to the canonical Git 1M CSVs, that the downloader's current runtime database contains the expected history, or that any historical row is unrevised.

## 6. Gate disposition

This review closes the following **source-code understanding** questions: exact SQLite conflict/update policy; exact confirmed-only CSV projection and lower-bound filter; preservation of the raw timestamp integer in export; and separate retention of all three volume fields.

It does **not** close VPS-to-canonical data lineage, immutable acquisition history, full timestamp/API provenance, volume-unit validation, funding-price fidelity, or real-input execution-engine acceptance. Gate 0 remains **CONDITIONAL HOLD**. No candidate generation, Gate 2 execution-resolution comparison, strategy PnL backtest, or Phase 1 handoff is authorized by this checkpoint.

No downloader execution, API retrieval, SQLite read/write, VPS modification, service change, cleanup, or deletion occurred.
