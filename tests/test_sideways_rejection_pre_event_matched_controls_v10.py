import unittest
import numpy as np
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES
from research.sideways_rejection_pre_event_matched_controls_v10 import audit_structure

class V10StructureTests(unittest.TestCase):
    def fixture(self):
        rows=[]
        for cls,off in ((CLASSES[0],0.0),(CLASSES[1],0.1)):
            for asset in ("BTC","ETH"):
                for i in range(8):
                    r={"event_id":f"{cls}-{asset}-{i}","definition":"broad","sequence_class":cls,"asset":asset,"direction":"upper"}
                    for j,c in enumerate(COVARIATES): r[c]=float(i+off)*(j+1)+(.01*j*i*i)
                    rows.append(r)
        eligible=pd.DataFrame(rows)
        pairs=pd.DataFrame([{"definition":"broad","target_caliper_robust_sd":.25,"asset":"BTC","direction":"upper",
          "separation_event_id":f"{CLASSES[0]}-BTC-0","retest_event_id":f"{CLASSES[1]}-BTC-0"}])
        feasibility=pd.DataFrame([{"definition":"broad","target_caliper_robust_sd":.25,"asset":"BTC","direction":"upper",
          "candidate_edges":2,"edges_if_overall_distance_removed":4,"edges_if_component_limit_removed":5,
          "edges_if_target_caliper_removed":6,"edges_if_time_gap_removed":7}])
        return eligible,pairs,feasibility
    def test_outputs_and_bottleneck(self):
        e,p,f=self.fixture()
        s,b,a,k=audit_structure(e,p,f)
        self.assertGreater(len(s),0); self.assertEqual(len(b),len(COVARIATES))
        self.assertEqual(len(a),len(COVARIATES))
        self.assertEqual(k.iloc[0]["additional_edges_if_time_gap_removed"],5)
    def test_duplicate_ids_rejected(self):
        e,p,f=self.fixture(); e.loc[1,"event_id"]=e.loc[0,"event_id"]
        with self.assertRaises(ValueError): audit_structure(e,p,f)
    def test_missing_feasibility_field_rejected(self):
        e,p,f=self.fixture()
        with self.assertRaises(ValueError): audit_structure(e,p,f.drop(columns=["candidate_edges"]))
if __name__=="__main__": unittest.main()
