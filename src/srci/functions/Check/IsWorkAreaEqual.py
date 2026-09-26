"""IsWorkAreaEqual

ST-Source: Functions/Check/IsWorkAreaEqual.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
from srci.iec.rt import ADR, SysDepMemCmp, copy_into, copy_value
from srci.types import RobotLibraryConstants, RobotWorkAreaData

__all__ = ['IsWorkAreaEqual']


def IsWorkAreaEqual(*, Data1: RobotWorkAreaData | None = None, Data2: RobotWorkAreaData | None = None, IgnoreTimestamp: bool = False) -> bool:
    if Data1 is None:
        Data1 = RobotWorkAreaData()
    else:
        Data1 = copy_value(Data1)  # VAR_INPUT is a copy in ST
    if Data2 is None:
        Data2 = RobotWorkAreaData()
    else:
        Data2 = copy_value(Data2)  # VAR_INPUT is a copy in ST
    IsWorkAreaEqual: bool = False

    if IgnoreTimestamp:
        copy_into(Data1.Timestamp, Data2.Timestamp)

    IsWorkAreaEqual = SysDepMemCmp(pData1=ADR(Data1, None, _iec.StructType(RobotWorkAreaData)), pData2=ADR(Data2, None, _iec.StructType(RobotWorkAreaData)), DataLen=148) == RobotLibraryConstants.OK
    return IsWorkAreaEqual
