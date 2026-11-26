#!/usr/bin/env python3
"""Read-only G0-05 source provenance and identity reconciliation; emits no candidates."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from research.phase3_g0_05_candidate_contract_v1 import (
    exact_threshold_for_snapshot, validate_source_key_join, validate_disposition_reason,
)

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


def audit_rejections(root: Path, loaded: dict, threshold_by_key: dict) -> dict:
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
    underlying = {}
    for row in ledger:
        raw_rejection = (row.get("first_strong_rejection_ts_ms") or "").strip()
        if not raw_rejection:
            continue
        eid = rejection_event_id(row)
        if eid in seen:
            fail(f"duplicate rejection source identity {eid}")
        seen.add(eid)
        asset = row["asset"]
        definition = row["definition"].lower()
        idx = int(row["snapshot_index"])
        features = feature_rows[asset]
        if idx < 0 or idx + 1 >= len(features):
            fail(f"{eid}: snapshot index outside feature ledger")
        current, nxt = features[idx], features[idx + 1]
        available = ms(row["snapshot_available_at_ts_ms"], "snapshot availability")
        next_available = ms(row["snapshot_next_available_at_ts_ms"], "next snapshot availability")
        if next_available <= available:
            fail(f"{eid}: invalid snapshot validity interval")
        if ms(current["available_at_ts_ms"], "feature availability") != available:
            fail(f"{eid}: feature/snapshot availability mismatch")
        if ms(nxt["available_at_ts_ms"], "next feature availability") != next_available:
            fail(f"{eid}: next feature/snapshot availability mismatch")
        anatomy_row = anatomy_by_id.get(eid)
        if anatomy_row is None:
            fail(f"{eid}: missing anatomy row")
        rejection_open = ms(raw_rejection, "rejection candle open")
        confirmation = rejection_open + 900000
        if ms(anatomy_row["confirmation_ts_ms"], "anatomy confirmation") != confirmation:
            fail(f"{eid}: confirmation timestamp mismatch")
        if float(anatomy_row["upper"]) != float(current["upper"]) or float(anatomy_row["lower"]) != float(current["lower"]):
            fail(f"{eid}: frozen boundary mismatch")
        if available > rejection_open:
            fail(f"{eid}: source snapshot was not available at rejection candle open")
        if confirmation == next_available:
            endpoint[definition] += 1
        elif confirmation > next_available:
            fail(f"{eid}: confirmation occurs after next snapshot availability")
        matched += 1
        by_definition[definition] += 1
        # The historical definition is cohort membership, not a second
        # independent physical boundary-test event.
        physical_key = (asset, row["direction"], idx, int(row["segment_id"]),
                        int(row["test_rank"]), ms(row["test_start_ts_ms"], "test start"))
        item = underlying.setdefault(physical_key, {})
        if definition in item:
            fail(f"duplicate physical rejection membership {physical_key}/{definition}")
        item[definition] = {"row": row, "event_id": eid, "confirmation_ms": confirmation,
                             "available_ms": available, "next_available_ms": next_available}
    if seen != set(anatomy_by_id):
        fail(f"rejection identity/anatomy mismatch: source={len(seen)} anatomy={len(anatomy_by_id)}")
    if by_definition != Counter({"broad": 1154, "strict": 838}):
        fail(f"rejection cohort counts differ: {dict(by_definition)}")
    if endpoint != Counter({"broad": 40, "strict": 29}):
        fail(f"snapshot-endpoint exclusion counts differ: {dict(endpoint)}")
    if len(underlying) != 1154:
        fail(f"physical rejection identity count {len(underlying)} != 1,154")
    if any("broad" not in item for item in underlying.values()):
        fail("a strict historical rejection is not nested in broad membership")
    strict_keys = {key for key, item in underlying.items() if "strict" in item}
    broad_keys = {key for key, item in underlying.items() if "broad" in item}
    if not strict_keys.issubset(broad_keys) or len(strict_keys) != 838:
        fail("historical strict rejection identities are not nested in broad")

    causal_counts = Counter()
    causal_by_asset = {}
    for physical_key, memberships in underlying.items():
        asset = physical_key[0]
        source = memberships["broad"]["row"]
        idx = int(source["snapshot_index"])
        feature = feature_rows[asset][idx]
        snapshot = ms(feature["available_at_ts_ms"], "feature snapshot")
        threshold = exact_threshold_for_snapshot(threshold_by_key, asset, snapshot,
                                     "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS")
        confirmation = memberships["broad"]["confirmation_ms"]
        next_available = memberships["broad"]["next_available_ms"]
        if confirmation >= next_available:
            disposition = "SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION"
        elif threshold is None:
            disposition = "CAUSAL_THRESHOLD_WARMUP"
        else:
            width = float(feature["channel_width_pct"])
            efficiency = float(feature["directional_efficiency"])
            overlap_value = float(feature["mean_overlap"])
            if not all(map(lambda x: x == x and abs(x) != float("inf"),
                           (width, efficiency, overlap_value))):
                fail(f"{physical_key}: non-finite causal detector feature")
            strict_ok = (width <= float(threshold["p25"]) and efficiency <= 0.30 and overlap_value >= 0.70)
            broad_ok = (width <= float(threshold["p40"]) and efficiency <= 0.30 and overlap_value >= 0.70)
            if strict_ok and not broad_ok:
                fail(f"{physical_key}: strict causal cohort not nested in broad")
            if strict_ok:
                disposition = "CAUSAL_STRICT_ELIGIBLE"
            elif broad_ok:
                disposition = "CAUSAL_BROAD_ONLY_ELIGIBLE"
            else:
                disposition = "CAUSAL_REGIME_NOT_ELIGIBLE"
        causal_counts[disposition] += 1
        causal_by_asset.setdefault(asset, Counter())[disposition] += 1
    expired_physical = causal_counts["SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION"]
    if expired_physical != 40:
        fail(f"unique physical snapshot-expired rejection events {expired_physical} != 40")
    return {
        "boundary_ledger_rows": len(ledger),
        "rejection_rows_with_confirmation": matched,
        "anatomy_rows": len(anatomy),
        "identity_join": "ONE_TO_ONE_PASS",
        "historical_cohort_rows": dict(by_definition),
        "historical_unique_physical_events": len(underlying),
        "historical_strict_physical_events": len(strict_keys),
        "historical_strict_nested_in_broad": True,
        "confirmation_at_next_snapshot_endpoint_rows": dict(endpoint),
        "causal_disposition_counts_by_unique_physical_event": dict(causal_counts),
        "causal_disposition_counts_by_asset": {a: dict(v) for a, v in causal_by_asset.items()},
        "disposition": "SOURCE_ONLY_AUDIT; NO CANDIDATE RECORDS EMITTED",
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
                      "raw_keys": raw_keys, "raw_rows": raw, "threshold_by_key": threshold_by_key}


def first_eligible_minute_or_blank(disposition: str, confirmation_ms: int | None) -> int | str:
    """Only an eligible event may expose a first-eligible minute timestamp."""
    if disposition != "ELIGIBLE_FOR_FURTHER_VALIDATION":
        return ""
    if confirmation_ms is None:
        fail("eligible failed-breakout event is missing its confirmation minute")
    return int(confirmation_ms)


def validate_module_b_horizons(events: list[dict[str, str]],
                               horizons: list[dict[str, str]]) -> dict:
    """Reconcile all four horizon rows to each Module B event and its 12H outcome."""
    expected_horizons = {"15M", "1H", "4H", "12H"}
    event_by_id = {}
    for event in events:
        event_id = (event.get("event_id") or "").strip()
        if not event_id or event_id in event_by_id:
            fail(f"missing or duplicate Module B event_id: {event_id!r}")
        event_by_id[event_id] = event

    horizon_by_id = {}
    seen_pairs = set()
    for row in horizons:
        event_id = (row.get("event_id") or "").strip()
        horizon = (row.get("horizon") or "").strip()
        if event_id not in event_by_id:
            fail(f"horizon row has unknown event_id: {event_id!r}")
        if horizon not in expected_horizons:
            fail(f"unexpected Module B horizon label: {horizon!r}")
        pair = (event_id, horizon)
        if pair in seen_pairs:
            fail(f"duplicate Module B horizon row: {pair}")
        seen_pairs.add(pair)
        horizon_by_id.setdefault(event_id, {})[horizon] = row

    if set(horizon_by_id) != set(event_by_id):
        missing = sorted(set(event_by_id) - set(horizon_by_id))
        extra = sorted(set(horizon_by_id) - set(event_by_id))
        fail(f"Module B horizon event coverage mismatch: missing={missing[:5]}, extra={extra[:5]}")

    confirmations = 0
    for event_id, event in event_by_id.items():
        rows = horizon_by_id[event_id]
        if set(rows) != expected_horizons:
            fail(f"Module B event {event_id} does not have exactly 15M/1H/4H/12H horizons")
        horizon_12h = rows["12H"]
        event_complete = (event.get("complete_12h") or "").strip().lower()
        horizon_complete = (horizon_12h.get("complete") or "").strip().lower()
        if event_complete not in {"true", "false"} or horizon_complete not in {"true", "false"}:
            fail(f"Module B event {event_id} has invalid 12H completion flag")
        if event_complete != horizon_complete:
            fail(f"Module B event {event_id} 12H completion flag mismatch")
        event_confirmation = (event.get("first_15m_return_inside_close_ts_ms") or "").strip()
        horizon_confirmation = (horizon_12h.get("first_15m_return_inside_close_ts_ms") or "").strip()
        if event_confirmation != horizon_confirmation:
            fail(f"Module B event {event_id} 12H confirmation timestamp mismatch")
        if event_confirmation:
            signal_ms = ms(event["signal_time_ms"], "Module B signal")
            confirmation_ms = ms(event_confirmation, "Module B 12H confirmation")
            if confirmation_ms <= signal_ms or confirmation_ms > signal_ms + 43200000:
                fail(f"Module B event {event_id} confirmation outside 12-hour horizon")
            confirmations += 1

    return {
        "events_reconciled": len(event_by_id),
        "horizon_rows_reconciled": len(horizons),
        "horizon_rows_per_event": 4,
        "horizon_types": sorted(expected_horizons),
        "twelve_hour_confirmations": confirmations,
        "twelve_hour_completion_and_confirmation_match": True,
    }


def grouped_disposition_counts(rows: list[dict[str, str]], fields: tuple[str, ...]) -> list[dict]:
    """Return deterministic grouped row counts without changing source identities."""
    grouped = Counter(
        tuple((row.get(field) or "NOT_APPLICABLE").strip() for field in fields)
        for row in rows
    )
    return [
        {**dict(zip(fields, key)), "rows": count}
        for key, count in sorted(grouped.items())
    ]


def validate_disposition_ledger(rows: list[dict[str, str]],
                                 identity_field: str, expected_rows: int) -> dict:
    """Require one unique physical source identity and one valid disposition per row."""
    if len(rows) != expected_rows:
        fail(f"disposition ledger row count {len(rows)} != expected {expected_rows}")
    identities = [(row.get(identity_field) or "").strip() for row in rows]
    if any(not value for value in identities):
        fail(f"disposition ledger has blank {identity_field}")
    if len(identities) != len(set(identities)):
        fail(f"disposition ledger has duplicate {identity_field}")
    allowed = {"ELIGIBLE_FOR_FURTHER_VALIDATION", "REJECTED", "EXPIRED", "CENSORED"}
    dispositions = [row.get("disposition") for row in rows]
    invalid = sorted(set(dispositions) - allowed)
    if invalid or any(not value for value in dispositions):
        fail(f"disposition ledger has invalid status values: {invalid}")
    for row in rows:
        try:
            validate_disposition_reason(
                row.get("disposition", ""),
                row.get("reason_code", ""),
                row.get("censoring_reason", ""),
            )
        except ValueError as exc:
            fail(f"disposition reason contract violation: {exc}")
    counts = Counter(dispositions)
    if sum(counts.values()) != expected_rows:
        fail("disposition totals do not equal the source population")
    return {"rows": len(rows), "dispositions": dict(counts)}


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
        "signal_time_ms", "snapshot", "zone_pct_of_channel", "complete_12h",
        "first_15m_return_inside_close_ts_ms"})
    require_columns(str(horizon_path), hf, {"event_id", "horizon", "complete",
        "first_15m_return_inside_close_ts_ms"})
    if len(events) != 1592 or len(horizons) != 6368:
        fail(f"Module B row counts differ: events={len(events)} horizons={len(horizons)}")
    horizon_reconciliation = validate_module_b_horizons(events, horizons)
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
    try:
        validate_source_key_join(list(event_keys), list(g004_raw_keys), exact=False)
    except ValueError as exc:
        fail(f"Module B source identities absent from G0-04 raw ledger: {exc}")
    return {"event_rows": len(events), "horizon_rows": len(horizons),
            "events_git_blob_sha1": git_blob_sha1(event_path.read_bytes()),
            "events_sha256": sha256_bytes(event_path.read_bytes()),
            "horizons_git_blob_sha1": git_blob_sha1(horizon_path.read_bytes()),
            "horizons_sha256": sha256_bytes(horizon_path.read_bytes()),
            "unique_source_keys": len(event_keys), "definition_rows": dict(definitions),
            "module_b_keys_missing_from_g004_raw": 0,
            "horizon_reconciliation": horizon_reconciliation,
            "link_cardinality": "MODULE_B_COHORT_ROWS_TO_G004_RAW_IDENTITIES_RECONCILED"}


def row_disposition_dry_run(root: Path, artifact: Path, out: Path,
                            g004_data: dict, rejection_audit: dict) -> dict:
    """Emit source-only physical-event disposition ledgers; never candidates."""
    minute_opens = {}
    input_audit = {}
    for asset in ASSETS:
        p = root / "data/market_1m" / f"{asset}_USDT_USDT_1m.csv"
        if not p.is_file():
            fail(f"missing exact-minute source {p}")
        h = hashlib.sha256()
        stamps = set()
        with p.open("rb") as raw:
            for chunk in iter(lambda: raw.read(1 << 20), b""):
                h.update(chunk)
        expected = {
            "BTC":"3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633",
            "ETH":"8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2",
            "SOL":"8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3",
            "DOGE":"eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4",
            "AVAX":"44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5"}[asset]
        if h.hexdigest() != expected:
            fail(f"{asset} 1m SHA256 mismatch before exact-minute lookup")
        with p.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != ["ts","open","high","low","close","vol"]:
                fail(f"{asset} 1m schema mismatch")
            for row in reader:
                t = ms(row["ts"], f"{asset} 1m ts")
                if t % 60000 or t in stamps:
                    fail(f"{asset} duplicate or off-grid 1m timestamp {t}")
                stamps.add(t)
        minute_opens[asset] = stamps
        input_audit[asset] = {"rows":len(stamps),"sha256":h.hexdigest()}

    def minute_check(asset, timestamp):
        t = ms(str(timestamp), "first eligible minute")
        if t % 60000:
            return "CENSORED", "MISSING_OR_GAPPED_MINUTES"
        if t not in minute_opens[asset]:
            return "CENSORED", "MISSING_OR_GAPPED_MINUTES"
        return "ELIGIBLE_FOR_FURTHER_VALIDATION", ""

    rows_out = []
    # Rejection source: collapse historical strict/broad rows to one physical event.
    ledger_path = root / "reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv"
    anatomy_path = root / "reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv"
    _, ledger = read_csv(ledger_path)
    _, anatomy = read_csv(anatomy_path)
    anatomy_by_id = {r["event_id"]:r for r in anatomy}
    feature_by_asset = {}
    for asset in ASSETS:
        _, fr = read_csv(root / "reports/sideways_detector_original_v1" / f"{asset}_features_original_v1.csv")
        feature_by_asset[asset] = fr
    physical = {}
    for row in ledger:
        if not (row.get("first_strong_rejection_ts_ms") or "").strip():
            continue
        eid = rejection_event_id(row)
        idx = int(row["snapshot_index"])
        key = (row["asset"],row["direction"],idx,int(row["segment_id"]),
               int(row["test_rank"]),ms(row["test_start_ts_ms"],"test start"))
        d = physical.setdefault(key, {"members":[]})
        d["members"].append(row)
        d["event_ids"].append(eid) if "event_ids" in d else d.update({"event_ids":[eid]})
    rejection_rows = []
    thresholds = g004_data["threshold_by_key"]
    for key, item in physical.items():
        asset, direction, idx, segment, rank, start = key
        broad = next((r for r in item["members"] if r["definition"].lower()=="broad"), None)
        if broad is None:
            fail(f"physical rejection missing broad cohort row: {key}")
        feature = feature_by_asset[asset][idx]
        snapshot = ms(feature["available_at_ts_ms"],"rejection feature snapshot")
        threshold = exact_threshold_for_snapshot(thresholds, asset, snapshot,
                                         "EXPANDING_PRIOR", "UNIQUE_4H_FEATURE_ROWS")
        confirm = ms(broad["first_strong_rejection_ts_ms"],"rejection open") + 900000
        next_available = ms(broad["snapshot_next_available_at_ts_ms"],"next snapshot")
        causal_cohort = "NOT_EVALUATED"
        if confirm >= next_available:
            status, reason = "EXPIRED","SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION"
        elif threshold is None:
            status, reason = "REJECTED","CAUSAL_THRESHOLD_WARMUP"
            causal_cohort = "WARMUP"
        else:
            width,eff,ov = (float(feature[k]) for k in ("channel_width_pct","directional_efficiency","mean_overlap"))
            strict = width <= float(threshold["p25"]) and eff <= .30 and ov >= .70
            broad_ok = width <= float(threshold["p40"]) and eff <= .30 and ov >= .70
            if strict:
                status,reason="ELIGIBLE_FOR_FURTHER_VALIDATION","NONE"
                causal_cohort = "CAUSAL_STRICT"
            elif broad_ok:
                status,reason="ELIGIBLE_FOR_FURTHER_VALIDATION","NONE"
                causal_cohort = "CAUSAL_BROAD_ONLY"
            else:
                status,reason="REJECTED","CAUSAL_REGIME_NOT_ELIGIBLE"
                causal_cohort = "NOT_ELIGIBLE"
        if status=="ELIGIBLE_FOR_FURTHER_VALIDATION":
            status, minute_reason = minute_check(asset, confirm)
            if minute_reason:
                reason = minute_reason
        rejection_rows.append({
            "asset":asset,"source_event_row_ids":";".join(sorted(item["event_ids"])),
            "historical_cohort_memberships":";".join(sorted({r["definition"].upper() for r in item["members"]})),
            "causal_cohort":causal_cohort,
            "direction":direction,"family":"SUPPORT_REJECTION" if direction.lower()=="lower" else "RESISTANCE_REJECTION",
            "family_direction":"LONG" if direction.lower()=="lower" else "SHORT",
            "confirmation_ts_ms":confirm,"first_eligible_1m_open_ts_ms":first_eligible_minute_or_blank(status, confirm),
            "disposition":status,"reason_code":reason,
            "censoring_reason":reason if status=="CENSORED" else ""})
    # Raw breakout crossings: retain one row per raw source crossing.
    raw_rows = g004_data["raw_rows"]
    breakout_rows = []
    tag="EXPANDING_PRIOR__UNIQUE_4H_FEATURE_ROWS"
    for r in raw_rows:
        asset=r["asset"]; signal=ms(r["signal_time_ms"],"breakout signal")
        snap=ms(r["context_snapshot_ms"],"breakout snapshot")
        if r[tag+"__strict"].lower()=="true":
            eligible=True; cohort="CAUSAL_STRICT"
        elif r[tag+"__broad"].lower()=="true":
            eligible=True; cohort="CAUSAL_BROAD_ONLY"
        else:
            eligible=False; cohort="CAUSAL_THRESHOLD_WARMUP" if not any(
                (asset,snap,pol,pop) in thresholds for pol in ("FIXED_180","EXPANDING_PRIOR","ROLLING_180") for pop in ("UNIQUE_4H_FEATURE_ROWS","JOINED_15M_ROWS")) else "CAUSAL_REGIME_NOT_ELIGIBLE"
        status="ELIGIBLE_FOR_FURTHER_VALIDATION" if eligible else "REJECTED"
        reason="NONE" if eligible else cohort
        if eligible:
            status, minute_reason=minute_check(asset,signal)
            if minute_reason:
                reason=minute_reason
        breakout_rows.append({"asset":asset,"source_event_key":f"{asset}|{r['direction']}|{signal}|{snap}",
            "direction":r["direction"],"family":"BREAKOUT_CONTINUATION",
            "family_direction":"LONG" if r["direction"]=="UPPER" else "SHORT",
            "signal_time_ms":signal,"first_eligible_1m_open_ts_ms":first_eligible_minute_or_blank(status, signal),
            "causal_cohort":cohort,"disposition":status,"reason_code":reason,
            "censoring_reason":reason if status=="CENSORED" else ""})
    # Every G0-04 raw crossing must appear exactly once in the continuation ledger.
    expected_breakout_keys = [
        f"{r['asset']}|{r['direction']}|{ms(r['signal_time_ms'], 'raw signal')}|{ms(r['context_snapshot_ms'], 'raw snapshot')}"
        for r in raw_rows
    ]
    observed_breakout_keys = [r["source_event_key"] for r in breakout_rows]
    try:
        validate_source_key_join(expected_breakout_keys, observed_breakout_keys, exact=True)
    except ValueError as exc:
        fail(f"breakout source-key reconciliation failed: {exc}")
    # Module B: collapse strict/broad cohort rows to unique source events.
    base=root/"reports/phase3_breakout_lifecycle_v1_1"
    _, events=read_csv(base/"breakout_lifecycle_events_v1_1.csv")
    grouped={}
    for r in events:
        key=(r["asset"],r["direction"],ms(r["signal_time_ms"],"Module B signal"),iso_ms(r["snapshot"],"Module B snapshot"))
        grouped.setdefault(key,[]).append(r)
    failed_rows=[]
    for key, members in grouped.items():
        asset,direction,signal,snapshot=key
        definitions={x["definition"] for x in members}
        if len(members) not in (1,2) or "BROAD_P40" not in definitions or not definitions.issubset({"BROAD_P40","STRICT_P25"}):
            fail(f"Module B physical event cohort collapse mismatch: {key}")
        confirmations={ms(x["first_15m_return_inside_close_ts_ms"],"failure confirmation")
                       for x in members if (x.get("first_15m_return_inside_close_ts_ms") or "").strip()}
        complete={x["complete_12h"].lower()=="true" for x in members}
        if len(confirmations)>1 or len(complete)!=1:
            fail(f"Module B cohort rows disagree on horizon outcome: {key}")
        raw=next((x for x in raw_rows if x["asset"]==asset and x["direction"]==direction
                  and ms(x["signal_time_ms"],"raw signal")==signal
                  and ms(x["context_snapshot_ms"],"raw snapshot")==snapshot),None)
        if raw is None:
            fail(f"Module B event missing raw crossing: {key}")
        if raw[tag+"__strict"].lower()=="true": source_ok=True; source_cohort="CAUSAL_STRICT"
        elif raw[tag+"__broad"].lower()=="true": source_ok=True; source_cohort="CAUSAL_BROAD_ONLY"
        else: source_ok=False; source_cohort="NOT_ELIGIBLE"
        confirmation=next(iter(confirmations)) if confirmations else None
        if not source_ok:
            status,reason="REJECTED","NO_VALID_SOURCE_BREAKOUT"
        elif confirmation is None:
            if next(iter(complete)):
                status,reason="EXPIRED","EXPIRED_NO_RETURN_INSIDE_WITHIN_12H"
            else:
                status,reason="CENSORED","SOURCE_END_BEFORE_RESOLUTION"
        else:
            if confirmation<=signal or confirmation>signal+43200000:
                fail(f"Module B failure confirmation outside 12h horizon: {key}")
            status,reason=minute_check(asset,confirmation)
            if not reason:
                reason="NONE"
        failed_rows.append({"asset":asset,"source_event_key":f"{asset}|{direction}|{signal}|{snapshot}",
            "source_event_row_ids":";".join(sorted(x["event_id"] for x in members)),
            "historical_cohort_memberships":";".join(sorted({x["definition"] for x in members})),"direction":direction,
            "family":"FAILED_BREAKOUT_REVERSAL","family_direction":"SHORT" if direction=="UPPER" else "LONG","signal_time_ms":signal,
            "confirmation_ts_ms":confirmation or "",
            "first_eligible_1m_open_ts_ms":first_eligible_minute_or_blank(status, confirmation),
            "causal_source_cohort":source_cohort,"disposition":status,"reason_code":reason,
            "censoring_reason":reason if status=="CENSORED" else ""})
    out.mkdir(parents=True,exist_ok=True)
    files={"rejection_source_dispositions.csv":rejection_rows,
           "breakout_source_dispositions.csv":breakout_rows,
           "failed_breakout_source_dispositions.csv":failed_rows}
    counts={}
    identity_fields = {
        "rejection_source_dispositions.csv": ("source_event_row_ids", 1154),
        "breakout_source_dispositions.csv": ("source_event_key", 2861),
        "failed_breakout_source_dispositions.csv": ("source_event_key", 932),
    }
    for name, rows in files.items():
        if not rows: fail(f"empty row disposition output {name}")
        identity_field, expected_rows = identity_fields[name]
        counts[name] = validate_disposition_ledger(rows, identity_field, expected_rows)
        for field, keys in (
            ("by_asset_disposition", ("asset", "disposition")),
            ("by_family_side_disposition_reason", ("family", "family_direction", "disposition", "reason_code")),
            ("by_source_direction_disposition", ("direction", "disposition")),
        ):
            counts[name][field] = grouped_disposition_counts(rows, keys)
        cohort_rows = [
            {**row, "causal_cohort_summary": row.get("causal_cohort") or row.get("causal_source_cohort") or "NOT_APPLICABLE"}
            for row in rows
        ]
        counts[name]["by_causal_cohort_disposition"] = grouped_disposition_counts(
            cohort_rows, ("causal_cohort_summary", "disposition"))
        counts[name]["by_reason_code"] = grouped_disposition_counts(rows, ("reason_code",))
        with (out/name).open("w",encoding="utf-8",newline="") as h:
            writer=csv.DictWriter(h,fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)
    return {"market_1m_inputs":input_audit,"row_level_outputs":counts,
            "scope":"SOURCE-ONLY DISPOSITION DRY-RUN; NO CANDIDATE GENERATION"}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--g004-artifact-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("g0_05_source_audit_output"))
    args = parser.parse_args()
    manifest, loaded = verify_pinned_sources(args.repo_root)
    meta, g004, g004_data = audit_g004_artifact(args.g004_artifact_dir)
    rejection = audit_rejections(args.repo_root, loaded, g004_data["threshold_by_key"])
    module_b = audit_module_b(args.repo_root, g004_data["raw_keys"])
    dry_run = row_disposition_dry_run(args.repo_root, args.g004_artifact_dir, args.output_dir, g004_data, rejection)
    report = {
        "status": "G0_05_SOURCE_PROVENANCE_AND_IDENTITY_AUDIT_PASS",
        "scope": "read-only source integrity and identity reconciliation; no candidate generation",
        "g004_artifact": {"code_revision": meta["code_revision"],
            "raw_crossing_rows": g004["raw_rows"], "historical_baseline": "20/20",
            "historical_reconciliation_mismatches": 0,
            "threshold_event_joins_and_flag_recomputations": g004["threshold_event_joins_and_flag_recomputations"],
            "warmup_raw_events": g004["warmup_raw_events"],
            "warmup_by_asset": g004["warmup_by_asset"],
            "policy_population_counts": g004["policy_population_counts"]},
        "rejection_sources": rejection,
        "module_b_sources": module_b,
        "row_level_disposition_dry_run": dry_run,
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
