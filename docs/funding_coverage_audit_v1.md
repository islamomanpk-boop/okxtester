# Phase 3 Funding Coverage Audit V1

## Purpose

Provide a fail-closed, reproducible audit of the five locally stored OKX realized funding CSVs before any Phase 3 perpetual-swap PnL backtest.

## What it checks

- Presence of all five files: BTC, ETH, SOL, DOGE and AVAX USDT swaps.
- Required columns and exact instrument name.
- Positive integer millisecond timestamps, strict chronological order and no duplicates.
- Finite realized rates with absolute value no greater than 1.
- SHA-256 checksum and absolute source path for each file.
- Exact expected first/last settlement timestamps and configured interval.
- Missing and irregular settlement intervals.
- Equality of settlement timestamp sets across all five instruments.
- JSON manifest plus human-readable Markdown report.

No missing settlement is imputed or replaced with a zero rate.

## Historical audit window

Defaults reflect the period covered by the existing funding reconciliation report:
- Start: 2025-10-20 00:00 UTC (1760918400000).
- End: 2026-11-19 16:00 UTC (1795104000000).
- Expected interval: 8 hours (28800000 ms), based on the observed 1,187 intervals in the prior report.

The interval and endpoints are explicit audit assumptions, not a universal claim about every OKX instrument or every future period. If the source history legitimately has a documented schedule change, investigate and approve that separately; do not silently relax the cadence.

## Run locally

    python -m unittest discover -s src -p 'test_funding_coverage_audit.py' -v
    python src/funding_coverage_audit.py --funding-dir "$HOME/okx_scalping_data/funding_rates/processed" --output-dir reports/funding_coverage_audit_v1

A successful real-data run must produce:
- reports/funding_coverage_audit_v1/funding_coverage_manifest.json
- reports/funding_coverage_audit_v1/funding_coverage_audit.md

The script exits non-zero if any file is absent, malformed, incomplete, out of order, duplicated, has a wrong instrument, contains invalid rates, or differs from the other assets' timestamp set.

## Important limitation

GitHub Actions runs unit tests using synthetic fixtures only. Funding CSVs are intentionally local and not committed to Git, so a green workflow proves the audit logic tests pass—not that the user's actual funding files passed. The real-data command must run in the environment where the five processed files are present. Archive the resulting manifest/report after a real-data PASS; never claim a real funding audit passed based only on the unit-test workflow.
