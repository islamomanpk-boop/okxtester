# G0-07 Historical L2 Book Reconstruction Sample V1 — 2026-11-28

## Official update semantics

OKX's order-book documentation describes incremental updates as changes to price levels: insert new levels, replace size at existing levels, and remove a level when quantity becomes zero. Derivative order-book quantities are expressed in contracts. The historical archive uses a compact three-field level `[price, size, order_count]`; the live REST/WS documentation examples may include an additional deprecated field.

Official reference: https://www.okx.com/docs-v5/en/#order-book-trading-ws-order-book-channel (book update and sequence semantics).

## Reconstruction experiment

This workflow reconstructs one BTC-USDT-SWAP module-5 archive for 2025-11-01 in memory:
- A `snapshot` replaces both book sides.
- An `update` replaces or inserts a price level; zero size removes the level.
- Snapshot records supply up to 5,000 levels per side; incremental updates are applied by price without artificially truncating the reconstructed maps.
- It records crossed-book observations, spread basis points and top-10 visible depth in contracts.
- The compressed archive is deleted after processing; only a compact statistics JSON report is retained.

The archive does not expose `seqId` or `prevSeqId`; therefore, the reconstruction is an explicitly provisional interpretation of the historical archive's snapshot/update stream. Timestamp ordering and periodic snapshots are not a substitute for exchange sequence-ID continuity.

## Files

- Reconstruction: `src/reconstruct_okx_historical_l2_book.py`
- Tests: `src/test_reconstruct_okx_historical_l2_book.py`
- Workflow: `.github/workflows/g0-07-historical-l2-book-reconstruction.yml`
- Report: `reports/g0_07_historical_l2_book_reconstruction_v1.json` (CI artifact only).

This is one instrument/day and is not a fill simulator. No account credentials, order placement, or strategy PnL are involved. G0-07 remains OPEN pending the observed reconstruction result, cross-asset/date validation, event alignment, and explicit execution-cost limitations.


## Single-day BTC reconstruction results and cross-asset extension — 2026-11-28

The BTC 2025-11-01 reconstruction workflow completed SUCCESS:
- 86,400 records; 96 snapshots and 86,304 updates.
- Snapshot intervals were overwhelmingly 900,000 ms (15 minutes), with small millisecond variation.
- No duplicate or backwards timestamps.
- 86,351/86,399 adjacent intervals were exactly 1,000 ms; 48 intervals differed.
- No sequence identifiers were present.
- At 10-record metric sampling (about 10 seconds): 8,641 metric points, zero crossed-book observations and zero empty-book observations.
- Spread basis points: min 0.00905074, median 0.00908663, p95 0.00912432, max 0.23629382.
- Top-10 depth in contracts: bid median 452.10 / p95 1,547.03; ask median 483.43 / p95 1,671.72.
- A second run at 60-record (about one-minute) sampling gave median spread 0.00908654 and p95 0.00912471, with zero crossed-book observations. Top-10 depth medians were 434.44 bid contracts and 466.44 ask contracts.
- Both runs downloaded and deleted the same 82,822,265-byte archive (SHA-256 `940c807fec7e39cf10fba718afe36ac2fb2ecfeb887e1645d4b7c07c6cf4e102`). Reports are CI artifacts 15272944656 and 15273664101.

The spread statistics are stable between 10-second and one-minute metric sampling for this one day. The top-10 depth medians vary modestly with sampling interval, as expected for a time-varying book. These are observed visible-book statistics, not fills or calibrated slippage assumptions.

The next workflow extends the same snapshot/update reconstruction to all five project instruments on 2025-11-01. It downloads each archive sequentially in GitHub Actions, reconstructs in memory, and deletes each temporary archive. It does not store raw order-book archives in GitHub or on the VPS.


## Verified BTC reconstruction result — 2026-11-28

