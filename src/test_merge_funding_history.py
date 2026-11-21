import unittest

from merge_funding_history import merge_records, parse_api_records


class FundingMergeTests(unittest.TestCase):
    def test_api_uses_realized_rate(self):
        payload = {
            "code": "0",
            "data": [{
                "instId": "BTC-USDT-SWAP",
                "fundingTime": "1760918400000",
                "fundingRate": "0.9",
                "realizedRate": "0.0001",
            }],
        }
        result = parse_api_records(payload, "BTC-USDT-SWAP")
        self.assertEqual(str(result[1760918400000]), "0.0001")

    def test_missing_realized_rate_rejected(self):
        payload = {
            "code": "0",
            "data": [{
                "instId": "BTC-USDT-SWAP",
                "fundingTime": "1760918400000",
                "fundingRate": "0.0001",
            }],
        }
        with self.assertRaises(ValueError):
            parse_api_records(payload, "BTC-USDT-SWAP")

    def test_wrong_instrument_rejected(self):
        payload = {
            "code": "0",
            "data": [{
                "instId": "ETH-USDT-SWAP",
                "fundingTime": "1760918400000",
                "realizedRate": "0.0001",
            }],
        }
        with self.assertRaises(ValueError):
            parse_api_records(payload, "BTC-USDT-SWAP")

    def test_matching_overlap_merges(self):
        archive = {1760918400000: __import__("decimal").Decimal("0.0001")}
        api = {1760918400000: __import__("decimal").Decimal("0.0001")}
        # Add enough overlap points for the validation threshold.
        for i in range(1, 20):
            ts = 1760918400000 + i * 28_800_000
            archive[ts] = __import__("decimal").Decimal("0.0002")
            api[ts] = __import__("decimal").Decimal("0.0002")
        # The final timestamp must reach the required November 19 coverage.
        final_ts = 1795132800000
        api[final_ts] = __import__("decimal").Decimal("0.0003")
        merged, overlap = merge_records(archive, api, "BTC-USDT-SWAP")
        self.assertEqual(overlap, 20)
        self.assertEqual(len(merged), 21)

    def test_conflicting_overlap_rejected(self):
        from decimal import Decimal
        archive = {}
        api = {}
        start = 1760918400000
        for i in range(20):
            ts = start + i * 28_800_000
            archive[ts] = Decimal("0.0001")
            api[ts] = Decimal("0.0002")
        api[1795132800000] = Decimal("0.0003")
        with self.assertRaises(ValueError):
            merge_records(archive, api, "BTC-USDT-SWAP")


if __name__ == "__main__":
    unittest.main()
