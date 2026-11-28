"""Historical 1m open-through-stop gap-risk audit; no trade simulation or PnL."""
import argparse, csv, hashlib, json, math
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SYMBOLS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
DEFAULT_STOP_DISTANCES_PCT = (0.05, 0.1, 0.15, 0.2, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0)
SYNTHETIC_GAP_BEYOND_STOP_PCT = (0.05, 0.1, 0.25, 0.5, 1.0, 2.0)
INTERVAL_MS = 60_000
PERCENTILES = (50, 90, 95, 99)

def _percentile(values, percentile):
    if not values: return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile / 100.0
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper: return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight

def _empty_bucket():
    return {"loss_multiples": [], "overshoot_bps": [], "adverse_move_bps": []}

def _summarize_bucket(bucket):
    result = {"gap_events": len(bucket["loss_multiples"])}
    for key, values in (
        ("gap_loss_multiple", bucket["loss_multiples"]),
        ("stop_overshoot_bps", bucket["overshoot_bps"]),
        ("adverse_open_move_bps", bucket["adverse_move_bps"]),
    ):
        result[key] = {f"p{p}": _percentile(values, p) for p in PERCENTILES}
        result[key]["max"] = max(values) if values else None
    return result

def analyze_bars(rows, stop_distances):
    """Analyze consecutive one-minute transitions from prior close to next open."""
    distances = tuple(float(value) for value in stop_distances)
    if not distances or any(not math.isfinite(v) or not 0 < v < 100 for v in distances):
        raise ValueError("Stop distances must be finite percentages in (0, 100)")
    buckets = {(d, side): _empty_bucket() for d in distances for side in ("LONG", "SHORT")}
    eligible = skipped = row_count = 0
    first_ts = last_ts = None
    previous = None
    open_jump_abs_bps = []
    long_adverse_open_jump_bps = []
    short_adverse_open_jump_bps = []
    for row in rows:
        row_count += 1
        try:
            ts_value = float(row["ts"])
            if not math.isfinite(ts_value) or not ts_value.is_integer(): raise ValueError
            ts = int(ts_value)
            prices = {name: float(row[name]) for name in ("open", "high", "low", "close")}
        except (KeyError, TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"Invalid timestamp/OHLC at row {row_count}") from exc
        if ts <= 0 or not all(math.isfinite(v) and v > 0 for v in prices.values()):
            raise ValueError(f"Non-positive or non-finite timestamp/OHLC at row {row_count}")
        if prices["high"] < max(prices["open"], prices["close"], prices["low"]):
            raise ValueError(f"Inconsistent high at row {row_count}")
        if prices["low"] > min(prices["open"], prices["close"], prices["high"]):
            raise ValueError(f"Inconsistent low at row {row_count}")
        if first_ts is None: first_ts = ts
        if previous is not None:
            delta = ts - previous["ts"]
            if delta <= 0: raise ValueError("Timestamps must be strictly increasing and unique")
            if delta == INTERVAL_MS:
                eligible += 1
                reference, next_open = previous["close"], prices["open"]
                signed_jump_bps = (next_open / reference - 1.0) * 10_000.0
                open_jump_abs_bps.append(abs(signed_jump_bps))
                long_adverse_open_jump_bps.append(max(0.0, -signed_jump_bps))
                short_adverse_open_jump_bps.append(max(0.0, signed_jump_bps))
                for distance_pct in distances:
                    distance = distance_pct / 100.0
                    long_stop = reference * (1.0 - distance)
                    if next_open <= long_stop:
                        bucket = buckets[(distance_pct, "LONG")]
                        bucket["loss_multiples"].append((reference - next_open) / (reference * distance))
                        bucket["overshoot_bps"].append((long_stop - next_open) / long_stop * 10_000.0)
                        bucket["adverse_move_bps"].append((reference - next_open) / reference * 10_000.0)
                    short_stop = reference * (1.0 + distance)
                    if next_open >= short_stop:
                        bucket = buckets[(distance_pct, "SHORT")]
                        bucket["loss_multiples"].append((next_open - reference) / (reference * distance))
                        bucket["overshoot_bps"].append((next_open - short_stop) / short_stop * 10_000.0)
                        bucket["adverse_move_bps"].append((next_open - reference) / reference * 10_000.0)
            else:
                skipped += 1
        previous = {"ts": ts, "close": prices["close"]}
        last_ts = ts
    if row_count < 2: raise ValueError("At least two candles are required")
    jump_distributions = {}
    for name, values in (
        ("absolute_open_jump", open_jump_abs_bps),
        ("long_adverse_open_jump", long_adverse_open_jump_bps),
        ("short_adverse_open_jump", short_adverse_open_jump_bps),
    ):
        jump_distributions[name] = {f"p{p}": _percentile(values, p) for p in PERCENTILES}
        jump_distributions[name]["max"] = max(values) if values else None
    results = []
    for distance_pct in distances:
        for side in ("LONG", "SHORT"):
            summary = _summarize_bucket(buckets[(distance_pct, side)])
            summary.update({
                "stop_distance_pct": distance_pct, "side": side,
                "eligible_minute_transitions": eligible,
                "skipped_nonconsecutive_transitions": skipped,
                "gap_rate_pct": summary["gap_events"] / eligible * 100.0 if eligible else None,
            })
            results.append(summary)
    return {
        "row_count": row_count, "first_timestamp_ms": first_ts, "last_timestamp_ms": last_ts,
        "first_utc": datetime.fromtimestamp(first_ts / 1000.0, timezone.utc).isoformat(),
        "last_utc": datetime.fromtimestamp(last_ts / 1000.0, timezone.utc).isoformat(),
        "open_jump_distributions_bps": jump_distributions,
        "eligible_minute_transitions": eligible,
        "skipped_nonconsecutive_transitions": skipped, "scenarios": results,
    }

