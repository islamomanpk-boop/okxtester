import unittest
from dataclasses import replace
from decimal import Decimal

from okx_contract_sizing import (
    OKXLinearSwapSpec,
    round_stop_price_for_risk,
    size_position_in_contracts,
)


def record(asset, ct_val, tick, lot, minimum, max_market="35000",
           max_stop="35000", max_trigger="100000000"):
    return {
        "instId": f"{asset}-USDT-SWAP",
        "instType": "SWAP",
        "ctType": "linear",
        "ctVal": ct_val,
        "ctValCcy": asset,
        "ctMult": "1",
        "settleCcy": "USDT",
        "tickSz": tick,
        "lotSz": lot,
        "minSz": minimum,
        "maxMktSz": max_market,
        "maxStopSz": max_stop,
        "maxTriggerSz": max_trigger,
        "state": "live",
    }


SPECS = {
    "BTC": record("BTC", "0.01", "0.1", "0.01", "0.01", "35000", "35000"),
    "ETH": record("ETH", "0.1", "0.01", "0.01", "0.01", "90000", "90000"),
    "SOL": record("SOL", "1", "0.01", "0.01", "0.01", "39000", "39000"),
    "DOGE": record("DOGE", "1000", "0.00001", "0.01", "0.01", "24000", "24000"),
    "AVAX": record("AVAX", "1", "0.001", "0.1", "0.1", "27000", "27000"),
}


