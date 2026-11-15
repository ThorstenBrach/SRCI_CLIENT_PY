# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      INTERPOLATION_MODE_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-02-01
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

"""INTERPOLATION_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/INTERPOLATION_MODE_TO_STRING.st
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
from srci.types import InterpolationMode

__all__ = ['INTERPOLATION_MODE_TO_STRING']


def INTERPOLATION_MODE_TO_STRING(*, Value: InterpolationMode = InterpolationMode.Linear_interpolation) -> str:
    INTERPOLATION_MODE_TO_STRING: str = ''

    match Value:
        case InterpolationMode.Linear_interpolation:
            INTERPOLATION_MODE_TO_STRING = trunc_str(StrReplace(Str='LINEAR_INTERPOLATION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case InterpolationMode.Direct_interpolation:
            INTERPOLATION_MODE_TO_STRING = trunc_str(StrReplace(Str='DIRECT_INTERPOLATION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            INTERPOLATION_MODE_TO_STRING = trunc_str(CONCAT('INTERPOLATION_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return INTERPOLATION_MODE_TO_STRING
