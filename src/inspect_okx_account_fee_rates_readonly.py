#!/usr/bin/env python3
"""Read-only OKX account fee-rate probe; run locally with a dedicated read-only API key.

Calls only GET /api/v5/public/time and GET /api/v5/account/trade-fee.
Never places, amends, or cancels orders and never prints or writes credentials.
"""
import argparse
import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://www.okx.com"
ASSETS = ("BTC", "ETH", "SOL", "DOGE", "AVAX")
FEE_GROUP_ID = "4"
USER_AGENT = "okxtester-g0-08-readonly-fee-audit/1.0"


def _decimal(value, field):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field} is not a valid decimal: {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def timestamp_from_server_ms(value):
    try:
        milliseconds = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid OKX server timestamp") from exc
    return datetime.fromtimestamp(
        milliseconds / 1000, timezone.utc
    ).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def build_signature(timestamp, method, request_path, body, secret):
    prehash = f"{timestamp}{method.upper()}{request_path}{body}"
    digest = hmac.new(
        secret.encode("utf-8"), prehash.encode("utf-8"), hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode("ascii")


def build_request_path(endpoint, params):
    query = urlencode(params)
    return endpoint + (f"?{query}" if query else "")


def parse_fee_payload(asset, payload, expected_group_id=FEE_GROUP_ID):
    if not isinstance(payload, dict) or payload.get("code") != "0":
        code = payload.get("code") if isinstance(payload, dict) else None
        message = payload.get("msg") if isinstance(payload, dict) else None
        raise ValueError(f"{asset}: fee endpoint failed: code={code} msg={message}")
    rows = payload.get("data")
    if not isinstance(rows, list) or len(rows) != 1:
        raise ValueError(
            f"{asset}: expected exactly one fee response row, got "
            f"{len(rows) if isinstance(rows, list) else 'non-list'}"
        )
    row = rows[0]
    level = row.get("level")
    if not isinstance(level, str) or not level:
        raise ValueError(f"{asset}: account fee level is missing")
    groups = row.get("feeGroup")
    if not isinstance(groups, list):
        raise ValueError(f"{asset}: feeGroup must be a list")
    matching = [
        group for group in groups
        if isinstance(group, dict) and str(group.get("groupId")) == expected_group_id
    ]
    if len(matching) != 1:
        raise ValueError(
            f"{asset}: expected exactly one fee group {expected_group_id}, "
            f"got {len(matching)}"
        )
    group = matching[0]
    maker_raw = _decimal(group.get("maker"), "maker")
    taker_raw = _decimal(group.get("taker"), "taker")
    # OKX documents negative rates as commission and positive rates as rebates.
    # The engine expects nonnegative costs; do not count rebates as negative costs.
    maker_cost = max(Decimal(0), -maker_raw)
    taker_cost = max(Decimal(0), -taker_raw)
    return {
        "asset": asset,
        "inst_type": row.get("instType", "SWAP"),
        "inst_family": f"{asset}-USDT",
        "account_fee_level": level,
        "fee_group_id": expected_group_id,
        "maker_rate_raw": str(maker_raw),
        "taker_rate_raw": str(taker_raw),
        "maker_commission_cost_rate": str(maker_cost),
        "taker_commission_cost_rate": str(taker_cost),
        "response_timestamp_ms": row.get("ts", ""),
    }


def _http_json(url, headers=None, timeout=20):
    request = Request(
        url, headers={"User-Agent": USER_AGENT, **(headers or {})}, method="GET"
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("OKX returned a non-object JSON response")
    return payload


def get_server_time_ms(timeout=20):
    payload = _http_json(f"{BASE_URL}/api/v5/public/time", timeout=timeout)
    if payload.get("code") != "0":
        raise RuntimeError(
            f"OKX public time error: {payload.get('code')} {payload.get('msg')}"
        )
    rows = payload.get("data")
    if not isinstance(rows, list) or len(rows) != 1 or "ts" not in rows[0]:
        raise ValueError("OKX public time response is malformed")
    return int(rows[0]["ts"])


def fetch_account_fee(asset, api_key, secret, passphrase, timeout=20):
    endpoint = "/api/v5/account/trade-fee"
    params = {"instType": "SWAP", "instFamily": f"{asset}-USDT"}
    request_path = build_request_path(endpoint, params)
    timestamp = timestamp_from_server_ms(get_server_time_ms(timeout=timeout))
    signature = build_signature(timestamp, "GET", request_path, "", secret)
    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json",
    }
    payload = _http_json(BASE_URL + request_path, headers=headers, timeout=timeout)
    return parse_fee_payload(asset, payload)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=Path("reports/g0_08_account_fee_rates_local_v1.json"),
    )
    args = parser.parse_args(argv)
    env_names = ("OKX_API_KEY", "OKX_API_SECRET", "OKX_API_PASSPHRASE")
    missing = [name for name in env_names if not os.environ.get(name)]
    if missing:
        parser.error(
            "Missing environment variables: " + ", ".join(missing)
            + ". Use a dedicated OKX API key with Read permission only; "
              "do not paste credentials into chat."
        )
    api_key = os.environ["OKX_API_KEY"]
    secret = os.environ["OKX_API_SECRET"]
    passphrase = os.environ["OKX_API_PASSPHRASE"]
    results, errors = [], {}
    for asset in ASSETS:
        try:
            results.append(fetch_account_fee(asset, api_key, secret, passphrase))
        except Exception as exc:
            # Never include request headers, credentials, or signature material.
            errors[asset] = f"{type(exc).__name__}: {exc}"
    report = {
        "audit_id": "G0-08_OKX_ACCOUNT_FEE_RATES_READONLY_V1",
        "status": (
            "ACCOUNT_FEE_RATE_SNAPSHOT_PASS"
            if len(results) == len(ASSETS) and not errors
            else "ACCOUNT_FEE_RATE_SNAPSHOT_INCOMPLETE"
        ),
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_endpoint": "GET /api/v5/account/trade-fee",
        "authentication": "authenticated read-only request",
        "required_api_key_permission": "Read only; no Trade or Withdraw permission",
        "credentials_written_or_printed": False,
        "fee_group_id": FEE_GROUP_ID,
        "assets": results,
        "errors": errors,
        "interpretation": {
            "raw_rate_sign": "Negative rates are commission; positive rates are rebates.",
            "cost_rate": "Commission cost is max(0, -raw_rate); rebates are not credited as negative costs.",
            "scope": "Current account fee rates only; does not establish historical fee tiers.",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G0-08 READ-ONLY ACCOUNT FEE RATE PROBE")
    print(f"Status: {report['status']}")
    for row in results:
        print(
            f"{row['asset']}: level={row['account_fee_level']} "
            f"maker_cost={row['maker_commission_cost_rate']} "
            f"taker_cost={row['taker_commission_cost_rate']} "
            f"groupId={row['fee_group_id']}"
        )
    if errors:
        print("Errors: " + json.dumps(errors, sort_keys=True))
    print(f"Local report: {args.output}")
    print("Credentials were not printed or written to the report.")
    if report["status"] != "ACCOUNT_FEE_RATE_SNAPSHOT_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
