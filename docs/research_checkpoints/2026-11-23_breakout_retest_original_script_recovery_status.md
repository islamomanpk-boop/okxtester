# Breakout/retest original Python source recovery status

**Date:** 2026-11-23  
**Research track:** OKX price-action / sideways-channel breakout and retest  
**Status:** Original source identified in prior conversation; source file not yet recovered into GitHub.

## Confirmed prior source

- Prior conversation date: 2026-11-22.
- Exact conversation/script title: `FINAL TIMING-CORRECTED BREAKOUT AND RETEST RESEARCH`.
- The original assistant output was a complete runnable Termux heredoc beginning with:
  ```sh
  cd ~/okxtester
  python - <<'PY'
  ```
  and ending with `PY`.
- It covered BTC, ETH, SOL, DOGE, AVAX and 15M/1H/4H/12H follow-up horizons.
- Its timing rules mapped the 15M close label to the final 1M candle inside the signal (signal close label minus one minute), began follow-up at the next 1M candle, and included the first follow-up minute in retest search.
- It measured band approach separately from actual penetration of the original channel boundary and retained only complete candles/horizons.

## Existing result record

The final empirical results were saved in:
`docs/research/sideways_breakout_retest_timing_corrected_empirical_results_v1.md`

Original result commit:
`9dbd53c4e3c499eccbe71fec87c73671e553f4f8`

That commit added the results report only; inspection of its full diff confirms it did not add the Python source.

## Recovery limitation and next action

The prior conversation/source has been identified, but the full verbatim code body was not returned by the available conversation-retrieval result in this session. Do not reconstruct or label replacement code as the original.

Next action: recover the complete code block from the 2026-11-22 conversation titled `FINAL TIMING-CORRECTED BREAKOUT AND RETEST RESEARCH`, then commit it as a runnable source file in this repository. Preserve the original verbatim first; any audit or corrections must be made in a separately named version with tests and a clear change log.

## Research safeguards

- Do not substitute the separate 1M-to-15M/4H OHLCV aggregation audit.
- Do not substitute either historical sideways detector implementation.
- Before using this engine for matched-control work, reproduce all 20 accepted breakout counts exactly. Any mismatch is a hard stop.
- Keep the research descriptive; this script's MFE/MAE and retest observations are not a strategy backtest or evidence of profitability.
