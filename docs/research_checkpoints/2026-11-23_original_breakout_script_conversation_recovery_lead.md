# Original timing-corrected breakout script — conversation recovery lead

Date: 2026-11-23  
Research track: OKX price-action / sideways-channel breakout and retest  
Status: exact source identified by conversation title/time; full literal code body still not recovered into repository.

## Exact historical conversation lead

- Conversation title: `FINAL TIMING-CORRECTED BREAKOUT AND RETEST RESEARCH`.
- Assistant code message timestamp: approximately 2026-11-22 13:37:41 UTC.
- User execution timestamp: approximately 2026-11-22 13:41:39 UTC.
- The command was a complete Termux heredoc beginning:
  ```sh
  cd ~/okxtester
  python - <<'PY'
  ```
  and ending with the heredoc terminator `PY`.

## User-confirmed output from that exact run

| Asset | Broad lower | Broad upper | Strict lower | Strict upper |
|---|---:|---:|---:|---:|
| BTC | 91 | 115 | 62 | 81 |
| ETH | 87 | 77 | 51 | 51 |
| SOL | 117 | 96 | 77 | 71 |
| DOGE | 81 | 75 | 55 | 65 |
| AVAX | 84 | 109 | 64 | 83 |

## Accepted method details recorded with the conversation

- Complete right-labelled, left-closed 15M and 4H bars.
- Causal prior 12 completed 4H context candles.
- Backward as-of feature/snapshot mapping and same-snapshot guard.
- Upper event mask: `sideways & same_snapshot & (previous_close <= upper) & (current_close > upper)`.
- Lower event mask: `sideways & same_snapshot & (previous_close >= lower) & (current_close < lower)`.
- No additional previous-sideways/previous-selected requirement.
- No cooldown or de-clustering.
- Signal final 1M candle is the 15M signal close label minus one minute.
- Follow-up begins at the next 1M candle; the first follow-up minute is included in retest search.
- The run included 48H features, P25/P40 widths, band approach/penetration, and next completed 15M hold.

## Important source distinction

The 506-line file currently preserved as `research/archive/final_timing_corrected_breakout_and_retest_research_original_v1.sh` is **not confirmed as this exact conversation source**. It differs in material ways: it applies `previous_selected` and calculates quantiles from unique 4H feature rows. V5 demonstrated that this archived file's event logic does not reproduce the historical 20 counts.

Do not overwrite or relabel the 506-line archive. Preserve it as its own recovered artifact until the actual 2026-11-22 heredoc is retrieved verbatim.

## Recovery status and next action

Conversation metadata identifies the exact title, timestamp, and user-confirmed output, but the complete literal code body was not returned by the available retrieval result. Do not reconstruct missing code or claim the source has been recovered.

Retrieve the assistant's original code block from the 2026-11-22 conversation and preserve it verbatim as a separate source file. Then independently run its event-count section and verify all 20 counts before using it for matched-control research.

## Research restriction

**HOLD:** no matched controls, forward outcomes, matching, inference, or profitability calculations until the exact original code is preserved and its 20 counts are reproduced, or a new engine is explicitly approved as a new baseline.
