"""IsSwLimitsEqual

ST-Source: Functions/Check/IsSwLimitsEqual.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
from srci.iec.rt import ADR, SysDepMemCmp, copy_into, copy_value
from srci.types import RobotLibraryConstants, SWLimits

__all__ = ['IsSwLimitsEqual']


def IsSwLimitsEqual(*, Data1: SWLimits | None = None, Data2: SWLimits | None = None, IgnoreTimestamp: bool = False) -> bool:
    if Data1 is None:
        Data1 = SWLimits()
    else:
        Data1 = copy_value(Data1)  # VAR_INPUT is a copy in ST
    if Data2 is None:
        Data2 = SWLimits()
    else:
        Data2 = copy_value(Data2)  # VAR_INPUT is a copy in ST
    IsSwLimitsEqual: bool = False

    if IgnoreTimestamp:
        copy_into(Data1.Timestamp, Data2.Timestamp)

    IsSwLimitsEqual = SysDepMemCmp(pData1=ADR(Data1, None, _iec.StructType(SWLimits)), pData2=ADR(Data2, None, _iec.StructType(SWLimits)), DataLen=102) == RobotLibraryConstants.OK
    return IsSwLimitsEqual
