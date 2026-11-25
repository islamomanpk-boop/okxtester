import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from funding_coverage import validate_funding_contract
from run_exit_experiments import load_funding_contract


class FundingLoaderTests(unittest.TestCase):
    def write_source(self, directory):
        path = Path(directory) / "BTC_USDT_SWAP_funding_rates.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["instrument_name", "funding_time", "funding_rate"],
            )
            writer.writeheader()
            writer.writerow({
                "instrument_name": "BTC-USDT-SWAP",
                "funding_time": "100",
                "funding_rate": "0.0001",
            })
        return path

    def manifest_asset(self, path):
        return {
            "instrument_name": "BTC-USDT-SWAP",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "rows": 1,
            "first_timestamp_ms": 100,
            "last_timestamp_ms": 100,
            "expected_interval_ms": 28_800_000,
            "missing_settlement_count": 0,
            "issues": [],
        }

    def test_loader_verifies_hash_and_builds_full_coverage_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_source(directory)
            contract = load_funding_contract(
                path, "BTC", self.manifest_asset(path)
            )
            self.assertEqual(contract["coverage"]["mark_price_mode"], "candle_close_proxy")
            self.assertEqual(contract["coverage"]["coverage_start_ms"], 100)
            validated = validate_funding_contract(
                {"BTC": [{"ts": 100}]}, {"BTC": contract}
            )
            self.assertEqual(
                validated["BTC"]["expected_settlements"], [100]
            )

    def test_loader_rejects_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_source(directory)
            manifest = self.manifest_asset(path)
            manifest["sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                load_funding_contract(path, "BTC", manifest)

    def test_loader_rejects_instrument_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_source(directory)
            text = path.read_text(encoding="utf-8").replace(
                "BTC-USDT-SWAP", "ETH-USDT-SWAP"
            )
            path.write_text(text, encoding="utf-8")
            manifest = self.manifest_asset(path)
            with self.assertRaisesRegex(ValueError, "instrument mismatch"):
                load_funding_contract(path, "BTC", manifest)


if __name__ == "__main__":
    unittest.main()
