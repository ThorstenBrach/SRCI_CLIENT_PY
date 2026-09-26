"""ARM_CONFIG_ELBOW_TO_STRING

ST-Source: Functions/Convert/TO_STRING/ARM_CONFIG_ELBOW_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import INT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import ArmConfigElbow

__all__ = ['ARM_CONFIG_ELBOW_TO_STRING']


def ARM_CONFIG_ELBOW_TO_STRING(*, Value: ArmConfigElbow = ArmConfigElbow.USE_CONFIG) -> str:
    ARM_CONFIG_ELBOW_TO_STRING: str = ''

    match Value:
        case ArmConfigElbow.USE_CONFIG:
            ARM_CONFIG_ELBOW_TO_STRING = trunc_str(StrReplace(Str='Elbow = USE_CONFIG ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case ArmConfigElbow.SAME:
            ARM_CONFIG_ELBOW_TO_STRING = trunc_str(StrReplace(Str='Elbow = SAME ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case ArmConfigElbow.FREE:
            ARM_CONFIG_ELBOW_TO_STRING = trunc_str(StrReplace(Str='Elbow = FREE ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case ArmConfigElbow.DOWN:
            ARM_CONFIG_ELBOW_TO_STRING = trunc_str(StrReplace(Str='Elbow = DOWN ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case ArmConfigElbow.UP:
            ARM_CONFIG_ELBOW_TO_STRING = trunc_str(StrReplace(Str='Elbow = UP ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case _:
            ARM_CONFIG_ELBOW_TO_STRING = trunc_str(CONCAT('ARM_CONFIG_ELBOW_TO_STRING Function: Error -> no parsing for value ', INT_TO_STRING(Value)), 80)
    return ARM_CONFIG_ELBOW_TO_STRING
