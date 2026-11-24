import tempfile, unittest
from pathlib import Path
from research.sideways_rejection_pre_event_matched_controls_v10_3 import summarize

class V103Tests(unittest.TestCase):
    def test_frontier_counts_and_diagnostics(self):
        balance=[
          {"definition":"broad","target_caliper_robust_sd":"0.25","asset":"BTC","direction":"upper","covariate":"wick","abs_smd":"0.20"},
          {"definition":"broad","target_caliper_robust_sd":"0.25","asset":"BTC","direction":"upper","covariate":"vol","abs_smd":"0.05"},
          {"definition":"broad","target_caliper_robust_sd":"0.25","asset":"ETH","direction":"lower","covariate":"wick","abs_smd":"0.30"},
          {"definition":"broad","target_caliper_robust_sd":"0.25","asset":"ETH","direction":"lower","covariate":"vol","abs_smd":"0.10"}]
        pairs=[{"definition":"broad","target_caliper_robust_sd":"0.25"} for _ in range(3)]
        feas=[{"definition":"broad","target_caliper_robust_sd":"0.25","independent_maximum_feasible_pairs":"4"}]
        f,r=summarize(balance,pairs,feas)
        self.assertEqual(f[0]["matched_pairs"],3)
        self.assertEqual(f[0]["independent_maximum_feasible_pairs"],4)
        self.assertEqual(f[0]["cells_abs_smd_gt_0_10"],2)
        self.assertEqual(r[0]["covariate"],"wick")
    def test_missing_feasibility_rejected(self):
        with self.assertRaises(ValueError):
            summarize([{"definition":"broad","target_caliper_robust_sd":"0.25","asset":"BTC","direction":"upper","covariate":"x","abs_smd":"0.1"}],
              [{"definition":"broad","target_caliper_robust_sd":"0.25"}],[])
if __name__=="__main__": unittest.main()
