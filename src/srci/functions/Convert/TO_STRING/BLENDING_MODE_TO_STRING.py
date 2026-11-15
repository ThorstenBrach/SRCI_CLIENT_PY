# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      BLENDING_MODE_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-01-23
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

"""BLENDING_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/BLENDING_MODE_TO_STRING.st
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
from srci.types import BlendingMode

__all__ = ['BLENDING_MODE_TO_STRING']


def BLENDING_MODE_TO_STRING(*, Value: BlendingMode = BlendingMode.EXACT_STOP) -> str:
    BLENDING_MODE_TO_STRING: str = ''

    match Value:
        case BlendingMode.EXACT_STOP:
            BLENDING_MODE_TO_STRING = trunc_str(StrReplace(Str='EXACT_STOP ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case BlendingMode.DEFINED_VELOCITY:
            BLENDING_MODE_TO_STRING = trunc_str(StrReplace(Str='DEFINED_VELOCITY ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case BlendingMode.CORNER_DISTANCE:
            BLENDING_MODE_TO_STRING = trunc_str(StrReplace(Str='CORNER_DISTANCE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case BlendingMode.MAX_CORNER_DEVIATION:
            BLENDING_MODE_TO_STRING = trunc_str(StrReplace(Str='MAX_CORNER_DEVIATION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case BlendingMode.CORNER_DISTANCE_2R:
            BLENDING_MODE_TO_STRING = trunc_str(StrReplace(Str='CORNER_DISTANCE_2R ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case BlendingMode.RAMP_OVERLAP:
            BLENDING_MODE_TO_STRING = trunc_str(StrReplace(Str='RAMP_OVERLAP ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case BlendingMode.CORNER_DISTANCE_1R:
            BLENDING_MODE_TO_STRING = trunc_str(StrReplace(Str='CORNER_DISTANCE_1R ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            BLENDING_MODE_TO_STRING = trunc_str(CONCAT('BLENDING_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return BLENDING_MODE_TO_STRING
