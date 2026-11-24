#!/usr/bin/env python3
"""Descriptive forward outcomes for historically detected breakouts V1."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

from research.breakout_test_count.breakout_test_count_study_v1 import (
    ASSETS,
    EXPECTED_COUNTS,
    EXPECTED_QUANTILES,
    SOURCE_REL,
    SOURCE_BLOB_SHA,
    ZONE_FRACS,
    EFFICIENCY_MAX,
    OVERLAP_MIN,
    build_joined,
    original_events,
)

HORIZONS = {"15M": 15, "1H": 60, "4H": 240, "12H": 720}
DIRECTIONS = ("UPPER", "LOWER")
DEFINITIONS = ("BROAD_P40", "STRICT_P25")
GROUPS = (
    "DIRECT", "CONTACT_ONLY", "ONE_REJECTION",
    "TWO_REJECTIONS", "THREE_PLUS_REJECTIONS",
)
OHLCV = ["open", "high", "low", "close", "vol"]
EVENT_KEYS = ["asset", "definition", "direction", "signal_time"]
CLASS_KEYS = EVENT_KEYS + ["zone_pct_of_channel"]
EXPECTED_CLASSIFICATION_ROWS = 4776
FIFTEEN_MIN = pd.Timedelta(minutes=15)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git_blob_sha(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path)],
        check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def load_common_data(data_dir: Path):
    """Strictly validate raw source order, timestamps, and OHLC consistency."""
    data = {}
    hashes = {}
    source_rows = {}
    source_first = {}
    source_last = {}

    for asset in ASSETS:
        path = data_dir / f"{asset}_USDT_USDT_1m.csv"
        if not path.is_file():
            raise FileNotFoundError(path)

        raw = pd.read_csv(path)
        required = {"ts", *OHLCV}
        missing = required - set(raw.columns)
        if missing:
            raise ValueError(f"{asset}: missing columns {sorted(missing)}")

        raw = raw[["ts", *OHLCV]].copy()
        numeric_ts = pd.to_numeric(raw["ts"], errors="coerce")
        if numeric_ts.isna().any() or (numeric_ts % 1 != 0).any():
            raise ValueError(f"{asset}: invalid millisecond timestamps")

        timestamps = pd.to_datetime(
            numeric_ts.astype("int64"), unit="ms", utc=True
        )
        if timestamps.duplicated().any():
            raise ValueError(f"{asset}: duplicate timestamps")
        if not timestamps.is_monotonic_increasing:
            raise ValueError(f"{asset}: source timestamps are not ordered")

        for col in OHLCV:
            raw[col] = pd.to_numeric(raw[col], errors="coerce")
        values = raw[OHLCV].to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError(f"{asset}: non-finite OHLCV values")

        o = raw["open"].to_numpy(dtype=float)
        h = raw["high"].to_numpy(dtype=float)
        l = raw["low"].to_numpy(dtype=float)
        c = raw["close"].to_numpy(dtype=float)

        if (o <= 0).any() or (h <= 0).any() or (l <= 0).any() or (c <= 0).any():
            raise ValueError(f"{asset}: non-positive OHLC price")
        if (h < np.maximum.reduce([o, l, c])).any():
            raise ValueError(f"{asset}: high inconsistent with OHLC")
        if (l > np.minimum.reduce([o, h, c])).any():
            raise ValueError(f"{asset}: low inconsistent with OHLC")

        raw.index = pd.DatetimeIndex(timestamps, name="ts")
        data[asset] = raw[OHLCV]
        hashes[asset] = sha256_file(path)
        source_rows[asset] = len(raw)
        source_first[asset] = str(raw.index[0])
        source_last[asset] = str(raw.index[-1])

    common = data[ASSETS[0]].index
    for asset in ASSETS[1:]:
        common = common.intersection(data[asset].index)
    common = common.sort_values()

    if len(common) < 10000:
        raise RuntimeError(f"Common timeline unexpectedly small: {len(common)}")

    for asset in ASSETS:
        data[asset] = data[asset].reindex(common)

    gaps = int(
        (common.to_series().diff().dropna() != pd.Timedelta(minutes=1)).sum()
    )

    return data, common, hashes, source_rows, source_first, source_last, gaps


def parse_utc(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, utc=True, errors="raise")


def classification_group(touch_count: int, rejection_count: int) -> str:
    if touch_count < 0 or rejection_count < 0 or rejection_count > touch_count:
        raise ValueError("Invalid touch/rejection counts")
    if rejection_count == 0:
        return "DIRECT" if touch_count == 0 else "CONTACT_ONLY"
    if rejection_count == 1:
        return "ONE_REJECTION"
    if rejection_count == 2:
        return "TWO_REJECTIONS"
    return "THREE_PLUS_REJECTIONS"


def validate_classifications(classifications: pd.DataFrame,
                              links: pd.DataFrame,
                              events: list[dict]) -> pd.DataFrame:
    c = classifications.copy()
    l = links.copy()

    required = set(CLASS_KEYS + [
        "zone_pct_of_channel", "boundary", "upper", "lower",
        "channel_width_price", "prior_touch_test_count",
        "prior_confirmed_rejection_count",
        "prior_contact_only_test_count",
    ])
    missing = required - set(c.columns)
    if missing:
        raise RuntimeError(f"Classification input missing columns: {sorted(missing)}")

    c["signal_time"] = parse_utc(c["signal_time"])
    c["zone_pct_of_channel"] = pd.to_numeric(c["zone_pct_of_channel"])
    l["signal_time"] = parse_utc(l["signal_time"])
    l["test_start_time"] = parse_utc(l["test_start_time"])
    l["first_rejection_time"] = pd.to_datetime(
        l["first_rejection_time"], utc=True, errors="coerce"
    )

    if len(c) != EXPECTED_CLASSIFICATION_ROWS:
        raise RuntimeError(
            f"Expected {EXPECTED_CLASSIFICATION_ROWS} classification rows; got {len(c)}"
        )
    if c.duplicated(CLASS_KEYS).any():
        raise RuntimeError("Duplicate event-zone classification keys")

    expected_zones = {5.0, 10.0, 15.0}
    if set(c["zone_pct_of_channel"].unique()) != expected_zones:
        raise RuntimeError("Unexpected classification zone set")

    c["prior_touch_test_count"] = pd.to_numeric(
        c["prior_touch_test_count"], errors="raise"
    ).astype(int)
    c["prior_confirmed_rejection_count"] = pd.to_numeric(
        c["prior_confirmed_rejection_count"], errors="raise"
    ).astype(int)
    c["prior_contact_only_test_count"] = pd.to_numeric(
        c["prior_contact_only_test_count"], errors="raise"
    ).astype(int)

    if not (
        c["prior_touch_test_count"]
        == c["prior_confirmed_rejection_count"]
        + c["prior_contact_only_test_count"]
    ).all():
        raise RuntimeError("Classification touch/rejection counts do not reconcile")

    c["pre_breakout_group"] = [
        classification_group(t, r)
        for t, r in zip(
            c["prior_touch_test_count"],
            c["prior_confirmed_rejection_count"],
        )
    ]

    # Every reconstructed original event must map to exactly three zone rows.
    event_frame = pd.DataFrame(events)
    event_frame["signal_time"] = pd.to_datetime(
        event_frame["signal_time"], utc=True
    )
    expected = event_frame[EVENT_KEYS].drop_duplicates()
    actual = c[EVENT_KEYS].drop_duplicates()

    expected_index = pd.MultiIndex.from_frame(expected[EVENT_KEYS])
    actual_index = pd.MultiIndex.from_frame(actual[EVENT_KEYS])
    if len(expected_index.difference(actual_index)):
        raise RuntimeError("Original events missing from prior classifications")
    if len(actual_index.difference(expected_index)):
        raise RuntimeError("Unexpected classifications without original events")

    per_event_zones = c.groupby(EVENT_KEYS)["zone_pct_of_channel"].agg(list)
    if not per_event_zones.map(lambda x: sorted(x) == [5.0, 10.0, 15.0]).all():
        raise RuntimeError("An original event does not have exactly three zone rows")

    # Check link counts against each event-zone's touch-test count.
    if not l.empty:
        link_counts = (
            l.groupby(CLASS_KEYS, dropna=False)
            .size().rename("linked_test_count").reset_index()
        )
    else:
        link_counts = pd.DataFrame(columns=CLASS_KEYS + ["linked_test_count"])

    c = c.merge(link_counts, on=CLASS_KEYS, how="left", validate="one_to_one")
    c["linked_test_count"] = c["linked_test_count"].fillna(0).astype(int)
    if not (
        c["linked_test_count"] == c["prior_touch_test_count"]
    ).all():
        raise RuntimeError("Prior-test links do not reconcile with classifications")

    if not l.empty:
        if not (l["test_start_time"] < l["signal_time"]).all():
            raise RuntimeError("Prior-test link starts at/after breakout")
        bad_rejection = (
            l["first_rejection_time"].notna()
            & (l["first_rejection_time"] >= l["signal_time"])
        )
        if bad_rejection.any():
            raise RuntimeError("A linked rejection is not strictly before breakout")

    return c


def measure_horizon(
    window: pd.DataFrame,
    direction: str,
    entry_price: float,
    boundary: float,
    channel_width: float,
    entry_time: pd.Timestamp,
) -> dict:
    """Measure one complete, consecutive N-candle post-entry window."""
    if direction not in DIRECTIONS:
        raise ValueError("Unknown direction")
    if not np.isfinite(entry_price) or entry_price <= 0:
        raise ValueError("Invalid entry price")
    if not np.isfinite(boundary) or boundary <= 0:
        raise ValueError("Invalid boundary")
    if not np.isfinite(channel_width) or channel_width <= 0:
        raise ValueError("Invalid channel width")
    if window.empty:
        raise ValueError("Empty outcome window")

    highs = window["high"].to_numpy(dtype=float)
    lows = window["low"].to_numpy(dtype=float)
    closes = window["close"].to_numpy(dtype=float)

    if direction == "UPPER":
        favourable_pos = int(np.argmax(highs))
        adverse_pos = int(np.argmin(lows))
        favourable_price = float(highs[favourable_pos])
        adverse_price = float(lows[adverse_pos])
        favourable_move = max(0.0, favourable_price - entry_price)
        adverse_move = max(0.0, entry_price - adverse_price)
        immediate_adverse = bool(entry_price <= boundary)
        failures = np.flatnonzero(closes <= boundary)
        signed = (float(closes[-1]) / entry_price - 1.0) * 100.0
    else:
        favourable_pos = int(np.argmin(lows))
        adverse_pos = int(np.argmax(highs))
        favourable_price = float(lows[favourable_pos])
        adverse_price = float(highs[adverse_pos])
        favourable_move = max(0.0, entry_price - favourable_price)
        adverse_move = max(0.0, adverse_price - entry_price)
        immediate_adverse = bool(entry_price >= boundary)
        failures = np.flatnonzero(closes >= boundary)
        signed = -(float(closes[-1]) / entry_price - 1.0) * 100.0

    favourable_pct = favourable_move / entry_price * 100.0
    adverse_pct = adverse_move / entry_price * 100.0
    failure_pos = int(failures[0]) if len(failures) else None

    return {
        "directional_close_return_pct": signed,
        "mfe_pct": favourable_pct,
        "mae_pct": adverse_pct,
        "mfe_channel_width_pct": favourable_move / channel_width * 100.0,
        "mae_channel_width_pct": adverse_move / channel_width * 100.0,
        "favourable_extreme_price": favourable_price,
        "favourable_extreme_time": window.index[favourable_pos],
        "time_to_mfe_minutes": favourable_pos,
        "adverse_extreme_price": adverse_price,
        "adverse_extreme_time": window.index[adverse_pos],
        "time_to_mae_minutes": adverse_pos,
        "entry_open_already_through_boundary": immediate_adverse,
        "boundary_failure": failure_pos is not None,
        "boundary_failure_time": (
            window.index[failure_pos] if failure_pos is not None else pd.NaT
        ),
        "minutes_to_boundary_failure": failure_pos,
    }


def build_event_rows(classifications: pd.DataFrame,
                     data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []

    for _, event in classifications.iterrows():
        asset = event["asset"]
        minute = data[asset]
        signal_time = event["signal_time"]
        direction = event["direction"]

        # The signal's final 1M candle opens at signal_time - 1 minute.
        # The entry candle opens exactly at signal_time.
        expected_entry_time = signal_time
        entry_pos = minute.index.get_indexer([expected_entry_time])[0]

        entry_reason = None
        entry_price = np.nan
        entry_open = np.nan

        if entry_pos < 0:
            entry_reason = "entry_candle_missing"
        else:
            entry_row = minute.iloc[entry_pos]
            entry_open = float(entry_row["open"])
            if not np.isfinite(entry_open) or entry_open <= 0:
                entry_reason = "entry_open_invalid"
            else:
                entry_price = entry_open

        boundary = float(event["boundary"])
        channel_width = float(event["channel_width_price"])

        for horizon, n_candles in HORIZONS.items():
            base = {
                **{k: event[k] for k in CLASS_KEYS},
                "snapshot": event["snapshot"],
                "boundary": boundary,
                "upper": float(event["upper"]),
                "lower": float(event["lower"]),
                "channel_width_price": channel_width,
                "channel_width_pct": float(event["channel_width_pct"]),
                "prior_touch_test_count": int(event["prior_touch_test_count"]),
                "prior_confirmed_rejection_count": int(
                    event["prior_confirmed_rejection_count"]
                ),
                "prior_contact_only_test_count": int(
                    event["prior_contact_only_test_count"]
                ),
                "pre_breakout_group": event["pre_breakout_group"],
                "entry_time": expected_entry_time,
                "entry_open": entry_open,
                "entry_price": entry_price,
                "horizon": horizon,
                "horizon_minutes": n_candles,
                "horizon_status": None,
                "exclusion_reason": None,
            }

            if entry_reason:
                base["horizon_status"] = "ENTRY_EXCLUDED"
                base["exclusion_reason"] = entry_reason
                rows.append(base)
                continue

            if entry_pos != minute.index.get_indexer([signal_time])[0]:
                raise RuntimeError("Entry index/timestamp mismatch")
            if minute.index[entry_pos] <= signal_time - pd.Timedelta(minutes=1):
                raise RuntimeError("Entry is not strictly after signal candle")

            end_pos = entry_pos + n_candles
            if end_pos > len(minute):
                base["horizon_status"] = "INCOMPLETE"
                base["exclusion_reason"] = "insufficient_candles_at_dataset_end"
                rows.append(base)
                continue

            window = minute.iloc[entry_pos:end_pos]
            expected_length = n_candles
            if len(window) != expected_length:
                base["horizon_status"] = "INCOMPLETE"
                base["exclusion_reason"] = "wrong_horizon_candle_count"
                rows.append(base)
                continue

            expected_index = pd.date_range(
                start=expected_entry_time,
                periods=n_candles,
                freq="1min",
                tz="UTC",
            )
            if not window.index.equals(expected_index):
                base["horizon_status"] = "INCOMPLETE"
                base["exclusion_reason"] = "missing_or_nonconsecutive_minute"
                rows.append(base)
                continue

            if not np.isfinite(
                window[["open", "high", "low", "close"]].to_numpy(dtype=float)
            ).all():
                base["horizon_status"] = "INCOMPLETE"
                base["exclusion_reason"] = "invalid_ohlc_inside_horizon"
                rows.append(base)
                continue

            if (
                (window["high"] < window[["open", "low", "close"]].max(axis=1)).any()
                or (window["low"] > window[["open", "high", "close"]].min(axis=1)).any()
            ):
                base["horizon_status"] = "INCOMPLETE"
                base["exclusion_reason"] = "inconsistent_ohlc_inside_horizon"
                rows.append(base)
                continue

            measurements = measure_horizon(
                window=window,
                direction=direction,
                entry_price=entry_price,
                boundary=boundary,
                channel_width=channel_width,
                entry_time=expected_entry_time,
            )
            base["horizon_status"] = "COMPLETE"
            base.update(measurements)
            rows.append(base)

    result = pd.DataFrame(rows)
    key = CLASS_KEYS + ["horizon"]
    if result.duplicated(key).any():
        raise RuntimeError("Duplicate event-zone-horizon output rows")
    expected_rows = len(classifications) * len(HORIZONS)
    if len(result) != expected_rows:
        raise RuntimeError(
            f"Output row reconciliation failed: {len(result)} != {expected_rows}"
        )
    return result


def build_summary(outcomes: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "asset", "definition", "direction", "zone_pct_of_channel",
        "pre_breakout_group", "horizon",
    ]
    rows = []

    for group_key, frame in outcomes.groupby(keys, dropna=False, sort=True):
        complete = frame[frame["horizon_status"] == "COMPLETE"]
        eligible = frame[frame["horizon_status"] != "ENTRY_EXCLUDED"]
        row = dict(zip(keys, group_key))
        row.update({
            "n_original_classified_events": len(frame),
            "n_entry_eligible": len(eligible),
            "n_complete_horizons": len(complete),
            "n_excluded_or_incomplete": len(frame) - len(complete),
            "exclusion_reason_counts": json.dumps(
                frame.loc[
                    frame["horizon_status"] != "COMPLETE", "exclusion_reason"
                ].value_counts(dropna=False).to_dict(),
                sort_keys=True,
            ),
        })

        metrics = [
            "directional_close_return_pct", "mfe_pct", "mae_pct",
            "mfe_channel_width_pct", "mae_channel_width_pct",
            "time_to_mfe_minutes", "time_to_mae_minutes",
        ]
        for metric in metrics:
            values = complete[metric].dropna()
            row[f"{metric}_mean"] = float(values.mean()) if len(values) else np.nan
            row[f"{metric}_median"] = float(values.median()) if len(values) else np.nan
            for q in (10, 25, 50, 75, 90):
                row[f"{metric}_p{q}"] = (
                    float(values.quantile(q / 100)) if len(values) else np.nan
                )

        if len(complete):
            row["pct_positive_directional_close_return"] = float(
                (complete["directional_close_return_pct"] > 0).mean() * 100
            )
            row["pct_boundary_failure"] = float(
                complete["boundary_failure"].astype(bool).mean() * 100
            )
            row["n_boundary_failures"] = int(
                complete["boundary_failure"].astype(bool).sum()
            )
            row["n_immediate_adverse_entries"] = int(
                complete["entry_open_already_through_boundary"].astype(bool).sum()
            )
        else:
            row["pct_positive_directional_close_return"] = np.nan
            row["pct_boundary_failure"] = np.nan
            row["n_boundary_failures"] = 0
            row["n_immediate_adverse_entries"] = 0

        rows.append(row)

    summary = pd.DataFrame(rows)
    if int(summary["n_original_classified_events"].sum()) != len(outcomes):
        raise RuntimeError("Grouped summary denominators do not reconcile")
    if int(summary["n_complete_horizons"].sum()) != int(
        (outcomes["horizon_status"] == "COMPLETE").sum()
    ):
        raise RuntimeError("Grouped complete-horizon counts do not reconcile")
    return summary


def run(data_dir: Path, output_dir: Path):
    if output_dir.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing output directory: {output_dir}"
        )

    source_path = Path(SOURCE_REL)
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    actual_blob = git_blob_sha(source_path)
    if actual_blob != SOURCE_BLOB_SHA:
        raise RuntimeError(
            f"Original source Git blob mismatch: {actual_blob} != {SOURCE_BLOB_SHA}"
        )

    data, common, source_hashes, source_rows, first_ts, last_ts, common_gaps = (
        load_common_data(data_dir)
    )

    joined_by_asset = {}
    all_events = []
    all_quantiles = {}
    reproduced_counts = {}
    audit_rows = []

    for asset in ASSETS:
        joined, bars15, bars4 = build_joined(data[asset])
        joined_by_asset[asset] = joined
        events, quantiles, counts = original_events(
            asset, joined, data[asset]
        )
        all_events.extend(events)
        all_quantiles[asset] = quantiles
        reproduced_counts.update(counts)

        audit_rows.append({
            "asset": asset,
            "source_1m_rows": source_rows[asset],
            "common_1m_rows": len(common),
            "common_1m_gaps": common_gaps,
            "common_first_timestamp": str(common[0]),
            "common_last_timestamp": str(common[-1]),
            "source_first_timestamp": first_ts[asset],
            "source_last_timestamp": last_ts[asset],
            "complete_15m_bars": len(bars15),
            "complete_4h_bars": len(bars4),
            "joined_15m_rows": len(joined),
            "source_sha256": source_hashes[asset],
        })

    count_mismatches = []
    for key, expected in EXPECTED_COUNTS.items():
        actual = reproduced_counts.get(key, 0)
        if actual != expected:
            count_mismatches.append((key, expected, actual))

    quantile_mismatches = []
    for asset, (p25, p40) in EXPECTED_QUANTILES.items():
        actual = all_quantiles[asset]
        for name, expected in (("P25", p25), ("P40", p40)):
            if not np.isclose(
                actual[name], expected, rtol=0, atol=0.0000005
            ):
                quantile_mismatches.append(
                    (asset, name, expected, actual[name])
                )

    if count_mismatches or quantile_mismatches:
        raise RuntimeError(
            "Original reproduction gate FAILED. "
            f"Counts={count_mismatches}; quantiles={quantile_mismatches}"
        )

    strict_keys = {
        (e["asset"], e["direction"], e["signal_time"])
        for e in all_events if e["definition"] == "STRICT_P25"
    }
    broad_keys = {
        (e["asset"], e["direction"], e["signal_time"])
        for e in all_events if e["definition"] == "BROAD_P40"
    }
    if not strict_keys.issubset(broad_keys):
        raise RuntimeError("Strict event set is not a subset of broad event set")

    prior_dir = output_dir.parent / "breakout_prior_test_count_v1"
    input_paths = {
        "classifications": prior_dir / "breakout_prior_test_classifications_v1.csv",
        "links": prior_dir / "breakout_prior_test_links_v1.csv",
        "original_reproduction": prior_dir / "original_event_reproduction_v1.csv",
        "reconstruction_audit": prior_dir / "reconstruction_audit_v1.csv",
        "prior_metadata": prior_dir / "run_metadata.json",
    }
    for label, path in input_paths.items():
        if not path.is_file():
            raise FileNotFoundError(f"Missing {label} input: {path}")

    classifications = pd.read_csv(input_paths["classifications"])
    links = pd.read_csv(input_paths["links"])
    classifications = validate_classifications(
        classifications, links, all_events
    )

    outcomes = build_event_rows(classifications, data)
    summary = build_summary(outcomes)

    exclusions = outcomes.loc[
        outcomes["horizon_status"] != "COMPLETE"
    ].copy()

    reproduction_rows = []
    for key, expected in EXPECTED_COUNTS.items():
        reproduction_rows.append({
            "asset": key[0], "definition": key[1], "direction": key[2],
            "expected_event_count": expected,
            "reproduced_event_count": reproduced_counts.get(key, 0),
            "passed": reproduced_counts.get(key, 0) == expected,
        })
    reproduction = pd.DataFrame(reproduction_rows)

    quantile_rows = []
    for asset, vals in all_quantiles.items():
        for name, expected in (
            ("P25", EXPECTED_QUANTILES[asset][0]),
            ("P40", EXPECTED_QUANTILES[asset][1]),
        ):
            quantile_rows.append({
                "asset": asset, "quantile": name,
                "expected": expected, "reproduced": vals[name],
                "passed": bool(np.isclose(
                    vals[name], expected, rtol=0, atol=0.0000005
                )),
            })
    quantile_audit = pd.DataFrame(quantile_rows)

    output_dir.mkdir(parents=True, exist_ok=False)
    outputs = {
        "breakout_forward_outcomes_v1.csv": outcomes,
        "breakout_forward_group_summary_v1.csv": summary,
        "breakout_forward_exclusions_audit_v1.csv": exclusions,
        "original_event_reproduction_v1.csv": reproduction,
        "original_quantile_reproduction_v1.csv": quantile_audit,
        "reconstruction_audit_v1.csv": pd.DataFrame(audit_rows),
    }
    for name, frame in outputs.items():
        frame.to_csv(output_dir / name, index=False)

    run_log = [
        "BREAKOUT FORWARD OUTCOME STUDY V1",
        "PASS: original breakout event counts 20/20 reproduced.",
        "PASS: original channel-width quantiles 10/10 reproduced.",
        "PASS: original source Git blob SHA verified.",
        "PASS: every original event maps to exactly three prior-test zones.",
        "PASS: prior-test links reconcile with touch-test counts.",
        f"Common 1M timestamps: {len(common):,}",
        f"Original breakout events: {len(all_events):,}",
        f"Classification rows: {len(classifications):,}",
        f"Event-zone-horizon rows: {len(outcomes):,}",
        f"Complete horizon rows: {(outcomes['horizon_status'] == 'COMPLETE').sum():,}",
        f"Excluded/incomplete horizon rows: {len(exclusions):,}",
        "Entry: next 1M candle OPEN at signal_time.",
        "Horizon lengths: 15, 60, 240, and 720 consecutive 1M candles.",
        "Descriptive gross price movement only; no profitability inference.",
        "Full-sample channel quantiles are retrospective, not live calibrated.",
        "Touch-zone variants overlap and are not independent samples.",
        "Volume excluded because source units are unverified.",
    ]
    (output_dir / "run.log").write_text("\n".join(run_log) + "\n")

    input_hashes = {
        label: sha256_file(path) for label, path in input_paths.items()
    }
    output_hashes = {
        path.name: sha256_file(path)
        for path in output_dir.iterdir()
        if path.is_file()
    }

    metadata = {
        "study": "breakout_forward_outcome_study_v1",
        "specification": "docs/research_checkpoints/2026-11-24_breakout_forward_outcome_study_spec_v1.md",
        "measurement_clarification": "docs/research_checkpoints/2026-11-24_breakout_forward_outcome_study_measurement_clarification_v1.md",
        "original_source": SOURCE_REL,
        "original_source_git_blob_sha": actual_blob,
        "assets": ASSETS,
        "definitions": list(DEFINITIONS),
        "directions": list(DIRECTIONS),
        "zones_pct_of_channel": [5.0, 10.0, 15.0],
        "primary_zone_pct": 10.0,
        "horizons_minutes": HORIZONS,
        "entry_convention": "First 1M candle opening at signal_time; entry price is its OPEN.",
        "outcome_rows": len(outcomes),
        "classification_rows": len(classifications),
        "complete_horizon_rows": int(
            (outcomes["horizon_status"] == "COMPLETE").sum()
        ),
        "excluded_or_incomplete_rows": len(exclusions),
        "common_1m_timestamps": len(common),
        "common_1m_gaps": common_gaps,
        "source_rows": source_rows,
        "source_sha256": source_hashes,
        "input_sha256": input_hashes,
        "output_sha256": output_hashes,
        "expected_event_counts_reproduced": 20,
        "expected_quantiles_reproduced": 10,
        "strict_events_are_subset_of_broad": True,
        "pre_breakout_groups": list(GROUPS),
        "limitations": [
            "Descriptive historical forward outcomes only; no strategy or profitability inference.",
            "No fees, slippage, spread, funding, sizing, stops, or portfolio constraints.",
            "Full-sample channel-width quantiles are retrospective, not live calibrated.",
            "Touch-zone variants overlap and are not independent samples.",
            "OHLC data gives candle-level, not intraminute, extreme timing.",
            "Volume excluded because source units are unverified.",
        ],
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2, default=str) + "\n"
    )

    print("PASS: original event counts 20/20 and quantiles 10/10 reproduced.")
    print(f"Common 1M timestamps: {len(common):,}; gaps: {common_gaps}")
    print(f"Classification rows: {len(classifications):,}")
    print(f"Event-zone-horizon rows: {len(outcomes):,}")
    print(f"Complete horizons: {(outcomes['horizon_status'] == 'COMPLETE').sum():,}")
    print(f"Excluded/incomplete horizons: {len(exclusions):,}")
    print(f"Reports: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path,
        default=Path.home() / "okx_scalping_data",
    )
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path.home() / "okxtester" / "reports"
        / "breakout_forward_outcome_v1",
    )
    args = parser.parse_args()
    run(args.data_dir, args.output_dir)


if __name__ == "__main__":
    main()
