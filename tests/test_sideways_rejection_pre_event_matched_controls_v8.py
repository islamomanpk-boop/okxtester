import unittest
import numpy as np
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v8 import audit_common_support
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES

class V8CommonSupportTests(unittest.TestCase):
    def fixture(self):
        rows=[]
        for cls, vals in ((CLASSES[0],[0.,1.,2.,3.]),(CLASSES[1],[.2,1.2,2.2,3.2])):
            for i,v in enumerate(vals):
                r={"event_id":f"{cls}-{i}","definition":"broad","sequence_class":cls,"asset":"BTC","direction":"upper"}
                for c in COVARIATES: r[c]=v
                rows.append(r)
        eligible=pd.DataFrame(rows)
        pairs=pd.DataFrame([{"definition":"broad","target_caliper_robust_sd":.25,"pair_id":"p1","separation_event_id":f"{CLASSES[0]}-1","retest_event_id":f"{CLASSES[1]}-1","asset":"BTC","direction":"upper"},
            {"definition":"broad","target_caliper_robust_sd":.25,"pair_id":"p2","separation_event_id":f"{CLASSES[0]}-2","retest_event_id":f"{CLASSES[1]}-2","asset":"BTC","direction":"upper"}])
        return pairs,eligible
    def test_reports_reference_scale_and_support(self):
        p,e=self.fixture()
        coverage,diag,summary=audit_common_support(p,e)
        self.assertEqual(len(coverage),1)
        self.assertEqual(len(diag),len(COVARIATES))
        self.assertTrue((diag.eligible_reference_pooled_sd>0).all())
        self.assertTrue(np.isfinite(diag.smd_using_eligible_reference_sd).all())
        self.assertTrue((diag.central_90pct_range_overlap_ratio>=0).all())
    def test_reused_endpoint_rejected(self):
        p,e=self.fixture()
        p.loc[1,"separation_event_id"]=p.loc[0,"separation_event_id"]
        with self.assertRaises(ValueError): audit_common_support(p,e)
    def test_unknown_endpoint_rejected(self):
        p,e=self.fixture()
        p.loc[0,"retest_event_id"]="missing"
        with self.assertRaises(ValueError): audit_common_support(p,e)
if __name__=="__main__": unittest.main()
