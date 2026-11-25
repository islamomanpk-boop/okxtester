import unittest
from decimal import Decimal

from phase3_funding_mark_price_full_coverage_v1 import (
    bps_difference,
    distribution,
    evenly_spaced,
    merge_funding_records,
    month_range,
    percentile,
)


class Phase3FundingMarkPriceAuditTests(unittest.TestCase):
    def test_month_range_includes_both_endpoints(self):
        months = month_range("2025-10", "2026-02")
        self.assertEqual(
            months,
            ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02"],
        )

    def test_month_range_crosses_year_boundary(self):
        self.assertEqual(month_range("2025-12", "2026-01"), ["2025-12", "2026-01"])

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

    def test_archive_api_merge_prefers_api_after_tolerance_check(self):
        archive = {1: Decimal("0.0001"), 2: Decimal("0.0002")}
        api = {2: Decimal("0.0002000000005"), 3: Decimal("-0.0001")}
        merged, overlap = merge_funding_records(archive, api)
        self.assertEqual(overlap, 1)
        self.assertEqual(merged[1], Decimal("0.0001"))
        self.assertEqual(merged[2], api[2])
        self.assertEqual(merged[3], Decimal("-0.0001"))

    def test_archive_api_merge_rejects_rate_conflict(self):
        archive = {1: Decimal("0.0001")}
        api = {1: Decimal("0.0002")}
        with self.assertRaises(ValueError):
            merge_funding_records(archive, api)


if __name__ == "__main__":
    unittest.main()
