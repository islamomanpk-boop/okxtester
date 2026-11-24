import unittest
import numpy as np
import pandas as pd

from research.sideways_rejection_pre_event_matched_controls_v4 import (
    COVARIATES, greedy_match, paired_block_bootstrap,
)


class MatchedControlTests(unittest.TestCase):
    def frame(self):
        rows = []
        for label, offsets in (("SEPARATION_FIRST", [0.0, 1.0]),
                               ("RETEST_FIRST", [0.05, 1.05])):
            for i, x in enumerate(offsets):
                row = {"event_id": f"{label}-{i}", "sequence_class": label,
                       "asset": "BTC", "direction": "upper",
                       "confirmation_month": "2025-10",
                       "confirmation_ts_ms": 1760000000000 + i * 60000 + (0 if label == "SEPARATION_FIRST" else 30000)}
                row.update({c: x for c in COVARIATES})
                rows.append(row)
        return pd.DataFrame(rows)

    def test_greedy_match_is_one_to_one_and_within_strata(self):
        pairs = greedy_match(self.frame(), max_distance=3.0)
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs.separation_event_id.nunique(), 2)
        self.assertEqual(pairs.retest_event_id.nunique(), 2)

    def test_no_cross_asset_or_month_matches(self):
        f = self.frame()
        f.loc[f.sequence_class == "RETEST_FIRST", "asset"] = "ETH"
        self.assertTrue(greedy_match(f).empty)

    def test_rejects_pairs_outside_30_day_time_window(self):
        f = self.frame()
        mask = f.sequence_class == "RETEST_FIRST"
        f.loc[mask, "confirmation_ts_ms"] += 31 * 86400000
        self.assertTrue(greedy_match(f).empty)

    def test_paired_block_bootstrap_returns_observed_mean(self):
        d = pd.DataFrame({"pair_confirmation_ts_ms": [
            1760000000000, 1760000060000, 1760086400000, 1760086460000],
            "difference": [1.0, 2.0, 3.0, 4.0]})
        r = paired_block_bootstrap(d, block_days=1, replicates=200,
                                   rng=np.random.default_rng(7))
        self.assertAlmostEqual(r["observed_difference"], 2.5)
        self.assertEqual(r["pairs"], 4)
        self.assertEqual(r["valid_replicates"], 200)


if __name__ == "__main__":
    unittest.main()
