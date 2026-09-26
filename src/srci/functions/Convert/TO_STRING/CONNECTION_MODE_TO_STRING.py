"""CONNECTION_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/CONNECTION_MODE_TO_STRING.st
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
from srci.types import ConnectionMode

__all__ = ['CONNECTION_MODE_TO_STRING']


def CONNECTION_MODE_TO_STRING(*, Value: ConnectionMode = ConnectionMode.RC_CONNECTED) -> str:
    CONNECTION_MODE_TO_STRING: str = ''

    match Value:
        case ConnectionMode.RC_CONNECTED:
            CONNECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='RC_CONNECTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ConnectionMode.PLC_CONNECTED:
            CONNECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='PLC_CONNECTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            CONNECTION_MODE_TO_STRING = trunc_str(CONCAT('CONNECTION_MODE_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return CONNECTION_MODE_TO_STRING
