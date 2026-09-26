"""IEC 61131-3 type descriptors used by the generated types.

The generated dataclasses use plain Python values (``bool``, ``int``, ``float``,
``str``, ``list``, ``IntEnum``). The IEC layout information that is needed for the
byte codec (element type, array bounds, string length, enum base type) is kept
separately in the class attribute ``_IEC_FIELDS_`` as a tuple of :class:`IecField`.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, ClassVar, Protocol, SupportsIndex, TypeVar, overload

__all__ = [
    "BOOL",
    "BYTE",
    "DATE",
    "DINT",
    "DWORD",
    "ELEMENTARY",
    "INT",
    "LINT",
    "LREAL",
    "LWORD",
    "REAL",
    "SINT",
    "TIME",
    "TOD",
    "UDINT",
    "UINT",
    "ULINT",
    "USINT",
    "WORD",
    "ArrayType",
    "Elementary",
    "EnumType",
    "IecArray",
    "IecField",
    "IecStruct",
    "IecType",
    "InstanceType",
    "PointerType",
    "StringType",
    "StructType",
    "enum_base",
    "register_enum",
]


# --------------------------------------------------------------------------- descriptors


@dataclass(frozen=True, slots=True)
class Elementary:
    """Elementary IEC type.

    ``fmt`` is the :mod:`struct` format character (without byte order prefix).
    """

    name: str
    size: int
    fmt: str
    python_type: type
    signed: bool = False

    @property
    def min(self) -> int | float:
        if self.python_type is float:
            return -3.4028234663852886e38 if self.size == 4 else -1.7976931348623157e308
        if self.python_type is bool:
            return 0
        return -(1 << (self.size * 8 - 1)) if self.signed else 0

    @property
    def max(self) -> int | float:
        if self.python_type is float:
            return 3.4028234663852886e38 if self.size == 4 else 1.7976931348623157e308
        if self.python_type is bool:
            return 1
        return (1 << (self.size * 8 - 1)) - 1 if self.signed else (1 << (self.size * 8)) - 1


BOOL = Elementary("BOOL", 1, "?", bool)
BYTE = Elementary("BYTE", 1, "B", int)
WORD = Elementary("WORD", 2, "H", int)
DWORD = Elementary("DWORD", 4, "I", int)
LWORD = Elementary("LWORD", 8, "Q", int)
SINT = Elementary("SINT", 1, "b", int, signed=True)
USINT = Elementary("USINT", 1, "B", int)
INT = Elementary("INT", 2, "h", int, signed=True)
UINT = Elementary("UINT", 2, "H", int)
DINT = Elementary("DINT", 4, "i", int, signed=True)
UDINT = Elementary("UDINT", 4, "I", int)
LINT = Elementary("LINT", 8, "q", int, signed=True)
ULINT = Elementary("ULINT", 8, "Q", int)
REAL = Elementary("REAL", 4, "f", float, signed=True)
LREAL = Elementary("LREAL", 8, "d", float, signed=True)
# TIME is a 32 bit value in milliseconds, TOD milliseconds since midnight,
# DATE (Codesys 16 bit IEC_DATE is a UINT alias) - see the PLC library.
TIME = Elementary("TIME", 4, "I", int)
TOD = Elementary("TOD", 4, "I", int)
DATE = Elementary("DATE", 4, "I", int)

ELEMENTARY: dict[str, Elementary] = {
    t.name: t
    for t in (
        BOOL,
        BYTE,
        WORD,
        DWORD,
        LWORD,
        SINT,
        USINT,
        INT,
        UINT,
        DINT,
        UDINT,
        LINT,
        ULINT,
        REAL,
        LREAL,
        TIME,
        TOD,
        DATE,
    )
}


@dataclass(frozen=True, slots=True)
class StringType:
    """``STRING(length)`` - ``length`` characters plus a terminating NUL byte."""

    length: int

    @property
    def size(self) -> int:
        return self.length + 1


@dataclass(frozen=True, slots=True)
class ArrayType:
    """``ARRAY[lower..upper] OF element``."""

    lower: int
    upper: int
    element: IecType

    @property
    def count(self) -> int:
        return self.upper - self.lower + 1


_ENUM_BASE: dict[type[IntEnum], Elementary] = {}


def register_enum(enum: type[IntEnum], base: Elementary) -> None:
    """Register the IEC base type of a generated enum (called by the generated code)."""
    _ENUM_BASE[enum] = base


def enum_base(enum: type[IntEnum]) -> Elementary:
    """IEC base type of a generated enum."""
    return _ENUM_BASE[enum]


@dataclass(frozen=True, slots=True)
class EnumType:
    """Reference to a generated enum (``IntEnum``) with its IEC base type."""

    enum: type[IntEnum]

    @property
    def base(self) -> Elementary:
        return _ENUM_BASE[self.enum]


@dataclass(frozen=True, slots=True)
class StructType:
    """Reference to a generated structure."""

    struct: type[IecStruct]


@dataclass(frozen=True, slots=True)
class PointerType:
    """``POINTER TO ...`` - only used in internal structures, never transmitted."""

    target: str


@dataclass(frozen=True, slots=True)
class InstanceType:
    """Function block / interface instance inside an internal structure (e.g. ``R_TRIG``).

    Such members are created by the hand written core, never transmitted.
    """

    name: str


IecType = Elementary | StringType | ArrayType | EnumType | StructType | PointerType | InstanceType


@dataclass(frozen=True, slots=True)
class IecField:
    """IEC description of one structure member.

    ``name`` is the Python attribute name, ``st_name`` the original ST name (they only
    differ if the ST name is a Python keyword).
    """

    name: str
    type: IecType
    st_name: str = ""

    def __post_init__(self) -> None:
        if not self.st_name:
            object.__setattr__(self, "st_name", self.name)


# --------------------------------------------------------------------------- protocols


class IecStruct(Protocol):
    """Protocol implemented by the generated structures."""

    _IEC_FIELDS_: ClassVar[tuple[IecField, ...]]


# --------------------------------------------------------------------------- arrays

T = TypeVar("T")


class IecArray(list[T]):
    """List with IEC index bounds (``ARRAY[lower..upper]``).

    Integer indices are interpreted like in ST (``arr[lower]`` is the first element),
    so ported code can keep the original indices. Slices and iteration behave like a
    normal list. The length is fixed to ``upper - lower + 1``.
    """

    __slots__ = ("lower",)

    def __init__(self, lower: int, items: Iterable[T]) -> None:
        super().__init__(items)
        self.lower = lower

    @property
    def upper(self) -> int:
        return self.lower + len(self) - 1

    def _index(self, index: SupportsIndex) -> int:
        i = index.__index__()
        if i < self.lower or i > self.upper:
            raise IndexError(f"index {i} out of range [{self.lower}..{self.upper}]")
        return i - self.lower

    @overload
    def __getitem__(self, index: SupportsIndex) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> list[T]: ...
    def __getitem__(self, index: SupportsIndex | slice) -> T | list[T]:
        if isinstance(index, slice):
            return list(super().__getitem__(index))
        return super().__getitem__(self._index(index))

    @overload
    def __setitem__(self, index: SupportsIndex, value: T) -> None: ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[T]) -> None: ...
    def __setitem__(self, index: SupportsIndex | slice, value: Any) -> None:
        if isinstance(index, slice):
            items = list(value)
            if len(super().__getitem__(index)) != len(items):
                raise ValueError("IecArray has a fixed length")
            super().__setitem__(index, items)
            return
        super().__setitem__(self._index(index), value)

    def __repr__(self) -> str:
        return f"IecArray[{self.lower}..{self.upper}]({list.__repr__(self)})"

    def __copy__(self) -> IecArray[T]:
        return IecArray(self.lower, self)

    def __deepcopy__(self, memo: dict[int, Any]) -> IecArray[T]:
        import copy

        return IecArray(self.lower, (copy.deepcopy(x, memo) for x in self))

    # length changing operations are not allowed
    def _fixed(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("IecArray has a fixed length")

    append = extend = insert = pop = remove = clear = _fixed  # type: ignore[assignment]
    __delitem__ = __iadd__ = __imul__ = _fixed  # type: ignore[assignment]
