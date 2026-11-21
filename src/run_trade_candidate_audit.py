from pathlib import Path
import os
import time

import numpy as np
import pandas as pd

from trade_candidate_engine import build_candidates

ASSETS = ["BTC", "ETH", "SOL", "DOGE", "AVAX"]
DATA_DIR = Path(
    "~/okx_adaptive_bot/reports/price_action_signals"
).expanduser()

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

lines = [
    "# Trade Candidate Engine V1 — Five-Asset Audit",
    "",
    "Sequential audit of the five 15-minute price-action datasets.",
    "",
]

total_rows = 0
total_candidates = 0
all_passed = True

for asset in ASSETS:
    path = DATA_DIR / f"{asset}_15m_price_action_signals.csv"

    print(f"\n===== {asset} =====")
    started = time.perf_counter()

    df = pd.read_csv(path)
    candidates = build_candidates(df, asset=asset)
    elapsed = time.perf_counter() - started

    result = pd.DataFrame(candidates)

    rows = len(df)
    count = len(result)
    total_rows += rows
    total_candidates += count

    if count:
        duplicate_count = int(result["signal_ts"].duplicated().sum())
        timing_ok = bool(
            (
                result["signal_available_at"]
                - result["signal_ts"]
                == 900000
            ).all()
        )
        stops_ok = bool(
            np.isfinite(result["stop_reference_price"]).all()
        )
        distances_ok = bool(
            (
                np.isfinite(result["stop_distance_atr"])
                & (result["stop_distance_atr"] > 0)
            ).all()
        )
        asset_ok = bool((result["asset"] == asset).all())
        priority_ok = bool(
            result["signal_priority"].isin([1, 2, 3]).all()
        )
        side_ok = bool(result["side"].isin([1, -1]).all())
        family_ok = bool(
            (result["strategy_family"] == "MODEL_A_TREND").all()
        )

        checks = {
            "No duplicate signal timestamps": duplicate_count == 0,
            "Availability exactly +15 minutes": timing_ok,
            "Finite stop references": stops_ok,
            "Positive finite ATR stop distances": distances_ok,
            "Correct asset labels": asset_ok,
            "Valid priorities": priority_ok,
            "Valid trade directions": side_ok,
            "Correct strategy family": family_ok,
        }

        passed = all(checks.values())
    else:
        checks = {
            "No duplicate signal timestamps": True,
            "Availability exactly +15 minutes": True,
            "Finite stop references": True,
            "Positive finite ATR stop distances": True,
            "Correct asset labels": True,
            "Valid priorities": True,
            "Valid trade directions": True,
            "Correct strategy family": True,
        }
        passed = True

    all_passed = all_passed and passed

    long_count = (
        int((result["side"] == 1).sum()) if count else 0
    )
    short_count = (
        int((result["side"] == -1).sum()) if count else 0
    )

    priority_counts = (
        result["signal_priority"].value_counts().to_dict()
        if count else {}
    )

    print("Dataset rows:", rows)
    print("Candidates:", count)
    print("LONG:", long_count)
    print("SHORT:", short_count)
    print("Priority 1:", priority_counts.get(1, 0))
    print("Priority 2:", priority_counts.get(2, 0))
    print("Priority 3:", priority_counts.get(3, 0))
    print("Processing seconds:", round(elapsed, 3))

    for name, passed_check in checks.items():
        print(("PASS" if passed_check else "FAIL"), "-", name)

    if count:
        print("\nSignal types:")
        print(result["signal_type"].value_counts().to_string())

    lines.extend([
        f"## {asset}",
        "",
        f"- Dataset rows: {rows:,}",
        f"- Candidates: {count:,}",
        f"- LONG: {long_count:,}",
        f"- SHORT: {short_count:,}",
        f"- Priority 1: {priority_counts.get(1, 0):,}",
        f"- Priority 2: {priority_counts.get(2, 0):,}",
        f"- Priority 3: {priority_counts.get(3, 0):,}",
        f"- Processing seconds: {elapsed:.3f}",
        "",
        "### Validation",
        "",
    ])

    for name, passed_check in checks.items():
        lines.append(
            f"- {'PASS' if passed_check else 'FAIL'} — {name}"
        )

    lines.extend(["", "### Signal types", ""])

    if count:
        for signal_type, signal_count in (
            result["signal_type"].value_counts().items()
        ):
            lines.append(f"- {signal_type}: {signal_count:,}")
    else:
        lines.append("- No candidates generated.")

    lines.append("")

    del df
    del result

lines.extend([
    "## Combined results",
    "",
    f"- Assets audited: {len(ASSETS)}",
    f"- Total dataset rows: {total_rows:,}",
    f"- Total candidates: {total_candidates:,}",
    f"- Overall validation: {'PASS' if all_passed else 'FAIL'}",
    "",
])

report_path = REPORT_DIR / "trade_candidate_audit.md"
report_path.write_text("\n".join(lines) + "\n")

print("\n===== COMBINED AUDIT =====")
print("Assets:", len(ASSETS))
print("Dataset rows:", total_rows)
print("Candidates:", total_candidates)
print("Overall:", "PASS" if all_passed else "FAIL")
print("Report:", report_path)

if not all_passed:
    raise SystemExit("AUDIT FAILED — do not commit yet.")

print("\nFive-asset candidate audit completed successfully.")
