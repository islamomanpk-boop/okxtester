import unittest
import numpy as np
import pandas as pd

from research.sideways_rejection_matched_asset_robustness_v1 import paired_block_bootstrap


class AssetRobustnessTests(unittest.TestCase):
    def test_small_samples_do_not_claim_bootstrap_interval(self):
        frame = pd.DataFrame({"pair_confirmation_ts_ms": [1760000000000] * 4,
                              "difference": [1.0, 2.0, 3.0, 4.0]})
        result = paired_block_bootstrap(frame, block_days=3, replicates=100,
                                        rng=np.random.default_rng(11))
        self.assertEqual(result["bootstrap_status"], "too_few_pairs")
        self.assertTrue(np.isnan(result["ci_2_5"]))

    def test_calendar_block_bootstrap_runs_for_five_pairs(self):
        frame = pd.DataFrame({"pair_confirmation_ts_ms": [
            1760000000000, 1760000060000, 1760086400000, 1760086460000, 1760172800000],
            "difference": [1.0, 2.0, 3.0, 4.0, 5.0]})
        result = paired_block_bootstrap(frame, block_days=1, replicates=200,
                                        rng=np.random.default_rng(11))
        self.assertEqual(result["bootstrap_status"], "complete")
        self.assertEqual(result["valid_replicates"], 200)
        self.assertLessEqual(result["ci_2_5"], result["ci_97_5"])


if __name__ == "__main__":
    unittest.main()
