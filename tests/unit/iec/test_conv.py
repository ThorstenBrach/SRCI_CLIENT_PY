"""IEC type conversions (srci.iec.conv)."""

from __future__ import annotations

import math

import pytest

from srci.iec import conv
from srci.types import CmdMessageState


@pytest.mark.parametrize(
    ("name", "value", "expected"),
    [
        ("INT_TO_USINT", -1, 255),
        ("DINT_TO_UINT", 70000, 70000 - 65536),
        ("UDINT_TO_DINT", 2**32 - 1, -1),
        ("USINT_TO_SINT", 200, -56),
        ("BOOL_TO_INT", True, 1),
        ("INT_TO_BOOL", 5, True),
        ("REAL_TO_INT", 2.5, 3),
        ("REAL_TO_INT", -2.5, -3),
        ("REAL_TO_DINT", 1.4, 1),
        ("REAL_TO_UINT", -1.0, 65535),
        ("REAL_TO_INT", math.nan, 0),
        ("TIME_TO_UDINT", 5000, 5000),
        ("DINT_TO_TIME", -1, 2**32 - 1),
        ("USINT_TO_REAL", 3, 3.0),
        ("STRING_TO_INT", " 42 ", 42),
        ("STRING_TO_INT", "16#FF", 255),
        ("STRING_TO_INT", "abc", 0),
        ("STRING_TO_REAL", "1.5", 1.5),
        ("STRING_TO_REAL", "x", 0.0),
        ("STRING_TO_BOOL", "TRUE", True),
    ],
)
def test_numeric_conversions(name: str, value: object, expected: object) -> None:
    assert getattr(conv, name)(value) == expected


def test_real_is_rounded_to_single_precision() -> None:
    assert conv.LREAL_TO_REAL(0.1) != 0.1
    assert conv.LREAL_TO_REAL(0.1) == pytest.approx(0.1)


@pytest.mark.parametrize(
    ("name", "value", "expected"),
    [
        ("BOOL_TO_STRING", True, "TRUE"),
        ("BOOL_TO_STRING", False, "FALSE"),
        ("INT_TO_STRING", -5, "-5"),
        ("USINT_TO_STRING", CmdMessageState.DONE, str(int(CmdMessageState.DONE))),
        ("REAL_TO_STRING", 1.5, "1.5"),
        ("REAL_TO_STRING", 100.0, "100.0"),
        ("REAL_TO_STRING", 0.1, "0.1"),
        ("REAL_TO_STRING", 1e-7, "1.0e-07"),
        ("REAL_TO_STRING", math.nan, "NaN"),
        ("REAL_TO_STRING", -math.inf, "-INF"),
        ("LREAL_TO_STRING", 0.1, "0.1"),
        ("TIME_TO_STRING", 0, "T#0ms"),
        ("TIME_TO_STRING", 90_500, "T#1m30s500ms"),
        ("TIME_TO_STRING", 90_061_001, "T#1d1h1m1s1ms"),
        ("TOD_TO_STRING", 15 * 3_600_000 + 18 * 60_000 + 4_567, "TOD#15:18:4.567"),
        ("TOD_TO_STRING", 3_600_000, "TOD#1:0:0"),
        ("DATE_TO_STRING", 1_736_035_200, "D#2025-1-5"),
        ("DT_TO_STRING", 1_736_035_200 + 3661, "DT#2025-1-5-1:1:1"),
        ("STRING_TO_STRING", "abc", "abc"),
    ],
)
def test_to_string(name: str, value: object, expected: str) -> None:
    assert getattr(conv, name)(value) == expected


def test_trunc() -> None:
    assert conv.TRUNC(2.9) == 2
    assert conv.TRUNC(-2.9) == -2


def test_unknown_conversion() -> None:
    with pytest.raises(AttributeError):
        conv.FOO_TO_BAR  # noqa: B018
    with pytest.raises(AttributeError):
        conv.INT_TO  # noqa: B018
    assert conv.INT_TO_BYTE.__name__ == "INT_TO_BYTE"
