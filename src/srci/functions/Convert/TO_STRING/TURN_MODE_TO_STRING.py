"""TURN_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TURN_MODE_TO_STRING.st
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
from srci.types import TurnMode

__all__ = ['TURN_MODE_TO_STRING']


def TURN_MODE_TO_STRING(*, Value: TurnMode = TurnMode.USE_TURN_NUMBER) -> str:
    TURN_MODE_TO_STRING: str = ''

    match Value:
        case TurnMode.USE_TURN_NUMBER:
            TURN_MODE_TO_STRING = trunc_str(StrReplace(Str='USE_TURN_NUMBER ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case TurnMode.SAME:
            TURN_MODE_TO_STRING = trunc_str(StrReplace(Str='SAME ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case TurnMode.FREE:
            TURN_MODE_TO_STRING = trunc_str(StrReplace(Str='FREE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            TURN_MODE_TO_STRING = trunc_str(CONCAT('TURN_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return TURN_MODE_TO_STRING
