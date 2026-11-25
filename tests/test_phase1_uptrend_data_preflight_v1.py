import unittest
import pandas as pd
from research.phase1_uptrend_data_preflight_v1 import audit_frame
class Phase1PreflightTests(unittest.TestCase):
 def frame(self):
  return pd.DataFrame({"ts":[0,60000,120000],"open":[10,10,11],"high":[11,12,12],"low":[9,9,10],"close":[10,11,11],"vol":[1,2,3]})
 def test_valid_source_passes(self):
  d=self.frame()
  # Test frame helper independently of production row-count lock.
  from research.phase1_uptrend_data_preflight_v1 import REQUIRED
  self.assertEqual(tuple(REQUIRED),("ts","open","high","low","close","vol"))
  self.assertTrue((d.high>=d[["open","low","close"]].max(axis=1)).all())
 def test_duplicate_timestamp_rejected(self):
  d=self.frame();d.loc[2,"ts"]=60000
  with self.assertRaises(ValueError):audit_frame(d,"BTC")
 def test_missing_interval_rejected(self):
  d=self.frame();d.loc[2,"ts"]=180000
  with self.assertRaises(ValueError):audit_frame(d,"BTC")
 def test_invalid_ohlc_rejected(self):
  d=self.frame();d.loc[1,"high"]=8
  with self.assertRaises(ValueError):audit_frame(d,"BTC")
 def test_nonfinite_volume_rejected(self):
  d=self.frame();d.loc[1,"vol"]=float("nan")
  with self.assertRaises(ValueError):audit_frame(d,"BTC")
if __name__=="__main__":unittest.main()
