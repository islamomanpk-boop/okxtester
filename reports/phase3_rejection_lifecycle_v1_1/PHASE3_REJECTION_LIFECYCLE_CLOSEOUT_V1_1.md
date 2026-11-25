# Phase 3 Rejection Lifecycle V1.1 — Descriptive Closeout

**Date:** 2026-11-25  
**Decision:** **ACCEPTED — descriptive Module A complete**  
**Phase 3 Gate 1:** **PARTIAL / OPEN** — breakout failed-lifecycle Module B remains outstanding.  
**Strategy / PnL authorization:** None. This closeout does not authorize Gate 2 entries, Gate 3 candidate entries, Gate 4 exits, or Gate 6 strategy PnL backtests.

## 1. Research question and scope

After a historically reconstructed 15-minute rejection at a frozen sideways-channel boundary is confirmed, how often does price revisit the boundary band, move inward, close through the boundary, reclaim it, or make repeated retests?

This is a descriptive price-path study. It does not test executable entries, fills, costs, profitability, causality, or prediction.

The study used the accepted source event ledger, exact frozen feature snapshots, accepted rejection-anatomy rows, and five committed 1-minute market files. It preserves the strict cohort as a nested subgroup of broad; counts across broad and strict must never be summed as independent market events.

## 2. Frozen population, provenance, and timing

- Assets: BTC, ETH, SOL, DOGE, AVAX.
- Accepted source ledger rows: 2,452.
- Eligible first-strong-rejection rows: 1,992, comprising 1,154 broad and 838 strict.
- Strict is nested within broad.
- Frozen boundary values were joined by asset and zero-based snapshot index, with current and next feature availability timestamps checked.
- Event IDs were reproduced and matched one-to-one to all 1,992 accepted anatomy rows.
- Time zero: exact 1-minute candle opening at the completed 15-minute rejection candle's close, exactly 900,000 ms after its source open timestamp.
- Primary geometry: 10% channel-width boundary band and 20% inward-separation line.
- Horizons: 15m, 1h, 4h, 24h.
- All 1,992 events had an exact confirmation minute.
- Five source 1-minute files were pinned to their Git blob IDs; row counts were BTC 569,125, ETH 569,125, SOL 569,126, DOGE 569,126, AVAX 569,127. No source had a 1-minute gap.

The exact input Git blob IDs and output SHA-256 values are in `reports/phase3_rejection_lifecycle_v1_1/run_metadata_v1.json`.

## 3. Descriptive findings

### 3.1 Event-level first passages

| Cohort / side | Events | First retest | First inward separation | First close-through | First reclaim after close-through |
|---|---:|---:|---:|---:|---:|
| Broad — upper | 596 | 543 (91.1%) | 420 (70.5%) | 457 (76.7%) | 433 (72.7%) |
| Broad — lower | 558 | 517 (92.7%) | 359 (64.3%) | 462 (82.8%) | 420 (75.3%) |
| **Broad — total** | **1,154** | **1,060 (91.9%)** | **779 (67.5%)** | **919 (79.6%)** | **853 (73.9%)** |
| Strict — upper | 442 | 404 (91.4%) | 312 (70.6%) | 348 (78.7%) | 327 (74.0%) |
| Strict — lower | 396 | 369 (93.2%) | 259 (65.4%) | 334 (84.3%) | 305 (77.0%) |
| **Strict — total** | **838** | **773 (92.2%)** | **571 (68.1%)** | **682 (81.4%)** | **632 (75.4%)** |

These are separate descriptive cohorts; strict is a nested sensitivity subgroup, not additional independent evidence. First inward separation and first close-through can both occur in the same event at different times. A retest is not a successful-hold label.

Among events with a first close-through, a later reclaim was observed within the available window for 853/919 broad events (92.8%) and 632/682 strict events (92.7%). A reclaim is a later close back inside the frozen boundary; it is not proof of a profitable reversal or a valid entry.

### 3.2 Retest episodes and ambiguity

The run produced:
- 3,028 distinct retest episodes across 1,833 event rows with at least one episode;
- 1,601 episodes resolved by a close-through of the frozen boundary;
- 1,416 resolved by inward separation;
- 11 remained unresolved at the 24-hour observation limit.

A 1-minute candle can satisfy more than one OHLC condition. There were 1,626 same-bar-ambiguous episode resolutions: all 1,601 close-through resolutions and 25 inward-separation resolutions. No intrabar ordering was invented. The remaining 1,402 episode resolutions did not have same-bar ambiguity.

### 3.3 Horizon completeness

| Horizon | Event rows | Complete | Censored |
|---|---:|---:|---:|
| 15 minutes | 1,992 | 1,992 | 0 |
| 1 hour | 1,992 | 1,992 | 0 |
| 4 hours | 1,992 | 1,992 | 0 |
| 24 hours | 1,992 | 1,982 | 10 |

