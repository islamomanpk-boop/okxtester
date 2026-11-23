from pathlib import Path
import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
BASE = Path.home() / "okx_scalping_data"

HORIZONS = {"15M": 15, "1H": 60, "4H": 240, "12H": 720}
EFFICIENCY_MAX = 0.30
OVERLAP_MIN = 0.70
RETEST_BAND_PCT = 0.10

print("=" * 76)
print("FINAL TIMING-CORRECTED BREAKOUT AND RETEST RESEARCH")
print("FIVE ASSETS | READ ONLY | 15M / 1H / 4H / 12H")
print("=" * 76)

# ------------------------------------------------------------
# 1. LOAD FIVE DATASETS AND FIND COMMON MINUTE TIMESTAMPS
# ------------------------------------------------------------

data = {}

for asset in ASSETS:
    path = BASE / f"{asset}_USDT_USDT_1m.csv"
    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(path)
    required = {"ts", "open", "high", "low", "close", "vol"}

    if not required.issubset(df.columns):
        raise ValueError(f"{asset}: missing required columns")

    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df = df.set_index("ts").sort_index()

    if df.index.has_duplicates:
        raise ValueError(f"{asset}: duplicate timestamps")

    data[asset] = df[["open", "high", "low", "close", "vol"]]

common = data[ASSETS[0]].index

for asset in ASSETS[1:]:
    common = common.intersection(data[asset].index)

common = common.sort_values()

print(f"\nCommon 1M timestamps: {len(common):,}")

if len(common) < 10000:
    raise ValueError("Common dataset unexpectedly small")

# Use the same common timestamps for all five assets.
for asset in ASSETS:
    data[asset] = data[asset].reindex(common)

# ------------------------------------------------------------
# 2. BUILD ONLY COMPLETE HIGHER-TIMEFRAME CANDLES
# ------------------------------------------------------------

def complete_bars(df, rule, expected):
    grouped = df.resample(
        rule,
        label="right",
        closed="left"
    )

    bars = grouped.agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "vol": "sum",
    })

    counts = grouped["close"].count()
    return bars.loc[counts == expected].dropna()

def pct(a, b):
    if not np.isfinite(a) or not np.isfinite(b) or b == 0:
        return np.nan
    return (a / b - 1) * 100

def overlap_ratio(high, low):
    previous_high = high.shift(1)
    previous_low = low.shift(1)

    intersection = (
        np.minimum(high, previous_high) -
        np.maximum(low, previous_low)
    ).clip(lower=0)

    smaller = np.minimum(
        high - low,
        previous_high - previous_low
    )

    return (
        intersection / smaller.replace(0, np.nan)
    ).clip(0, 1)

# ------------------------------------------------------------
# 3. BUILD CAUSAL 48H SIDEWAYS CONTEXT
# ------------------------------------------------------------

def build_context(bars4):
    x = bars4.copy()

    # Channel uses the previous 12 completed 4H candles.
    x["upper"] = x["high"].rolling(12).max().shift(1)
    x["lower"] = x["low"].rolling(12).min().shift(1)

    x["channel_width"] = (
        x["upper"] / x["lower"] - 1
    ) * 100

    # Previous 48H net movement.
    net = (
        x["close"].shift(1) /
        x["close"].shift(13) - 1
    ).abs()

    # Previous 48H total absolute close-to-close movement.
    path = (
        x["close"].pct_change().abs()
        .rolling(12).sum().shift(1)
    )

    x["efficiency"] = net / path.replace(0, np.nan)

    x["overlap"] = (
        overlap_ratio(x["high"], x["low"])
        .rolling(12).mean().shift(1)
    )

    return x

# ------------------------------------------------------------
# 4. ANALYSE ONE ASSET
# ------------------------------------------------------------

