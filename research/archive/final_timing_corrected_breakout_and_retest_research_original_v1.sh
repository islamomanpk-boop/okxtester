cd ~/okxtester

python - <<'PY'
import pandas as pd
import numpy as np
from pathlib import Path

assets = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
base = Path.home() / "okx_scalping_data"

print("SIDEWAYS BREAKOUT CONTINUATION AND RETEST STUDY")
print("15M CONFIRMED BREAKOUT | 1M FOLLOW-UP | READ ONLY")

# --------------------------------------------------
# 1. LOAD COMMON 1M TIMESTAMPS
# --------------------------------------------------

raw = {}

for asset in assets:
    path = base / f"{asset}_USDT_USDT_1m.csv"

    d = pd.read_csv(path, usecols=[
        "ts", "open", "high", "low", "close"
    ])

    d["ts"] = pd.to_datetime(
        d["ts"], unit="ms", utc=True
    )

    d = d.set_index("ts").sort_index()
    raw[asset] = d

common = raw[assets[0]].index

for asset in assets[1:]:
    common = common.intersection(raw[asset].index)

common = common.sort_values()

data = {
    asset: raw[asset].loc[common].copy()
    for asset in assets
}

print("Common 1M candles:", len(common))
print("All calculations use common timestamps.")

# --------------------------------------------------
# 2. RESAMPLING
# --------------------------------------------------

def make_bars(df, rule, expected):
    x = df.resample(
        rule, origin="epoch",
        label="left", closed="left"
    ).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last"
    })

    counts = df["close"].resample(
        rule, origin="epoch",
        label="left", closed="left"
    ).count()

    return x.loc[counts == expected].copy()

# --------------------------------------------------
# 3. SIDEWAYS CLASSIFICATION AND BREAKOUTS
# --------------------------------------------------

horizons = {
    "1H": (60, 4),
    "4H": (240, 16),
    "12H": (720, 48)
}

RETEST_BAND_PCT = 0.10

def pct(x):
    return 100.0 * x

