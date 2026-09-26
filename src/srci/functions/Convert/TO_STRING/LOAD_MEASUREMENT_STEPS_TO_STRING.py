"""LOAD_MEASUREMENT_STEPS_TO_STRING

ST-Source: Functions/Convert/TO_STRING/LOAD_MEASUREMENT_STEPS_TO_STRING.st
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
from srci.types import LoadMeasurementSteps

__all__ = ['LOAD_MEASUREMENT_STEPS_TO_STRING']


def LOAD_MEASUREMENT_STEPS_TO_STRING(*, Value: LoadMeasurementSteps = LoadMeasurementSteps.RESET) -> str:
    LOAD_MEASUREMENT_STEPS_TO_STRING: str = ''

    match Value:
        case LoadMeasurementSteps.RESET:
            LOAD_MEASUREMENT_STEPS_TO_STRING = trunc_str(StrReplace(Str='RESET ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case LoadMeasurementSteps.FIRST_POSITION:
            LOAD_MEASUREMENT_STEPS_TO_STRING = trunc_str(StrReplace(Str='FIRST_POSITION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case LoadMeasurementSteps.SECOND_POSITION:
            LOAD_MEASUREMENT_STEPS_TO_STRING = trunc_str(StrReplace(Str='SECOND_POSITION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case LoadMeasurementSteps.THIRD_POSITION:
            LOAD_MEASUREMENT_STEPS_TO_STRING = trunc_str(StrReplace(Str='THIRD_POSITION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case LoadMeasurementSteps.FOURTH_POSITION:
            LOAD_MEASUREMENT_STEPS_TO_STRING = trunc_str(StrReplace(Str='FOURTH_POSITION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case LoadMeasurementSteps.LOAD_CALCULATION:
            LOAD_MEASUREMENT_STEPS_TO_STRING = trunc_str(StrReplace(Str='LOAD_CALCULATION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            LOAD_MEASUREMENT_STEPS_TO_STRING = trunc_str(CONCAT('LOAD_MEASUREMENT_STEPS_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return LOAD_MEASUREMENT_STEPS_TO_STRING
