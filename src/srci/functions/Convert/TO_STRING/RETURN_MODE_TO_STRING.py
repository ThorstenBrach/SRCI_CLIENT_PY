"""RETURN_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/RETURN_MODE_TO_STRING.st
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
from srci.types import ReturnMode

__all__ = ['RETURN_MODE_TO_STRING']


def RETURN_MODE_TO_STRING(*, Value: ReturnMode = ReturnMode.INTERRUPT_POSITION) -> str:
    RETURN_MODE_TO_STRING: str = ''

    match Value:
        case ReturnMode.INTERRUPT_POSITION:
            RETURN_MODE_TO_STRING = trunc_str(StrReplace(Str='INTERRUPT_POSITION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ReturnMode.END_POSITION:
            RETURN_MODE_TO_STRING = trunc_str(StrReplace(Str='END_POSITION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            RETURN_MODE_TO_STRING = trunc_str(CONCAT('RETURN_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return RETURN_MODE_TO_STRING
