"""Verify local funding CSVs against the committed coverage manifest.

This is a data-source check only; it does not run a backtest.
"""
import argparse
from pathlib import Path

from funding_coverage import validate_funding_contract
from run_exit_experiments import (
    ASSETS,
    load_funding_contract,
    load_funding_manifest,
)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args(argv)

    manifest, manifest_assets, manifest_sha256 = load_funding_manifest(
        args.repo_root
    )
    funding_dir = args.home / "okx_scalping_data/funding_rates/processed"
    contracts = {}
    for asset in ASSETS:
        path = funding_dir / f"{asset}_USDT_SWAP_funding_rates.csv"
        contracts[asset] = load_funding_contract(
            path, asset, manifest_assets[asset]
        )

    validated = validate_funding_contract(
        {asset: [] for asset in ASSETS}, contracts
    )

    print("LOCAL FUNDING MANIFEST VERIFICATION: PASS")
    print(f"Manifest SHA-256: {manifest_sha256}")
    print(f"Manifest status: {manifest['status']}")
    for asset in ASSETS:
        contract = validated[asset]
        coverage = contract["coverage"]
        print(
            f"{asset}: {coverage['instrument_name']} | "
            f"{len(contract['events'])} settlements | "
            f"{coverage['coverage_start_ms']}..{coverage['coverage_end_ms']} | "
            f"schedule={coverage['schedule_id']} | "
            f"mark_mode={coverage['mark_price_mode']} | "
            f"sha256={coverage['source_sha256']}"
        )
    print("No backtest was run.")


if __name__ == "__main__":
    main()