The 24-hour censoring is source-end censoring: 8 broad rows and 2 strict rows. There were no gap-censored events because all five 1-minute files had zero gaps. Strict/broad rows overlap and must not be added as independent observations.

### 3.4 Overlap-cluster audit

V1.1 assigns interval-graph connected components by asset across both definitions and both boundary directions. The half-open observed windows overlap only when the next event starts strictly before the running cluster end.

- Total overlap clusters: **380**
- BTC: 76; ETH: 79; SOL: 78; DOGE: 71; AVAX: 76
- Largest cluster: **32 event rows**
- Cluster-size distribution: 53 singleton clusters, 90 size-2, 21 size-3, 70 size-4, 9 size-5, 34 size-6, 8 size-7, 29 size-8, 4 size-9, 21 size-10, 6 size-11, 11 size-12, 2 size-13, 3 size-14, 3 size-16, 1 size-17, 7 size-18, 1 size-19, 3 size-20, 1 size-21, 2 size-22, and 1 size-32 cluster.

Cluster IDs and sizes are propagated to event, episode, and horizon rows. The independent audit recomputed the interval components and obtained zero cluster-ID mismatches. The sum of cluster sizes equals all 1,992 event rows. Clusters are dependence groups, not new events and not a reason to remove source rows.

## 4. Independent output-integrity audit

The following checks passed independently against the committed CSV blobs:

- 1,992 unique event IDs; no invalid channel widths or confirmation timestamps.
- 3,028 unique episode IDs; zero orphan episodes; zero duplicate IDs.
- Event-to-episode count reconciliation: zero mismatches.
- Episode timestamp / elapsed-minute / positive-bar-count checks: zero failures.
- 7,968 horizon rows: exactly four horizon rows per event; no missing event/horizon combinations.
- Cluster IDs independently recomputed: zero mismatches.
- Episode and horizon cluster IDs/sizes matched their parent event rows exactly.
- 200 grouped summary rows.
- All five source 1-minute datasets had zero timestamp gaps.

This is an independent structural and provenance audit of the outputs and cluster assignment, not a separate second implementation of every price-path calculation. The code and synthetic tests remain the primary reproducible calculation.

## 5. Tests and reproducibility

- Protocol: `docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md`
- Frozen V1.1 amendment: `docs/research_checkpoints/2026-11-25_phase3_rejection_lifecycle_v1_1_overlap_cluster_amendment.md`
- Implementation: `research/phase3_rejection_lifecycle_v1_1.py`
- Tests: `tests/test_phase3_rejection_lifecycle_v1_1.py`
- Workflow: `.github/workflows/phase3-rejection-lifecycle-v1-1.yml`
- Synthetic tests: **12 passed**
- Historical workflow run: [45627723414 — success](https://github.com/islamomanpk-boop/okxtester/actions/runs/45627723414)
- Workflow artifact ID: `15028138933`; artifact digest: `sha256:e8d12a4d2de9ebe3ffb7c2375fa8a4ac1e30364a59882c1a3a4424ff17a3d116`
- Output archive commit: `2987ca84a4277170beea9ae36ef88133c886d6bb`

Output SHA-256 values:
- Events: `56d48f52a6b2eeaa62f0e8696c62802a2a3a0839d6e6bd4038f5dfdc8de60f65`
- Episodes: `27c39aed94bbd9354603bce24ef6095d3f02eb5da20c48b514d453571db6d9af`
- Horizons: `038f2e1167d101ff63674f3b9d1a8fee1440ebfe35f811ac8f1c1b0bf53999c0`
- Group summary: `060b325ea893e918b0a4733a69d45a0885bbd0d4fed88d366051d184d8fa66c6`

The initial V1 run without overlap clusters is preserved in `reports/phase3_rejection_lifecycle_v1/` as a pilot. V1.1 is the acceptance archive; it does not overwrite the pilot.

## 6. Decision and practical consequence

**Module A is accepted as a completed descriptive rejection-lifecycle study.** The results show that boundary-band revisits are common, but close-throughs are also common, and many episode resolutions are intrabar ambiguous. Therefore, a boundary retest or a single rejection label cannot be treated as a confirmed successful hold or executable signal.

This acceptance means the rejection lifecycle is now sufficiently defined to serve as a fixed 15-minute signal cohort for later Gate 2 execution-resolution research, but Gate 2 remains closed until Module B (breakout failure/reclaim lifecycle) also completes and the overall Gate 1 closeout is issued.

No strategy was selected. No entry, fill, stop, target, cost, funding, position sizing, PnL, or profitability claim was tested. Overlapping events remain dependent, strict is nested within broad, and OHLC cannot establish intrabar order.

## 7. Next action

Complete Module B under the frozen lifecycle protocol: outside retest/hold, 1-minute return-inside, completed-15-minute return-inside confirmation, breakout-side reclaim, inside retest after failure, and reversal-direction path. Keep upper/lower breakout sides separate and preserve the original breakout source cohort. Then issue the overall Gate 1 decision.
