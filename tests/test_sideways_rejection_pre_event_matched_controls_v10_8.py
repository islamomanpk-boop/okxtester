import unittest
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v10_8 import analyze

class TestV108(unittest.TestCase):
    def frame(self):
        rows=[]
        for minimum in (3,5):
            for design in ("a","b"):
                for cov,eligible,bad,med in (("vol",2,2,0.2),("wick",2,0,0.05)):
                    rows.append({"minimum_pairs":minimum,"design":design,"definition":"broad",
                      "target_caliper_robust_sd":0.25,"covariate":cov,"strata_with_pairs":2,
                      "eligible_strata":eligible,"eligible_strata_abs_smd_over_0_10":bad,
                      "median_eligible_abs_smd":med})
        return pd.DataFrame(rows)
    def test_persistence_ranking_and_counts(self):
        p,d=analyze(self.frame())
        row=p[(p.minimum_pairs==3)&(p.covariate=="vol")].iloc[0]
        self.assertEqual(row.eligible_stratum_cells,4)
        self.assertEqual(row.imbalanced_stratum_cells,4)
        self.assertEqual(row.imbalance_rate,1.0)
        self.assertEqual(int(row.imbalance_rate_rank),1)
        self.assertEqual(len(d),4)
        self.assertTrue((d.acceptance_status=="NOT_ACCEPTED_FOR_OUTCOME_COMPARISON").all())
    def test_rejects_inconsistent_counts(self):
        x=self.frame(); x.loc[0,"eligible_strata"]=3
        with self.assertRaises(ValueError): analyze(x)
    def test_rejects_missing_columns(self):
        with self.assertRaises(ValueError): analyze(pd.DataFrame({"minimum_pairs":[3]}))
if __name__=="__main__": unittest.main()
