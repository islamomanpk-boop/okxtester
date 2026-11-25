"""Fail-closed audit for local OKX realized funding-rate CSVs."""
import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
DEFAULT_START_MS = 1760918400000
DEFAULT_END_MS = 1795104000000
DEFAULT_INTERVAL_MS = 28_800_000


def sha256_file(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_string(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, timezone.utc).isoformat()


def audit_funding_file(path, asset, expected_start_ms, expected_end_ms,
                       expected_interval_ms):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: funding file missing: {path}")
    if expected_interval_ms <= 0:
        raise ValueError("Expected interval must be positive")
    if expected_end_ms < expected_start_ms:
        raise ValueError("Expected end precedes expected start")

    expected_instrument = f"{asset}-USDT-SWAP"
    timestamps = []
    seen = set()
    min_rate = math.inf
    max_rate = -math.inf

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"instrument_name", "funding_rate", "funding_time"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{asset}: missing columns {sorted(missing)}")

        for row_number, row in enumerate(reader, start=2):
            instrument = (row.get("instrument_name") or "").strip()
            if instrument != expected_instrument:
                raise ValueError(
                    f"{asset}: row {row_number}: expected {expected_instrument}, got {instrument!r}"
                )
            try:
                ts = int(row["funding_time"])
                rate = float(row["funding_rate"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{asset}: row {row_number}: invalid timestamp/rate") from exc
            if ts <= 0:
                raise ValueError(f"{asset}: row {row_number}: timestamp must be positive")
            if not math.isfinite(rate) or abs(rate) > 1:
                raise ValueError(f"{asset}: row {row_number}: invalid realized funding rate {rate}")
            if ts in seen:
                raise ValueError(f"{asset}: duplicate funding timestamp {ts} ({utc_string(ts)})")
            seen.add(ts)
            timestamps.append(ts)
            min_rate = min(min_rate, rate)
            max_rate = max(max_rate, rate)

    if not timestamps:
        raise ValueError(f"{asset}: funding file is empty")
    if timestamps != sorted(timestamps):
        raise ValueError(f"{asset}: funding timestamps are not strictly increasing")

    issues = []
    if timestamps[0] != expected_start_ms:
        issues.append(
            f"first timestamp mismatch: expected {expected_start_ms} ({utc_string(expected_start_ms)}), "
            f"found {timestamps[0]} ({utc_string(timestamps[0])})"
        )
    if timestamps[-1] != expected_end_ms:
        issues.append(
            f"last timestamp mismatch: expected {expected_end_ms} ({utc_string(expected_end_ms)}), "
            f"found {timestamps[-1]} ({utc_string(timestamps[-1])})"
        )

    gaps = []
    irregular = []
    for previous, current in zip(timestamps, timestamps[1:]):
        delta = current - previous
        if delta != expected_interval_ms:
            if delta > expected_interval_ms and delta % expected_interval_ms == 0:
                gaps.append({
                    "after_ms": previous,
                    "before_ms": current,
                    "missing_settlements": delta // expected_interval_ms - 1,
                })
            else:
                irregular.append({
                    "after_ms": previous,
                    "before_ms": current,
                    "delta_ms": delta,
                })

    span = expected_end_ms - expected_start_ms
    expected_count = span // expected_interval_ms + 1
    if span % expected_interval_ms:
        issues.append("configured coverage endpoints do not align to expected interval")
    if len(timestamps) != expected_count:
        issues.append(f"row count mismatch: expected {expected_count}, found {len(timestamps)}")
    if gaps:
        issues.append(f"{sum(g['missing_settlements'] for g in gaps)} expected settlement(s) missing")
    if irregular:
        issues.append(f"{len(irregular)} irregular settlement interval(s) found")

    return {
        "asset": asset,
        "instrument_name": expected_instrument,
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "rows": len(timestamps),
        "first_timestamp_ms": timestamps[0],
        "first_utc": utc_string(timestamps[0]),
        "last_timestamp_ms": timestamps[-1],
        "last_utc": utc_string(timestamps[-1]),
        "min_realized_rate": min_rate,
        "max_realized_rate": max_rate,
        "expected_interval_ms": expected_interval_ms,
        "expected_rows": expected_count,
        "missing_settlement_count": sum(g["missing_settlements"] for g in gaps),
        "gaps": gaps,
        "irregular_intervals": irregular,
        "issues": issues,
        "timestamps": timestamps,
    }


def audit_all(funding_dir, expected_start_ms=DEFAULT_START_MS,
              expected_end_ms=DEFAULT_END_MS,
              expected_interval_ms=DEFAULT_INTERVAL_MS):
    funding_dir = Path(funding_dir)
    results = []
    failures = []
    for asset in ASSETS:
        path = funding_dir / f"{asset}_USDT_SWAP_funding_rates.csv"
        try:
            results.append(audit_funding_file(
                path, asset, expected_start_ms, expected_end_ms,
                expected_interval_ms
            ))
        except Exception as exc:
            failures.append(f"{asset}: {exc}")

    if len(results) == len(ASSETS):
        reference = set(results[0]["timestamps"])
        for result in results[1:]:
            current = set(result["timestamps"])
            missing = sorted(reference - current)
            extra = sorted(current - reference)
            if missing or extra:
                failures.append(
                    f"{result['asset']}: settlement timestamps differ from {results[0]['asset']} "
                    f"(missing={len(missing)}, extra={len(extra)})"
                )
        for result in results:
            failures.extend(f"{result['asset']}: {issue}" for issue in result["issues"])

    return {
        "status": "PASS" if not failures and len(results) == len(ASSETS) else "FAIL",
        "expected_start_ms": expected_start_ms,
        "expected_start_utc": utc_string(expected_start_ms),
        "expected_end_ms": expected_end_ms,
        "expected_end_utc": utc_string(expected_end_ms),
        "expected_interval_ms": expected_interval_ms,
        "expected_interval_hours": expected_interval_ms / 3_600_000,
        "assets": [
            {k: v for k, v in result.items() if k != "timestamps"}
            for result in results
        ],
        "failures": failures,
        "note": "No missing settlements are imputed or replaced with zero.",
    }


def write_reports(result, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "funding_coverage_manifest.json"
    md_path = output_dir / "funding_coverage_audit.md"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# OKX Realized Funding Coverage Audit",
        "",
        f"**Result: {result['status']}**",
        "",
        f"- Expected start: {result['expected_start_utc']} ({result['expected_start_ms']})",
        f"- Expected end: {result['expected_end_utc']} ({result['expected_end_ms']})",
        f"- Expected settlement interval: {result['expected_interval_hours']} hours",
        "- Funding source: processed OKX realized-rate CSVs",
        "- Missing settlements are never imputed or treated as zero.",
        "",
        "| Asset | Rows | Missing | First UTC | Last UTC | SHA-256 |",
        "|---|---:|---:|---|---|---|",
    ]
    for asset in result["assets"]:
        lines.append(
            f"| {asset['asset']} | {asset['rows']} | {asset['missing_settlement_count']} "
            f"| {asset['first_utc']} | {asset['last_utc']} | {asset['sha256']} |"
        )
    lines.extend(["", "## Source paths", ""])
    for asset in result["assets"]:
        lines.append(f"- {asset['asset']}: {asset['path']}")
    lines.extend(["", "## Failures", ""])
    lines.extend([f"- {failure}" for failure in result["failures"]] or ["None."])
    lines.extend(["", "## Interpretation", "", result["note"], ""])
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--funding-dir",
        default=str(Path.home() / "okx_scalping_data/funding_rates/processed"),
    )
    parser.add_argument("--output-dir", default="reports/funding_coverage_audit_v1")
    parser.add_argument("--start-ms", type=int, default=DEFAULT_START_MS)
    parser.add_argument("--end-ms", type=int, default=DEFAULT_END_MS)
    parser.add_argument("--interval-ms", type=int, default=DEFAULT_INTERVAL_MS)
    args = parser.parse_args()

    result = audit_all(
        args.funding_dir, args.start_ms, args.end_ms, args.interval_ms
    )
    json_path, md_path = write_reports(result, args.output_dir)
    print(f"Funding coverage audit: {result['status']}")
    print(f"JSON manifest: {json_path}")
    print(f"Markdown report: {md_path}")
    for failure in result["failures"]:
        print(f"FAIL: {failure}")
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
