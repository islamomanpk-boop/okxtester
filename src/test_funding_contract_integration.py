import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from audit_funding_contract_integration import audit_funding_contract_integration


ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
START = 1_700_000_000_000
INTERVAL = 28_800_000


class FundingContractIntegrationTests(unittest.TestCase):
    def write_inputs(self, root, shifted_asset=None):
        funding_dir = Path(root) / "funding"
        funding_dir.mkdir()
        manifest_assets = []
        for asset in ASSETS:
            shift = 1000 if asset == shifted_asset else 0
            timestamps = [START + shift + i * INTERVAL for i in range(3)]
            path = funding_dir / f"{asset}_USDT_SWAP_funding_rates.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["instrument_name", "funding_time", "funding_rate"],
                )
                writer.writeheader()
                for index, ts in enumerate(timestamps):
                    writer.writerow({
                        "instrument_name": f"{asset}-USDT-SWAP",
                        "funding_time": ts,
                        "funding_rate": 0.0001 * (index + 1),
                    })
            manifest_assets.append({
                "asset": asset,
                "instrument_name": f"{asset}-USDT-SWAP",
                "rows": len(timestamps),
                "first_timestamp_ms": timestamps[0],
                "last_timestamp_ms": timestamps[-1],
                "expected_interval_ms": INTERVAL,
                "missing_settlement_count": 0,
                "issues": [],
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
        manifest_path = Path(root) / "funding_manifest.json"
        manifest_path.write_text(json.dumps({
            "status": "PASS",
            "assets": manifest_assets,
        }), encoding="utf-8")
        return funding_dir, manifest_path

    def test_real_input_integration_builds_and_validates_five_contracts(self):
        with tempfile.TemporaryDirectory() as tmp:
            funding_dir, manifest_path = self.write_inputs(tmp)
            result = audit_funding_contract_integration(funding_dir, manifest_path)
            self.assertEqual(result["status"], "REAL_FUNDING_INPUT_CONTRACT_INTEGRATION_PASS")
            self.assertEqual(result["total_source_rows"], 15)
            self.assertEqual(result["common_timestamp_count"], 3)
            self.assertTrue(result["common_timestamps_identical_across_assets"])
            self.assertFalse(result["exact_settlement_mark_price_verified"])
            self.assertFalse(result["trade_simulation_performed"])
            for asset in ASSETS:
                self.assertEqual(result["assets"][asset]["rows"], 3)
                self.assertEqual(result["assets"][asset]["mark_price_mode"], "candle_close_proxy")
                self.assertEqual(result["assets"][asset]["entry_exclusive_exit_inclusive_count"], 2)
                self.assertTrue(result["assets"][asset]["entry_timestamp_excluded"])
                self.assertTrue(result["assets"][asset]["exit_timestamp_included"])

    def test_cross_asset_timestamp_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            funding_dir, manifest_path = self.write_inputs(tmp, shifted_asset="AVAX")
            with self.assertRaisesRegex(ValueError, "timestamps differ"):
                audit_funding_contract_integration(funding_dir, manifest_path)

    def test_manifest_must_be_pass_and_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            funding_dir, manifest_path = self.write_inputs(tmp)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["status"] = "FAIL"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not PASS"):
                audit_funding_contract_integration(funding_dir, manifest_path)


if __name__ == "__main__":
    unittest.main()
