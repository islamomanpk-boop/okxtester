import io
import json
import unittest
from reconstruct_okx_module4_historical_l2_book import reconstruct_jsonl


def rec(action="snapshot", ts=1000, bids=None, asks=None):
    return {"instId":"BTC-USDT-SWAP","action":action,"ts":str(ts),
            "bids":bids if bids is not None else [["99","2","1"]],
            "asks":asks if asks is not None else [["101","3","1"]]}


def stream(rows):
    return io.BytesIO(b"".join((json.dumps(x)+"\n").encode() for x in rows))


class Module4BookReconstructionTests(unittest.TestCase):
    def test_snapshot_and_incremental_updates(self):
        rows=[rec(bids=[["99","2","1"],["98","3","1"]],asks=[["101","3","1"]]),
              rec("update",2000,bids=[["99","4","2"],["98","0","0"],["97","1","1"]],asks=[])]
        result=reconstruct_jsonl(stream(rows),sample_every=1)
        self.assertEqual(result["record_count"],2)
        self.assertEqual(result["max_bid_levels_observed"],2)
        self.assertEqual(result["action_counts"],{"snapshot":1,"update":1})
        self.assertEqual(result["metric_sample_count"],2)

    def test_later_snapshot_replaces_both_sides(self):
        rows=[rec(),rec("snapshot",2000,bids=[["90","1","1"]],asks=[["110","1","1"]])]
        result=reconstruct_jsonl(stream(rows),sample_every=1)
        self.assertEqual(result["snapshot_count"],2)
        self.assertEqual(result["max_bid_levels_observed"],1)

    def test_rejects_update_before_snapshot(self):
        with self.assertRaisesRegex(ValueError,"before initial snapshot"):
            reconstruct_jsonl(stream([rec("update")]),sample_every=1)

    def test_rejects_unsorted_snapshot(self):
        bad=rec(bids=[["98","1","1"],["99","1","1"]])
        with self.assertRaisesRegex(ValueError,"not sorted"):
            reconstruct_jsonl(stream([bad]),sample_every=1)

    def test_rejects_wrong_instrument(self):
        bad=rec(); bad["instId"]="ETH-USDT-SWAP"
        with self.assertRaisesRegex(ValueError,"Instrument ID"):
            reconstruct_jsonl(stream([bad]),sample_every=1)


if __name__ == "__main__":
    unittest.main()
