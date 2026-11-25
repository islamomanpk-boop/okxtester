import unittest
import pandas as pd
from research.phase1_uptrend_data_preflight_v1 import audit_frame
class Phase1PreflightTests(unittest.TestCase):
 def frame(self):
  return pd.DataFrame({"ts":[0,60000,120000],"open":[10,10,11],"high":[11,12,12],"low":[9,9,10],"close":[10,11,11],"vol":[1,2,3]})
 def test_valid_source_passes(self):
  info,times=audit_frame(self.frame(),"BTC",expected_rows=3)
  self.assertEqual(info["rows"],3);self.assertEqual(len(times),3)
 def test_duplicate_timestamp_rejected(self):
  d=self.frame();d.loc[2,"ts"]=60000
  with self.assertRaises(ValueError):audit_frame(d,"BTC",expected_rows=3)
 def test_missing_interval_rejected(self):
  d=self.frame();d.loc[2,"ts"]=180000
  with self.assertRaises(ValueError):audit_frame(d,"BTC")
 def test_invalid_ohlc_rejected(self):
  d=self.frame();d.loc[1,"high"]=8
  with self.assertRaises(ValueError):audit_frame(d,"BTC")
 def test_unaligned_timestamp_rejected(self):
  d=self.frame();d.loc[1,"ts"]=60001
  with self.assertRaises(ValueError):audit_frame(d,"BTC",expected_rows=3)
 def test_nonfinite_volume_rejected(self):
  d=self.frame();d.loc[1,"vol"]=float("nan")
  with self.assertRaises(ValueError):audit_frame(d,"BTC")
if __name__=="__main__":unittest.main()
