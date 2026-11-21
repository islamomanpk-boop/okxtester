import io
import unittest
import zipfile

from download_funding_archives import month_range, parse_archive


def make_zip(rows, filename="sample.csv"):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(filename, rows)
    return buffer.getvalue()


class FundingArchiveTests(unittest.TestCase):
    def test_month_range_crosses_year(self):
        self.assertEqual(
            month_range("2025-11", "2026-02"),
            ["2025-11", "2025-12", "2026-01", "2026-02"],
        )

    def test_valid_archive(self):
        data = make_zip(
            "instrument_name,funding_rate,funding_time\n"
            "BTC-USDT-SWAP,0.0001,1759248000000\n"
        )
        rows = parse_archive(data, "BTC-USDT-SWAP")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["funding_rate"], "0.0001")

    def test_invalid_zip_rejected(self):
        with self.assertRaises(ValueError):
            parse_archive(b"not a zip", "BTC-USDT-SWAP")

    def test_wrong_instrument_rejected(self):
        data = make_zip(
            "instrument_name,funding_rate,funding_time\n"
            "ETH-USDT-SWAP,0.0001,1759248000000\n"
        )
        with self.assertRaises(ValueError):
            parse_archive(data, "BTC-USDT-SWAP")

    def test_bad_timestamp_rejected(self):
        data = make_zip(
            "instrument_name,funding_rate,funding_time\n"
            "BTC-USDT-SWAP,0.0001,not-a-time\n"
        )
        with self.assertRaises(ValueError):
            parse_archive(data, "BTC-USDT-SWAP")

    def test_wrong_columns_rejected(self):
        data = make_zip("symbol,rate,time\nBTC,0.1,123\n")
        with self.assertRaises(ValueError):
            parse_archive(data, "BTC-USDT-SWAP")


if __name__ == "__main__":
    unittest.main()
