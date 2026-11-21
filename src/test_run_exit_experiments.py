import csv
import tempfile
import unittest
from array import array
from pathlib import Path

from compact_bar_series import CompactBarSeries
from run_exit_experiments import (
    load_funding,
    trim_series_to_window,
    write_rows,
)


class TestExitExperimentRunner(unittest.TestCase):
    def make_bars(self):
        bars = CompactBarSeries()
        for i in range(5):
            price = 100.0 + i
            bars.append(
                1_000_000 + i * 60_000,
                price, price + 1, price - 1, price + 0.5, 10
            )
        return bars

    def test_trim_keeps_inclusive_common_window(self):
        bars = self.make_bars()
        trim_series_to_window(
            bars, 1_060_000, 1_180_000
        )
        self.assertEqual(
            list(bars.timestamps),
            [1_060_000, 1_120_000, 1_180_000],
        )
        self.assertEqual(len(bars), 3)

    def test_trim_rejects_empty_window(self):
        bars = self.make_bars()
        with self.assertRaises(ValueError):
            trim_series_to_window(bars, 2_000_000, 3_000_000)

    def test_funding_load_filters_to_window(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "funding.csv"
            with path.open("w", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["instrument_name", "funding_rate", "funding_time"],
                )
                writer.writeheader()
                writer.writerow({
                    "instrument_name": "BTC-USDT-SWAP",
                    "funding_rate": "0.0001",
                    "funding_time": "1000",
                })
                writer.writerow({
                    "instrument_name": "BTC-USDT-SWAP",
                    "funding_rate": "-0.0002",
                    "funding_time": "2000",
                })
                writer.writerow({
                    "instrument_name": "BTC-USDT-SWAP",
                    "funding_rate": "0.0003",
                    "funding_time": "3000",
                })

            events = load_funding(path, 1500, 3000)
            self.assertEqual(len(events), 2)
            self.assertEqual(events[0]["funding_time"], 2000)
            self.assertAlmostEqual(events[1]["funding_rate"], 0.0003)

    def test_write_rows_creates_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "result.csv"
            write_rows(path, [{"a": 1, "b": 2}], ["a", "b"])
            with path.open(newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows, [{"a": "1", "b": "2"}])

    def test_empty_trade_output_still_has_headers(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "trades.csv"
            write_rows(path, [], ["asset", "net_pnl"])
            with path.open(newline="") as handle:
                self.assertEqual(handle.readline().strip(), "asset,net_pnl")


if __name__ == "__main__":
    unittest.main()
