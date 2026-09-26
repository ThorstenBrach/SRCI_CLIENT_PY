"""TRIGGER_CONDITION_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TRIGGER_CONDITION_TO_STRING.st
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
from srci.types import TriggerCondition

__all__ = ['TRIGGER_CONDITION_TO_STRING']


def TRIGGER_CONDITION_TO_STRING(*, Value: TriggerCondition = TriggerCondition.TARGET_POSITION_TIME_MS) -> str:
    TRIGGER_CONDITION_TO_STRING: str = ''

    match Value:
        case TriggerCondition.TARGET_POSITION_TIME_MS:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='TARGET_POSITION_TIME_MS ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.TARGET_POSITION_TCP_VELOCITY_ABSOLUTE:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='TARGET_POSITION_TCP_VELOCITY_ABSOLUTE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.TARGET_POSITION_TCP_VELOCITY_PERCENT:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='TARGET_POSITION_TCP_VELOCITY_PERCENT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.TARGET_POSITION_DISTANCE_ABSOLUTE:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='TARGET_POSITION_DISTANCE_ABSOLUTE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.TARGET_POSITION_DISTANCE_PERCENT:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='TARGET_POSITION_DISTANCE_PERCENT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.UNDEFINED:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='UNDEFINED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.START_POSITION_DISTANCE_PERCENT:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='START_POSITION_DISTANCE_PERCENT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.START_POSITION_DISTANCE_ABSOLUTE:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='START_POSITION_DISTANCE_ABSOLUTE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.START_POSITION_TCP_VELOCITY_PERCENT:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='START_POSITION_TCP_VELOCITY_PERCENT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.START_POSITION_TCP_VELOCIT_ABSOLUTE:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='START_POSITION_TCP_VELOCIT_ABSOLUTE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerCondition.START_POSITION_TIME_MS:
            TRIGGER_CONDITION_TO_STRING = trunc_str(StrReplace(Str='START_POSITION_TCP_VELOCIT_ABSOLUTE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            TRIGGER_CONDITION_TO_STRING = trunc_str(CONCAT('TRIGGER_CONDITION_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return TRIGGER_CONDITION_TO_STRING
