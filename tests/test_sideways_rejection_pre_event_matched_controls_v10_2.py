import unittest
import numpy as np
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES
from research.sideways_rejection_pre_event_matched_controls_v10_2 import audit

class V102Tests(unittest.TestCase):
    def setUp(self):
        rows=[]
        for cls,offset in [("SEPARATION_FIRST",0.0),("RETEST_FIRST",0.2)]:
            for i in range(12):
                r={"event_id":f"{cls}-{i}","definition":"broad","sequence_class":cls,"asset":"BTC","direction":"upper"}
                for j,c in enumerate(COVARIATES): r[c]=float(i+j+offset)
                rows.append(r)
        self.eligible=pd.DataFrame(rows)
        self.pairs=pd.DataFrame([{"definition":"broad","target_caliper_robust_sd":0.25,
            "separation_event_id":f"SEPARATION_FIRST-{i}","retest_event_id":f"RETEST_FIRST-{i}",
            "asset":"BTC","direction":"upper"} for i in range(6)])
        self.corr=pd.DataFrame([{"definition":"broad","asset":"BTC","direction":"upper",
            "sequence_class":"SEPARATION_FIRST","scope":"within_sequence_class",
            "covariate_a":COVARIATES[0],"covariate_b":COVARIATES[1],
            "correlation":0.95,"abs_correlation":0.95}])
    def test_outputs_and_flags(self):
        red,balance,attr,high=audit(self.eligible,self.pairs,self.corr)
        self.assertEqual(len(balance),len(COVARIATES))
        self.assertEqual(len(attr),len(COVARIATES))
        self.assertEqual(len(high),1)
        self.assertGreaterEqual(red.iloc[0].groups_ge_0_90,1)
    def test_unknown_pair_event_rejected(self):
        bad=self.pairs.copy(); bad.loc[0,"separation_event_id"]="missing"
        with self.assertRaises(ValueError): audit(self.eligible,bad,self.corr)

if __name__=="__main__": unittest.main()
