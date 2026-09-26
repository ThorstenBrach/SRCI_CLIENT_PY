"""ABORTING_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/ABORTING_MODE_TO_STRING.st
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
from srci.types import AbortingMode

__all__ = ['ABORTING_MODE_TO_STRING']


def ABORTING_MODE_TO_STRING(*, Value: AbortingMode = AbortingMode.BUFFER) -> str:
    ABORTING_MODE_TO_STRING: str = ''

    match Value:
        case AbortingMode.BUFFER:
            ABORTING_MODE_TO_STRING = trunc_str(StrReplace(Str='BUFFER ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case AbortingMode.ABORT:
            ABORTING_MODE_TO_STRING = trunc_str(StrReplace(Str='ABORT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            ABORTING_MODE_TO_STRING = trunc_str(CONCAT('ABORTING_MODE_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return ABORTING_MODE_TO_STRING
