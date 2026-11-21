"""Causal 15-minute price-action signal detectors for OKX Price Action V1."""

import numpy as np
import pandas as pd

REQUIRED = ["open", "high", "low", "close", "atr14"]

SIGNAL_COLUMNS = [
    "pivot_high_confirmed",
    "pivot_low_confirmed",
    "bullish_engulfing",
    "bearish_engulfing",
    "bullish_pinbar",
    "bearish_pinbar",
    "support_rejection",
    "resistance_rejection",
    "support_zone_touch",
    "resistance_zone_touch",
    "bullish_ob_created",
    "bearish_ob_created",
    "bullish_ob_first_retest",
    "bearish_ob_first_retest",
]


def validate_candles(df):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("Input candles are empty")

    if df.index.has_duplicates:
        raise ValueError("Duplicate dataframe index")

    values = df[["open", "high", "low", "close"]].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Invalid OHLC values")

    if (values <= 0).any():
        raise ValueError("Prices must be positive")

    invalid = (
        (df["high"].to_numpy() < np.maximum.reduce([
            df["open"].to_numpy(),
            df["close"].to_numpy(),
            df["low"].to_numpy(),
        ]))
        | (df["low"].to_numpy() > np.minimum(
            df["open"].to_numpy(), df["close"].to_numpy()
        ))
    )
    if invalid.any():
        raise ValueError("Invalid OHLC candle structure")

    atr = pd.to_numeric(df["atr14"], errors="coerce").to_numpy()
    if np.isinf(atr).any() or (atr[np.isfinite(atr)] < 0).any():
        raise ValueError("ATR must be finite when present and non-negative")


