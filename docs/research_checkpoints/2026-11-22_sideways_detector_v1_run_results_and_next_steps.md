# Sideways Detector V1 Run Results and Continuation Checkpoint

Date: 2026-11-22
Branch: `price-action-v1`
Repository: `islamomanpk-boop/okxtester`

## Purpose

Record the first successful local execution of the reconstructed sideways detector V1, preserve its observed outputs, and define the safe continuation point. This checkpoint records the summarized console results supplied during the research session; it does not claim that the local CSV report files have been uploaded to GitHub.

## Execution and tests

- Detector: `research/sideways_detector_v1.py`
- Tests: `tests/test_sideways_detector_v1.py`
- Test discovery fix: `tests/__init__.py`
- Unit tests: **8/8 passed**.
- Source 4H candles per asset: **2,370**.
- Rolling snapshots per asset: **2,359**.
- Output directory on the user's Termux environment: `reports/sideways_detector_v1/`
- Summary CSV: `reports/sideways_detector_v1/detector_summary_v1.csv`
- Per-asset snapshot CSVs were also generated.
- No source market data was modified.

## Observed run results

| Asset | P25 width % | P40 width % | Strict width pass | Broad width pass | ER pass | Overlap pass | Final strict | Final broad |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 3.19048229 | 3.87218109 | 592 | 947 | 1229 | 0 | 0 | 0 |
| ETH | 4.15974679 | 5.33563939 | 590 | 945 | 1236 | 2 | 2 | 2 |
| SOL | 4.94208992 | 5.93314927 | 590 | 945 | 1293 | 0 | 0 | 0 |
| DOGE | 5.03566026 | 6.07382367 | 593 | 945 | 1302 | 0 | 0 | 0 |
| AVAX | 5.54782779 | 6.68503993 | 590 | 946 | 1317 | 0 | 0 | 0 |

## Interpretation and hold point

The run and unit tests establish that the reconstructed implementation executes and passes its own tests. They do **not** establish that it reproduces the formulas used in the earlier empirical sideways-market research.

A material formula discrepancy was identified between the reconstructed detector and earlier research documents:

1. Adjacent-candle range overlap: reconstructed V1 uses intersection divided by union (IoU); earlier research appears to use intersection divided by the smaller candle range.
2. Channel width: reconstructed V1 uses `(upper - lower) / midpoint * 100`; earlier research uses `(upper / lower - 1) * 100`.
3. Directional efficiency: reconstructed V1 uses 12 closes and 11 close-to-close changes; earlier methodology appears to define 12 close-to-close changes, which requires 13 closes.
4. Snapshot indexing/counts may therefore differ and must be reconciled against the original scripts/reports.

These differences can materially change the overlap and final sideways classifications. The near-zero final classifications in this run are therefore a diagnostic result, not evidence that the market had no sideways periods and not a reason to discard the earlier research.

## Next steps

1. Retrieve and inspect the complete original methodology, feature-distribution, joint-frequency, and formula-recovery documents from this repository.
2. Establish the exact historical formulas, window indexing, quantile method, edge-case handling, and expected snapshot counts from evidence. Do not infer missing details.
3. Implement the historical/original detector as a separate version with independent unit tests. Do not overwrite `research/sideways_detector_v1.py` or its outputs.
4. Compare original and reconstructed detectors asset by asset, including thresholds, feature distributions, pass counts, final classifications, and snapshot-level agreement.
5. Document and explain all differences before deciding which detector should drive the 15M repeated-boundary-test reconstruction.
6. Only after this reconciliation, resume event/timing/outcome research. Preserve the existing provisional results as provisional until their formulas and event construction are independently audited.

## Research safeguards

- Keep the original and reconstructed detector versions separate.
- Do not modify source candle data.
- Do not treat detector unit-test success as validation of historical methodology.
- Do not interpret post-rejection MFE/MAE summaries as strategy profitability or verified fills.
- Keep the full-sample P25/P40 thresholds explicitly labeled retrospective/exploratory unless a causal threshold design is separately established.
