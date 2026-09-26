"""SPLINE_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/SPLINE_MODE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import UINT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import SplineMode

__all__ = ['SPLINE_MODE_TO_STRING']


def SPLINE_MODE_TO_STRING(*, Value: SplineMode = SplineMode.DISCRETE_POINTS) -> str:
    SPLINE_MODE_TO_STRING: str = ''

    match Value:
        case SplineMode.DISCRETE_POINTS:
            SPLINE_MODE_TO_STRING = trunc_str(StrReplace(Str='DISCRETE_POINTS ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(Value)), 80)
        case SplineMode.BEZIER_SPLINE:
            SPLINE_MODE_TO_STRING = trunc_str(StrReplace(Str='BEZIER_SPLINE ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(Value)), 80)
        case SplineMode.B_SPLINES:
            SPLINE_MODE_TO_STRING = trunc_str(StrReplace(Str='B_SPLINES ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(Value)), 80)
        case SplineMode.CUBIC_HERMITE_SPLINE:
            SPLINE_MODE_TO_STRING = trunc_str(StrReplace(Str='CUBIC_HERMITE_SPLINE ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(Value)), 80)
        case SplineMode.C_SPLINES:
            SPLINE_MODE_TO_STRING = trunc_str(StrReplace(Str='C_SPLINES ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(Value)), 80)
        case _:
            SPLINE_MODE_TO_STRING = trunc_str(CONCAT('SPLINE_MODE_TO_STRING Function: Error -> no parsing for value ', UINT_TO_STRING(Value)), 80)
    return SPLINE_MODE_TO_STRING
