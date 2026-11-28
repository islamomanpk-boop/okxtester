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
