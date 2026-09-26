"""LOG_LEVEL_TO_STRING

ST-Source: Functions/Convert/TO_STRING/LOG_LEVEL_TO_STRING.st
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
from srci.types import LogLevel, Severity

__all__ = ['LOG_LEVEL_TO_STRING']


def LOG_LEVEL_TO_STRING(*, Value: Severity = Severity.DEACTIVATE) -> str:
    LOG_LEVEL_TO_STRING: str = ''

    match Value:
        case Severity.DEACTIVATE:
            LOG_LEVEL_TO_STRING = trunc_str(StrReplace(Str='DEACTIVATE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case Severity.DEBUG:
            LOG_LEVEL_TO_STRING = trunc_str(StrReplace(Str='DEBUG ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case Severity.INFO:
            LOG_LEVEL_TO_STRING = trunc_str(StrReplace(Str='INFO ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case Severity.WARNING:
            LOG_LEVEL_TO_STRING = trunc_str(StrReplace(Str='WARNING ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case Severity.ERROR:
            LOG_LEVEL_TO_STRING = trunc_str(StrReplace(Str='ERROR ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case Severity.FATAL_ERROR:
            LOG_LEVEL_TO_STRING = trunc_str(StrReplace(Str='FATAL_ERROR ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            LOG_LEVEL_TO_STRING = trunc_str(CONCAT('LOG_LEVEL_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return LOG_LEVEL_TO_STRING
