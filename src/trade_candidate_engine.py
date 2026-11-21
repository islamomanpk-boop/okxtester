"""Causal, vectorized Model A trend trade-candidate generation."""

import math

import numpy as np
import pandas as pd


DURATION_MS = 15 * 60 * 1000
STOP_ATR_BUFFER = 0.10

REQUIRED = [
    "ts",
    "signal_available_at",
    "open",
    "high",
    "low",
    "close",
    "atr14",
    "pa_direction_permission",
    "bullish_engulfing",
    "bearish_engulfing",
    "bullish_pinbar",
    "bearish_pinbar",
    "support_rejection",
    "resistance_rejection",
    "support_zone_touch",
    "resistance_zone_touch",
    "bullish_ob_first_retest",
    "bearish_ob_first_retest",
]


def _bool(value):
    """Convert supported CSV boolean representations safely."""
    if pd.isna(value):
        return False
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (int, float, np.integer, np.floating)):
        if value == 0:
            return False
        if value == 1:
            return True
        raise ValueError(f"Invalid boolean value: {value!r}")
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "1", "yes"):
            return True
        if normalized in ("false", "0", "no", ""):
            return False
    raise ValueError(f"Invalid boolean value: {value!r}")


def _timestamp_ms(series, column_name):
    """Convert a timestamp column to Unix milliseconds."""
    if pd.api.types.is_numeric_dtype(series):
        numeric = pd.to_numeric(series, errors="raise")
        if numeric.isna().any():
            raise ValueError(f"Missing timestamps in {column_name}")
        values = numeric.to_numpy(dtype=np.float64)
        if not np.isfinite(values).all():
            raise ValueError(f"Invalid timestamps in {column_name}")
        return values.astype(np.int64)

    parsed = pd.to_datetime(series, utc=True, errors="raise")
    if parsed.isna().any():
        raise ValueError(f"Missing timestamps in {column_name}")

    # Explicit nanosecond conversion supports pandas datetime64[us] too.
    parsed_ns = parsed.astype("datetime64[ns, UTC]")
    return parsed_ns.astype("int64").to_numpy() // 1_000_000


