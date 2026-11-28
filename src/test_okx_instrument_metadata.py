import unittest

from audit_okx_instrument_metadata import (
    ASSETS,
    build_report,
    validate_instrument,
    validate_payload,
)


def fixture(asset="BTC"):
    return {
        "instId": f"{asset}-USDT-SWAP",
        "instType": "SWAP",
        "ctType": "linear",
        "ctVal": "0.01",
        "ctValCcy": asset,
        "ctMult": "1",
        "settleCcy": "USDT",
        "tickSz": "0.1",
        "lotSz": "0.01",
        "minSz": "0.01",
        "maxMktSz": "35000",
        "maxStopSz": "35000",
        "maxTriggerSz": "100000000",
        "groupId": "4",
        "state": "live",
        "listTime": "1573557408000",
        "expTime": "",
        "upcChg": [],
    }


class OKXInstrumentMetadataTests(unittest.TestCase):
    def test_valid_linear_usdt_swap_passes(self):
        result = validate_instrument("BTC", fixture())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["contract_value"], "0.01")
        self.assertEqual(result["lot_size_contracts"], "0.01")
        self.assertEqual(result["minimum_order_size_contracts"], "0.01")

    def test_all_project_assets_have_exact_expected_ids(self):
        for asset in ASSETS:
            with self.subTest(asset=asset):
                result = validate_instrument(asset, fixture(asset))
                self.assertEqual(result["inst_id"], f"{asset}-USDT-SWAP")

    def test_wrong_instrument_id_fails_closed(self):
        row = fixture()
        row["instId"] = "BTC-USDT"
        with self.assertRaisesRegex(ValueError, "instId"):
            validate_instrument("BTC", row)

    def test_wrong_contract_type_fails_closed(self):
        row = fixture()
        row["ctType"] = "inverse"
        with self.assertRaisesRegex(ValueError, "ctType"):
            validate_instrument("BTC", row)

    def test_wrong_settlement_currency_fails_closed(self):
        row = fixture()
        row["settleCcy"] = "BTC"
        with self.assertRaisesRegex(ValueError, "settleCcy"):
            validate_instrument("BTC", row)

    def test_wrong_contract_value_currency_fails_closed(self):
        row = fixture()
        row["ctValCcy"] = "USDT"
        with self.assertRaisesRegex(ValueError, "ctValCcy"):
            validate_instrument("BTC", row)

    def test_non_live_instrument_fails_closed(self):
        row = fixture()
        row["state"] = "suspend"
        with self.assertRaisesRegex(ValueError, "state"):
            validate_instrument("BTC", row)

    def test_zero_tick_size_fails_closed(self):
        row = fixture()
        row["tickSz"] = "0"
        with self.assertRaisesRegex(ValueError, "tickSz must be positive"):
            validate_instrument("BTC", row)

    def test_non_multiple_minimum_size_fails_closed(self):
        row = fixture()
        row["lotSz"] = "0.03"
        row["minSz"] = "0.05"
        with self.assertRaisesRegex(ValueError, "integer multiple"):
            validate_instrument("BTC", row)

    def test_invalid_decimal_fails_closed(self):
        row = fixture()
        row["ctVal"] = "NaN"
        with self.assertRaisesRegex(ValueError, "must be finite"):
            validate_instrument("BTC", row)

    def test_upcoming_change_schema_is_checked(self):
        row = fixture()
        row["upcChg"] = [{"param": "tickSz", "newValue": "0.01"}]
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            validate_instrument("BTC", row)

    def test_payload_requires_success_code(self):
        with self.assertRaisesRegex(ValueError, "not successful"):
            validate_payload("BTC", {"code": "500", "msg": "failed", "data": []})

    def test_payload_requires_exactly_one_record(self):
        row = fixture()
        with self.assertRaisesRegex(ValueError, "exactly one"):
            validate_payload("BTC", {"code": "0", "data": [row, row]})

    def test_report_does_not_claim_historical_or_account_fee_coverage(self):
        result = validate_instrument("BTC", fixture())
        report = build_report(1000, 2000, {"BTC": result}, {"ETH": "sample"})
        self.assertEqual(
            report["historical_metadata"]["status"],
            "NOT_VERIFIED_CURRENT_SNAPSHOT_ONLY",
        )
        self.assertEqual(
            report["account_fee_tier"]["status"],
            "NOT_FETCHED_AUTHENTICATED_ACCOUNT_ENDPOINT_REQUIRED",
        )
        self.assertIn("FAIL_CLOSED", report["status"])


if __name__ == "__main__":
    unittest.main()
