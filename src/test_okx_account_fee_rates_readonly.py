import unittest

from inspect_okx_account_fee_rates_readonly import (
    build_request_path,
    build_signature,
    parse_fee_payload,
    timestamp_from_server_ms,
)


def payload(maker="-0.0002", taker="-0.0005", group_id="4", level="Lv1"):
    return {
        "code": "0",
        "msg": "",
        "data": [{
            "instType": "SWAP",
            "level": level,
            "ts": "1795879389254",
            "feeGroup": [{
                "groupId": group_id,
                "maker": maker,
                "taker": taker,
            }],
        }],
    }


class OKXAccountFeeProbeTests(unittest.TestCase):
    def test_signature_is_deterministic_and_base64(self):
        args = (
            "2026-11-28T15:23:09.254Z",
            "GET",
            "/api/v5/account/trade-fee?instType=SWAP&instFamily=BTC-USDT",
            "",
            "test-secret",
        )
        first = build_signature(*args)
        self.assertEqual(first, build_signature(*args))
        self.assertEqual(len(first), 44)

    def test_request_path_is_deterministic(self):
        self.assertEqual(
            build_request_path(
                "/api/v5/account/trade-fee",
                {"instType": "SWAP", "instFamily": "BTC-USDT"},
            ),
            "/api/v5/account/trade-fee?instType=SWAP&instFamily=BTC-USDT",
        )

    def test_server_timestamp_is_iso8601_utc(self):
        self.assertEqual(
            timestamp_from_server_ms(1795879389254),
            "2026-11-28T15:23:09.254Z",
        )

    def test_negative_commission_rates_become_positive_costs(self):
        result = parse_fee_payload("BTC", payload())
        self.assertEqual(result["account_fee_level"], "Lv1")
        self.assertEqual(result["maker_rate_raw"], "-0.0002")
        self.assertEqual(result["taker_rate_raw"], "-0.0005")
        self.assertEqual(result["maker_commission_cost_rate"], "0.0002")
        self.assertEqual(result["taker_commission_cost_rate"], "0.0005")

    def test_positive_rebate_is_not_counted_as_negative_cost(self):
        result = parse_fee_payload("BTC", payload(maker="0.0001", taker="0.00005"))
        self.assertEqual(result["maker_commission_cost_rate"], "0")
        self.assertEqual(result["taker_commission_cost_rate"], "0")

    def test_wrong_group_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "fee group 4"):
            parse_fee_payload("BTC", payload(group_id="5"))

    def test_multiple_matching_groups_fail_closed(self):
        data = payload()
        data["data"][0]["feeGroup"].append({
            "groupId": "4", "maker": "-0.0002", "taker": "-0.0005"
        })
        with self.assertRaisesRegex(ValueError, "exactly one fee group"):
            parse_fee_payload("BTC", data)

    def test_missing_level_fails_closed(self):
        data = payload()
        data["data"][0]["level"] = ""
        with self.assertRaisesRegex(ValueError, "fee level is missing"):
            parse_fee_payload("BTC", data)

    def test_invalid_fee_decimal_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "not a valid decimal"):
            parse_fee_payload("BTC", payload(taker="not-a-rate"))

    def test_failed_api_payload_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "fee endpoint failed"):
            parse_fee_payload("BTC", {"code": "500", "msg": "failure"})


if __name__ == "__main__":
    unittest.main()
