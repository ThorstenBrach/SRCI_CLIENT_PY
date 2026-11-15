# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      ORI_MODE_TO_STRING
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

"""ORI_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/ORI_MODE_TO_STRING.st
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
from srci.types import OriMode

__all__ = ['ORI_MODE_TO_STRING']


def ORI_MODE_TO_STRING(*, Value: OriMode = OriMode.LINEAR_INTERPOLATED) -> str:
    ORI_MODE_TO_STRING: str = ''

    match Value:
        case OriMode.LINEAR_INTERPOLATED:
            ORI_MODE_TO_STRING = trunc_str(StrReplace(Str='LINEAR_INTERPOLATED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case OriMode.JOINT_INTERPOLATED:
            ORI_MODE_TO_STRING = trunc_str(StrReplace(Str='JOINT_INTERPOLATED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case OriMode.FIX:
            ORI_MODE_TO_STRING = trunc_str(StrReplace(Str='FIX ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case OriMode.PATH:
            ORI_MODE_TO_STRING = trunc_str(StrReplace(Str='PATH ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            ORI_MODE_TO_STRING = trunc_str(CONCAT('ORI_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return ORI_MODE_TO_STRING
