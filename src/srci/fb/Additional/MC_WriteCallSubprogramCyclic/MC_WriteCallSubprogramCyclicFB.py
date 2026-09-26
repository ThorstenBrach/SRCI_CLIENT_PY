# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_WriteCallSubprogramCyclicFB
#  Author:      Thorsten Brach
#  Date:        2024-06-01
#
#  Description:
#    Writes cyclic data of called subprogram
#
#  Copyright:
#    (C) 2024 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""Writes cyclic data of called subprogram

ST-Source: POUs/Additional/MC_WriteCallSubprogramCyclic/MC_WriteCallSubprogramCyclicFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import srci.types as _T
from srci.fb._internal.BaseFBs.RobotLibraryBaseEnableFB import RobotLibraryBaseEnableFB
from srci.iec.rt import copy_into, trunc_str
from srci.types import ExecutionMode, PriorityLevel, Severity, WriteCallSubprogramCyclicOutCmd, WriteCallSubprogramCyclicParCmd

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_WriteCallSubprogramCyclicFB']


class MC_WriteCallSubprogramCyclicFB(RobotLibraryBaseEnableFB):
    """Writes cyclic data of called subprogram"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: WriteCallSubprogramCyclicParCmd = WriteCallSubprogramCyclicParCmd()
        # VAR_OUTPUT
        # command outputs
        self.OutCmd: WriteCallSubprogramCyclicOutCmd = WriteCallSubprogramCyclicOutCmd()

    def __call__(self, *, ParCmd: WriteCallSubprogramCyclicParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ParCmd is not None:
            copy_into(self.ParCmd, ParCmd)
        if Enable is not None:
            self.Enable = Enable
        if Name is not None:
            self.Name = trunc_str(Name, 80)
        if ExecMode is not None:
            self.ExecMode = ExecutionMode(ExecMode)
        if Priority is not None:
            self.Priority = PriorityLevel(Priority)
        if AxesGroup is not None:
            self.AxesGroup = AxesGroup
        if InternalLogger is not None:
            self.InternalLogger = InternalLogger
        if ExternalLogger is not None:
            self.ExternalLogger = ExternalLogger
        if LogLevel is not None:
            self.LogLevel = Severity(LogLevel)
        self.__body()

    def __body(self) -> None:
        super().__call__(AxesGroup=self.AxesGroup)

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.WriteCallSubprogramCyclic

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_WriteCallSubprogramCyclicFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnExecErrorClear(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecErrorClear: int = 0

        # Overwrite base implementation, because FB does not send telegrams via ACR
        OnExecErrorClear = self.Reset()
        return OnExecErrorClear

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecRun: int = 0

        # call base implementation
        super().OnExecRun(AxesGroup=AxesGroup)

        AxesGroup.Parameter.Plc.OptionalCyclic.UseCallSubprogram = self.Enable

        # {warning 'ToDo: modify like MC_ReadActualPositionCyclic'}
        self.Enabled = AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Active
        self.Busy = self.Enabled != self.Enable

        copy_into(AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Data, self.ParCmd.Data)
        return OnExecRun
