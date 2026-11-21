import unittest

from portfolio_engine import PortfolioConfig, allocate_candidates


class PortfolioSafetyTests(unittest.TestCase):
    def test_existing_positions_over_exposure_limit_raise(self):
        with self.assertRaisesRegex(ValueError, "already exceed"):
            allocate_candidates(
                [],
                equity=1000,
                open_positions=[
                    {"asset": "BTC", "quantity": 1, "mark_price": 1001}
                ],
            )

    def test_duplicate_existing_asset_positions_raise(self):
        positions = [
            {"asset": "BTC", "quantity": 0.1, "mark_price": 50000},
            {"asset": "BTC", "quantity": 0.1, "mark_price": 50000},
        ]
        with self.assertRaisesRegex(ValueError, "one open position"):
            allocate_candidates([], equity=1000, open_positions=positions)

    def test_non_finite_equity_raises(self):
        with self.assertRaises(ValueError):
            allocate_candidates([], equity=float("nan"))

    def test_non_finite_config_raises(self):
        with self.assertRaises(ValueError):
            PortfolioConfig(max_gross_leverage=float("inf")).validate()


if __name__ == "__main__":
    unittest.main()
