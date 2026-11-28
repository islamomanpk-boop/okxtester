import io
import json
import unittest

from reconstruct_okx_historical_l2_book import reconstruct_jsonl_member


class HistoricalL2BookReconstructionTests(unittest.TestCase):
    def stream(self, rows):
        return io.BytesIO(b"".join((json.dumps(row) + "\n").encode() for row in rows))

    def test_snapshot_update_replace_and_zero_removal(self):
        rows = [
            {
                "instId": "BTC-USDT-SWAP", "action": "snapshot", "ts": "1000",
                "bids": [["99", "2", "1"], ["98", "3", "1"]],
                "asks": [["101", "4", "1"], ["102", "5", "1"]],
            },
            {
                "instId": "BTC-USDT-SWAP", "action": "update", "ts": "2000",
                "bids": [["99", "0", "0"], ["100", "1", "1"]],
                "asks": [["101", "6", "2"]],
            },
        ]
        result = reconstruct_jsonl_member(self.stream(rows), "BTC-USDT-SWAP")
        self.assertEqual(result["record_count"], 2)
        self.assertEqual(result["action_counts"], {"snapshot": 1, "update": 1})
        self.assertEqual(result["crossed_book_observations"], 0)
        self.assertLess(result["spread_bps"]["min"], result["spread_bps"]["max"])
        self.assertEqual(result["spread_bps"]["max"], 200.0)

    def test_snapshot_resets_previous_book(self):
        rows = [
            {
                "instId": "BTC-USDT-SWAP", "action": "snapshot", "ts": "1000",
                "bids": [["99", "2", "1"]], "asks": [["101", "2", "1"]],
            },
            {
                "instId": "BTC-USDT-SWAP", "action": "snapshot", "ts": "2000",
                "bids": [["89", "2", "1"]], "asks": [["91", "2", "1"]],
            },
        ]
        result = reconstruct_jsonl_member(self.stream(rows), "BTC-USDT-SWAP")
        self.assertEqual(result["action_counts"]["snapshot"], 2)
        self.assertEqual(result["snapshot_intervals_ms"], {"1000": 1})
        self.assertEqual(result["crossed_book_observations"], 0)

    def test_update_before_snapshot_rejected(self):
        row = {
            "instId": "BTC-USDT-SWAP", "action": "update", "ts": "1000",
            "bids": [], "asks": [],
        }
        with self.assertRaisesRegex(ValueError, "before first snapshot"):
            reconstruct_jsonl_member(self.stream([row]), "BTC-USDT-SWAP")


if __name__ == "__main__":
    unittest.main()
