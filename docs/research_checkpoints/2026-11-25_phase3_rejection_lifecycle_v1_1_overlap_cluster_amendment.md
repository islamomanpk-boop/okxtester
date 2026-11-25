# Phase 3 Rejection Lifecycle V1.1 — Overlap-Cluster Amendment

**Date:** 2026-11-25  
**Parent protocol:** `docs/research_checkpoints/2026-11-25_phase3_boundary_lifecycle_closure_protocol_v1.md`  
**Status:** Frozen before V1.1 implementation and historical rerun.  
**Reason:** Independent audit of the V1 pilot found that dependence was disclosed but overlap clusters were not explicitly assigned in the event-level outputs. Gate 1 requires event de-clustering and dependence reporting.

## 1. Scope of amendment

This amendment changes only the dependence-cluster reporting for Module A — Rejection Lifecycle. It does not change:
- source populations, event IDs, frozen boundaries, time zero, inclusion/exclusion rules;
- the 10% retest band, 20% inward-separation line, 24-hour window, or state machine;
- OHLC ambiguity, censoring, event outcomes, or summary statistics;
- the no-trading/no-PnL boundary.

The V1 run remains preserved as a pilot snapshot. V1.1 is the acceptance candidate.

## 2. Frozen overlap-cluster definition

Construct connected components of overlapping observed post-confirmation windows, grouped by **asset** across both strict/broad definitions and both boundary directions. This deliberately groups nested-cohort duplicates and opposite-side events that share the same asset price path.

For each event:
- window start = `confirmation_ts_ms`;
- window end-exclusive = `confirmation_ts_ms + observed_bars_24h * 60000`;
- observed bars stop at the first data gap or available source end, and never exceed 1,440 bars.

Within each asset, sort events by start timestamp, then immutable `event_id`. Assign interval-graph connected components using a running maximum end-exclusive timestamp:
- if the next event's start is strictly less than the current component's running end, it belongs to that component;
- if its start is equal to or later than the running end, start a new component;
- update the running end to the maximum end in the component.

This makes touching but non-overlapping half-open intervals separate clusters, while transitive overlaps remain in one cluster.

Each event receives:
- stable `overlap_cluster_id` = `{asset}|overlap|{zero-padded component number}`;
- `overlap_cluster_size`;
- `overlap_cluster_start_ts_ms`;
- `overlap_cluster_end_exclusive_ts_ms`.

Propagate the same cluster fields to every retest-episode and horizon row. Group summaries must report the number of distinct clusters represented, in addition to event counts and complete/censored counts.

## 3. Interpretation and stopping rules

- Clusters are dependence groups, not new market events and not a reason to delete or relabel source events.
- Strict remains nested within broad. Because clustering is across both definitions, the same cluster IDs may appear in both cohort summaries; do not sum cluster counts across strict and broad.
- Upper/lower events for the same asset may share a cluster when their windows overlap.
- Do not compute independent-event standard errors, p-values, or confidence intervals from the clustered rows in V1.1.
- Report total clusters, clusters by asset, largest cluster size, cluster-size distribution, and event counts per cluster.
- If cluster assignment is non-deterministic, any source identity is lost, or any event lacks a positive observed window, stop and do not accept the run.

## 4. Reproducibility

The V1.1 implementation must retain the V1 source Git blob pins, event and episode IDs, and output definitions, while recording:
- this amendment path;
- implementation and test SHA-256;
- cluster algorithm and output cluster counts;
- all V1.1 output SHA-256 hashes;
- workflow run, artifact and output commit references.

V1.1 outputs must use a new archive directory and must not overwrite the V1 pilot.
