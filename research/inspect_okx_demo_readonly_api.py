#!/usr/bin/env python3
"""Read-only OKX demo API smoke test for funding-bill field availability.

This script NEVER places orders, transfers funds, changes settings, or writes API
responses to disk. It only calls GET /account/config and GET /account/bills.
Credentials are prompted with getpass and are never printed.
"""
from __future__ import annotations

import base64
import getpass
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_BASE = "https://www.okx.com"
TIMEOUT_SECONDS = 20
FUNDING_SUBTYPES = {"173", "174"}
RELEVANT_FIELDS = (
    "instId", "instType", "subType", "ts", "px", "sz", "pnl",
    "balChg", "posBalChg", "ccy", "mgnMode",
)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def make_signature(timestamp: str, method: str, request_path: str, secret: str) -> str:
    prehash = f"{timestamp}{method.upper()}{request_path}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), prehash, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")


def get_json(base: str, path: str, params: dict[str, str],
             api_key: str, secret: str, passphrase: str) -> dict:
    query = urlencode(params)
    request_path = f"{path}?{query}" if query else path
    timestamp = utc_timestamp()
    headers = {
        "Accept": "application/json",
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": make_signature(timestamp, "GET", request_path, secret),
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase,
        "x-simulated-trading": "1",
    }
    req = Request(f"{base.rstrip('/')}{request_path}", headers=headers, method="GET")
    try:
        with urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as exc:
        # Do not print request headers, credentials, or raw response bodies.
        raise RuntimeError(f"HTTP request failed with status {exc.code}") from None
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from None

    try:
        result = json.loads(payload)
    except json.JSONDecodeError:
        raise RuntimeError("Exchange returned a non-JSON response") from None
    if not isinstance(result, dict):
        raise RuntimeError("Unexpected response structure")
    return result


def require_ok(result: dict, label: str) -> list:
    code = str(result.get("code", ""))
    if code != "0":
        msg = str(result.get("msg", ""))
        # Exchange error messages are safe to show; never echo request headers.
        raise RuntimeError(f"{label} rejected: code={code}, message={msg[:240]}")
    data = result.get("data", [])
    if not isinstance(data, list):
        raise RuntimeError(f"{label} returned an unexpected data field")
    return data


def main() -> int:
    print("OKX DEMO API — READ-ONLY SMOKE TEST")
    print("Only GET account endpoints are called. No orders or account changes.")
    print("Credentials are entered locally and are not displayed or saved.\n")

    api_key = getpass.getpass("Demo API key: ").strip()
    secret = getpass.getpass("Demo API secret: ").strip()
    passphrase = getpass.getpass("Demo API passphrase: ").strip()
    if not all((api_key, secret, passphrase)):
        print("ERROR: all three credential fields are required.")
        return 2

    base = os.environ.get("OKX_API_BASE", DEFAULT_BASE).strip()
    if not base.startswith("https://"):
        print("ERROR: OKX_API_BASE must begin with https://")
        return 2

    try:
        config = get_json(base, "/api/v5/account/config", {}, api_key, secret, passphrase)
        config_rows = require_ok(config, "Account configuration")
        print("Authentication and account/config: PASS")

        bills = get_json(
            base,
            "/api/v5/account/bills",
            {"instType": "SWAP", "limit": "100"},
            api_key,
            secret,
            passphrase,
        )
        bill_rows = require_ok(bills, "Account bills (last 7 days)")
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        print("No credentials or response records were printed.")
        return 1

    funding_rows = [row for row in bill_rows if str(row.get("subType", "")) in FUNDING_SUBTYPES]
    print(f"Account configuration rows: {len(config_rows)}")
    print(f"SWAP bill rows returned (last 7 days, max 100): {len(bill_rows)}")
    print(f"Funding subtype rows (173/174): {len(funding_rows)}")

    if funding_rows:
        print("Funding-field presence (counts of non-empty values):")
        for field in RELEVANT_FIELDS:
            present = sum(1 for row in funding_rows if str(row.get(field, "")).strip())
            print(f"  {field}: {present}/{len(funding_rows)}")
    else:
        print("No demo funding bill rows were returned in this page.")
        print("This is not a failure of authentication and does not validate production bills.")

    print("\nRESULT: demo API integration test completed.")
    print("SCOPE LIMIT: demo records cannot validate real-account settlement marks.")
    print("No response records or credentials were written to disk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
