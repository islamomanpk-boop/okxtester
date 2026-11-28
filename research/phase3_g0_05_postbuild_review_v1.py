#!/usr/bin/env python3
"""Independent read-only post-build review of the real G0-05 canonical ledger."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

RULE = "G0_05_CANDIDATE_RULE_V1"
EXPECTED_FIELDS = frozenset("""
candidate_id source_event_id source_event_row_ids family instrument_id asset side
boundary_side regime_definition_version candidate_rule_version source_pipeline_version
historical_cohort_memberships causal_cohort_label overlap_cluster_id overlap_cluster_size
overlap_window_start_ts_ms overlap_window_end_ts_ms repeated_signal_group_id snapshot_id
snapshot_available_at_ts_ms snapshot_valid_from_ts_ms snapshot_valid_until_ts_ms
frozen_upper_boundary frozen_lower_boundary channel_width_pct threshold_policy_id
threshold_population_id threshold_value threshold_percentile threshold_calibration_start_ts_ms
threshold_calibration_end_ts_ms threshold_prior_observation_count efficiency_value
efficiency_limit overlap_value overlap_minimum source_file_paths source_git_blob_ids
source_sha256_manifest_id signal_candle_open_ts_ms signal_candle_close_ts_ms
signal_available_at_ts_ms confirmation_rule_id confirmation_bar_interval_ms
confirmation_status first_eligible_execution_bar_open_ts_ms event_observed_at_ts_ms
ambiguity_flags decluster_policy_id candidate_status exclusion_reason censoring_reason
invalidation_reference_type invalidation_reference_value invalidation_reference_ts_ms
expiry_rule_id expiry_ts_ms source_breakout_candidate_id source_reconciliation_status
source_join_cardinality
""".split())
EXPECTED_FAMILY_COUNTS = {
    "SUPPORT_REJECTION": 558,
    "RESISTANCE_REJECTION": 596,
    "BREAKOUT_CONTINUATION": 2861,
    "FAILED_BREAKOUT_REVERSAL": 932,
}
EXPECTED_DISPOSITIONS = {
    "ELIGIBLE_FOR_FURTHER_VALIDATION": 2856,
    "REJECTED": 1884,
    "EXPIRED": 207,
    "CENSORED": 0,
}
INHERITED_FIELDS = (
    "asset", "instrument_id", "boundary_side", "regime_definition_version",
    "source_pipeline_version", "historical_cohort_memberships", "causal_cohort_label",
    "snapshot_id", "snapshot_available_at_ts_ms", "snapshot_valid_from_ts_ms",
    "snapshot_valid_until_ts_ms", "frozen_upper_boundary", "frozen_lower_boundary",
    "channel_width_pct", "threshold_policy_id", "threshold_population_id",
    "threshold_value", "threshold_percentile", "threshold_calibration_start_ts_ms",
    "threshold_calibration_end_ts_ms", "threshold_prior_observation_count",
    "efficiency_value", "efficiency_limit", "overlap_value", "overlap_minimum",
    "source_sha256_manifest_id", "repeated_signal_group_id", "overlap_cluster_id",
    "overlap_cluster_size", "overlap_window_start_ts_ms", "overlap_window_end_ts_ms",
)


def stop(message: str) -> None:
    raise SystemExit(f"G0-05 POST-BUILD REVIEW FAILED: {message}")


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def deterministic_id(source_identity: str, family: str, rule: str) -> str:
    payload = "\x1f".join((source_identity, family, rule)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_source_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        stop(f"missing source ledger {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            stop(f"missing CSV header {path}")
        return list(reader)


def split_semicolon(value: str | None) -> list[str]:
    if value is None or value.strip() == "":
        return []
    return [part for part in value.split(";") if part != ""]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.evidence_dir
    canonical = root / "canonical"

    source_report = json.loads((root / "source_audit_report.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "independent_source_verification.json").read_text(encoding="utf-8"))
    source_manifest = json.loads((root / "source_manifest.json").read_text(encoding="utf-8"))
    build_report = json.loads((canonical / "g0_05_canonical_build_report.json").read_text(encoding="utf-8"))

    if source_report.get("status") != "G0_05_SOURCE_PROVENANCE_AND_IDENTITY_AUDIT_PASS":
        stop("primary source audit status is not PASS")
    if independent.get("status") != "INDEPENDENT_SOURCE_IDENTITY_AND_LIFECYCLE_PASS":
        stop("independent source verification status is not PASS")
    if build_report.get("status") != "G0_05_REAL_CANONICAL_CANDIDATE_LEDGER_BUILD_AND_VALIDATION_PASS":
        stop("canonical build report status is not PASS")
    manifest_id = hashlib.sha256(
        (json.dumps(source_manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    ).hexdigest()
    if manifest_id != source_report.get("source_sha256_manifest_id") or manifest_id != build_report.get("source_manifest_id"):
        stop("source manifest ID does not reconcile across reports")

    jsonl_path = canonical / "g0_05_canonical_candidate_ledger.jsonl"
    csv_path = canonical / "g0_05_canonical_candidate_ledger.csv"
    for path in (jsonl_path, csv_path):
        expected_hash = build_report.get("outputs", {}).get(path.name, {}).get("sha256")
        if not expected_hash or digest_file(path) != expected_hash:
            stop(f"canonical output SHA-256 mismatch: {path.name}")

    records = []
    with jsonl_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                stop(f"invalid JSONL at line {line_number}: {exc}")
    if len(records) != 4947:
        stop(f"canonical JSONL row count {len(records)} != 4947")
    if len(EXPECTED_FIELDS) != 60:
        stop("independent reviewer field list is not exactly 60 fields")

    candidate_ids = set()
    family_source_ids = set()
    family_counts = Counter()
    dispositions = Counter()
    by_id = {}
    previous_key = None
    for index, row in enumerate(records, 1):
        if set(row) != EXPECTED_FIELDS or len(row) != 60:
            stop(f"row {index} does not contain exactly the independent 60-field schema")
        family = row["family"]
        source_identity = row["source_event_id"]
        if row["candidate_rule_version"] != RULE:
            stop(f"row {index} candidate rule version mismatch")
        expected_id = deterministic_id(source_identity, family, RULE)
        if row["candidate_id"] != expected_id:
            stop(f"row {index} deterministic candidate ID mismatch")
        if expected_id in candidate_ids or (family, source_identity) in family_source_ids:
            stop(f"duplicate candidate/source identity at row {index}")
        candidate_ids.add(expected_id)
        family_source_ids.add((family, source_identity))
        by_id[expected_id] = row
        family_counts[family] += 1
        dispositions[row["candidate_status"]] += 1
        key = (family, row["candidate_id"])
        if previous_key is not None and key < previous_key:
            stop("canonical JSONL order is not deterministic")
        previous_key = key
        if row["source_sha256_manifest_id"] != manifest_id:
            stop(f"row {index} source manifest ID mismatch")

    if dict(family_counts) != EXPECTED_FAMILY_COUNTS:
        stop(f"family counts mismatch: {dict(family_counts)}")
    disposition_result = {key: dispositions.get(key, 0) for key in EXPECTED_DISPOSITIONS}
    if disposition_result != EXPECTED_DISPOSITIONS:
        stop(f"aggregate dispositions mismatch: {disposition_result}")

    # Compare the CSV export byte-semantically at each field to the canonical JSONL values.
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != EXPECTED_FIELDS:
            stop("CSV export header does not match the 60-field schema")
        csv_rows = list(reader)
    if len(csv_rows) != len(records):
        stop("CSV and JSONL record counts differ")
    for index, (csv_row, record) in enumerate(zip(csv_rows, records), 1):
        for field, value in record.items():
            expected_cell = (
                json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                if isinstance(value, (list, dict)) else
                "" if value is None else str(value)
            )
            if csv_row[field] != expected_cell:
                stop(f"CSV/JSONL mismatch at row {index}, field {field}")

    rejection = read_source_csv(root / "rejection_source_dispositions.csv")
    breakout = read_source_csv(root / "breakout_source_dispositions.csv")
    failed = read_source_csv(root / "failed_breakout_source_dispositions.csv")
    if (len(rejection), len(breakout), len(failed)) != (1154, 2861, 932):
        stop("source-only ledger row counts differ from frozen population")

    expected_pairs = set()
    source_to_breakout_id = {}
    source_status_counts = Counter()
    for source in rejection + breakout:
        family = source["family"]
        identity = source["source_event_id"]
        candidate = deterministic_id(identity, family, RULE)
        expected_pairs.add((family, identity, candidate))
        source_status_counts[source["disposition"]] += 1
        if family == "BREAKOUT_CONTINUATION":
            if identity in source_to_breakout_id:
                stop("duplicate source breakout identity in source-only ledger")
            source_to_breakout_id[identity] = candidate

    failed_link_count = 0
    for source in failed:
        source_breakout_identity = source["source_breakout_source_event_id"]
        linked_candidate = source_to_breakout_id.get(source_breakout_identity)
        if linked_candidate is None:
            stop("failed-breakout source row has no exact source breakout identity")
        confirmation = source.get("signal_available_at_ts_ms", "").strip()
        if not confirmation:
            if (source.get("confirmation_status") == "CENSORED"
                    and source.get("reason_code") == "INCOMPLETE_15M_CONFIRMATION"):
                confirmation = str(int(source["event_observed_at_ts_ms"]))
            else:
                confirmation = "NO_CONFIRMATION"
        identity = f"{linked_candidate}|{confirmation}|{RULE}"
        family = source["family"]
        candidate = deterministic_id(identity, family, RULE)
        expected_pairs.add((family, identity, candidate))
        source_status_counts[source["disposition"]] += 1
        canonical_row = by_id.get(candidate)
        if canonical_row is None:
            stop("failed-breakout candidate ID missing from canonical ledger")
        if canonical_row["source_breakout_candidate_id"] != linked_candidate:
            stop("failed-breakout candidate links to the wrong source breakout candidate")
        source_breakout_row = by_id.get(linked_candidate)
        if source_breakout_row is None or source_breakout_row["family"] != "BREAKOUT_CONTINUATION":
            stop("failed-breakout link does not resolve to a breakout continuation row")
        for field in INHERITED_FIELDS:
            if canonical_row[field] != source_breakout_row[field]:
                stop(f"failed-breakout source inheritance mismatch: {field}")
        if canonical_row["expiry_ts_ms"] != source_breakout_row["signal_available_at_ts_ms"] + 43200000:
            stop("failed-breakout expiry differs from linked source breakout +12h")
        if canonical_row["confirmation_status"] == "CONFIRMED":
            available = canonical_row["signal_available_at_ts_ms"]
            expiry = canonical_row["expiry_ts_ms"]
            source_available = source_breakout_row["signal_available_at_ts_ms"]
            if not source_available < available < expiry:
                stop("failed-breakout confirmation is not strictly inside the half-open 12h window")
        failed_link_count += 1

    observed_pairs = {
        (row["family"], row["source_event_id"], row["candidate_id"])
        for row in records
    }
    if expected_pairs != observed_pairs or len(expected_pairs) != 4947:
        stop("source-to-canonical exact-once identity reconciliation failed")
    if failed_link_count != 932:
        stop(f"failed-breakout links validated {failed_link_count} != 932")
    source_dispositions = {key: source_status_counts.get(key, 0) for key in EXPECTED_DISPOSITIONS}
    if source_dispositions != disposition_result:
        stop("source-only and canonical disposition counts do not reconcile")

    result = {
        "status": "G0_05_POST_BUILD_EVIDENCE_REVIEW_PASS",
        "canonical_rows": len(records),
        "canonical_fields_per_row": 60,
        "canonical_field_schema_exact": True,
        "jsonl_csv_semantic_equivalence": True,
        "canonical_output_hashes_reverified": True,
        "source_manifest_identity_reverified": True,
        "source_to_canonical_exact_once_reconciliation": True,
        "candidate_ids_recomputed_independently": True,
        "failed_breakout_source_links_and_inheritance": failed_link_count,
        "family_counts": dict(sorted(family_counts.items())),
        "aggregate_dispositions": disposition_result,
        "source_manifest_id": manifest_id,
    }
    output = canonical / "g0_05_postbuild_review_report.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["status"])
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