def _validate_dataset(df):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Dataset must be a pandas DataFrame")

    missing = [column for column in REQUIRED if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("Dataset is empty")

    ts = _timestamp_ms(df["ts"], "ts")
    available = _timestamp_ms(
        df["signal_available_at"], "signal_available_at"
    )

    if pd.Series(ts).duplicated().any():
        raise ValueError("Duplicate signal timestamps")

    if np.any(np.diff(ts) <= 0):
        raise ValueError("Signal timestamps must be strictly chronological")

    if not np.array_equal(available, ts + DURATION_MS):
        raise ValueError(
            "signal_available_at must equal ts plus 15 minutes"
        )

    permissions = df["pa_direction_permission"].astype(str).to_numpy()
    allowed = np.isin(
        permissions, ["LONG_ONLY", "SHORT_ONLY", "NO_TREND"]
    )
    if not allowed.all():
        raise ValueError("Invalid direction permission")

    numeric = df[["open", "high", "low", "close", "atr14"]].apply(
        pd.to_numeric, errors="coerce"
    )
    prices = numeric[["open", "high", "low", "close"]].to_numpy(
        dtype=np.float64
    )
    atr = numeric["atr14"].to_numpy(dtype=np.float64)

    if not np.isfinite(prices).all() or np.any(prices <= 0):
        raise ValueError("OHLC prices must be finite and positive")

    open_values = prices[:, 0]
    high_values = prices[:, 1]
    low_values = prices[:, 2]
    close_values = prices[:, 3]

    if (
        np.any(high_values < np.maximum.reduce(
            [open_values, close_values, low_values]
        ))
        or np.any(low_values > np.minimum.reduce(
            [open_values, close_values, high_values]
        ))
    ):
        raise ValueError("Invalid OHLC candle structure")

    if np.isinf(atr).any() or np.any(atr[np.isfinite(atr)] < 0):
        raise ValueError("Invalid ATR values")

    boolean_columns = [
        "bullish_engulfing",
        "bearish_engulfing",
        "bullish_pinbar",
        "bearish_pinbar",
        "support_rejection",
        "resistance_rejection",
        "support_zone_touch",
        "resistance_zone_touch",
        "bullish_ob_first_retest",
        "bearish_ob_first_retest",
    ]

    flags = {}
    for column in boolean_columns:
        try:
            flags[column] = df[column].map(_bool).to_numpy(dtype=bool)
        except ValueError as exc:
            raise ValueError(f"Invalid boolean in {column}: {exc}") from exc

    return {
        "ts": ts,
        "available": available,
        "permissions": permissions,
        "open": open_values,
        "high": high_values,
        "low": low_values,
        "close": close_values,
        "atr": atr,
        "flags": flags,
    }


def build_candidates(df, asset=None):
    """Build one highest-priority candidate per asset and signal candle."""
    data = _validate_dataset(df)
    count = len(df)

    if asset is None:
        if "symbol" not in df.columns:
            raise ValueError("asset is required when symbol column is absent")
        symbols = df["symbol"].astype(str).to_numpy()
        unique_symbols = pd.unique(symbols)
        if len(unique_symbols) != 1:
            raise ValueError(
                "Dataset must contain exactly one symbol when asset is omitted"
            )
        asset = unique_symbols[0]

    permissions = data["permissions"]
    long_allowed = permissions == "LONG_ONLY"
    short_allowed = permissions == "SHORT_ONLY"
    flags = data["flags"]

    # Keep only the best event for each candle.
    best_priority = np.zeros(count, dtype=np.int8)
    best_type = np.full(count, "", dtype=object)
    best_side = np.zeros(count, dtype=np.int8)

    events = [
        (
            long_allowed & flags["support_rejection"],
            3, 1, "support_rejection",
        ),
        (
            long_allowed & flags["bullish_ob_first_retest"],
            3, 1, "bullish_ob_first_retest",
        ),
        (
            short_allowed & flags["resistance_rejection"],
            3, -1, "resistance_rejection",
        ),
        (
            short_allowed & flags["bearish_ob_first_retest"],
            3, -1, "bearish_ob_first_retest",
        ),
        (
            long_allowed
            & flags["bullish_engulfing"]
            & flags["support_zone_touch"],
            2, 1, "bullish_engulfing_at_support",
        ),
        (
            long_allowed
            & flags["bullish_pinbar"]
            & flags["support_zone_touch"],
            2, 1, "bullish_pinbar_at_support",
        ),
        (
            short_allowed
            & flags["bearish_engulfing"]
            & flags["resistance_zone_touch"],
            2, -1, "bearish_engulfing_at_resistance",
        ),
        (
            short_allowed
            & flags["bearish_pinbar"]
            & flags["resistance_zone_touch"],
            2, -1, "bearish_pinbar_at_resistance",
        ),
        (
            long_allowed & flags["bullish_engulfing"],
            1, 1, "bullish_engulfing",
        ),
        (
            long_allowed & flags["bullish_pinbar"],
            1, 1, "bullish_pinbar",
        ),
        (
            short_allowed & flags["bearish_engulfing"],
            1, -1, "bearish_engulfing",
        ),
        (
            short_allowed & flags["bearish_pinbar"],
            1, -1, "bearish_pinbar",
        ),
    ]

    for mask, priority, side, signal_type in events:
        better = mask & (
            (best_priority < priority)
            | (
                (best_priority == priority)
                & (
                    (best_type == "")
                    | (signal_type < best_type)
                )
            )
        )
        best_priority[better] = priority
        best_type[better] = signal_type
        best_side[better] = side

    candidate_indices = np.flatnonzero(
        (best_priority > 0)
        & np.isfinite(data["atr"])
        & (data["atr"] > 0)
    )

    if len(candidate_indices) == 0:
        return []

    if "daily_structure" in df.columns:
        daily = df["daily_structure"].astype(str).to_numpy()
    else:
        daily = np.full(count, "", dtype=object)

    if "four_hour_structure" in df.columns:
        four_hour = df["four_hour_structure"].astype(str).to_numpy()
    else:
        four_hour = np.full(count, "", dtype=object)

    if "symbol" in df.columns:
        symbols = df["symbol"].astype(str).to_numpy()
    else:
        symbols = np.full(count, str(asset), dtype=object)

    candidates = []

    # Python iteration is now limited to actual candidates, not all candles.
    for i in candidate_indices:
        side = int(best_side[i])
        atr = float(data["atr"][i])
        close = float(data["close"][i])

        if side == 1:
            stop_reference = float(
                data["low"][i] - STOP_ATR_BUFFER * atr
            )
        else:
            stop_reference = float(
                data["high"][i] + STOP_ATR_BUFFER * atr
            )

        candidates.append({
            "asset": str(asset if asset is not None else symbols[i]),
            "side": side,
            "signal_ts": int(data["ts"][i]),
            "signal_available_at": int(data["available"][i]),
            "signal_priority": int(best_priority[i]),
            "signal_type": str(best_type[i]),
            "strategy_family": "MODEL_A_TREND",
            "daily_structure": str(daily[i]),
            "four_hour_structure": str(four_hour[i]),
            "stop_reference_price": stop_reference,
            "stop_distance_atr": abs(close - stop_reference) / atr,
            "signal_atr14": atr,
            "signal_open": float(data["open"][i]),
            "signal_high": float(data["high"][i]),
            "signal_low": float(data["low"][i]),
            "signal_close": close,
        })

    return sorted(
        candidates,
        key=lambda c: (
            c["signal_available_at"],
            c["asset"],
            -c["signal_priority"],
            c["signal_type"],
        ),
    )


def build_candidates_by_asset(datasets):
    """Build candidates from {asset: dataframe}, preserving asset identity."""
    if not isinstance(datasets, dict) or not datasets:
        raise ValueError("datasets must be a non-empty asset dictionary")

    result = []
    for asset in sorted(datasets):
        result.extend(build_candidates(datasets[asset], asset=asset))

    return sorted(
        result,
        key=lambda c: (
            c["signal_available_at"],
            -c["signal_priority"],
            c["stop_distance_atr"],
            c["asset"],
        ),
    )
