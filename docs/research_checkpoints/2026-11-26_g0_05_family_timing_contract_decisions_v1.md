# G0-05 Family Timing Contract Decisions — V1

**Date:** 2026-11-26  
**Project:** OKX Price Action V1 — Phase 3 Sideways / Range  
**Dependencies:** G0-04 accepted; primary threshold policy/population recorded in `2026-11-26_g0_05_threshold_policy_population_decision_v1.md`.  
**Status:** Design decisions frozen for synthetic-test implementation; canonical candidate generation remains blocked until source inventory, tests, and full contract review pass.

## 1. Shared time and snapshot convention

All timestamps are UTC epoch milliseconds.

A 4-hour feature snapshot is available at its recorded `available_at_ts_ms`. Its validity interval is half-open:

`[snapshot_available_at_ts_ms, snapshot_next_available_at_ts_ms)`

At the next snapshot availability timestamp, the old snapshot is no longer current. Never treat the endpoint as inclusive for a new signal confirmation. The exact boundary case is covered by `2026-11-26_g0_05_rejection_snapshot_validity_audit_v1.md`.

The primary causal regime classification uses the G0-05 selected `EXPANDING_PRIOR + UNIQUE_4H_FEATURE_ROWS` thresholds, with a minimum of 180 prior completed contexts. Re-evaluate regime eligibility at the event's actual source snapshot; historical full-sample STRICT_P25/BROAD_P40 labels are retained only as source-cohort metadata and reconciliation dimensions.

Apply the original sideways feature conditions at that same snapshot:
- channel width percentage <= the selected causal P25 or P40 threshold;
- directional efficiency <= 0.30;
- mean overlap >= 0.70.

The strict P25 cohort is a nested subset of broad P40. Preserve both labels and all unselected policy/population sensitivities.

## 2. Support rejection and resistance rejection

**Source:** accepted boundary-test ledger and event-anatomy archive, joined to the exact detector feature snapshot and canonical 1-minute data.

- Preserve the source event identity: asset, original definition, direction, snapshot index, segment ID, test rank, and test-start timestamp.
- Preserve the first strong-rejection 15-minute candle open timestamp and original OHLC.
- The source rejection timestamp is the 15-minute candle open, not signal availability.
- Confirmation is the completed rejection candle close: `confirmation_ts_ms = first_strong_rejection_ts_ms + 900000`.
- Require the exact 4-hour snapshot to be available by the rejection candle open and still valid at confirmation: `confirmation_ts_ms < snapshot_next_available_at_ts_ms`.
- The first eligible 1-minute bar opens exactly at the confirmation timestamp. The rejection candle itself is never post-confirmation data.
- Lower/support rejection maps to LONG. Upper/resistance rejection maps to SHORT.
- One candidate may be emitted per source boundary-test identity, using its first qualifying strong rejection. The source repeated-test protocol already requires a completed inward-separation candle before a subsequent test begins; preserve its test rank and identity.
- Do not deduplicate overlapping events across snapshots, assets, definitions, or directions. Preserve overlap clusters as metadata and report both raw and clustered counts.
- If the source event's old snapshot expires at or before confirmation, disposition it as `SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION`; do not rebind the rejection to a newer boundary.

The 1,114 broad / 809 strict counts in the snapshot-validity audit are provisional source ceilings before re-evaluation under the causal threshold policy and all other source/feature checks. They are not expected final candidate counts.

## 3. Breakout continuation

**Source:** G0-04 accepted raw crossing ledger, never the historical 932 selected-identity list or the retrospective Module B event list.

- Each raw crossing identity is evaluated using its recorded 15-minute signal close and accepted 4-hour snapshot.
- A valid upper-boundary crossing maps to LONG; a valid lower-boundary crossing maps to SHORT.
- The 15-minute close label is the signal availability timestamp. The first eligible 1-minute bar opens exactly at that close timestamp.
- Require the same accepted snapshot and causal threshold context to be valid for the crossing at signal availability. A context transition or incomplete 15-minute bar is not silently bridged.
- Preserve each distinct raw crossing identity. A later crossing after a completed return inside is a distinct source event under the raw crossing definition; do not collapse it merely because it shares an asset or snapshot.
- Do not merge continuation candidates with retest-entry hypotheses. Retest execution remains outside G0-05.
- Do not deduplicate overlapping candidates; assign deterministic overlap-cluster IDs for dependence-aware reporting.

