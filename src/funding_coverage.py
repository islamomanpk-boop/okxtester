"""Coverage-aware validation for historical funding inputs.

The contract separates source coverage, the versioned settlement schedule,
the events loaded for a backtest window, and the mark-price provenance.
"""
import math


_REQUIRED_COVERAGE_FIELDS = (
    "instrument_name",
    "source_sha256",
    "coverage_start_ms",
    "coverage_end_ms",
    "schedule_id",
    "schedule_start_ms",
    "schedule_interval_ms",
    "schedule_end_ms",
    "event_window_start_ms",
    "event_window_end_ms",
    "mark_price_mode",
)


def expected_settlements(start_ms, end_ms, schedule_start_ms, interval_ms,
                         schedule_end_ms):
    """Return scheduled timestamps in (start_ms, end_ms] from a fixed schedule."""
    values = (start_ms, end_ms, schedule_start_ms, interval_ms, schedule_end_ms)
    if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
        raise ValueError("Funding schedule timestamps and interval must be integers")
    if interval_ms <= 0 or schedule_end_ms < schedule_start_ms:
        raise ValueError("Invalid funding schedule bounds or interval")
    if start_ms > end_ms:
        raise ValueError("Funding event window is reversed")
    first_index = max(0, (start_ms - schedule_start_ms) // interval_ms + 1)
    first = schedule_start_ms + first_index * interval_ms
    if first > schedule_end_ms:
        return []
    last = min(end_ms, schedule_end_ms)
    if first > last:
        return []
    count = (last - first) // interval_ms + 1
    return [first + i * interval_ms for i in range(count)]


def validate_funding_contract(bars_by_asset, funding_by_asset):
    """Validate per-asset funding contract and return normalized metadata.

    funding_by_asset[asset] must be:
      {"events": [...], "coverage": {...}}

    Events must exactly match the versioned schedule inside the declared
    event window. The event window is allowed to be narrower than source
    coverage, for example when the backtest uses a trimmed candle window.
    """
    if not isinstance(funding_by_asset, dict):
        raise ValueError("Explicit funding contract is required for every asset")

    normalized = {}
    for asset, bars in bars_by_asset.items():
        if asset not in funding_by_asset:
            raise ValueError(f"Funding contract missing for {asset}")
        item = funding_by_asset[asset]
        if not isinstance(item, dict) or set(("events", "coverage")) - set(item):
            raise ValueError(f"{asset} funding contract must contain events and coverage")
        events = item["events"]
        coverage = item["coverage"]
        if not isinstance(events, (list, tuple)):
            raise ValueError(f"{asset} funding events must be an explicit list")
        if not isinstance(coverage, dict):
            raise ValueError(f"{asset} funding coverage metadata is required")
        missing = [key for key in _REQUIRED_COVERAGE_FIELDS if key not in coverage]
        if missing:
            raise ValueError(f"{asset} funding coverage missing fields: {', '.join(missing)}")

        instrument = coverage["instrument_name"]
        source_hash = coverage["source_sha256"]
        if not isinstance(instrument, str) or not instrument.strip():
            raise ValueError(f"{asset} funding instrument identity is invalid")
        if not isinstance(source_hash, str) or len(source_hash) != 64:
            raise ValueError(f"{asset} funding source SHA-256 is invalid")
        try:
            int(source_hash, 16)
        except ValueError as exc:
            raise ValueError(f"{asset} funding source SHA-256 is invalid") from exc

        integer_fields = (
            "coverage_start_ms", "coverage_end_ms", "schedule_start_ms",
            "schedule_interval_ms", "schedule_end_ms",
            "event_window_start_ms", "event_window_end_ms",
        )
        if any(
            not isinstance(coverage[key], int) or isinstance(coverage[key], bool)
            for key in integer_fields
        ):
            raise ValueError(f"{asset} funding coverage timestamps must be integers")
        start = coverage["coverage_start_ms"]
        end = coverage["coverage_end_ms"]
        window_start = coverage["event_window_start_ms"]
        window_end = coverage["event_window_end_ms"]
        if start > end or window_start > window_end:
            raise ValueError(f"{asset} funding coverage or event window is reversed")
        if window_start < start or window_end > end:
            raise ValueError(f"{asset} funding event window exceeds source coverage")
        if not isinstance(coverage["schedule_id"], str) or not coverage["schedule_id"].strip():
            raise ValueError(f"{asset} funding schedule_id is required")
        mode = coverage["mark_price_mode"]
        if mode not in ("exact", "candle_close_proxy"):
            raise ValueError(f"{asset} funding mark_price_mode must be exact or candle_close_proxy")

        expected = expected_settlements(
            window_start, window_end,
            coverage["schedule_start_ms"],
            coverage["schedule_interval_ms"],
            coverage["schedule_end_ms"],
        )
        actual = []
        previous = None
        for event in events:
            if not isinstance(event, dict):
                raise ValueError(f"{asset} funding event must be a mapping")
            if "funding_time" not in event or "funding_rate" not in event:
                raise ValueError(f"{asset} funding event is missing fields")
            ts = event["funding_time"]
            if not isinstance(ts, int) or isinstance(ts, bool):
                raise ValueError(f"{asset} funding timestamp must be an integer")
            rate = float(event["funding_rate"])
            if not math.isfinite(rate) or not -1 <= rate <= 1:
                raise ValueError(f"{asset} has invalid funding rate")
            if previous is not None and ts <= previous:
                raise ValueError(f"{asset} funding events must be unique and chronological")
            if mode == "exact":
                if event.get("mark_price") is None:
                    raise ValueError(f"{asset} exact funding mode requires mark_price")
                mark = float(event["mark_price"])
                if not math.isfinite(mark) or mark <= 0:
                    raise ValueError(f"{asset} has invalid exact funding mark price")
            elif event.get("mark_price") is not None:
                mark = float(event["mark_price"])
                if not math.isfinite(mark) or mark <= 0:
                    raise ValueError(f"{asset} has invalid funding mark price")
            actual.append(ts)
            previous = ts

        if actual != expected:
            missing_ts = sorted(set(expected) - set(actual))
            extra_ts = sorted(set(actual) - set(expected))
            raise ValueError(
                f"{asset} funding schedule mismatch: "
                f"{len(missing_ts)} missing, {len(extra_ts)} unexpected settlements"
            )

        normalized[asset] = {
            "events": list(events),
            "coverage": dict(coverage),
            "expected_settlements": expected,
        }
    return normalized


def validate_trade_funding_window(asset, entry_time, exit_time, contract):
    """Fail if the full holding interval lies outside verified source coverage."""
    coverage = contract["coverage"]
    start = int(coverage["coverage_start_ms"])
    end = int(coverage["coverage_end_ms"])
    if entry_time < start or exit_time > end:
        raise ValueError(
            f"{asset} trade holding interval exceeds verified funding coverage"
        )
    expected = expected_settlements(
        int(entry_time), int(exit_time),
        coverage["schedule_start_ms"],
        coverage["schedule_interval_ms"],
        coverage["schedule_end_ms"],
    )
    actual = [
        int(event["funding_time"])
        for event in contract["events"]
        if entry_time < int(event["funding_time"]) <= exit_time
    ]
    if actual != expected:
        raise ValueError(
            f"{asset} trade funding interval is incomplete: "
            f"{len(sorted(set(expected) - set(actual)))} missing settlements"
        )
    return expected
