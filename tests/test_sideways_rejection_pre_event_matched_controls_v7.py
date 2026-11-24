import unittest
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v7 import audit_pairs

class V7AuditTests(unittest.TestCase):
    def fixture(self):
        anatomy = pd.DataFrame([
            {"event_id":"a1","asset":"BTC","direction":"upper","definition":"broad","test_start_ts_ms":0,"confirmation_ts_ms":60000,"x":1.0},
            {"event_id":"b1","asset":"BTC","direction":"upper","definition":"broad","test_start_ts_ms":30000,"confirmation_ts_ms":90000,"x":1.2},
            {"event_id":"a2","asset":"BTC","direction":"upper","definition":"broad","test_start_ts_ms":50000,"confirmation_ts_ms":120000,"x":1.1},
            {"event_id":"b2","asset":"BTC","direction":"upper","definition":"broad","test_start_ts_ms":110000,"confirmation_ts_ms":180000,"x":1.3},
        ])
        pairs = pd.DataFrame([
            {"definition":"broad","target_caliper_robust_sd":0.25,"pair_id":"p1","separation_event_id":"a1","retest_event_id":"b1","asset":"BTC","direction":"upper","match_time_gap_days":0.1,"match_distance_rms_robust_sd":0.2,"target_abs_difference_robust_sd":0.1},
            {"definition":"broad","target_caliper_robust_sd":0.25,"pair_id":"p2","separation_event_id":"a2","retest_event_id":"b2","asset":"BTC","direction":"upper","match_time_gap_days":0.2,"match_distance_rms_robust_sd":0.3,"target_abs_difference_robust_sd":0.2},
        ])
        return pairs, anatomy
    def test_reports_coverage_balance_and_overlaps(self):
        p,a=self.fixture()
        strata,balance,summary=audit_pairs(p,a)
        self.assertEqual(len(strata),1)
        self.assertEqual(strata.iloc[0].matched_pairs,2)
        self.assertEqual(len(balance),1)
        self.assertEqual(summary.iloc[0].pairs_with_cross_pair_window_overlap,2)
    def test_event_reuse_rejected(self):
        p,a=self.fixture()
        p.loc[1,"separation_event_id"]="a1"
        with self.assertRaises(ValueError): audit_pairs(p,a)
    def test_stratum_mismatch_rejected(self):
        p,a=self.fixture()
        a.loc[a.event_id=="b1","asset"]="ETH"
        with self.assertRaises(ValueError): audit_pairs(p,a)
if __name__=="__main__": unittest.main()