## 4. Failed-breakout reversal

**Source:** descriptive Module B lifecycle records only as a source for event anatomy and cross-checks. A Module B historical event is not itself an eligible candidate.

- Require a linked, valid G0-05 breakout-continuation source candidate. The old full-sample Module B cohort cannot substitute for this link.
- Use the breakout's original frozen boundary and snapshot identity throughout its failure lifecycle.
- Confirmation is the first **completed 15-minute close** back inside the original frozen range after the breakout signal:
  - upper breakout: completed close <= original upper boundary;
  - lower breakout: completed close >= original lower boundary.
- Require all 15 component 1-minute bars for the confirmation 15-minute candle. The close timestamp is the reversal signal availability timestamp.
- Upper-breakout failure maps to SHORT; lower-breakout failure maps to LONG.
- The first eligible 1-minute bar opens at the completed 15-minute close timestamp, never inside the confirmation candle.
- The source breakout's snapshot may have rolled over during the lifecycle; this does not rewrite the original breakout boundary. The reversal is evaluated against the immutable source-breakout boundary, not a newly refreshed range.
- Limit the failure-observation lifecycle to 12 hours after the source breakout signal, matching the frozen Module B maximum observation horizon. If no completed return-inside close occurs by that endpoint, record `EXPIRED_NO_RETURN_INSIDE_WITHIN_12H`. If the required data is incomplete or has a gap before resolution, record a specific censored status instead of an expiry.
- Preserve any 15-minute candle whose wick crosses outside while its close returns inside as an OHLC-path ambiguity flag; the completed-close rule confirms the event but does not infer intrabar ordering.
- Preserve later breakout-side reclaim as a separate lifecycle field; it does not revoke the already confirmed return-inside event.
- Never infer a fill or execution price from the confirmation bar.

## 5. Cross-family disposition and de-clustering

- Every source event must receive exactly one explicit terminal or emitted disposition: eligible candidate, rejected with a machine-readable reason, expired, censored, or ambiguous pending a predeclared resolution.
- Candidate identity is deterministic from immutable source identity + family + rule version.
- The source identity, original historical cohort, causal strict/broad label, threshold version, snapshot identity, confirmation timestamp, and first eligible 1-minute timestamp are separate fields.
- Keep support rejection, resistance rejection, breakout continuation, failed upside reversal, and failed downside reversal separately reportable.
- Overlap clusters are descriptive grouping metadata, not a reason to delete candidates.
- A source event may not disappear through an inner join. All left/right source reconciliation counts and row-level mismatch reasons are required.

## 6. Required synthetic tests before canonical execution

In addition to the full 20-case G0-05 contract matrix:
1. Rejection confirmation at the snapshot endpoint is rejected; one millisecond before is accepted.
2. Rejection candle open is not confirmation; the first eligible minute is exactly its completed close.
3. A historical strict/broad label that fails the causal expanding-prior threshold is not emitted as a causal candidate.
4. A raw G0-04 upper crossing maps LONG and lower crossing maps SHORT.
5. A breakout candidate's first eligible minute is exactly the completed 15-minute close.
6. A later raw crossing after a completed return inside remains a separate identity.
7. A failed-breakout reversal without a valid linked breakout candidate is rejected.
8. An upper breakout's completed 15-minute close <= original upper confirms SHORT; lower breakout's close >= original lower confirms LONG.
9. A wick outside with a close back inside is flagged as path ambiguity without overriding the completed-close confirmation rule.
10. An incomplete 15-minute bar cannot confirm failure.
11. The 12-hour endpoint is tested at one millisecond before, exactly at, and one millisecond after the expiry boundary.
12. A new 4-hour snapshot during the failure lifecycle does not replace the source breakout's frozen boundary.
13. Missing or duplicate 1-minute components censor/reject rather than being interpolated.
14. Candidate IDs and substantive outputs are deterministic across identical reruns.

## 7. Execution boundary

This document authorizes only contract finalization and synthetic-test implementation. It does not authorize canonical candidate generation until all source manifests and schemas are frozen, the full test suite passes, and the implementation is independently reproducible within the project's documented no-human-review process.

No orders, fills, synthetic execution prices, stops, targets, costs, fees, funding, position sizing, PnL, profitability, strategy backtests, or OOS claims are authorized. Gate 0 remains CONDITIONAL HOLD pending its other numbered blockers.
