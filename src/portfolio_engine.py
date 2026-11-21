"""Deterministic shared-capital allocator for Price Action V1."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PortfolioConfig:
    risk_fraction: float = 0.005
    max_gross_leverage: float = 1.0

    def validate(self):
        if not math.isfinite(self.risk_fraction) or not 0 < self.risk_fraction < 1:
            raise ValueError("risk_fraction must be between 0 and 1")
        if not math.isfinite(self.max_gross_leverage) or self.max_gross_leverage <= 0:
            raise ValueError("max_gross_leverage must be positive")


def _validate_candidate(candidate):
    required = (
        "asset", "side", "entry_price", "stop_price",
        "signal_available_at", "signal_priority",
        "stop_distance_atr",
    )
    if any(key not in candidate for key in required):
        raise ValueError("Candidate is missing required fields")

    if not str(candidate["asset"]).strip():
        raise ValueError("Asset cannot be empty")
    if candidate["side"] not in (-1, 1):
        raise ValueError("Side must be 1 for long or -1 for short")

    entry = float(candidate["entry_price"])
    stop = float(candidate["stop_price"])
    priority = int(candidate["signal_priority"])
    atr_distance = float(candidate["stop_distance_atr"])

    if not all(math.isfinite(v) for v in (entry, stop, atr_distance)):
        raise ValueError("Candidate prices and ATR distance must be finite")
    if entry <= 0 or stop <= 0 or entry == stop:
        raise ValueError("Entry and stop prices must be positive and different")
    if candidate["side"] == 1 and stop >= entry:
        raise ValueError("Long stop must be below entry")
    if candidate["side"] == -1 and stop <= entry:
        raise ValueError("Short stop must be above entry")
    if priority not in (1, 2, 3):
        raise ValueError("Signal priority must be 1, 2, or 3")
    if atr_distance <= 0:
        raise ValueError("ATR stop distance must be positive")

    if "risk_per_unit" in candidate:
        risk_per_unit = float(candidate["risk_per_unit"])
        if not math.isfinite(risk_per_unit) or risk_per_unit <= 0:
            raise ValueError("risk_per_unit must be finite and positive")


def _validate_open_positions(open_positions):
    seen_assets = set()
    for position in open_positions:
        if not all(k in position for k in ("asset", "quantity", "mark_price")):
            raise ValueError("Open position is missing required fields")
        asset = str(position["asset"])
        if asset in seen_assets:
            raise ValueError("Only one open position per asset is allowed")
        seen_assets.add(asset)
        quantity = float(position["quantity"])
        mark_price = float(position["mark_price"])
        if not math.isfinite(quantity) or not math.isfinite(mark_price):
            raise ValueError("Open position values must be finite")
        if quantity <= 0 or mark_price <= 0:
            raise ValueError("Open position quantity and mark price must be positive")


def allocate_candidates(candidates, equity, open_positions=(), config=None):
    """
    Allocate a simultaneous batch of candidates against shared equity.

    Candidate priority:
      3 = support/resistance rejection or first OB retest
      2 = engulfing/pinbar at a confirmed S/R level
      1 = standalone engulfing/pinbar

    Within a priority tier, smaller ATR-normalized stop distance wins.
    Asset symbol is the final deterministic tie-breaker.

    Existing positions consume gross exposure before new candidates.
    Only one position per asset is allowed.
    """
    if config is None:
        config = PortfolioConfig()

    config.validate()
    _validate_open_positions(open_positions)

    equity = float(equity)
    if not math.isfinite(equity) or equity <= 0:
        raise ValueError("Equity must be positive")

    candidates = list(candidates)
    if candidates:
        for candidate in candidates:
            _validate_candidate(candidate)

        timestamps = {int(c["signal_available_at"]) for c in candidates}
        if len(timestamps) != 1:
            raise ValueError("Candidates must belong to the same decision timestamp")

    max_exposure = equity * config.max_gross_leverage
    used_exposure = sum(
        float(p["quantity"]) * float(p["mark_price"])
        for p in open_positions
    )
    if used_exposure > max_exposure + 1e-9:
        raise ValueError("Existing positions already exceed portfolio exposure limit")
    remaining_exposure = max(0.0, max_exposure - used_exposure)

    occupied_assets = {str(p["asset"]) for p in open_positions}

    ranked = sorted(
        candidates,
        key=lambda c: (
            -int(c["signal_priority"]),
            float(c["stop_distance_atr"]),
            str(c["asset"]),
        ),
    )

    accepted = []
    rejected = []

    for candidate in ranked:
        asset = str(candidate["asset"])

        if asset in occupied_assets:
            rejected.append({
                "asset": asset,
                "reason": "asset_already_has_open_position",
            })
            continue

        if remaining_exposure <= 0:
            rejected.append({
                "asset": asset,
                "reason": "portfolio_exposure_limit_reached",
            })
            continue

        entry = float(candidate["entry_price"])
        stop = float(candidate["stop_price"])
        distance = abs(entry - stop)

        risk_budget = equity * config.risk_fraction
        risk_per_unit = float(candidate.get("risk_per_unit", distance))
        risk_quantity = risk_budget / risk_per_unit
        exposure_quantity = remaining_exposure / entry
        quantity = min(risk_quantity, exposure_quantity)

        if quantity <= 0:
            rejected.append({
                "asset": asset,
                "reason": "no_available_exposure",
            })
            continue

        notional = quantity * entry
        planned_risk = quantity * distance

        accepted.append({
            "asset": asset,
            "side": "LONG" if candidate["side"] == 1 else "SHORT",
            "quantity": quantity,
            "entry_price": entry,
            "stop_price": stop,
            "risk_budget": risk_budget,
            "planned_stop_risk": planned_risk,
            "planned_cost_adjusted_risk": quantity * risk_per_unit,
            "risk_per_unit": risk_per_unit,
            "gross_exposure": notional,
            "signal_priority": int(candidate["signal_priority"]),
            "signal_available_at": int(candidate["signal_available_at"]),
        })

        occupied_assets.add(asset)
        remaining_exposure -= notional

    final_exposure = used_exposure + sum(p["gross_exposure"] for p in accepted)

    return {
        "equity": equity,
        "max_gross_exposure": max_exposure,
        "existing_gross_exposure": used_exposure,
        "new_gross_exposure": sum(p["gross_exposure"] for p in accepted),
        "total_gross_exposure": final_exposure,
        "remaining_exposure": remaining_exposure,
        "accepted": accepted,
        "rejected": rejected,
    }
