"""Read-only sample comparison of repository OHLCV candles against OKX V5 history-candles."""
import argparse
import csv
import hashlib
import json
import math
import random
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SYMBOLS = {
    "BTC": "BTC-USDT-SWAP",
    "ETH": "ETH-USDT-SWAP",
    "SOL": "SOL-USDT-SWAP",
    "DOGE": "DOGE-USDT-SWAP",
    "AVAX": "AVAX-USDT-SWAP",
}
BASE_URL = "https://www.okx.com/api/v5/market/history-candles"


def _sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def select_samples(rows, sample_per_class=3, seed=20261128):
    """Reservoir-sample exact and changed opens, plus the largest adjacent jump."""
    rng = random.Random(seed)
    selected = {"exact": [], "changed": []}
    seen_counts = {"exact": 0, "changed": 0}
    previous = None
    max_jump = None

    for raw in rows:
        row = {
            "ts": int(raw["ts"]),
            "open": float(raw["open"]),
            "high": float(raw["high"]),
            "low": float(raw["low"]),
            "close": float(raw["close"]),
            "vol": float(raw["vol"]),
        }
        if previous is not None and row["ts"] - previous["ts"] == 60_000:
            kind = "exact" if row["open"] == previous["close"] else "changed"
            sample = {
                "classification": kind,
                "previous_timestamp_ms": previous["ts"],
                "previous_close": previous["close"],
                "candle": row,
            }
            seen_counts[kind] += 1
            if len(selected[kind]) < sample_per_class:
                selected[kind].append(sample)
            else:
                slot = rng.randrange(seen_counts[kind])
                if slot < sample_per_class:
                    selected[kind][slot] = sample

            jump_bps = abs(row["open"] / previous["close"] - 1.0) * 10_000.0
            if max_jump is None or jump_bps > max_jump["jump_bps"]:
                max_jump = {**sample, "jump_bps": jump_bps}
        previous = row

    combined = selected["exact"] + selected["changed"]
    if max_jump is not None:
        max_jump = {**max_jump, "classification": "largest_absolute_adjacent_open_jump"}
        combined.append(max_jump)

    deduplicated = []
    seen_timestamps = set()
    for item in combined:
        ts = item["candle"]["ts"]
        if ts not in seen_timestamps:
            deduplicated.append(item)
            seen_timestamps.add(ts)
    return {
        "transition_counts": seen_counts,
        "samples": deduplicated,
        "largest_adjacent_jump_bps": max_jump["jump_bps"] if max_jump else None,
    }


