# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.iec.test_rt
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Runtime support of the transpiled code (srci.iec.rt).
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

"""Runtime support of the transpiled code (srci.iec.rt)."""

from __future__ import annotations

import math

import pytest

from srci.iec import rt
from srci.types import (
    AxesGroupAcyclicAcrEntry,
    CmdHeader,
    CmdType,
    ExecutionMode,
    ReadToolDataSendData,
    SWLimits,
    Tool,
    iec,
)

# ---------------------------------------------------------------- integers


@pytest.mark.parametrize(
    ("value", "type_name", "expected"),
    [
        (256, "USINT", 0),
        (-1, "USINT", 255),
        (-1, "BYTE", 255),
        (128, "SINT", -128),
        (-129, "SINT", 127),
        (65536 + 5, "UINT", 5),
        (32768, "INT", -32768),
        (2**31, "DINT", -(2**31)),
        (-1, "UDINT", 2**32 - 1),
        (2**32 + 7, "TIME", 7),
    ],
)
def test_wrap(value: int, type_name: str, expected: int) -> None:
    assert rt.wrap(value, type_name) == expected


@pytest.mark.parametrize(
    ("a", "b", "div", "mod"), [(7, 2, 3, 1), (-7, 2, -3, -1), (7, -2, -3, 1), (-7, -2, 3, -1), (6, 3, 2, 0)]
)
def test_integer_division_truncates_towards_zero(a: int, b: int, div: int, mod: int) -> None:
    assert rt.idiv(a, b) == div
    assert rt.imod(a, b) == mod


def test_integer_division_by_zero() -> None:
    with pytest.raises(ZeroDivisionError):
        rt.idiv(1, 0)


@pytest.mark.parametrize(
    ("start", "end", "step", "expected"),
    [(1, 5, 1, 6), (1, 0, 1, 1), (0, 10, 3, 12), (5, 1, -1, 0), (1, 5, -1, 1)],
)
def test_for_end_value(start: int, end: int, step: int, expected: int) -> None:
    i = start
    while (step > 0 and i <= end) or (step < 0 and i >= end):
        i += step
    assert i == expected
    assert rt.st_for_end(start, end, step) == expected


def test_st_range() -> None:
    assert list(rt.st_range(1, 5, 2)) == [1, 3, 5]
    assert list(rt.st_range(5, 1, -2)) == [5, 3, 1]


def test_rol_ror() -> None:
    assert rt.ROL(0b1000_0001, 1, "BYTE") == 0b0000_0011
    assert rt.ROR(0b0000_0011, 1, "BYTE") == 0b1000_0001
    assert rt.ROL(0x8000, 1, "WORD") == 1


def test_bounds() -> None:
    assert rt.LOWER_BOUND(iec.IecArray(3, [0, 0])) == 3
    assert rt.UPPER_BOUND(iec.IecArray(3, [0, 0])) == 4
    assert rt.LOWER_BOUND(bytearray(4)) == 0
    assert rt.UPPER_BOUND([1, 2, 3]) == 2


# ---------------------------------------------------------------- standard functions


def test_limit_min_max() -> None:
    assert rt.LIMIT(0, 5, 3) == 3
    assert rt.LIMIT(0, -5, 3) == 0
    assert rt.LIMIT(0, 2, 3) == 2
    assert rt.MIN(3, 1, 2) == 1
    assert rt.MAX(3, 1, 2) == 3


def test_string_functions() -> None:
    assert rt.CONCAT("ab", "cd", "e") == "abcde"
    assert len(rt.CONCAT("x" * 200, "y" * 200)) == 255
    assert rt.LEN("abc") == 3
    assert rt.LEFT("abcdef", 2) == "ab"
    assert rt.RIGHT("abcdef", 2) == "ef"
    assert rt.RIGHT("abc", 0) == ""
    assert rt.MID("abcdef", 2, 3) == "cd"
    assert rt.MID("abcdef", 2, 0) == ""
    assert rt.FIND("abcabc", "ca") == 3
    assert rt.FIND("abc", "x") == 0
    assert rt.REPLACE("Tool {1} ok", "7", 3, 6) == "Tool 7 ok"
    assert rt.INSERT("abef", "cd", 2) == "abcdef"
    assert rt.DELETE("abcdef", 2, 3) == "abef"
    assert rt.trunc_str("abcdef", 3) == "abc"
    assert rt.trunc_str("ab", 3) == "ab"


