import unittest
import numpy as np
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v10_10 import joint_support_audit
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES,CLASSES

class V1010Tests(unittest.TestCase):
    def fixture(self):
        rows=[]
        for cls,vals in ((CLASSES[0],[0.,1.,2.,3.,4.,5.]),(CLASSES[1],[0.,1.,2.,3.,4.,5.])):
            for i,v in enumerate(vals):
                r={"event_id":f"{cls}-{i}","definition":"broad","sequence_class":cls,"asset":"BTC","direction":"upper"}
                for c in COVARIATES:r[c]=v
                rows.append(r)
        e=pd.DataFrame(rows)
        p=pd.DataFrame([
          {"definition":"broad","target_caliper_robust_sd":.25,"pair_id":"p1","separation_event_id":f"{CLASSES[0]}-2","retest_event_id":f"{CLASSES[1]}-2","asset":"BTC","direction":"upper"},
          {"definition":"broad","target_caliper_robust_sd":.25,"pair_id":"p2","separation_event_id":f"{CLASSES[0]}-3","retest_event_id":f"{CLASSES[1]}-3","asset":"BTC","direction":"upper"}])
        return p,e
    def test_identical_classes_retain_matched_pairs(self):
        p,e=self.fixture();d,s=joint_support_audit(p,e)
        self.assertEqual(len(d),len(COVARIATES))
        self.assertEqual(int(d.iloc[0].pairs_both_endpoints_in_joint_support),2)
        self.assertEqual(float(s.iloc[0].matched_pair_joint_retention),1.0)
    def test_disjoint_dimension_means_no_joint_support(self):
        p,e=self.fixture();m=e.sequence_class==CLASSES[1];e.loc[m,COVARIATES[0]]=e.loc[m,COVARIATES[0]]+100
        d,_=joint_support_audit(p,e)
        self.assertTrue((d.nonoverlap_dimensions>=1).all())
        self.assertTrue((d.pairs_both_endpoints_in_joint_support==0).all())
    def test_reused_endpoint_rejected(self):
        p,e=self.fixture();p.loc[1,"separation_event_id"]=p.loc[0,"separation_event_id"]
        with self.assertRaises(ValueError):joint_support_audit(p,e)
    def test_unknown_endpoint_rejected(self):
        p,e=self.fixture();p.loc[0,"retest_event_id"]="missing"
        with self.assertRaises(ValueError):joint_support_audit(p,e)
if __name__=="__main__":unittest.main()
