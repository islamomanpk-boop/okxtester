"""Event-driven, shared-capital one-minute portfolio backtester."""

from bisect import bisect_left
from datetime import datetime, timezone
import math

from portfolio_engine import PortfolioConfig, allocate_candidates
from trailing_exit import validate_trailing_settings, update_trailing_state
from exit_experiment_config import resolve_exit_prices
from compact_bar_series import TimestampBarLookup
from funding_coverage import validate_funding_contract, validate_trade_funding_window


class PortfolioBacktestConfig:
    def __init__(
        self,
        initial_equity=1000.0,
        risk_fraction=0.005,
        max_gross_leverage=1.0,
        taker_fee_rate=None,
        slippage_bps=None,
        record_equity_curve=True,
    ):
        self.initial_equity = float(initial_equity)
        self.risk_fraction = float(risk_fraction)
        self.max_gross_leverage = float(max_gross_leverage)
        self.taker_fee_rate = taker_fee_rate
        self.slippage_bps = slippage_bps
        self.record_equity_curve = record_equity_curve
        self.validate()

    def validate(self):
        values = (
            self.initial_equity,
            self.risk_fraction,
            self.max_gross_leverage,
        )
        if not all(math.isfinite(v) for v in values):
            raise ValueError("Portfolio configuration must be finite")
        if self.initial_equity <= 0:
            raise ValueError("Initial equity must be positive")
        if not 0 < self.risk_fraction < 1:
            raise ValueError("Risk fraction must be between 0 and 1")
        if self.max_gross_leverage <= 0:
            raise ValueError("Maximum leverage must be positive")
        if self.taker_fee_rate is None or self.slippage_bps is None:
            raise ValueError("Taker fee and slippage assumptions are required")
        if not math.isfinite(float(self.taker_fee_rate)):
            raise ValueError("Taker fee must be finite")
        if not math.isfinite(float(self.slippage_bps)):
            raise ValueError("Slippage must be finite")
        if self.taker_fee_rate < 0 or self.slippage_bps < 0:
            raise ValueError("Taker fee and slippage cannot be negative")
        if not isinstance(self.record_equity_curve, bool):
            raise ValueError("record_equity_curve must be boolean")


def _validate_bars_by_asset(bars_by_asset):
    if not isinstance(bars_by_asset, dict) or not bars_by_asset:
        raise ValueError("bars_by_asset must be a non-empty dictionary")

    from array import array

    reference = None

    for asset_index, (asset, bars) in enumerate(bars_by_asset.items()):
        if not str(asset).strip() or not bars:
            raise ValueError("Every asset needs a name and execution candles")

        if asset_index == 0:
            reference = (
                bars.timestamps
                if hasattr(bars, "timestamps")
                else array("q")
            )

        previous = None

        # Validate this asset's own candle sequence first.
        for index, bar in enumerate(bars):
            required = ("ts", "open", "high", "low", "close")
            if any(key not in bar for key in required):
                raise ValueError(f"{asset} candle is missing required fields")

            ts = int(bar["ts"])
            o, h, low, close = (
                float(bar["open"]),
                float(bar["high"]),
                float(bar["low"]),
                float(bar["close"]),
            )

            if not all(math.isfinite(v) for v in (o, h, low, close)):
                raise ValueError(f"{asset} has non-finite OHLC values")
            if min(o, h, low, close) <= 0:
                raise ValueError(f"{asset} has non-positive OHLC values")
            if low > h or h < max(o, close) or low > min(o, close):
                raise ValueError(f"{asset} has inconsistent OHLC values")

            if previous is not None and ts - previous != 60_000:
                raise ValueError(
                    f"{asset} candles must be strictly chronological "
                    "and exactly one minute apart"
                )

            if asset_index == 0 and not hasattr(bars, "timestamps"):
                reference.append(ts)

            previous = ts

        # Only compare assets after their individual timelines are valid.
        if asset_index > 0:
            if len(bars) != len(reference):
                raise ValueError(
                    f"{asset} timestamps do not match the common portfolio timeline"
                )

            for index, bar in enumerate(bars):
                if int(bar["ts"]) != reference[index]:
                    raise ValueError(
                        f"{asset} timestamps do not match the common portfolio timeline"
                    )

    return reference


