import unittest
import numpy as np
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES, CLASSES
from research.sideways_rejection_pre_event_matched_controls_v5 import CALIPERS
from research.sideways_rejection_pre_event_matched_controls_v9 import audit_feasibility

class V9FeasibilityTests(unittest.TestCase):
    def fixture(self):
        rows=[]
        for cls, offset in ((CLASSES[0],0.0),(CLASSES[1],0.05)):
            for i in range(3):
                row={"event_id":f"{cls}-{i}","definition":"broad","sequence_class":cls,
                     "asset":"BTC","direction":"upper","confirmation_ts_ms":i*86400000}
                for c in COVARIATES: row[c]=float(i)+offset
                rows.append(row)
        frame=pd.DataFrame(rows)
        pairs=pd.DataFrame([{"definition":"broad","target_caliper_robust_sd":float(CALIPERS[0]),
            "asset":"BTC","direction":"upper","separation_event_id":f"{CLASSES[0]}-0",
            "retest_event_id":f"{CLASSES[1]}-0"}])
        return frame,pairs
    def test_independent_maximum_cardinality(self):
        frame,pairs=self.fixture()
        strata,summary=audit_feasibility(frame,pairs)
        row=summary[summary.target_caliper_robust_sd==float(CALIPERS[0])].iloc[0]
        self.assertEqual(row.independent_maximum_feasible_pairs,3)
        self.assertEqual(row.archived_v6_pairs,1)
    def test_missing_required_column_rejected(self):
        frame,pairs=self.fixture()
        with self.assertRaises(ValueError): audit_feasibility(frame.drop(columns=["asset"]),pairs)
    def test_duplicate_event_ids_rejected(self):
        frame,pairs=self.fixture()
        frame.loc[1,"event_id"]=frame.loc[0,"event_id"]
        with self.assertRaises(ValueError): audit_feasibility(frame,pairs)
if __name__=="__main__": unittest.main()
