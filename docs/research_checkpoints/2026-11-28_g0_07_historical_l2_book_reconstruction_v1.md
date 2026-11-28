# G0-07 Historical L2 Book Reconstruction Sample V1 — 2026-11-28

## Official update semantics

OKX's order-book documentation describes incremental updates as changes to price levels: insert new levels, replace size at existing levels, and remove a level when quantity becomes zero. Derivative order-book quantities are expressed in contracts. The historical archive uses a compact three-field level `[price, size, order_count]`; the live REST/WS documentation examples may include an additional deprecated field.

Official reference: https://www.okx.com/docs-v5/en/#order-book-trading-ws-order-book-channel (book update and sequence semantics).

## Reconstruction experiment

This workflow reconstructs one BTC-USDT-SWAP module-5 archive for 2025-11-01 in memory:
- A `snapshot` replaces both book sides.
- An `update` replaces or inserts a price level; zero size removes the level.
- The book is trimmed to the best 5,000 price levels per side after updates.
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
