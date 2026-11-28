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
from bisect import bisect_left
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
        numeric = float(value)
        if not numeric.is_integer():
            raise ValueError("not an exact integer")
        number = int(numeric)
    except (KeyError, TypeError, ValueError, OverflowError):
        stop(f"{label}: invalid exact-integer field {field}")
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



def load_thresholds(artifact: Path) -> dict[tuple[str, int], dict[str, str]]:
    rows = read_rows(artifact / "causal_thresholds_by_context.csv")
    result = {}
    for row in rows:
        if row.get("policy") != "EXPANDING_PRIOR" or row.get("population") != "UNIQUE_4H_FEATURE_ROWS":
            continue
        key = (row["asset"], integer(row, "snapshot_ms", "threshold"))
        if key in result:
            stop(f"duplicate primary causal threshold: {key}")
        p25, p40 = float(row["p25"]), float(row["p40"])
        if p25 > p40:
            stop(f"causal P25 exceeds P40: {key}")
        result[key] = row
    return result


def causal_label(asset: str, snapshot: int, width: float, efficiency: float,
                 overlap: float, thresholds: dict) -> str:
    threshold = thresholds.get((asset, snapshot))
    if threshold is None:
        return "CAUSAL_THRESHOLD_WARMUP"
    strict = width <= float(threshold["p25"]) and efficiency <= 0.30 and overlap >= 0.70
    broad = width <= float(threshold["p40"]) and efficiency <= 0.30 and overlap >= 0.70
    if strict:
        return "CAUSAL_STRICT"
    if broad:
        return "CAUSAL_BROAD_ONLY"
    return "CAUSAL_REGIME_NOT_ELIGIBLE"


