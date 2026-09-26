"""IEC 61131-3 type conversion functions ``<X>_TO_<Y>`` (Codesys semantics).

All combinations of the elementary types are available as module attributes, e.g.
``conv.INT_TO_USINT(-1) == 255`` or ``conv.REAL_TO_STRING(1.5) == '1.5'``. They are created
on first access.
"""

from __future__ import annotations

import math
import struct
from collections.abc import Callable
from functools import cache
from typing import Any

from srci.iec.rt import wrap

__all__ = ["convert", "real_to_string", "time_to_string"]

_INTS = {
    "BYTE",
    "WORD",
    "DWORD",
    "LWORD",
    "SINT",
    "USINT",
    "INT",
    "UINT",
    "DINT",
    "UDINT",
    "LINT",
    "ULINT",
    "TIME",
    "LTIME",
    "TOD",
    "TIME_OF_DAY",
    "DATE",
    "DT",
    "DATE_AND_TIME",
}
_WRAP_AS = {
    "TIME": "UDINT",
    "LTIME": "ULINT",
    "TOD": "UDINT",
    "TIME_OF_DAY": "UDINT",
    "DATE": "UDINT",
    "DT": "UDINT",
    "DATE_AND_TIME": "UDINT",
}
_REALS = {"REAL", "LREAL"}
_TYPES = _INTS | _REALS | {"BOOL", "STRING", "WSTRING"}


def _f32(value: float) -> float:
    try:
        return float(struct.unpack("<f", struct.pack("<f", value))[0])
    except OverflowError:
        return math.copysign(math.inf, value)


def _round_iec(value: float) -> int:
    """REAL to integer: round to nearest, halves away from zero (Codesys)."""
    if not math.isfinite(value):
        return 0
    return math.floor(abs(value) + 0.5) * (1 if value >= 0 else -1)


def real_to_string(value: float, single: bool = True) -> str:
    """Codesys ``REAL_TO_STRING``: shortest representation, at least one decimal."""
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "INF" if value > 0 else "-INF"
    if single:
        text = f"{_f32(value):.7g}"
        # shortest representation that survives the round trip as float32
        for digits in range(1, 10):
            candidate = f"{value:.{digits}g}"
            if _f32(float(candidate)) == _f32(value):
                text = candidate
                break
    else:
        text = repr(float(value))
    if "e" in text or "E" in text:
        mantissa, exp = text.lower().split("e")
        if "." not in mantissa:
            mantissa += ".0"
        return f"{mantissa}e{int(exp):+03d}"
    if "." not in text and "n" not in text:
        text += ".0"
    return text


def time_to_string(ms: int) -> str:
    """Codesys ``TIME_TO_STRING``: ``T#1h2m3s4ms``."""
    if ms == 0:
        return "T#0ms"
    parts: list[str] = []
    rest = ms
    for unit, size in (("d", 86_400_000), ("h", 3_600_000), ("m", 60_000), ("s", 1_000), ("ms", 1)):
        count, rest = divmod(rest, size)
        if count:
            parts.append(f"{count}{unit}")
    return "T#" + "".join(parts)


def _date_parts(seconds: int) -> tuple[int, int, int, int, int, int]:
    import datetime as dt

    d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=seconds)
    return d.year, d.month, d.day, d.hour, d.minute, d.second


def _to_string(src: str, value: Any) -> str:
    if src == "BOOL":
        return "TRUE" if value else "FALSE"
    if src in _REALS:
        return real_to_string(float(value), single=src == "REAL")
    if src in ("TIME", "LTIME"):
        return time_to_string(int(value))
    if src in ("TOD", "TIME_OF_DAY"):
        ms = int(value)
        h, rest = divmod(ms, 3_600_000)
        m, rest = divmod(rest, 60_000)
        s, milli = divmod(rest, 1000)
        return f"TOD#{h}:{m}:{s}" + (f".{milli:03d}".rstrip("0") if milli else "")
    if src == "DATE":
        y, mo, d, *_ = _date_parts(int(value))
        return f"D#{y}-{mo}-{d}"
    if src in ("DT", "DATE_AND_TIME"):
        y, mo, d, h, mi, s = _date_parts(int(value))
        return f"DT#{y}-{mo}-{d}-{h}:{mi}:{s}"
    if src in ("STRING", "WSTRING"):
        return str(value)
    return str(int(value))


def _from_string(dst: str, text: str) -> Any:
    t = text.strip()
    if dst == "BOOL":
        return t.upper() == "TRUE" or t == "1"
    if dst in _REALS:
        try:
            return float(t)
        except ValueError:
            return 0.0
    try:
        if "#" in t:
            base, digits = t.split("#", 1)
            number = int(digits.replace("_", ""), int(base))
        else:
            number = int(float(t))
    except ValueError:
        number = 0
    return wrap(number, _WRAP_AS.get(dst, dst))


def convert(value: Any, src: str, dst: str) -> Any:
    """``<src>_TO_<dst>(value)``."""
    if dst in ("STRING", "WSTRING"):
        return _to_string(src, value)
    if src in ("STRING", "WSTRING"):
        return _from_string(dst, str(value))
    if dst == "BOOL":
        return bool(value)
    if dst in _REALS:
        return _f32(float(value)) if dst == "REAL" else float(value)
    # integer target
    number = _round_iec(float(value)) if src in _REALS else int(value)
    return wrap(number, _WRAP_AS.get(dst, dst))


@cache
def _converter(name: str) -> Callable[[Any], Any]:
    src, _, dst = name.partition("_TO_")
    if not src or not dst or src not in _TYPES or dst not in _TYPES:
        raise AttributeError(name)

    def conv(value: Any) -> Any:
        return convert(value, src, dst)

    conv.__name__ = conv.__qualname__ = name
    return conv


def TRUNC(value: float) -> int:
    """REAL -> DINT towards zero."""
    return wrap(math.trunc(value), "DINT")


def __getattr__(name: str) -> Callable[[Any], Any]:
    return _converter(name)
