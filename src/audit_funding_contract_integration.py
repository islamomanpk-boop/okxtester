#!/usr/bin/env python3
"""Read-only real-input integration audit for the five local OKX funding CSVs.

This validates the production loader and funding contract against the user's
actual local CSV files. It does not simulate trades or calculate strategy PnL.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from funding_coverage import validate_funding_contract, validate_trade_funding_window
from run_exit_experiments import ASSETS, load_funding_contract


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_funding_contract_integration(funding_dir: Path, manifest_path: Path) -> dict:
    funding_dir = Path(funding_dir).expanduser()
    manifest_path = Path(manifest_path).expanduser()
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Archived funding manifest is missing: {manifest_path}")
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if manifest.get("status") != "PASS":
        raise ValueError("Archived funding coverage manifest is not PASS")

    assets = manifest.get("assets", [])
    by_asset = {item.get("asset"): item for item in assets}
    if len(assets) != len(ASSETS) or set(by_asset) != set(ASSETS):
        raise ValueError("Funding manifest must contain each of the five assets exactly once")

    results = {}
    common_timestamps = None
    for asset in ASSETS:
        item = by_asset[asset]
        if item.get("issues") or int(item.get("missing_settlement_count", -1)) != 0:
            raise ValueError(f"{asset}: manifest contains funding audit issues")
        path = funding_dir / f"{asset}_USDT_SWAP_funding_rates.csv"
        contract = load_funding_contract(path, asset, item)
        normalized = validate_funding_contract(
            {asset: []}, {asset: contract}
        )[asset]

        events = normalized["events"]
        timestamps = [int(event["funding_time"]) for event in events]
        if len(timestamps) != int(item["rows"]):
            raise ValueError(f"{asset}: loaded event count differs from manifest")
        if not timestamps:
            raise ValueError(f"{asset}: funding event list is empty")
        if timestamps[0] != int(item["first_timestamp_ms"]):
            raise ValueError(f"{asset}: first loaded timestamp differs from manifest")
        if timestamps[-1] != int(item["last_timestamp_ms"]):
            raise ValueError(f"{asset}: last loaded timestamp differs from manifest")
        if any("mark_price" in event for event in events):
            raise ValueError(f"{asset}: rate-only loader unexpectedly supplied settlement mark prices")
        if normalized["coverage"]["mark_price_mode"] != "candle_close_proxy":
            raise ValueError(f"{asset}: current production loader mark-price mode changed unexpectedly")

        # Validate the exact production trade-window convention without simulating a trade.
        charged_window = validate_trade_funding_window(
            asset, timestamps[0], timestamps[-1], normalized
        )
        if charged_window != timestamps[1:]:
            raise ValueError(
                f"{asset}: entry-exclusive/exit-inclusive settlement boundary mismatch"
            )
        if len(normalized["expected_settlements"]) != len(timestamps):
            raise ValueError(f"{asset}: contract schedule and loaded event count differ")

        if common_timestamps is None:
            common_timestamps = timestamps
        elif timestamps != common_timestamps:
            raise ValueError(f"{asset}: settlement timestamps differ from the other assets")

        results[asset] = {
            "instrument_name": item["instrument_name"],
            "rows": len(events),
            "first_timestamp_ms": timestamps[0],
            "last_timestamp_ms": timestamps[-1],
            "expected_interval_ms": int(item["expected_interval_ms"]),
            "source_sha256": sha256_file(path),
            "schedule_id": normalized["coverage"]["schedule_id"],
            "mark_price_mode": normalized["coverage"]["mark_price_mode"],
            "exact_mark_price_available": False,
            "expected_schedule_count": len(normalized["expected_settlements"]),
            "entry_exclusive_exit_inclusive_count": len(charged_window),
            "entry_timestamp_excluded": timestamps[0] not in charged_window,
            "exit_timestamp_included": timestamps[-1] in charged_window,
        }

    return {
        "status": "REAL_FUNDING_INPUT_CONTRACT_INTEGRATION_PASS",
        "scope": "read-only real local funding CSV -> production loader -> fail-closed funding contract validation",
        "assets": results,
        "total_source_rows": sum(item["rows"] for item in results.values()),
        "common_timestamp_count": len(common_timestamps or []),
        "common_timestamps_identical_across_assets": True,
        "funding_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "mark_price_mode": "candle_close_proxy",
        "exact_settlement_mark_price_verified": False,
        "trade_simulation_performed": False,
        "strategy_pnl_calculated": False,
        "source_csvs_copied_or_uploaded": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--funding-dir",
        type=Path,
        default=Path.home() / "okx_scalping_data" / "funding_rates" / "processed",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "reports/sideways_phase3_research_archive_v1/funding_coverage_audit_v1/funding_coverage_manifest.json",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = audit_funding_contract_integration(args.funding_dir, args.manifest)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
