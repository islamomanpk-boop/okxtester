import unittest

from exit_experiment_config import (
    build_baseline_experiments,
    build_experiment_matrix,
    resolve_exit_prices,
    validate_experiment_matrix,
)


class ExitExperimentConfigTests(unittest.TestCase):

    def setUp(self):
        self.candidate_long = {
            "side": 1,
            "signal_high": 102.0,
            "signal_low": 98.0,
            "signal_atr14": 2.0,
        }
        self.candidate_short = {
            "side": -1,
            "signal_high": 102.0,
            "signal_low": 98.0,
            "signal_atr14": 2.0,
        }

    def find(self, experiments, stop, target, trailing="none"):
        return next(
            x for x in experiments
            if x.stop_model == stop
            and x.target_model == target
            and x.trailing_mode == trailing
        )

    def test_matrix_has_66_unique_experiments(self):
        matrix = build_experiment_matrix()
        self.assertEqual(len(matrix), 66)
        self.assertEqual(len({x.experiment_id for x in matrix}), 66)

    def test_groups_have_22_each(self):
        matrix = build_experiment_matrix()
        self.assertEqual(
            sum(x.trailing_mode == "none" for x in matrix), 22
        )
        self.assertEqual(
            sum(x.trailing_mode == "trailing_stop_loss" for x in matrix), 22
        )
        self.assertEqual(
            sum(x.trailing_mode == "trailing_take_profit" for x in matrix), 22
        )

    def test_original_16_fixed_target_combinations_are_preserved(self):
        baseline = build_baseline_experiments()
        fixed = [
            x for x in baseline
            if x.target_model.startswith("fixed_target")
        ]
        self.assertEqual(len(fixed), 16)

    def test_six_candle_stop_r_multiple_combinations_exist(self):
        baseline = build_baseline_experiments()
        r_tests = [
            x for x in baseline
            if x.target_model in ("target_1R", "target_1_5R", "target_2R")
        ]
        self.assertEqual(len(r_tests), 6)

    def test_exact_long_stop_uses_signal_low(self):
        matrix = build_baseline_experiments()
        exp = self.find(
            matrix, "signal_extreme_exact", "target_1R"
        )
        result = resolve_exit_prices(exp, self.candidate_long, 100)
        self.assertEqual(result["stop_price"], 98.0)
        self.assertEqual(result["target_price"], 102.0)

    def test_exact_short_stop_uses_signal_high(self):
        matrix = build_baseline_experiments()
        exp = self.find(
            matrix, "signal_extreme_exact", "target_1R"
        )
        result = resolve_exit_prices(exp, self.candidate_short, 100)
        self.assertEqual(result["stop_price"], 102.0)
        self.assertEqual(result["target_price"], 98.0)

    def test_buffered_long_stop_uses_point_one_atr(self):
        matrix = build_baseline_experiments()
        exp = self.find(
            matrix, "signal_extreme_atr_buffer_0_10", "target_1R"
        )
        result = resolve_exit_prices(exp, self.candidate_long, 100)
        self.assertAlmostEqual(result["stop_price"], 97.8)
        self.assertAlmostEqual(result["target_price"], 102.2)

    def test_buffered_short_stop_uses_point_one_atr(self):
        matrix = build_baseline_experiments()
        exp = self.find(
            matrix, "signal_extreme_atr_buffer_0_10", "target_1R"
        )
        result = resolve_exit_prices(exp, self.candidate_short, 100)
        self.assertAlmostEqual(result["stop_price"], 102.2)
        self.assertAlmostEqual(result["target_price"], 97.8)

    def test_r_targets_use_actual_entry_to_stop_distance(self):
        matrix = build_baseline_experiments()
        exp = self.find(
            matrix, "signal_extreme_exact", "target_1_5R"
        )
        result = resolve_exit_prices(exp, self.candidate_long, 100)
        self.assertEqual(result["risk_distance"], 2.0)
        self.assertEqual(result["target_price"], 103.0)

    def test_fixed_stop_and_target_are_entry_relative(self):
        matrix = build_baseline_experiments()
        exp = self.find(
            matrix, "fixed_stop_0_50pct", "fixed_target_0_75pct"
        )
        result = resolve_exit_prices(exp, self.candidate_long, 100)
        self.assertAlmostEqual(result["stop_price"], 99.5)
        self.assertAlmostEqual(result["target_price"], 100.75)

    def test_invalid_long_stop_side_is_rejected(self):
        matrix = build_baseline_experiments()
        exp = self.find(
            matrix, "signal_extreme_exact", "target_1R"
        )
        with self.assertRaisesRegex(ValueError, "Long stop"):
            resolve_exit_prices(exp, self.candidate_long, 97)

    def test_invalid_short_stop_side_is_rejected(self):
        matrix = build_baseline_experiments()
        exp = self.find(
            matrix, "signal_extreme_exact", "target_1R"
        )
        with self.assertRaisesRegex(ValueError, "Short stop"):
            resolve_exit_prices(exp, self.candidate_short, 103)

    def test_trailing_stop_rule_is_one_r_activation_and_distance(self):
        matrix = build_experiment_matrix()
        exp = self.find(
            matrix,
            "signal_extreme_exact",
            "target_1R",
            "trailing_stop_loss",
        )
        result = resolve_exit_prices(exp, self.candidate_long, 100)
        self.assertEqual(result["trailing_activation_r"], 1.0)
        self.assertEqual(result["trailing_distance_r"], 1.0)

    def test_trailing_tp_activates_at_original_target(self):
        matrix = build_experiment_matrix()
        exp = self.find(
            matrix,
            "signal_extreme_exact",
            "target_2R",
            "trailing_take_profit",
        )
        result = resolve_exit_prices(exp, self.candidate_long, 100)
        self.assertTrue(result["trailing_activation_at_target"])
        self.assertEqual(result["trailing_distance_r"], 0.5)

    def test_matrix_validation_rejects_missing_variant(self):
        matrix = build_experiment_matrix()
        with self.assertRaises(ValueError):
            validate_experiment_matrix(matrix[:-1])


if __name__ == "__main__":
    unittest.main()
