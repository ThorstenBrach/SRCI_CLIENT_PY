"""LOAD_MEASUREMENT_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/LOAD_MEASUREMENT_MODE_TO_STRING.st
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
from srci.types import LoadMeasurementMode

__all__ = ['LOAD_MEASUREMENT_MODE_TO_STRING']


def LOAD_MEASUREMENT_MODE_TO_STRING(*, Value: LoadMeasurementMode = LoadMeasurementMode.ONE_POSITION) -> str:
    LOAD_MEASUREMENT_MODE_TO_STRING: str = ''

    match Value:
        case LoadMeasurementMode.ONE_POSITION:
            LOAD_MEASUREMENT_MODE_TO_STRING = trunc_str(StrReplace(Str='ONE_POSITION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case LoadMeasurementMode.CONFIGURATION_ANGLE:
            LOAD_MEASUREMENT_MODE_TO_STRING = trunc_str(StrReplace(Str='CONFIGURATION_ANGLE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case LoadMeasurementMode.AREA:
            LOAD_MEASUREMENT_MODE_TO_STRING = trunc_str(StrReplace(Str='AREA ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case LoadMeasurementMode.TWO_POSITIONS:
            LOAD_MEASUREMENT_MODE_TO_STRING = trunc_str(StrReplace(Str='TWO_POSITIONS ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            LOAD_MEASUREMENT_MODE_TO_STRING = trunc_str(CONCAT('LOAD_MEASUREMENT_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return LOAD_MEASUREMENT_MODE_TO_STRING
