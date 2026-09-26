# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.types.test_iec_misc
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#
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

import pytest

from srci import types as T
from srci.errors import ValueRangeError
from srci.iec.sizeof import SIZEOF, sizeof_type
from srci.iec.types import bit, check_range, set_bit
from srci.types import iec


def test_sizeof_pack_mode_1() -> None:
    assert SIZEOF(T.TelegramPlcToRobHeader) == 18
    assert SIZEOF(T.TelegramRobToPlcFragmentHeader()) == 8
    assert SIZEOF(T.VersionStruct) == 3
    assert sizeof_type(iec.StringType(20)) == 21
    assert sizeof_type(iec.ArrayType(1, 4, iec.REAL)) == 16
    assert sizeof_type(iec.EnumType(T.ArmConfigElbow)) == 2
    with pytest.raises(TypeError):
        SIZEOF(42)
    with pytest.raises(TypeError):
        sizeof_type(iec.PointerType("X"))


def test_bits_and_ranges() -> None:
    assert bit(0b100, 2) and not bit(0b100, 1)
    assert set_bit(0, 3, True) == 8 and set_bit(15, 0, False) == 14
    check_range(255, iec.BYTE)
    for bad in (256, -1, 1.5):
        with pytest.raises(ValueRangeError):
            check_range(bad, iec.BYTE)
    check_range(-1.5, iec.REAL)


def test_enum_accepts_undefined_values_of_the_base_type() -> None:
    m = T.OperationMode(0)
    assert m.name == "UNDEFINED_0" and m == 0 and m is T.OperationMode(0)
    assert T.OperationMode(0) not in list(T.OperationMode)
    with pytest.raises(ValueError):
        T.ArmConfigElbow(1 << 20)  # outside INT
    with pytest.raises(ValueError):
        T.ArmConfigElbow("x")  # type: ignore[arg-type]
