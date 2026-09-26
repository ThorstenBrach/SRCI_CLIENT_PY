"""CMD_MESSAGE_STATE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/CMD_MESSAGE_STATE_TO_STRING.st
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
from srci.types import CmdMessageState

__all__ = ['CMD_MESSAGE_STATE_TO_STRING']


def CMD_MESSAGE_STATE_TO_STRING(*, Value: CmdMessageState = CmdMessageState.EMPTY) -> str:
    CMD_MESSAGE_STATE_TO_STRING: str = ''

    match Value:
        case CmdMessageState.EMPTY:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='EMPTY ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.CREATED:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='CREATED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.BUFFERED:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='BUFFERED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.BUFFERED_IN_PLANNER:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='BUFFERED_IN_PLANNER ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.ACTIVE:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='ACTIVE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.INTERRUPTED:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='INTERRUPTED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.ABORT_REQUEST:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='ABORT_REQUEST ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.DONE:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='DONE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.ABORTED:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='ABORTED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case CmdMessageState.ERROR:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            CMD_MESSAGE_STATE_TO_STRING = trunc_str(CONCAT('CMD_MESSAGE_STATE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return CMD_MESSAGE_STATE_TO_STRING