def verify_rejection_identity(root: Path, artifact: Path, rows: list[dict[str, str]]) -> dict:
    source = read_rows(root / "reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv")
    physical: dict[str, list[str]] = defaultdict(list)
    source_rows_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
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
        source_rows_by_key[key].append(row)
    if len(physical) != EXPECTED["rejection"]:
        stop(f"reconstructed physical rejection identities={len(physical)}")
    thresholds = load_thresholds(artifact)
    feature_by_asset = {asset: read_rows(root / "reports/sideways_detector_original_v1" / f"{asset}_features_original_v1.csv") for asset in ASSETS}
    observed = {}
    for row in rows:
        key = row.get("source_event_id", "")
        if not key or key in observed:
            stop("blank or duplicate canonical rejection source_event_id")
        observed[key] = row
    if set(observed) != set(physical):
        stop(f"rejection physical-key mismatch source={len(physical)} output={len(observed)}")
    for key, ids in physical.items():
        row = observed[key]
        expected_ids = ";".join(sorted(ids))
        if observed[key].get("source_event_row_ids") != expected_ids:
            stop(f"rejection source-row membership mismatch: {key}")
        status = observed[key].get("disposition")
        reason = observed[key].get("reason_code")
        if status == "ELIGIBLE_FOR_FURTHER_VALIDATION" and reason != "NONE":
            stop(f"eligible rejection has non-NONE reason: {key}")
        members = source_rows_by_key[key]
        broad = next((member for member in members if member["definition"].lower() == "broad"), None)
        if broad is None:
            stop(f"rejection physical event lacks broad source membership: {key}")
        asset = broad["asset"]
        index = integer(broad, "snapshot_index", "rejection source")
        if index >= len(feature_by_asset[asset]):
            stop(f"rejection feature index out of range: {key}")
        feature = feature_by_asset[asset][index]
        snapshot = integer(broad, "snapshot_available_at_ts_ms", "rejection source")
        if integer(feature, "available_at_ts_ms", "detector feature") != snapshot:
            stop(f"rejection feature snapshot mismatch: {key}")
        next_snapshot = integer(broad, "snapshot_next_available_at_ts_ms", "rejection source")
        confirmation = integer(broad, "first_strong_rejection_ts_ms", "rejection source") + 900_000
        label = causal_label(asset, snapshot, float(feature["channel_width_pct"]),
                             float(feature["directional_efficiency"]), float(feature["mean_overlap"]), thresholds)
        if confirmation >= next_snapshot:
            expected_status, expected_reason, expected_cohort = "EXPIRED", "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION", "NOT_EVALUATED"
        elif label == "CAUSAL_THRESHOLD_WARMUP":
            expected_status, expected_reason, expected_cohort = "REJECTED", label, "WARMUP"
        elif label == "CAUSAL_REGIME_NOT_ELIGIBLE":
            expected_status, expected_reason, expected_cohort = "REJECTED", label, "NOT_ELIGIBLE"
        else:
            expected_status, expected_reason = "ELIGIBLE_FOR_FURTHER_VALIDATION", "NONE"
            expected_cohort = label
        if status not in (expected_status, "CENSORED" if expected_status == "ELIGIBLE_FOR_FURTHER_VALIDATION" else expected_status):
            stop(f"independently recomputed rejection disposition mismatch: {key}")
        if reason != expected_reason or row.get("causal_cohort") != expected_cohort:
            policy_population_counts = Counter((item.get("policy", ""), item.get("population", "")) for item in read_rows(artifact / "causal_thresholds_by_context.csv"))
            nearby = sorted((abs(k[1] - snapshot), k[1]) for k in thresholds if k[0] == asset)[:3]
            stop(f"independent rejection mismatch {key}; expected=({expected_status},{expected_reason},{expected_cohort}); actual=({status},{reason},{row.get('causal_cohort')}); threshold={thresholds.get((asset, snapshot)) is not None}; nearby_thresholds={nearby}; policy_population_counts={dict(policy_population_counts)}; snapshot={snapshot}; output_snapshot={row.get('snapshot_available_at_ts_ms')}; output_threshold=({row.get('threshold_value')},{row.get('threshold_percentile')},{row.get('threshold_prior_observation_count')},{row.get('threshold_calibration_start_ts_ms')},{row.get('threshold_calibration_end_ts_ms')})")
        if expected_status != "ELIGIBLE_FOR_FURTHER_VALIDATION" and (row.get("first_eligible_1m_open_ts_ms") or "").strip():
            stop(f"non-eligible rejection exposes first eligible minute: {key}")
    return {"physical_events": len(physical), "source_memberships": sum(map(len, physical.values())),
            "causal_dispositions": dict(Counter(f"{item.get('causal_cohort')}|{item.get('disposition')}|{item.get('reason_code')}" for item in observed.values())),
            "exact_source_identity_and_membership": True}


