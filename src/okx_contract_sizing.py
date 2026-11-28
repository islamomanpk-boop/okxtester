"""Fail-closed current-metadata sizing for linear OKX USDT swaps.

Pure sizing adapter only: no API calls, orders, or integration into the existing
backtest engines. The caller must supply metadata effective for the modeled date.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR
from typing import Mapping


def _decimal(value, field):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a valid decimal") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def _positive(value, field):
    result = _decimal(value, field)
    if result <= 0:
        raise ValueError(f"{field} must be positive")
    return result


def _fmt(value):
    return format(value.normalize(), "f") if value else "0"


def _floor_to_step(value, step):
    return (value / step).to_integral_value(rounding=ROUND_FLOOR) * step


def _ceil_to_step(value, step):
    return (value / step).to_integral_value(rounding=ROUND_CEILING) * step


@dataclass(frozen=True)
class OKXLinearSwapSpec:
    inst_id: str
    contract_value: Decimal
    contract_value_currency: str
    contract_multiplier: Decimal
    tick_size: Decimal
    lot_size_contracts: Decimal
    minimum_order_size_contracts: Decimal
    max_market_size_contracts: Decimal
    max_stop_size_contracts: Decimal
    max_trigger_size_contracts: Decimal

    @property
    def base_units_per_contract(self):
        return self.contract_value * self.contract_multiplier

    @classmethod
    def from_okx_record(cls, asset, record):
        asset = str(asset).upper()
        if not isinstance(record, Mapping):
            raise ValueError("Instrument metadata record must be a mapping")
        expected = {
            "instId": f"{asset}-USDT-SWAP",
            "instType": "SWAP",
            "ctType": "linear",
            "ctValCcy": asset,
            "settleCcy": "USDT",
            "state": "live",
        }
        for field, wanted in expected.items():
            if str(record.get(field, "")) != wanted:
                raise ValueError(f"{field} must equal {wanted}")

        values = {
            "contract_value": _positive(record.get("ctVal"), "ctVal"),
            "contract_multiplier": _positive(record.get("ctMult"), "ctMult"),
            "tick_size": _positive(record.get("tickSz"), "tickSz"),
            "lot_size_contracts": _positive(record.get("lotSz"), "lotSz"),
            "minimum_order_size_contracts": _positive(record.get("minSz"), "minSz"),
            "max_market_size_contracts": _positive(record.get("maxMktSz"), "maxMktSz"),
            "max_stop_size_contracts": _positive(record.get("maxStopSz"), "maxStopSz"),
            "max_trigger_size_contracts": _positive(record.get("maxTriggerSz"), "maxTriggerSz"),
        }
        if values["minimum_order_size_contracts"] % values["lot_size_contracts"] != 0:
            raise ValueError("minSz must be an integer multiple of lotSz")
        for field in (
            "max_market_size_contracts",
            "max_stop_size_contracts",
            "max_trigger_size_contracts",
        ):
            if values[field] < values["minimum_order_size_contracts"]:
                raise ValueError(f"{field} must be at least minSz")

        return cls(
            inst_id=expected["instId"],
            contract_value_currency=asset,
            **values,
        )


def round_stop_price_for_risk(stop_price, side, tick_size):
    """Round away from entry so planned stop risk is not understated.

    LONG stops round down; SHORT stops round up. This is risk-conservative
    rounding, not a claim about earliest trigger timing.
    """
    stop = _positive(stop_price, "stop_price")
    tick = _positive(tick_size, "tick_size")
    side = str(side).upper()
    if side == "LONG":
        return _floor_to_step(stop, tick)
    if side == "SHORT":
        return _ceil_to_step(stop, tick)
    raise ValueError("side must be LONG or SHORT")


def size_position_in_contracts(
    equity,
    entry_price,
    stop_price,
    side,
    risk_fraction,
    max_gross_leverage,
    taker_fee_rate,
    slippage_bps,
    instrument,
    order_kind="market",
):
    """Risk-size a linear swap in base units, then floor to exchange contracts.

    Fee and slippage inputs are mandatory. Risk is recalculated using the
    rounded stop and floored contract quantity. Below-minimum and over-limit
    orders are rejected rather than rounded up or silently split.
    """
    if not isinstance(instrument, OKXLinearSwapSpec):
        raise ValueError("instrument must be a validated OKXLinearSwapSpec")

    side = str(side).upper()
    if side not in ("LONG", "SHORT"):
        raise ValueError("side must be LONG or SHORT")
    order_kind = str(order_kind).lower()
    max_sizes = {
        "market": instrument.max_market_size_contracts,
        "stop": instrument.max_stop_size_contracts,
        "trigger": instrument.max_trigger_size_contracts,
    }
    if order_kind not in max_sizes:
        raise ValueError("order_kind must be market, stop, or trigger")

    equity = _positive(equity, "equity")
    entry = _positive(entry_price, "entry_price")
    raw_stop = _positive(stop_price, "stop_price")
    risk_fraction = _positive(risk_fraction, "risk_fraction")
    leverage = _positive(max_gross_leverage, "max_gross_leverage")
    fee_rate = _decimal(taker_fee_rate, "taker_fee_rate")
    slippage_fraction = _decimal(slippage_bps, "slippage_bps") / Decimal("10000")
    if not Decimal("0") < risk_fraction < Decimal("1"):
        raise ValueError("risk_fraction must be between 0 and 1")
    if fee_rate < 0 or slippage_fraction < 0 or slippage_fraction >= 1:
        raise ValueError(
            "fee and slippage must be nonnegative; slippage must be below 10000 bps"
        )

    rounded_stop = round_stop_price_for_risk(raw_stop, side, instrument.tick_size)
    if side == "LONG" and not rounded_stop < entry:
        raise ValueError("Rounded LONG stop must remain below entry")
    if side == "SHORT" and not rounded_stop > entry:
        raise ValueError("Rounded SHORT stop must remain above entry")

    direction = Decimal("1") if side == "LONG" else Decimal("-1")
    stop_exit_fill = rounded_stop * (
        Decimal("1") - direction * slippage_fraction
    )
    if stop_exit_fill <= 0:
        raise ValueError("Adverse stop-exit fill must be positive")
    risk_per_base_unit = (
        abs(entry - stop_exit_fill)
        + fee_rate * (entry + stop_exit_fill)
    )
    if risk_per_base_unit <= 0:
        raise ValueError("Cost-adjusted risk per base unit must be positive")

    risk_budget = equity * risk_fraction
    risk_limited_base = risk_budget / risk_per_base_unit
    exposure_limited_base = equity * leverage / entry
    requested_base = min(risk_limited_base, exposure_limited_base)

    base_per_contract = instrument.base_units_per_contract
    raw_contracts = requested_base / base_per_contract
    contracts = _floor_to_step(raw_contracts, instrument.lot_size_contracts)
    if contracts < instrument.minimum_order_size_contracts:
        raise ValueError(
            "Rounded contract quantity is below minSz; reject rather than round up"
        )

    max_size = max_sizes[order_kind]
    if contracts > max_size:
        raise ValueError(f"Rounded contract quantity exceeds {order_kind} max size")

    actual_base = contracts * base_per_contract
    actual_risk = actual_base * risk_per_base_unit
    if actual_risk > risk_budget:
        raise ArithmeticError("Post-rounding risk exceeds the configured risk budget")

    gross_exposure = actual_base * entry
    return {
        "inst_id": instrument.inst_id,
        "side": side,
        "order_kind": order_kind,
        "entry_price": _fmt(entry),
        "requested_stop_price": _fmt(raw_stop),
        "risk_conservative_stop_price": _fmt(rounded_stop),
        "stop_price_rounding_policy": "LONG=floor_to_tick; SHORT=ceil_to_tick; away_from_entry",
        "base_units_per_contract": _fmt(base_per_contract),
        "requested_contracts_before_lot_floor": _fmt(raw_contracts),
        "contract_quantity": _fmt(contracts),
        "base_quantity_after_lot_floor": _fmt(actual_base),
        "lot_size_contracts": _fmt(instrument.lot_size_contracts),
        "minimum_order_size_contracts": _fmt(instrument.minimum_order_size_contracts),
        "risk_budget_usdt": _fmt(risk_budget),
        "risk_per_base_unit_usdt": _fmt(risk_per_base_unit),
        "post_rounding_cost_adjusted_risk_usdt": _fmt(actual_risk),
        "gross_exposure_usdt": _fmt(gross_exposure),
        "effective_gross_leverage": _fmt(gross_exposure / equity),
        "max_order_size_contracts": _fmt(max_size),
    }
