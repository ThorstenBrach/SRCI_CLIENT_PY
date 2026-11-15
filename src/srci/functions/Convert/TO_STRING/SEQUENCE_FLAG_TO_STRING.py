# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      SEQUENCE_FLAG_TO_STRING
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

"""SEQUENCE_FLAG_TO_STRING

ST-Source: Functions/Convert/TO_STRING/SEQUENCE_FLAG_TO_STRING.st
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
from srci.types import SequenceFlag

__all__ = ['SEQUENCE_FLAG_TO_STRING']


def SEQUENCE_FLAG_TO_STRING(*, Value: SequenceFlag = SequenceFlag.NO_SEQUENCE) -> str:
    SEQUENCE_FLAG_TO_STRING: str = ''

    match Value:
        case SequenceFlag.NO_SEQUENCE:
            SEQUENCE_FLAG_TO_STRING = trunc_str(StrReplace(Str='NO_SEQUENCE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case SequenceFlag.PRIMARY_SEQUENCE:
            SEQUENCE_FLAG_TO_STRING = trunc_str(StrReplace(Str='PRIMARY_SEQUENCE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case SequenceFlag.SECONDARY_SEQUENCE:
            SEQUENCE_FLAG_TO_STRING = trunc_str(StrReplace(Str='SECONDARY_SEQUENCE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            SEQUENCE_FLAG_TO_STRING = trunc_str(CONCAT('SEQUENCE_FLAG_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return SEQUENCE_FLAG_TO_STRING
