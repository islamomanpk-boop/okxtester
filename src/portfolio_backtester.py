"""Event-driven, shared-capital one-minute portfolio backtester."""

from bisect import bisect_left
import math

from portfolio_engine import PortfolioConfig, allocate_candidates
from trailing_exit import validate_trailing_settings, update_trailing_state
from exit_experiment_config import resolve_exit_prices


class PortfolioBacktestConfig:
    def __init__(
        self,
        initial_equity=1000.0,
        risk_fraction=0.005,
        max_gross_leverage=1.0,
        taker_fee_rate=None,
        slippage_bps=None,
    ):
        self.initial_equity = float(initial_equity)
        self.risk_fraction = float(risk_fraction)
        self.max_gross_leverage = float(max_gross_leverage)
        self.taker_fee_rate = taker_fee_rate
        self.slippage_bps = slippage_bps
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


def _validate_bars_by_asset(bars_by_asset):
    if not isinstance(bars_by_asset, dict) or not bars_by_asset:
        raise ValueError("bars_by_asset must be a non-empty dictionary")

    timelines = {}
    for asset, bars in bars_by_asset.items():
        if not str(asset).strip() or not bars:
            raise ValueError("Every asset needs a name and execution candles")

        timestamps = []
        previous = None

        for bar in bars:
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

            if previous is not None:
                if ts - previous != 60_000:
                    raise ValueError(
                        f"{asset} candles must be strictly chronological "
                        "and exactly one minute apart"
                    )

            timestamps.append(ts)
            previous = ts

        timelines[asset] = timestamps

    reference = next(iter(timelines.values()))
    for asset, timestamps in timelines.items():
        if timestamps != reference:
            raise ValueError(
                f"{asset} timestamps do not match the common portfolio timeline"
            )

    return reference


def _validate_funding(bars_by_asset, funding_by_asset):
    if not isinstance(funding_by_asset, dict):
        raise ValueError("Explicit funding data is required for every asset")

    for asset in bars_by_asset:
        if asset not in funding_by_asset:
            raise ValueError(f"Funding data key missing for {asset}")

        previous = None
        for event in funding_by_asset[asset]:
            if "funding_time" not in event or "funding_rate" not in event:
                raise ValueError(f"{asset} funding event is missing fields")

            ts = int(event["funding_time"])
            rate = float(event["funding_rate"])

            if not math.isfinite(rate) or not -1 <= rate <= 1:
                raise ValueError(f"{asset} has invalid funding rate")
            if previous is not None and ts <= previous:
                raise ValueError(f"{asset} funding events must be chronological")

            if event.get("mark_price") is not None:
                mark = float(event["mark_price"])
                if not math.isfinite(mark) or mark <= 0:
                    raise ValueError(f"{asset} has invalid funding mark price")

            previous = ts


def _validate_candidates(candidates, bars_by_asset, timestamps):
    scheduled = {ts: [] for ts in timestamps}

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
        scheduled[entry_ts].append(dict(candidate))

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
    _validate_funding(bars_by_asset, funding_by_asset)

    scheduled = _validate_candidates(
        candidates, bars_by_asset, timestamps
    )

    assets = list(bars_by_asset)
    bars_at = {
        asset: {
            int(bar["ts"]): bar for bar in bars_by_asset[asset]
        }
        for asset in assets
    }

    funding_at = {asset: {} for asset in assets}
    for asset in assets:
        for event in funding_by_asset[asset]:
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
            "stop_price": position["stop_price"],
            "target_price": position["target_price"],
            "signal_priority": position["signal_priority"],
            "gross_pnl": gross_pnl,
            "funding_pnl": position["funding_pnl"],
            "entry_fee": position["entry_fee"],
            "exit_fee": exit_fee,
            "total_fees": position["entry_fee"] + exit_fee,
            "net_pnl": net_pnl,
            "exit_reason": reason,
        })

    for ts in timestamps:
        # 1. Apply funding to positions open before this settlement time.
        # The candle close is a documented proxy if mark_price is absent.
        for asset in assets:
            position = positions.get(asset)
            if position is None or position["entry_time"] >= ts:
                continue

            bar = bars_at[asset][ts]
            for event in funding_at[asset].get(ts, []):
                mark = event.get("mark_price")
                if mark is None:
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
                update_trailing_state(position, bar)

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
                    "trailing_tp_active": False,
                    "trailing_tp_price": None,
                    "best_favorable_price": entry_price,
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
                    update_trailing_state(position, bars_at[asset][ts])

        # 4. Mark remaining positions at this minute's close.
        unrealized = 0.0
        gross_exposure = 0.0
        for asset, position in positions.items():
            close = float(bars_at[asset][ts]["close"])
            position["mark_price"] = close
            unrealized += _unrealized_pnl(position, close)
            gross_exposure += position["quantity"] * close

        equity = config.initial_equity + realized_pnl + unrealized
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

    if equity_curve:
        equity_curve[-1] = {
            "timestamp": final_ts,
            "equity": final_equity,
            "realized_pnl": realized_pnl,
            "unrealized_pnl": 0.0,
            "gross_exposure": 0.0,
            "open_positions": 0,
        }

    peak = config.initial_equity
    max_drawdown = 0.0
    for point in equity_curve:
        peak = max(peak, point["equity"])
        if peak > 0:
            drawdown = (peak - point["equity"]) / peak
            max_drawdown = max(max_drawdown, drawdown)

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
        "trade_count": len(trades),
        "total_gross_pnl": total_gross_pnl,
        "total_fees": total_fees,
        "total_funding_pnl": total_funding,
        "trades": trades,
        "equity_curve": equity_curve,
        "decisions": decisions,
    }
