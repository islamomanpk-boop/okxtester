"""Deterministic exit experiment matrix for Price Action V1."""

from dataclasses import dataclass
import math


FIXED_STOPS = {
    "fixed_stop_0_50pct": 0.005,
    "fixed_stop_0_75pct": 0.0075,
    "fixed_stop_1_00pct": 0.01,
}

FIXED_TARGETS = {
    "fixed_target_0_75pct": 0.0075,
    "fixed_target_1_00pct": 0.01,
    "fixed_target_1_50pct": 0.015,
    "fixed_target_2_00pct": 0.02,
}

R_TARGETS = {
    "target_1R": 1.0,
    "target_1_5R": 1.5,
    "target_2R": 2.0,
}

CANDLE_STOPS = (
    "signal_extreme_exact",
    "signal_extreme_atr_buffer_0_10",
)

TRAILING_MODES = (
    "none",
    "trailing_stop_loss",
    "trailing_take_profit",
)


@dataclass(frozen=True)
class ExitExperiment:
    experiment_id: str
    stop_model: str
    target_model: str
    target_value: float
    trailing_mode: str = "none"
    trailing_activation_r: float | None = None
    trailing_distance_r: float | None = None
    trailing_activation_at_target: bool = False


def _make_id(stop_model, target_model):
    return f"{stop_model}__{target_model}"


def build_baseline_experiments():
    """Build 16 original fixed-target tests plus 6 candle-stop R tests."""
    experiments = []

    # Preserve the original 16 combinations.
    stop_models = {
        **FIXED_STOPS,
        "signal_extreme_atr_buffer_0_10": None,
    }

    for stop_model in stop_models:
        for target_model, target_value in FIXED_TARGETS.items():
            experiments.append(ExitExperiment(
                experiment_id=_make_id(stop_model, target_model),
                stop_model=stop_model,
                target_model=target_model,
                target_value=target_value,
            ))

    # Add exact and buffered candle stops with 1R, 1.5R and 2R.
    for stop_model in CANDLE_STOPS:
        for target_model, target_value in R_TARGETS.items():
            experiments.append(ExitExperiment(
                experiment_id=_make_id(stop_model, target_model),
                stop_model=stop_model,
                target_model=target_model,
                target_value=target_value,
            ))

    return tuple(experiments)


def build_experiment_matrix():
    """Return 22 baseline, 22 trailing-stop and 22 trailing-TP variants."""
    baseline = build_baseline_experiments()
    experiments = list(baseline)

    for base in baseline:
        experiments.append(ExitExperiment(
            experiment_id=base.experiment_id + "__trailing_sl",
            stop_model=base.stop_model,
            target_model=base.target_model,
            target_value=base.target_value,
            trailing_mode="trailing_stop_loss",
            trailing_activation_r=1.0,
            trailing_distance_r=1.0,
        ))

    for base in baseline:
        experiments.append(ExitExperiment(
            experiment_id=base.experiment_id + "__trailing_tp",
            stop_model=base.stop_model,
            target_model=base.target_model,
            target_value=base.target_value,
            trailing_mode="trailing_take_profit",
            trailing_distance_r=0.5,
            trailing_activation_at_target=True,
        ))

    validate_experiment_matrix(experiments)
    return tuple(experiments)


def validate_experiment_matrix(experiments):
    if len(experiments) != 66:
        raise ValueError("Experiment matrix must contain exactly 66 variants")

    ids = [item.experiment_id for item in experiments]
    if len(ids) != len(set(ids)):
        raise ValueError("Experiment IDs must be unique")

    baseline = [x for x in experiments if x.trailing_mode == "none"]
    trailing_sl = [
        x for x in experiments
        if x.trailing_mode == "trailing_stop_loss"
    ]
    trailing_tp = [
        x for x in experiments
        if x.trailing_mode == "trailing_take_profit"
    ]

    if not (len(baseline) == len(trailing_sl) == len(trailing_tp) == 22):
        raise ValueError("Each experiment group must contain 22 variants")

    if any(
        x.trailing_activation_r != 1.0 or x.trailing_distance_r != 1.0
        for x in trailing_sl
    ):
        raise ValueError("Trailing stop-loss rule is inconsistent")

    if any(
        x.trailing_distance_r != 0.5
        or not x.trailing_activation_at_target
        for x in trailing_tp
    ):
        raise ValueError("Trailing take-profit rule is inconsistent")

    return True


def resolve_exit_prices(experiment, candidate, entry_price):
    """
    Resolve initial stop and target from an actual execution entry.

    Candidate requires:
      side, signal_high, signal_low, signal_atr14
    """
    side = candidate.get("side")
    if side not in (-1, 1):
        raise ValueError("Side must be 1 or -1")

    entry = float(entry_price)
    if not math.isfinite(entry) or entry <= 0:
        raise ValueError("Entry price must be finite and positive")

    stop_model = experiment.stop_model

    if stop_model in FIXED_STOPS:
        distance_pct = FIXED_STOPS[stop_model]
        stop = entry * (1 - side * distance_pct)

    elif stop_model in CANDLE_STOPS:
        high = float(candidate["signal_high"])
        low = float(candidate["signal_low"])

        if not all(math.isfinite(x) and x > 0 for x in (high, low)):
            raise ValueError("Signal candle high/low must be positive and finite")
        if low > high:
            raise ValueError("Signal candle low cannot exceed high")

        if stop_model == "signal_extreme_exact":
            buffer = 0.0
        else:
            atr = float(candidate["signal_atr14"])
            if not math.isfinite(atr) or atr <= 0:
                raise ValueError("Signal ATR14 must be finite and positive")
            buffer = 0.10 * atr

        stop = low - buffer if side == 1 else high + buffer

    else:
        raise ValueError(f"Unknown stop model: {stop_model}")

    if not math.isfinite(stop) or stop <= 0:
        raise ValueError("Resolved stop must be finite and positive")

    if side == 1 and stop >= entry:
        raise ValueError("Long stop must be below actual entry")
    if side == -1 and stop <= entry:
        raise ValueError("Short stop must be above actual entry")

    risk_distance = abs(entry - stop)

    if experiment.target_model in FIXED_TARGETS:
        target_pct = FIXED_TARGETS[experiment.target_model]
        target = entry * (1 + side * target_pct)

    elif experiment.target_model in R_TARGETS:
        target_r = R_TARGETS[experiment.target_model]
        target = entry + side * target_r * risk_distance

    else:
        raise ValueError(f"Unknown target model: {experiment.target_model}")

    if not math.isfinite(target) or target <= 0:
        raise ValueError("Resolved target must be finite and positive")

    if side == 1 and target <= entry:
        raise ValueError("Long target must be above entry")
    if side == -1 and target >= entry:
        raise ValueError("Short target must be below entry")

    return {
        "stop_price": stop,
        "target_price": target,
        "risk_distance": risk_distance,
        "risk_per_unit": risk_distance,
        "trailing_mode": experiment.trailing_mode,
        "trailing_activation_r": experiment.trailing_activation_r,
        "trailing_distance_r": experiment.trailing_distance_r,
        "trailing_activation_at_target": (
            experiment.trailing_activation_at_target
        ),
    }


if __name__ == "__main__":
    matrix = build_experiment_matrix()
    print("Total experiments:", len(matrix))
    for mode in TRAILING_MODES:
        print(
            mode + ":",
            sum(x.trailing_mode == mode for x in matrix)
        )
