#!/usr/bin/env python3
"""Pre-event matched-control sensitivity study for sideways rejection sequences V1.

Matches SEPARATION_FIRST and RETEST_FIRST events on asset, boundary direction,
calendar month, and pre-confirmation market/channel/candle covariates. Outcomes
are evaluated only after the already-defined 15-minute classification landmark.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

CLASSES = ("SEPARATION_FIRST", "RETEST_FIRST")
HORIZONS = ("1h", "4h", "24h")
METRICS = ("final_close_direction_adjusted_midpoint_width",
           "max_inward_excursion_width", "max_outward_penetration_width")
FEATURES = ("channel_width_pct", "directional_efficiency", "mean_overlap",
            "width_p50_pct")
ANATOMY = ("range_channel_width", "body_range_ratio", "upper_wick_range_ratio",
           "lower_wick_range_ratio", "close_location_in_range",
           "signed_close_boundary_distance_width")
COVARIATES = (*FEATURES, *ANATOMY, "pre_60m_realized_vol",
              "pre_240m_realized_vol", "test_rank", "test_duration_minutes")


def robust_scale(frame: pd.DataFrame, columns=COVARIATES) -> tuple[np.ndarray, np.ndarray]:
    x = frame[list(columns)].to_numpy(dtype=float)
    med = np.nanmedian(x, axis=0)
    mad = np.nanmedian(np.abs(x - med), axis=0) * 1.4826
    std = np.nanstd(x, axis=0, ddof=1)
    scale = np.where(np.isfinite(mad) & (mad > 1e-12), mad, std)
    scale = np.where(np.isfinite(scale) & (scale > 1e-12), scale, 1.0)
    return med, scale


def greedy_match(frame: pd.DataFrame, *, max_distance: float = 3.0) -> pd.DataFrame:
    """Greedy global minimum-distance 1:1 matching within exact strata."""
    required = {"event_id", "sequence_class", "asset", "direction", "confirmation_month", *COVARIATES}
    if not required.issubset(frame.columns):
        raise ValueError("matching frame is missing required columns")
    data = frame[frame.sequence_class.isin(CLASSES)].copy().reset_index(drop=True)
    if data.event_id.duplicated().any():
        raise ValueError("event_id must be unique for matching")
    med, scale = robust_scale(data)
    z = (data[list(COVARIATES)].to_numpy(dtype=float) - med) / scale
    if not np.isfinite(z).all():
        raise ValueError("non-finite matching covariates")
    data["_row"] = np.arange(len(data))
    pairs = []
    strata = ["asset", "direction", "confirmation_month"]
    for _, group in data.groupby(strata, sort=True, dropna=False):
        a = group[group.sequence_class == CLASSES[0]]
        b = group[group.sequence_class == CLASSES[1]]
        if a.empty or b.empty:
            continue
        ai, bi = a["_row"].to_numpy(), b["_row"].to_numpy()
        dist = np.sqrt(np.mean((z[ai, None, :] - z[None, bi, :]) ** 2, axis=2))
        edges = [(float(dist[i, j]), int(ai[i]), int(bi[j]))
                 for i in range(len(ai)) for j in range(len(bi))
                 if dist[i, j] <= max_distance]
        edges.sort(key=lambda item: (item[0], item[1], item[2]))
        used_a, used_b = set(), set()
        for d, ia, ib in edges:
            if ia in used_a or ib in used_b:
                continue
            used_a.add(ia); used_b.add(ib)
            ra, rb = data.iloc[ia], data.iloc[ib]
            pairs.append({"pair_id": f"P{len(pairs)+1:06d}",
                          "separation_event_id": ra.event_id,
                          "retest_event_id": rb.event_id,
                          "asset": ra.asset, "direction": ra.direction,
                          "confirmation_month": ra.confirmation_month,
                          "separation_confirmation_ts_ms": int(ra['confirmation_ts_ms']),
                          "retest_confirmation_ts_ms": int(rb['confirmation_ts_ms']),
                          "pair_confirmation_ts_ms": int((int(ra.confirmation_ts_ms)+int(rb.confirmation_ts_ms))//2),
                          "match_distance_rms_robust_sd": d})
    return pd.DataFrame(pairs, columns=["pair_id", "separation_event_id", "retest_event_id",
        "asset", "direction", "confirmation_month", "separation_confirmation_ts_ms",
        "retest_confirmation_ts_ms", "pair_confirmation_ts_ms", "match_distance_rms_robust_sd"])


def smd(a: pd.Series, b: pd.Series) -> float:
    x, y = a.to_numpy(dtype=float), b.to_numpy(dtype=float)
    pooled = np.sqrt((np.nanvar(x, ddof=1) + np.nanvar(y, ddof=1)) / 2)
    return float((np.nanmean(x) - np.nanmean(y)) / pooled) if pooled > 0 else 0.0


def paired_block_bootstrap(differences: pd.DataFrame, *, block_days: int,
                           replicates: int, rng: np.random.Generator) -> dict:
    if differences.empty:
        return {"observed_difference": np.nan, "ci_2_5": np.nan, "ci_97_5": np.nan,
                "valid_replicates": 0, "pairs": 0}
    d = differences.copy()
    d["day"] = pd.to_datetime(d.pair_confirmation_ts_ms, unit="ms", utc=True).dt.floor("D")
    first, last = d.day.min(), d.day.max()
    n_days = int((last-first)/pd.Timedelta(days=1))+1
    day_ix = ((d.day-first)/pd.Timedelta(days=1)).to_numpy(dtype=np.int64)
    sums, counts = np.zeros(n_days), np.zeros(n_days)
    np.add.at(sums, day_ix, d.difference.to_numpy(dtype=float))
    np.add.at(counts, day_ix, 1)
    observed = float(sums.sum()/counts.sum())
    block_days = min(block_days, n_days)
    starts = np.arange(n_days-block_days+1)
    offsets = np.arange(block_days)
    nblocks = int(np.ceil(n_days/block_days))
    boot = []
    for _ in range(replicates):
        ix = (rng.choice(starts, size=nblocks, replace=True)[:, None]+offsets).ravel()
        mult = np.bincount(ix, minlength=n_days).astype(float)
        denom = float(np.dot(counts, mult))
        if denom:
            boot.append(float(np.dot(sums, mult)/denom))
    ci = np.quantile(boot, [.025, .975]) if boot else [np.nan, np.nan]
    return {"observed_difference": observed, "ci_2_5": float(ci[0]),
            "ci_97_5": float(ci[1]), "valid_replicates": len(boot), "pairs": len(d)}


def build_covariates(anatomy_path: Path, sequence_path: Path, feature_dir: Path,
                     minute_dir: Path) -> pd.DataFrame:
    anatomy = pd.read_csv(anatomy_path)
    seq = pd.read_csv(sequence_path)
    base = anatomy.merge(seq[["event_id", "definition", "sequence_class",
        "confirmation_ts_ms", "classification_status"]], on=["event_id", "definition"],
        how="inner", validate="one_to_one", suffixes=("", "_seq"))
    if (base.confirmation_ts_ms != base.confirmation_ts_ms_seq).any():
        raise ValueError("anatomy/sequence confirmation mismatch")
    feature_rows = []
    for asset in sorted(base.asset.unique()):
        f = pd.read_csv(feature_dir / f"{asset}_features_original_v1.csv")
        needed = ["available_at_ts_ms", *FEATURES]
        if not set(needed).issubset(f.columns):
            raise ValueError(f"{asset}: missing frozen feature columns")
        f = f[needed].copy()
        f["asset"] = asset
        f["available_at_ts_ms"] = pd.to_numeric(f.available_at_ts_ms, errors="raise").astype("int64")
        feature_rows.append(f)
    features = pd.concat(feature_rows, ignore_index=True)
    base = base.merge(features, left_on=["asset", "snapshot_available_at_ts_ms"],
                      right_on=["asset", "available_at_ts_ms"], how="left",
                      validate="many_to_one")
    if base[list(FEATURES)].isna().any().any():
        raise ValueError("feature snapshot join has missing covariates")
    for asset in sorted(base.asset.unique()):
        path = minute_dir / f"{asset}_USDT_USDT_1m.csv"
        m = pd.read_csv(path, usecols=["ts", "close"])
        ts = pd.to_numeric(m.ts, errors="raise").to_numpy(dtype=np.int64)
        close = pd.to_numeric(m.close, errors="raise").to_numpy(dtype=float)
        if len(ts) < 300 or not np.isfinite(close).all() or (close <= 0).any():
            raise ValueError(f"{asset}: invalid minute data for volatility")
        mask = base.asset.to_numpy() == asset
        rows = base.loc[mask]
        v60, v240 = [], []
        for confirm in rows.confirmation_ts_ms.to_numpy(dtype=np.int64):
            ix = int(np.searchsorted(ts, confirm, side="left"))
            if ix < 241 or ix >= len(ts) or ts[ix] != confirm:
                v60.append(np.nan); v240.append(np.nan); continue
            ret = np.diff(np.log(close[ix-240:ix+1]))
            v60.append(float(np.std(ret[-60:], ddof=1)))
            v240.append(float(np.std(ret, ddof=1)))
        base.loc[mask, "pre_60m_realized_vol"] = v60
        base.loc[mask, "pre_240m_realized_vol"] = v240
    base["test_duration_minutes"] = (
        pd.to_numeric(base.confirmation_ts_ms) - pd.to_numeric(base.test_start_ts_ms)
    ) / 60000.0
    base["confirmation_month"] = pd.to_datetime(base.confirmation_ts_ms, unit="ms", utc=True).dt.strftime("%Y-%m")
    base["test_rank"] = pd.to_numeric(base.test_rank, errors="raise")
    keep = base[(base.classification_status == "complete") &
                base.sequence_class.isin(CLASSES)].copy()
    if keep[list(COVARIATES)].isna().any().any():
        raise ValueError("matching covariates contain missing values")
    return keep


def run(anatomy_path: Path, sequence_path: Path, outcomes_path: Path, feature_dir: Path,
        minute_dir: Path, output_dir: Path, replicates: int = 10000,
        seed: int = 20261124, max_distance: float = 3.0, blocks=(3, 7, 14)) -> pd.DataFrame:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing non-empty output directory: {output_dir}")
    cov = build_covariates(anatomy_path, sequence_path, feature_dir, minute_dir)
    out = pd.read_csv(outcomes_path)
    pairs_by_def, diagnostics, balance = {}, [], []
    for definition in ("broad", "strict"):
        cohort = cov[cov.definition == definition].copy()
        pairs = greedy_match(cohort, max_distance=max_distance)
        pairs_by_def[definition] = pairs
        diagnostics.append({"definition": definition, "eligible_separation_first": int((cohort.sequence_class==CLASSES[0]).sum()),
            "eligible_retest_first": int((cohort.sequence_class==CLASSES[1]).sum()), "matched_pairs": len(pairs),
            "unmatched_separation_first": int((cohort.sequence_class==CLASSES[0]).sum())-len(pairs),
            "unmatched_retest_first": int((cohort.sequence_class==CLASSES[1]).sum())-len(pairs),
            "max_distance_rms_robust_sd": max_distance})
        a = cohort[cohort.sequence_class == CLASSES[0]]
        b = cohort[cohort.sequence_class == CLASSES[1]]
        amap = a.set_index("event_id"); bmap = b.set_index("event_id")
        for c in COVARIATES:
            before = smd(a[c], b[c])
            if len(pairs):
                pa = amap.loc[pairs.separation_event_id, c]
                pb = bmap.loc[pairs.retest_event_id, c]
                after = smd(pa, pb)
            else:
                after = np.nan
            balance.append({"definition": definition, "covariate": c,
                            "smd_before": before, "smd_after": after})
    pair_df = pd.concat([pairs.assign(definition=d) for d,pairs in pairs_by_def.items()], ignore_index=True)
    rng = np.random.default_rng(seed)
    contrasts = []
    for definition, pairs in pairs_by_def.items():
        for horizon in HORIZONS:
            h = out[(out.definition == definition) & (out.horizon == horizon) &
                    (out.status == "complete")].set_index("event_id")
            for metric in METRICS:
                rows = []
                for p in pairs.itertuples(index=False):
                    if p.separation_event_id not in h.index or p.retest_event_id not in h.index:
                        continue
                    va, vb = h.at[p.separation_event_id, metric], h.at[p.retest_event_id, metric]
                    if pd.notna(va) and pd.notna(vb):
                        rows.append({"pair_id": p.pair_id, "pair_confirmation_ts_ms": p.pair_confirmation_ts_ms,
                                     "difference": float(va-vb)})
                d = pd.DataFrame(rows)
                for block in blocks:
                    r = paired_block_bootstrap(d, block_days=block, replicates=replicates, rng=rng)
                    contrasts.append({"definition": definition, "horizon": horizon, "metric": metric,
                                      "block_days": block, "contrast": "matched SEPARATION_FIRST minus RETEST_FIRST",
                                      **r})
    output_dir.mkdir(parents=True, exist_ok=True)
    pair_df.to_csv(output_dir/"matched_pairs_v1.csv", index=False)
    pd.DataFrame(diagnostics).to_csv(output_dir/"match_diagnostics_v1.csv", index=False)
    pd.DataFrame(balance).to_csv(output_dir/"covariate_balance_v1.csv", index=False)
    result = pd.DataFrame(contrasts)
    result.to_csv(output_dir/"matched_outcome_contrasts_v1.csv", index=False)
    metadata = {"study":"Sideways Rejection Pre-event Matched Control Sensitivity V1",
        "matching":"1:1 greedy nearest-neighbour without replacement; exact asset, direction, and UTC confirmation month strata",
        "distance":"root-mean-square difference on robust median/MAD-scaled pre-confirmation covariates",
        "maximum_match_distance_rms_robust_sd":max_distance,
        "covariates":list(COVARIATES),
        "pre_event_only":True,"outcomes":"strictly post-15-minute classification landmark",
        "bootstrap":"paired differences resampled in shared UTC calendar-day moving blocks",
        "block_lengths_days":list(blocks),"replicates_per_contrast":replicates,"seed":seed,
        "contrast":"SEPARATION_FIRST minus RETEST_FIRST",
        "limitations":["observational matched sensitivity analysis, not causal identification",
            "greedy matching is not globally optimal and caliper may leave unmatched events",
            "exact asset/direction/month strata reduce generalizability and sample size",
            "matching cannot remove unmeasured confounding",
            "bootstrap intervals are not adjusted for multiple comparisons",
            "broad and strict cohorts are nested, not independent"]}
    (output_dir/"run_metadata_v1.json").write_text(json.dumps(metadata,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {len(result)} matched contrasts and {len(pair_df)} matched pairs")
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("anatomy","sequence","outcomes","feature-dir","minute-dir","output"):
        p.add_argument("--"+arg, type=Path, required=True)
    p.add_argument("--replicates",type=int,default=10000)
    p.add_argument("--seed",type=int,default=20261124)
    p.add_argument("--max-distance",type=float,default=3.0)
    a=p.parse_args()
    run(a.anatomy,a.sequence,a.outcomes,a.feature_dir,a.minute_dir,a.output,
        a.replicates,a.seed,a.max_distance)


if __name__=="__main__":
    main()