def analyse_asset(asset, one):

    h4 = make_bars(one, "4h", 240)
    m15 = make_bars(one, "15min", 15)

    print("\n" + "=" * 70)
    print("ASSET:", asset)
    print("4H bars:", len(h4), "| 15M bars:", len(m15))

    # 48H channel: 12 complete 4H candles
    upper = h4["high"].rolling(12).max()
    lower = h4["low"].rolling(12).min()

    width = (upper / lower - 1) * 100

    # Directional efficiency across 12 candles
    net_move = (
        h4["close"] / h4["close"].shift(11) - 1
    ).abs()

    path_move = (
        h4["close"].pct_change().abs()
        .rolling(11).sum()
    )

    efficiency = net_move / path_move.replace(0, np.nan)

    # Mean overlap across 11 adjacent candle pairs
    prev_high = h4["high"].shift(1)
    prev_low = h4["low"].shift(1)

    intersection = (
        np.minimum(h4["high"], prev_high)
        - np.maximum(h4["low"], prev_low)
    ).clip(lower=0)

    smaller_range = np.minimum(
        h4["high"] - h4["low"],
        prev_high - prev_low
    )

    overlap_pair = (
        intersection / smaller_range.replace(0, np.nan)
    )

    overlap = overlap_pair.rolling(11).mean()

    features = pd.DataFrame({
        "upper": upper,
        "lower": lower,
        "width": width,
        "efficiency": efficiency,
        "overlap": overlap
    })

    features = features.dropna()

    q25 = features["width"].quantile(0.25)
    q40 = features["width"].quantile(0.40)

    # A feature snapshot becomes available only
    # after its 4H candle has completed.
    features["snapshot_time"] = (
        features.index + pd.Timedelta(hours=4)
    )

    snapshots = features.reset_index(drop=True)

    # Map the latest confirmed 4H snapshot to 15M bars
    m15_temp = m15.copy()
    m15_temp.index.name = "bar_start"
    m15_temp = m15_temp.reset_index()

    aligned = pd.merge_asof(
        m15_temp.sort_values("bar_start"),
        snapshots.sort_values("snapshot_time"),
        left_on="bar_start",
        right_on="snapshot_time",
        direction="backward"
    ).set_index("bar_start")

    # Full-sample quantiles are exploratory only.
    definitions = {
        "STRICT_P25": q25,
        "BROAD_P40": q40
    }

    for definition, threshold in definitions.items():

        selected = (
            (aligned["width"] <= threshold)
            & (aligned["efficiency"] <= 0.30)
            & (aligned["overlap"] >= 0.70)
        )

        same_snapshot = (
            aligned["snapshot_time"]
            .eq(aligned["snapshot_time"].shift(1))
        )

        previous_selected = (
            selected.shift(1).fillna(False).astype(bool)
        )

        valid_cross = (
            selected
            & previous_selected
            & same_snapshot
        )

        previous_close = aligned["close"].shift(1)

        # Breakout must cross the same frozen boundary.
        upper_events = valid_cross & (
            (aligned["close"] > aligned["upper"])
            & (previous_close <= aligned["upper"])
        )

        lower_events = valid_cross & (
            (aligned["close"] < aligned["lower"])
            & (previous_close >= aligned["lower"])
        )

        print("\n", definition)
        print("Channel width threshold:", round(threshold, 4), "%")
        print("Selected 15M bars:", int(selected.sum()))

        minute_index = one.index
        m15_index = m15.index

        for direction, mask in [
            ("UPPER", upper_events),
            ("LOWER", lower_events)
        ]:

            event_positions = np.flatnonzero(mask.to_numpy())

            events = []

            for p in event_positions:
                event_time = aligned.index[p]

                boundary = (
                    aligned["upper"].iloc[p]
                    if direction == "UPPER"
                    else aligned["lower"].iloc[p]
                )

                confirmation = (
                    event_time + pd.Timedelta(minutes=15)
                )

                # Exact next-minute timestamp required
                minute_pos = minute_index.get_indexer(
                    [confirmation]
                )[0]

                if minute_pos < 0:
                    continue

                # Find the original 15M event bar
                m15_pos = m15_index.get_indexer(
                    [event_time]
                )[0]

                if m15_pos < 0:
                    continue

                events.append({
                    "time": event_time,
                    "confirmation": confirmation,
                    "boundary": float(boundary),
                    "minute_pos": int(minute_pos),
                    "m15_pos": int(m15_pos)
                })

            print("\n", direction)
            print("Confirmed breakout events:", len(events))

            for horizon_name, (minutes, bars15) in horizons.items():

                records = []

                for event in events:

                    start = event["minute_pos"]
                    end = start + minutes

                    if end > len(one):
                        continue

                    future = one.iloc[start:end]

                    # Require exact continuous 1M coverage
                    expected_index = pd.date_range(
                        start=future.index[0],
                        periods=minutes,
                        freq="1min"
                    )

                    if not future.index.equals(expected_index):
                        continue

                    boundary = event["boundary"]
                    entry = float(future["open"].iloc[0])

                    if direction == "UPPER":
                        favourable = pct(
                            future["high"].max() / entry - 1
                        )
                        adverse = pct(
                            1 - future["low"].min() / entry
                        )
                        extension = pct(
                            future["high"].max() / boundary - 1
                        )

                        touch = (
                            (future["low"] <= boundary * (
                                1 + RETEST_BAND_PCT / 100
                            ))
                            & (future["high"] >= boundary * (
                                1 - RETEST_BAND_PCT / 100
                            ))
                        )

                        inside = (
                            future["close"] <= boundary
                        )

                    else:
                        favourable = pct(
                            1 - future["low"].min() / entry
                        )
                        adverse = pct(
                            future["high"].max() / entry - 1
                        )
                        extension = pct(
                            1 - future["low"].min() / boundary
                        )

                        touch = (
                            (future["high"] >= boundary * (
                                1 - RETEST_BAND_PCT / 100
                            ))
                            & (future["low"] <= boundary * (
                                1 + RETEST_BAND_PCT / 100
                            ))
                        )

                        inside = (
                            future["close"] >= boundary
                        )

                    # First retest of the frozen boundary zone
                    touch_positions = np.flatnonzero(
                        touch.to_numpy()
                    )

                    has_retest = len(touch_positions) > 0

                    retest_minutes = np.nan
                    retest_depth = np.nan
                    retest_range = np.nan
                    retest_body = np.nan
                    retest_hold = np.nan

                    if has_retest:
                        r = int(touch_positions[0])
                        candle = future.iloc[r]

                        retest_minutes = r

                        retest_range = pct(
                            candle["high"] / candle["low"] - 1
                        )

                        retest_body = pct(
                            abs(candle["close"] / candle["open"] - 1)
                        )

                        if direction == "UPPER":
                            retest_depth = max(
                                0,
                                pct(
                                    1 - candle["low"] / boundary
                                )
                            )
                            retest_hold = (
                                candle["close"] >= boundary
                            )
                        else:
                            retest_depth = max(
                                0,
                                pct(
                                    candle["high"] / boundary - 1
                                )
                            )
                            retest_hold = (
                                candle["close"] <= boundary
                            )

                    # Return-inside test uses subsequent
                    # completed 15M closes and frozen boundary.
                    p15 = event["m15_pos"] + 1
                    future15 = m15.iloc[p15:p15 + bars15]

                    if len(future15) != bars15:
                        continue

                    expected15 = pd.date_range(
                        start=event["time"] + pd.Timedelta(minutes=15),
                        periods=bars15,
                        freq="15min"
                    )

                    if not future15.index.equals(expected15):
                        continue

                    if direction == "UPPER":
                        returned_inside = (
                            future15["close"] <= boundary
                        )
                    else:
                        returned_inside = (
                            future15["close"] >= boundary
                        )

                    records.append({
                        "favourable": favourable,
                        "adverse": adverse,
                        "extension": extension,
                        "retest": has_retest,
                        "retest_minutes": retest_minutes,
                        "retest_depth": retest_depth,
                        "retest_range": retest_range,
                        "retest_body": retest_body,
                        "retest_hold": retest_hold,
                        "returned_inside": bool(
                            returned_inside.any()
                        ),
                        "ended_inside": bool(
                            returned_inside.iloc[-1]
                        )
                    })

                r = pd.DataFrame(records)

                if r.empty:
                    print(horizon_name, "No complete events.")
                    continue

                retests = r[r["retest"]]

                print(
                    f"\n{horizon_name} | n={len(r)} "
                    f"| RETEST={r['retest'].mean()*100:.1f}% "
                    f"| RETURN_INSIDE="
                    f"{r['returned_inside'].mean()*100:.1f}% "
                    f"| ENDED_INSIDE="
                    f"{r['ended_inside'].mean()*100:.1f}%"
                )

                print(
                    "  Continuation beyond boundary: "
                    f"median={r['extension'].median():.3f}% "
                    f"P90={r['extension'].quantile(.90):.3f}%"
                )

                print(
                    "  Favourable excursion: "
                    f"median={r['favourable'].median():.3f}% "
                    f"P90={r['favourable'].quantile(.90):.3f}%"
                )

                print(
                    "  Adverse excursion: "
                    f"median={r['adverse'].median():.3f}% "
                    f"P90={r['adverse'].quantile(.90):.3f}%"
                )

                if len(retests):
                    print(
                        "  First retest: "
                        f"n={len(retests)} "
                        f"median time={retests['retest_minutes'].median():.0f} min "
                        f"median penetration={retests['retest_depth'].median():.3f}%"
                    )

                    print(
                        "  First retest candle: "
                        f"median range={retests['retest_range'].median():.3f}% "
                        f"median body={retests['retest_body'].median():.3f}% "
                        f"close holds breakout side="
                        f"{retests['retest_hold'].mean()*100:.1f}%"
                    )
                else:
                    print("  No retests in this horizon.")

    print("\nCompleted:", asset)


# --------------------------------------------------
# 4. RUN ALL FIVE ASSETS
# --------------------------------------------------

for asset in assets:
    analyse_asset(asset, data[asset])

print("\n" + "=" * 70)
print("===== END OF STUDY =====")
print("Breakout confirmed at completed 15M candle close.")
print("Follow-up begins at the next 1M candle.")
print("The original breakout boundary is frozen per event.")
print("Retest zone is 0.10% around that boundary.")
print("Return-inside test uses subsequent completed 15M closes.")
print("Full-sample channel quantiles are exploratory, not live thresholds.")
print("Overlapping breakout follow-ups may occur.")
print("No fees, fills or profitability are modelled.")
print("READ ONLY - NO FILES WRITTEN OR CHANGED.")
PY