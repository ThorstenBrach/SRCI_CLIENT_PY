# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      ROBOT_AXES_FLAGS_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-02-26
#
#  Description:
#
#
#  Copyright:
#    (C) 2025 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""ROBOT_AXES_FLAGS_TO_STRING

ST-Source: Functions/Convert/TO_STRING/ROBOT_AXES_FLAGS_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.Convert.TO_STRING.BYTE_TO_STRING_BIN import BYTE_TO_STRING_BIN
from srci.iec.rt import bit, set_bit
from srci.types import RobotAxesFlags

__all__ = ['ROBOT_AXES_FLAGS_TO_STRING']


def ROBOT_AXES_FLAGS_TO_STRING(*, Value: RobotAxesFlags | None = None) -> str:
    if Value is None:
        Value = RobotAxesFlags()
    ROBOT_AXES_FLAGS_TO_STRING: str = ''
    _tmpByte: int = 0

    _tmpByte = set_bit(_tmpByte, 0, Value.Bit00)
    _tmpByte = set_bit(_tmpByte, 1, Value.AxisJ1)
    _tmpByte = set_bit(_tmpByte, 2, Value.AxisJ2)
    _tmpByte = set_bit(_tmpByte, 3, Value.AxisJ3)
    _tmpByte = set_bit(_tmpByte, 4, Value.AxisJ4)
    _tmpByte = set_bit(_tmpByte, 5, Value.AxisJ5)
    _tmpByte = set_bit(_tmpByte, 6, Value.AxisJ6)
    _tmpByte = set_bit(_tmpByte, 7, Value.Bit07)

    ROBOT_AXES_FLAGS_TO_STRING = BYTE_TO_STRING_BIN(Value=_tmpByte)
    return ROBOT_AXES_FLAGS_TO_STRING
