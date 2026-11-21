"""Memory-efficient, columnar storage for synchronized OHLCV candles."""

from array import array
import csv
import math


class CompactBarSeries:
    """Store candle columns in compact numeric arrays."""

    REQUIRED = ("ts", "open", "high", "low", "close")

    def __init__(self):
        self.timestamps = array("q")
        self.opens = array("d")
        self.highs = array("d")
        self.lows = array("d")
        self.closes = array("d")
        self.volumes = array("d")

    def __len__(self):
        return len(self.timestamps)

    def __bool__(self):
        return len(self) > 0

    def append(self, ts, open_price, high, low, close, volume=0.0):
        self.timestamps.append(int(ts))
        self.opens.append(float(open_price))
        self.highs.append(float(high))
        self.lows.append(float(low))
        self.closes.append(float(close))
        self.volumes.append(float(volume))

    def __getitem__(self, index):
        if isinstance(index, slice):
            raise TypeError("CompactBarSeries does not support slicing")
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(index)
        return {
            "ts": self.timestamps[index],
            "open": self.opens[index],
            "high": self.highs[index],
            "low": self.lows[index],
            "close": self.closes[index],
            "vol": self.volumes[index],
        }

    def __iter__(self):
        for index in range(len(self)):
            yield self[index]

    @classmethod
    def from_csv(cls, path):
        """Load a candle CSV without constructing a DataFrame or row dict list."""
        result = cls()
        with open(path, "r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError(f"{path}: CSV has no header")

            missing = [
                name for name in cls.REQUIRED
                if name not in reader.fieldnames
            ]
            if missing:
                raise ValueError(f"{path}: missing columns {missing}")

            has_volume = "vol" in reader.fieldnames

            for line_number, row in enumerate(reader, start=2):
                try:
                    ts_value = float(row["ts"])
                    values = [
                        float(row[name])
                        for name in ("open", "high", "low", "close")
                    ]
                    volume = float(row["vol"]) if has_volume else 0.0
                except (TypeError, ValueError) as exc:
                    raise ValueError(
                        f"{path}: invalid numeric value on line {line_number}"
                    ) from exc

                if not math.isfinite(ts_value):
                    raise ValueError(
                        f"{path}: invalid timestamp on line {line_number}"
                    )
                if not all(math.isfinite(value) for value in values):
                    raise ValueError(
                        f"{path}: invalid OHLC on line {line_number}"
                    )
                if not math.isfinite(volume):
                    raise ValueError(
                        f"{path}: invalid volume on line {line_number}"
                    )

                result.append(
                    int(ts_value), *values, volume=volume
                )

        if not result:
            raise ValueError(f"{path}: no candles found")
        return result


class TimestampBarLookup:
    """Resolve a timestamp to one candle without a timestamp dictionary."""

    def __init__(self, bars, interval_ms=60_000):
        self.bars = bars
        self.interval_ms = int(interval_ms)
        self.first_ts = int(bars[0]["ts"])
        self.length = len(bars)

    def __getitem__(self, timestamp):
        timestamp = int(timestamp)
        offset = timestamp - self.first_ts

        if offset < 0 or offset % self.interval_ms:
            raise KeyError(timestamp)

        index = offset // self.interval_ms
        if index >= self.length:
            raise KeyError(timestamp)

        bar = self.bars[index]
        if int(bar["ts"]) != timestamp:
            raise KeyError(timestamp)
        return bar
