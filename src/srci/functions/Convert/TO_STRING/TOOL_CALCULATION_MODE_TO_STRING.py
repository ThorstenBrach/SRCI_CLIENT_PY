"""TOOL_CALCULATION_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TOOL_CALCULATION_MODE_TO_STRING.st
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
from srci.types import ToolCalculationMode

__all__ = ['TOOL_CALCULATION_MODE_TO_STRING']


def TOOL_CALCULATION_MODE_TO_STRING(*, Value: ToolCalculationMode = ToolCalculationMode.TWO_POINT_Z_METHOD) -> str:
    TOOL_CALCULATION_MODE_TO_STRING: str = ''

    match Value:
        case ToolCalculationMode.TWO_POINT_Z_METHOD:
            TOOL_CALCULATION_MODE_TO_STRING = trunc_str(StrReplace(Str='TWO_POINT_Z_METHOD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ToolCalculationMode.THREE_POINT_METHOD:
            TOOL_CALCULATION_MODE_TO_STRING = trunc_str(StrReplace(Str='THREE_POINT_METHOD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ToolCalculationMode.FOUR_POINT_METHOD:
            TOOL_CALCULATION_MODE_TO_STRING = trunc_str(StrReplace(Str='FOUR_POINT_METHOD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ToolCalculationMode.FIVE_POINT_METHOD:
            TOOL_CALCULATION_MODE_TO_STRING = trunc_str(StrReplace(Str='FIVE_POINT_METHOD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ToolCalculationMode.SIX_POINT_METHOD:
            TOOL_CALCULATION_MODE_TO_STRING = trunc_str(StrReplace(Str='SIX_POINT_METHOD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ToolCalculationMode.ABC_WORLD_METHOD:
            TOOL_CALCULATION_MODE_TO_STRING = trunc_str(StrReplace(Str='ABC_WORLD_METHOD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case ToolCalculationMode.ABC_TWO_POINT_METHOD:
            TOOL_CALCULATION_MODE_TO_STRING = trunc_str(StrReplace(Str='ABC_TWO_POINT_METHOD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            TOOL_CALCULATION_MODE_TO_STRING = trunc_str(CONCAT('TOOL_CALCULATION_MODE_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return TOOL_CALCULATION_MODE_TO_STRING
