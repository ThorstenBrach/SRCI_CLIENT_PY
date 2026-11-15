# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      REFERENCE_TYPE_TO_STRING
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

"""REFERENCE_TYPE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/REFERENCE_TYPE_TO_STRING.st
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
from srci.types import ReferenceType

__all__ = ['REFERENCE_TYPE_TO_STRING']


def REFERENCE_TYPE_TO_STRING(*, Value: ReferenceType = ReferenceType.TOOL) -> str:
    REFERENCE_TYPE_TO_STRING: str = ''

    match Value:
        case ReferenceType.TOOL:
            REFERENCE_TYPE_TO_STRING = trunc_str(StrReplace(Str='TOOL ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ReferenceType.FRAME:
            REFERENCE_TYPE_TO_STRING = trunc_str(StrReplace(Str='FRAME ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            REFERENCE_TYPE_TO_STRING = trunc_str(CONCAT('REFERENCE_TYPE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return REFERENCE_TYPE_TO_STRING
