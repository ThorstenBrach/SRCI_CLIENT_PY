"""OPERATION_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/OPERATION_MODE_TO_STRING.st
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
from srci.types import OperationMode

__all__ = ['OPERATION_MODE_TO_STRING']


def OPERATION_MODE_TO_STRING(*, Value: OperationMode = OperationMode.T1_LOCAL) -> str:
    OPERATION_MODE_TO_STRING: str = ''

    match Value:
        case OperationMode.T1_LOCAL:
            OPERATION_MODE_TO_STRING = trunc_str(StrReplace(Str='T1_LOCAL ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case OperationMode.T2_LOCAL:
            OPERATION_MODE_TO_STRING = trunc_str(StrReplace(Str='T2_LOCAL ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case OperationMode.AUTO:
            OPERATION_MODE_TO_STRING = trunc_str(StrReplace(Str='AUTO ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case OperationMode.AUTO_EXT:
            OPERATION_MODE_TO_STRING = trunc_str(StrReplace(Str='AUTO_EXT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case OperationMode.T1_EXT:
            OPERATION_MODE_TO_STRING = trunc_str(StrReplace(Str='T1_EXT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case OperationMode.T2_EXT:
            OPERATION_MODE_TO_STRING = trunc_str(StrReplace(Str='T2_EXT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            OPERATION_MODE_TO_STRING = trunc_str(CONCAT('OPERATION_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return OPERATION_MODE_TO_STRING
