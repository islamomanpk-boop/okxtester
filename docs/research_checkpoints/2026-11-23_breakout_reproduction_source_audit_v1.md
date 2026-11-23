# Breakout Reproduction Source Audit V1

**Date:** 2026-11-23  
**Branch:** `price-action-v1`  
**Status:** Audit checkpoint; no new breakout reproduction has been run.  
**Purpose:** Prevent an incorrect reuse of the historical sideways-detector implementation when reconstructing the accepted breakout event masks.

## Findings

1. The local Termux research data directory contains the five required original 1-minute files: BTC, ETH, SOL, DOGE, and AVAX. A LINK file is also present but is outside the accepted five-asset universe.
2. `synchronized_5asset_1m.csv` has the expected wide schema (`ts` plus OHLCV columns for each of the five accepted assets) and 569,125 data rows (569,126 lines including the header). This agrees with the previously accepted common-timestamp count. This header/row-count check is not a fresh data-quality or event-reproduction audit.
3. The repository contains `research/sideways_detector_original_v1.py`, which reconstructs the historical 48H detector from its own documented alignment and feature sample. It is not the accepted breakout/retest event engine.
4. The accepted breakout reproduction checkpoint records its own dynamically recomputed P25/P40 thresholds and exact 20 event counts. Those accepted thresholds must be recomputed through the accepted breakout pipeline and its joined observation sample. Do not substitute thresholds from another detector reconstruction, even if the formulas appear related.
5. The accepted breakout masks require the same frozen 4H snapshot for prior/current 15M observations, prior close at/inside the boundary and current close outside, no added previous-sideways condition, and no de-clustering/cooldown. The 15M close label maps to the final 1M candle at label minus one minute; follow-up starts at the next minute.

## Reproduction gate

Before any matched-control candidate or outcome calculation:

- Reconstruct the accepted breakout feature/snapshot pipeline from its original code or sufficiently complete recorded specification.
- Recompute the dynamic thresholds using the accepted joined observation sample; do not hard-code rounded values.
- Reproduce all 20 accepted asset × definition × direction event counts exactly.
- Stop on any mismatch and report it without tuning definitions to force agreement.
- Keep the calculation read-only and preserve existing local reports, untracked research folders, and backups.

## Source recovery status

The complete original breakout/retest Python source has not yet been located in the current GitHub tree. The current audit has not established that the existing historical detector source is an interchangeable replacement. The exact original breakout feature construction and joined quantile sample remain to be verified before implementing the reproduction.

## Accepted reference

See `docs/research_checkpoints/2026-11-22_original_breakout_event_reproduction_pass.md` for the accepted thresholds, event counts, and mask rules. This checkpoint records a source-audit finding only; it does not supersede or alter that accepted result.
