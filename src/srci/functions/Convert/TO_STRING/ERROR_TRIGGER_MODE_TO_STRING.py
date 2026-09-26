"""ERROR_TRIGGER_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/ERROR_TRIGGER_MODE_TO_STRING.st
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
from srci.types import ErrorTriggerMode

__all__ = ['ERROR_TRIGGER_MODE_TO_STRING']


def ERROR_TRIGGER_MODE_TO_STRING(*, Value: ErrorTriggerMode = ErrorTriggerMode.ANY_COMMAND) -> str:
    ERROR_TRIGGER_MODE_TO_STRING: str = ''

    match Value:
        case ErrorTriggerMode.ANY_COMMAND:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='ANY_COMMAND ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.GENERAL_COMMANDS:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='GENERAL_COMMANDS ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.ADMINISTRATIVE_COMMANDS:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='ADMINISTRATIVE_COMMANDS ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.MOVE_COMMANDS:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='MOVE_COMMANDS ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.PERIPHERY_COMMANDS:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='PERIPHERY_COMMANDS ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.EXTENDED_COMMANDS:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='EXTENDED_COMMANDS ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.SPECIFIC_COMMAND_OR_RI_MESSAGE:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='SPECIFIC_COMMAND_OR_RI_MESSAGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.SPECIFIC_RC_OR_RA_MESSAGE_CODE:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='SPECIFIC_RC_OR_RA_MESSAGE_CODE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.ANY_RI_MESSAGE_CODE:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='ANY_RI_MESSAGE_CODE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ErrorTriggerMode.ANY_RC_OR_RA_MESSAGE_CODE:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(StrReplace(Str='ANY_RC_OR_RA_MESSAGE_CODE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            ERROR_TRIGGER_MODE_TO_STRING = trunc_str(CONCAT('ERROR_TRIGGER_MODE_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return ERROR_TRIGGER_MODE_TO_STRING
