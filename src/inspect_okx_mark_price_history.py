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
    args = parser.parse_args(argv)

    if args.pause_seconds < 0.1:
        parser.error("--pause-seconds must be at least 0.1 to respect API rate limits")

    manifest, manifest_assets, manifest_sha = load_funding_manifest(args.repo_root)
    funding_dir = args.home / "okx_scalping_data/funding_rates/processed"
    candle_dir = args.home / "okx_scalping_data"

    print("OKX HISTORICAL MARK-PRICE SAMPLE AUDIT")
    print(f"Funding manifest SHA-256: {manifest_sha}")
    print("Samples per instrument: first / middle / last audited settlement")
    print("Mark-price source: GET /api/v5/market/history-mark-price-candles")
    print("Bar: 1m | No backtest | No exact-settlement claim")
    print()

    request_count = 0
    errors = 0
    missing_mark = 0
    missing_trade = 0

    for asset in ASSETS:
        funding_path = funding_dir / f"{asset}_USDT_SWAP_funding_rates.csv"
        contract = load_funding_contract(
            funding_path, asset, manifest_assets[asset]
        )
        events = contract["events"]
        indices = (0, len(events) // 2, len(events) - 1)

        candle_path = candle_dir / f"{asset}_USDT_USDT_1m.csv"
        targets = [int(events[index]["funding_time"]) for index in indices]
        trade_closes = load_trade_closes(candle_path, targets)

        for label, index in zip(SAMPLE_LABELS, indices):
            event = events[index]
            target = int(event["funding_time"])
            try:
                mark_rows = fetch_mark_candles(
                    manifest_assets[asset]["instrument_name"], target
                )
                request_count += 1
            except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError) as exc:
                errors += 1
                print(
                    f"{asset} {label} ts={target}: API_ERROR "
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
                    f"{asset} {label} ts={target}: MARK_CANDLE_NOT_FOUND "
                    f"rows={len(mark_rows)} nearest={nearest_text}"
                )
            else:
                if len(exact) > 1:
                    print(
                        f"{asset} {label} ts={target}: DUPLICATE_MARK_CANDLE "
                        f"count={len(exact)}"
                    )
                row = exact[-1]
                trade_close = trade_closes.get(target)
                if trade_close is None:
                    missing_trade += 1
                    trade_text = "TRADE_CANDLE_NOT_FOUND"
                else:
                    diff_bps = (row["close"] / trade_close - 1.0) * 10_000
                    trade_text = f"{trade_close:.12g} close_diff_bps={diff_bps:.6f}"
                print(
                    f"{asset} {label} ts={target}: "
                    f"mark_o={row['open']:.12g} mark_h={row['high']:.12g} "
                    f"mark_l={row['low']:.12g} mark_c={row['close']:.12g} "
                    f"confirm={row['confirm']} trade={trade_text}"
                )
            time.sleep(args.pause_seconds)

    print()
    print(
        "SUMMARY "
        f"requests={request_count} api_errors={errors} "
        f"missing_mark_candles={missing_mark} "
        f"missing_trade_candles={missing_trade}"
    )
    print(
        "IMPORTANT: a mark-price candle is still an OHLC interval aggregate. "
        "Matching its timestamp to a funding timestamp does not establish "
        "that its open or close was the exact exchange settlement mark."
    )
    print("No backtest was run.")


if __name__ == "__main__":
    main()
