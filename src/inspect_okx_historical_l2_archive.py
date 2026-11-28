"""Inspect one public OKX historical L2 archive without retaining the archive.

Downloads only the BTC-USDT-SWAP 5,000-level archive for 2025-11-01,
inspects the tar member names and a tiny prefix of the first regular member,
then deletes the temporary archive. No credentials are used.
"""
import argparse
import csv
import hashlib
import io
import json
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://www.okx.com"
API_PATH = "/api/v5/public/market-data-history"
SAMPLE_DAY = "2025-11-01"
SAMPLE_FAMILY = "BTC-USDT"
SAMPLE_MODULE = "5"


def _first_member_preview(archive_path):
    with tarfile.open(archive_path, mode="r:gz") as archive:
        members = [m for m in archive.getmembers() if m.isfile()]
        if not members:
            raise ValueError("Archive contains no regular files")
        member = members[0]
        handle = archive.extractfile(member)
        if handle is None:
            raise ValueError("Unable to read first archive member")
        raw_lines = []
        for _ in range(5):
            line = handle.readline()
            if not line:
                break
            raw_lines.append(line.decode("utf-8", errors="replace").rstrip("\r\n")[:500])
        if not raw_lines:
            raise ValueError("First archive member is empty")
        parsed = list(csv.reader(io.StringIO("\n".join(raw_lines))))
        return {
            "member_count": len(members),
            "first_member_name": member.name,
            "first_member_size_bytes": member.size,
            "preview_lines": raw_lines,
            "preview_field_counts": [len(row) for row in parsed],
        }


def fetch_archive_url():
    stamp = str(int(datetime.strptime(SAMPLE_DAY, "%Y-%m-%d")
                   .replace(tzinfo=timezone.utc).timestamp() * 1000))
    params = {
        "module": SAMPLE_MODULE,
        "instType": "SWAP",
        "instFamilyList": SAMPLE_FAMILY,
        "dateAggrType": "daily",
        "begin": stamp,
        "end": stamp,
    }
    url = BASE_URL + API_PATH + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": "okxtester-g0-07-l2-archive-inspector/1.0"})
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if str(payload.get("code")) != "0":
        raise ValueError("OKX historical-data API returned a nonzero code")
    for block in payload.get("data", []):
        for detail in block.get("details", []):
            if detail.get("instFamily") != SAMPLE_FAMILY:
                continue
            for item in detail.get("groupDetails", []):
                if SAMPLE_DAY in item.get("filename", "") and item.get("url", "").startswith("https://"):
                    return item["url"], item
    raise ValueError("Expected BTC 5000-level archive is not available")


def inspect_download(url, metadata):
    digest = hashlib.sha256()
    size = 0
    with tempfile.NamedTemporaryFile(prefix="okx_l2_probe_", suffix=".tar.gz") as tmp:
        request = Request(url, headers={"User-Agent": "okxtester-g0-07-l2-archive-inspector/1.0"})
        with urlopen(request, timeout=120) as response:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                tmp.write(chunk)
                digest.update(chunk)
                size += len(chunk)
        tmp.flush()
        preview = _first_member_preview(tmp.name)
    return {
        "filename": metadata["filename"],
        "advertised_size_mb": metadata.get("sizeMB"),
        "downloaded_size_bytes": size,
        "downloaded_sha256": digest.hexdigest(),
        "archive_format": "tar.gz",
        **preview,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("reports/g0_07_historical_l2_archive_format_v1.json"))
    args = parser.parse_args(argv)
    url, metadata = fetch_archive_url()
    result = inspect_download(url, metadata)
    report = {
        "audit_id": "G0-07_OKX_HISTORICAL_L2_ARCHIVE_FORMAT_V1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "instrument_family": SAMPLE_FAMILY,
        "date_utc": SAMPLE_DAY,
        "module": SAMPLE_MODULE,
        "module_description": "5000-level orderbook",
        "downloaded_archive_retained": False,
        "result": result,
        "limitations": [
            "One BTC instrument/day archive only; not evidence of full-period or all-asset integrity.",
            "A short member prefix is inspected; full row count, timestamp continuity and sequence integrity remain unverified.",
            "L2 depth does not establish queue priority, hidden liquidity, latency or guaranteed executable fills.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("G0-07 HISTORICAL L2 ARCHIVE FORMAT INSPECTION")
    print(f"Archive: {result['filename']}")
    print(f"Downloaded: {result['downloaded_size_bytes']} bytes")
    print(f"SHA-256: {result['downloaded_sha256']}")
    print(f"Members: {result['member_count']}")
    print(f"First member: {result['first_member_name']}")
    print(f"Sample field counts: {result['preview_field_counts']}")
    print("Archive retained: no")
    print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
