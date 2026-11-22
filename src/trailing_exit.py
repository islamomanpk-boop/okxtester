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


def update_trailing_state(position, bar, timestamp=None):
    """
    Update trailing levels after this candle has completed.
    Record activation/update telemetry; new levels apply next candle.
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
    favorable_r = abs(best - entry) / risk
    position["max_favorable_excursion_r"] = max(
        float(position.get("max_favorable_excursion_r", 0.0)), favorable_r
    )
    position["max_favorable_price"] = best
    if timestamp is not None:
        position["max_favorable_time"] = int(timestamp)

    distance = float(position["trailing_distance_r"]) * risk

    if mode == "trailing_stop_loss":
        activation = float(position["trailing_activation_r"]) * risk
        activation_price = entry + side * activation

        activated = (
            best >= activation_price if side == 1
            else best <= activation_price
        )

        if activated:
            if not position.get("trailing_sl_active", False):
                position["trailing_sl_activation_time"] = int(timestamp) if timestamp is not None else None
                position["trailing_sl_activation_price"] = best
                position["trailing_sl_activation_level"] = activation_price
                position["trailing_sl_activation_r"] = favorable_r
            position["trailing_sl_active"] = True
            proposed = best - side * distance
            previous_stop = float(position["stop_price"])
            updated_stop = max(previous_stop, proposed) if side == 1 else min(previous_stop, proposed)
            improved = updated_stop > previous_stop if side == 1 else updated_stop < previous_stop
            if improved:
                position["stop_price"] = updated_stop
                position["trailing_sl_update_count"] = int(position.get("trailing_sl_update_count", 0)) + 1
                if timestamp is not None:
                    position["trailing_sl_last_update_time"] = int(timestamp)

    elif mode == "trailing_take_profit":
        target = float(position["target_price"])
        activated = (
            best >= target if side == 1
            else best <= target
        )

        if activated:
            if not position.get("trailing_tp_active", False):
                position["trailing_tp_activation_time"] = int(timestamp) if timestamp is not None else None
                position["trailing_tp_activation_price"] = best
                position["trailing_tp_activation_level"] = target
                position["trailing_tp_activation_r"] = favorable_r
            position["trailing_tp_active"] = True
            proposed = best - side * distance
            previous = position.get("trailing_tp_price")
            if previous is None:
                updated = proposed
                moved = True
            elif side == 1:
                updated = max(float(previous), proposed)
                moved = updated > float(previous)
            else:
                updated = min(float(previous), proposed)
                moved = updated < float(previous)
            position["trailing_tp_price"] = updated
            if moved:
                position["trailing_tp_update_count"] = int(position.get("trailing_tp_update_count", 0)) + 1
                if timestamp is not None:
                    position["trailing_tp_last_update_time"] = int(timestamp)
