import unittest
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v10_11 import percentile_sensitivity,RANGES
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES,CLASSES
class V1011Tests(unittest.TestCase):
 def fixture(self):
  rows=[]
  for cls,vals in ((CLASSES[0],[0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.]),(CLASSES[1],[0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.])):
   for i,v in enumerate(vals):
    r={"event_id":f"{cls}-{i}","definition":"broad","sequence_class":cls,"asset":"BTC","direction":"upper"}
    for j,c in enumerate(COVARIATES):r[c]=v+j*.01
    rows.append(r)
  e=pd.DataFrame(rows);p=pd.DataFrame([{"definition":"broad","target_caliper_robust_sd":.25,"pair_id":"p1","separation_event_id":f"{CLASSES[0]}-9","retest_event_id":f"{CLASSES[1]}-9","asset":"BTC","direction":"upper"}])
  return p,e
 def test_identical_distributions_retain_pair_all_ranges(self):
  p,e=self.fixture();d,s=percentile_sensitivity(p,e)
  self.assertEqual(set(d.range),set(RANGES));self.assertTrue((d.pairs_both_endpoints_in_joint_support==1).all())
 def test_shifted_dimension_changes_support_by_range(self):
  p,e=self.fixture();m=e.sequence_class==CLASSES[1]
  # Shift one dimension enough to separate central 90/80 while retaining a tail overlap at 98.
  c=COVARIATES[0];e.loc[m,c]=e.loc[m,c]+8.5
  d,_=percentile_sensitivity(p,e);z=d.set_index("range")
  self.assertEqual(int(z.loc["central_98","nonoverlap_dimensions"]),0)
  self.assertEqual(int(z.loc["central_98","pairs_both_endpoints_in_joint_support"]),1)
  self.assertEqual(int(z.loc["central_80","nonoverlap_dimensions"]),1)
  self.assertEqual(int(z.loc["central_80","pairs_both_endpoints_in_joint_support"]),0)
 def test_disjoint_dimension_empties_joint_support(self):
  p,e=self.fixture();m=e.sequence_class==CLASSES[1];e.loc[m,COVARIATES[0]]+=100
  d,_=percentile_sensitivity(p,e);self.assertTrue((d.nonoverlap_dimensions>0).all());self.assertTrue((d.pairs_both_endpoints_in_joint_support==0).all())
 def test_reused_endpoint_rejected(self):
  p,e=self.fixture();p.loc[0,"retest_event_id"]=p.loc[0,"separation_event_id"]
  with self.assertRaises(ValueError):percentile_sensitivity(p,e)
 def test_missing_endpoint_rejected(self):
  p,e=self.fixture();p.loc[0,"retest_event_id"]="missing"
  with self.assertRaises(ValueError):percentile_sensitivity(p,e)
if __name__=="__main__":unittest.main()
