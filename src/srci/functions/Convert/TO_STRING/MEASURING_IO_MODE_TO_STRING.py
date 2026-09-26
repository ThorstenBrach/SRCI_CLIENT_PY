# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MEASURING_IO_MODE_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-02-23
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

"""MEASURING_IO_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/MEASURING_IO_MODE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import USINT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import MeasuringIoMode

__all__ = ['MEASURING_IO_MODE_TO_STRING']


def MEASURING_IO_MODE_TO_STRING(*, Value: MeasuringIoMode = MeasuringIoMode.MEASUREMENT_AT_NEXT_RISING_EDGE) -> str:
    MEASURING_IO_MODE_TO_STRING: str = ''

    match Value:
        case MeasuringIoMode.MEASUREMENT_AT_NEXT_RISING_EDGE:
            MEASURING_IO_MODE_TO_STRING = trunc_str(StrReplace(Str='MEASUREMENT_AT_NEXT_RISING_EDGE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MeasuringIoMode.MEASUREMENT_AT_NEXT_FALLING_EDGE:
            MEASURING_IO_MODE_TO_STRING = trunc_str(StrReplace(Str='MEASUREMENT_AT_NEXT_FALLING_EDGE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MeasuringIoMode.MEASUREMENT_AT_NEXT_EDGE:
            MEASURING_IO_MODE_TO_STRING = trunc_str(StrReplace(Str='MEASUREMENT_AT_NEXT_EDGE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MeasuringIoMode.MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_RISING:
            MEASURING_IO_MODE_TO_STRING = trunc_str(StrReplace(Str='MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_RISING ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MeasuringIoMode.MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_FALLING:
            MEASURING_IO_MODE_TO_STRING = trunc_str(StrReplace(Str='MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_FALLING ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            MEASURING_IO_MODE_TO_STRING = trunc_str(CONCAT('MEASURING_IO_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return MEASURING_IO_MODE_TO_STRING
