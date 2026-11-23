# Historical Boundary Event Reconstruction V1 — Code Review and Outcome-Timing Notes

Date: 2026-11-23
Branch: `price-action-v1`
Reviewed files:
- `research/sideways_boundary_events_historical_v1.py`
- `tests/test_sideways_boundary_events_historical_v1.py`
- `docs/research_checkpoints/2026-11-23_historical_boundary_event_reconstruction_spec_v1.md`
- `docs/research_checkpoints/2026-11-23_historical_boundary_event_reconstruction_integrity_pass.md`

## Review conclusion

The core state-machine implementation is consistent with the frozen event protocol on the inspected paths:
- Upper and lower directions maintain independent active-test and rank state.
- A test begins on a touch; further touches remain in the same active test.
- Strong rejection is recorded at most once per test.
- Separation requires a non-touch candle and the specified 20%-of-width close condition.
- A separation candle closes/arms but does not also start a new test.
- A 15M timestamp gap closes an active test at the previous observed candle label, resets rank, and increments the continuity segment.
- Snapshot processing is bounded to bars with opening timestamps in [feature availability, next feature availability); the first observed bar in that interval is suppressed.
- Snapshot changes create a fresh process call and therefore reset state/rank.
- The output directory guard refuses to write into a non-empty directory.

This is a focused code review, not a new run or a replacement for the six passed output-integrity checks.

## Critical timestamp convention for future outcomes

The source 15M `ts` values label candle OPEN times. The reconstruction currently stores:
- `test_start_ts_ms`: opening timestamp of the first touch candle.
- `first_strong_rejection_ts_ms`: opening timestamp of the first qualifying rejection candle.
- `test_end_ts_ms`: opening timestamp of the last candle included in the test, including a separation candle when closure_reason is `separated`, or the final eligible candle when closure_reason is `snapshot_end`.

The OHLC close of a 15M candle is not known until 15 minutes after its opening timestamp. Therefore:
- A rejection identified from candle label T is only confirmed at T + 15 minutes.
- A separation confirmed using candle label T is only known at T + 15 minutes.
- For a snapshot-end test, the last included candle's close is known at `test_end_ts_ms + 15 minutes`; in ordinary complete snapshot intervals this should coincide with the next snapshot availability.
- Any forward-return or execution study must start no earlier than the confirmed signal time. It must never include any part of the rejection candle or earlier movement as post-signal performance.
- If using 1M data, the first eligible 1M candle must have an opening timestamp at or after the rejection candle close. Entry/fill assumptions must be specified separately and must not assume a fill at a price that was only knowable before signal confirmation.

Do not silently reinterpret the stored `first_strong_rejection_ts_ms` as a candle-close or executable-entry timestamp. Preserve the existing event ledger and derive a separate explicit `rejection_confirmed_at_ts_ms = first_strong_rejection_ts_ms + 900000` field in any downstream dataset, with validation against the 1M timeline.

## Remaining targeted checks before outcomes

1. Confirm final eligible 15M candle close timestamps against each snapshot's next availability, especially the final feature snapshot and dataset tail.
2. Confirm the 1M data contains the exact 15M rejection-candle close timestamp and that the next 1M candle opens there; inspect incomplete tail behavior.
3. Add unit tests/documentation that make the open-time versus close-confirmation convention explicit before implementing outcomes.
4. Keep snapshot-end and gap-terminated tests clearly identified as censored/administratively closed observations; do not treat their end as a rejection signal.
5. Do not use the earlier unreconciled 2,095-event outcome study.

## Status and limits

No source code, test, event CSV, detector feature, or prior report was modified by this review. No forward outcomes, fills, costs, funding, profitability, or predictive claims were calculated. The event reconstruction's existing integrity-pass status remains unchanged.
