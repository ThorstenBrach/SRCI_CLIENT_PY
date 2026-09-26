# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      CIRC_PLANE_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-01-30
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

"""CIRC_PLANE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/CIRC_PLANE_TO_STRING.st
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
from srci.types import CircPlane

__all__ = ['CIRC_PLANE_TO_STRING']


def CIRC_PLANE_TO_STRING(*, Value: CircPlane = CircPlane.XZ_PLANE) -> str:
    CIRC_PLANE_TO_STRING: str = ''

    match Value:
        case CircPlane.XZ_PLANE:
            CIRC_PLANE_TO_STRING = trunc_str(StrReplace(Str='XZ_PLANE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case CircPlane.YZ_PLANE:
            CIRC_PLANE_TO_STRING = trunc_str(StrReplace(Str='YZ_PLANE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case CircPlane.XY_PLANE:
            CIRC_PLANE_TO_STRING = trunc_str(StrReplace(Str='XY_PLANE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            CIRC_PLANE_TO_STRING = trunc_str(CONCAT('CIRC_PLANE_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return CIRC_PLANE_TO_STRING
