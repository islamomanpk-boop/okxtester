#!/usr/bin/env python3
"""Independent G0-05 exact-minute membership verification; no audit-module imports."""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import Counter
from pathlib import Path

ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
EXPECTED = {
    "BTC": ("3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633", 569125),
    "ETH": ("8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2", 569125),
    "SOL": ("8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3", 569126),
    "DOGE": ("eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4", 569126),
    "AVAX": ("44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5", 569127),
}
# One historical failed-breakout observation occurs exactly at +12h and is excluded canonically.
EXPECTED_FAMILY = {"rejection": 1083, "breakout": 1038, "failed_breakout": 735}

def require(ok, message):
    if not ok:
        raise RuntimeError("INDEPENDENT MINUTE MEMBERSHIP FAIL-CLOSED: " + message)

def load_minutes(root: Path):
    indexes, audit = {}, {}
    for asset in ASSETS:
        path = root / "data/market_1m" / f"{asset}_USDT_USDT_1m.csv"
        require(path.is_file(), f"missing raw input {path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        expected_hash, expected_rows = EXPECTED[asset]
        require(digest == expected_hash, f"{asset} SHA-256 mismatch: {digest}")
        stamps = set()
        previous = None
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            require(reader.fieldnames == ["ts", "open", "high", "low", "close", "vol"],
                    f"{asset} schema mismatch")
            for row_number, row in enumerate(reader, start=2):
                try:
                    stamp = int(row["ts"])
                except (TypeError, ValueError):
                    raise RuntimeError(f"{asset} invalid timestamp at CSV row {row_number}")
                require(stamp % 60000 == 0, f"{asset} off-minute timestamp {stamp}")
                require(stamp not in stamps, f"{asset} duplicate timestamp {stamp}")
                if previous is not None:
                    require(stamp > previous, f"{asset} timestamps not strictly increasing")
                    require(stamp - previous == 60000, f"{asset} missing/gapped minute after {previous}")
                stamps.add(stamp)
                previous = stamp
        require(len(stamps) == expected_rows,
                f"{asset} row count {len(stamps)} != {expected_rows}")
        indexes[asset] = stamps
        audit[asset] = {"rows": len(stamps), "sha256": digest,
                        "strictly_increasing": True, "continuous_1m_grid": True}
    return indexes, audit

def verify_ledger(path: Path, family: str, indexes: dict, expected_rows: int):
    require(path.is_file(), f"missing audit ledger {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    require(len(rows) == expected_rows, f"{family} row count {len(rows)} != {expected_rows}")
    counts = Counter(row.get("disposition", "") for row in rows)
    eligible = 0
    for i, row in enumerate(rows, start=2):
        asset = row.get("asset", "")
        require(asset in indexes, f"{family} row {i} has unknown asset {asset!r}")
        status = row.get("disposition", "")
        value = (row.get("first_eligible_1m_open_ts_ms") or "").strip()
        if status == "ELIGIBLE_FOR_FURTHER_VALIDATION":
            require(value, f"{family} eligible row {i} has blank first-minute timestamp")
            try:
                stamp = int(value)
            except ValueError:
                raise RuntimeError(f"{family} row {i} first-minute timestamp is not an integer")
            require(stamp % 60000 == 0, f"{family} row {i} first-minute timestamp is off-grid")
            require(stamp in indexes[asset], f"{family} row {i} timestamp absent from {asset} raw data")
            if family == "rejection":
                expected = int(row["confirmation_ts_ms"])
            elif family == "breakout":
                expected = int(row["signal_time_ms"])
            else:
                expected = int(row["confirmation_ts_ms"])
            require(stamp == expected, f"{family} row {i} first-minute timestamp differs from signal/confirmation")
            eligible += 1
        else:
            require(not value, f"{family} non-eligible row {i} improperly exposes first-eligible timestamp")
    require(eligible == EXPECTED_FAMILY[family],
            f"{family} eligible count {eligible} != {EXPECTED_FAMILY[family]}")
    return {"rows": len(rows), "eligible": eligible, "dispositions": dict(counts),
            "every_eligible_timestamp_exactly_present": True,
            "noneligible_first_minute_fields_blank": True}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--audit-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=Path("independent_minute_verification.json"))
    args = ap.parse_args()
    indexes, raw_audit = load_minutes(args.repo_root)
    ledgers = {
        "rejection": args.audit_dir / "rejection_source_dispositions.csv",
        "breakout": args.audit_dir / "breakout_source_dispositions.csv",
        "failed_breakout": args.audit_dir / "failed_breakout_source_dispositions.csv",
    }
    result = {name: verify_ledger(path, name, indexes, expected)
              for name, path in ledgers.items()
              for expected in [1154 if name == "rejection" else 2861 if name == "breakout" else 932]}
    report = {
        "status": "INDEPENDENT_EXACT_MINUTE_MEMBERSHIP_PASS",
        "method": "separate verifier; standard-library CSV/hash parsing; no imports from G0-05 audit or contract modules",
        "raw_1m_inputs": raw_audit,
        "disposition_ledgers": result,
        "eligible_rows_checked": sum(v["eligible"] for v in result.values()),
        "eligible_rows_expected": 2856,
        "scope": "raw timestamp membership and eligible-field semantics only; not G0-05 gate approval",
    }
    require(report["eligible_rows_checked"] == 2856, "aggregate eligible row count mismatch")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))

if __name__ == "__main__":
    main()
