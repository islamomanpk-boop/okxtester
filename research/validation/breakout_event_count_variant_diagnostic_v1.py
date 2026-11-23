#!/usr/bin/env python3
"""Read-only diagnostic for the accepted breakout event-count reproduction.

Compares:
  1) width quantiles from unique completed 4H feature rows vs joined 15M rows
  2) accepted mask (no previous-selected filter) vs archived-script mask
Prints raw and 15-minute-follow-up-eligible counts against the accepted 20-count reference.
Does not write files, modify source data, or calculate outcomes.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
BASE = Path.home() / "okx_scalping_data"
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

def make_bars(df, rule, expected):
    bars = df.resample(
        rule, origin="epoch", label="left", closed="left"
    ).agg({"open": "first", "high": "max", "low": "min", "close": "last"})
    counts = df["close"].resample(
        rule, origin="epoch", label="left", closed="left"
    ).count()
    return bars.loc[counts.eq(expected)].copy()

def features_for(h4):
    upper = h4["high"].rolling(12).max()
    lower = h4["low"].rolling(12).min()
    width = (upper / lower - 1.0) * 100.0

    net_move = (h4["close"] / h4["close"].shift(11) - 1.0).abs()
    path_move = h4["close"].pct_change().abs().rolling(11).sum()
    efficiency = net_move / path_move.replace(0, np.nan)

    prev_high = h4["high"].shift(1)
    prev_low = h4["low"].shift(1)
    intersection = (
        np.minimum(h4["high"], prev_high)
        - np.maximum(h4["low"], prev_low)
    ).clip(lower=0)
    smaller_range = np.minimum(
        h4["high"] - h4["low"], prev_high - prev_low
    )
    overlap_pair = intersection / smaller_range.replace(0, np.nan)
    overlap = overlap_pair.rolling(11).mean()

    f = pd.DataFrame({
        "upper": upper, "lower": lower, "width": width,
        "efficiency": efficiency, "overlap": overlap,
    }).dropna()
    f["snapshot_time"] = f.index + pd.Timedelta(hours=4)
    return f

def main():
    raw = {}
    for asset in ASSETS:
        path = BASE / f"{asset}_USDT_USDT_1m.csv"
        if not path.exists():
            raise FileNotFoundError(f"Missing required source file: {path}")
        d = pd.read_csv(path, usecols=["ts", "open", "high", "low", "close"])
        d["ts"] = pd.to_datetime(d["ts"], unit="ms", utc=True)
        d = d.set_index("ts").sort_index()
        if d.index.has_duplicates:
            raise ValueError(f"{asset}: duplicate 1M timestamps")
        raw[asset] = d

    common = raw[ASSETS[0]].index
    for asset in ASSETS[1:]:
        common = common.intersection(raw[asset].index)
    common = common.sort_values()
    if len(common) != 569125:
        raise ValueError(
            f"Common timestamp count changed: {len(common)}; expected 569125. Stop."
        )
    common_deltas = common.to_series().diff().dropna()
    if not common_deltas.eq(pd.Timedelta(minutes=1)).all():
        bad = common_deltas[~common_deltas.eq(pd.Timedelta(minutes=1))]
        raise ValueError(
            "Common 1M index is not exactly continuous. First irregular intervals:\n"
            + bad.head(10).to_string()
        )

    print("READ-ONLY BREAKOUT REPRODUCTION DIAGNOSTIC")
    print("Common 1M timestamps:", len(common))
    print("No source files will be changed.")
    rows = []

    for asset in ASSETS:
        one = raw[asset].loc[common]
        h4 = make_bars(one, "4h", 240)
        m15 = make_bars(one, "15min", 15)
        f = features_for(h4)

        m15x = m15.copy()
        m15x.index.name = "bar_start"
        aligned = pd.merge_asof(
            m15x.reset_index().sort_values("bar_start"),
            f.reset_index(drop=True).sort_values("snapshot_time"),
            left_on="bar_start", right_on="snapshot_time",
            direction="backward",
        ).set_index("bar_start")

        # The two quantile populations under audit.
        thresholds = {
            "UNIQUE_4H": {
                "P25": float(f["width"].quantile(.25)),
                "P40": float(f["width"].quantile(.40)),
            },
            "JOINED_15M": {
                "P25": float(aligned["width"].quantile(.25)),
                "P40": float(aligned["width"].quantile(.40)),
            },
        }

        same_snapshot = aligned["snapshot_time"].eq(
            aligned["snapshot_time"].shift(1)
        )
        previous_close = aligned["close"].shift(1)
        previous_selected_cache = {}

        for population, qs in thresholds.items():
            for definition, threshold in qs.items():
                selected = (
                    aligned["width"].le(threshold)
                    & aligned["efficiency"].le(.30)
                    & aligned["overlap"].ge(.70)
                )
                previous_selected = selected.shift(1).fillna(False).astype(bool)

                for mask_version, require_previous_selected in [
                    ("ACCEPTED_MASK_NO_PREVIOUS_SIDEWAYS", False),
                    ("ARCHIVED_MASK_WITH_PREVIOUS_SIDEWAYS", True),
                ]:
                    valid = selected & same_snapshot
                    if require_previous_selected:
                        valid = valid & previous_selected

                    masks = {
                        "UPPER": valid & previous_close.le(aligned["upper"])
                                 & aligned["close"].gt(aligned["upper"]),
                        "LOWER": valid & previous_close.ge(aligned["lower"])
                                 & aligned["close"].lt(aligned["lower"]),
                    }

                    for direction, mask in masks.items():
                        raw_count = int(mask.sum())
                        eligible_count = 0
                        for event_time in aligned.index[mask.fillna(False)]:
                            confirmation = event_time + pd.Timedelta(minutes=15)
                            pos = common.get_indexer([confirmation])[0]
                            if pos < 0 or pos + 15 > len(common):
                                continue
                            expected_minutes = pd.date_range(
                                confirmation, periods=15, freq="1min"
                            )
                            if common[pos:pos + 15].equals(expected_minutes):
                                eligible_count += 1

                        key = (asset, definition, direction)
                        expected = EXPECTED[key]
                        rows.append({
                            "asset": asset, "quantile_population": population,
                            "mask": mask_version, "definition": definition,
                            "direction": direction, "threshold_pct": threshold,
                            "threshold_n": int(
                                f["width"].notna().sum()
                                if population == "UNIQUE_4H"
                                else aligned["width"].notna().sum()
                            ),
                            "raw_count": raw_count,
                            "eligible_15m_count": eligible_count,
                            "accepted_reference": expected,
                            "raw_match": raw_count == expected,
                            "eligible_match": eligible_count == expected,
                        })

    out = pd.DataFrame(rows)
    for population in ["UNIQUE_4H", "JOINED_15M"]:
        for mask_version in [
            "ACCEPTED_MASK_NO_PREVIOUS_SIDEWAYS",
            "ARCHIVED_MASK_WITH_PREVIOUS_SIDEWAYS",
        ]:
            part = out[
                out["quantile_population"].eq(population)
                & out["mask"].eq(mask_version)
            ]
            raw_pass = int(part["raw_match"].sum())
            eligible_pass = int(part["eligible_match"].sum())
            print("\n" + "=" * 78)
            print(population, "|", mask_version)
            print(f"Exact matches: raw {raw_pass}/20 | eligible {eligible_pass}/20")
            print(part[[
                "asset", "definition", "direction", "threshold_pct",
                "raw_count", "eligible_15m_count", "accepted_reference",
                "raw_match", "eligible_match",
            ]].to_string(index=False, float_format=lambda x: f"{x:.6f}"))

    print("\nDiagnostic complete. No matching, outcomes, or profitability calculations.")
    print("Do not select a variant merely because it matches; review the full table and methodology.")

if __name__ == "__main__":
    main()
