import io
import json
import unittest

from inspect_okx_module4_historical_l2_archive import inspect_jsonl_member


def line(action="snapshot", ts="1000", bids=None, asks=None, inst="BTC-USDT-SWAP"):
    return {
        "instId": inst,
        "action": action,
        "ts": ts,
        "bids": bids if bids is not None else [["99", "2", "1"]],
        "asks": asks if asks is not None else [["101", "3", "1"]],
    }


class Module4ArchiveInspectionTests(unittest.TestCase):
    def test_accepts_400_level_snapshot_and_updates(self):
        rows = [
            line(bids=[["99", "2", "1"], ["98", "3", "1"]],
                 asks=[["101", "3", "1"], ["102", "4", "1"]]),
            line("update", "2000", bids=[["99", "1", "1"]], asks=[]),
        ]
        stream = io.BytesIO(b"".join((json.dumps(row) + "\n").encode() for row in rows))
        result = inspect_jsonl_member(stream)
        self.assertEqual(result["record_count"], 2)
        self.assertEqual(result["action_counts"], {"snapshot": 1, "update": 1})
        self.assertEqual(result["snapshot_bid_level_count_min"], 2)
        self.assertEqual(result["snapshot_ask_level_count_max"], 2)
        self.assertEqual(result["timestamp_delta_exactly_1000ms_count"], 1)

    def test_rejects_update_as_first_record(self):
        stream = io.BytesIO((json.dumps(line("update")) + "\n").encode())
        with self.assertRaisesRegex(ValueError, "First archive record"):
            inspect_jsonl_member(stream)

    def test_rejects_invalid_level(self):
        row = line(bids=[["0", "1", "1"]])
        stream = io.BytesIO((json.dumps(row) + "\n").encode())
        with self.assertRaisesRegex(ValueError, "out-of-range"):
            inspect_jsonl_member(stream)

    def test_rejects_wrong_instrument(self):
        stream = io.BytesIO((json.dumps(line(inst="ETH-USDT-SWAP")) + "\n").encode())
        with self.assertRaisesRegex(ValueError, "instrument ID"):
            inspect_jsonl_member(stream)


if __name__ == "__main__":
    unittest.main()