def _fetch_okx_candle(inst_id, timestamp_ms, timeout=20):
    params = urlencode({
        "instId": inst_id,
        "bar": "1m",
        "after": str(timestamp_ms + 60_000),
        "limit": "5",
    })
    request = Request(
        BASE_URL + "?" + params,
        headers={"User-Agent": "okxtester-readonly-source-audit/1.0"},
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("code") != "0":
        raise RuntimeError(f"OKX API returned code={payload.get('code')} msg={payload.get('msg')}")
    for item in payload.get("data", []):
        if int(item[0]) == int(timestamp_ms):
            return item
    return None


def _close(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-10, abs_tol=1e-12)


def compare_candle(csv_row, api_row):
    if api_row is None:
        return {"timestamp_found": False, "ohlc_match": False, "volume_match": False}
    comparisons = {
        "open": _close(csv_row["open"], api_row[1]),
        "high": _close(csv_row["high"], api_row[2]),
        "low": _close(csv_row["low"], api_row[3]),
        "close": _close(csv_row["close"], api_row[4]),
    }
    return {
        "timestamp_found": True,
        "ohlc_match": all(comparisons.values()),
        "ohlc_fields_match": comparisons,
        "volume_match": _close(csv_row["vol"], api_row[5]),
        "okx_volume_unit_note": "OKX V5 vol is contracts for derivatives; confirm the CSV uses the same unit.",
    }


def audit_symbol(data_dir, symbol, sample_per_class, delay_seconds):
    path = data_dir / f"{symbol}_USDT_USDT_1m.csv"
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"ts", "open", "high", "low", "close", "vol"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{symbol}: missing required columns {sorted(required - set(reader.fieldnames or []))}")
        selection = select_samples(reader, sample_per_class, seed=20261128 + len(symbol))

    checks = []
    errors = []
    for sample in selection["samples"]:
        candle = sample["candle"]
        try:
            api_row = _fetch_okx_candle(SYMBOLS[symbol], candle["ts"])
            comparison = compare_candle(candle, api_row)
            checks.append({
                "classification": sample["classification"],
                "timestamp_ms": candle["ts"],
                "previous_timestamp_ms": sample["previous_timestamp_ms"],
                "previous_close": sample["previous_close"],
                "repository_candle": candle,
                "comparison": comparison,
            })
        except Exception as exc:
            errors.append({"timestamp_ms": candle["ts"], "error": str(exc)})
            checks.append({
                "classification": sample["classification"],
                "timestamp_ms": candle["ts"],
                "comparison": {"timestamp_found": False, "ohlc_match": False, "volume_match": False},
            })
        time.sleep(delay_seconds)

    found = [item for item in checks if item["comparison"]["timestamp_found"]]
    ohlc_matches = sum(item["comparison"]["ohlc_match"] for item in found)
    volume_matches = sum(item["comparison"]["volume_match"] for item in found)
    if errors or len(found) != len(checks):
        status = "API_UNAVAILABLE_OR_INCOMPLETE"
    elif ohlc_matches == len(checks):
        status = "OKX_SAMPLE_OHLC_MATCH"
    else:
        status = "OKX_SAMPLE_OHLC_MISMATCH"

    return {
        "symbol": symbol,
        "candidate_okx_instrument_id": SYMBOLS[symbol],
        "source_file": path.name,
        "source_sha256": _sha256(path),
        "transition_counts": selection["transition_counts"],
        "sample_count": len(checks),
        "ohlc_matches": ohlc_matches,
        "volume_matches": volume_matches,
        "status": status,
        "largest_adjacent_jump_bps": selection["largest_adjacent_jump_bps"],
        "checks": checks,
        "errors": errors,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compare deterministic OHLCV samples against the public OKX V5 historical candles endpoint."
    )
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data" / "market_1m")
    parser.add_argument("--output", type=Path, default=Path("reports/g0_07_okx_source_sample_verification_v1.json"))
    parser.add_argument("--symbols", default="BTC,ETH,SOL,DOGE,AVAX")
    parser.add_argument("--samples-per-class", type=int, default=3)
    parser.add_argument("--delay-seconds", type=float, default=0.12)
    args = parser.parse_args(argv)
    if args.samples_per_class < 1 or args.delay_seconds < 0.1:
        parser.error("samples-per-class must be >=1 and delay-seconds must be >=0.1")

    symbols = [item.strip().upper() for item in args.symbols.split(",") if item.strip()]
    assets = [audit_symbol(args.data_dir, symbol, args.samples_per_class, args.delay_seconds) for symbol in symbols]
    statuses = [asset["status"] for asset in assets]
    if any(status == "API_UNAVAILABLE_OR_INCOMPLETE" for status in statuses):
        overall = "UNVERIFIED_API_UNAVAILABLE_OR_INCOMPLETE"
    elif all(status == "OKX_SAMPLE_OHLC_MATCH" for status in statuses):
        overall = "OKX_SAMPLE_OHLC_MATCH_NOT_FULL_PROVENANCE"
    else:
        overall = "OKX_SAMPLE_OHLC_MISMATCH"

    report = {
        "audit_id": "G0-07_OKX_PUBLIC_CANDLE_SOURCE_SAMPLE_VERIFICATION_V1",
        "overall_status": overall,
        "scope": "Read-only deterministic sample comparison of repository 1m OHLCV candles with the public OKX V5 history-candles endpoint. This is a sample check, not full-dataset provenance certification.",
        "endpoint": BASE_URL,
        "selection": "Reservoir sample of exact-open-match and changed-open transitions plus the largest adjacent open jump per asset.",
        "assets": assets,
        "interpretation": {
            "OKX_SAMPLE_OHLC_MATCH_NOT_FULL_PROVENANCE": "All sampled OHLC values match OKX for the candidate instrument IDs. This supports, but does not prove, full-dataset source provenance or the absence of transformations.",
            "OKX_SAMPLE_OHLC_MISMATCH": "At least one sampled OHLC candle differs from OKX; investigate instrument mapping, timestamp convention, data provider, or transformations.",
            "UNVERIFIED_API_UNAVAILABLE_OR_INCOMPLETE": "The public API did not provide all requested timestamps or a request failed; no source conclusion can be drawn.",
            "volume": "Volume is compared separately because derivative volume units must be confirmed; OKX documents vol in contracts for derivatives.",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("G0-07 OKX SOURCE SAMPLE VERIFICATION")
    print(f"Overall: {overall}")
    for asset in assets:
        print(f"{asset['symbol']}: {asset['status']}, OHLC matches={asset['ohlc_matches']}/{asset['sample_count']}, volume matches={asset['volume_matches']}/{asset['sample_count']}, API errors={len(asset['errors'])}")
    print(f"JSON report: {args.output}")


if __name__ == "__main__":
    main()