def detect_signals(candles):
    """
    Return a copy of candles with causal signal columns.

    Every signal is assigned to the candle on which it becomes knowable.
    No signal uses information from a candle that has not yet closed.
    """
    validate_candles(candles)
    df = candles.reset_index(drop=True).copy()
    n = len(df)

    for col in SIGNAL_COLUMNS:
        df[col] = False

    df["confirmed_pivot_high"] = np.nan
    df["confirmed_pivot_low"] = np.nan
    df["bullish_ob_low"] = np.nan
    df["bullish_ob_high"] = np.nan
    df["bearish_ob_low"] = np.nan
    df["bearish_ob_high"] = np.nan

    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    atr = df["atr14"].to_numpy(float)

    # ---------------------------------------------------------
    # 1. Engulfing and pin-bar signals: completed candles only.
    # ---------------------------------------------------------
    for i in range(1, n):
        prev_bull = c[i - 1] > o[i - 1]
        prev_bear = c[i - 1] < o[i - 1]
        curr_bull = c[i] > o[i]
        curr_bear = c[i] < o[i]

        prev_body_low = min(o[i - 1], c[i - 1])
        prev_body_high = max(o[i - 1], c[i - 1])
        curr_body_low = min(o[i], c[i])
        curr_body_high = max(o[i], c[i])

        df.at[i, "bullish_engulfing"] = bool(
            curr_bull and prev_bear
            and curr_body_low <= prev_body_low
            and curr_body_high >= prev_body_high
        )

        df.at[i, "bearish_engulfing"] = bool(
            curr_bear and prev_bull
            and curr_body_low <= prev_body_low
            and curr_body_high >= prev_body_high
        )

        body = abs(c[i] - o[i])
        candle_range = h[i] - l[i]

        if body > 0 and candle_range > 0:
            upper_wick = h[i] - max(o[i], c[i])
            lower_wick = min(o[i], c[i]) - l[i]

            df.at[i, "bullish_pinbar"] = bool(
                lower_wick >= 2.0 * body
                and upper_wick <= body
                and c[i] >= l[i] + 0.75 * candle_range
            )

            df.at[i, "bearish_pinbar"] = bool(
                upper_wick >= 2.0 * body
                and lower_wick <= body
                and c[i] <= l[i] + 0.25 * candle_range
            )

    # ---------------------------------------------------------
    # 2. Confirmed pivots and causal support/resistance zones.
    #
    # A pivot at j is confirmed at j+3, never at j itself.
    # Existing zones are evaluated before adding new pivots
    # confirmed on the current candle.
    # ---------------------------------------------------------
    clusters = {"support": [], "resistance": []}

    for i in range(n):
        # Evaluate zones formed by previously confirmed pivots.
        for kind, signal_col, touch_col in [
            ("support", "support_rejection", "support_zone_touch"),
            ("resistance", "resistance_rejection", "resistance_zone_touch"),
        ]:
            for zone in clusters[kind]:
                if zone["count"] < 2:
                    continue

                lower = zone["center"] - zone["tolerance"]
                upper = zone["center"] + zone["tolerance"]

                overlaps = l[i] <= upper and h[i] >= lower

                # A touch is recorded independently of rejection.
                if overlaps:
                    df.at[i, touch_col] = True

                if kind == "support" and overlaps and c[i] > upper:
                    df.at[i, signal_col] = True

                if kind == "resistance" and overlaps and c[i] < lower:
                    df.at[i, signal_col] = True

        # Confirm candidate pivot exactly three candles ago.
        candidate = i - 3
        if candidate >= 3:
            start = candidate - 3
            end = candidate + 4

            window_highs = h[start:end]
            window_lows = l[start:end]

            pivot_high = (
                h[candidate] == np.max(window_highs)
                and np.count_nonzero(window_highs == h[candidate]) == 1
            )
            pivot_low = (
                l[candidate] == np.min(window_lows)
                and np.count_nonzero(window_lows == l[candidate]) == 1
            )

            if pivot_high:
                df.at[i, "pivot_high_confirmed"] = True
                df.at[i, "confirmed_pivot_high"] = h[candidate]

                tolerance = (
                    0.25 * atr[candidate]
                    if np.isfinite(atr[candidate]) else np.nan
                )
                if np.isfinite(tolerance) and tolerance > 0:
                    _add_zone(
                        clusters["resistance"], h[candidate], tolerance
                    )

            if pivot_low:
                df.at[i, "pivot_low_confirmed"] = True
                df.at[i, "confirmed_pivot_low"] = l[candidate]

                tolerance = (
                    0.25 * atr[candidate]
                    if np.isfinite(atr[candidate]) else np.nan
                )
                if np.isfinite(tolerance) and tolerance > 0:
                    _add_zone(
                        clusters["support"], l[candidate], tolerance
                    )

    # ---------------------------------------------------------
    # 3. Displacement-based order blocks.
    #
    # ATR is taken from the previous candle, so the
    # displacement candle cannot influence its own threshold.
    # Only the first subsequent retest is recorded.
    # Expiry: four completed candles after creation.
    # Invalidation: close beyond the far edge of the zone.
    # ---------------------------------------------------------
    active = {"bullish": [], "bearish": []}

    for i in range(5, n):
        # Check previously created zones first.
        for direction in ("bullish", "bearish"):
            remaining = []

            for zone in active[direction]:
                age = i - zone["created_at"]

                if age > 4:
                    continue

                # Invalidation takes priority over a retest.
                if direction == "bullish" and c[i] < zone["low"]:
                    continue
                if direction == "bearish" and c[i] > zone["high"]:
                    continue

                overlaps = l[i] <= zone["high"] and h[i] >= zone["low"]

                if overlaps:
                    col = (
                        "bullish_ob_first_retest"
                        if direction == "bullish"
                        else "bearish_ob_first_retest"
                    )
                    df.at[i, col] = True
                    continue

                remaining.append(zone)

            active[direction] = remaining

        # ATR must be known before the displacement candle.
        prior_atr = atr[i - 1]
        if not np.isfinite(prior_atr) or prior_atr <= 0:
            continue

        body = abs(c[i] - o[i])
        previous_high = np.max(h[i - 5:i])
        previous_low = np.min(l[i - 5:i])

        # Bullish displacement and last bearish candle.
        if c[i] > o[i] and body >= 1.5 * prior_atr and c[i] > previous_high:
            candidates = [
                j for j in range(i - 5, i)
                if c[j] < o[j]
            ]
            if candidates:
                j = candidates[-1]
                zone = {
                    "low": l[j],
                    "high": h[j],
                    "created_at": i,
                }
                active["bullish"].append(zone)
                df.at[i, "bullish_ob_created"] = True
                df.at[i, "bullish_ob_low"] = l[j]
                df.at[i, "bullish_ob_high"] = h[j]

        # Bearish displacement and last bullish candle.
        if c[i] < o[i] and body >= 1.5 * prior_atr and c[i] < previous_low:
            candidates = [
                j for j in range(i - 5, i)
                if c[j] > o[j]
            ]
            if candidates:
                j = candidates[-1]
                zone = {
                    "low": l[j],
                    "high": h[j],
                    "created_at": i,
                }
                active["bearish"].append(zone)
                df.at[i, "bearish_ob_created"] = True
                df.at[i, "bearish_ob_low"] = l[j]
                df.at[i, "bearish_ob_high"] = h[j]

    return df


def _add_zone(zones, price, tolerance):
    """Add a pivot to a nearby zone or create a new zone."""
    for zone in zones:
        if abs(price - zone["center"]) <= max(
            tolerance, zone["tolerance"]
        ):
            zone["center"] = (
                zone["center"] * zone["count"] + price
            ) / (zone["count"] + 1)
            zone["count"] += 1
            zone["tolerance"] = max(zone["tolerance"], tolerance)
            return

    zones.append({
        "center": float(price),
        "tolerance": float(tolerance),
        "count": 1,
    })


if __name__ == "__main__":
    print("Price Action V1 signal detector module loaded.")
    print("Import detect_signals() from this module to process candles.")
