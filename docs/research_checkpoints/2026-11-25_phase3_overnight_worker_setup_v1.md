# Phase 3 Overnight Worker Setup V1

**Date:** 2026-11-25  
**Research branch:** `price-action-v1`  
**Launcher branch:** `main`  
**Status:** CREATED AND VERIFIED IN REPOSITORY; NOT YET DISPATCHED

## Purpose

Provide a single, easy-to-find manual GitHub Actions entry point and a stable recovery artifact for overnight Phase 3 work. The launcher lives on the default branch because GitHub requires a `workflow_dispatch` workflow to exist on the default branch. It checks out the research branch explicitly; research code and outputs remain scoped to `price-action-v1` and workflow artifacts.

## Files

1. Launcher: `.github/workflows/phase3-overnight-research.yml` on `main`.
2. Worker: `research/phase3_overnight_worker_v1.py` on `price-action-v1`.
3. Morning artifact name: `phase3-overnight`.
4. Artifact contents:
   - `PHASE3_OVERNIGHT_INDEX.md` — first file to open in the morning.
   - `input_manifest.json` — source hashes, row counts, OHLCV validation and common-index checks.
   - `gate_status.csv` — machine-readable gate/blocker status.

## Current worker scope

This first version is deliberately read-only. It verifies the five canonical 1M source hashes, expected source row counts, required columns, timestamp uniqueness/order, finite and valid OHLCV, common timestamp intersection and exact 60,000 ms cadence. It verifies the presence of the controlling research documents and produces a recovery index.

It does **not** yet implement or run the causal breakout reconstruction, the six past-only threshold variants, Gate 2 execution-resolution experiments, Gate 3 entry experiments, Gate 4 stop/target experiments, or Gate 5 engine acceptance tests. Those stages must be implemented and accepted in dependency order. The worker must not represent blocked or unimplemented work as complete.

## Hard safety boundaries

- Gate 0 remains CONDITIONAL HOLD.
- Gate 2–5 experiments remain blocked until the required causal event cohort and execution contracts are accepted.
- Gate 6–7 strategy backtesting and chronological validation are not authorized.
- No candidate generation, matched controls, orders, fills, forward outcomes, inference or PnL.
- No repository write permission in the workflow; no commits or pushes from the runner.
- No secrets, VPS access, external exchange requests, raw-data mutation, database changes or service changes.
- Workflow is manual-only; no schedule or automatic repeat.
- Artifact retention is 14 days. Save the artifact or its contents to the research archive if longer-term retention is needed.

## Morning recovery

Open the latest run for **Phase 3 Overnight Research Worker** in GitHub Actions and download the artifact named `phase3-overnight`. Open `PHASE3_OVERNIGHT_INDEX.md` first, then inspect `input_manifest.json` and `gate_status.csv`. The run URL and artifact are the authoritative record of that execution.

## Honest completion status

The workflow launcher and first read-only preflight worker are installed. No workflow run has been dispatched by this setup. This is a reliable first overnight checkpoint, not completion of the remaining Phase 3 gates. Subsequent worker stages must be added only after their research implementations, synthetic tests and prerequisite gates are reviewed.
