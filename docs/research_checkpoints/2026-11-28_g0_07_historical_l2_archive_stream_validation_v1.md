# G0-07 Historical L2 Archive Stream Validation V1 — 2026-11-28

## Availability and archive format evidence

The public availability probe found all 35/35 sampled archive slots for BTC, ETH, SOL, DOGE and AVAX across the selected 2025-10-20, 2025-11-01, 2026-06-01 and 2026-11-19 dates and module 4/5 combinations. Availability manifest artifact: [15273647547](https://github.com/islamomanpk-boop/okxtester/actions/runs/46170780016/artifacts/15273647547).

The representative BTC-USDT-SWAP module 5 archive for 2025-11-01 was downloaded and inspected in GitHub Actions:
- Workflow: https://github.com/islamomanpk-boop/okxtester/actions/runs/46170961132
- Archive: `BTC-USDT-SWAP-L2orderbook-5000lv-2025-11-01.tar.gz`
- Download size: 82,822,265 bytes (advertised 78.99 MB).
- SHA-256: `940c807fec7e39cf10fba718afe36ac2fb2ecfeb887e1645d4b7c07c6cf4e102`.
- Container: gzip-compressed tar archive with one `.data` member.
- Uncompressed member size: 422,406,413 bytes.
- Sample records are JSON Lines with `instId`, `action` (`snapshot` / `update`), millisecond `ts`, and `bids` / `asks` arrays.
- The initial sample shows a snapshot followed by updates at one-second timestamps. Each depth level is represented as price, size and order count.
- The archive was deleted after inspection; only the compact metadata report was retained as a CI artifact (ID 15273418992).

The follow-up full-stream validator parses every JSONL record in this one archive, checks instrument identity, snapshot/update structure, bid/ask level shape and numeric values, timestamp monotonicity/deltas, and sequence fields when present. It does not reconstruct the full book or claim execution/fill fidelity.

## Scope and limitations

This is one instrument and one day only. It establishes that the archive format is machine-readable and contains a timestamped order-book snapshot/update stream; it does not establish full-period or all-asset integrity, complete coverage, sequence-chain correctness across all data, or executable fill prices.

No archive is retained in the repository or VPS. No trading credentials, orders, backtest engines, or strategy logic are used or changed. G0-07 remains OPEN pending full-stream validation, representative cross-asset/date checks, book reconstruction/alignment to stop events, and evidence-based execution-cost modeling.


## Full-stream validation result — 2026-11-28

Workflow [46171069740](https://github.com/islamomanpk-boop/okxtester/actions/runs/46171069740) completed SUCCESS on commit a2e2511d32715ccf240e6d5ec5bf57c15a7d1d39. The complete BTC 2025-11-01 module-5 stream was parsed:
- 86,400 JSONL records: 96 `snapshot` and 86,304 `update` actions.
- The initial snapshot contained 5,000 bid levels and 5,000 ask levels.
- 86,351 of 86,399 adjacent timestamp intervals were exactly 1,000 ms; the remaining 48 intervals differed. There were zero duplicate timestamps and zero backwards timestamps.
- First timestamp: 1761955200007 ms; last timestamp: 1762041599002 ms; elapsed span: 86,398.995 seconds.
- The records contain no `seqId` or `prevSeqId` fields. Timestamp checks therefore cannot prove lossless update delivery or exchange sequence continuity.
- Archive SHA-256 remains `940c807fec7e39cf10fba718afe36ac2fb2ecfeb887e1645d4b7c07c6cf4e102`; the archive was deleted after the run. Compact report artifact ID: 15272739253.

This validates the complete record stream's basic schema and timestamp ordering for one asset/day. It does not reconstruct the evolving order book, prove continuity through every non-1,000-ms interval, or establish historical fills. Next: reconstruct the book from snapshot plus updates, verify reset/recovery behavior, then repeat targeted samples for other assets and dates before designing event-aligned spread/depth measurements.
