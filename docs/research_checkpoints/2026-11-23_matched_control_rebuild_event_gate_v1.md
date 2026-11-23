# Matched-Control Rebuild V1 — Event Gate Implementation Checkpoint

**Date:** 2026-11-23  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Status:** implementation committed; runtime validation pending  
**Scope:** mandatory read-only reproduction gate only. This checkpoint does not accept any matched-control result.

## New code

- `research/matched_controls/matched_control_event_gate_v1.py`
- GitHub commit: `da8823b6fcb06eefb49df38232f7136787a5807e`
- GitHub file: https://github.com/islamomanpk-boop/okxtester/blob/price-action-v1/research/matched_controls/matched_control_event_gate_v1.py

The committed file was fetched back from the target branch after creation. Its stored content was verified; this is a GitHub storage check, not a runtime test against the user's Termux data.

## Important source reconstruction decision

The accepted event-count diagnostic establishes that the channel-width quantiles must be calculated from the **joined 15M observation population**, after backward-as-of mapping of completed 4H snapshots to 15M bars. Calculating quantiles only from unique 4H feature rows is a different population and must not be substituted.

The gate preserves:
- 4H and 15M epoch-aligned, left-labelled/left-closed aggregation;
- complete 4H and 15M candles only;
- 12 completed 4H candles for the frozen channel;
- directional efficiency <= 0.30 and mean adjacent overlap >= 0.70;
- joined-15M full-sample P25 and P40 quantiles;
- backward-as-of snapshot alignment;
- same-snapshot prior/current 15M requirement;
- exact accepted upper/lower crossing masks;
- no previous-sideways requirement, no de-clustering and no cooldown;
- the accepted five-asset common 1M timestamp intersection and exact one-minute continuity.

## Hard stop

The script compares all 20 asset × definition × direction counts against the accepted reference table. Any mismatch returns a non-zero exit and prints a STOP message. It performs no control construction or outcome calculations.

Expected counts (lower / upper):

| Asset | Broad P40 | Strict P25 |
|---|---:|---:|
| BTC | 91 / 115 | 62 / 81 |
| ETH | 87 / 77 | 51 / 51 |
| SOL | 117 / 96 | 77 / 71 |
| DOGE | 81 / 75 | 55 / 65 |
| AVAX | 84 / 109 | 64 / 83 |

## Current status and next action

- Code creation: committed.
- GitHub read-back: verified.
- Runtime execution against the user's local data: **pending**.
- Matched-control implementation: not yet added; it must remain blocked until this gate passes 20/20.

Run from Termux after pulling the branch:

```bash
cd ~/okxtester || exit 1
git pull --ff-only origin price-action-v1
python research/matched_controls/matched_control_event_gate_v1.py
```

Do not proceed to matching if the script reports anything other than 20/20. Preserve the complete terminal output in the next checkpoint before adding the matching/outcome stage.