def test_is_valid_real() -> None:
    assert rt.SysDepIsValidReal(1.5)
    assert not rt.SysDepIsValidReal(math.nan)
    assert not rt.SysDepIsValidReal(math.inf)


# ---------------------------------------------------------------- values


def test_new_value() -> None:
    assert rt.new_value(iec.BOOL) is False
    assert rt.new_value(iec.REAL) == 0.0
    assert rt.new_value(iec.StringType(10)) == ""
    arr = rt.new_value(iec.ArrayType(1, 3, iec.INT))
    assert isinstance(arr, iec.IecArray) and arr.lower == 1 and list(arr) == [0, 0, 0]
    assert rt.new_value(iec.ArrayType(0, 1, iec.StructType(Tool)))[1] == Tool()


def test_copy_into_keeps_identity_and_copies_deep() -> None:
    src = SWLimits()
    src.J1LowerLimit = -10.0
    src.Timestamp.IEC_DATE = 3
    dst = SWLimits()
    ts = dst.Timestamp
    rt.copy_into(dst, src)
    assert dst == src and dst.Timestamp is ts
    src.Timestamp.IEC_DATE = 4
    assert dst.Timestamp.IEC_DATE == 3


def test_copy_into_base_type_from_derived() -> None:
    """``_cmdHeader := _command`` (derived structure assigned to its base)."""
    cmd = ReadToolDataSendData(CmdTyp=CmdType.ReadToolData, ExecMode=ExecutionMode.PARALLEL, ToolNo=3)
    header = CmdHeader()
    rt.copy_into(header, cmd)
    assert header.CmdTyp == CmdType.ReadToolData and header.ExecMode == ExecutionMode.PARALLEL


def test_copy_into_arrays() -> None:
    dst = [Tool(), Tool()]
    first = dst[0]
    src = [Tool(), Tool()]
    src[1].Available = True
    rt.copy_into(dst, src)
    assert dst[0] is first and dst[1].Available
    buf = bytearray(3)
    rt.copy_into(buf, [1, 2, 3])
    assert buf == b"\x01\x02\x03"
    with pytest.raises(ValueError):
        rt.copy_into([0, 0], [1])
    with pytest.raises(TypeError):
        rt.copy_into(object(), object())


def test_copy_value_is_deep() -> None:
    a = SWLimits()
    b = rt.copy_value(a)
    assert a == b and a is not b and a.Timestamp is not b.Timestamp


# ---------------------------------------------------------------- memory image


def test_mem_image_layout_pack1_little_endian() -> None:
    cmd = ReadToolDataSendData(
        CmdTyp=CmdType.ReadToolData, ExecMode=ExecutionMode.PARALLEL, ParSeq=2, ToolNo=7
    )
    image = rt.mem_image(cmd)
    assert len(image) == rt.type_size(iec.StructType(ReadToolDataSendData))
    assert image[:2] == int(CmdType.ReadToolData).to_bytes(2, "little")
    assert image[-1] == 7


def test_mem_image_string_and_bool() -> None:
    assert rt.mem_image("ab", iec.StringType(4)) == b"ab\0\0\0"
    assert rt.mem_image(True, iec.BOOL) == b"\x01"


def test_pointer_read_write_through_offsets() -> None:
    buf = iec.IecArray(1, [0] * 6)
    p = rt.ADR(buf, None, iec.ArrayType(1, 6, iec.BYTE))
    (p + 2).write(b"\x05\x06")
    assert list(buf) == [0, 0, 5, 6, 0, 0]
    assert (p + 2).read(2) == b"\x05\x06"
    with pytest.raises(IndexError):
        (p + 5).read(2)
    assert (p + 3 - 1).offset == 2