Workflow [46171636969](https://github.com/islamomanpk-boop/okxtester/actions/runs/46171636969) completed SUCCESS on commit 62fb7f9d3d451d749c4b95b7fada12e8ed6420be. The full BTC 2025-11-01 archive reconstructed in memory:
- 86,400 records: 96 snapshots and 86,304 updates.
- 96 snapshots were spaced at approximately 900,000 ms (15 minutes); 73 of 95 intervals were exactly 900,000 ms.
- 86,351/86,399 record-to-record timestamp intervals were exactly 1,000 ms; 48 differed. No duplicate or backwards timestamps.
- No crossed or empty books at 8,641 sampled points (one sample every 10 records).
- Spread (bps): min 0.00905074, p50 0.00908663, p95 0.00912432, max 0.23629382.
- Top-10 visible depth in contracts: bid p50 452.10 / p95 1,547.03; ask p50 483.43 / p95 1,671.72.
- No sequence identifiers were present; continuity cannot be certified by sequence ID.

A second successful run [46171705890](https://github.com/islamomanpk-boop/okxtester/actions/runs/46171705890) used one-minute metric sampling and did not artificially truncate depth maps. Its spread p50/p95 were 0.00908654/0.00912471 bps; top-10 depth p50 was 434.44 bid contracts and 466.44 ask contracts. Both runs reported zero crossed-book observations at sampled points. This is a useful sampling-policy robustness check for one BTC day, not a validation of all dates/assets.

The five-asset extension for 2025-11-01 is running separately. No raw archive is committed or retained on the VPS. G0-07 remains OPEN pending cross-asset/date checks, event alignment and conservative execution-cost modelling.


## Five-asset same-day reconstruction result — 2026-11-28

Workflow [46172153289](https://github.com/islamomanpk-boop/okxtester/actions/runs/46172153289) completed SUCCESS on commit `f55b18bba393d8ba0de06da15886140b3f61d0ed`. Compilation and all three reconstruction unit tests passed. The corrected compact JSON report was parsed back successfully by the workflow before upload; artifact ID `15274400627` (ZIP SHA-256 `67beabeee39f8e37b5ba4b23e4c8c886e9b33e3f801686fc516dd58168d5d1f0`). Raw archives were processed in memory on the GitHub-hosted runner and not retained.

All five assets had 96 snapshots. BTC, ETH, SOL and DOGE each had 86,400 records (96 snapshots and 86,304 updates), with every snapshot containing exactly 5,000 bid and 5,000 ask levels. AVAX had 86,397 records (96 snapshots and 86,301 updates); its snapshot bid levels ranged from 2,155 to 2,558 and ask levels from 4,391 to 4,722. The AVAX archive contained three 2,000 ms adjacent timestamp intervals. There were no duplicate or backwards timestamps for any asset. Because no seqId/prevSeqId fields were present, the three longer AVAX intervals cannot be classified conclusively as missing updates versus source cadence irregularity.

One-minute metric sampling produced these spread summaries (bps):

| Asset | p50 | p95 |
|---|---:|---:|
| BTC | 0.00908654 | 0.00912471 |
| ETH | 0.02583682 | 0.02602327 |
| SOL | 0.53753326 | 0.54049672 |
| DOGE | 0.53526027 | 0.53843048 |
| AVAX | 0.53860448 | 0.54985841 |

No crossed or empty books were observed at sampled metric points. Top-10 depth is reported in contracts and is not directly comparable across assets without historical effective contract-value metadata. The AVAX archive itself provides materially fewer bid levels than the other four assets; this is an archive-depth limitation, not evidence of a reconstruction defect.

**Limits and disposition:** one date (2025-11-01) only; no sequence-ID continuity proof; AVAX has three 2,000 ms timestamp intervals and fewer snapshot levels; sampled visible depth does not establish fills, queue position, hidden liquidity, latency or market impact. These spread summaries are not calibrated slippage assumptions. G0-07 remains OPEN; Gate 0 remains CONDITIONAL HOLD. No strategy PnL, execution simulation, orders or fills were run.


## Module-4 BTC archive inspection — 2025-10-20

Workflow [46173396236](https://github.com/islamomanpk-boop/okxtester/actions/runs/46173396236) completed SUCCESS on commit `170ed819b8ddbcf0f1c72b4d7154309323d59116`. Four focused unit tests passed. The module-4 archive was streamed and validated on a GitHub-hosted runner; only a compact JSON report was retained (artifact ID `15274204016`, ZIP SHA-256 `154bcaa0bb2e8e0c604a0a15dd87b7ee835a9ce4ea7406583f9de9370871612d`). Downloaded archive bytes: 491,283,675; uncompressed JSONL member: 3,320,895,476 bytes. Archive SHA-256: `8f730ffe83ec71eb819a29881259a36b68c701e4a65b1cc9287e914ca50ee6f6`. Raw archive was not retained.

The BTC-USDT-SWAP 400-level stream contained 6,876,834 records over 86,399.975 seconds: 1,440 snapshots and 6,875,394 updates. Every snapshot contained exactly 400 bid and 400 ask levels. There were no duplicate or backwards timestamps. The adjacent timestamp distribution was predominantly 10 ms (5,978,609 intervals), followed by 20 ms (511,928), 30 ms (188,716), and 40 ms (88,902); other intervals also occurred. No seqId/prevSeqId fields were present. Thus this is a high-frequency archive stream, but timestamps alone do not prove lossless continuity.

This was a format/stream integrity inspection, not a full evolving-book reconstruction or spread/depth/slippage analysis. The 400-level archive has a materially different cadence and record volume from the module-5 5,000-level daily archive. Before comparing modules, implement and test reconstruction semantics against the module-4 format and establish how snapshots and incremental updates are represented. One BTC date only; no cross-asset/date generalization.

**Disposition:** module-4 availability and stream structure validated for this sample date. Reconstruction, event alignment and execution-cost calibration remain open. G0-07 remains OPEN; Gate 0 remains CONDITIONAL HOLD.


## Module-4 BTC full book reconstruction result — 2025-10-20

Workflow [46173859847](https://github.com/islamomanpk-boop/okxtester/actions/runs/46173859847) completed SUCCESS on commit `0e81fd1bed535af58a2152995774e47ad2f9ff1e`. Compilation and all five focused reconstruction tests passed; the full 400-level BTC module-4 archive was reconstructed in memory and the compact JSON report uploaded as artifact `15274908032` (ZIP SHA-256 `b58a53bccf1611dd10b01f275e50da232e24070446619d0dc9c364ecf10b3b75`). The report was downloaded and parsed successfully. Raw archive was not retained.

The BTC-USDT-SWAP 2025-10-20 archive contained 6,876,834 records over 86,399.975 seconds: 1,440 snapshots and 6,875,394 updates. All snapshots contained exactly 400 bid and 400 ask levels. There were no duplicate or non-monotonic timestamps. The stream had no `seqId`/`prevSeqId` fields. Adjacent timestamp deltas were predominantly 10 ms (5,978,609), 20 ms (511,928), 30 ms (188,716), and 40 ms (88,902). The reconstruction applied snapshot replacement of both sides, price-level replacement/insertion on updates, and zero-size deletion.

Metrics sampled every 10,000 records yielded 689 observations: zero crossed books and zero empty books. Spread (bps): min 0.00895848, p50 0.00902937, p95 0.00926145, max 6.09560315. Top-10 visible depth in contracts: bid p50 538.82 / p95 1,784.45; ask p50 493.27 / p95 1,636.69. The maximum spread is retained as an observed sampled outlier; do not substitute the median/p95 summaries for event-aligned execution-cost estimates.

**Limits and disposition:** one BTC instrument/day only; sampling does not capture every transient state; absent sequence IDs mean timestamp ordering cannot certify lossless update continuity; visible depth does not establish queue position, hidden liquidity, latency, market impact or fills; historical effective contract-value metadata remains unresolved, so contract depth is not normalized into notional. This validates successful reconstruction mechanics for this sample, not full-period or cross-asset market quality. G0-07 remains OPEN; Gate 0 remains CONDITIONAL HOLD. No strategy PnL, execution simulation, orders or fills were run.
