#!/usr/bin/env python3
"""Read-only current OKX SWAP instrument metadata snapshot for G0-08.

Uses public endpoints only. No credentials, private account endpoints, orders,
trades, fills, or strategy calculations are used.
"""
import argparse
import hashlib
import json
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://www.okx.com/api/v5"
ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
USER_AGENT = "okxtester-g0-08-public-instrument-audit/1.0"
POSITIVE_DECIMAL_FIELDS = ("ctVal", "tickSz", "lotSz", "minSz")


def _decimal(value, field):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field} is not a valid decimal: {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def validate_instrument(asset, record):
    """Validate one current USDT-linear perpetual instrument record."""
    if not isinstance(record, dict):
        raise ValueError(f"{asset}: instrument record must be an object")

    expected = {
        "instId": f"{asset}-USDT-SWAP",
        "instType": "SWAP",
        "ctType": "linear",
        "ctValCcy": asset,
        "settleCcy": "USDT",
        "state": "live",
    }
    for field, value in expected.items():
        if record.get(field) != value:
            raise ValueError(
                f"{asset}: expected {field}={value!r}, got {record.get(field)!r}"
            )

    for field in ("ctVal", "tickSz", "lotSz", "minSz", "groupId", "listTime"):
        value = record.get(field)
        if value is None or str(value).strip() == "":
            raise ValueError(f"{asset}: required instrument field {field} is empty")

    numeric = {}
    for field in POSITIVE_DECIMAL_FIELDS:
        numeric[field] = _decimal(record[field], field)
        if numeric[field] <= 0:
            raise ValueError(f"{asset}: {field} must be positive")

    lot_units = numeric["minSz"] / numeric["lotSz"]
    if lot_units != lot_units.to_integral_value():
        raise ValueError(
            f"{asset}: minSz must be an integer multiple of lotSz"
        )

    ct_mult = record.get("ctMult")
    if ct_mult not in (None, ""):
        multiplier = _decimal(ct_mult, "ctMult")
        if multiplier <= 0:
            raise ValueError(f"{asset}: ctMult must be positive when supplied")

    upcoming = record.get("upcChg")
    if not isinstance(upcoming, list):
        raise ValueError(f"{asset}: upcChg must be a list")

    for change in upcoming:
        if not isinstance(change, dict):
            raise ValueError(f"{asset}: malformed upcoming change")
        if not all(key in change for key in ("param", "newValue", "effTime")):
            raise ValueError(f"{asset}: upcoming change missing required fields")

    return {
        "asset": asset,
        "inst_id": record["instId"],
        "status": "PASS",
        "contract_type": record["ctType"],
        "contract_value": record["ctVal"],
        "contract_value_currency": record["ctValCcy"],
        "contract_multiplier": record.get("ctMult", ""),
        "settlement_currency": record["settleCcy"],
        "tick_size": record["tickSz"],
        "lot_size_contracts": record["lotSz"],
        "minimum_order_size_contracts": record["minSz"],
        "maximum_market_size_contracts": record.get("maxMktSz", ""),
        "maximum_stop_size_contracts": record.get("maxStopSz", ""),
        "maximum_trigger_size_contracts": record.get("maxTriggerSz", ""),
        "instrument_fee_group_id": record["groupId"],
        "state": record["state"],
        "list_time_ms": record["listTime"],
        "expiry_time_ms": record.get("expTime", ""),
        "upcoming_changes": upcoming,
        "raw_record": record,
    }


def validate_payload(asset, payload):
    if not isinstance(payload, dict) or payload.get("code") != "0":
        code = payload.get("code") if isinstance(payload, dict) else None
        message = payload.get("msg") if isinstance(payload, dict) else None
        raise ValueError(f"{asset}: OKX API response not successful: {code} {message}")
    rows = payload.get("data")
    if not isinstance(rows, list) or len(rows) != 1:
        raise ValueError(
            f"{asset}: expected exactly one instrument record, got "
            f"{len(rows) if isinstance(rows, list) else 'non-list'}"
        )
    return validate_instrument(asset, rows[0])


def request_json(endpoint, params=None, timeout=20):
    query = urlencode(params or {})
    url = f"{API_BASE}{endpoint}" + (f"?{query}" if query else "")
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict) or payload.get("code") != "0":
        raise RuntimeError(
            f"OKX API error for {endpoint}: "
            f"code={payload.get('code') if isinstance(payload, dict) else None} "
            f"msg={payload.get('msg') if isinstance(payload, dict) else None}"
        )
    return payload