def test_pointer_to_member_and_element() -> None:
    limits = SWLimits()
    p = rt.ADR(limits, "J1LowerLimit", iec.REAL)
    p.write(rt.mem_image(-1.5, iec.REAL))
    assert limits.J1LowerLimit == -1.5
    tools = [Tool(), Tool(), Tool()]
    e = rt.ADR_ELEM(tools, 1, iec.StructType(Tool))
    assert e.deref(iec.StructType(Tool)) is tools[1]
    assert (e + rt.type_size(iec.StructType(Tool))).deref(iec.StructType(Tool)) is tools[2]
    with pytest.raises(IndexError):
        (e + 1).deref(iec.StructType(Tool))


def test_pointer_scalar_access() -> None:
    value = rt.ADR_VALUE(0x1234, iec.UINT)
    assert value.deref(iec.UINT) == 0x1234
    assert (value + 1).deref(iec.BYTE) == 0x12
    value.store(iec.UINT, 0x0102)
    assert value.value == 0x0102
    (value + 0).store(iec.BYTE, 0xFF)
    assert value.value == 0x01FF


def test_mem_read_into_local() -> None:
    payload = [0x39, 0x23, 0, 0]
    p = rt.ADR(payload, None, iec.ArrayType(0, 3, iec.BYTE))
    assert rt.mem_read(p, iec.UINT, 2, 0) == 0x2339


def test_memcpy_memset_memcmp_fast_and_byte_paths() -> None:
    a, b = SWLimits(), SWLimits()
    a.J2UpperLimit = 5.0
    pa = rt.ADR(a, None, iec.StructType(SWLimits))
    pb = rt.ADR(b, None, iec.StructType(SWLimits))
    size = pa.size
    assert rt.SysDepMemCmp(pa, pb, size) != 0
    rt.SysDepMemCpy(pb, pa, size)
    assert b == a and rt.SysDepMemCmp(pa, pb, size) == 0
    rt.SysDepMemSet(pa, 0, size)
    assert a == SWLimits()
    # partial (byte level) operations
    rt.SysDepMemSet(pa + 2, 0xFF, 2)
    assert rt.mem_image(a)[2:4] == b"\xff\xff"
    assert rt.SysDepMemCmp(pa, pb, 1) == 0
    assert rt.SysDepMemCmp(pa + 2, pb + 2, 2) == 1
    assert rt.SysDepMemCpy(pa, pb, 0) == rt.SysDepMemSet(pa, 0, 0) == 0


def test_memcmp_nan_uses_byte_image() -> None:
    a, b = SWLimits(), SWLimits()
    a.J1LowerLimit = b.J1LowerLimit = math.nan
    pa = rt.ADR(a, None, iec.StructType(SWLimits))
    pb = rt.ADR(b, None, iec.StructType(SWLimits))
    assert rt.SysDepMemCmp(pa, pb, pa.size) == 0  # like memcmp (same bit pattern)


def test_memset_resets_pointers_and_instances() -> None:
    entry = AxesGroupAcyclicAcrEntry()
    marker = object()
    entry.pCommandFB = marker
    entry.UniqueID = 5
    p = rt.ADR(entry, None, iec.StructType(AxesGroupAcyclicAcrEntry))
    rt.SysDepMemSet(p, 0, p.size)
    assert entry.pCommandFB is None and entry.UniqueID == 0
    # a pointer survives the byte image round trip
    entry.pCommandFB = marker
    rt.SysDepMemSet(p + 0, 0, 2)  # only UniqueID
    assert entry.pCommandFB is marker


def test_sizeof_value_of_variable_arrays() -> None:
    assert rt.sizeof_value([Tool(), Tool()], iec.StructType(Tool)) == 2 * rt.type_size(iec.StructType(Tool))
    assert rt.array_type(iec.IecArray(2, [0, 0]), iec.BYTE) == iec.ArrayType(2, 3, iec.BYTE)
