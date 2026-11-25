"""Sample OKX historical mark-price candles around audited funding settlements.

This is a source-reconnaissance tool only. It does not assign mark-candle OHLC
values as exact funding settlement marks and does not run a backtest.
"""
import argparse
import csv
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from run_exit_experiments import (
    ASSETS,
    load_funding_contract,
    load_funding_manifest,
)

BASE_URL = "https://www.okx.com/api/v5/market/history-mark-price-candles"
SAMPLE_LABELS = ("first", "middle", "last")


def fetch_mark_candles(inst_id, target_ts, timeout=20):
    """Fetch a small 1m history window ending just after target_ts."""
    params = urlencode({
        "instId": inst_id,
        "bar": "1m",
        # The API's after cursor returns records earlier than this timestamp.
        # Advancing one minute makes the target minute eligible for the page.
        "after": str(int(target_ts) + 60_000),
        "limit": "100",
    })
    request = Request(
        f"{BASE_URL}?{params}",
        headers={"User-Agent": "okxtester-funding-source-audit/1.0"},
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if payload.get("code") != "0":
        raise RuntimeError(
            f"OKX API error for {inst_id}: "
            f"code={payload.get('code')} msg={payload.get('msg')}"
        )
    rows = payload.get("data")
    if not isinstance(rows, list):
        raise RuntimeError(f"OKX returned a non-list data field for {inst_id}")
    parsed = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 6:
            raise RuntimeError(f"Unexpected mark-candle row for {inst_id}: {row!r}")
        parsed.append({
            "ts": int(row[0]),
            "open": float(row[1]),
            "high": float(row[2]),
            "low": float(row[3]),
            "close": float(row[4]),
            "confirm": str(row[5]),
        })
    return parsed


def load_trade_closes(path, target_timestamps):
    """Read only the three requested trade-candle closes; keep memory small."""
    targets = set(int(value) for value in target_timestamps)
    found = {}
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"ts", "close"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path}: candle CSV must contain ts and close")
        for line_number, row in enumerate(reader, start=2):
            try:
                timestamp = int(float(row["ts"]))
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{path}: invalid timestamp on line {line_number}"
                ) from exc
            if timestamp not in targets:
                continue
            if timestamp in found:
                raise ValueError(
                    f"{path}: duplicate candle timestamp {timestamp}"
                )
            try:
                found[timestamp] = float(row["close"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{path}: invalid close on line {line_number}"
                ) from exc
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--pause-seconds", type=float, default=0.15)
    parser.add_argument("--samples-per-asset", type=int, default=12)
    args = parser.parse_args(argv)

    if args.pause_seconds < 0.1:
        parser.error("--pause-seconds must be at least 0.1 to respect API rate limits")
    if args.samples_per_asset < 2:
        parser.error("--samples-per-asset must be at least 2")

    manifest, manifest_assets, manifest_sha = load_funding_manifest(args.repo_root)
    funding_dir = args.home / "okx_scalping_data/funding_rates/processed"
    candle_dir = args.home / "okx_scalping_data"

    print("OKX HISTORICAL MARK-PRICE DISTRIBUTED SAMPLE AUDIT")
    print(f"Funding manifest SHA-256: {manifest_sha}")
    print(f"Target samples per instrument: {args.samples_per_asset}")
    print("Sampling: evenly spaced across each audited funding-event history")
    print("Mark-price source: GET /api/v5/market/history-mark-price-candles")
    print("Bar: 1m | No backtest | No exact-settlement claim")
    print()

    request_count = 0
    errors = 0
    missing_mark = 0
    missing_trade = 0
    duplicate_mark = 0
    incomplete_mark = 0

    for asset in ASSETS:
        funding_path = funding_dir / f"{asset}_USDT_SWAP_funding_rates.csv"
        contract = load_funding_contract(
            funding_path, asset, manifest_assets[asset]
        )
        events = contract["events"]
        sample_count = min(args.samples_per_asset, len(events))
        if sample_count < 2:
            raise ValueError(f"{asset}: fewer than two funding events available")
        indices = sorted({
            round(i * (len(events) - 1) / (sample_count - 1))
            for i in range(sample_count)
        })

        candle_path = candle_dir / f"{asset}_USDT_USDT_1m.csv"
        targets = [int(events[index]["funding_time"]) for index in indices]
        trade_closes = load_trade_closes(candle_path, targets)
        asset_diffs = []
        asset_matched = 0
        asset_boundary_excluded = 0
        asset_found = 0

        print(
            f"{asset}: funding_events={len(events)} "
            f"samples={len(indices)}"
        )
        for sample_number, (index, target) in enumerate(zip(indices, targets), 1):
            request_count += 1
            try:
                mark_rows = fetch_mark_candles(
                    manifest_assets[asset]["instrument_name"], target
                )
            except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError) as exc:
                errors += 1
                print(
                    f"  sample={sample_number:02d} ts={target}: API_ERROR "
                    f"{type(exc).__name__}: {exc}"
                )
                time.sleep(args.pause_seconds)
                continue

            exact = [row for row in mark_rows if row["ts"] == target]
            if not exact:
                missing_mark += 1
                nearest = min(
                    mark_rows,
                    key=lambda row: abs(row["ts"] - target),
                    default=None,
                )
                nearest_text = (
                    "none" if nearest is None
                    else f"{nearest['ts']} (delta_ms={nearest['ts'] - target})"
                )
                print(
                    f"  sample={sample_number:02d} ts={target}: "
                    f"MARK_CANDLE_NOT_FOUND rows={len(mark_rows)} "
                    f"nearest={nearest_text}"
                )
            else:
                asset_found += 1
                if len(exact) > 1:
                    duplicate_mark += len(exact) - 1
                    print(
                        f"  sample={sample_number:02d} ts={target}: "
                        f"DUPLICATE_MARK_CANDLE count={len(exact)}"
                    )
                row = exact[-1]
                if row["confirm"] != "1":
                    incomplete_mark += 1
                trade_close = trade_closes.get(target)
                if trade_close is None:
                    missing_trade += 1
                    asset_boundary_excluded += 1
                    trade_text = "TRADE_CANDLE_OUTSIDE_LOCAL_COVERAGE"
                else:
                    diff_bps = (row["close"] / trade_close - 1.0) * 10_000
                    asset_diffs.append(diff_bps)
                    asset_matched += 1
                    trade_text = (
                        f"trade_close={trade_close:.12g} "
                        f"close_diff_bps={diff_bps:.6f}"
                    )
                print(
                    f"  sample={sample_number:02d} ts={target}: "
                    f"mark_o={row['open']:.12g} mark_h={row['high']:.12g} "
                    f"mark_l={row['low']:.12g} mark_c={row['close']:.12g} "
                    f"confirm={row['confirm']} {trade_text}"
                )
            time.sleep(args.pause_seconds)

        if asset_diffs:
            ordered = sorted(asset_diffs)
            median = (
                ordered[len(ordered) // 2]
                if len(ordered) % 2
                else (ordered[len(ordered) // 2 - 1] + ordered[len(ordered) // 2]) / 2
            )
            print(
                f"  ASSET_SUMMARY mark_found={asset_found}/{len(indices)} "
                f"trade_comparisons={asset_matched} "
                f"boundary_excluded={asset_boundary_excluded} "
                f"close_diff_bps_min={ordered[0]:.6f} "
                f"median={median:.6f} max={ordered[-1]:.6f}"
            )
        else:
            print(
                f"  ASSET_SUMMARY mark_found={asset_found}/{len(indices)} "
                f"trade_comparisons=0 boundary_excluded={asset_boundary_excluded} "
                "close_diff_bps=NO_COMPARABLE_SAMPLES"
            )
        print()

    print(
        "SUMMARY "
        f"requests={request_count} api_errors={errors} "
        f"missing_mark_candles={missing_mark} "
        f"duplicate_extra_mark_rows={duplicate_mark} "
        f"incomplete_mark_candles={incomplete_mark} "
        f"missing_trade_comparisons_outside_local_coverage={missing_trade}"
    )
    print(
        "IMPORTANT: a mark-price candle is still an OHLC interval aggregate. "
        "Matching its timestamp to a funding timestamp does not establish "
        "that its open or close was the exact exchange settlement mark."
    )
    print("No backtest was run.")


if __name__ == "__main__":
    main()
