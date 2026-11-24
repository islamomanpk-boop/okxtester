import unittest
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES
from research.sideways_rejection_pre_event_matched_controls_v5 import TARGET
from research.sideways_rejection_pre_event_matched_controls_v6 import optimal_match

class OptimalMatchingTests(unittest.TestCase):
    def frame(self):
        rows=[]
        # Greedy nearest edge can consume the only control available to the
        # second event; optimal assignment should retain two valid pairs.
        for cls, vals in [("SEPARATION_FIRST",[0.0,0.4]),("RETEST_FIRST",[0.1,0.8])]:
            for i,x in enumerate(vals):
                r={"event_id":f"{cls}-{i}","sequence_class":cls,"asset":"BTC",
                   "direction":"upper","confirmation_ts_ms":1760000000000+i*60000,
                   "confirmation_month":"2025-10"}
                for c in COVARIATES:r[c]=x
                r[TARGET]=x
                rows.append(r)
        return pd.DataFrame(rows)
    def test_one_to_one_and_within_strata(self):
        p=optimal_match(self.frame(),2.0)
        self.assertEqual(len(p),2)
        self.assertEqual(p.separation_event_id.nunique(),2)
        self.assertEqual(p.retest_event_id.nunique(),2)
        self.assertTrue((p.match_time_gap_days<=30).all())
    def test_target_caliper_enforced(self):
        p=optimal_match(self.frame(),0.01)
        self.assertTrue((p.target_abs_difference_robust_sd<=0.01).all())
    def test_duplicate_ids_rejected(self):
        f=self.frame(); f.loc[1,"event_id"]=f.loc[0,"event_id"]
        with self.assertRaises(ValueError): optimal_match(f,1.0)
if __name__=="__main__": unittest.main()
