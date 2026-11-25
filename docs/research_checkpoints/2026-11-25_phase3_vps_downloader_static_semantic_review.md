# Phase 3 Gate 0 — VPS downloader static semantic review

**Date:** 2026-11-25  
**Scope:** Read-only AST inspection of the exact VPS downloader fingerprinted in the preceding checkpoint. No downloader execution, OKX API request, database query/write, VPS file modification, service operation, or cleanup was performed.

## Source identity

The semantic review's computed source SHA-256 exactly matches the prior source fingerprint:

`b2cd563b373ca613e8e26a6a08e628f76a88ad3f927e10000a084279c4f28a01`

- Semantic review workflow: [45652223245](https://github.com/islamomanpk-boop/okxtester_private/actions/runs/45652223245)
- Workflow commit: `ee00bba397779a24c1ea8ae3bdfd5c5b8ceba4d4`
- Sanitized artifact ID: `15040652836`
- Artifact digest: `sha256:f10ff5686dad7d07241bd98cb1ed951b8aa8e2041199d66e9c286d6b5aa4a591`
- The first semantic-review attempt failed because the AST summarizer did not handle nested attribute expressions. The summarizer was corrected; the second run completed its static inspection step successfully and produced the artifact. The failed attempt did not alter the VPS.

## Acquisition and pagination behavior identified

Static AST structure confirms:

1. The request parameter dictionary includes `instId`, `bar`, and `limit`; the bar interval is `1m`.
2. When an `after` cursor is supplied, it is converted to a string and added to the request parameters.
3. The downloader calls the OKX public history-candles endpoint identified in the preceding source fingerprint.
4. The request function allows up to 8 attempts, uses a 30-second request timeout, and calculates retry delay as `min(30, 2 ** attempt)`.
5. It parses JSON, checks the response `code` against success value `0`, raises on API error, and returns the response `data` array.
6. Instrument IDs are constructed as `{asset}-USDT-SWAP` for the five configured assets.
7. The historical download loop begins from the latest stored timestamp when one exists, otherwise starts from the latest endpoint response; it moves the cursor to the oldest timestamp in each page. The source includes a guard against pagination failing to move backward.
8. Candle rows must contain exactly 9 elements. Timestamp at index 0 is converted to integer milliseconds and filtered against `START_MS`.

These findings identify the broad pagination/retry structure. They do not establish all edge cases (e.g. API ordering changes, rate-limit response handling, duplicate/overlap behavior in every scenario, or retry treatment of every exception class).

## Candle-field mapping identified

The AST output explicitly shows the 9-element API row being assembled into a database record in this order:

| OKX response row index | Stored database column | Static interpretation |
|---:|---|---|
| 0 | `ts` | Timestamp, converted to integer |
| 1 | `open` | Open |
| 2 | `high` | High |
| 3 | `low` | Low |
| 4 | `close` | Close |
| 5 | `vol` | OKX `vol` field |
| 6 | `vol_ccy` | OKX `volCcy` field |
| 7 | `vol_ccy_quote` | OKX `volCcyQuote` field |
| 8 | `confirm` | Converted to integer |

The SQLite schema defines these fields as text for OHLC and volume values, integer for timestamp and confirmation, with primary key `(inst_id, ts)`. This confirms that all three distinct OKX volume fields are preserved in the database record; it does **not** establish their unit definitions or justify treating them as interchangeable.

## Database and export behavior: evidence limits

- The source creates the `candles` table if absent and enables SQLite WAL mode and `synchronous=NORMAL`.
- The `save_records` function uses `executemany` followed by `commit`.
- The `download_asset` routine checks the existing latest timestamp, tracks SQLite `total_changes`, and advances the historical cursor by page.
- The export/audit function writes CSV, counts rows, checks timestamp gaps and invalid OHLC relationships, and reports a “Confirmed CSV rows” metric.
- The exact SQL statement passed to `executemany` and the precise export SELECT/filter expressions were not recoverable from the sanitized summary because SQL placeholders were redacted. Therefore the conflict policy (ignore vs update), confirmation filter predicate, and exact CSV column/header list are **not yet independently verified from this inspection**.
- The static summary shows CSV numeric conversion applied to the selected row's values after the timestamp. The precise SQL projection must be reviewed before asserting which database fields are included in the CSV.

## Timestamp and volume conclusions

- Timestamp values are cast to integers from API row index 0 and compared against a millisecond-named start boundary. No timestamp unit conversion was visible in the reviewed assignment/field mapping summary. This supports a millisecond representation hypothesis, but a complete expression-level review of all timestamp transformations is still required before treating it as proven end-to-end.
- The three volume columns are distinctly retained as `vol`, `vol_ccy`, and `vol_ccy_quote`. Their exact OKX unit semantics should be checked against the relevant OKX API documentation and the historical export pipeline before selecting a volume field for any future feature.
- The downloader's source hash proves the inspected file identity at inspection time only. It does not prove that this exact source version produced every historical database row or tracked CSV.

## Gate disposition

- VPS downloader file fingerprint: **PASS for the inspected snapshot**.
- Endpoint, request parameter names, retry envelope, and pagination cursor structure: **PARTIALLY IDENTIFIED**.
- Nine-field API row to SQLite record mapping: **IDENTIFIED**.
- Timestamp end-to-end unit/label semantics: **PARTIALLY IDENTIFIED; NOT YET CLOSED**.
- Volume field preservation: **IDENTIFIED**; volume units and downstream choice **OPEN**.
- SQLite conflict/update policy and precise confirmed-only CSV filter: **OPEN**.
- Historical acquisition-version lineage and canonical Git snapshot byte identity: **UNVERIFIED**.
- Gate 0: **CONDITIONAL HOLD remains**.
- G0-04/G0-05, candidate generation, Gate 2, and all PnL strategy backtests: **NOT AUTHORIZED**.

## Safety record

Both semantic inspection attempts used Python AST parsing only. The successful run did not import or execute the downloader, issue requests to OKX, read the SQLite database, write to the VPS project, change services, or delete data. The artifact contains sanitized structural expressions rather than source lines or credential values.

## Next safe research step

Complete the remaining static SQL review with a purpose-built redactor that preserves SQL structure and placeholder positions while removing all values. Specifically establish the `executemany` conflict clause, the export SELECT projection and confirmation predicate, and the exact timestamp serialization expression. Then compare the retained volume fields with the applicable OKX API field definitions. No runtime execution or database mutation is needed for that work.


## Follow-up — SQL review and volume units resolved (2026-11-25)

This follow-up supersedes the earlier open items above concerning SQL conflict semantics, CSV export selection, and volume-unit definitions.

The subsequent SQL review established that duplicate `(inst_id, ts)` rows are updated with `ON CONFLICT ... DO UPDATE`, and that CSV export selects `ts, open, high, low, close, vol, vol_ccy, vol_ccy_quote, confirm` with `confirm=1` and `ts>=START_MS`, ordered ascending. See [the downloader SQL/export checkpoint](2026-11-25_phase3_vps_downloader_sql_export_update_semantics_v1.md).

The current OKX V5 documentation defines derivative `vol` as contract count, `volCcy` as base-currency quantity, and `volCcyQuote` as quote-currency quantity. Exact Decimal reconciliation found that canonical Git `vol` equals VPS `volCcy` on every overlapping timestamp across all five instruments. The canonical field is therefore base-currency volume, not contracts. The execution-data audit now records explicit unit names and cross-asset normalization requirements. Full comparison: [canonical/VPS OHLCV reconciliation](2026-11-25_phase3_vps_canonical_ohlcv_reconciliation_v1.md).

Remaining source-lineage limits are unchanged: the original historical Termux inputs lack contemporaneous hashes; the VPS database is mutable; and the historical SOL 2026-08-28 08:30 UTC candle remains `confirm=0` in both current API response and SQLite. Gate 0 remains CONDITIONAL HOLD.
