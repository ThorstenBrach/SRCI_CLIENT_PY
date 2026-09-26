"""REFERENCE_ELEMENT_TO_STRING

ST-Source: Functions/Convert/TO_STRING/REFERENCE_ELEMENT_TO_STRING.st
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
from srci.types import ReferenceElement

__all__ = ['REFERENCE_ELEMENT_TO_STRING']


def REFERENCE_ELEMENT_TO_STRING(*, Value: ReferenceElement = ReferenceElement.NOT_USED) -> str:
    REFERENCE_ELEMENT_TO_STRING: str = ''

    match Value:
        case ReferenceElement.NOT_USED:
            REFERENCE_ELEMENT_TO_STRING = trunc_str(StrReplace(Str='NOT_USED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ReferenceElement.X_AXIS:
            REFERENCE_ELEMENT_TO_STRING = trunc_str(StrReplace(Str='X_AXIS ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ReferenceElement.Y_AXIS:
            REFERENCE_ELEMENT_TO_STRING = trunc_str(StrReplace(Str='Y_AXIS ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ReferenceElement.Z_AXIS:
            REFERENCE_ELEMENT_TO_STRING = trunc_str(StrReplace(Str='Z_AXIS ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ReferenceElement.XY_PLANE:
            REFERENCE_ELEMENT_TO_STRING = trunc_str(StrReplace(Str='XY_PLANE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ReferenceElement.XZ_PLANE:
            REFERENCE_ELEMENT_TO_STRING = trunc_str(StrReplace(Str='XZ_PLANE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ReferenceElement.YZ_PLANE:
            REFERENCE_ELEMENT_TO_STRING = trunc_str(StrReplace(Str='YZ_PLANE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            REFERENCE_ELEMENT_TO_STRING = trunc_str(CONCAT('REFERENCE_ELEMENT_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return REFERENCE_ELEMENT_TO_STRING
