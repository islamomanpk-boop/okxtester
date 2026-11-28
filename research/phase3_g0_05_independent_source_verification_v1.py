#!/usr/bin/env python3
"""Independent G0-05 source identity and lifecycle cross-check.

Uses only the Python standard library. It deliberately imports neither the
canonical candidate contract nor the primary source-audit implementation.
It reads frozen source ledgers and the three source-disposition outputs; it
does not generate candidates or alter research data.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
EXPECTED = {"rejection": 1154, "breakout": 2861, "failed_breakout": 932}
HORIZON_MS = 43_200_000
MINUTE_MS = 60_000


def stop(message: str) -> None:
    raise RuntimeError("INDEPENDENT G0-05 SOURCE CHECK FAIL-CLOSED: " + message)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        stop(f"missing input: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            stop(f"missing CSV header: {path}")
        return list(reader)


def integer(row: dict[str, str], field: str, label: str) -> int:
    try:
        value = row[field].strip()
        if not value:
            raise ValueError("blank")
        number = int(value)
    except (KeyError, TypeError, ValueError):
        stop(f"{label}: invalid integer field {field}")
    return number


def disposition_rows(audit_dir: Path) -> dict[str, list[dict[str, str]]]:
    paths = {
        "rejection": audit_dir / "rejection_source_dispositions.csv",
        "breakout": audit_dir / "breakout_source_dispositions.csv",
        "failed_breakout": audit_dir / "failed_breakout_source_dispositions.csv",
    }
    result = {family: read_rows(path) for family, path in paths.items()}
    for family, rows in result.items():
        if len(rows) != EXPECTED[family]:
            stop(f"{family}: {len(rows)} rows != {EXPECTED[family]}")
    return result


def verify_rejection_identity(root: Path, rows: list[dict[str, str]]) -> dict:
    source = read_rows(root / "reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv")
    physical: dict[str, list[str]] = defaultdict(list)
    for row in source:
        if not (row.get("first_strong_rejection_ts_ms") or "").strip():
            continue
        key = "|".join((
            row["asset"], row["direction"].upper(),
            str(integer(row, "snapshot_index", "rejection source")),
            str(integer(row, "segment_id", "rejection source")),
            str(integer(row, "test_rank", "rejection source")),
            str(integer(row, "test_start_ts_ms", "rejection source")),
        ))
        event_id = "|".join((
            row["asset"], row["definition"].lower(), row["direction"].lower(),
            str(integer(row, "snapshot_index", "rejection source")),
            str(integer(row, "segment_id", "rejection source")),
            str(integer(row, "test_rank", "rejection source")),
            str(integer(row, "test_start_ts_ms", "rejection source")),
        ))
        physical[key].append(event_id)
    if len(physical) != EXPECTED["rejection"]:
        stop(f"reconstructed physical rejection identities={len(physical)}")
    observed = {}
    for row in rows:
        key = row.get("source_event_id", "")
        if not key or key in observed:
            stop("blank or duplicate canonical rejection source_event_id")
        observed[key] = row
    if set(observed) != set(physical):
        stop(f"rejection physical-key mismatch source={len(physical)} output={len(observed)}")
    for key, ids in physical.items():
        expected_ids = ";".join(sorted(ids))
        if observed[key].get("source_event_row_ids") != expected_ids:
            stop(f"rejection source-row membership mismatch: {key}")
        status = observed[key].get("disposition")
        reason = observed[key].get("reason_code")
        if status == "ELIGIBLE_FOR_FURTHER_VALIDATION" and reason != "NONE":
            stop(f"eligible rejection has non-NONE reason: {key}")
        if status == "EXPIRED" and reason != "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION":
            stop(f"expired rejection has wrong reason: {key}")
    return {"physical_events": len(physical), "source_memberships": sum(map(len, physical.values())),
            "exact_source_identity_and_membership": True}


def verify_breakout_identity(root: Path, artifact: Path, rows: list[dict[str, str]]) -> tuple[dict, dict]:
    raw = read_rows(artifact / "unique_raw_crossing_events_with_six_variants.csv")
    module_b = read_rows(root / "reports/phase3_breakout_lifecycle_v1_1/breakout_lifecycle_events_v1_1.csv")
    observed_by_key = {}
    for event in module_b:
        key = "|".join((event["asset"], event["direction"],
                        str(integer(event, "signal_time_ms", "Module B event")),
                        str(_iso_ms(event["snapshot"]))))
        observed = integer(event, "observed_bars_12h", "Module B event")
        if key in observed_by_key and observed_by_key[key] != observed:
            stop(f"Module B cohort rows disagree on observed window: {key}")
        observed_by_key[key] = observed
    expected = {}
    for row in raw:
        key = "|".join((row["asset"], row["direction"],
                        str(integer(row, "signal_time_ms", "G0-04 raw")),
                        str(integer(row, "context_snapshot_ms", "G0-04 raw"))))
        if key in expected:
            stop(f"duplicate G0-04 raw crossing: {key}")
        expected[key] = row
    observed = {}
    for row in rows:
        key = row.get("source_event_key", "")
        if not key or key in observed:
            stop("blank or duplicate breakout source_event_key")
        observed[key] = row
    if len(expected) != EXPECTED["breakout"] or set(expected) != set(observed):
        stop(f"breakout exact reconciliation failed source={len(expected)} output={len(observed)}")

    # Independently reconstruct connected components of overlapping, half-open
    # 12-hour observation intervals; no production clustering helper is used.
    grouped: dict[str, list[tuple[int, int, str]]] = defaultdict(list)
    for key, source in expected.items():
        asset = source["asset"]
        start = integer(source, "signal_time_ms", "G0-04 raw")
        observed_bars = observed_by_key.get(key, 720)
        if not 0 < observed_bars <= 720:
            stop(f"invalid observed 12-hour window: {key}")
        grouped[asset].append((start, start + observed_bars * MINUTE_MS, key))
    cluster_by_key = {}
    summary = Counter()
    for asset, intervals in grouped.items():
        intervals.sort(key=lambda x: (x[0], x[2]))
        component = []
        component_end = None
        number = 0

        def finish():
            nonlocal component, number
            if not component:
                return
            number += 1
            cluster_id = f"{asset}|g0_05_raw_overlap|{number:04d}"
            size = len(component)
            for event_key in component:
                cluster_by_key[event_key] = (cluster_id, size)
            summary[asset] += 1

        for start, end, key in intervals:
            if component and start >= component_end:
                finish()
                component = []
                component_end = None
            component.append(key)
            component_end = end if component_end is None else max(component_end, end)
        finish()

    for key, row in observed.items():
        expected_cluster = cluster_by_key[key]
        actual_cluster = (row.get("overlap_cluster_id", ""),
                          integer(row, "overlap_cluster_size", "breakout output"))
        if actual_cluster != expected_cluster:
            stop(f"independent breakout interval-cluster mismatch: {key}")
        status = row.get("disposition", "")
        reason = row.get("reason_code", "")
        if status == "ELIGIBLE_FOR_FURTHER_VALIDATION" and reason != "NONE":
            stop(f"eligible breakout has non-NONE reason: {key}")
        if status == "REJECTED" and reason not in (
            "CAUSAL_THRESHOLD_WARMUP", "CAUSAL_REGIME_NOT_ELIGIBLE"
        ):
            stop(f"rejected breakout has unexpected reason: {key}")
    return ({"raw_crossings": len(expected), "exact_source_identity_reconciliation": True,
             "independently_rebuilt_interval_clusters": len(set(v[0] for v in cluster_by_key.values())),
             "cluster_counts_by_asset": dict(summary)}, observed)


def verify_failed_breakouts(root: Path, rows: list[dict[str, str]], breakout_rows: dict[str, dict[str, str]]) -> dict:
    source = read_rows(root / "reports/phase3_breakout_lifecycle_v1_1/breakout_lifecycle_events_v1_1.csv")
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source:
        key = "|".join((row["asset"], row["direction"],
                        str(integer(row, "signal_time_ms", "Module B event")),
                        str(_iso_ms(row["snapshot"]))))
        grouped[key].append(row)
    if len(grouped) != EXPECTED["failed_breakout"]:
        stop(f"Module B physical source events={len(grouped)}")
    observed = {}
    for row in rows:
        key = row.get("source_event_key", "")
        if not key or key in observed:
            stop("blank or duplicate failed-breakout source_event_key")
        observed[key] = row
    if set(grouped) != set(observed):
        stop(f"failed-breakout exact source reconciliation failed source={len(grouped)} output={len(observed)}")

    for key, members in grouped.items():
        row = observed[key]
        definitions = {member["definition"] for member in members}
        if "BROAD_P40" not in definitions or not definitions.issubset({"BROAD_P40", "STRICT_P25"}):
            stop(f"invalid historical cohort membership at {key}")
        if len(members) not in (1, 2):
            stop(f"invalid cohort collapse cardinality at {key}")
        ids = ";".join(sorted(member["event_id"] for member in members))
        if row.get("source_event_row_ids") != ids:
            stop(f"failed-breakout source-row membership mismatch: {key}")
        if row.get("source_breakout_source_event_id") != key:
            stop(f"failed-breakout does not link to its exact source breakout: {key}")
        source_breakout = breakout_rows.get(key)
        if source_breakout is None:
            stop(f"failed-breakout source is absent from raw breakout disposition: {key}")
        signal = integer(row, "signal_time_ms", "failed-breakout")
        expiry = integer(row, "expiry_ts_ms", "failed-breakout")
        if expiry != signal + HORIZON_MS:
            stop(f"failed-breakout expiry is not exactly +12h: {key}")
        raw_confirmations = {
            integer(member, "first_15m_return_inside_close_ts_ms", "Module B confirmation")
            for member in members if (member.get("first_15m_return_inside_close_ts_ms") or "").strip()
        }
        if len(raw_confirmations) > 1:
            stop(f"cohort rows disagree on return-inside time: {key}")
        confirmation = next(iter(raw_confirmations)) if raw_confirmations else None
        if confirmation is not None and not signal < confirmation < expiry:
            stop(f"confirmation is not strictly inside half-open 12h horizon: {key}")
        complete_values = {member.get("complete_12h", "").lower() == "true" for member in members}
        if len(complete_values) != 1:
            stop(f"cohort rows disagree on 12h completion: {key}")
        complete = next(iter(complete_values))
        status = row.get("confirmation_status", "")
        observed_at = integer(row, "event_observed_at_ts_ms", "failed-breakout")
        if confirmation is None:
            if complete:
                if status != "NOT_CONFIRMED" or observed_at != expiry:
                    stop(f"completed no-confirmation lifecycle mismatch: {key}")
            elif status != "CENSORED" or not signal < observed_at < expiry:
                stop(f"source-end censoring mismatch: {key}")
        else:
            if observed_at != confirmation or status not in ("CONFIRMED", "CENSORED"):
                stop(f"observed return-inside identity mismatch: {key}")
            if status == "CONFIRMED":
                close = (row.get("signal_candle_close_ts_ms") or "").strip()
                if not close or int(close) != confirmation:
                    stop(f"completed 15m confirmation close mismatch: {key}")
            else:
                if (row.get("signal_candle_close_ts_ms") or "").strip():
                    stop(f"incomplete 15m confirmation exposes completed candle: {key}")
        source_ok = source_breakout.get("disposition") == "ELIGIBLE_FOR_FURTHER_VALIDATION"
        disposition = row.get("disposition", "")
        reason = row.get("reason_code", "")
        if not source_ok and (disposition != "REJECTED" or reason != "NO_VALID_SOURCE_BREAKOUT"):
            stop(f"failed-breakout inherits invalid source disposition incorrectly: {key}")
        if disposition == "EXPIRED" and reason != "EXPIRED_NO_RETURN_INSIDE_WITHIN_12H":
            stop(f"expired failed-breakout reason mismatch: {key}")
        if disposition == "CENSORED" and reason not in (
            "SOURCE_END_BEFORE_RESOLUTION", "INCOMPLETE_15M_CONFIRMATION",
            "MISSING_OR_GAPPED_MINUTES"
        ):
            stop(f"censored failed-breakout reason mismatch: {key}")
        if disposition == "ELIGIBLE_FOR_FURTHER_VALIDATION" and reason != "NONE":
            stop(f"eligible failed-breakout has non-NONE reason: {key}")
    return {"physical_source_events": len(grouped), "source_cohort_rows": len(source),
            "exact_source_identity_and_linkage": True,
            "half_open_12h_lifecycle_checks": len(grouped)}


def _iso_ms(value: str) -> int:
    from datetime import datetime, timezone
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        stop(f"invalid Module B snapshot timestamp: {value!r}")
    if parsed.tzinfo is None:
        stop("Module B snapshot timestamp has no timezone")
    return int(parsed.astimezone(timezone.utc).timestamp() * 1000)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    ledgers = disposition_rows(args.audit_dir)
    rejection = verify_rejection_identity(args.repo_root, ledgers["rejection"])
    breakout, breakout_map = verify_breakout_identity(args.repo_root, args.artifact_dir, ledgers["breakout"])
    failed = verify_failed_breakouts(args.repo_root, ledgers["failed_breakout"], breakout_map)
    report = {
        "status": "INDEPENDENT_SOURCE_IDENTITY_AND_LIFECYCLE_PASS",
        "method": "separate standard-library implementation; no imports from canonical contract or primary source audit",
        "rejection": rejection,
        "breakout": breakout,
        "failed_breakout": failed,
        "scope": "independent source identity, cohort membership, breakout overlap components, source linkage, and half-open failed-breakout lifecycle; not final G0-05 gate approval",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
