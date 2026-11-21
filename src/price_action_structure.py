"""Causal, indicator-free multi-timeframe price structure detector."""

import math
import numpy as np
import pandas as pd

REQUIRED = ("open", "high", "low", "close")
STRUCTURE_COLUMNS = (
    "pivot_high_confirmed",
    "pivot_low_confirmed",
    "confirmed_pivot_high",
    "confirmed_pivot_low",
    "structure",
    "bos_bullish",
    "bos_bearish",
    "bos_level",
    "structure_available_at",
)


def validate_candles(candles):
    missing = [c for c in REQUIRED if c not in candles.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if candles.empty:
        raise ValueError("Input candles are empty")

    values = candles[list(REQUIRED)].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values <= 0).any():
        raise ValueError("OHLC values must be finite and positive")

    o, h, low, close = values.T
    if (
        (h < np.maximum.reduce([o, close, low])).any()
        or (low > np.minimum(o, close)).any()
    ):
        raise ValueError("Invalid OHLC candle structure")

    if "ts" in candles.columns:
        ts = pd.to_numeric(candles["ts"], errors="coerce").to_numpy()
        if not np.isfinite(ts).all():
            raise ValueError("Timestamps must be finite")
        if len(ts) > 1 and not np.all(np.diff(ts) > 0):
            raise ValueError("Timestamps must be strictly increasing")


def detect_structure(candles, timeframe_ms, left=3, right=3):
    """
    Detect confirmed swings, HH/HL or LH/LL structure, and BOS.

    Input timestamps (if supplied) are candle OPEN timestamps in
    milliseconds. structure_available_at is the candle CLOSE time.

    A swing at index j is confirmed only at j + right.
    BOS is recorded only when a later completed candle crosses a
    previously confirmed swing level. Repeated breaks of one level
    are not emitted.
    """
    validate_candles(candles)

    if not isinstance(timeframe_ms, int) or timeframe_ms <= 0:
        raise ValueError("timeframe_ms must be a positive integer")
    if not isinstance(left, int) or not isinstance(right, int):
        raise ValueError("left and right must be integers")
    if left < 1 or right < 1:
        raise ValueError("left and right must be at least one")

    df = candles.reset_index(drop=True).copy()
    n = len(df)
    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    close = df["close"].to_numpy(float)

    if "ts" in df.columns:
        open_ts = df["ts"].to_numpy(dtype=np.int64)
    else:
        open_ts = np.arange(n, dtype=np.int64) * timeframe_ms

    df["pivot_high_confirmed"] = False
    df["pivot_low_confirmed"] = False
    df["confirmed_pivot_high"] = np.nan
    df["confirmed_pivot_low"] = np.nan
    df["structure"] = "NEUTRAL"
    df["bos_bullish"] = False
    df["bos_bearish"] = False
    df["bos_level"] = np.nan
    df["structure_available_at"] = open_ts + timeframe_ms

    highs = []
    lows = []
    broken_highs = set()
    broken_lows = set()

    for i in range(n):
        candidate = i - right

        # A pivot becomes knowable only after all right candles close.
        if candidate >= left:
            hs = h[candidate-left:candidate+right+1]
            ls = low[candidate-left:candidate+right+1]

            is_high = (
                h[candidate] == hs.max()
                and np.count_nonzero(hs == h[candidate]) == 1
            )
            is_low = (
                low[candidate] == ls.min()
                and np.count_nonzero(ls == low[candidate]) == 1
            )

            if is_high:
                highs.append((candidate, float(h[candidate])))
                df.at[i, "pivot_high_confirmed"] = True
                df.at[i, "confirmed_pivot_high"] = h[candidate]

            if is_low:
                lows.append((candidate, float(low[candidate]))
                )
                df.at[i, "pivot_low_confirmed"] = True
                df.at[i, "confirmed_pivot_low"] = low[candidate]

        # Classify using the latest two confirmed highs and lows.
        state = "NEUTRAL"
        if len(highs) >= 2 and len(lows) >= 2:
            hh = highs[-1][1] > highs[-2][1]
            hl = lows[-1][1] > lows[-2][1]
            lh = highs[-1][1] < highs[-2][1]
            ll = lows[-1][1] < lows[-2][1]

            if hh and hl:
                state = "BULLISH"
            elif lh and ll:
                state = "BEARISH"

        df.at[i, "structure"] = state

        # BOS must occur AFTER the level is confirmed. Requiring a
        # close-to-close crossing prevents retroactive BOS labels.
        if i > 0 and highs:
            level_index, level = highs[-1]
            if (
                i > level_index + right
                and close[i - 1] <= level < close[i]
                and level_index not in broken_highs
            ):
                df.at[i, "bos_bullish"] = True
                df.at[i, "bos_level"] = level
                broken_highs.add(level_index)

        if i > 0 and lows:
            level_index, level = lows[-1]
            if (
                i > level_index + right
                and close[i - 1] >= level > close[i]
                and level_index not in broken_lows
            ):
                df.at[i, "bos_bearish"] = True
                df.at[i, "bos_level"] = level
                broken_lows.add(level_index)

    return df


def align_structure_to_signals(signals, structure, signal_available_col,
                               structure_available_col="structure_available_at"):
    """
    Backward-align completed higher-timeframe structure to signal times.
    Exact availability-time matches are allowed; future rows are forbidden.
    """
    if signal_available_col not in signals:
        raise ValueError(f"Missing {signal_available_col}")
    if structure_available_col not in structure:
        raise ValueError(f"Missing {structure_available_col}")

    left = signals.copy()
    right = structure.copy()
    left["_original_order"] = np.arange(len(left))

    left[signal_available_col] = pd.to_numeric(
        left[signal_available_col], errors="raise"
    )
    right[structure_available_col] = pd.to_numeric(
        right[structure_available_col], errors="raise"
    )

    left = left.sort_values(signal_available_col)
    right = right.sort_values(structure_available_col)

    result = pd.merge_asof(
        left,
        right,
        left_on=signal_available_col,
        right_on=structure_available_col,
        direction="backward",
        allow_exact_matches=True,
        suffixes=("", "_structure"),
    )
    result = result.sort_values("_original_order").drop(
        columns="_original_order"
    ).reset_index(drop=True)

    matched = result[structure_available_col].notna()
    if (
        result.loc[matched, structure_available_col]
        > result.loc[matched, signal_available_col]
    ).any():
        raise AssertionError("Future structure data was attached")

    return result
