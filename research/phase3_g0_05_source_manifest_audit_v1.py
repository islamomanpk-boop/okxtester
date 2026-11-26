#!/usr/bin/env python3
"""Read-only G0-05 source provenance and identity reconciliation; emits no candidates."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_BLOBS = {
    "reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv": "2af6f85cd60194019f903a17f16216841ae61f8c",
    "reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv": "c58de65ec1936607790c2ee40b828897e6f726dc",
    "reports/sideways_detector_original_v1/BTC_features_original_v1.csv": "e422073b993cf5d9d11050216509165277339710",
    "reports/sideways_detector_original_v1/ETH_features_original_v1.csv": "c38641d3846931afd6e44a7f39318251fe3c5653",
    "reports/sideways_detector_original_v1/SOL_features_original_v1.csv": "5ba90a99a33924f3de6bcbe9cd1d76aa0a9dd207",
    "reports/sideways_detector_original_v1/DOGE_features_original_v1.csv": "5fb8cb621628e069b1e2500f8047eb908b031909",
    "reports/sideways_detector_original_v1/AVAX_features_original_v1.csv": "06b6f7ee947ef5e62b8cf2b9cc64fb7caaa523e5",
}
ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
G004_REVISION = "86b49598d676b6ab00649bf31d4490ffbb1e608f"
G004_OUTPUTS = (
    "causal_thresholds_by_context.csv",
    "historical_932_identity_reconciliation.csv",
    "context_coverage_and_cross_pipeline_audit.json",
    "historical_baseline_reproduction.csv",
    "input_manifest.csv",
    "raw_crossing_summary.csv",
    "unique_raw_crossing_events_with_six_variants.csv",
)


def fail(message: str) -> None:
    raise RuntimeError("G0-05 SOURCE AUDIT FAIL-CLOSED: " + message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            fail(f"missing CSV header: {path}")
        return list(reader.fieldnames), list(reader)


def require_columns(path: str, fields: list[str], required: set[str]) -> None:
    missing = required - set(fields)
    if missing:
        fail(f"{path} missing columns: {sorted(missing)}")


def ms(value: str, label: str) -> int:
    try:
        n = float(value)
    except (TypeError, ValueError):
        fail(f"{label} is not numeric: {value!r}")
    if not n.is_integer():
        fail(f"{label} is not an exact millisecond value: {value!r}")
    return int(n)


def iso_ms(value: str, label: str) -> int:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        fail(f"{label} is not ISO timestamp: {value!r}")
    if dt.tzinfo is None:
        fail(f"{label} lacks timezone: {value!r}")
    return int(dt.astimezone(timezone.utc).timestamp() * 1000)


def rejection_event_id(row: dict[str, str]) -> str:
    return "|".join((
        row["asset"], row["definition"].lower(), row["direction"].lower(),
        str(int(row["snapshot_index"])), str(int(row["segment_id"])),
        str(int(row["test_rank"])), str(ms(row["test_start_ts_ms"], "test_start_ts_ms")),
    ))


def verify_pinned_sources(root: Path) -> tuple[dict, dict]:
    manifest, loaded = {}, {}
    for relative, expected_blob in EXPECTED_BLOBS.items():
        path = root / relative
        if not path.is_file():
            fail(f"missing pinned source {relative}")
        data = path.read_bytes()
        actual_blob = git_blob_sha1(data)
        if actual_blob != expected_blob:
            fail(f"Git blob mismatch {relative}: {actual_blob} != {expected_blob}")
        fields, rows = read_csv(path)
        manifest[relative] = {
            "git_blob_sha1": actual_blob,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "rows": len(rows),
            "columns": fields,
        }
        loaded[relative] = (fields, rows)
    return manifest, loaded


def audit_rejections(root: Path, loaded: dict) -> dict:
    ledger_path = "reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv"
    anatomy_path = "reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv"
    lf, ledger = loaded[ledger_path]
    af, anatomy = loaded[anatomy_path]
    require_columns(ledger_path, lf, {
        "asset", "definition", "direction", "snapshot_index", "segment_id",
        "test_rank", "test_start_ts_ms", "first_strong_rejection_ts_ms",
        "snapshot_available_at_ts_ms", "snapshot_next_available_at_ts_ms",
    })
    require_columns(anatomy_path, af, {
        "event_id", "confirmation_ts_ms", "upper", "lower",
        "rejection_open", "rejection_high", "rejection_low", "rejection_close",
    })
    if len(ledger) != 2452 or len(anatomy) != 1992:
        fail(f"rejection source row counts differ: ledger={len(ledger)}, anatomy={len(anatomy)}")
    anatomy_by_id = {r["event_id"]: r for r in anatomy}
    if len(anatomy_by_id) != len(anatomy):
        fail("duplicate event_id in rejection anatomy")
    feature_rows = {}
    for asset in ASSETS:
        path = f"reports/sideways_detector_original_v1/{asset}_features_original_v1.csv"
        fields, rows = loaded[path]
        require_columns(path, fields, {"available_at_ts_ms", "upper", "lower", "channel_width_pct",
                                       "directional_efficiency", "mean_overlap"})
        if len(rows) != 2358:
            fail(f"{asset} detector feature row count {len(rows)} != 2358")
        previous = None
        for index, row in enumerate(rows):
            if row.get("asset", asset) != asset:
                fail(f"{asset} feature asset mismatch at row {index}")
            t = ms(row["available_at_ts_ms"], f"{asset} available_at_ts_ms")
            if previous is not None and t <= previous:
                fail(f"{asset} feature availability is duplicate or unordered")
            previous = t
        feature_rows[asset] = rows

    seen, matched, endpoint = set(), 0, Counter()
    by_definition = Counter()
    for row in ledger:
        raw_rejection = (row.get("first_strong_rejection_ts_ms") or "").strip()
        if not raw_rejection:
            continue
        eid = rejection_event_id(row)
        if eid in seen:
            fail(f"duplicate rejection source identity {eid}")
        seen.add(eid)
        a = row["asset"]
        idx = int(row["snapshot_index"])
        features = feature_rows[a]
        if idx < 0 or idx + 1 >= len(features):
            fail(f"{eid}: snapshot index outside feature ledger")
        current, nxt = features[idx], features[idx + 1]
        available = ms(row["snapshot_available_at_ts_ms"], "snapshot availability")
        next_available = ms(row["snapshot_next_available_at_ts_ms"], "next snapshot availability")
        if ms(current["available_at_ts_ms"], "feature availability") != available:
            fail(f"{eid}: feature/snapshot availability mismatch")
        if ms(nxt["available_at_ts_ms"], "next feature availability") != next_available:
            fail(f"{eid}: next feature/snapshot availability mismatch")
        anatomy_row = anatomy_by_id.get(eid)
        if anatomy_row is None:
            fail(f"{eid}: missing anatomy row")
        confirmation = ms(raw_rejection, "rejection candle open") + 900000
        if ms(anatomy_row["confirmation_ts_ms"], "anatomy confirmation") != confirmation:
            fail(f"{eid}: confirmation timestamp mismatch")
        if float(anatomy_row["upper"]) != float(current["upper"]) or float(anatomy_row["lower"]) != float(current["lower"]):
            fail(f"{eid}: frozen boundary mismatch")
        if confirmation == next_available:
            endpoint[row["definition"].lower()] += 1
        elif confirmation > next_available:
            fail(f"{eid}: confirmation occurs after next snapshot availability")
        matched += 1
        by_definition[row["definition"].lower()] += 1
    if seen != set(anatomy_by_id):
        fail(f"rejection identity/anatomy mismatch: source={len(seen)} anatomy={len(anatomy_by_id)}")
    if by_definition != Counter({"broad": 1154, "strict": 838}):
        fail(f"rejection cohort counts differ: {dict(by_definition)}")
    if endpoint != Counter({"broad": 40, "strict": 29}):
        fail(f"snapshot-endpoint exclusion counts differ: {dict(endpoint)}")
    return {
        "boundary_ledger_rows": len(ledger),
        "rejection_rows_with_confirmation": matched,
        "anatomy_rows": len(anatomy),
        "identity_join": "ONE_TO_ONE_PASS",
        "cohort_rows": dict(by_definition),
        "confirmation_at_next_snapshot_endpoint": dict(endpoint),
        "disposition": "PRESERVE_SOURCE_ROWS; EXCLUDE FROM CAUSAL REJECTION ELIGIBILITY",
    }


def audit_g004_artifact(artifact: Path) -> tuple[dict, dict, dict]:
    meta_path = artifact / "run_metadata.json"
    if not meta_path.is_file():
        fail("G0-04 artifact missing run_metadata.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta.get("status") != "DESCRIPTIVE_RECONSTRUCTION_COMPLETE_BASELINE_20_OF_20":
        fail("G0-04 artifact status is not complete")
    if meta.get("code_revision") != G004_REVISION:
        fail("G0-04 artifact code revision mismatch")
    output_hashes = meta.get("output_sha256", {})
    for name in G004_OUTPUTS:
        path = artifact / name
        if not path.is_file():
            fail(f"G0-04 artifact missing member {name}")
        actual = sha256_bytes(path.read_bytes())
        if output_hashes.get(name) != actual:
            fail(f"G0-04 member hash mismatch: {name}")
    _, baseline = read_csv(artifact / "historical_baseline_reproduction.csv")
    if len(baseline) != 20 or any(r["passed"].lower() != "true" for r in baseline):
        fail("G0-04 historical baseline is not 20/20")
    _, raw = read_csv(artifact / "unique_raw_crossing_events_with_six_variants.csv")
    raw_keys = set()
    for row in raw:
        key = (row["asset"], row["direction"], ms(row["signal_time_ms"], "raw signal"),
               ms(row["context_snapshot_ms"], "raw context snapshot"))
        if key in raw_keys:
            fail(f"duplicate G0-04 raw crossing key {key}")
        raw_keys.add(key)
    if len(raw) != 2861:
        fail(f"G0-04 raw crossing count {len(raw)} != 2861")
    if sum(r["was_historical_selected"].lower() == "true" for r in raw) != 932:
        fail("G0-04 raw ledger does not retain 932 historical selected identities")
    _, reconciliation = read_csv(artifact / "historical_932_identity_reconciliation.csv")
    if len(reconciliation) != 120 or sum(int(r["raw_source_mismatch"]) for r in reconciliation) != 0:
        fail("G0-04 historical identity reconciliation failed")
    _, thresholds = read_csv(artifact / "causal_thresholds_by_context.csv")
    if len(thresholds) != 65310:
        fail("G0-04 threshold row count mismatch")
    threshold_by_key = {}
    for row in thresholds:
        key = (row["asset"], ms(row["snapshot_ms"], "threshold snapshot"),
               row["policy"], row["population"])
        if key in threshold_by_key:
            fail(f"duplicate threshold key {key}")
        snapshot = key[1]
        prior_count = int(row["prior_context_count"])
        if prior_count < 180:
            fail(f"threshold row has fewer than 180 prior contexts: {key}")
        if int(row["prior_15m_row_count"]) != prior_count * 16:
            fail(f"threshold prior 15M row count mismatch: {key}")
        if ms(row["last_prior_context_ms"], "last prior context") >= snapshot:
            fail(f"threshold includes current/future context: {key}")
        if ms(row["first_prior_context_ms"], "first prior context") > ms(row["last_prior_context_ms"], "last prior context"):
            fail(f"threshold calibration interval is reversed: {key}")
        if row["policy"] in ("FIXED_180", "ROLLING_180") and prior_count != 180:
            fail(f"fixed/rolling threshold does not use 180 contexts: {key}")
        threshold_by_key[key] = row
        if float(row["p25"]) > float(row["p40"]):
            fail("G0-04 P25 exceeds P40")
    first_threshold_by_asset = {}
    for row in thresholds:
        asset = row["asset"]
        snapshot = ms(row["snapshot_ms"], "threshold snapshot")
        first_threshold_by_asset[asset] = min(snapshot, first_threshold_by_asset.get(asset, snapshot))
    variants = {}
    recomputed = 0
    warmup_by_asset = Counter()
    for policy in ("FIXED_180", "EXPANDING_PRIOR", "ROLLING_180"):
        for population in ("UNIQUE_4H_FEATURE_ROWS", "JOINED_15M_ROWS"):
            tag = policy + "__" + population
            strict_n = broad_n = 0
            for row in raw:
                asset = row["asset"]
                snapshot = ms(row["context_snapshot_ms"], "raw context snapshot")
                signal = ms(row["signal_time_ms"], "raw signal")
                if snapshot > signal:
                    fail(f"raw event uses future context: {asset}/{signal}")
                threshold = threshold_by_key.get((asset, snapshot, policy, population))
                if threshold is None:
                    continue
                width, efficiency, overlap_value = (float(row[k]) for k in
                    ("channel_width_pct", "efficiency", "overlap"))
                strict_expected = (width <= float(threshold["p25"]) and
                                   efficiency <= 0.30 and overlap_value >= 0.70)
                broad_expected = (width <= float(threshold["p40"]) and
                                  efficiency <= 0.30 and overlap_value >= 0.70)
                strict_actual = row[tag + "__strict"].lower() == "true"
                broad_actual = row[tag + "__broad"].lower() == "true"
                if strict_actual != strict_expected or broad_actual != broad_expected:
                    fail(f"stored threshold flags do not recompute: {asset}/{signal}/{tag}")
                if strict_actual and not broad_actual:
                    fail(f"strict cohort not nested for {tag}")
                strict_n += int(strict_actual)
                broad_n += int(broad_actual)
                recomputed += 1
            variants[tag] = {"strict": strict_n, "broad": broad_n}
    # Raw crossings before the first available causal threshold are explicit
    # warm-up exclusions. They must have no threshold row under any variant
    # and all six stored eligibility flags must remain false.
    warmup_keys = set()
    for row in raw:
        asset = row["asset"]
        snapshot = ms(row["context_snapshot_ms"], "raw context snapshot")
        keys = [(asset, snapshot, policy, population)
                for policy in ("FIXED_180", "EXPANDING_PRIOR", "ROLLING_180")
                for population in ("UNIQUE_4H_FEATURE_ROWS", "JOINED_15M_ROWS")]
        present = [key in threshold_by_key for key in keys]
        flags = [row[key] for key in row if key.endswith("__strict") or key.endswith("__broad")]
        if not any(present):
            if snapshot >= first_threshold_by_asset[asset]:
                fail(f"threshold missing after calibration warm-up: {asset}/{snapshot}")
            if any(value.lower() == "true" for value in flags):
                fail(f"warm-up event incorrectly marked eligible: {asset}/{snapshot}")
            warmup_keys.add((asset, row["direction"], ms(row["signal_time_ms"], "raw signal"), snapshot))
            warmup_by_asset[asset] += 1
        elif not all(present):
            fail(f"partial threshold policy/population coverage: {asset}/{snapshot}")
    if len(warmup_keys) != 262:
        fail(f"unexpected causal threshold warm-up event count: {len(warmup_keys)} != 262")
    return meta, {"raw_rows": len(raw), "unique_keys": len(raw_keys),
                  "historical_selected": 932, "baseline_passed": 20,
                  "reconciliation_rows": len(reconciliation), "raw_source_mismatches": 0,
                  "threshold_rows": len(thresholds), "threshold_event_joins_and_flag_recomputations": recomputed,
                  "warmup_raw_events": len(warmup_keys), "warmup_by_asset": dict(warmup_by_asset),
                  "policy_population_counts": variants}, {
                      "raw_keys": raw_keys, "raw_rows": raw}


def audit_module_b(root: Path, g004_raw_keys: set) -> dict:
    base = root / "reports/phase3_breakout_lifecycle_v1_1"
    metadata = json.loads((base / "run_metadata_v1_1.json").read_text(encoding="utf-8"))
    event_path = base / "breakout_lifecycle_events_v1_1.csv"
    horizon_path = base / "breakout_lifecycle_horizons_v1_1.csv"
    for path, key in ((event_path, "breakout_lifecycle_events_v1_1.csv"),
                      (horizon_path, "breakout_lifecycle_horizons_v1_1.csv")):
        if not path.is_file():
            fail(f"missing Module B source {path}")
        if sha256_bytes(path.read_bytes()) != metadata["output_sha256"][key]:
            fail(f"Module B output hash mismatch: {key}")
    ef, events = read_csv(event_path)
    hf, horizons = read_csv(horizon_path)
    require_columns(str(event_path), ef, {"event_id", "asset", "definition", "direction",
        "signal_time_ms", "snapshot", "zone_pct_of_channel"})
    require_columns(str(horizon_path), hf, {"event_id"})
    if len(events) != 1592 or len(horizons) != 6368:
        fail(f"Module B row counts differ: events={len(events)} horizons={len(horizons)}")
    if len({r["event_id"] for r in events}) != len(events):
        fail("duplicate Module B event_id")
    definitions = Counter(r["definition"] for r in events)
    if definitions != Counter({"BROAD_P40": 932, "STRICT_P25": 660}):
        fail(f"Module B cohort counts differ: {dict(definitions)}")
    event_keys = set()
    for row in events:
        if float(row["zone_pct_of_channel"]) != 10.0:
            fail("Module B primary event has unexpected zone definition")
        key = (row["asset"], row["direction"],
               ms(row["signal_time_ms"], "Module B signal"),
               iso_ms(row["snapshot"], "Module B snapshot"))
        event_keys.add(key)
    unmatched = event_keys - g004_raw_keys
    if unmatched:
        fail(f"Module B source identities absent from G0-04 raw ledger: {len(unmatched)}")
    return {"event_rows": len(events), "horizon_rows": len(horizons),
            "events_git_blob_sha1": git_blob_sha1(event_path.read_bytes()),
            "events_sha256": sha256_bytes(event_path.read_bytes()),
            "horizons_git_blob_sha1": git_blob_sha1(horizon_path.read_bytes()),
            "horizons_sha256": sha256_bytes(horizon_path.read_bytes()),
            "unique_source_keys": len(event_keys), "definition_rows": dict(definitions),
            "module_b_keys_missing_from_g004_raw": 0,
            "link_cardinality": "MODULE_B_COHORT_ROWS_TO_G004_RAW_IDENTITIES_RECONCILED"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--g004-artifact-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("g0_05_source_audit_output"))
    args = parser.parse_args()
    manifest, loaded = verify_pinned_sources(args.repo_root)
    rejection = audit_rejections(args.repo_root, loaded)
    meta, g004, g004_data = audit_g004_artifact(args.g004_artifact_dir)
    module_b = audit_module_b(args.repo_root, g004_data["raw_keys"])
    report = {
        "status": "G0_05_SOURCE_PROVENANCE_AND_IDENTITY_AUDIT_PASS",
        "scope": "read-only source integrity and identity reconciliation; no candidate generation",
        "g004_artifact": {"code_revision": meta["code_revision"],
            "raw_crossing_rows": g004["raw_rows"], "historical_baseline": "20/20",
            "historical_reconciliation_mismatches": 0,
            "policy_population_counts": g004["policy_population_counts"]},
        "rejection_sources": rejection,
        "module_b_sources": module_b,
        "source_manifest": manifest,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "source_audit_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.output_dir / "source_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(report["status"])
    print(json.dumps({"raw_crossings": g004["raw_rows"],
        "rejection_rows": rejection["rejection_rows_with_confirmation"],
        "module_b_rows": module_b["event_rows"],
        "module_b_unique_keys": module_b["unique_source_keys"]}, sort_keys=True))


if __name__ == "__main__":
    main()
