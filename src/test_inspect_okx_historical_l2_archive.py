import io
import json
import unittest

from inspect_okx_historical_l2_archive import inspect_jsonl_member


class HistoricalL2ArchiveTests(unittest.TestCase):
    def test_validates_snapshot_and_update_stream(self):
        rows = [
            {
                "instId": "BTC-USDT-SWAP", "action": "snapshot", "ts": "1000",
                "seqId": "10", "prevSeqId": "-1",
                "bids": [["99", "2", "1"], ["98", "3", "1"]],
                "asks": [["101", "4", "1"], ["102", "5", "1"]],
            },
            {
                "instId": "BTC-USDT-SWAP", "action": "update", "ts": "2000",
                "seqId": "11", "prevSeqId": "10",
                "bids": [["99", "1", "1"]], "asks": [],
            },
        ]
        stream = io.BytesIO(b"".join((json.dumps(x) + "\n").encode() for x in rows))
        result = inspect_jsonl_member(stream, "BTC-USDT-SWAP")
        self.assertEqual(result["record_count"], 2)
        self.assertEqual(result["action_counts"], {"snapshot": 1, "update": 1})
        self.assertEqual(result["timestamp_delta_counts_ms_top10"], {"1000": 1})
        self.assertEqual(result["snapshot_bid_level_count"], 2)
        self.assertEqual(result["snapshot_ask_level_count"], 2)
        self.assertEqual(result["sequence_chain_mismatches"], 0)

    def test_rejects_non_snapshot_first_record(self):
        row = {
            "instId": "BTC-USDT-SWAP", "action": "update", "ts": "1000",
            "bids": [], "asks": [],
        }
        stream = io.BytesIO((json.dumps(row) + "\n").encode())
        with self.assertRaisesRegex(ValueError, "First archive record"):
            inspect_jsonl_member(stream, "BTC-USDT-SWAP")

    def test_rejects_wrong_instrument(self):
        row = {
            "instId": "ETH-USDT-SWAP", "action": "snapshot", "ts": "1000",
            "bids": [], "asks": [],
        }
        stream = io.BytesIO((json.dumps(row) + "\n").encode())
        with self.assertRaisesRegex(ValueError, "instrument ID"):
            inspect_jsonl_member(stream, "BTC-USDT-SWAP")


if __name__ == "__main__":
    unittest.main()
