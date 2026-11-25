import csv
import tempfile
import unittest
from pathlib import Path

from funding_coverage_audit import ASSETS, audit_all, audit_funding_file, write_reports

START = 1_700_000_000_000
INTERVAL = 28_800_000
END = START + 2 * INTERVAL


def write_funding(path, asset, timestamps, rates=None):
    rates = rates or [0.0001] * len(timestamps)
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["instrument_name", "funding_rate", "funding_time"])
        for ts, rate in zip(timestamps, rates):
            writer.writerow([f"{asset}-USDT-SWAP", rate, ts])


class FundingCoverageAuditTests(unittest.TestCase):
    def test_valid_file_hashes_and_checks_expected_cadence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "BTC.csv"
            write_funding(path, "BTC", [START, START + INTERVAL, END])
            result = audit_funding_file(path, "BTC", START, END, INTERVAL)
            self.assertEqual(result["rows"], 3)
            self.assertEqual(result["missing_settlement_count"], 0)
            self.assertEqual(len(result["sha256"]), 64)
            self.assertEqual(result["issues"], [])

    def test_missing_settlement_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "BTC.csv"
            write_funding(path, "BTC", [START, END])
            result = audit_funding_file(path, "BTC", START, END, INTERVAL)
            self.assertEqual(result["missing_settlement_count"], 1)
            self.assertTrue(result["issues"])

    def test_duplicate_timestamp_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "BTC.csv"
            write_funding(path, "BTC", [START, START, END])
            with self.assertRaisesRegex(ValueError, "duplicate"):
                audit_funding_file(path, "BTC", START, END, INTERVAL)

    def test_wrong_instrument_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "BTC.csv"
            write_funding(path, "ETH", [START, START + INTERVAL, END])
            with self.assertRaisesRegex(ValueError, "expected BTC-USDT-SWAP"):
                audit_funding_file(path, "BTC", START, END, INTERVAL)

    def test_invalid_rate_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "BTC.csv"
            write_funding(path, "BTC", [START, START + INTERVAL, END],
                          [0.0001, float("nan"), 0.0001])
            with self.assertRaisesRegex(ValueError, "invalid realized funding rate"):
                audit_funding_file(path, "BTC", START, END, INTERVAL)

    def test_missing_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = audit_all(tmp, START, END, INTERVAL)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(len(result["failures"]), len(ASSETS))

    def test_five_asset_timestamp_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            for asset in ASSETS:
                timestamps = [START, START + INTERVAL, END]
                if asset == "AVAX":
                    timestamps = [START, END]
                write_funding(Path(tmp) / f"{asset}_USDT_SWAP_funding_rates.csv",
                              asset, timestamps)
            result = audit_all(tmp, START, END, INTERVAL)
            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any("AVAX" in issue for issue in result["failures"]))

    def test_report_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            for asset in ASSETS:
                write_funding(Path(tmp) / f"{asset}_USDT_SWAP_funding_rates.csv",
                              asset, [START, START + INTERVAL, END])
            result = audit_all(tmp, START, END, INTERVAL)
            json_path, md_path = write_reports(result, Path(tmp) / "out")
            self.assertTrue(json_path.is_file())
            self.assertTrue(md_path.is_file())


if __name__ == "__main__":
    unittest.main()
