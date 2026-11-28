import unittest
from audit_okx_source_samples import compare_candle, select_samples

def row(ts, o, h, low, close, vol=1):
    return {"ts": ts, "open": o, "high": h, "low": low, "close": close, "vol": vol}

class OKXSourceSampleTests(unittest.TestCase):
    def test_selects_exact_changed_and_largest_jump(self):
        rows = [
            row(60000, 100, 100.2, 99.8, 100),
            row(120000, 100, 100.2, 99.8, 100),
            row(180000, 100.5, 101, 100.4, 100.8),
            row(240000, 100.6, 101, 100.4, 100.7),
        ]
        result = select_samples(rows, sample_per_class=1, seed=1)
        self.assertEqual(result["transition_counts"], {"exact": 1, "changed": 2})
        classes = {x["classification"] for x in result["samples"]}
        self.assertIn("exact", classes)
        self.assertIn("changed", classes)
        self.assertIn("largest_absolute_adjacent_open_jump", classes)

    def test_compare_ohlc_and_volume(self):
        source = row(60000, 100, 101, 99, 100.5, 7)
        api = ["60000", "100", "101", "99", "100.5", "7", "1", "1", "1"]
        result = compare_candle(source, api)
        self.assertTrue(result["ohlc_match"])
        self.assertTrue(result["volume_match"])

    def test_compare_reports_volume_separately(self):
        source = row(60000, 100, 101, 99, 100.5, 7)
        api = ["60000", "100", "101", "99", "100.5", "8", "1", "1", "1"]
        result = compare_candle(source, api)
        self.assertTrue(result["ohlc_match"])
        self.assertFalse(result["volume_match"])

    def test_missing_timestamp_is_not_a_match(self):
        result = compare_candle(row(60000, 100, 101, 99, 100.5), None)
        self.assertFalse(result["timestamp_found"])
        self.assertFalse(result["ohlc_match"])

if __name__ == "__main__":
    unittest.main()