def get_server_time():
    payload = request_json("/public/time")
    rows = payload.get("data")
    if not isinstance(rows, list) or len(rows) != 1 or "ts" not in rows[0]:
        raise ValueError("OKX public time endpoint returned an invalid payload")
    return int(rows[0]["ts"])


def build_report(pulled_at_start_ms, pulled_at_end_ms, results, errors):
    passed = len(results) == len(ASSETS) and not errors
    raw_records = {
        asset: results[asset]["raw_record"]
        for asset in ASSETS if asset in results
    }
    canonical = json.dumps(
        raw_records, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return {
        "audit_id": "G0-08_OKX_PUBLIC_INSTRUMENT_METADATA_SNAPSHOT_V1",
        "status": (
            "OKX_PUBLIC_INSTRUMENT_METADATA_SNAPSHOT_PASS_CURRENT_ONLY"
            if passed else "OKX_PUBLIC_INSTRUMENT_METADATA_SNAPSHOT_FAIL_CLOSED"
        ),
        "source": {
            "endpoint": "GET /api/v5/public/instruments",
            "instrument_type": "SWAP",
            "instrument_ids": [f"{asset}-USDT-SWAP" for asset in ASSETS],
            "authentication": "public endpoint; no credentials used",
            "raw_metadata_sha256": hashlib.sha256(canonical).hexdigest(),
        },
        "capture": {
            "server_time_start_ms": pulled_at_start_ms,
            "server_time_end_ms": pulled_at_end_ms,
        },
        "assets": [results[asset] for asset in ASSETS if asset in results],
        "errors": errors,
        "historical_metadata": {
            "status": "NOT_VERIFIED_CURRENT_SNAPSHOT_ONLY",
            "note": (
                "This endpoint supplies current instrument settings and upcoming "
                "changes; it does not establish historical tick/lot/contract-value "
                "settings over the research dataset."
            ),
        },
        "account_fee_tier": {
            "status": "NOT_FETCHED_AUTHENTICATED_ACCOUNT_ENDPOINT_REQUIRED",
            "endpoint": "GET /api/v5/account/trade-fee",
            "note": (
                "The public instrument fee-group ID is not the user's account fee "
                "tier or actual taker rate. No account credentials were used."
            ),
        },
        "scope": [
            "Current public instrument metadata only",
            "Linear USDT-margined perpetual contract assumptions",
            "Tick, lot, minimum size, contract value, multiplier and settlement currency",
            "Upcoming parameter changes returned by the public endpoint",
            "No private account data, orders, trades, fills or strategy calculations",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=Path("reports/g0_08_public_instrument_metadata_v1.json"),
    )
    parser.add_argument("--pause-seconds", type=float, default=0.12)
    args = parser.parse_args(argv)
    if args.pause_seconds < 0.1:
        parser.error("--pause-seconds must be at least 0.1")

    start_ms = get_server_time()
    results = {}
    errors = {}
    for asset in ASSETS:
        try:
            payload = request_json(
                "/public/instruments",
                {"instType": "SWAP", "instId": f"{asset}-USDT-SWAP"},
            )
            results[asset] = validate_payload(asset, payload)
        except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError) as exc:
            errors[asset] = f"{type(exc).__name__}: {exc}"
        time.sleep(args.pause_seconds)
    end_ms = get_server_time()

    report = build_report(start_ms, end_ms, results, errors)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("G0-08 OKX PUBLIC INSTRUMENT METADATA SNAPSHOT")
    print(f"Status: {report['status']}")
    for item in report["assets"]:
        print(
            f"{item['asset']}: ctVal={item['contract_value']} "
            f"{item['contract_value_currency']} ctMult={item['contract_multiplier']} "
            f"tickSz={item['tick_size']} lotSz={item['lot_size_contracts']} "
            f"minSz={item['minimum_order_size_contracts']} "
            f"groupId={item['instrument_fee_group_id']} state={item['state']}"
        )
        if item["upcoming_changes"]:
            print(f"  upcoming_changes={item['upcoming_changes']}")
    if errors:
        print(f"Errors: {json.dumps(errors, sort_keys=True)}")
    print("Historical metadata: NOT VERIFIED")
    print("Account-specific fee tier: NOT FETCHED")
    print(f"JSON report: {args.output}")
    if not report["status"].endswith("PASS_CURRENT_ONLY"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
