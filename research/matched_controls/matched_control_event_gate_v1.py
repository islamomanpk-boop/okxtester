#!/usr/bin/env python3
"""Read-only event-count gate for the corrected matched-control rebuild.

This is the mandatory first stage. It reconstructs the accepted 15M breakout
masks using the joined-15M width-quantile population and stops unless all 20
asset × definition × direction counts match the accepted reference exactly.

No matching, outcomes, strategy simulation, or file writes occur here.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
DATA_DIR = Path.home() / "okx_scalping_data"
EXPECTED_COMMON_MINUTES = 569_125
MINUTE = pd.Timedelta(minutes=1)

EXPECTED = {
    ("BTC", "P25", "LOWER"): 62, ("BTC", "P25", "UPPER"): 81,
    ("BTC", "P40", "LOWER"): 91, ("BTC", "P40", "UPPER"): 115,
    ("ETH", "P25", "LOWER"): 51, ("ETH", "P25", "UPPER"): 51,
    ("ETH", "P40", "LOWER"): 87, ("ETH", "P40", "UPPER"): 77,
    ("SOL", "P25", "LOWER"): 77, ("SOL", "P25", "UPPER"): 71,
    ("SOL", "P40", "LOWER"): 117, ("SOL", "P40", "UPPER"): 96,
    ("DOGE", "P25", "LOWER"): 55, ("DOGE", "P25", "UPPER"): 65,
    ("DOGE", "P40", "LOWER"): 81, ("DOGE", "P40", "UPPER"): 75,
    ("AVAX", "P25", "LOWER"): 64, ("AVAX", "P25", "UPPER"): 83,
    ("AVAX", "P40", "LOWER"): 84, ("AVAX", "P40", "UPPER"): 109,
}


def load_one_minute(asset: str) -> pd.DataFrame:
    path = DATA_DIR / f"{asset}_USDT_USDT_1m.csv"
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: required source file not found: {path}")

    frame = pd.read_csv(path, usecols=["ts", "open", "high", "low", "close"])
    ts = pd.to_numeric(frame["ts"], errors="coerce")
    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{asset}: invalid/non-integer millisecond timestamps")
    frame["ts"] = pd.to_datetime(ts.astype("int64"), unit="ms", utc=True)
    frame = frame.set_index("ts").sort_index()

    if frame.index.has_duplicates:
        raise ValueError(f"{asset}: duplicate 1M timestamps")
    for col in ["open", "high", "low", "close"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    values = frame[["open", "high", "low", "close"]].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values <= 0).any():
        raise ValueError(f"{asset}: non-finite or non-positive OHLC values")
    invalid = (
        (frame["high"] < frame[["open", "close", "low"]].max(axis=1))
        | (frame["low"] > frame[["open", "close", "high"]].min(axis=1))
    )
    if invalid.any():
        raise ValueError(f"{asset}: {int(invalid.sum())} invalid OHLC rows")
    return frame


def make_complete_bars(
    one: pd.DataFrame, rule: str, expected_minutes: int
) -> pd.DataFrame:
    bars = one.resample(
        rule, origin="epoch", label="left", closed="left"
    ).agg({
        "open": "first", "high": "max", "low": "min", "close": "last"
    })
    counts = one["close"].resample(
        rule, origin="epoch", label="left", closed="left"
    ).count()
    return bars.loc[counts.eq(expected_minutes)].copy()


def build_features(h4: pd.DataFrame) -> pd.DataFrame:
    upper = h4["high"].rolling(12, min_periods=12).max()
    lower = h4["low"].rolling(12, min_periods=12).min()
    width = (upper / lower - 1.0) * 100.0

    net_move = (h4["close"] / h4["close"].shift(11) - 1.0).abs()
    path_move = h4["close"].pct_change().abs().rolling(11, min_periods=11).sum()
    efficiency = net_move / path_move.replace(0.0, np.nan)

    previous_high = h4["high"].shift(1)
    previous_low = h4["low"].shift(1)
    intersection = (
        np.minimum(h4["high"], previous_high)
        - np.maximum(h4["low"], previous_low)
    ).clip(lower=0.0)
    smaller_range = np.minimum(
        h4["high"] - h4["low"], previous_high - previous_low
    )
    overlap_pair = intersection / smaller_range.replace(0.0, np.nan)
    overlap = overlap_pair.rolling(11, min_periods=11).mean()

    features = pd.DataFrame({
        "upper": upper,
        "lower": lower,
        "width": width,
        "efficiency": efficiency,
        "overlap": overlap,
    }).dropna()
    features["snapshot_time"] = features.index + pd.Timedelta(hours=4)
    return features


def exact_common_index(raw: dict[str, pd.DataFrame]) -> pd.DatetimeIndex:
    common = raw[ASSETS[0]].index
    for asset in ASSETS[1:]:
        common = common.intersection(raw[asset].index)
    common = common.sort_values()

    if len(common) != EXPECTED_COMMON_MINUTES:
        raise ValueError(
            f"Common timestamp count is {len(common):,}; "
            f"accepted reference is {EXPECTED_COMMON_MINUTES:,}. STOP."
        )
    deltas = common.to_series().diff().dropna()
    bad = deltas.ne(MINUTE)
    if bad.any():
        raise ValueError(
            "Common 1M timestamps are not exactly continuous. "
            "First irregular intervals:\n" + deltas[bad].head(10).to_string()
        )
    return common


def reproduce_asset(
    asset: str, one: pd.DataFrame
) -> tuple[list[dict], dict[str, float]]:
    h4 = make_complete_bars(one, "4h", 240)
    m15 = make_complete_bars(one, "15min", 15)
    if len(h4) != 2_370 or len(m15) != 37_941:
        raise ValueError(
            f"{asset}: complete bar counts changed: "
            f"4H={len(h4):,}, 15M={len(m15):,}; expected 2,370 and 37,941."
        )

    features = build_features(h4)
    m15x = m15.copy()
    m15x.index.name = "bar_start"
    aligned = pd.merge_asof(
        m15x.reset_index().sort_values("bar_start"),
        features.reset_index(drop=True).sort_values("snapshot_time"),
        left_on="bar_start",
        right_on="snapshot_time",
        direction="backward",
    ).set_index("bar_start")

    # Critical: the accepted thresholds are calculated from the joined 15M
    # observation population, not from unique 4H feature rows.
    thresholds = {
        "P25": float(aligned["width"].quantile(0.25)),
        "P40": float(aligned["width"].quantile(0.40)),
    }

    same_snapshot = aligned["snapshot_time"].eq(
        aligned["snapshot_time"].shift(1)
    )
    previous_close = aligned["close"].shift(1)
    rows: list[dict] = []

    for definition, threshold in thresholds.items():
        selected = (
            aligned["width"].le(threshold)
            & aligned["efficiency"].le(0.30)
            & aligned["overlap"].ge(0.70)
        )
        # No previous_selected/previous_sideways filter and no cooldown.
        valid = selected & same_snapshot

        masks = {
            "UPPER": (
                valid
                & previous_close.le(aligned["upper"])
                & aligned["close"].gt(aligned["upper"])
            ),
            "LOWER": (
                valid
                & previous_close.ge(aligned["lower"])
                & aligned["close"].lt(aligned["lower"])
            ),
        }

        for direction, mask in masks.items():
            count = int(mask.fillna(False).sum())
            key = (asset, definition, direction)
            expected = EXPECTED[key]
            rows.append({
                "asset": asset,
                "definition": definition,
                "direction": direction,
                "threshold_pct": threshold,
                "actual": count,
                "expected": expected,
                "pass": count == expected,
            })

    return rows, thresholds


def main() -> int:
    print("=" * 78)
    print("CORRECTED MATCHED-CONTROL REBUILD — EVENT COUNT GATE")
    print("Read-only | no matching | no outcome calculations | no file writes")
    print("=" * 78)

    raw = {asset: load_one_minute(asset) for asset in ASSETS}
    common = exact_common_index(raw)
    print(f"Common synchronized 1M timestamps: {len(common):,}")
    print("Common timestamp continuity: PASS (every interval exactly 1 minute)")

    all_rows: list[dict] = []
    for asset in ASSETS:
        rows, thresholds = reproduce_asset(asset, raw[asset].loc[common])
        all_rows.extend(rows)
        print(
            f"{asset}: joined-15M P25={thresholds['P25']:.9f}% | "
            f"P40={thresholds['P40']:.9f}%"
        )

    result = pd.DataFrame(all_rows)
    passed = int(result["pass"].sum())
    print("\n" + result.to_string(
        index=False,
        formatters={"threshold_pct": lambda x: f"{x:.9f}"},
    ))
    print(f"\nEXACT EVENT-COUNT VALIDATION: {passed}/20")

    if passed != 20:
        print("VALIDATION FAILED — STOP. No matched controls may be constructed.")
        return 2

    print("VALIDATION PASSED — all 20 accepted event counts reproduced exactly.")
    print("This gate alone does not validate matching or forward outcomes.")
    print("Next stage: corrected control eligibility, matching, balance and outcomes.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FATAL VALIDATION ERROR — STOP: {exc}", file=sys.stderr)
        raise
