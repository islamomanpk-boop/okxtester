# Research Track Review — 2026-11-23

**Repository:** islamomanpk-boop/okxtester  
**Branch:** `price-action-v1`  
**Reviewed branch head before this checkpoint:** `d62602f7830db95c2b61b6f15925c2f89ebbf0dc`  
**Review status:** On track for the historical sideways-boundary research objective; downstream event reconstruction remains pending.

## 1. GitHub repository verification

The active branch was fetched directly from GitHub. The branch head was `d62602f7830db95c2b61b6f15925c2f89ebbf0dc`, which is the commit recording the original five-asset 1M integrity/alignment audit.

The repository contains and preserves:
- Historical detector formula-level implementation: `research/sideways_detector_original_v1.py`.
- Historical detector tests: `tests/test_sideways_detector_original_v1.py`.
- Historical detector specification, build checkpoint, reproduction results, and version-usage checkpoint.
- Earlier repeated-boundary protocol, timing-validation, preliminary audit, visit-audit hold, and provisional outcome audit.
- Original 1M rejection follow-up report.
- The 2026-11-22 1M-to-15M/4H aggregation audit.

No dedicated downstream historical-detector boundary/rejection event-builder script was found in the current repository tree. The only files in `research/` are the two sideways detector implementations. The earlier event/outcome outputs must therefore not be assumed to have a recoverable, verified source implementation.

## 2. Current 1M source data audit — confirmed against prior checkpoint

The current Termux audit of `~/okx_scalping_data/{ASSET}_USDT_USDT_1m.csv` confirms:

- BTC: 569,125 rows, timestamps 1760950200000 through 1795097640000.
- ETH: 569,125 rows, timestamps 1760950200000 through 1795097640000.
- SOL: 569,126 rows, timestamps 1760950200000 through 1795097700000.
- DOGE: 569,126 rows, timestamps 1760950200000 through 1795097700000.
- AVAX: 569,127 rows, timestamps 1760950200000 through 1795097760000.

All five files have zero duplicate timestamps, zero missing internal 1M intervals, zero unexpected intervals, and zero invalid OHLCV rows under the performed checks. All share the same start timestamp. The union has 569,127 timestamps and the five-way intersection has 569,125; the two unmatched timestamps are at the tail. Combined five-asset work must use exact timestamp intersection, never row-number alignment or fabricated candles.

These row counts and endpoints agree with the 2026-11-22 source-data integrity checkpoint, which identifies the same five 1M source paths.

## 3. Important existing aggregation work — do not repeat blindly

GitHub already contains `docs/research_checkpoints/2026-11-22_1m_to_15m_4h_aggregation_audit.md`.

That checkpoint documents an independent 1M-to-15M and 1M-to-4H reconstruction using:
- epoch-origin buckets;
- left-labeled and left-closed intervals;
- open=first, high=max, low=min, close=last, volume=sum;
- retention of only complete buckets with exactly 15 or 240 constituent 1M candles.

Recorded results:
- All five assets passed both timeframes (10/10 asset/timeframe comparisons).
- Each asset: 37,941 complete 15M candles and 2,370 complete 4H candles.
- Zero missing/extra timestamps and zero OHLCV field mismatches against the supplied higher-timeframe files.

The companion source-data checkpoint explicitly identifies the 1M files under `~/okx_scalping_data/` and 15M/4H files under `~/okx_adaptive_bot/data/`. This is the same path arrangement used by the historical detector's default 4H input directory. The current 1M row counts and endpoints match the earlier source-data checkpoint.

**Decision:** Treat the 1M-to-15M/4H aggregation audit as completed evidence for those identified files and conventions. Do not rerun the full aggregation audit without a specific discrepancy. A small targeted read-only verification may still be appropriate if file identity or modification history is uncertain.

## 4. Historical detector status — accepted reference

Use `research/sideways_detector_original_v1.py` for reproducing the documented historical 48H sideways detector. It is a formula-level reconstruction, not recovery of the original missing Python source.

Recorded validation:
- 16/16 tests passed.
- 2,370 4H inputs produce 2,358 feature rows per asset.
- P25/P40 width thresholds match the historical references to three decimals for all five assets.
- Strict and broad qualifying counts match all five historical reference counts exactly.

Important limits:
- The detector uses full-sample width quantiles, which are retrospective/exploratory and not live-safe.
- `research/sideways_detector_v1.py` is superseded for historical reproduction and must not be substituted.
- Historical detector labels become available only after the corresponding 4H candle has closed; downstream 15M logic must preserve this causal availability time.

## 5. Are we on track?

**Yes, with a clear remaining gate.** The sequence is now:

1. Preserve the original 1M files and use exact five-asset timestamp intersection for combined analysis.
2. Reuse the already-audited 1M-to-15M/4H aggregation convention and source files; do not regenerate or overwrite the supplied data.
3. Use the historical detector implementation as the sole reference for the historical 48H study.
4. Reconstruct the timestamped detector snapshots/labels and 15M boundary-test state machine from scratch or independently verify any candidate implementation.
5. Enforce exact 15M continuity, causal 4H availability, frozen boundary definitions, and the strict non-touch separation rule in the repeated-test protocol.
6. Generate first-strong-rejection events and reconcile event-level counts/timestamps before computing any forward outcomes.
7. Only then rebuild 1M follow-up outcomes with explicit formulas, exact 15M-to-1M mapping, complete-window rules, OHLC ambiguity handling, and explicit denominators.
8. Keep matched controls and any strategy/backtest work on hold until the event population and outcome formulas pass audit.

## 6. Do not reuse as accepted evidence

The following remain historical/provisional and must not be silently treated as verified outputs of the historical detector:
- Earlier 2,095 repeated-test/rejection cohorts and provisional post-rejection outcomes.
- Preliminary visit counts and unreconciled strong-rejection counts.
- Any event population generated from the superseded detector.
- The first matched-control run, which remains on audit hold.

Rebuild/reconcile these against the historical detector and the accepted strict timing protocol. Preserve earlier reports and CSVs unchanged.

## 7. Remaining open issues

- Original exchange/API provenance and exact instrument identity for the five 1M files remain unverified.
- Volume unit/meaning remains unverified.
- Funding source and coverage remain unresolved.
- The historical detector's original source code and some undocumented edge conventions were not recovered.
- Reconstructed event/outcome code does not yet exist as an audited implementation in the current repository tree.

No profitability, fill-quality, or live-readiness conclusion follows from the completed data and detector audits. No strategy backtest is authorized by this checkpoint.

## 8. Next immediate action

Perform a read-only inventory of the existing local 15M and 4H input files and the detector output files, confirming their paths, row counts, timestamps, and whether the historical detector outputs already exist locally. Do not rerun the detector or write/overwrite files until this inventory is reviewed.
