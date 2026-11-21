"""Causal one-minute trade execution engine for Price Action V1."""

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class ExecutionConfig:
    risk_fraction: float = 0.005
    max_gross_leverage: float = 1.0
    taker_fee_rate: Optional[float] = None
    slippage_bps: Optional[float] = None

    def validate(self):
        if not 0 < self.risk_fraction < 1:
            raise ValueError("risk_fraction must be between 0 and 1")
        if self.max_gross_leverage <= 0:
            raise ValueError("max_gross_leverage must be positive")
        if self.taker_fee_rate is None or self.taker_fee_rate < 0:
            raise ValueError("A non-negative taker_fee_rate is required")
        if self.slippage_bps is None or self.slippage_bps < 0:
            raise ValueError("A non-negative slippage_bps value is required")


def size_position(equity, entry_price, stop_price, side, config):
    """Return quantity, risk budget and actual stop risk."""
    config.validate()

    if equity <= 0 or entry_price <= 0:
        raise ValueError("Equity and entry price must be positive")
    if side not in (-1, 1):
        raise ValueError("side must be 1 for long or -1 for short")

    distance = abs(entry_price - stop_price)
    if distance <= 0:
        raise ValueError("Stop price must differ from entry price")

    if side == 1 and stop_price >= entry_price:
        raise ValueError("Long stop must be below entry")
    if side == -1 and stop_price <= entry_price:
        raise ValueError("Short stop must be above entry")

    risk_budget = equity * config.risk_fraction
    risk_quantity = risk_budget / distance
    exposure_quantity = (
        equity * config.max_gross_leverage / entry_price
    )
    quantity = min(risk_quantity, exposure_quantity)

    return {
        "quantity": quantity,
        "risk_budget": risk_budget,
        "planned_stop_risk": quantity * distance,
        "gross_exposure": quantity * entry_price,
    }


def _validate_bars(bars):
    if not bars:
        raise ValueError("At least one execution candle is required")

    previous_ts = None
    for bar in bars:
        required = ("ts", "open", "high", "low", "close")
        if any(key not in bar for key in required):
            raise ValueError("Execution candle is missing required fields")

        ts = int(bar["ts"])
        o, h, l, c = (
            float(bar["open"]),
            float(bar["high"]),
            float(bar["low"]),
            float(bar["close"]),
        )

        if min(o, h, l, c) <= 0 or l > h:
            raise ValueError("Invalid OHLC prices")
        if h < max(o, c) or l > min(o, c):
            raise ValueError("OHLC values are inconsistent")
        if previous_ts is not None:
            if ts <= previous_ts:
                raise ValueError(
                    "Candle timestamps must be strictly increasing"
                )
            if ts - previous_ts != 60_000:
                raise ValueError(
                    "Execution candles must be exactly 1 minute apart"
                )

        previous_ts = ts


