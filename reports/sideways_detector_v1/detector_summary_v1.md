# Reconstructed Sideways Detector v1 — Run Summary

**Status:** calculation run completed; independent formula/data audit still required.

Research-only. Full-sample asset-specific P25/P40 thresholds are retrospective.

| Asset | Valid snapshots | P25 width % | P40 width % | Strict sideways | Broad sideways |
|---|---:|---:|---:|---:|---:|
| BTC | 2359 | 3.19048229 | 3.87218109 | 0 | 0 |
| ETH | 2359 | 4.15974679 | 5.33563939 | 2 | 2 |
| SOL | 2359 | 4.94208992 | 5.93314927 | 0 | 0 |
| DOGE | 2359 | 5.03566026 | 6.07382367 | 0 | 0 |
| AVAX | 2359 | 5.54782779 | 6.68503993 | 0 | 0 |

## Required interpretation limits

- This output contains 4H detector snapshots only; no 15M tests/rejections or outcomes.
- Each snapshot becomes available at the close of its final 4H candle.
- The first 15M candle at the availability timestamp must be excluded downstream.
- P25/P40 use all valid snapshots in the supplied history and therefore are not live-safe.
- Independent recomputation and timestamp mapping must pass before downstream reconstruction.
