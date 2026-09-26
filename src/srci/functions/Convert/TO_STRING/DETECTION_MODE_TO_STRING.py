"""DETECTION_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/DETECTION_MODE_TO_STRING.st
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
from srci.types import DetectionMode

__all__ = ['DETECTION_MODE_TO_STRING']


def DETECTION_MODE_TO_STRING(*, Value: DetectionMode = DetectionMode.TORQUE) -> str:
    DETECTION_MODE_TO_STRING: str = ''

    match Value:
        case DetectionMode.TORQUE:
            DETECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='TORQUE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DetectionMode.FORCE:
            DETECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='FORCE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DetectionMode.ELECTRICAL_CURRENT:
            DETECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='ELECTRICAL_CURRENT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case DetectionMode.FOLLOWING_ERROR:
            DETECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='FOLLOWING_ERROR ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            DETECTION_MODE_TO_STRING = trunc_str(CONCAT('DETECTION_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return DETECTION_MODE_TO_STRING