def _validate_funding(bars_by_asset, funding_by_asset, timestamps):
    """Validate explicit coverage contracts and the 1m settlement timeline."""
    normalized = validate_funding_contract(bars_by_asset, funding_by_asset)
    timeline = set(timestamps)
    for asset, contract in normalized.items():
        for event in contract["events"]:
            if int(event["funding_time"]) not in timeline:
                raise ValueError(
                    f"{asset} funding settlement does not align with the 1m execution timeline"
                )
    return normalized


def _validate_candidates(candidates, bars_by_asset, timestamps):
    scheduled = {}

    common_required = (
        "asset", "side", "signal_available_at",
        "signal_priority", "stop_distance_atr",
    )

    for candidate in candidates:
        if any(key not in candidate for key in common_required):
            raise ValueError("Signal candidate is missing required fields")

        asset = str(candidate["asset"])
        if asset not in bars_by_asset:
            raise ValueError(f"Candidate asset has no execution data: {asset}")

        if candidate["side"] not in (-1, 1):
            raise ValueError("Candidate side must be 1 or -1")

        atr_distance = float(candidate["stop_distance_atr"])
        if not math.isfinite(atr_distance) or atr_distance <= 0:
            raise ValueError("Candidate ATR distance must be finite and positive")

        experiment = candidate.get("exit_experiment")

        if experiment is not None:
            experiment_required = (
                "signal_high", "signal_low", "signal_atr14",
            )
            if any(key not in candidate for key in experiment_required):
                raise ValueError(
                    "Experiment candidate is missing signal candle data"
                )
        else:
            legacy_required = ("stop_price", "target_pct")
            if any(key not in candidate for key in legacy_required):
                raise ValueError(
                    "Legacy candidate requires stop_price and target_pct"
                )

            stop = float(candidate["stop_price"])
            target_pct = float(candidate["target_pct"])

            if not all(math.isfinite(v) for v in (stop, target_pct)):
                raise ValueError(
                    "Candidate stop and target must be finite"
                )
            if stop <= 0 or target_pct <= 0:
                raise ValueError(
                    "Candidate stop and target must be positive"
                )

        validate_trailing_settings(candidate)

        available_at = int(candidate["signal_available_at"])
        index = bisect_left(timestamps, available_at)

        if index >= len(timestamps):
            continue

        entry_ts = timestamps[index]
        scheduled.setdefault(entry_ts, []).append(dict(candidate))

    return scheduled

def _exit_fill(position, bar, slippage):
    """Check exits using levels active before this candle."""
    side = position["side"]
    stop = float(position["stop_price"])
    mode = position.get("trailing_mode", "none")

    o = float(bar["open"])
    h = float(bar["high"])
    low = float(bar["low"])
    raw_exit = None
    reason = None

    if side == 1:
        if o <= stop:
            raw_exit, reason = o, "stop_gap"
        elif low <= stop:
            raw_exit, reason = stop, "stop"
        elif mode == "trailing_take_profit":
            if position.get("trailing_tp_active", False):
                trail = float(position["trailing_tp_price"])
                if o <= trail:
                    raw_exit, reason = o, "trailing_take_profit_gap"
                elif low <= trail:
                    raw_exit, reason = trail, "trailing_take_profit"
        else:
            target = float(position["target_price"])
            if o >= target:
                raw_exit, reason = target, "target_gap"
            elif h >= target:
                raw_exit, reason = target, "target"
    else:
        if o >= stop:
            raw_exit, reason = o, "stop_gap"
        elif h >= stop:
            raw_exit, reason = stop, "stop"
        elif mode == "trailing_take_profit":
            if position.get("trailing_tp_active", False):
                trail = float(position["trailing_tp_price"])
                if o >= trail:
                    raw_exit, reason = o, "trailing_take_profit_gap"
                elif h >= trail:
                    raw_exit, reason = trail, "trailing_take_profit"
        else:
            target = float(position["target_price"])
            if o <= target:
                raw_exit, reason = target, "target_gap"
            elif low <= target:
                raw_exit, reason = target, "target"

    if raw_exit is None:
        return None

    exit_price = raw_exit * (1 - side * slippage)
    return exit_price, reason


def _unrealized_pnl(position, mark_price):
    return (
        position["side"]
        * position["quantity"]
        * (mark_price - position["entry_price"])
    )