def simulate_trade(
    bars,
    entry_index,
    side,
    stop_price,
    target_price,
    equity,
    config,
    funding_events: Iterable = (),
):
    """
    Simulate one market-entry trade.

    bars use candle-open timestamps in milliseconds.
    Funding events are dictionaries with funding_time and funding_rate.
    Positive funding: longs pay, shorts receive.
    """
    config.validate()
    _validate_bars(bars)

    if not 0 <= entry_index < len(bars):
        raise ValueError("entry_index is outside the candle data")
    if side not in (-1, 1):
        raise ValueError("side must be 1 for long or -1 for short")

    entry_bar = bars[entry_index]
    raw_entry = float(entry_bar["open"])
    slip = config.slippage_bps / 10000.0

    # Slippage is adverse to the trader.
    entry_price = raw_entry * (1 + side * slip)
    stop_price = float(stop_price)
    target_price = float(target_price)

    if side == 1:
        if not stop_price < entry_price < target_price:
            raise ValueError("Long requires stop < entry < target")
    else:
        if not target_price < entry_price < stop_price:
            raise ValueError("Short requires target < entry < stop")

    sizing = size_position(
        equity, entry_price, stop_price, side, config
    )
    quantity = sizing["quantity"]

    exit_price = None
    exit_time = None
    exit_reason = None

    for bar in bars[entry_index:]:
        ts = int(bar["ts"])
        o = float(bar["open"])
        h = float(bar["high"])
        l = float(bar["low"])

        if side == 1:
            # A gap through the stop receives the worse opening price.
            if o <= stop_price:
                exit_price = o * (1 - slip)
                exit_reason = "stop_gap"
            # A favorable target gap is conservatively filled at target.
            elif o >= target_price:
                exit_price = target_price * (1 - slip)
                exit_reason = "target_gap"
            else:
                hit_stop = l <= stop_price
                hit_target = h >= target_price
                if hit_stop:
                    exit_price = stop_price * (1 - slip)
                    exit_reason = "stop"
                elif hit_target:
                    exit_price = target_price * (1 - slip)
                    exit_reason = "target"
        else:
            if o >= stop_price:
                exit_price = o * (1 + slip)
                exit_reason = "stop_gap"
            elif o <= target_price:
                exit_price = target_price * (1 + slip)
                exit_reason = "target_gap"
            else:
                hit_stop = h >= stop_price
                hit_target = l <= target_price
                if hit_stop:
                    exit_price = stop_price * (1 + slip)
                    exit_reason = "stop"
                elif hit_target:
                    exit_price = target_price * (1 + slip)
                    exit_reason = "target"

        if exit_price is not None:
            exit_time = ts
            break

    if exit_price is None:
        last_bar = bars[-1]
        exit_price = float(last_bar["close"]) * (1 - side * slip)
        exit_time = int(last_bar["ts"])
        exit_reason = "end_of_data"

    entry_notional = quantity * entry_price
    exit_notional = quantity * exit_price
    entry_fee = entry_notional * config.taker_fee_rate
    exit_fee = exit_notional * config.taker_fee_rate

    gross_pnl = side * quantity * (exit_price - entry_price)

    funding_pnl = 0.0
    bars_by_timestamp = {int(bar["ts"]): bar for bar in bars}

    for event in funding_events:
        funding_time = int(event["funding_time"])
        rate = float(event["funding_rate"])

        # Position must be open at the funding settlement instant.
        if int(entry_bar["ts"]) < funding_time <= exit_time:
            if not -1 <= rate <= 1:
                raise ValueError("Funding rate outside allowed range")

            # Prefer an explicitly supplied settlement mark price.
            # Otherwise use the settlement-minute candle close as a proxy.
            if event.get("mark_price") is not None:
                settlement_price = float(event["mark_price"])
            else:
                settlement_bar = bars_by_timestamp.get(funding_time)
                if settlement_bar is None:
                    raise ValueError(
                        "Missing 1m candle at funding timestamp; "
                        "provide mark_price or complete execution data"
                    )
                settlement_price = float(settlement_bar["close"])

            if settlement_price <= 0:
                raise ValueError("Invalid funding settlement price")

            notional_at_settlement = quantity * settlement_price
            funding_pnl += -side * notional_at_settlement * rate

    total_fees = entry_fee + exit_fee
    net_pnl = gross_pnl + funding_pnl - total_fees

    return {
        "side": "LONG" if side == 1 else "SHORT",
        "entry_time": int(entry_bar["ts"]),
        "exit_time": exit_time,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "quantity": quantity,
        "risk_budget": sizing["risk_budget"],
        "planned_stop_risk": sizing["planned_stop_risk"],
        "gross_exposure": sizing["gross_exposure"],
        "gross_pnl": gross_pnl,
        "funding_pnl": funding_pnl,
        "entry_fee": entry_fee,
        "exit_fee": exit_fee,
        "total_fees": total_fees,
        "net_pnl": net_pnl,
        "equity_before": equity,
        "equity_after": equity + net_pnl,
        "exit_reason": exit_reason,
    }


def find_next_entry_index(bars, signal_available_at):
    """Find first 1m candle opening at or after signal availability."""
    available = int(signal_available_at)

    for index, bar in enumerate(bars):
        if int(bar["ts"]) >= available:
            return index

    return None
