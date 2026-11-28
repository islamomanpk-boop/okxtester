#!/usr/bin/env python3
"""Build and validate the owner-authorized real G0-05 canonical candidate ledger."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from phase3_g0_05_candidate_contract_v1 import (
    CANONICAL_REQUIRED_FIELDS,
    serialize_source_disposition_ledgers,
    validate_canonical_candidate_ledger,
)

AUTHORIZATION_RECORD = "OWNER_APPROVED_2026-11-28"
EXPECTED_ROWS = {
    "rejection_source_dispositions.csv": 1154,
    "breakout_source_dispositions.csv": 2861,
    "failed_breakout_source_dispositions.csv": 932,
}
EXPECTED_REJECTION_DISPOSITIONS = {
    "ELIGIBLE_FOR_FURTHER_VALIDATION": 1083, "REJECTED": 31, "EXPIRED": 40, "CENSORED": 0
}
EXPECTED_DISPOSITIONS = {
    "BREAKOUT_CONTINUATION": {
        "ELIGIBLE_FOR_FURTHER_VALIDATION": 1038, "REJECTED": 1823, "EXPIRED": 0, "CENSORED": 0
    },
    "FAILED_BREAKOUT_REVERSAL": {
        "ELIGIBLE_FOR_FURTHER_VALIDATION": 735, "REJECTED": 30, "EXPIRED": 167, "CENSORED": 0
    },
}
EXPECTED_FAMILY_TOTALS = {
    "BREAKOUT_CONTINUATION": 2861,
    "FAILED_BREAKOUT_REVERSAL": 932,
}
EXPECTED_TOTAL_ROWS = 4947
EXPECTED_TOTAL_DISPOSITIONS = {
    "ELIGIBLE_FOR_FURTHER_VALIDATION": 2856,
    "REJECTED": 1884,
    "EXPIRED": 207,
    "CENSORED": 0,
}


def stop(message: str) -> None:
    raise SystemExit(f"G0-05 CANONICAL BUILD BLOCKED: {message}")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        stop(f"missing source disposition file: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            stop(f"source disposition file has no header: {path}")
        rows = list(reader)
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_canonical_csv(path: Path, records: list[dict]) -> None:
    fields = list(records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow({
                key: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                if isinstance(value, (list, dict)) else
                "" if value is None else value
                for key, value in record.items()
            })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--authorization-record", required=True)
    args = parser.parse_args()

    if args.authorization_record != AUTHORIZATION_RECORD:
        stop("explicit owner authorization record is missing or does not match")
    report_path = args.audit_dir / "source_audit_report.json"
    manifest_path = args.audit_dir / "source_manifest.json"
    if not report_path.is_file() or not manifest_path.is_file():
        stop("source audit report or complete source manifest is missing")
    source_report = json.loads(report_path.read_text(encoding="utf-8"))
    source_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if source_report.get("status") != "G0_05_SOURCE_PROVENANCE_AND_IDENTITY_AUDIT_PASS":
        stop("primary source provenance/identity audit did not pass")
    source_manifest_id = source_report.get("source_sha256_manifest_id")
    calculated_manifest_id = hashlib.sha256(
        (json.dumps(source_manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    ).hexdigest()
    if source_manifest_id != calculated_manifest_id:
        stop("source manifest identity does not match the primary audit report")

    inputs = {}
    input_hashes = {}
    for filename, expected_rows in EXPECTED_ROWS.items():
        path = args.audit_dir / filename
        rows = read_csv(path)
        if len(rows) != expected_rows:
            stop(f"{filename} row count {len(rows)} != expected {expected_rows}")
        for index, row in enumerate(rows):
            if row.get("source_sha256_manifest_id") != source_manifest_id:
                stop(f"{filename} row {index + 1} carries a different source manifest ID")
        inputs[filename] = rows
        input_hashes[filename] = sha256_file(path)

    rejection_rows = inputs["rejection_source_dispositions.csv"]
    breakout_rows = inputs["breakout_source_dispositions.csv"]
    failed_rows = inputs["failed_breakout_source_dispositions.csv"]

    # The frozen source audit has one rejection family per side; keep both explicit.
    rejection_families = Counter(row.get("family", "") for row in rejection_rows)
    if set(rejection_families) != {"SUPPORT_REJECTION", "RESISTANCE_REJECTION"}:
        stop(f"unexpected rejection families: {dict(rejection_families)}")

    source_family_counts = Counter()
    source_dispositions = defaultdict(Counter)
    for row in rejection_rows + breakout_rows + failed_rows:
        family = row.get("family", "")
        status = row.get("disposition", "")
        source_family_counts[family] += 1
        source_dispositions[family][status] += 1

    rejection_aggregate = Counter()
    for family in ("SUPPORT_REJECTION", "RESISTANCE_REJECTION"):
        rejection_aggregate.update(source_dispositions[family])
    rejection_actual = {status: rejection_aggregate.get(status, 0)
                        for status in ("ELIGIBLE_FOR_FURTHER_VALIDATION", "REJECTED", "EXPIRED", "CENSORED")}
    if rejection_actual != EXPECTED_REJECTION_DISPOSITIONS:
        stop(f"rejection source disposition counts mismatch: {rejection_actual} != {EXPECTED_REJECTION_DISPOSITIONS}")
    for family, expected in EXPECTED_DISPOSITIONS.items():
        actual = {status: source_dispositions[family].get(status, 0)
                  for status in ("ELIGIBLE_FOR_FURTHER_VALIDATION", "REJECTED", "EXPIRED", "CENSORED")}
        if actual != expected:
            stop(f"{family} source disposition counts mismatch: {actual} != {expected}")
    if source_family_counts["BREAKOUT_CONTINUATION"] != EXPECTED_FAMILY_TOTALS["BREAKOUT_CONTINUATION"]:
        stop("breakout family total differs from frozen reconciliation")
    if source_family_counts["FAILED_BREAKOUT_REVERSAL"] != EXPECTED_FAMILY_TOTALS["FAILED_BREAKOUT_REVERSAL"]:
        stop("failed-breakout family total differs from frozen reconciliation")
    if sum(source_family_counts.values()) != EXPECTED_TOTAL_ROWS:
        stop(f"source disposition total mismatch: {sum(source_family_counts.values())}")
    aggregate = Counter()
    for counts in source_dispositions.values():
        aggregate.update(counts)
    aggregate_expected = {status: aggregate.get(status, 0)
                          for status in EXPECTED_TOTAL_DISPOSITIONS}
    if aggregate_expected != EXPECTED_TOTAL_DISPOSITIONS:
        stop(f"aggregate disposition totals mismatch: {aggregate_expected}")

    # Serializer creates deterministic IDs and failed-breakout -> breakout candidate links.
    records = serialize_source_disposition_ledgers(rejection_rows, breakout_rows, failed_rows)
    if len(records) != EXPECTED_TOTAL_ROWS:
        stop(f"canonical record count {len(records)} != {EXPECTED_TOTAL_ROWS}")
    if set(records[0]) != set(CANONICAL_REQUIRED_FIELDS) or len(records[0]) != 60:
        stop("canonical serializer did not emit exactly the 60 required fields")
    if any(set(row) != set(CANONICAL_REQUIRED_FIELDS) or len(row) != 60 for row in records):
        stop("one or more canonical records do not contain exactly 60 required fields")

    ledger_validation = validate_canonical_candidate_ledger(records)
    canonical_family_counts = Counter(row["family"] for row in records)
    canonical_dispositions = defaultdict(Counter)
    for row in records:
        canonical_dispositions[row["family"]][row["candidate_status"]] += 1
    if canonical_family_counts["SUPPORT_REJECTION"] != rejection_families["SUPPORT_REJECTION"]:
        stop("support rejection candidate count changed during serialization")
    if canonical_family_counts["RESISTANCE_REJECTION"] != rejection_families["RESISTANCE_REJECTION"]:
        stop("resistance rejection candidate count changed during serialization")
    if canonical_family_counts["BREAKOUT_CONTINUATION"] != 2861:
        stop("breakout canonical candidate count mismatch")
    if canonical_family_counts["FAILED_BREAKOUT_REVERSAL"] != 932:
        stop("failed-breakout canonical candidate count mismatch")
    for family, counts in source_dispositions.items():
        if canonical_dispositions[family] != counts:
            stop(f"canonical disposition counts changed for {family}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.output_dir / "g0_05_canonical_candidate_ledger.jsonl"
    with jsonl_path.open("w", encoding="utf-8", newline="") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    csv_path = args.output_dir / "g0_05_canonical_candidate_ledger.csv"
    write_canonical_csv(csv_path, records)

    family_dispositions = {
        family: {status: counts.get(status, 0) for status in
                 ("ELIGIBLE_FOR_FURTHER_VALIDATION", "REJECTED", "EXPIRED", "CENSORED")}
        for family, counts in sorted(canonical_dispositions.items())
    }
    total_dispositions = {
        status: sum(counts.get(status, 0) for counts in canonical_dispositions.values())
        for status in ("ELIGIBLE_FOR_FURTHER_VALIDATION", "REJECTED", "EXPIRED", "CENSORED")
    }
    result = {
        "status": "G0_05_REAL_CANONICAL_CANDIDATE_LEDGER_BUILD_AND_VALIDATION_PASS",
        "authorization_record": args.authorization_record,
        "candidate_rule_version": ledger_validation["candidate_rule_version"],
        "canonical_candidate_generation_authorized": True,
        "scope": "real canonical G0-05 point-event disposition ledger only; no orders, fills, execution simulation, PnL, strategy selection or live trading",
        "source_manifest_id": source_manifest_id,
        "source_audit_status": source_report["status"],
        "source_disposition_input_sha256": input_hashes,
        "canonical_required_field_count": len(CANONICAL_REQUIRED_FIELDS),
        "canonical_rows": len(records),
        "family_counts": dict(sorted(canonical_family_counts.items())),
        "dispositions_by_family": family_dispositions,
        "aggregate_dispositions": total_dispositions,
        "ledger_validation": ledger_validation,
        "failed_breakout_source_links": ledger_validation["failed_breakout_source_links_validated"],
        "outputs": {
            jsonl_path.name: {"sha256": sha256_file(jsonl_path), "bytes": jsonl_path.stat().st_size},
            csv_path.name: {"sha256": sha256_file(csv_path), "bytes": csv_path.stat().st_size},
        },
    }
    (args.output_dir / "g0_05_canonical_build_report.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["status"])
    print(json.dumps({
        "canonical_rows": result["canonical_rows"],
        "family_counts": result["family_counts"],
        "aggregate_dispositions": result["aggregate_dispositions"],
        "failed_breakout_source_links": result["failed_breakout_source_links"],
        "jsonl_sha256": result["outputs"][jsonl_path.name]["sha256"],
        "csv_sha256": result["outputs"][csv_path.name]["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