def _sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""): digest.update(chunk)
    return digest.hexdigest()

def audit_csv(path, symbol, stop_distances):
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"ts", "open", "high", "low", "close"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            missing = sorted(required - set(reader.fieldnames or []))
            raise ValueError(f"{symbol}: missing required CSV columns: {missing}")
        analysis = analyze_bars(reader, stop_distances)
    return {"symbol": symbol, "source_file": path.name, "source_sha256": _sha256(path), **analysis}

def main(argv=None):
    parser = argparse.ArgumentParser(description="Measure historical 1m opens that gap through hypothetical stop levels.")
    default_data_dir = Path(__file__).resolve().parents[1] / "data" / "market_1m"
    parser.add_argument("--data-dir", type=Path, default=default_data_dir)
    parser.add_argument("--output", type=Path, default=Path("reports/g0_07_stop_gap_risk_audit_v1.json"))
    parser.add_argument("--symbols", default=",".join(DEFAULT_SYMBOLS))
    parser.add_argument("--stop-distances-pct", default=",".join(str(v) for v in DEFAULT_STOP_DISTANCES_PCT))
    args = parser.parse_args(argv)
    symbols = tuple(item.strip().upper() for item in args.symbols.split(",") if item.strip())
    try: distances = tuple(float(item) for item in args.stop_distances_pct.split(","))
    except ValueError as exc: parser.error(f"Invalid stop distance: {exc}")
    if not symbols or len(set(symbols)) != len(symbols): parser.error("Symbols must be non-empty and unique")
    assets = []
    for symbol in symbols:
        path = args.data_dir / f"{symbol}_USDT_USDT_1m.csv"
        if not path.is_file(): raise FileNotFoundError(f"Required historical candle file not found: {path}")
        assets.append(audit_csv(path, symbol, distances))
    report = {
        "audit_id": "G0-07_STOP_GAP_RISK_HISTORICAL_1M_V1",
        "status": "HISTORICAL_OPEN_THROUGH_STOP_AUDIT_COMPLETE",
        "method": "For each contiguous 1m pair, prior candle close is a hypothetical reference entry; next candle open is tested against stops at the configured percentage distance.",
        "scope": [
            "Historical OHLC open-through-stop frequency and severity only",
            "No strategy signals, trade selection, order simulation, or strategy PnL",
            "No measured order-book liquidity, queue position, or execution slippage",
            "No contract multiplier, lot/tick rounding, or account fee-tier assumptions",
        ],
        "stop_distances_pct": list(distances), "percentiles": list(PERCENTILES), "assets": assets,
        "synthetic_stress_scenarios": [
            {
                "stop_distance_pct": distance,
                "gap_beyond_stop_pct_of_reference_entry": gap,
                "price_loss_multiple": (distance + gap) / distance,
                "synthetic_only": True,
            }
            for distance in distances for gap in SYNTHETIC_GAP_BEYOND_STOP_PCT
        ],
        "interpretation": {
            "gap_loss_multiple": "Adverse prior-close-to-next-open price move divided by the hypothetical stop distance; values are at least 1 for counted events.",
            "stop_overshoot_bps": "Distance from the stop level to the next open, in basis points of the stop level.",
            "gap_rate_pct": "Counted open-through-stop transitions divided by contiguous one-minute transitions.",
            "open_jump_distributions_bps": "Absolute and direction-specific adverse next-open movement relative to the previous close across every contiguous transition, including zero values for the non-adverse direction.",
            "synthetic_stress_scenarios": "Hypothetical extra gap beyond the stop, expressed as a percentage of reference entry; price loss multiple equals (stop distance + extra gap) / stop distance and excludes fees, slippage, and market impact.",
            "limitations": "This is a candle-open gap proxy, not a guaranteed fill-price distribution. It excludes intraminute execution slippage and order-book impact. Stop distances are sensitivity scenarios, not strategy parameters.",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("G0-07 HISTORICAL STOP-GAP AUDIT")
    print(f"Assets: {len(assets)}")
    for asset in assets:
        jumps = asset["open_jump_distributions_bps"]
        print(f"{asset['symbol']}: rows={asset['row_count']:,}, eligible={asset['eligible_minute_transitions']:,}, nonconsecutive_skipped={asset['skipped_nonconsecutive_transitions']:,}, period={asset['first_utc']}..{asset['last_utc']}, sha256={asset['source_sha256']}")
        print(f"  open-jump abs bps: p50={jumps['absolute_open_jump']['p50']:.4f}, p99={jumps['absolute_open_jump']['p99']:.4f}, max={jumps['absolute_open_jump']['max']:.4f}")
        print(f"  adverse max bps: long={jumps['long_adverse_open_jump']['max']:.4f}, short={jumps['short_adverse_open_jump']['max']:.4f}")
        for item in asset["scenarios"]:
            p95 = item["gap_loss_multiple"]["p95"]
            print(f"  {item['side']:5s} stop={item['stop_distance_pct']:g}% gaps={item['gap_events']:,} rate={item['gap_rate_pct'] if item['gap_rate_pct'] is not None else 'n/a'} p95_gap_loss={'n/a' if p95 is None else f'{p95:.4f}R'}")
    print(f"JSON report: {args.output}")
    print("No strategy PnL or execution simulation was performed.")

if __name__ == "__main__":
    main()
