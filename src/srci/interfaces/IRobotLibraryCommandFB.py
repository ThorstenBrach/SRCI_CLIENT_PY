"""IRobotLibraryCommandFB

ST-Source: Interfaces/IRobotLibraryCommandFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing import Protocol

if TYPE_CHECKING:
    from srci.fb._internal.Send.RobotLibrarySendDataFB import RobotLibrarySendDataFB
    from srci.types import AxesGroupAcyclicAcrEntryRspBuffer

__all__ = ['IRobotLibraryCommandFB']


class IRobotLibraryCommandFB(Protocol):
    def CallBack(self, *, RspData: AxesGroupAcyclicAcrEntryRspBuffer | None = None) -> int: ...
    CommandData: RobotLibrarySendDataFB
