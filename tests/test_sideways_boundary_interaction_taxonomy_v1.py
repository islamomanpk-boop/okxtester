"""Unit tests for the independent candle-level sideways boundary taxonomy V1."""

import unittest
from types import SimpleNamespace

from research.sideways_boundary_interaction_taxonomy.sideways_boundary_interaction_taxonomy_v1 import (
    classify_side,
    classify_candle,
    strong_rejection_reference,
)


U = 110.0
L = 100.0


class TestUpperBoundaryTaxonomy(unittest.TestCase):
    def classify(self, open_, high, low, close, band=0.10):
        return classify_side("UPPER", open_, high, low, close, U, L, band)

    def test_close_outside_has_highest_priority(self):
        result = self.classify(109.0, 112.0, 108.0, 110.01)
        self.assertEqual(result["interaction_class"], "CLOSE_OUTSIDE")
        self.assertTrue(result["closed_outside"])

    def test_reentry_from_outside_is_distinct(self):
        result = self.classify(111.0, 112.0, 108.0, 110.0)
        self.assertEqual(result["interaction_class"], "REENTRY_INSIDE")
        self.assertTrue(result["opened_outside"])
        self.assertTrue(result["returned_inside_after_outside"])

    def test_wick_penetration_requires_open_inside_or_at_boundary(self):
        result = self.classify(109.0, 110.1, 108.0, 109.5)
        self.assertEqual(result["interaction_class"], "WICK_PENETRATION")
        self.assertTrue(result["strict_penetration"])
        self.assertAlmostEqual(result["penetration_depth_w"], 0.01)

    def test_exact_touch_is_not_penetration(self):
        result = self.classify(109.0, 110.0, 108.0, 109.5)
        self.assertEqual(result["interaction_class"], "BOUNDARY_TOUCH")
        self.assertTrue(result["exact_boundary_contact"])
        self.assertFalse(result["strict_penetration"])
        self.assertEqual(result["penetration_depth_w"], 0.0)

    def test_touch_does_not_count_as_approach(self):
        result = self.classify(109.0, 110.0, 108.0, 109.5, 0.15)
        self.assertFalse(result["approach"])

    def test_approach_band_thresholds_are_distinct(self):
        # High is 0.08 channel widths inside the upper boundary.
        at_8pct = self.classify(108.0, 109.2, 107.0, 108.5, 0.05)
        at_10pct = self.classify(108.0, 109.2, 107.0, 108.5, 0.10)
        at_15pct = self.classify(108.0, 109.2, 107.0, 108.5, 0.15)
        self.assertEqual(at_8pct["interaction_class"], "NO_APPROACH")
        self.assertEqual(at_10pct["interaction_class"], "APPROACH_ONLY")
        self.assertEqual(at_15pct["interaction_class"], "APPROACH_ONLY")

    def test_no_approach(self):
        result = self.classify(105.0, 107.0, 104.0, 106.0)
        self.assertEqual(result["interaction_class"], "NO_APPROACH")

    def test_close_exactly_at_boundary_is_not_outside(self):
        result = self.classify(109.0, 110.2, 108.0, 110.0)
        self.assertEqual(result["interaction_class"], "WICK_PENETRATION")
        self.assertFalse(result["closed_outside"])


class TestLowerBoundaryTaxonomy(unittest.TestCase):
    def classify(self, open_, high, low, close, band=0.10):
        return classify_side("LOWER", open_, high, low, close, U, L, band)

    def test_lower_close_outside(self):
        result = self.classify(101.0, 102.0, 98.0, 99.99)
        self.assertEqual(result["interaction_class"], "CLOSE_OUTSIDE")

    def test_lower_reentry(self):
        result = self.classify(99.0, 102.0, 98.0, 100.0)
        self.assertEqual(result["interaction_class"], "REENTRY_INSIDE")
        self.assertTrue(result["returned_inside_after_outside"])

    def test_lower_wick_penetration(self):
        result = self.classify(101.0, 102.0, 99.9, 100.5)
        self.assertEqual(result["interaction_class"], "WICK_PENETRATION")
        self.assertAlmostEqual(result["penetration_depth_w"], 0.01)

    def test_lower_exact_touch(self):
        result = self.classify(101.0, 102.0, 100.0, 100.5)
        self.assertEqual(result["interaction_class"], "BOUNDARY_TOUCH")
        self.assertTrue(result["exact_boundary_contact"])
        self.assertFalse(result["strict_penetration"])

    def test_lower_approach(self):
        result = self.classify(102.0, 103.0, 100.8, 101.0, 0.10)
        self.assertEqual(result["interaction_class"], "APPROACH_ONLY")


class TestCandleAndReferenceFlags(unittest.TestCase):
    def test_dual_boundary_flag_uses_15_percent_band(self):
        row = SimpleNamespace(open=101.0, high=109.5, low=100.5, close=105.0)
        upper, lower, dual = classify_candle(row, U, L)
        self.assertTrue(dual)
        self.assertEqual(upper[0.15]["interaction_class"], "APPROACH_ONLY")
        self.assertEqual(lower[0.15]["interaction_class"], "APPROACH_ONLY")

    def test_strong_rejection_reference_keeps_outer_zone_definition(self):
        self.assertTrue(strong_rejection_reference("UPPER", 109.5, 108.0, 108.8, U, L))
        self.assertTrue(strong_rejection_reference("LOWER", 102.0, 100.5, 101.2, U, L))
        self.assertFalse(strong_rejection_reference("UPPER", 108.0, 107.0, 108.0, U, L))

    def test_invalid_side_and_nonpositive_width_rejected(self):
        with self.assertRaises(ValueError):
            classify_side("MIDDLE", 105, 106, 104, 105, U, L, 0.10)
        with self.assertRaises(ValueError):
            classify_side("UPPER", 105, 106, 104, 105, L, U, 0.10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
