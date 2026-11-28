import unittest

from probe_okx_historical_orderbook_availability import parse_archive_metadata


class HistoricalOrderbookAvailabilityTests(unittest.TestCase):
    def test_parses_files_by_expected_instrument_family(self):
        payload = {
            "code": "0",
            "data": [{
                "details": [{
                    "instFamily": "BTC-USDT",
                    "groupDetails": [{
                        "filename": "BTC-USDT-SWAP-orderbook-2025-11-01.zip",
                        "sizeMB": "12.5",
                        "url": "https://static.okx.com/archive.zip",
                        "dataTs": "1761955200000",
                    }],
                }],
            }],
        }
        result = parse_archive_metadata(payload, {"BTC-USDT"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["inst_family"], "BTC-USDT")
        self.assertEqual(result[0]["size_mb"], "12.5")

    def test_ignores_unrequested_family(self):
        payload = {
            "code": "0",
            "data": [{
                "details": [{
                    "instFamily": "ETH-USDT",
                    "groupDetails": [{
                        "filename": "ETH-USDT-SWAP-orderbook.zip",
                        "sizeMB": "1",
                        "url": "https://static.okx.com/archive.zip",
                    }],
                }],
            }],
        }
        self.assertEqual(parse_archive_metadata(payload, {"BTC-USDT"}), [])

    def test_rejects_api_error(self):
        with self.assertRaisesRegex(ValueError, "response code"):
            parse_archive_metadata({"code": "500", "data": []}, {"BTC-USDT"})

    def test_rejects_incomplete_archive_metadata(self):
        payload = {
            "code": "0",
            "data": [{
                "details": [{
                    "instFamily": "BTC-USDT",
                    "groupDetails": [{
                        "filename": "BTC.zip",
                        "sizeMB": "1",
                        "url": "http://insecure.example/file.zip",
                    }],
                }],
            }],
        }
        with self.assertRaisesRegex(ValueError, "incomplete"):
            parse_archive_metadata(payload, {"BTC-USDT"})


if __name__ == "__main__":
    unittest.main()
