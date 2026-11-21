import unittest

from trailing_exit import (
    validate_trailing_settings,
    update_trailing_state,
)


class TrailingExitTests(unittest.TestCase):

    def make_position(self, side, mode):
        return {
            "side": side,
            "entry_price": 100.0,
            "risk_distance": 1.0,
            "stop_price": 99.0 if side == 1 else 101.0,
            "target_price": 102.0 if side == 1 else 98.0,
            "trailing_mode": mode,
            "trailing_activation_r": 1.0,
            "trailing_distance_r": 1.0,
            "trailing_activation_at_target": True,
            "trailing_sl_active": False,
            "trailing_tp_active": False,
            "trailing_tp_price": None,
            "best_favorable_price": 100.0,
        }

    def test_long_trailing_stop_moves_up(self):
        p = self.make_position(1, "trailing_stop_loss")
        update_trailing_state(p, {"high": 102.0, "low": 100.5})
        self.assertTrue(p["trailing_sl_active"])
        self.assertEqual(p["stop_price"], 101.0)

    def test_short_trailing_stop_moves_down(self):
        p = self.make_position(-1, "trailing_stop_loss")
        update_trailing_state(p, {"high": 99.5, "low": 98.0})
        self.assertTrue(p["trailing_sl_active"])
        self.assertEqual(p["stop_price"], 99.0)

    def test_long_trailing_tp_activates_at_target(self):
        p = self.make_position(1, "trailing_take_profit")
        p["trailing_distance_r"] = 0.5
        update_trailing_state(p, {"high": 103.0, "low": 102.1})
        self.assertTrue(p["trailing_tp_active"])
        self.assertEqual(p["trailing_tp_price"], 102.5)

    def test_short_trailing_tp_activates_at_target(self):
        p = self.make_position(-1, "trailing_take_profit")
        p["trailing_distance_r"] = 0.5
        update_trailing_state(p, {"high": 97.9, "low": 97.0})
        self.assertTrue(p["trailing_tp_active"])
        self.assertEqual(p["trailing_tp_price"], 97.5)

    def test_invalid_trailing_mode_rejected(self):
        with self.assertRaises(ValueError):
            validate_trailing_settings({"trailing_mode": "unknown"})

    def test_trailing_stop_requires_settings(self):
        with self.assertRaises(ValueError):
            validate_trailing_settings({
                "trailing_mode": "trailing_stop_loss"
            })


if __name__ == "__main__":
    unittest.main()
