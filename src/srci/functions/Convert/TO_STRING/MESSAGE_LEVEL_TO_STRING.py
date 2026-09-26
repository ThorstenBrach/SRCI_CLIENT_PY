"""MESSAGE_LEVEL_TO_STRING

ST-Source: Functions/Convert/TO_STRING/MESSAGE_LEVEL_TO_STRING.st
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
from srci.types import MessageLevel

__all__ = ['MESSAGE_LEVEL_TO_STRING']


def MESSAGE_LEVEL_TO_STRING(*, Value: MessageLevel = MessageLevel.DEBUG) -> str:
    MESSAGE_LEVEL_TO_STRING: str = ''

    match Value:
        case MessageLevel.DEBUG:
            MESSAGE_LEVEL_TO_STRING = trunc_str(StrReplace(Str='DEBUG ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MessageLevel.INFO:
            MESSAGE_LEVEL_TO_STRING = trunc_str(StrReplace(Str='INFO ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MessageLevel.WARNING:
            MESSAGE_LEVEL_TO_STRING = trunc_str(StrReplace(Str='WARNING ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MessageLevel.ERROR:
            MESSAGE_LEVEL_TO_STRING = trunc_str(StrReplace(Str='ERROR ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            MESSAGE_LEVEL_TO_STRING = trunc_str(CONCAT('MESSAGE_LEVEL_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return MESSAGE_LEVEL_TO_STRING