class OKXContractSizingTests(unittest.TestCase):
    def spec(self, asset="BTC"):
        return OKXLinearSwapSpec.from_okx_record(asset, SPECS[asset])

    def test_current_five_asset_contract_base_units(self):
        expected = {"BTC": "0.01", "ETH": "0.1", "SOL": "1", "DOGE": "1000", "AVAX": "1"}
        for asset, units in expected.items():
            with self.subTest(asset=asset):
                self.assertEqual(self.spec(asset).base_units_per_contract, Decimal(units))

    def test_long_stop_rounds_down_away_from_entry(self):
        self.assertEqual(round_stop_price_for_risk("99.96", "LONG", "0.1"), Decimal("99.9"))

    def test_short_stop_rounds_up_away_from_entry(self):
        self.assertEqual(round_stop_price_for_risk("100.04", "SHORT", "0.1"), Decimal("100.1"))

    def test_btc_sizing_floors_contracts_and_recomputes_risk(self):
        result = size_position_in_contracts(
            equity="10000", entry_price="100000", stop_price="99900.04",
            side="LONG", risk_fraction="0.005", max_gross_leverage="1",
            taker_fee_rate="0.0003", slippage_bps="5", instrument=self.spec("BTC"),
        )
        contracts = Decimal(result["contract_quantity"])
        self.assertEqual(contracts % Decimal("0.01"), Decimal("0"))
        self.assertLessEqual(
            Decimal(result["post_rounding_cost_adjusted_risk_usdt"]),
            Decimal(result["risk_budget_usdt"]),
        )
        self.assertEqual(result["risk_conservative_stop_price"], "99900")
        self.assertLessEqual(
            Decimal(result["base_quantity_after_lot_floor"]),
            Decimal(result["requested_contracts_before_lot_floor"]) * Decimal("0.01"),
        )

    def test_short_sizing_uses_rounded_stop_and_risk_budget(self):
        result = size_position_in_contracts(
            equity="10000", entry_price="100", stop_price="100.004",
            side="SHORT", risk_fraction="0.005", max_gross_leverage="1",
            taker_fee_rate="0.0003", slippage_bps="5", instrument=self.spec("ETH"),
        )
        self.assertEqual(result["risk_conservative_stop_price"], "100.01")
        self.assertLessEqual(
            Decimal(result["post_rounding_cost_adjusted_risk_usdt"]),
            Decimal(result["risk_budget_usdt"]),
        )

    def test_doge_base_quantity_is_converted_to_contracts(self):
        result = size_position_in_contracts(
            equity="10000", entry_price="0.1", stop_price="0.099",
            side="LONG", risk_fraction="0.01", max_gross_leverage="1",
            taker_fee_rate="0.0003", slippage_bps="5", instrument=self.spec("DOGE"),
        )
        self.assertEqual(
            Decimal(result["base_quantity_after_lot_floor"]),
            Decimal(result["contract_quantity"]) * Decimal("1000"),
        )

    def test_avax_uses_0_1_contract_minimum_and_step(self):
        result = size_position_in_contracts(
            equity="10000", entry_price="30", stop_price="29",
            side="LONG", risk_fraction="0.01", max_gross_leverage="1",
            taker_fee_rate="0.0003", slippage_bps="5", instrument=self.spec("AVAX"),
        )
        contracts = Decimal(result["contract_quantity"])
        self.assertEqual(contracts % Decimal("0.1"), Decimal("0"))
        self.assertGreaterEqual(contracts, Decimal("0.1"))

    def test_below_minimum_is_rejected_not_rounded_up(self):
        with self.assertRaisesRegex(ValueError, "below minSz"):
            size_position_in_contracts(
                equity="1", entry_price="100", stop_price="99", side="LONG",
                risk_fraction="0.000001", max_gross_leverage="1",
                taker_fee_rate="0.0003", slippage_bps="0", instrument=self.spec("AVAX"),
            )

    def test_max_order_size_is_enforced(self):
        limited = replace(self.spec("BTC"), max_market_size_contracts=Decimal("0.01"))
        with self.assertRaisesRegex(ValueError, "exceeds market max size"):
            size_position_in_contracts(
                equity="1000000", entry_price="100", stop_price="99", side="LONG",
                risk_fraction="0.5", max_gross_leverage="10", taker_fee_rate="0",
                slippage_bps="0", instrument=limited,
            )

    def test_stop_order_uses_stop_maximum(self):
        limited = replace(self.spec("BTC"), max_stop_size_contracts=Decimal("0.01"))
        with self.assertRaisesRegex(ValueError, "exceeds stop max size"):
            size_position_in_contracts(
                equity="1000000", entry_price="100", stop_price="99", side="LONG",
                risk_fraction="0.5", max_gross_leverage="10", taker_fee_rate="0",
                slippage_bps="0", instrument=limited, order_kind="stop",
            )

    def test_invalid_instrument_contract_fails_closed(self):
        bad = dict(SPECS["BTC"])
        bad["ctType"] = "inverse"
        with self.assertRaisesRegex(ValueError, "ctType"):
            OKXLinearSwapSpec.from_okx_record("BTC", bad)

    def test_minimum_must_be_lot_multiple(self):
        bad = dict(SPECS["BTC"])
        bad["lotSz"] = "0.03"
        bad["minSz"] = "0.05"
        with self.assertRaisesRegex(ValueError, "integer multiple"):
            OKXLinearSwapSpec.from_okx_record("BTC", bad)

    def test_missing_max_trigger_size_fails_closed(self):
        bad = dict(SPECS["BTC"])
        del bad["maxTriggerSz"]
        with self.assertRaisesRegex(ValueError, "maxTriggerSz"):
            OKXLinearSwapSpec.from_okx_record("BTC", bad)

    def test_invalid_side_and_order_kind_rejected(self):
        with self.assertRaisesRegex(ValueError, "side must"):
            round_stop_price_for_risk("99", "BUY", "0.1")
        with self.assertRaisesRegex(ValueError, "order_kind must"):
            size_position_in_contracts(
                "1000", "100", "99", "LONG", "0.01", "1",
                "0.0003", "5", self.spec(), order_kind="limit",
            )

    def test_invalid_fee_and_slippage_rejected(self):
        with self.assertRaisesRegex(ValueError, "fee and slippage"):
            size_position_in_contracts(
                equity="1000", entry_price="100", stop_price="99",
                side="LONG", risk_fraction="0.01", max_gross_leverage="1",
                taker_fee_rate="-0.1", slippage_bps="5", instrument=self.spec(),
            )


if __name__ == "__main__":
    unittest.main()
