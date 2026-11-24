import unittest
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v10_6 import summarize, MIN_PAIRS

class V106Tests(unittest.TestCase):
    def test_excludes_small_strata_from_stable_balance(self):
        rows=[]
        for n,smd in [(4,0.9),(5,0.2),(8,0.05)]:
            rows.append(dict(design="d",definition="broad",target_caliper_robust_sd=0.25,
                asset_direction=f"A|{n}",matched_pairs=n,covariate="x",
                abs_smd_after=smd,small_stratum_flag=n<MIN_PAIRS))
        detail,overall=summarize(pd.DataFrame(rows))
        row=detail.iloc[0]
        self.assertEqual(row.stable_strata_n,2)
        self.assertEqual(row.stable_strata_abs_smd_over_0_10,1)
        self.assertEqual(row.unstable_strata_n,1)
        self.assertEqual(overall.iloc[0].acceptance_status,"NOT_ACCEPTED_FOR_OUTCOME_COMPARISON")
    def test_missing_columns_fail_closed(self):
        with self.assertRaises(ValueError):
            summarize(pd.DataFrame({"design":["d"]}))

if __name__=="__main__": unittest.main()
