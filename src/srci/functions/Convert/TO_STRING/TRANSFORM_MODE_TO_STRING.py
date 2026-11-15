# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      TRANSFORM_MODE_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-01-24
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

"""TRANSFORM_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TRANSFORM_MODE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import SINT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import TransformMode

__all__ = ['TRANSFORM_MODE_TO_STRING']


def TRANSFORM_MODE_TO_STRING(*, Value: TransformMode = TransformMode.MIRROR_AT_POINT) -> str:
    TRANSFORM_MODE_TO_STRING: str = ''

    match Value:
        case TransformMode.MIRROR_AT_POINT:
            TRANSFORM_MODE_TO_STRING = trunc_str(StrReplace(Str='MIRROR_AT_POINT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TransformMode.MIRROR_AT_STRAIGHT_LINE:
            TRANSFORM_MODE_TO_STRING = trunc_str(StrReplace(Str='MIRROR_AT_STRAIGHT_LINE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TransformMode.MIRROR_AT_PLANE:
            TRANSFORM_MODE_TO_STRING = trunc_str(StrReplace(Str='MIRROR_AT_PLANE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TransformMode.ROTATE_AROUND_STRAIGHT_LINE:
            TRANSFORM_MODE_TO_STRING = trunc_str(StrReplace(Str='ROTATE_AROUND_STRAIGHT_LINE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TransformMode.SHIFT_BY_VECTOR:
            TRANSFORM_MODE_TO_STRING = trunc_str(StrReplace(Str='SHIFT_BY_VECTOR ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            TRANSFORM_MODE_TO_STRING = trunc_str(CONCAT('TRANSFORM_MODE_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return TRANSFORM_MODE_TO_STRING
