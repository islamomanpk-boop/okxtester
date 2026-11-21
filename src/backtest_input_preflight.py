import csv
import math
from datetime import datetime
from pathlib import Path

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]

SIGNAL_DIR = Path.home() / "okx_adaptive_bot/reports/price_action_signals"
EXEC_DIR = Path.home() / "okx_scalping_data"
FUNDING_DIR = EXEC_DIR / "funding_rates/processed"
REPORT = Path("reports/backtest_input_preflight.md")


def timestamp_ms(value):
    value = value.strip()
    try:
        return int(value)
    except ValueError:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError("Timestamp has no timezone")
        return int(dt.timestamp() * 1000)


def inspect_file(path, required, asset, kind):
    issues = []

    if not path.exists():
        return None, [f"Missing file: {path}"]

    count = 0
    first = last = previous = None

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        missing = set(required) - set(reader.fieldnames or [])
        if missing:
            return None, [
                f"{path.name}: missing columns {sorted(missing)}"
            ]

        for row in reader:
            count += 1

            try:
                if kind == "funding":
                    ts = timestamp_ms(row["funding_time"])
                else:
                    ts = timestamp_ms(row["ts"])

                if previous is not None and ts <= previous:
                    issues.append(
                        f"{path.name}: timestamp not increasing at row {count}"
                    )
                    break

                if first is None:
                    first = ts
                last = ts
                previous = ts

                if kind == "signal":
                    available = timestamp_ms(row["signal_available_at"])
                    if available != ts + 900000:
                        issues.append(
                            f"{path.name}: availability is not exactly "
                            f"15 minutes after signal at row {count}"
                        )
                        break

                elif kind == "execution":
                    for col in ("open", "high", "low", "close", "vol"):
                        value = float(row[col])
                        if not math.isfinite(value):
                            raise ValueError(f"Invalid {col}")

                elif kind == "funding":
                    rate = float(row["funding_rate"])
                    if not math.isfinite(rate) or abs(rate) > 1:
                        raise ValueError("Invalid funding rate")

                    expected = f"{asset}-USDT-SWAP"
                    if row["instrument_name"] != expected:
                        raise ValueError(
                            f"Expected {expected}, got {row['instrument_name']}"
                        )

            except Exception as exc:
                issues.append(
                    f"{path.name}: invalid data at row {count}: {exc}"
                )
                break

    if count == 0:
        issues.append(f"{path.name}: file is empty")

    return {
        "rows": count,
        "first": first,
        "last": last,
    }, issues


def main():
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    all_issues = []
    results = []

    print("Starting corrected input preflight...", flush=True)

    for asset in ASSETS:
        print(f"Checking {asset}...", flush=True)

        signal, errors = inspect_file(
            SIGNAL_DIR / f"{asset}_15m_price_action_signals.csv",
            ["ts", "signal_available_at"],
            asset,
            "signal",
        )
        all_issues.extend(errors)

        execution, errors = inspect_file(
            EXEC_DIR / f"{asset}_USDT_USDT_1m.csv",
            ["ts", "open", "high", "low", "close", "vol"],
            asset,
            "execution",
        )
        all_issues.extend(errors)

        funding, errors = inspect_file(
            FUNDING_DIR / f"{asset}_USDT_SWAP_funding_rates.csv",
            ["instrument_name", "funding_rate", "funding_time"],
            asset,
            "funding",
        )
        all_issues.extend(errors)

        if signal and execution and funding:
            if execution["rows"] > 1:
                expected_span = (execution["rows"] - 1) * 60000
                actual_span = execution["last"] - execution["first"]

                if actual_span != expected_span:
                    all_issues.append(
                        f"{asset}: missing or irregular 1-minute candles"
                    )

            results.append((asset, signal, execution, funding))

    common_start = None
    common_end = None

    if len(results) == len(ASSETS):
        common_start = max(r[2]["first"] for r in results)
        common_end = min(r[2]["last"] for r in results)

        if common_start > common_end:
            all_issues.append("No common execution time window.")
        else:
            print(
                "Common execution window:",
                common_start,
                "to",
                common_end,
                flush=True,
            )

    lines = [
        "# Backtest Input Preflight",
        "",
        "Sequential CSV validation.",
        "Raw market and funding files remain local.",
        "",
    ]

    for asset, signal, execution, funding in results:
        lines.extend([
            f"## {asset}",
            f"- Signal rows: {signal['rows']}",
            f"- Execution rows: {execution['rows']}",
            f"- Execution first: {execution['first']}",
            f"- Execution last: {execution['last']}",
            f"- Funding rows: {funding['rows']}",
            f"- Funding first: {funding['first']}",
            f"- Funding last: {funding['last']}",
            "",
        ])

    lines.extend([
        "## Shared execution window",
        f"- Start: {common_start}",
        f"- End: {common_end}",
        "",
        "## Issues",
        "",
        *(all_issues or ["None detected."]),
        "",
        f"## Result: {'PASS' if not all_issues else 'FAIL'}",
        "",
    ])

    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("\n===== PREFLIGHT RESULT =====")
    print("Issues:", len(all_issues))
    print("Report:", REPORT)
    print("Result:", "PASS" if not all_issues else "FAIL")

    if all_issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
