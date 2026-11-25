import unittest
import numpy as np
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v10_9 import audit_distributional_overlap
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES,CLASSES

class V109Tests(unittest.TestCase):
    def fixture(self):
        rows=[]
        for cls,vals in ((CLASSES[0],[0.,1.,2.,3.,4.]),(CLASSES[1],[0.,1.,2.,3.,4.])):
            for i,v in enumerate(vals):
                r={"event_id":f"{cls}-{i}","definition":"broad","sequence_class":cls,"asset":"BTC","direction":"upper"}
                for c in COVARIATES:r[c]=v
                rows.append(r)
        eligible=pd.DataFrame(rows)
        pairs=pd.DataFrame([
          {"definition":"broad","target_caliper_robust_sd":.25,"pair_id":"p1","separation_event_id":f"{CLASSES[0]}-1","retest_event_id":f"{CLASSES[1]}-1","asset":"BTC","direction":"upper"},
          {"definition":"broad","target_caliper_robust_sd":.25,"pair_id":"p2","separation_event_id":f"{CLASSES[0]}-2","retest_event_id":f"{CLASSES[1]}-2","asset":"BTC","direction":"upper"}])
        return pairs,eligible
    def test_identical_distributions(self):
        p,e=self.fixture(); d,s=audit_distributional_overlap(p,e)
        self.assertEqual(len(d),len(COVARIATES))
        self.assertTrue(np.allclose(d.ks_statistic,0))
        self.assertTrue(np.allclose(d.wasserstein_distance,0))
        self.assertTrue((d.matched_endpoints_inside_shared_central90_fraction==1).all())
        self.assertEqual(s.iloc[0].acceptance_status,"NOT_ACCEPTED_FOR_OUTCOME_COMPARISON")
    def test_shifted_distribution_detected(self):
        p,e=self.fixture()
        mask=e.sequence_class==CLASSES[1]
        for c in COVARIATES:e.loc[mask,c]=e.loc[mask,c]+10
        d,_=audit_distributional_overlap(p,e)
        self.assertTrue((d.wasserstein_distance>0).all())
        self.assertTrue((d.ks_statistic>0).all())
    def test_duplicate_endpoint_rejected(self):
        p,e=self.fixture();p.loc[1,"separation_event_id"]=p.loc[0,"separation_event_id"]
        with self.assertRaises(ValueError):audit_distributional_overlap(p,e)
    def test_unknown_endpoint_rejected(self):
        p,e=self.fixture();p.loc[0,"retest_event_id"]="missing"
        with self.assertRaises(ValueError):audit_distributional_overlap(p,e)
if __name__=="__main__":unittest.main()
