# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      DATA_TYPE_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-03-05
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

"""DATA_TYPE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/DATA_TYPE_TO_STRING.st
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
from srci.types import DataType

__all__ = ['DATA_TYPE_TO_STRING']


def DATA_TYPE_TO_STRING(*, Value: DataType = DataType.TYPE_BOOL) -> str:
    DATA_TYPE_TO_STRING: str = ''

    match Value:
        case DataType.TYPE_BOOL:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='BOOL ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_BYTE:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='BYTE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_WORD:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='WORD ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_DWORD:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='DWORD ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_SINT:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='SINT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_USINT:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='USINT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_INT:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='INT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_UINT:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='UINT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_DINT:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='DINT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_UDINT:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='UDINT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_REAL:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='REAL ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_CHAR:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='CHAR ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DataType.TYPE_CHAR_ARRAY:
            DATA_TYPE_TO_STRING = trunc_str(StrReplace(Str='ARRAY[0..3] OF CHAR ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            DATA_TYPE_TO_STRING = trunc_str(CONCAT('DATA_TYPE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return DATA_TYPE_TO_STRING