def analyse_asset(asset, minute):
    bars15 = complete_bars(minute, "15min", 15)
    bars4 = complete_bars(minute, "4h", 240)

    context = build_context(bars4)

    print(f"\n{'=' * 76}")
    print(f"ASSET: {asset}")
    print(f"Complete 15M candles: {len(bars15):,}")
    print(f"Complete 4H candles: {len(bars4):,}")

    # 15M labels are candle closing times.
    # 4H context is available only after its completed close.
    left = bars15.reset_index()
    left = left.rename(columns={left.columns[0]: "time"})

    right = context.reset_index()
    right = right.rename(columns={right.columns[0]: "snapshot"})

    left = left.sort_values("time")
    right = right.sort_values("snapshot")

    joined = pd.merge_asof(
        left,
        right[[
            "snapshot", "upper", "lower",
            "channel_width", "efficiency", "overlap"
        ]],
        left_on="time",
        right_on="snapshot",
        direction="backward"
    ).set_index("time")

    widths = joined["channel_width"].dropna()
    p25 = widths.quantile(0.25)
    p40 = widths.quantile(0.40)

    definitions = {
        "STRICT_P25": p25,
        "BROAD_P40": p40
    }

    print(f"Channel width P25: {p25:.4f}%")
    print(f"Channel width P40: {p40:.4f}%")

    # Minute timestamps are candle OPEN times.
    minute_index = minute.index
    opens = minute["open"].to_numpy()
    highs = minute["high"].to_numpy()
    lows = minute["low"].to_numpy()
    closes = minute["close"].to_numpy()

    minute_positions = pd.Series(
        np.arange(len(minute)),
        index=minute_index
    )

    events = []

    for definition, width_limit in definitions.items():

        sideways = (
            (joined["channel_width"] <= width_limit) &
            (joined["efficiency"] <= EFFICIENCY_MAX) &
            (joined["overlap"] >= OVERLAP_MIN)
        )

        same_snapshot = joined["snapshot"].eq(
            joined["snapshot"].shift(1)
        )

        previous_close = joined["close"].shift(1)
        current_close = joined["close"]

        upper_break = (
            sideways & same_snapshot &
            (previous_close <= joined["upper"]) &
            (current_close > joined["upper"])
        )

        lower_break = (
            sideways & same_snapshot &
            (previous_close >= joined["lower"]) &
            (current_close < joined["lower"])
        )

        for direction, signal_mask in [
            ("UPPER", upper_break),
            ("LOWER", lower_break)
        ]:

            signal_times = joined.index[
                signal_mask.fillna(False)
            ]

            for signal_time in signal_times:
                row = joined.loc[signal_time]

                # CRITICAL TIMING CORRECTION:
                # 15M candle label is its closing time.
                # Its final 1M candle opens one minute earlier.
                last_signal_minute = (
                    signal_time - pd.Timedelta(minutes=1)
                )

                signal_pos = minute_positions.get(
                    last_signal_minute
                )

                if pd.isna(signal_pos):
                    continue

                signal_pos = int(signal_pos)
                start = signal_pos + 1

                if start >= len(minute):
                    continue

                boundary = float(
                    row["upper"] if direction == "UPPER"
                    else row["lower"]
                )

                if not np.isfinite(boundary) or boundary <= 0:
                    continue

                band_high = boundary * (
                    1 + RETEST_BAND_PCT / 100
                )
                band_low = boundary * (
                    1 - RETEST_BAND_PCT / 100
                )

                # The signal candle's final 1M close is the
                # previous close for the first follow-up minute.
                previous_minute_close = closes[signal_pos]

                retest_pos = None
                retest_depth = np.nan
                boundary_crossed = False
                retest_hold = np.nan
                hold_pos = None

                # Search up to 12H after signal confirmation.
                # Start at the FIRST follow-up minute.
                search_end = min(start + 720, len(minute))

                for j in range(start, search_end):

                    if direction == "UPPER":
                        approached = (
                            previous_minute_close > band_high
                            and lows[j] <= band_high
                        )

                        depth = max(
                            0.0,
                            (boundary - lows[j]) / boundary * 100
                        )

                        crossed = lows[j] <= boundary

                    else:
                        approached = (
                            previous_minute_close < band_low
                            and highs[j] >= band_low
                        )

                        depth = max(
                            0.0,
                            (highs[j] - boundary) / boundary * 100
                        )

                        crossed = highs[j] >= boundary

                    if approached:
                        retest_pos = j
                        retest_depth = depth
                        boundary_crossed = bool(crossed)

                        # Index of the next completed 15M close
                        # after the retest candle.
                        elapsed = j - start
                        hold_pos = (
                            start + ((elapsed // 15) + 1) * 15 - 1
                        )

                        if hold_pos < len(minute):
                            if direction == "UPPER":
                                retest_hold = (
                                    closes[hold_pos] > boundary
                                )
                            else:
                                retest_hold = (
                                    closes[hold_pos] < boundary
                                )
                        break

                    previous_minute_close = closes[j]

                # ------------------------------------------------
                # FOLLOW-UP HORIZONS
                # ------------------------------------------------

                for horizon, minutes in HORIZONS.items():

                    end = start + minutes

                    # Require a complete follow-up horizon.
                    if end > len(minute):
                        continue

                    window_high = highs[start:end]
                    window_low = lows[start:end]
                    window_close = closes[start:end]

                    entry = opens[start]

                    if direction == "UPPER":
                        mfe = pct(np.max(window_high), entry)
                        mae = pct(np.min(window_low), entry)
                        extension = pct(
                            np.max(window_high), boundary
                        )
                        returned = bool(
                            np.any(window_close < boundary)
                        )
                        ended_inside = bool(
                            window_close[-1] < boundary
                        )
                    else:
                        mfe = pct(entry, np.min(window_low))
                        mae = pct(entry, np.max(window_high))
                        extension = pct(
                            boundary, np.min(window_low)
                        )
                        returned = bool(
                            np.any(window_close > boundary)
                        )
                        ended_inside = bool(
                            window_close[-1] > boundary
                        )

                    approach_in_horizon = (
                        retest_pos is not None and retest_pos < end
                    )

                    penetration_in_horizon = (
                        approach_in_horizon and boundary_crossed
                    )

                    elapsed_minutes = (
                        retest_pos - start + 1
                        if approach_in_horizon else np.nan
                    )

                    depth_value = (
                        retest_depth
                        if approach_in_horizon else np.nan
                    )

                    # Only evaluate hold if its confirming 15M
                    # close is inside this follow-up horizon.
                    hold_value = (
                        retest_hold
                        if (
                            approach_in_horizon
                            and hold_pos is not None
                            and hold_pos < end
                        )
                        else np.nan
                    )

                    events.append({
                        "asset": asset,
                        "definition": definition,
                        "direction": direction,
                        "signal_time": signal_time,
                        "horizon": horizon,
                        "mfe_pct": mfe,
                        "mae_pct": mae,
                        "extension_pct": extension,
                        "return_inside": returned,
                        "ended_inside": ended_inside,
                        "band_approach": approach_in_horizon,
                        "boundary_penetration": penetration_in_horizon,
                        "retest_minutes": elapsed_minutes,
                        "penetration_depth_pct": depth_value,
                        "retest_hold": hold_value
                    })

    result = pd.DataFrame(events)

    if result.empty:
        print("No qualifying breakout events.")
        return result

    # Event counts once per signal, not once per horizon.
    unique_events = result.drop_duplicates(
        ["asset", "definition", "direction", "signal_time"]
    )

    print("\nBREAKOUT EVENT COUNTS")
    print(
        unique_events.groupby(
            ["definition", "direction"]
        ).size().to_string()
    )

    for horizon in HORIZONS:
        sub = result[result["horizon"] == horizon]

        print(f"\n--- {horizon} FOLLOW-UP ---")

        summary = sub.groupby(
            ["definition", "direction"]
        ).agg(
            n=("mfe_pct", "count"),
            median_extension_pct=("extension_pct", "median"),
            median_mfe_pct=("mfe_pct", "median"),
            median_mae_pct=("mae_pct", "median"),
            return_inside_pct=("return_inside", "mean"),
            ended_inside_pct=("ended_inside", "mean"),
            band_approach_pct=("band_approach", "mean"),
            boundary_penetration_pct=(
                "boundary_penetration", "mean"
            ),
            median_retest_minutes=("retest_minutes", "median"),
            median_penetration_depth_pct=(
                "penetration_depth_pct", "median"
            ),
            retest_hold_pct=("retest_hold", "mean")
        )

        percent_columns = [
            "return_inside_pct",
            "ended_inside_pct",
            "band_approach_pct",
            "boundary_penetration_pct",
            "retest_hold_pct"
        ]

        summary[percent_columns] *= 100

        print(summary.round(4).to_string())

    return result

# ------------------------------------------------------------
# 5. RUN ALL FIVE ASSETS
# ------------------------------------------------------------

all_results = []

for asset in ASSETS:
    result = analyse_asset(asset, data[asset])
    if not result.empty:
        all_results.append(result)

print("\n" + "=" * 76)
print("===== END OF FINAL TIMING-CORRECTED STUDY =====")
print("15M signals use completed candles only.")
print("Signal maps to the final 1M candle inside that 15M candle.")
print("Follow-up begins at the next 1M candle open.")
print("Incomplete 15M and 4H candles are excluded.")
print("Retest search includes the first follow-up minute.")
print("Band approach and actual boundary penetration are separate.")
print("Retest hold uses the next completed 15M close.")
print("All four follow-up horizons are included.")
print("No fees, slippage, funding, fills or profitability are tested.")
print("Full-sample P25/P40 thresholds remain exploratory.")
print("Read-only: no files written or changed.")
print("=" * 76)
