"""Runtime support for the ST -> Python transpiled code (``tools.st2py``).

Implements the IEC 61131-3 / Codesys semantics that Python does not have:

* value semantics of structures and arrays (``copy_into``)
* integer wrap around on assignment (``wrap``)
* integer division truncating towards zero (``idiv``/``imod``)
* standard functions (``LIMIT``, ``MIN``, ``MAX``, ``CONCAT``, ``MID`` ...)
* memory functions on a byte image of the data (``ADR``, ``SysDepMemCpy/Cmp/Set``) with
  the layout of the PLC (``pack_mode 1``, little endian like x86 PLCs)
"""

from __future__ import annotations

import copy
import math
import struct as _struct
from collections.abc import Callable
from functools import cache
from typing import Any

from srci.iec.types import bit, set_bit
from srci.types import iec

__all__ = [
    "ADR",
    "ADR_ELEM",
    "ADR_VALUE",
    "CONCAT",
    "DELETE",
    "FIND",
    "INSERT",
    "LEFT",
    "LEN",
    "LIMIT",
    "LOWER_BOUND",
    "MAX",
    "MID",
    "MIN",
    "REPLACE",
    "RIGHT",
    "ROL",
    "ROR",
    "UPPER_BOUND",
    "Ptr",
    "SysDepIsValidReal",
    "SysDepMemCmp",
    "SysDepMemCpy",
    "SysDepMemSet",
    "array_type",
    "bit",
    "copy_into",
    "copy_value",
    "idiv",
    "imod",
    "mem_image",
    "mem_read",
    "new_value",
    "set_bit",
    "sizeof_value",
    "st_for_end",
    "st_range",
    "trunc_str",
    "wrap",
]

# ---------------------------------------------------------------------- integers

_INT_RANGES: dict[str, tuple[int, int, bool]] = {
    t.name: (t.size * 8, 1 << (t.size * 8), t.signed)
    for t in iec.ELEMENTARY.values()
    if t.python_type is int and t.name != "BOOL"
}


def wrap(value: int, type_name: str) -> int:
    """Two's complement wrap around of ``value`` into the IEC integer type."""
    _, modulo, signed = _INT_RANGES[type_name]
    v = int(value) % modulo
    if signed and v >= modulo >> 1:
        v -= modulo
    return v


def idiv(a: int, b: int) -> int:
    """Integer ``/`` of ST: truncates towards zero (Python ``//`` floors)."""
    if b == 0:
        raise ZeroDivisionError("integer division by zero")
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def imod(a: int, b: int) -> int:
    """``MOD`` of ST: the sign follows the dividend."""
    return a - b * idiv(a, b)


def st_range(start: int, end: int, step: int) -> range:
    """Values of ``FOR i := start TO end BY step`` (step given at runtime)."""
    return range(start, end + (1 if step > 0 else -1), step)


def ROL(value: int, n: int, type_name: str) -> int:
    bits = _INT_RANGES[type_name][0]
    n %= bits
    mask = (1 << bits) - 1
    return ((value << n) | (value >> (bits - n))) & mask


def ROR(value: int, n: int, type_name: str) -> int:
    bits = _INT_RANGES[type_name][0]
    return ROL(value, bits - (n % bits), type_name)


def LOWER_BOUND(arr: Any, dim: int = 1) -> int:
    return arr.lower if isinstance(arr, iec.IecArray) else 0


def UPPER_BOUND(arr: Any, dim: int = 1) -> int:
    return LOWER_BOUND(arr) + len(arr) - 1


