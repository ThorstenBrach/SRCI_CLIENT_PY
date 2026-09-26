"""``SIZEOF`` for the generated types (``pack_mode 1`` like in the PLC library)."""

from __future__ import annotations

from functools import cache
from typing import Any

from srci.types import iec

__all__ = ["SIZEOF", "sizeof_type"]


def sizeof_type(t: iec.IecType) -> int:
    """Size in bytes of an IEC type descriptor."""
    if isinstance(t, iec.Elementary | iec.StringType):
        return t.size
    if isinstance(t, iec.EnumType):
        return t.base.size
    if isinstance(t, iec.StructType):
        return _struct_size(t.struct)
    if isinstance(t, iec.ArrayType):
        return t.count * sizeof_type(t.element)
    raise TypeError(f"SIZEOF is not defined for {t}")


@cache
def _struct_size(cls: type) -> int:
    fields: tuple[iec.IecField, ...] = cls._IEC_FIELDS_  # type: ignore[attr-defined]
    total = 0
    for f in fields:
        total += sizeof_type(f.type)
    return total


def SIZEOF(value: Any) -> int:
    """ST ``SIZEOF`` of a generated structure (class or instance)."""
    cls = value if isinstance(value, type) else type(value)
    if not hasattr(cls, "_IEC_FIELDS_"):
        raise TypeError(f"SIZEOF needs a generated IEC structure, got {cls.__name__}")
    return _struct_size(cls)
