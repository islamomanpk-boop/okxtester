# G0-07 Historical L2 Archive Format Inspection V1 — 2026-11-28

## Prior availability result

The read-only public availability workflow completed SUCCESS:
- Workflow: https://github.com/islamomanpk-boop/okxtester/actions/runs/46170780016
- Commit: c3fbce5f612ebb3c508b59eb2e263028f0528c75
- Artifact: g0-07-historical-orderbook-availability-v1, ID 15273647547
- Artifact ZIP SHA-256: a848b76333d89ca1623805366838add4147de61da17ed1fad1ecea03ee6e4b2a
- Result: 35/35 sampled archive slots returned (five instrument families × seven date/module combinations).

Per-sample archive sizes:
- 2025-10-20 module 4: 1,749.41 MB total across five assets.
- 2025-11-01 module 4: 855.67 MB.
- 2025-11-01 module 5: 284.76 MB.
- 2026-06-01 module 4: 1,056.33 MB.
- 2026-06-01 module 5: 330.20 MB.
- 2026-11-19 module 4: 1,458.57 MB.
- 2026-11-19 module 5: 474.88 MB.

All five families returned archive metadata at every sampled date/module combination. This is strong availability evidence at seven sample points, not proof of every date or complete contents. The file sizes show that a full-year bulk download is not appropriate for the 24 GB VPS; a targeted/event-based acquisition strategy is required.

## One-archive inspection

The follow-up workflow downloads only the BTC-USDT-SWAP module 5 archive for 2025-11-01 (advertised size approximately 78.99 MB), inspects the tar.gz member listing and a short prefix of the first regular member, computes a SHA-256 digest, and deletes the temporary archive. It retains only a compact JSON inspection report. No API credentials are used.

## Files

- Inspector: `src/inspect_okx_historical_l2_archive.py`
- Tests: `src/test_inspect_okx_historical_l2_archive.py`
- Workflow: `.github/workflows/g0-07-historical-l2-archive-inspection.yml`
- Report: `reports/g0_07_historical_l2_archive_format_v1.json` (CI artifact only).

## Acceptance boundary

A successful one-archive inspection will establish only the container/member format and a small sample schema. It will not certify full-day coverage, sequence continuity, complete order-book reconstruction, historical fill prices, queue priority or market impact. Further work must validate timestamp cadence, depth units, bid/ask structure, gaps, duplicate timestamps and the ability to align snapshots to historical stop events.

No existing backtest engine, market data file, or strategy logic is modified.
