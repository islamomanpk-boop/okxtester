import unittest

from portfolio_engine import (
    PortfolioConfig,
    allocate_candidates,
)


def candidate(
    asset,
    entry=100,
    stop=99,
    side=1,
    priority=1,
    atr_distance=1.0,
    timestamp=900000,
):
    return {
        "asset": asset,
        "entry_price": entry,
        "stop_price": stop,
        "side": side,
        "signal_priority": priority,
        "stop_distance_atr": atr_distance,
        "signal_available_at": timestamp,
    }


class PortfolioEngineTests(unittest.TestCase):
    def setUp(self):
        self.config = PortfolioConfig(
            risk_fraction=0.005,
            max_gross_leverage=1.0,
        )

    def test_single_position_uses_half_percent_risk(self):
        result = allocate_candidates(
            [candidate("BTC")], 1000, config=self.config
        )
        trade = result["accepted"][0]
        self.assertAlmostEqual(trade["planned_stop_risk"], 5.0)

    def test_total_exposure_never_exceeds_equity(self):
        candidates = [
            candidate("BTC", entry=100, stop=99),
            candidate("ETH", entry=100, stop=99),
            candidate("SOL", entry=100, stop=99),
        ]
        result = allocate_candidates(
            candidates, 1000, config=self.config
        )
        self.assertLessEqual(result["total_gross_exposure"], 1000.000001)

    def test_existing_positions_reduce_available_capacity(self):
        existing = [
            {"asset": "BTC", "quantity": 4, "mark_price": 100}
        ]
        result = allocate_candidates(
            [candidate("ETH")],
            1000,
            open_positions=existing,
            config=self.config,
        )
        self.assertAlmostEqual(result["existing_gross_exposure"], 400)
        self.assertLessEqual(result["total_gross_exposure"], 1000.000001)

    def test_one_open_position_per_asset(self):
        existing = [
            {"asset": "BTC", "quantity": 1, "mark_price": 100}
        ]
        result = allocate_candidates(
            [candidate("BTC")],
            1000,
            open_positions=existing,
            config=self.config,
        )
        self.assertEqual(len(result["accepted"]), 0)
        self.assertEqual(
            result["rejected"][0]["reason"],
            "asset_already_has_open_position",
        )

    def test_priority_wins_when_capital_is_insufficient(self):
        candidates = [
            candidate("BTC", priority=1),
            candidate("ETH", priority=3),
        ]
        result = allocate_candidates(
            candidates, 100, config=self.config
        )
        self.assertEqual(result["accepted"][0]["asset"], "ETH")

    def test_atr_distance_breaks_priority_tie(self):
        candidates = [
            candidate("BTC", priority=2, atr_distance=2.0),
            candidate("ETH", priority=2, atr_distance=1.0),
        ]
        result = allocate_candidates(
            candidates, 100, config=self.config
        )
        self.assertEqual(result["accepted"][0]["asset"], "ETH")

    def test_asset_symbol_is_final_tie_breaker(self):
        candidates = [
            candidate("SOL", priority=2, atr_distance=1.0),
            candidate("BTC", priority=2, atr_distance=1.0),
        ]
        result = allocate_candidates(
            candidates, 100, config=self.config
        )
        self.assertEqual(result["accepted"][0]["asset"], "BTC")

    def test_duplicate_asset_candidate_only_accepted_once(self):
        candidates = [
            candidate("BTC", priority=3),
            candidate("BTC", priority=1),
        ]
        result = allocate_candidates(
            candidates, 1000, config=self.config
        )
        self.assertEqual(len(result["accepted"]), 1)
        self.assertEqual(len(result["rejected"]), 1)

    def test_candidates_must_share_decision_timestamp(self):
        candidates = [
            candidate("BTC", timestamp=900000),
            candidate("ETH", timestamp=960000),
        ]
        with self.assertRaisesRegex(ValueError, "same decision timestamp"):
            allocate_candidates(candidates, 1000, config=self.config)

    def test_short_position_is_supported(self):
        result = allocate_candidates(
            [candidate("BTC", entry=100, stop=101, side=-1)],
            1000,
            config=self.config,
        )
        self.assertEqual(result["accepted"][0]["side"], "SHORT")

    def test_invalid_candidate_rejected(self):
        bad = candidate("BTC", stop=101, side=1)
        with self.assertRaisesRegex(ValueError, "Long stop"):
            allocate_candidates([bad], 1000, config=self.config)

    def test_empty_candidates_preserve_existing_exposure(self):
        existing = [
            {"asset": "BTC", "quantity": 2, "mark_price": 100}
        ]
        result = allocate_candidates(
            [], 1000, open_positions=existing, config=self.config
        )
        self.assertAlmostEqual(result["total_gross_exposure"], 200)
        self.assertEqual(len(result["accepted"]), 0)


if __name__ == "__main__":
    unittest.main()
