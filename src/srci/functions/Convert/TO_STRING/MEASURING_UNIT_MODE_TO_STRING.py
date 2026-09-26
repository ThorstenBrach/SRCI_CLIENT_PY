"""MEASURING_UNIT_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/MEASURING_UNIT_MODE_TO_STRING.st
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
from srci.types import MeasuringUnitMode

__all__ = ['MEASURING_UNIT_MODE_TO_STRING']


def MEASURING_UNIT_MODE_TO_STRING(*, Value: MeasuringUnitMode = MeasuringUnitMode.VECTOR_LENGTH) -> str:
    MEASURING_UNIT_MODE_TO_STRING: str = ''

    match Value:
        case MeasuringUnitMode.VECTOR_LENGTH:
            MEASURING_UNIT_MODE_TO_STRING = trunc_str(StrReplace(Str='VECTOR_LENGTH ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MeasuringUnitMode.SEGMENT_LENGTH:
            MEASURING_UNIT_MODE_TO_STRING = trunc_str(StrReplace(Str='SEGMENT_LENGTH ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case MeasuringUnitMode.TIME_DURATION:
            MEASURING_UNIT_MODE_TO_STRING = trunc_str(StrReplace(Str='TIME_DURATION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            MEASURING_UNIT_MODE_TO_STRING = trunc_str(CONCAT('MEASURING_UNIT_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return MEASURING_UNIT_MODE_TO_STRING
