# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.iec.types
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Helpers for IEC semantics that plain Python does not have.
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""Helpers for IEC semantics that plain Python does not have."""

from __future__ import annotations

from typing import SupportsIndex

from srci.errors import ValueRangeError
from srci.types.iec import Elementary

__all__ = ["bit", "check_range", "set_bit"]


def check_range(value: SupportsIndex | float, t: Elementary, name: str = "Value") -> None:
    """Raise :class:`ValueRangeError` if ``value`` does not fit into ``t``."""
    if isinstance(value, float) and t.python_type is not float:
        raise ValueRangeError(f"{name}={value!r} is not an integer ({t.name})")
    number = value if isinstance(value, float) else value.__index__()
    if not (t.min <= number <= t.max):
        raise ValueRangeError(f"{name}={value!r} does not fit into {t.name} [{t.min}..{t.max}]")


def bit(value: int, index: int) -> bool:
    """ST ``value.index``."""
    return bool((value >> index) & 1)


def set_bit(value: int, index: int, state: bool) -> int:
    """ST ``value.index := state`` - returns the new value."""
    return value | (1 << index) if state else value & ~(1 << index)
