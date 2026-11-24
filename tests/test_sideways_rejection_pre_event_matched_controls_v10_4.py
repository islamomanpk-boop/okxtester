import unittest
from research.sideways_rejection_pre_event_matched_controls_v10_4 import DESIGNS
class V104Tests(unittest.TestCase):
 def test_baseline_is_frozen_v6(self):
  self.assertEqual(DESIGNS[0],("v6_frozen",1.5,30.0))
 def test_relaxations_are_predeclared_and_do_not_tighten_target_caliper(self):
  self.assertTrue(any(x[1]>1.5 for x in DESIGNS))
  self.assertTrue(any(x[2]>30 for x in DESIGNS))
  self.assertEqual(len({x[0] for x in DESIGNS}),len(DESIGNS))
if __name__=="__main__":unittest.main()
