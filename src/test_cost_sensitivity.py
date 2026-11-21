import unittest

from run_cost_sensitivity import COST_SCENARIOS


class TestCostSensitivity(unittest.TestCase):
    def test_three_distinct_cost_scenarios_exist(self):
        self.assertEqual(len(COST_SCENARIOS), 3)
        self.assertEqual(
            len({item["scenario_id"] for item in COST_SCENARIOS}), 3
        )

    def test_zero_fee_scenario_keeps_two_bps_slippage(self):
        scenario = COST_SCENARIOS[0]
        self.assertEqual(scenario["taker_fee_rate"], 0.0)
        self.assertEqual(scenario["slippage_bps"], 2.0)

    def test_zero_slippage_scenario_keeps_baseline_fee(self):
        scenario = COST_SCENARIOS[1]
        self.assertEqual(scenario["taker_fee_rate"], 0.0005)
        self.assertEqual(scenario["slippage_bps"], 0.0)

    def test_high_slippage_scenario_keeps_baseline_fee(self):
        scenario = COST_SCENARIOS[2]
        self.assertEqual(scenario["taker_fee_rate"], 0.0005)
        self.assertEqual(scenario["slippage_bps"], 5.0)


if __name__ == "__main__":
    unittest.main()