def verify_breakout_identity(root: Path, artifact: Path, rows: list[dict[str, str]]) -> tuple[dict, dict]:
    raw = read_rows(artifact / "unique_raw_crossing_events_with_six_variants.csv")
    thresholds = load_thresholds(artifact)
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

    # Load only timestamps, not full OHLC dictionaries, and independently
    # reconstruct each source event's observed 1m horizon.
    minute_stamps = {}
    for asset in ASSETS:
        path = root / "data/market_1m" / f"{asset}_USDT_USDT_1m.csv"
        if not path.is_file():
            stop(f"missing raw 1m source: {path}")
        stamps = []
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                stamps.append(int(row["ts"]))
        if any(b <= a for a, b in zip(stamps, stamps[1:])):
            stop(f"{asset} raw 1m timestamps are not strictly increasing")
        minute_stamps[asset] = stamps

    # Independently reconstruct connected components of overlapping, half-open
    # observed 1m intervals; no production clustering helper is used.
    grouped: dict[str, list[tuple[int, int, str]]] = defaultdict(list)
    for key, source in expected.items():
        asset = source["asset"]
        start = integer(source, "signal_time_ms", "G0-04 raw")
        stamps = minute_stamps[asset]
        index = bisect_left(stamps, start)
        if index >= len(stamps) or stamps[index] != start:
            stop(f"raw 1m source lacks exact event-start minute: {key}")
        observed_bars = 0
        for stamp in stamps[index:index + 720]:
            if stamp != start + observed_bars * MINUTE_MS:
                break
            observed_bars += 1
        if not 0 < observed_bars <= 720:
            stop(f"invalid observed 12-hour window: {key}")
        if key in observed_by_key and observed_by_key[key] != observed_bars:
            stop(f"independent observed window differs from Module B: {key}")
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
        source = expected[key]
        asset = source["asset"]
        snapshot = integer(source, "context_snapshot_ms", "G0-04 raw")
        tag = "EXPANDING_PRIOR__UNIQUE_4H_FEATURE_ROWS"
        threshold = thresholds.get((asset, snapshot))
        if threshold is None:
            label = "CAUSAL_THRESHOLD_WARMUP"
            strict_expected = False
            broad_expected = False
        else:
            width = float(source["channel_width_pct"])
            efficiency = float(source["efficiency"])
            overlap = float(source["overlap"])
            label = causal_label(asset, snapshot, width, efficiency, overlap, thresholds)
            strict_expected = (width <= float(threshold["p25"])
                               and efficiency <= 0.30 and overlap >= 0.70)
            broad_expected = (width <= float(threshold["p40"])
                              and efficiency <= 0.30 and overlap >= 0.70)
        if (source[tag + "__strict"].lower() == "true") != strict_expected:
            stop(f"independent P25 eligibility recomputation mismatch: {key}")
        if (source[tag + "__broad"].lower() == "true") != broad_expected:
            stop(f"independent P40 eligibility recomputation mismatch: {key}")
        expected_status = "ELIGIBLE_FOR_FURTHER_VALIDATION" if label in ("CAUSAL_STRICT", "CAUSAL_BROAD_ONLY") else "REJECTED"
        expected_reason = "NONE" if expected_status == "ELIGIBLE_FOR_FURTHER_VALIDATION" else label
        if status != expected_status or reason != expected_reason or row.get("causal_cohort") != label:
            stop(f"independent breakout disposition recomputation mismatch: {key}")
        expected_minute = str(integer(source, "signal_time_ms", "G0-04 raw")) if expected_status == "ELIGIBLE_FOR_FURTHER_VALIDATION" else ""
        if (row.get("first_eligible_1m_open_ts_ms") or "") != expected_minute:
            stop(f"breakout first-eligible minute mismatch: {key}")
    return ({"raw_crossings": len(expected), "exact_source_identity_reconciliation": True,
             "causal_dispositions": dict(Counter(f"{item.get('causal_cohort')}|{item.get('disposition')}|{item.get('reason_code')}" for item in observed.values())),
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

    endpoint_exclusions = 0
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
        raw_confirmation = next(iter(raw_confirmations)) if raw_confirmations else None
        if raw_confirmation is not None and not signal < raw_confirmation <= expiry:
            stop(f"observed return-inside time is outside the 12h lifecycle: {key}")
        confirmation = raw_confirmation
        if confirmation == expiry:
            # The event was observed, but the exact right endpoint is excluded
            # from canonical confirmation by the half-open lifecycle rule.
            endpoint_exclusions += 1
            confirmation = None
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
    if endpoint_exclusions != 1:
        stop(f"expected one exact-12h endpoint exclusion, observed {endpoint_exclusions}")
    return {"physical_source_events": len(grouped), "source_cohort_rows": len(source),
            "exact_source_identity_and_linkage": True,
            "half_open_12h_lifecycle_checks": len(grouped),
            "exact_12h_endpoint_observations_excluded": endpoint_exclusions}


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
    rejection = verify_rejection_identity(args.repo_root, args.artifact_dir, ledgers["rejection"])
    breakout, breakout_map = verify_breakout_identity(args.repo_root, args.artifact_dir, ledgers["breakout"])
    failed = verify_failed_breakouts(args.repo_root, ledgers["failed_breakout"], breakout_map)
    report = {
        "status": "INDEPENDENT_SOURCE_IDENTITY_AND_LIFECYCLE_PASS",
        "method": "separate standard-library implementation; no imports from canonical contract or primary source audit",
        "rejection": rejection,
        "breakout": breakout,
        "failed_breakout": failed,
        "scope": "independent source identity, causal cohort/disposition recomputation, breakout overlap components, source linkage, and half-open failed-breakout lifecycle; not final G0-05 gate approval",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
