"""Causal one-minute trailing exit state updates."""

import math


def validate_trailing_settings(candidate):
    mode = candidate.get("trailing_mode", "none")
    if mode not in ("none", "trailing_stop_loss", "trailing_take_profit"):
        raise ValueError("Unknown trailing mode")

    if mode == "none":
        return

    activation = candidate.get("trailing_activation_r")
    distance = candidate.get("trailing_distance_r")

    if mode == "trailing_stop_loss":
        if activation is None or distance is None:
            raise ValueError("Trailing stop-loss requires activation and distance")
        if not math.isfinite(float(activation)) or float(activation) <= 0:
            raise ValueError("Trailing activation must be positive and finite")
        if not math.isfinite(float(distance)) or float(distance) <= 0:
            raise ValueError("Trailing distance must be positive and finite")

    if mode == "trailing_take_profit":
        if not candidate.get("trailing_activation_at_target", False):
            raise ValueError("Trailing take-profit must activate at original target")
        if distance is None:
            raise ValueError("Trailing take-profit requires a trailing distance")
        if not math.isfinite(float(distance)) or float(distance) <= 0:
            raise ValueError("Trailing distance must be positive and finite")


def update_trailing_state(position, bar):
    """
    Update trailing levels after this candle has completed.
    The updated levels are therefore first eligible on the next candle.
    """
    mode = position.get("trailing_mode", "none")
    if mode == "none":
        return

    side = int(position["side"])
    entry = float(position["entry_price"])
    risk = float(position["risk_distance"])
    high = float(bar["high"])
    low = float(bar["low"])

    if side == 1:
        best = max(float(position["best_favorable_price"]), high)
    else:
        best = min(float(position["best_favorable_price"]), low)

    position["best_favorable_price"] = best

    distance = float(position["trailing_distance_r"]) * risk

    if mode == "trailing_stop_loss":
        activation = float(position["trailing_activation_r"]) * risk
        activation_price = entry + side * activation

        activated = (
            best >= activation_price if side == 1
            else best <= activation_price
        )

        if activated:
            position["trailing_sl_active"] = True
            proposed = best - side * distance

            if side == 1:
                position["stop_price"] = max(
                    float(position["stop_price"]), proposed
                )
            else:
                position["stop_price"] = min(
                    float(position["stop_price"]), proposed
                )

    elif mode == "trailing_take_profit":
        target = float(position["target_price"])
        activated = (
            best >= target if side == 1
            else best <= target
        )

        if activated:
            position["trailing_tp_active"] = True
            proposed = best - side * distance
            previous = position.get("trailing_tp_price")

            if previous is None:
                position["trailing_tp_price"] = proposed
            elif side == 1:
                position["trailing_tp_price"] = max(
                    float(previous), proposed
                )
            else:
                position["trailing_tp_price"] = min(
                    float(previous), proposed
                )
