"""TRIGGER_REACTION_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TRIGGER_REACTION_MODE_TO_STRING.st
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
from srci.types import TriggerReactionMode

__all__ = ['TRIGGER_REACTION_MODE_TO_STRING']


def TRIGGER_REACTION_MODE_TO_STRING(*, Value: TriggerReactionMode = TriggerReactionMode.NO_REACTION) -> str:
    TRIGGER_REACTION_MODE_TO_STRING: str = ''

    match Value:

        case TriggerReactionMode.NO_REACTION:
            TRIGGER_REACTION_MODE_TO_STRING = trunc_str(StrReplace(Str='NO_REACTION ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerReactionMode.INTERRUPT:
            TRIGGER_REACTION_MODE_TO_STRING = trunc_str(StrReplace(Str='INTERRUPT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerReactionMode.GROUP_STOP:
            TRIGGER_REACTION_MODE_TO_STRING = trunc_str(StrReplace(Str='GROUP_STOP ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerReactionMode.DISABLE_ROBOT:
            TRIGGER_REACTION_MODE_TO_STRING = trunc_str(StrReplace(Str='DISABLE_ROBOT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerReactionMode.STOP_ACTUAL_MOTION_COMMAND:
            TRIGGER_REACTION_MODE_TO_STRING = trunc_str(StrReplace(Str='STOP_ACTUAL_MOTION_COMMAND ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            TRIGGER_REACTION_MODE_TO_STRING = trunc_str(CONCAT('TRIGGER_REACTION_MODE_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return TRIGGER_REACTION_MODE_TO_STRING
