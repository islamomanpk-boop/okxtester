import unittest
from research.sideways_rejection_pre_event_matched_controls_v10_5 import MIN_PAIRS_STABLE
from research.sideways_rejection_pre_event_matched_controls_v10_4 import DESIGNS

class V105Tests(unittest.TestCase):
    def test_reuses_frozen_v10_4_design_grid(self):
        self.assertEqual(len(DESIGNS), 6)
        self.assertEqual(DESIGNS[0], ("v6_frozen", 1.5, 30.0))
    def test_small_strata_are_flagged(self):
        self.assertEqual(MIN_PAIRS_STABLE, 5)

if __name__ == "__main__":
    unittest.main()
