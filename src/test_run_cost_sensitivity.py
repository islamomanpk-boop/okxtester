"""Tests for the real-world cost sensitivity scenario matrix."""

import unittest

from run_cost_sensitivity import COST_SCENARIOS


class CostSensitivityScenarioTests(unittest.TestCase):
    def test_includes_exact_baseline_cost_assumptions(self):
        baseline = [
            scenario
            for scenario in COST_SCENARIOS
            if scenario["taker_fee_rate"] == 0.0005
            and scenario["slippage_bps"] == 2.0
        ]
        self.assertEqual(len(baseline), 1)
        self.assertEqual(
            baseline[0]["scenario_id"],
            "baseline_fees_0_05pct_slippage_2bps",
        )

    def test_scenario_ids_are_unique(self):
        scenario_ids = [
            scenario["scenario_id"] for scenario in COST_SCENARIOS
        ]
        self.assertEqual(len(scenario_ids), len(set(scenario_ids)))

    def test_contains_zero_fee_and_slippage_stress_scenarios(self):
        assumptions = {
            (scenario["taker_fee_rate"], scenario["slippage_bps"])
            for scenario in COST_SCENARIOS
        }
        self.assertIn((0.0, 2.0), assumptions)
        self.assertIn((0.0005, 0.0), assumptions)
        self.assertIn((0.0005, 5.0), assumptions)


if __name__ == "__main__":
    unittest.main()
