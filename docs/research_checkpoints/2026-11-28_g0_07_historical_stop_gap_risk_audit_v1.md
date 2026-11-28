# G0-07 Historical Stop-Gap Risk Audit V1 — 2026-11-28

## Disposition

The historical candle-open gap audit and its synthetic unit tests completed successfully. This is **preliminary evidence only** because the upstream OHLCV source and candle construction process have not been verified. G0-07 remains **OPEN**; Gate 0 remains **CONDITIONAL HOLD**.

## Reproducible CI evidence

- Code/audit commit: `94654d356ca67c7e80d56511b1fc9c17757e0fde`.
- Follow-up long/short stop-gap test commit: `cfa422c069c21589d4ec7df7c207386dd781594f`.
- Successful workflow: [46157300415](https://github.com/islamomanpk-boop/okxtester/actions/runs/46157300415).
- Workflow job: [141016674599](https://github.com/islamomanpk-boop/okxtester/actions/runs/46157300415/job/141016674599).
- Stop-gap audit artifact: `g0-07-stop-gap-risk-audit-v1`, ID `15268555549`.
- Artifact ZIP SHA-256: `e9b622a3b4d7aafdc5edb8aa8fc059640e86a778dc2f68b60293db602f2e8dbf`.
- JSON report SHA-256: `5262b452e72c9cd1765c9b8576a5fcfaa11bb22b8d81058f46e7d75e0252800c`.

The workflow passed compilation, all 12 stop-gap audit unit tests, the five-asset historical audit, artifact upload, funding helper/contract tests, standalone execution-engine tests (17), portfolio backtester tests (20), portfolio integration tests and portfolio safety tests. New tests verify long and short stop-gap fills receive adverse slippage in both standalone and portfolio engines.

## Historical dataset scope

Five committed one-minute OHLCV files were analyzed. Each has roughly 569,125 rows, with no nonconsecutive timestamp transitions in the covered period. Coverage runs from 2025-10-20 08:50 UTC through 2026-11-19 14:14–14:16 UTC, depending on asset.

| Asset | Active transitions | Zero-volume rows | Exact open = previous close |
|---|---:|---:|---:|
| BTC | 569,124 | 0 | 54.90% |
| ETH | 569,124 | 0 | 53.95% |
| SOL | 569,125 | 0 | 58.47% |
| DOGE | 569,121 | 4 | 58.26% |
| AVAX | 568,500 | 626 | 53.86% |
| **Total** | **2,844,994** | **630** | **55.90% weighted** |

Per-file SHA-256:
- BTC: `3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633`
- ETH: `8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2`
- SOL: `8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3`
- DOGE: `eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4`
- AVAX: `44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5`

The audit uses positive-volume candles for active-trade transitions, bridges zero-volume rows, and resets the comparison across timestamp discontinuities. Adjacent-minute and active-trade opening-jump distributions are both reported.

## Preliminary empirical findings

Hypothetical stops are placed at the previous positive-volume candle close. The next positive-volume candle open is tested against the stop. Stop distances are a sensitivity grid, not selected strategy parameters.

Across all five assets:
- At a 0.05% stop distance: 18 long and 30 short open-through-stop events (48 total).
- At a 0.10% stop distance: 1 long and 1 short event (2 total).
- At 0.15% and wider: no events were observed in these files.
- Largest observed active-trade opening jump: 13.1281 bps (0.131281%) on SOL.
- Largest observed absolute opening jumps by asset: BTC 6.4570 bps; ETH 7.6547 bps; SOL 13.1281 bps; DOGE 12.5815 bps; AVAX 8.5251 bps.

The event counts at the narrowest stop are small. Their reported percentiles are explicitly flagged as descriptive only and not stable tail estimates.

## Synthetic stress scenarios

A separate synthetic table assumes an extra adverse gap beyond the stop, expressed as a percentage of reference entry. Price-loss multiple is:

`(stop distance + extra gap) / stop distance`

Examples:
- 0.25% stop + 0.25% extra gap = 2.0R price loss.
- 0.25% stop + 0.50% extra gap = 3.0R.
- 0.25% stop + 1.00% extra gap = 5.0R.
- 0.50% stop + 0.50% extra gap = 2.0R.
- 1.00% stop + 1.00% extra gap = 2.0R.

These are synthetic assumptions, not observed events, executable fills, or a maximum-loss bound. Fees, slippage and market impact are excluded from this simple multiplier.

## Critical source-provenance warning

The five CSVs were introduced by repository commit `966a23843d8bad6bc79e3ea48c56edcace9e3a5d`, which added the five data files but no upstream provider manifest or 1m acquisition/normalization procedure. The reviewed repository code's `src/prepare_data.py` consumes these 1m files and resamples higher timeframes; it does not document how the original 1m files were acquired or stitched.

More than half of every asset's consecutive candle opens exactly equal the preceding close (53.86%–58.47%), despite positive volume on almost all rows. This is a source-continuity warning, not proof that the data are synthetic. Until the original provider/export, candle boundary convention and any forward-fill/stitching transformations are verified, the very small observed gap counts must not be treated as representative market-tail evidence or used to accept G0-07.

## Remaining G0-07 work

1. Verify the original OHLCV provider/export and the process used to create the five CSVs. Compare selected exact-match and gap-event timestamps with source candles if the provider can be identified.
2. Keep candle-open gap statistics separate from actual stop-order execution risk. The audit does not measure order-book depth, spread, queue position, mark/index-trigger behavior, latency, or real stop-market slippage/market impact.
3. Complete contract lot/tick/minimum-quantity rounding only after G0-08 instrument metadata and fee assumptions are verified.
4. Reassess empirical gap-risk conclusions after source provenance is established; retain explicit synthetic stress cases.

## Safety boundary

This audit performed no strategy signal selection, trade simulation, strategy PnL calculation, execution-resolution comparison, orders, fills, or live trading. No Gate 2+ work is authorized by this checkpoint.


## Follow-up source verification — 2026-11-28

The later public-API sample verification supersedes the earlier source-warning disposition as follows: 35/35 sampled OHLC candles across BTC, ETH, SOL, DOGE and AVAX matched OKX V5 history-candles exactly, and 35/35 CSV volume values matched OKX volCcy (base-currency volume). The exact-open/previous-close pattern is therefore consistent with the sampled native OKX candles; it is not evidence by itself of synthetic stitching.

The CSV volume unit is base currency, not contract count. It matched OKX contract vol only for SOL and AVAX in these samples; it did not match contract vol for BTC, ETH or DOGE. Do not use the CSV vol column as exchange contract quantity or for contract-lot rounding.

- Source verification status: `OKX_SAMPLE_OHLC_AND_BASE_VOLUME_MATCH_NOT_FULL_PROVENANCE`.
- Successful workflow: [46157813117](https://github.com/islamomanpk-boop/okxtester/actions/runs/46157813117).
- Source sample artifact ID: `15267999478`.
- Combined artifact ZIP SHA-256: `9deaae351954f7046c42e4a189cef8a7f61b68bbfb09371aaa18f3cee14ea76d`.
- Gap report JSON SHA-256: `5262b452e72c9cd1765c9b8576a5fcfaa11bb22b8d81058f46e7d75e0252800c`.
- Source verification JSON SHA-256: `346b81ad2beb3f82848ff47b1516be9d382b2f8dc12613c3e0108cbafc7de4e8`.

This improves source confidence but does not certify every row or document the original full-file export pipeline. G0-07 remains OPEN for actual stop-order execution risk assumptions and exchange-specific sizing/rounding work after G0-08 metadata verification.
