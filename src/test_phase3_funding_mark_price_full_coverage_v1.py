import unittest
import hashlib
import tempfile
from decimal import Decimal
from pathlib import Path

from phase3_funding_mark_price_full_coverage_v1 import (
    bps_difference,
    build_funding_timestamps,
    distribution,
    evenly_spaced,
    percentile,
    write_mark_snapshot,
)


class Phase3FundingMarkPriceAuditTests(unittest.TestCase):
    def test_build_funding_timestamps_from_audited_manifest_record(self):
        record = {
            "rows": 4,
            "first_timestamp_ms": 1000,
            "last_timestamp_ms": 181000,
            "expected_interval_ms": 60000,
            "issues": [],
            "gaps": [],
            "irregular_intervals": [],
        }
        self.assertEqual(build_funding_timestamps(record), [1000, 61000, 121000, 181000])

    def test_build_funding_timestamps_rejects_gap_evidence(self):
        record = {
            "rows": 4,
            "first_timestamp_ms": 1000,
            "last_timestamp_ms": 181000,
            "expected_interval_ms": 60000,
            "issues": [],
            "gaps": [{"timestamp_ms": 61000}],
            "irregular_intervals": [],
        }
        with self.assertRaises(ValueError):
            build_funding_timestamps(record)

    def test_build_funding_timestamps_rejects_inconsistent_bounds(self):
        record = {
            "rows": 4,
            "first_timestamp_ms": 1000,
            "last_timestamp_ms": 181001,
            "expected_interval_ms": 60000,
            "issues": [],
            "gaps": [],
            "irregular_intervals": [],
        }
        with self.assertRaises(ValueError):
            build_funding_timestamps(record)

    def test_bps_difference_uses_comparison_as_denominator(self):
        self.assertAlmostEqual(
            bps_difference(Decimal("101"), Decimal("100")),
            100.0,
        )

    def test_percentile_interpolates(self):
        self.assertEqual(percentile([0.0, 10.0], 0.5), 5.0)

    def test_distribution_handles_empty_values(self):
        self.assertEqual(distribution([]), {"count": 0})

    def test_distribution_reports_expected_statistics(self):
        result = distribution([1.0, -1.0, 3.0])
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["min"], -1.0)
        self.assertEqual(result["median"], 1.0)
        self.assertEqual(result["max"], 3.0)
        self.assertAlmostEqual(result["mean_absolute"], 5.0 / 3.0)

    def test_evenly_spaced_returns_endpoints(self):
        self.assertEqual(evenly_spaced([0, 1, 2, 3, 4], 3), [0, 2, 4])

    def test_evenly_spaced_caps_to_available_values(self):
        self.assertEqual(evenly_spaced([1, 2], 12), [1, 2])


    def test_write_mark_snapshot_creates_stable_csv_and_hash(self):
        row = {
            "asset": "BTC",
            "inst_id": "BTC-USDT-SWAP",
            "funding_time_ms": 1760918400000,
            "mark_open": "100",
            "mark_high": "101",
            "mark_low": "99",
            "mark_close": "100.5",
            "confirm": 1,
            "bar": "4H",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mark.csv"
            digest = write_mark_snapshot(path, [row])
            self.assertTrue(path.is_file())
            self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertIn("funding_time_ms", path.read_text(encoding="utf-8"))
            self.assertIn("BTC-USDT-SWAP", path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
