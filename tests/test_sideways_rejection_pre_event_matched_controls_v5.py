import unittest
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES
from research.sideways_rejection_pre_event_matched_controls_v5 import match_with_target_caliper, TARGET


class V5CaliperTests(unittest.TestCase):
    def frame(self):
        rows=[]
        for asset in ["BTC","ETH"]:
            for direction in ["UPPER","LOWER"]:
                for cls,offset in [("SEPARATION_FIRST",0.0),("RETEST_FIRST",0.1)]:
                    r={"event_id":f"{asset}-{direction}-{cls}","sequence_class":cls,
                       "asset":asset,"direction":direction,"confirmation_ts_ms":1760000000000,
                       "confirmation_month":"2025-10"}
                    for c in COVARIATES:r[c]=1.0+offset
                    r[TARGET]=offset
                    rows.append(r)
        return pd.DataFrame(rows)

    def test_target_caliper_retains_balanced_pairs(self):
        pairs=match_with_target_caliper(self.frame(),0.5)
        self.assertEqual(len(pairs),4)
        self.assertTrue((pairs.target_abs_difference_robust_sd<=0.5).all())

    def test_tight_target_caliper_rejects_pairs(self):
        frame=self.frame()
        frame.loc[frame.sequence_class=="RETEST_FIRST",TARGET]=100.0
        pairs=match_with_target_caliper(frame,0.25)
        self.assertEqual(len(pairs),0)

    def test_duplicate_event_ids_rejected(self):
        frame=self.frame()
        frame.loc[1,"event_id"]=frame.loc[0,"event_id"]
        with self.assertRaises(ValueError):match_with_target_caliper(frame,0.5)


if __name__=="__main__":unittest.main()
