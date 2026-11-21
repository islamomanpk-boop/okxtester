import csv
import os
import tempfile
import unittest

from compact_bar_series import CompactBarSeries, TimestampBarLookup


class CompactBarSeriesTests(unittest.TestCase):
    def test_append_and_index_candles(self):
        bars = CompactBarSeries()
        bars.append(1_000_000, 100, 102, 99, 101, 5)
        bars.append(1_060_000, 101, 103, 100, 102, 6)

        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0]["ts"], 1_000_000)
        self.assertEqual(bars[1]["close"], 102)
        self.assertEqual(bars[-1]["vol"], 6)

    def test_timestamp_lookup(self):
        bars = CompactBarSeries()
        bars.append(1_000_000, 100, 102, 99, 101, 5)
        bars.append(1_060_000, 101, 103, 100, 102, 6)

        lookup = TimestampBarLookup(bars)

        self.assertEqual(lookup[1_000_000]["close"], 101)
        self.assertEqual(lookup[1_060_000]["close"], 102)

    def test_timestamp_lookup_rejects_invalid_timestamp(self):
        bars = CompactBarSeries()
        bars.append(1_000_000, 100, 102, 99, 101, 5)
        bars.append(1_060_000, 101, 103, 100, 102, 6)

        lookup = TimestampBarLookup(bars)

        with self.assertRaises(KeyError):
            lookup[1_000_001]

        with self.assertRaises(KeyError):
            lookup[1_120_000]

    def test_csv_loader(self):
        with tempfile.NamedTemporaryFile(
            mode="w", newline="", suffix=".csv", delete=False
        ) as handle:
            path = handle.name
            writer = csv.writer(handle)
            writer.writerow(["ts", "open", "high", "low", "close", "vol"])
            writer.writerow([1_000_000, 100, 102, 99, 101, 5])
            writer.writerow([1_060_000, 101, 103, 100, 102, 6])

        try:
            bars = CompactBarSeries.from_csv(path)
            self.assertEqual(len(bars), 2)
            self.assertEqual(bars[0]["open"], 100)
            self.assertEqual(bars[1]["vol"], 6)
        finally:
            os.unlink(path)

    def test_csv_loader_rejects_missing_columns(self):
        with tempfile.NamedTemporaryFile(
            mode="w", newline="", suffix=".csv", delete=False
        ) as handle:
            path = handle.name
            writer = csv.writer(handle)
            writer.writerow(["ts", "open", "high", "low", "close"])
            writer.writerow([1_000_000, 100, 102, 99, 101])

        try:
            # Volume is optional; all required OHLC columns are present.
            bars = CompactBarSeries.from_csv(path)
            self.assertEqual(len(bars), 1)
            self.assertEqual(bars[0]["vol"], 0.0)
        finally:
            os.unlink(path)

    def test_csv_loader_rejects_invalid_numeric_values(self):
        with tempfile.NamedTemporaryFile(
            mode="w", newline="", suffix=".csv", delete=False
        ) as handle:
            path = handle.name
            writer = csv.writer(handle)
            writer.writerow(["ts", "open", "high", "low", "close"])
            writer.writerow([1_000_000, "bad", 102, 99, 101])

        try:
            with self.assertRaisesRegex(ValueError, "invalid numeric"):
                CompactBarSeries.from_csv(path)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
