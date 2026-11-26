# G0-05 Repeated-Signal Group Metadata Decision — V1

**Date:** 2026-11-26  
**Scope:** Deterministic, metadata-only grouping for the G0-05 canonical candidate schema.  
**Status:** Decision frozen for source-only disposition metadata and synthetic testing.  
**Boundary:** Grouping never removes, merges, suppresses or changes the eligibility of an event.

## 1. Purpose

The canonical schema carries both `overlap_cluster_id` and `repeated_signal_group_id`. They describe different relationships:

- `overlap_cluster_id` groups events whose predeclared observed windows overlap in time. It is a dependence annotation.
- `repeated_signal_group_id` groups events that arise from the same frozen source context and repeated-test/crossing identity domain. It does not imply temporal overlap.

No group is a candidate filter or a trade/episode decision.

## 2. Frozen family mappings

### 2.1 Support/resistance rejection

Use the immutable accepted rejection source context:

`{asset}|rejection|{lower_or_upper}|snapshot_{snapshot_index}|segment_{segment_id}`

All distinct test ranks and test-start timestamps within the same asset, boundary direction, snapshot index and segment ID share the group ID. Each physical test remains a separate source event with its own source identity and candidate ID.

Rationale: the accepted rejection source identity already preserves snapshot, segment, test rank and test start. Test rank distinguishes repeated tests; snapshot+segment provides the stable parent group.

### 2.2 Breakout continuation

Use:

`{asset}|breakout|{UPPER_or_LOWER}|snapshot_{context_snapshot_ms}`

All distinct raw crossings of the same boundary side within the same frozen 4-hour context share the group ID. Each raw crossing remains a separate source event, including a later crossing after return inside.

Rationale: the accepted G0-04 raw source identity is asset + direction + signal time + context snapshot. Context and direction define the repeated-crossing domain without imposing a cooldown or collapsing events.

### 2.3 Failed-breakout reversal

A failed-breakout reversal inherits the `repeated_signal_group_id` of its exact linked source breakout. It does not create a new repeated-signal group.

Rationale: the reversal is a child lifecycle event of the original breakout and retains the same immutable source boundary/context lineage.

## 3. Determinism and constraints

- IDs are constructed only from immutable source fields available in the source record.
- No future price outcome, return-inside time, reclaim, MFE/MAE, PnL or trade result is used to create the group ID.
- No source event is deleted, deduplicated or relabelled because of group membership.
- Strict/broad cohort duplicates collapse only at the already-frozen physical-event identity step; group membership does not alter that rule.
- A missing asset, direction, snapshot, or required segment ID is a fail-closed source-schema error.
- The exact group ID is emitted in the source-only disposition ledger and later carried unchanged into the canonical candidate ledger.

## 4. Synthetic tests required

Test:
1. Rejection tests with different test ranks but the same asset/direction/snapshot/segment share a group.
2. Rejection tests in a different segment or snapshot do not share a group.
3. Breakout crossings with different signal times but the same asset/direction/snapshot share a group.
4. Crossings on the opposite boundary or a different snapshot do not share a group.
5. Failed-breakout reversal inherits its exact source breakout group.
6. Group IDs are deterministic under input-order changes.
7. Missing context fields fail closed.
8. Grouping never changes row counts, source identities or disposition totals.

## 5. Authorization boundary

This decision authorizes only deterministic metadata fields in the source-only disposition ledger and their tests. It does not authorize canonical candidate generation, execution simulation, backtesting, PnL or strategy selection.


## 6. Implementation and source-audit evidence

The frozen group IDs are now emitted in all three source-only disposition ledgers:
- Rejection groups use asset + boundary direction + snapshot index + segment ID.
- Breakout continuation groups use asset + boundary direction + context snapshot.
- Failed-breakout reversal inherits the exact linked breakout group.

Implementation commit: `63e659f7aa68e0b60062409ab3bff963ebea64f7`.

- Source audit [45804274324](https://github.com/islamomanpk-boop/okxtester/actions/runs/45804274324) — SUCCESS; artifact ID `15107399743`; ZIP SHA-256 `0b4ca8ab5e12129d988425d78786efc1d18b3be04be07afabc3b04398a23c124`, independently recomputed after download.
- Synthetic suite [45804297791](https://github.com/islamomanpk-boop/okxtester/actions/runs/45804297791) — SUCCESS; **97/97 tests passed**.

Group cardinality from the artifact:
- Rejection: 1,154 physical rows, 1,046 repeated-signal groups; largest group size 3.
- Breakout continuation: 2,861 raw crossings, 2,051 repeated-signal groups; largest group size 5.
- Failed-breakout reversal: 932 rows, 663 inherited source groups; largest group size 5.

These are metadata group counts, not independent-event counts. No rows are removed, merged, filtered or relabelled because of group membership.
