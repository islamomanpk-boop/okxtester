#!/usr/bin/env python3
"""Candle-level sideways boundary interaction and penetration taxonomy V1.

Implements the frozen 2026-11-24 specification and its data-source/tail amendment.
Descriptive research only; this module does not construct episodes or test strategies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
OHLCV = ["open", "high", "low", "close", "vol"]
REQUIRED = ["ts", *OHLCV]
FEATURE_REQUIRED = [
    "available_at_ts_ms", "channel_end_candle_ts_ms", "upper", "lower",
    "channel_width_pct", "directional_efficiency", "mean_overlap",
    "width_p25_pct", "width_p40_pct",
]
FIFTEEN_MIN_MS = 900_000
FOUR_HOURS_MS = 14_400_000
BANDS = (0.05, 0.10, 0.15)
DEFINITIONS = ("STRICT_P25", "BROAD_P40")
EXPECTED_15M_ROWS = 37_941
EXPECTED_FEATURE_ROWS = 2_358
EXPECTED_15M_SHA256 = {
    "BTC": "0721a4a25a61f1917be4f9952514096c641fbec64e7ae0d50c7cf1c3ebfe9658",
    "ETH": "7195e45315c360e9f1fdd37746125968359bce8632a0bfe51628f104792fdc04",
    "SOL": "5b34cbb006497ecd7ebe0cfa67b25b4230cb769d6362d2789911711a8f6da2d33",
    "DOGE": "3418c81fa16b531eee5de90d8b0ff6a5543db54357cb5572358ff31ab6627b5f",
    "AVAX": "75ef1a545686217a6d4ca55385690095c6e2a494438b7f4e38352d5ca35de493",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_15m(path: Path, asset: str, verify_hashes: bool = True) -> tuple[pd.DataFrame, str]:
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: missing 15M source file: {path}")
    actual_hash = sha256_file(path)
    if verify_hashes and actual_hash != EXPECTED_15M_SHA256[asset]:
        raise ValueError(
            f"{asset}: 15M SHA-256 mismatch; expected "
            f"{EXPECTED_15M_SHA256[asset]}, got {actual_hash}"
        )
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"{asset}: missing 15M columns {missing}")
    df = df[REQUIRED].copy()
    ts = pd.to_numeric(df["ts"], errors="coerce")
    if ts.isna().any() or (ts % 1 != 0).any():
        raise ValueError(f"{asset}: invalid 15M timestamps")
    df["ts"] = ts.astype("int64")
    for col in OHLCV:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    values = df[OHLCV].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError(f"{asset}: non-finite 15M OHLCV")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{asset}: non-positive 15M price")
    if (df["vol"] < 0).any():
        raise ValueError(f"{asset}: negative volume")
    invalid = (
        (df["high"] < df[["open", "close", "low"]].max(axis=1))
        | (df["low"] > df[["open", "close", "high"]].min(axis=1))
    )
    if invalid.any():
        raise ValueError(f"{asset}: {int(invalid.sum())} invalid OHLC rows")
    if (df["ts"] % FIFTEEN_MIN_MS != 0).any():
        raise ValueError(f"{asset}: timestamps are not epoch-grid aligned")
    if df["ts"].duplicated().any():
        raise ValueError(f"{asset}: duplicate 15M timestamps")
    if not df["ts"].is_monotonic_increasing:
        raise ValueError(f"{asset}: 15M timestamps are not ordered")
    if len(df) != EXPECTED_15M_ROWS:
        raise ValueError(f"{asset}: expected {EXPECTED_15M_ROWS} rows, got {len(df)}")
    deltas = df["ts"].diff().dropna()
    if not (deltas == FIFTEEN_MIN_MS).all():
        bad = int((deltas != FIFTEEN_MIN_MS).sum())
        raise ValueError(f"{asset}: {bad} unexplained global 15M cadence gaps")
    return df.reset_index(drop=True), actual_hash


def load_features(path: Path, asset: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"{asset}: missing feature file: {path}")
    df = pd.read_csv(path)
    missing = [c for c in FEATURE_REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"{asset}: feature file missing columns {missing}")
    for col in FEATURE_REQUIRED:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if not np.isfinite(df[FEATURE_REQUIRED].to_numpy(dtype=float)).all():
        raise ValueError(f"{asset}: non-finite required feature values")
    for col in ("available_at_ts_ms", "channel_end_candle_ts_ms"):
        if (df[col] % 1 != 0).any():
            raise ValueError(f"{asset}: non-integer feature timestamp {col}")
        df[col] = df[col].astype("int64")
    if df["available_at_ts_ms"].duplicated().any():
        raise ValueError(f"{asset}: duplicate snapshot availability")
    if not df["available_at_ts_ms"].is_monotonic_increasing:
        raise ValueError(f"{asset}: feature snapshots are not ordered")
    if not (
        df["available_at_ts_ms"] - df["channel_end_candle_ts_ms"] == FOUR_HOURS_MS
    ).all():
        raise ValueError(f"{asset}: snapshot availability/channel-end mismatch")
    if not (df["available_at_ts_ms"].diff().dropna() == FOUR_HOURS_MS).all():
        raise ValueError(f"{asset}: feature snapshots are not exactly 4H spaced")
    if (df["upper"] <= df["lower"]).any():
        raise ValueError(f"{asset}: invalid frozen channel bounds")
    if len(df) != EXPECTED_FEATURE_ROWS:
        raise ValueError(f"{asset}: expected {EXPECTED_FEATURE_ROWS} feature snapshots, got {len(df)}")
    return df.reset_index(drop=True)


def context_passes(row: pd.Series, definition: str) -> bool:
    limit = row["width_p25_pct"] if definition == "STRICT_P25" else row["width_p40_pct"]
    return bool(
        row["channel_width_pct"] <= limit
        and row["directional_efficiency"] <= 0.30
        and row["mean_overlap"] >= 0.70
    )


def classify_side(
    side: str, open_price: float, high: float, low: float, close: float,
    upper: float, lower: float, band: float,
) -> dict[str, Any]:
    """Return signed distances, exact interaction flags and one exclusive class."""
    if side not in ("UPPER", "LOWER"):
        raise ValueError(f"unknown side: {side}")
    width = upper - lower
    if not np.isfinite(width) or width <= 0:
        raise ValueError("channel width must be positive")

    if side == "UPPER":
        d_open = (upper - open_price) / width
        d_extreme = (upper - high) / width
        d_close = (upper - close) / width
        opened_outside = open_price > upper
        closed_outside = close > upper
        return_inside = high > upper and close <= upper
        exact_contact = high == upper
        strict_penetration = high > upper
        penetration = max(0.0, (high - upper) / width)
        close_outside = closed_outside
        reentry = opened_outside and close <= upper
        wick = open_price <= upper and high > upper and close <= upper
    else:
        d_open = (open_price - lower) / width
        d_extreme = (low - lower) / width
        d_close = (close - lower) / width
        opened_outside = open_price < lower
        closed_outside = close < lower
        return_inside = low < lower and close >= lower
        exact_contact = low == lower
        strict_penetration = low < lower
        penetration = max(0.0, (lower - low) / width)
        close_outside = closed_outside
        reentry = opened_outside and close >= lower
        wick = open_price >= lower and low < lower and close >= lower

    approach = 0.0 < d_extreme <= band
    if close_outside:
        interaction = "CLOSE_OUTSIDE"
    elif reentry:
        interaction = "REENTRY_INSIDE"
    elif wick:
        interaction = "WICK_PENETRATION"
    elif exact_contact:
        interaction = "BOUNDARY_TOUCH"
    elif approach:
        interaction = "APPROACH_ONLY"
    else:
        interaction = "NO_APPROACH"

    return {
        "signed_open_distance_w": d_open,
        "signed_extreme_distance_w": d_extreme,
        "signed_close_distance_w": d_close,
        "penetration_depth_w": penetration,
        "opened_outside": bool(opened_outside),
        "closed_outside": bool(closed_outside),
        "returned_inside_after_outside": bool(return_inside),
        "exact_boundary_contact": bool(exact_contact),
        "strict_penetration": bool(strict_penetration),
        "approach": bool(approach),
        "interaction_class": interaction,
    }


def strong_rejection_reference(
    side: str, high: float, low: float, close: float, upper: float, lower: float
) -> bool:
    """Unchanged 10%-outer-zone strong-rejection definition from accepted reconstruction."""
    width = upper - lower
    if side == "UPPER":
        touched = high >= upper - 0.10 * width
        return bool(touched and close < upper - 0.10 * width and close > lower)
    touched = low <= lower + 0.10 * width
    return bool(touched and close > lower + 0.10 * width and close < upper)


def classify_candle(row: Any, upper: float, lower: float) -> tuple[dict, dict, bool]:
    upper_results = {
        band: classify_side("UPPER", row.open, row.high, row.low, row.close, upper, lower, band)
        for band in BANDS
    }
    lower_results = {
        band: classify_side("LOWER", row.open, row.high, row.low, row.close, upper, lower, band)
        for band in BANDS
    }
    # Dual interaction is defined against the widest predeclared (15%) approach band.
    dual = (
        upper_results[0.15]["interaction_class"] != "NO_APPROACH"
        and lower_results[0.15]["interaction_class"] != "NO_APPROACH"
    )
    return upper_results, lower_results, bool(dual)


def penetration_distribution(group: pd.DataFrame) -> dict[str, Any]:
    """Summarize strictly positive penetration depths, keeping zeros explicit."""
    depths = group["penetration_depth_w"].astype(float)
    positive = depths[depths > 0]
    return {
        "observations": int(len(depths)),
        "zero_penetration_observations": int((depths == 0).sum()),
        "penetration_observations": int(len(positive)),
        "penetration_rate": float(len(positive) / len(depths)) if len(depths) else np.nan,
        "mean_positive_depth_w": float(positive.mean()) if len(positive) else np.nan,
        "median_positive_depth_w": float(positive.median()) if len(positive) else np.nan,
        "p90_positive_depth_w": float(positive.quantile(0.90)) if len(positive) else np.nan,
        "p95_positive_depth_w": float(positive.quantile(0.95)) if len(positive) else np.nan,
        "maximum_positive_depth_w": float(positive.max()) if len(positive) else np.nan,
    }


def compare_class_tables(counts: pd.DataFrame, key_left: str, key_right: str,
                         left_name: str, right_name: str, keys: list[str],
                         selector: str) -> pd.DataFrame:
    """Align class counts/proportions for descriptive cohort comparisons."""
    left = counts[counts[selector] == key_left][keys + ["count", "denominator", "proportion"]]
    right = counts[counts[selector] == key_right][keys + ["count", "denominator", "proportion"]]
    left = left.rename(columns={
        "count": f"{left_name}_count", "denominator": f"{left_name}_denominator",
        "proportion": f"{left_name}_proportion",
    })
    right = right.rename(columns={
        "count": f"{right_name}_count", "denominator": f"{right_name}_denominator",
        "proportion": f"{right_name}_proportion",
    })
    out = left.merge(right, on=keys, how="outer", validate="one_to_one")
    out[f"{right_name}_minus_{left_name}_proportion"] = (
        out[f"{right_name}_proportion"] - out[f"{left_name}_proportion"]
    )
    return out


def run(data_dir: Path, feature_dir: Path, output_dir: Path, verify_hashes: bool = True) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to write into non-empty output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    observations: list[dict] = []
    snapshot_audits: list[dict] = []
    source_metadata: list[dict] = []

    for asset in ASSETS:
        bars, source_hash = load_15m(data_dir / f"{asset}_USDT_15m.csv", asset, verify_hashes)
        features = load_features(feature_dir / f"{asset}_features_original_v1.csv", asset)
        source_metadata.append({
            "asset": asset, "15m_rows": len(bars), "15m_sha256": source_hash,
            "first_15m_ts_ms": int(bars.ts.iloc[0]),
            "last_15m_ts_ms": int(bars.ts.iloc[-1]),
            "feature_rows": len(features),
            "last_snapshot_available_at_ts_ms": int(features.available_at_ts_ms.iloc[-1]),
        })

        for definition in DEFINITIONS:
            for i, feature in features.iterrows():
                available = int(feature.available_at_ts_ms)
                next_available = (
                    int(features.available_at_ts_ms.iloc[i + 1])
                    if i + 1 < len(features) else available + FOUR_HOURS_MS
                )
                left = int(bars.ts.searchsorted(available, side="left"))
                right = int(bars.ts.searchsorted(next_available, side="left"))
                interval = bars.iloc[left:right]
                is_final_truncated = i == len(features) - 1
                qualifies = context_passes(feature, definition)

                # All non-final intervals must contain the full 16 15M bars.
                if not is_final_truncated:
                    if len(interval) != 16:
                        raise ValueError(
                            f"{asset}/{definition}/snapshot {i}: expected 16 15M bars, "
                            f"found {len(interval)}"
                        )
                    expected_ts = available + np.arange(16, dtype=np.int64) * FIFTEEN_MIN_MS
                    if not np.array_equal(interval.ts.to_numpy(), expected_ts):
                        raise ValueError(f"{asset}/snapshot {i}: interval timestamps misassigned")
                    eligible = interval.iloc[1:].copy()  # accepted first-bar suppression
                    tail_status = "COMPLETE_4H_SNAPSHOT"
                else:
                    # The final snapshot interval is right-truncated; never include it in primary rows.
                    eligible = interval.iloc[1:].copy() if len(interval) else interval.copy()
                    tail_status = "RIGHT_TRUNCATED_FINAL_SNAPSHOT_EXCLUDED"

                eligible_after_suppression = len(eligible)
                included_primary = bool(qualifies and not is_final_truncated)
                included_bars = eligible_after_suppression if included_primary else 0
                snapshot_audits.append({
                    "asset": asset, "definition": definition, "snapshot_index": i,
                    "available_at_ts_ms": available, "next_available_at_ts_ms": next_available,
                    "qualifies_for_range_cohort": qualifies,
                    "observed_15m_bars": len(interval),
                    "first_bar_suppressed_count": int(len(interval) > 0),
                    "eligible_bars_after_first_bar_suppression": eligible_after_suppression,
                    "eligible_bars_excluded_by_nonqualifying_context": (
                        eligible_after_suppression if not qualifies else 0
                    ),
                    "eligible_bars_excluded_by_final_tail_rule": (
                        eligible_after_suppression if is_final_truncated else 0
                    ),
                    "included_primary_15m_bars": included_bars,
                    "included_primary_side_rows_expected": included_bars * 2,
                    "included_in_primary": included_primary,
                    "tail_status": tail_status,
                })

                if not qualifies or is_final_truncated:
                    continue

                upper, lower = float(feature.upper), float(feature.lower)
                width = upper - lower
                if not np.isfinite(width) or width <= 0:
                    raise ValueError(f"{asset}/snapshot {i}: non-positive channel width")

                for bar in eligible.itertuples(index=False):
                    upper_result, lower_result, dual = classify_candle(bar, upper, lower)
                    for side, result_set in (("UPPER", upper_result), ("LOWER", lower_result)):
                        if side == "UPPER":
                            extreme_price = float(bar.high)
                            side_result = result_set[0.10]
                        else:
                            extreme_price = float(bar.low)
                            side_result = result_set[0.10]
                        base = {
                            "asset": asset, "definition": definition,
                            "snapshot_index": int(i),
                            "snapshot_available_at_ts_ms": available,
                            "snapshot_next_available_at_ts_ms": next_available,
                            "observation_ts_ms": int(bar.ts),
                            "open": float(bar.open), "high": float(bar.high),
                            "low": float(bar.low), "close": float(bar.close),
                            "upper": upper, "lower": lower, "channel_width": width,
                            "side": side, "relevant_extreme_price": extreme_price,
                            "dual_boundary_interaction_15pct": dual,
                            "strong_rejection_reference": strong_rejection_reference(
                                side, float(bar.high), float(bar.low), float(bar.close), upper, lower
                            ),
                        }
                        # Keep primary-band geometry once, plus explicit class/approach for each band.
                        base.update({
                            "signed_open_distance_w": side_result["signed_open_distance_w"],
                            "signed_extreme_distance_w": side_result["signed_extreme_distance_w"],
                            "signed_close_distance_w": side_result["signed_close_distance_w"],
                            "penetration_depth_w": side_result["penetration_depth_w"],
                            "opened_outside": side_result["opened_outside"],
                            "closed_outside": side_result["closed_outside"],
                            "returned_inside_after_outside": side_result["returned_inside_after_outside"],
                            "exact_boundary_contact": side_result["exact_boundary_contact"],
                            "strict_penetration": side_result["strict_penetration"],
                        })
                        for band in BANDS:
                            suffix = int(round(band * 100))
                            result = result_set[band]
                            base[f"approach_{suffix}"] = result["approach"]
                            base[f"interaction_class_{suffix}"] = result["interaction_class"]
                        observations.append(base)

    obs = pd.DataFrame(observations)
    if obs.empty:
        raise ValueError("No eligible observations produced; refusing empty research output")

    # Reconcile each asset/definition/side/band: exactly one class per observation.
    count_rows = []
    for (asset, definition, side), group in obs.groupby(["asset", "definition", "side"]):
        denominator = len(group)
        for band in (5, 10, 15):
            class_col = f"interaction_class_{band}"
            counts = group[class_col].value_counts()
            if int(counts.sum()) != denominator:
                raise ValueError(f"class count reconciliation failed: {asset}/{definition}/{side}/{band}")
            for label in (
                "CLOSE_OUTSIDE", "REENTRY_INSIDE", "WICK_PENETRATION",
                "BOUNDARY_TOUCH", "APPROACH_ONLY", "NO_APPROACH",
            ):
                n = int(counts.get(label, 0))
                count_rows.append({
                    "asset": asset, "definition": definition, "side": side,
                    "approach_band_pct": band, "interaction_class": label,
                    "count": n, "denominator": denominator,
                    "proportion": n / denominator,
                })

    class_counts = pd.DataFrame(count_rows)
    upper_lower = compare_class_tables(
        class_counts, "UPPER", "LOWER", "upper", "lower",
        ["asset", "definition", "approach_band_pct", "interaction_class"], "side",
    )
    strict_broad = compare_class_tables(
        class_counts, "STRICT_P25", "BROAD_P40", "strict", "broad",
        ["asset", "side", "approach_band_pct", "interaction_class"], "definition",
    )

    penetration_rows = []
    for (asset, definition, side), group in obs.groupby(["asset", "definition", "side"]):
        penetration_rows.append({
            "asset": asset, "definition": definition, "side": side,
            **penetration_distribution(group),
        })
    penetration = pd.DataFrame(penetration_rows)
    # Count each underlying candle once, not once per upper/lower side row.
    dual_candles = obs.drop_duplicates(
        subset=["asset", "definition", "snapshot_index", "observation_ts_ms"]
    )
    dual = (
        dual_candles.groupby(["asset", "definition"])["dual_boundary_interaction_15pct"]
        .agg(observed_candles="count", dual_boundary_candles="sum")
        .reset_index()
    )
    dual["dual_boundary_candle_proportion"] = (
        dual["dual_boundary_candles"] / dual["observed_candles"]
    )
    audit = (
        obs.groupby(["asset", "definition", "side"])
        .agg(primary_observations=("observation_ts_ms", "count"),
             strong_rejection_reference_count=("strong_rejection_reference", "sum"),
             exact_contact_count=("exact_boundary_contact", "sum"),
             strict_penetration_count=("strict_penetration", "sum"))
        .reset_index()
    )

    strong_rejection = (
        obs.groupby(["asset", "definition", "side", "interaction_class_10",
                    "strong_rejection_reference"])
        .size().rename("count").reset_index()
    )
    strong_denoms = (
        obs.groupby(["asset", "definition", "side"])
        .size().rename("denominator").reset_index()
    )
    strong_rejection = strong_rejection.merge(
        strong_denoms, on=["asset", "definition", "side"], validate="many_to_one"
    )
    strong_rejection["proportion_of_side_observations"] = (
        strong_rejection["count"] / strong_rejection["denominator"]
    )

    chronological = obs[[
        "asset", "definition", "side", "observation_ts_ms",
        "interaction_class_5", "interaction_class_10", "interaction_class_15",
    ]].copy()
    utc_dates = pd.to_datetime(chronological["observation_ts_ms"], unit="ms", utc=True)
    chronological["utc_quarter"] = (
        utc_dates.dt.year.astype(str) + "-Q" +
        (((utc_dates.dt.month - 1) // 3) + 1).astype(str)
    )
    chronological_rows = []
    for band in (5, 10, 15):
        part = chronological[[
            "asset", "definition", "side", "utc_quarter", f"interaction_class_{band}"
        ]].rename(columns={f"interaction_class_{band}": "interaction_class"})
        grouped = (
            part.groupby(["asset", "definition", "side", "utc_quarter", "interaction_class"])
            .size().rename("count").reset_index()
        )
        denominators = (
            part.groupby(["asset", "definition", "side", "utc_quarter"])
            .size().rename("denominator").reset_index()
        )
        grouped = grouped.merge(
            denominators,
            on=["asset", "definition", "side", "utc_quarter"],
            validate="many_to_one",
        )
        grouped["approach_band_pct"] = band
        grouped["proportion"] = grouped["count"] / grouped["denominator"]
        chronological_rows.append(grouped)
    chronological_summary = pd.concat(chronological_rows, ignore_index=True)

    snapshot_audit_df = pd.DataFrame(snapshot_audits)
    expected_side_rows = int(snapshot_audit_df["included_primary_side_rows_expected"].sum())
    if len(obs) != expected_side_rows:
        raise ValueError(
            f"observation reconciliation failed: produced {len(obs)} side rows, "
            f"snapshot audit expects {expected_side_rows}"
        )
    if not (snapshot_audit_df["included_in_primary"] ==
            (snapshot_audit_df["included_primary_15m_bars"] > 0)).all():
        raise ValueError("snapshot inclusion audit does not reconcile")

    obs.to_csv(output_dir / "candle_level_interactions_v1.csv", index=False)
    class_counts.to_csv(output_dir / "class_counts_proportions_v1.csv", index=False)
    penetration.to_csv(output_dir / "penetration_depth_summary_v1.csv", index=False)
    dual.to_csv(output_dir / "dual_boundary_summary_v1.csv", index=False)
    audit.to_csv(output_dir / "observation_audit_v1.csv", index=False)
    snapshot_audit_df.to_csv(output_dir / "snapshot_tail_audit_v1.csv", index=False)
    upper_lower.to_csv(output_dir / "upper_lower_class_comparison_v1.csv", index=False)
    strict_broad.to_csv(output_dir / "strict_broad_class_comparison_v1.csv", index=False)
    strong_rejection.to_csv(output_dir / "strong_rejection_reference_comparison_v1.csv", index=False)
    chronological_summary.to_csv(output_dir / "chronological_subperiod_summary_v1.csv", index=False)

    metadata = {
        "study": "Sideways Boundary Interaction and Penetration Taxonomy V1",
        "status": "DESCRIPTIVE_CANDLE_LEVEL_RESEARCH",
        "assets": ASSETS, "definitions": DEFINITIONS,
        "bands": list(BANDS), "primary_band": 0.10,
        "source_files": source_metadata,
        "observation_rows": int(len(obs)),
        "expected_observation_rows_from_snapshot_audit": expected_side_rows,
        "snapshot_audit_rows": int(len(snapshot_audits)),
        "chronological_period": "UTC calendar quarters",
        "penetration_summary_policy": "distribution statistics use strictly positive penetration depths only; zero counts reported separately",
        "comparison_policy": "upper/lower and strict/broad comparisons are descriptive; strict and broad cohorts overlap",
        "final_truncated_snapshot_excluded": True,
        "final_snapshot_tail_policy": "exclude entire final 4H interval from primary summaries",
        "timestamp_policy": "strict continuous 15M cadence; no gaps bridged",
        "first_bar_policy": "suppress first observed 15M candle at/after each snapshot availability",
        "dual_boundary_definition": "both sides have non-NO_APPROACH class under widest 15% band; counted once per candle",
        "snapshot_exclusion_note": "nonqualifying-context and final-tail exclusion counts are reason flags and can overlap",
        "volume_policy": "volume retained only in source validation; no volume-based inference",
        "limitations": [
            "Consecutive candle rows are not independent episodes.",
            "No predictive, causal, strategy, execution, or profitability inference.",
            "STRICT_P25 and BROAD_P40 cohorts overlap and must not be pooled as independent.",
            "Exact boundary contact uses exact parsed-price equality; no epsilon.",
        ],
    }
    (output_dir / "run_metadata_v1.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("===== SIDEWAYS BOUNDARY INTERACTION TAXONOMY V1 =====")
    print(f"Candle-side observation rows: {len(obs):,}")
    print(f"Assets: {', '.join(ASSETS)}")
    print(f"Reports saved: {output_dir}")
    print("Final truncated 4H snapshot excluded from primary observations.")
    print("Descriptive only; no episode independence or profitability claim.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path.home() / "okx_adaptive_bot" / "data")
    parser.add_argument("--feature-dir", type=Path, default=Path.home() / "okxtester" / "reports" / "sideways_detector_original_v1")
    parser.add_argument("--output-dir", type=Path, default=Path.home() / "okxtester" / "reports" / "sideways_boundary_interaction_taxonomy_v1")
    parser.add_argument("--skip-source-hash-check", action="store_true",
                        help="For controlled tests only; never use for the accepted production run.")
    args = parser.parse_args()
    run(args.data_dir, args.feature_dir, args.output_dir,
        verify_hashes=not args.skip_source_hash_check)


if __name__ == "__main__":
    main()