def st_for_end(start: int, end: int, step: int = 1) -> int:
    """Value of the loop variable after ``FOR i := start TO end BY step`` without EXIT."""
    if step > 0:
        return start if start > end else start + ((end - start) // step + 1) * step
    return start if start < end else start + ((start - end) // -step + 1) * step


# ---------------------------------------------------------------------- standard functions


def LIMIT(MN: Any, IN: Any, MX: Any) -> Any:
    return MN if IN < MN else MX if IN > MX else IN


def MIN(*values: Any) -> Any:
    return min(values)


def MAX(*values: Any) -> Any:
    return max(values)


def trunc_str(value: str, length: int) -> str:
    """Assignment to ``STRING(length)``: longer strings are cut."""
    return value if len(value) <= length else value[:length]


def CONCAT(*values: str) -> str:
    return trunc_str("".join(values), 255)


def LEN(STR: str) -> int:
    return len(STR)


def LEFT(STR: str, SIZE: int) -> str:
    return STR[: max(SIZE, 0)]


def RIGHT(STR: str, SIZE: int) -> str:
    return STR[len(STR) - SIZE :] if SIZE > 0 else ""


def MID(STR: str, LEN: int, POS: int) -> str:
    """``LEN`` characters from position ``POS`` (1 based)."""
    if POS < 1 or LEN <= 0:
        return ""
    return STR[POS - 1 : POS - 1 + LEN]


def FIND(STR1: str, STR2: str) -> int:
    """Position (1 based) of ``STR2`` in ``STR1``, 0 if not found."""
    return STR1.find(STR2) + 1


def REPLACE(STR1: str, STR2: str, L: int, P: int) -> str:
    """Replace ``L`` characters of ``STR1`` from position ``P`` (1 based) by ``STR2``."""
    pos = max(P, 1) - 1
    return trunc_str(STR1[:pos] + STR2 + STR1[pos + max(L, 0) :], 255)


def INSERT(STR1: str, STR2: str, POS: int) -> str:
    """Insert ``STR2`` into ``STR1`` after position ``POS``."""
    pos = min(max(POS, 0), len(STR1))
    return trunc_str(STR1[:pos] + STR2 + STR1[pos:], 255)


def DELETE(STR: str, LEN: int, POS: int) -> str:
    pos = max(POS, 1) - 1
    return STR[:pos] + STR[pos + max(LEN, 0) :]


def SysDepIsValidReal(Value: float) -> bool:
    return math.isfinite(Value)


# ---------------------------------------------------------------------- values


def new_value(t: iec.IecType) -> Any:
    """Default value of an IEC type (used for the initialization of local variables)."""
    if isinstance(t, iec.Elementary):
        return False if t.name == "BOOL" else 0.0 if t.python_type is float else 0
    if isinstance(t, iec.StringType):
        return ""
    if isinstance(t, iec.EnumType):
        return t.enum(0)
    if isinstance(t, iec.StructType):
        return t.struct()
    if isinstance(t, iec.ArrayType):
        items = [new_value(t.element) for _ in range(t.count)]
        return items if int(t.lower) == 0 else iec.IecArray(int(t.lower), items)
    return None


def copy_value(value: Any) -> Any:
    """Copy of a structure/array/FB passed as VAR_INPUT (ST passes a copy)."""
    return copy.deepcopy(value)


def array_type(value: Any, element: iec.IecType) -> iec.ArrayType:
    """Descriptor of an ``ARRAY[*]`` value."""
    lower = value.lower if isinstance(value, iec.IecArray) else 0
    return iec.ArrayType(lower, lower + len(value) - 1, element)


def sizeof_value(value: Any, element: iec.IecType) -> int:
    """``SIZEOF`` of an ``ARRAY[*]`` value."""
    return type_size(array_type(value, element))


def copy_into(dst: Any, src: Any) -> None:
    """ST assignment ``dst := src`` of a structure or an array (copy into ``dst``).

    ``dst`` keeps its identity, so references to it (VAR_IN_OUT, REFERENCE TO) see the new
    values. If ``dst`` is a base type of ``src`` only the fields of ``dst`` are copied.
    """
    if dst is src:
        return
    if isinstance(dst, bytearray):
        if len(dst) != len(src):
            raise ValueError(f"array assignment with different sizes ({len(dst)} <- {len(src)})")
        dst[:] = bytes(src)
        return
    if isinstance(dst, list):
        if len(dst) != len(src):
            raise ValueError(f"array assignment with different sizes ({len(dst)} <- {len(src)})")
        if not dst:
            return
        first = list.__getitem__(dst, 0)
        if isinstance(first, list) or hasattr(first, "_IEC_FIELDS_"):
            for i in range(len(dst)):
                copy_into(
                    list.__getitem__(dst, i),
                    src[i] if not isinstance(src, list) else list.__getitem__(src, i),
                )
        else:
            list.__setitem__(dst, slice(None), list(src))
        return
    copier = _copier(type(dst))  # type: ignore[arg-type]
    copier(dst, src)


_Copier = Callable[[Any, Any], None]


@cache
def _copier(cls: Any) -> _Copier:
    fields = getattr(cls, "_IEC_FIELDS_", None)
    if fields is None:
        raise TypeError(f"copy_into needs a structure or an array, got {cls.__name__}")
    simple = tuple(
        f.name for f in fields if not isinstance(f.type, iec.StructType | iec.ArrayType | iec.InstanceType)
    )
    nested = tuple(f.name for f in fields if isinstance(f.type, iec.StructType | iec.ArrayType))
    instances = tuple(f.name for f in fields if isinstance(f.type, iec.InstanceType))

    def copy_struct(dst: Any, src: Any) -> None:
        for name in simple:
            setattr(dst, name, getattr(src, name))
        for name in nested:
            copy_into(getattr(dst, name), getattr(src, name))
        for name in instances:
            setattr(dst, name, copy.copy(getattr(src, name)))

    return copy_struct


# ---------------------------------------------------------------------- memory image

_FMT = {
    "BOOL": "?",
    "BYTE": "B",
    "WORD": "H",
    "DWORD": "I",
    "LWORD": "Q",
    "SINT": "b",
    "USINT": "B",
    "INT": "h",
    "UINT": "H",
    "DINT": "i",
    "UDINT": "I",
    "LINT": "q",
    "ULINT": "Q",
    "REAL": "f",
    "LREAL": "d",
    "TIME": "I",
    "TOD": "I",
    "DATE": "I",
}

POINTER_SIZE = 8

_objects: dict[int, Any] = {}  # id -> object for pointers stored in a memory image


def _ref_id(obj: Any) -> int:
    if obj is None:
        return 0
    _objects[id(obj)] = obj
    return id(obj)


@cache
def type_size(t: iec.IecType) -> int:
    if isinstance(t, iec.PointerType | iec.InstanceType):
        return POINTER_SIZE
    if isinstance(t, iec.ArrayType):
        return t.count * type_size(t.element)
    if isinstance(t, iec.StructType):
        return sum(type_size(f.type) for f in t.struct._IEC_FIELDS_)
    from srci.iec.sizeof import sizeof_type

    return sizeof_type(t)


def type_of(value: Any) -> iec.IecType:
    """IEC type of a structure value (other values need an explicit type)."""
    if hasattr(type(value), "_IEC_FIELDS_"):
        return iec.StructType(type(value))
    raise TypeError(f"no IEC type information for {type(value).__name__}")


def _pack(value: Any, t: iec.IecType, out: bytearray) -> None:
    if isinstance(t, iec.Elementary):
        out += _struct.pack("<" + _FMT[t.name], value)
    elif isinstance(t, iec.EnumType):
        out += _struct.pack("<" + _FMT[t.base.name], int(value))
    elif isinstance(t, iec.StringType):
        raw = value.encode("latin-1", errors="replace")[: t.length]
        out += raw + bytes(t.size - len(raw))
    elif isinstance(t, iec.ArrayType):
        for item in value:
            _pack(item, t.element, out)
    elif isinstance(t, iec.StructType):
        for f in t.struct._IEC_FIELDS_:
            _pack(getattr(value, f.name), f.type, out)
    elif isinstance(t, iec.PointerType | iec.InstanceType):
        out += _struct.pack("<Q", _ref_id(value))
    else:
        raise TypeError(f"cannot pack {t}")


def mem_image(value: Any, t: iec.IecType | None = None) -> bytes:
    """Byte image of a value like in the PLC memory."""
    out = bytearray()
    _pack(value, t if t is not None else type_of(value), out)
    return bytes(out)


def _unpack(data: bytes, pos: int, t: iec.IecType, current: Any) -> tuple[Any, int]:
    """Value of type ``t`` at ``data[pos:]``; structures and arrays are updated in place."""
    if isinstance(t, iec.Elementary):
        (v,) = _struct.unpack_from("<" + _FMT[t.name], data, pos)
        return v, pos + t.size
    if isinstance(t, iec.EnumType):
        (v,) = _struct.unpack_from("<" + _FMT[t.base.name], data, pos)
        return t.enum(v), pos + t.base.size
    if isinstance(t, iec.StringType):
        raw = data[pos : pos + t.size]
        end = raw.find(b"\0")
        text = (raw if end < 0 else raw[:end]).decode("latin-1")
        return text[: t.length], pos + t.size
    if isinstance(t, iec.ArrayType):
        for i in range(t.count):
            item = list.__getitem__(current, i)
            new, pos = _unpack(data, pos, t.element, item)
            if new is not item:
                list.__setitem__(current, i, new)
        return current, pos
    if isinstance(t, iec.StructType):
        for f in t.struct._IEC_FIELDS_:
            item = getattr(current, f.name)
            new, pos = _unpack(data, pos, f.type, item)
            if new is not item:
                setattr(current, f.name, new)
        return current, pos
    if isinstance(t, iec.PointerType):
        (ref,) = _struct.unpack_from("<Q", data, pos)
        return (_objects.get(ref) if ref else None), pos + POINTER_SIZE
    if isinstance(t, iec.InstanceType):
        (ref,) = _struct.unpack_from("<Q", data, pos)
        if ref == 0:
            return type(current)(), pos + POINTER_SIZE
        return _objects.get(ref, current), pos + POINTER_SIZE
    raise TypeError(f"cannot unpack {t}")


class Ptr:
    """``POINTER TO`` data: owner object + key (attribute name / index) + IEC type + offset.

    ``key`` is ``None`` if the owner itself (a structure or an array) is the target.
    """

    __slots__ = ("key", "offset", "owner", "type")

    def __init__(self, owner: Any, key: str | int | None, t: iec.IecType | None, offset: int = 0) -> None:
        self.owner = owner
        self.key = key
        self.type = t if t is not None else type_of(self.value)
        self.offset = offset

    @property
    def value(self) -> Any:
        if self.key is None:
            return self.owner
        if isinstance(self.key, str):
            return getattr(self.owner, self.key)
        return self.owner[self.key]

    @value.setter
    def value(self, new: Any) -> None:
        if self.key is None:
            copy_into(self.owner, new)
        elif isinstance(self.key, str):
            setattr(self.owner, self.key, new)
        else:
            self.owner[self.key] = new

    def deref(self, t: iec.IecType) -> Any:
        """``p^`` for a pointer to ``t`` (also into an array of ``t``)."""
        if self.offset == 0 and self.type == t:
            return self.value
        if isinstance(self.type, iec.ArrayType) and self.type.element == t:
            size = type_size(t)
            index, rest = divmod(self.offset, size)
            if rest:
                raise IndexError("pointer does not point to an array element")
            return list.__getitem__(self.value, index)
        if isinstance(t, iec.Elementary | iec.EnumType | iec.StringType):
            size = type_size(t)
            value, _ = _unpack(self.read(size), 0, t, None)
            return value
        raise TypeError(f"dereference of a pointer to {self.type} as {t} (offset {self.offset})")

    def store(self, t: iec.IecType, value: Any) -> None:
        """``p^ := value`` for a pointer to a scalar ``t``."""
        self.write(mem_image(value, t))

    def __add__(self, offset: int) -> Ptr:
        return Ptr(self.owner, self.key, self.type, self.offset + int(offset))

    def __sub__(self, offset: int) -> Ptr:
        return self + (-int(offset))

    @property
    def size(self) -> int:
        return type_size(self.type)

    def read(self, n: int) -> bytes:
        image = mem_image(self.value, self.type)
        if self.offset < 0 or self.offset + n > len(image):
            raise IndexError(
                f"memory access [{self.offset}..{self.offset + n}) outside of {len(image)} bytes"
            )
        return image[self.offset : self.offset + n]

    def write(self, data: bytes) -> None:
        current = self.value
        image = bytearray(mem_image(current, self.type))
        end = self.offset + len(data)
        if self.offset < 0 or end > len(image):
            raise IndexError(f"memory access [{self.offset}..{end}) outside of {len(image)} bytes")
        image[self.offset : end] = data
        new, _ = _unpack(bytes(image), 0, self.type, current)
        if new is not current:
            self.value = new


class _ValuePtr(Ptr):
    """Pointer to a local scalar: the value lives in a box, the transpiled code copies it
    back to the local variable after the call (``local = ptr.value``)."""

    def __init__(self, value: Any, t: iec.IecType) -> None:
        super().__init__([value], 0, t)


def ADR(owner: Any, key: str | int | None = None, t: iec.IecType | None = None) -> Ptr:
    """``ADR(owner.key)`` / ``ADR(owner[key])`` / ``ADR(owner)`` (key None)."""
    return Ptr(owner, key, t)


def ADR_ELEM(arr: Any, index: int, element: iec.IecType) -> Ptr:
    """``ADR(arr[index])``: pointer into the array (C like access to the following elements)."""
    at = array_type(arr, element)
    return Ptr(arr, None, at, (index - int(at.lower)) * type_size(element))


def ADR_VALUE(value: Any, t: iec.IecType) -> Ptr:
    """``ADR`` of a local scalar used as source of a memory function."""
    return _ValuePtr(value, t)


def mem_read(src: Ptr, t: iec.IecType, n: int, current: Any) -> Any:
    """``SysDepMemCpy(ADR(local), src, n)`` for a local scalar: returns the new value."""
    image = bytearray(mem_image(current, t))
    image[:n] = src.read(n)
    value, _ = _unpack(bytes(image), 0, t, current)
    return value


def _whole(p: Ptr, n: int) -> bool:
    """``p`` points to the start of its value and ``n`` covers the complete value."""
    return p.offset == 0 and not isinstance(p, _ValuePtr) and n == p.size


def _zero(value: Any, t: iec.IecType) -> Any:
    """Value of type ``t`` with all bytes 0 (structures/arrays are changed in place)."""
    return _zeroer(t)(value)


_Zeroer = Callable[[Any], Any]


@cache
def _zeroer(t: iec.IecType) -> _Zeroer:
    """Compiled function that zeroes a value of type ``t`` (cached per type)."""
    if isinstance(t, iec.Elementary):
        zero: Any = False if t.name == "BOOL" else 0.0 if t.python_type is float else 0
        return lambda _v: zero
    if isinstance(t, iec.EnumType):
        member = t.enum(0)
        return lambda _v: member
    if isinstance(t, iec.StringType):
        return lambda _v: ""
    if isinstance(t, iec.PointerType):
        return lambda _v: None
    if isinstance(t, iec.InstanceType):
        return lambda v: type(v)()
    if isinstance(t, iec.ArrayType):
        elem = t.element
        if isinstance(elem, iec.Elementary | iec.EnumType | iec.StringType | iec.PointerType):
            scalar = _zeroer(elem)(None)

            def zero_scalars(v: Any) -> Any:
                if isinstance(v, bytearray):
                    v[:] = bytes(len(v))
                else:
                    list.__setitem__(v, slice(None), [scalar] * len(v))
                return v

            return zero_scalars
        inner = _zeroer(elem)

        def zero_items(v: Any) -> Any:
            for i in range(len(v)):
                item = list.__getitem__(v, i)
                new = inner(item)
                if new is not item:
                    list.__setitem__(v, i, new)
            return v

        return zero_items
    if isinstance(t, iec.StructType):
        simple: list[tuple[str, Any]] = []
        nested: list[tuple[str, _Zeroer]] = []
        for f in t.struct._IEC_FIELDS_:
            if isinstance(f.type, iec.Elementary | iec.EnumType | iec.StringType | iec.PointerType):
                simple.append((f.name, _zeroer(f.type)(None)))
            else:
                nested.append((f.name, _zeroer(f.type)))

        def zero_struct(v: Any) -> Any:
            for name, value in simple:
                setattr(v, name, value)
            for name, fn in nested:
                item = getattr(v, name)
                new = fn(item)
                if new is not item:
                    setattr(v, name, new)
            return v

        return zero_struct
    raise TypeError(f"cannot zero {t}")


def SysDepMemCpy(pDest: Ptr, pSrc: Ptr, DataLen: int) -> int:
    if DataLen <= 0:
        return 0
    if (
        _whole(pDest, DataLen)
        and _whole(pSrc, DataLen)
        and pDest.type == pSrc.type
        and not isinstance(pDest.type, iec.Elementary | iec.EnumType | iec.StringType)
    ):
        copy_into(pDest.value, pSrc.value)  # fast path: same type, complete value
        return 0
    pDest.write(pSrc.read(DataLen))
    return 0


def SysDepMemSet(pDest: Ptr, Value: int, DataLen: int) -> int:
    if DataLen <= 0:
        return 0
    if Value & 0xFF == 0 and _whole(pDest, DataLen):
        current = pDest.value
        new = _zero(current, pDest.type)
        if new is not current:
            pDest.value = new
        return 0
    pDest.write(bytes([Value & 0xFF]) * DataLen)
    return 0


def SysDepMemCmp(pData1: Ptr, pData2: Ptr, DataLen: int) -> int:
    """0 if equal, else -1/1 like ``memcmp``."""
    same = _whole(pData1, DataLen) and _whole(pData2, DataLen) and pData1.type == pData2.type
    if same and pData1.value == pData2.value:  # fast path (the byte image decides otherwise)
        return 0
    a = pData1.read(DataLen)
    b = pData2.read(DataLen)
    return 0 if a == b else (-1 if a < b else 1)


# ---------------------------------------------------------------------- misc


def call_or_none(func: Callable[..., Any] | None, **kwargs: Any) -> Any:
    return None if func is None else func(**kwargs)