def run_portfolio_backtest(
    bars_by_asset,
    candidates,
    funding_by_asset,
    config,
):
    """
    Run all assets on one synchronized one-minute timeline.

    Candidates require:
      asset, side, signal_available_at, signal_priority,
      stop_price, stop_distance_atr, target_pct.

    target_pct is decimal form: 0.01 means 1%.
    Funding must be explicitly supplied for every asset.
    """
    config.validate()
    timestamps = _validate_bars_by_asset(bars_by_asset)
    validated_funding = _validate_funding(
        bars_by_asset, funding_by_asset, timestamps
    )

    scheduled = _validate_candidates(
        candidates, bars_by_asset, timestamps
    )

    assets = list(bars_by_asset)
    bars_at = {
        asset: TimestampBarLookup(bars_by_asset[asset])
        for asset in assets
    }

    funding_at = {asset: {} for asset in assets}
    for asset in assets:
        for event in validated_funding[asset]["events"]:
            funding_at[asset].setdefault(
                int(event["funding_time"]), []
            ).append(event)

    slippage = float(config.slippage_bps) / 10_000.0
    fee_rate = float(config.taker_fee_rate)

    allocator_config = PortfolioConfig(
        risk_fraction=config.risk_fraction,
        max_gross_leverage=config.max_gross_leverage,
    )

    positions = {}
    trades = []
    decisions = []
    equity_curve = []
    realized_pnl = 0.0
    peak_equity = config.initial_equity
    max_drawdown = 0.0
    max_drawdown_amount = 0.0
    max_concurrent_positions = 0
    max_gross_exposure = 0.0
    max_capital_utilization = 0.0
    max_gross_exposure_equity_multiple = 0.0
    utilization_sum = 0.0
    utilization_samples = 0
    daily_marks_by_date = {}

    def close_position(asset, position, exit_price, exit_time, reason):
        nonlocal realized_pnl

        quantity = position["quantity"]
        side = position["side"]

        gross_pnl = side * quantity * (
            exit_price - position["entry_price"]
        )
        exit_fee = quantity * exit_price * fee_rate

        realized_pnl += gross_pnl - exit_fee

        net_pnl = (
            gross_pnl
            - position["entry_fee"]
            - exit_fee
            + position["funding_pnl"]
        )

        trades.append({
            "asset": asset,
            "side": "LONG" if side == 1 else "SHORT",
            "entry_time": position["entry_time"],
            "exit_time": int(exit_time),
            "entry_price": position["entry_price"],
            "exit_price": exit_price,
            "quantity": quantity,
            "initial_stop_price": position["initial_stop_price"],
            "stop_price": position["stop_price"],
            "target_price": position["target_price"],
            "trailing_mode": position.get("trailing_mode", "none"),
            "trailing_sl_active": position.get("trailing_sl_active", False),
            "trailing_sl_activation_time": position.get("trailing_sl_activation_time"),
            "trailing_sl_activation_price": position.get("trailing_sl_activation_price"),
            "trailing_sl_activation_level": position.get("trailing_sl_activation_level"),
            "trailing_sl_activation_r": position.get("trailing_sl_activation_r"),
            "trailing_sl_update_count": position.get("trailing_sl_update_count", 0),
            "trailing_sl_last_update_time": position.get("trailing_sl_last_update_time"),
            "trailing_tp_active": position.get("trailing_tp_active", False),
            "trailing_tp_activation_time": position.get("trailing_tp_activation_time"),
            "trailing_tp_activation_price": position.get("trailing_tp_activation_price"),
            "trailing_tp_activation_level": position.get("trailing_tp_activation_level"),
            "trailing_tp_activation_r": position.get("trailing_tp_activation_r"),
            "trailing_tp_price": position.get("trailing_tp_price"),
            "trailing_tp_update_count": position.get("trailing_tp_update_count", 0),
            "trailing_tp_last_update_time": position.get("trailing_tp_last_update_time"),
            "max_favorable_price": position.get("max_favorable_price", position["entry_price"]),
            "max_favorable_time": position.get("max_favorable_time"),
            "max_favorable_excursion_r": position.get("max_favorable_excursion_r", 0.0),
            "signal_priority": position["signal_priority"],
            "gross_pnl": gross_pnl,
            "funding_pnl": position["funding_pnl"],
            "entry_fee": position["entry_fee"],
            "exit_fee": exit_fee,
            "total_fees": position["entry_fee"] + exit_fee,
            "net_pnl": net_pnl,
            "funding_mark_price_mode": validated_funding[asset]["coverage"]["mark_price_mode"],
            "funding_source_sha256": validated_funding[asset]["coverage"]["source_sha256"],
            "funding_instrument_name": validated_funding[asset]["coverage"]["instrument_name"],
            "funding_schedule_id": validated_funding[asset]["coverage"]["schedule_id"],
            "funding_settlements_applied": len(validate_trade_funding_window(
                asset, position["entry_time"], int(exit_time), validated_funding[asset]
            )),
            "exit_reason": reason,
        })

    for ts in timestamps:
        # 1. Apply funding to positions open before this settlement time.
        # Proxy marks are used only when explicitly selected in coverage metadata.
        for asset in assets:
            position = positions.get(asset)
            if position is None or position["entry_time"] >= ts:
                continue

            bar = bars_at[asset][ts]
            for event in funding_at[asset].get(ts, []):
                mark = event.get("mark_price")
                if mark is None:
                    if validated_funding[asset]["coverage"]["mark_price_mode"] != "candle_close_proxy":
                        raise ValueError(f"{asset} exact funding mark price is missing")
                    mark = float(bar["close"])

                funding_pnl = (
                    -position["side"]
                    * position["quantity"]
                    * float(mark)
                    * float(event["funding_rate"])
                )
                position["funding_pnl"] += funding_pnl
                realized_pnl += funding_pnl

        # 2. Process exits before considering new entries.
        for asset in assets:
            position = positions.get(asset)
            if position is None:
                continue

            bar = bars_at[asset][ts]
            position["mark_price"] = float(bar["open"])

            result = _exit_fill(position, bar, slippage)
            if result is not None:
                exit_price, reason = result
                close_position(asset, position, exit_price, ts, reason)
                del positions[asset]
            else:
                update_trailing_state(position, bar, ts)

        # 3. Allocate candidates becoming eligible at this minute.
        batch = scheduled.get(ts, [])
        if batch:
            # Stable, deterministic ordering for overlapping signals
            # on the same asset before the allocator applies its ranking.
            batch.sort(key=lambda c: (
                -int(c["signal_priority"]),
                float(c["stop_distance_atr"]),
                str(c["asset"]),
                str(c.get("signal_type", "")),
                float(c.get("stop_price", c.get("stop_reference_price", 0.0))),
            ))

            equity_at_open = (
                config.initial_equity
                + realized_pnl
                + sum(
                    _unrealized_pnl(p, p["mark_price"])
                    for p in positions.values()
                )
            )

            open_for_allocator = [
                {
                    "asset": asset,
                    "quantity": p["quantity"],
                    "mark_price": p["mark_price"],
                }
                for asset, p in positions.items()
            ]

            experiment_rejections = []

            if equity_at_open <= 0:
                allocation = {
                    "accepted": [],
                    "rejected": [
                        {"asset": c["asset"], "reason": "non_positive_equity"}
                        for c in batch
                    ],
                    "total_gross_exposure": sum(
                        p["quantity"] * p["mark_price"]
                        for p in positions.values()
                    ),
                    "remaining_exposure": 0.0,
                }
            else:
                allocator_candidates = []
                for c in batch:
                    raw_open = float(bars_at[c["asset"]][ts]["open"])
                    fill_entry = raw_open * (
                        1 + int(c["side"]) * slippage
                    )
                    allocator_candidate = {
                        **c,
                        "entry_price": fill_entry,
                        "signal_available_at": ts,
                    }

                    experiment = c.get("exit_experiment")
                    if experiment is not None:
                        try:
                            resolved = resolve_exit_prices(
                                experiment, c, fill_entry
                            )
                            allocator_candidate.update(resolved)
                            validate_trailing_settings(allocator_candidate)
                        except (ValueError, TypeError, KeyError) as exc:
                            experiment_rejections.append({
                                "asset": c["asset"],
                                "reason": "invalid_experiment_entry: " + str(exc),
                            })
                            continue

                    # Entry slippage is already included in fill_entry.
                    stop_for_sizing = float(allocator_candidate["stop_price"])
                    stop_exit_fill = stop_for_sizing * (
                        1 - int(c["side"]) * slippage
                    )
                    effective_risk_per_unit = (
                        abs(fill_entry - stop_exit_fill)
                        + fee_rate * (fill_entry + stop_exit_fill)
                    )
                    allocator_candidate["risk_per_unit"] = (
                        effective_risk_per_unit
                    )

                    allocator_candidates.append(allocator_candidate)

                try:
                    allocation = allocate_candidates(
                        allocator_candidates,
                        equity=equity_at_open,
                        open_positions=open_for_allocator,
                        config=allocator_config,
                    )
                except ValueError as exc:
                    # Existing exposure can exceed the current equity
                    # cap after adverse mark-to-market movement. Do not
                    # add risk; preserve existing positions.
                    if "already exceed portfolio exposure limit" not in str(exc):
                        raise
                    allocation = {
                        "accepted": [],
                        "rejected": [
                            {
                                "asset": c["asset"],
                                "reason": "existing_exposure_above_current_equity",
                            }
                            for c in batch
                        ],
                        "total_gross_exposure": sum(
                            p["quantity"] * p["mark_price"]
                            for p in positions.values()
                        ),
                        "remaining_exposure": 0.0,
                    }

            allocation["rejected"].extend(experiment_rejections)

            decisions.append({
                "timestamp": ts,
                "equity_at_decision": equity_at_open,
                "accepted": allocation["accepted"],
                "rejected": allocation["rejected"],
                "remaining_exposure": allocation["remaining_exposure"],
            })

            # The allocator returns accepted candidates in ranked order.
            accepted_assets = {p["asset"] for p in allocation["accepted"]}
            candidate_by_asset = {}
            for c in allocator_candidates if equity_at_open > 0 else []:
                candidate_by_asset.setdefault(c["asset"], c)

            for accepted in allocation["accepted"]:
                asset = accepted["asset"]
                c = candidate_by_asset[asset]
                side = int(c["side"])
                entry_price = float(accepted["entry_price"])
                stop_price = float(accepted["stop_price"])
                if "target_price" in c:
                    target_price = float(c["target_price"])
                else:
                    target_pct = float(c["target_pct"])
                    target_price = entry_price * (
                        1 + side * target_pct
                    )

                if side == 1 and not stop_price < entry_price < target_price:
                    raise ValueError("Accepted long has invalid stop/target")
                if side == -1 and not target_price < entry_price < stop_price:
                    raise ValueError("Accepted short has invalid stop/target")

                quantity = float(accepted["quantity"])
                entry_fee = quantity * entry_price * fee_rate

                position = {
                    "side": side,
                    "quantity": quantity,
                    "entry_price": entry_price,
                    "initial_stop_price": stop_price,
                    "stop_price": stop_price,
                    "target_price": target_price,
                    "entry_time": ts,
                    "entry_fee": entry_fee,
                    "funding_pnl": 0.0,
                    "mark_price": float(bars_at[asset][ts]["open"]),
                    "signal_priority": int(c["signal_priority"]),
                    "risk_distance": abs(entry_price - stop_price),
                    "trailing_mode": c.get("trailing_mode", "none"),
                    "trailing_activation_r": c.get("trailing_activation_r"),
                    "trailing_distance_r": c.get("trailing_distance_r"),
                    "trailing_activation_at_target": c.get(
                        "trailing_activation_at_target", False
                    ),
                    "trailing_sl_active": False,
                    "trailing_sl_activation_time": None,
                    "trailing_sl_activation_price": None,
                    "trailing_sl_activation_level": None,
                    "trailing_sl_activation_r": None,
                    "trailing_sl_update_count": 0,
                    "trailing_sl_last_update_time": None,
                    "trailing_tp_active": False,
                    "trailing_tp_activation_time": None,
                    "trailing_tp_activation_price": None,
                    "trailing_tp_activation_level": None,
                    "trailing_tp_activation_r": None,
                    "trailing_tp_price": None,
                    "trailing_tp_update_count": 0,
                    "trailing_tp_last_update_time": None,
                    "best_favorable_price": entry_price,
                    "max_favorable_price": entry_price,
                    "max_favorable_time": None,
                    "max_favorable_excursion_r": 0.0,
                }

                positions[asset] = position
                realized_pnl -= entry_fee

                # The position is active from the candle open. Apply
                # conservative same-minute stop/target handling.
                same_bar_result = _exit_fill(
                    position, bars_at[asset][ts], slippage
                )
                if same_bar_result is not None:
                    exit_price, reason = same_bar_result
                    close_position(asset, position, exit_price, ts, reason)
                    del positions[asset]
                else:
                    update_trailing_state(position, bars_at[asset][ts], ts)

        # 4. Mark remaining positions at this minute's close.
        unrealized = 0.0
        gross_exposure = 0.0
        for asset, position in positions.items():
            close = float(bars_at[asset][ts]["close"])
            position["mark_price"] = close
            unrealized += _unrealized_pnl(position, close)
            gross_exposure += position["quantity"] * close

        equity = config.initial_equity + realized_pnl + unrealized

        # Collect reporting statistics online in both storage modes.
        # Exposure/utilization are sampled once per minute, including the
        # final candle's pre-liquidation mark.
        open_count = len(positions)
        max_concurrent_positions = max(max_concurrent_positions, open_count)
        max_gross_exposure = max(max_gross_exposure, gross_exposure)
        utilization = gross_exposure / equity if equity > 0 else 0.0
        utilization_sum += utilization
        utilization_samples += 1
        max_capital_utilization = max(max_capital_utilization, utilization)
        if equity > 0:
            max_gross_exposure_equity_multiple = max(
                max_gross_exposure_equity_multiple, utilization
            )

        # The final candle is measured after end-of-data liquidation below.
        if ts != timestamps[-1]:
            peak_equity = max(peak_equity, equity)
            drawdown_amount = max(0.0, peak_equity - equity)
            max_drawdown_amount = max(
                max_drawdown_amount, drawdown_amount
            )
            if peak_equity > 0:
                drawdown = drawdown_amount / peak_equity
                max_drawdown = max(max_drawdown, drawdown)

        day_utc = datetime.fromtimestamp(
            ts / 1000.0, tz=timezone.utc
        ).date().isoformat()
        daily_marks_by_date[day_utc] = {
            "timestamp": ts,
            "equity": equity,
        }

        if config.record_equity_curve:
            equity_curve.append({
                "timestamp": ts,
                "equity": equity,
                "realized_pnl": realized_pnl,
                "unrealized_pnl": unrealized,
                "gross_exposure": gross_exposure,
                "open_positions": len(positions),
            })

    # 5. Close any remaining positions at the final available close.
    final_ts = timestamps[-1]
    for asset in list(positions):
        position = positions[asset]
        raw_close = float(bars_at[asset][final_ts]["close"])
        exit_price = raw_close * (1 - position["side"] * slippage)
        close_position(
            asset, position, exit_price, final_ts, "end_of_data"
        )
        del positions[asset]

    final_equity = config.initial_equity + realized_pnl

    # Replace the final pre-liquidation daily mark with realized final equity.
    final_day_utc = datetime.fromtimestamp(
        final_ts / 1000.0, tz=timezone.utc
    ).date().isoformat()
    daily_marks_by_date[final_day_utc] = {
        "timestamp": final_ts,
        "equity": final_equity,
    }

    if equity_curve:
        equity_curve[-1] = {
            "timestamp": final_ts,
            "equity": final_equity,
            "realized_pnl": realized_pnl,
            "unrealized_pnl": 0.0,
            "gross_exposure": 0.0,
            "open_positions": 0,
        }

    peak_equity = max(peak_equity, final_equity)
    final_drawdown_amount = max(0.0, peak_equity - final_equity)
    max_drawdown_amount = max(
        max_drawdown_amount, final_drawdown_amount
    )
    if peak_equity > 0:
        final_drawdown = final_drawdown_amount / peak_equity
        max_drawdown = max(max_drawdown, final_drawdown)

    total_gross_pnl = sum(t["gross_pnl"] for t in trades)
    total_fees = sum(t["total_fees"] for t in trades)
    total_funding = sum(t["funding_pnl"] for t in trades)

    return {
        "initial_equity": config.initial_equity,
        "final_equity": final_equity,
        "net_pnl": final_equity - config.initial_equity,
        "return_pct": (
            (final_equity / config.initial_equity) - 1
        ) * 100,
        "max_drawdown_pct": max_drawdown * 100,
        "max_drawdown_amount": max_drawdown_amount,
        "start_ts": timestamps[0],
        "end_ts": final_ts,
        "daily_equity_marks": [
            daily_marks_by_date[day]
            for day in sorted(daily_marks_by_date)
        ],
        "max_concurrent_positions": max_concurrent_positions,
        "average_capital_utilization_pct": (
            utilization_sum / utilization_samples * 100.0
            if utilization_samples else None
        ),
        "max_capital_utilization_pct": max_capital_utilization * 100.0,
        "max_gross_exposure": max_gross_exposure,
        "max_gross_exposure_equity_multiple": (
            max_gross_exposure_equity_multiple
        ),
        "trade_count": len(trades),
        "total_gross_pnl": total_gross_pnl,
        "total_fees": total_fees,
        "total_funding_pnl": total_funding,
        "trades": trades,
        "equity_curve": equity_curve,
        "decisions": decisions,
    }
