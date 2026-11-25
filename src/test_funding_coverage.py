import unittest

from funding_coverage import (
    expected_settlements,
    validate_funding_contract,
    validate_trade_funding_window,
)


HASH = "a" * 64


def contract(events, mode="candle_close_proxy", **overrides):
    coverage = {
        "instrument_name": "BTC-USDT-SWAP",
        "source_sha256": HASH,
        "coverage_start_ms": 0,
        "coverage_end_ms": 300,
        "schedule_id": "test_fixed_interval_100ms_v1",
        "schedule_start_ms": 100,
        "schedule_interval_ms": 100,
        "schedule_end_ms": 300,
        "event_window_start_ms": 0,
        "event_window_end_ms": 300,
        "mark_price_mode": mode,
    }
    coverage.update(overrides)
    return {"events": events, "coverage": coverage}


class FundingCoverageTests(unittest.TestCase):
    def test_expected_schedule_uses_explicit_interval(self):
        self.assertEqual(expected_settlements(0, 300, 0, 100, 300), [100, 200, 300])

    def test_complete_schedule_passes_and_returns_metadata(self):
        item = contract([
            {"funding_time": 100, "funding_rate": 0.001},
            {"funding_time": 200, "funding_rate": -0.001},
            {"funding_time": 300, "funding_rate": 0.0},
        ])
        result = validate_funding_contract({"BTC": [1]}, {"BTC": item})
        self.assertEqual(result["BTC"]["expected_settlements"], [100, 200, 300])

    def test_omitted_asset_contract_fails(self):
        with self.assertRaisesRegex(ValueError, "missing for BTC"):
            validate_funding_contract({"BTC": [1]}, {})

    def test_missing_coverage_metadata_fails(self):
        with self.assertRaisesRegex(ValueError, "coverage missing fields"):
            validate_funding_contract({"BTC": [1]}, {"BTC": {"events": [], "coverage": {}}})

    def test_empty_events_with_expected_settlement_fails(self):
        with self.assertRaisesRegex(ValueError, "3 missing"):
            validate_funding_contract({"BTC": [1]}, {"BTC": contract([])})

    def test_empty_events_without_expected_settlement_passes(self):
        item = contract([], event_window_start_ms=100, event_window_end_ms=100,
                       schedule_start_ms=200, schedule_end_ms=200)
        result = validate_funding_contract({"BTC": [1]}, {"BTC": item})
        self.assertEqual(result["BTC"]["expected_settlements"], [])

    def test_missing_interior_settlement_fails(self):
        item = contract([
            {"funding_time": 100, "funding_rate": 0.001},
            {"funding_time": 300, "funding_rate": 0.001},
        ])
        with self.assertRaisesRegex(ValueError, "1 missing"):
            validate_funding_contract({"BTC": [1]}, {"BTC": item})

    def test_duplicate_or_out_of_order_fails(self):
        item = contract([
            {"funding_time": 200, "funding_rate": 0.001},
            {"funding_time": 100, "funding_rate": 0.001},
            {"funding_time": 300, "funding_rate": 0.001},
        ])
        with self.assertRaisesRegex(ValueError, "unique and chronological"):
            validate_funding_contract({"BTC": [1]}, {"BTC": item})

    def test_non_finite_rate_fails(self):
        item = contract([
            {"funding_time": 100, "funding_rate": float("nan")},
            {"funding_time": 200, "funding_rate": 0.001},
            {"funding_time": 300, "funding_rate": 0.001},
        ])
        with self.assertRaisesRegex(ValueError, "invalid funding rate"):
            validate_funding_contract({"BTC": [1]}, {"BTC": item})

    def test_exact_mode_requires_mark_price(self):
        item = contract([
            {"funding_time": 100, "funding_rate": 0.001},
            {"funding_time": 200, "funding_rate": 0.001},
            {"funding_time": 300, "funding_rate": 0.001},
        ], mode="exact")
        with self.assertRaisesRegex(ValueError, "requires mark_price"):
            validate_funding_contract({"BTC": [1]}, {"BTC": item})

    def test_exact_mode_accepts_positive_mark(self):
        events = [
            {"funding_time": ts, "funding_rate": 0.001, "mark_price": 100.0}
            for ts in (100, 200, 300)
        ]
        result = validate_funding_contract(
            {"BTC": [1]}, {"BTC": contract(events, mode="exact")}
        )
        self.assertEqual(result["BTC"]["coverage"]["mark_price_mode"], "exact")

    def test_trade_window_includes_exit_not_entry_settlement(self):
        item = contract([
            {"funding_time": 100, "funding_rate": 0.001},
            {"funding_time": 200, "funding_rate": 0.001},
            {"funding_time": 300, "funding_rate": 0.001},
        ])
        validated = validate_funding_contract({"BTC": [1]}, {"BTC": item})["BTC"]
        self.assertEqual(validate_trade_funding_window("BTC", 100, 200, validated), [200])

    def test_trade_outside_source_coverage_fails(self):
        item = contract([
            {"funding_time": 100, "funding_rate": 0.001},
            {"funding_time": 200, "funding_rate": 0.001},
            {"funding_time": 300, "funding_rate": 0.001},
        ])
        validated = validate_funding_contract({"BTC": [1]}, {"BTC": item})["BTC"]
        with self.assertRaisesRegex(ValueError, "exceeds verified"):
            validate_trade_funding_window("BTC", -1, 200, validated)


if __name__ == "__main__":
    unittest.main()
