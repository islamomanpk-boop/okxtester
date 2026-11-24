import unittest
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v10_7 import analyze

class V107Tests(unittest.TestCase):
    def frame(self):
        rows=[]
        for n,smd in [(2,.5),(4,.2),(6,.05),(9,.3),(12,.4)]:
            rows.append({"design":"d","definition":"broad","target_caliper_robust_sd":.25,
              "asset_direction":"BTC_up","matched_pairs":n,"covariate":"volatility","abs_smd_after":smd})
        return pd.DataFrame(rows)
    def test_thresholds_are_monotonic_in_eligible_counts(self):
        detail,summary=analyze(self.frame())
        counts=summary.sort_values("minimum_pairs").eligible_cells.tolist()
        self.assertEqual(counts,[5,4,3,2])
    def test_missing_columns_fail_closed(self):
        with self.assertRaises(ValueError): analyze(pd.DataFrame({"matched_pairs":[5]}))
    def test_no_outcome_fields_required(self):
        d,s=analyze(self.frame())
        self.assertTrue((s.acceptance_status=="NOT_ACCEPTED_FOR_OUTCOME_COMPARISON").all())
