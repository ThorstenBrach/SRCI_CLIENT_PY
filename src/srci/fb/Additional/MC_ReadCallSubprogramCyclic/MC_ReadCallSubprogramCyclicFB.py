"""Reads cyclic data of called subprogram

ST-Source: POUs/Additional/MC_ReadCallSubprogramCyclic/MC_ReadCallSubprogramCyclicFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
import srci.types as _T
from srci.fb._internal.BaseFBs.RobotLibraryBaseEnableFB import RobotLibraryBaseEnableFB
from srci.functions.Common import SetTimeout
from srci.iec.rt import ADR, SysDepMemCmp, SysDepMemSet, copy_into, trunc_str
from srci.types import ExecutionMode, MessageType, PriorityLevel, ReadCallSubprogramCyclicOutCmd, ReadCallSubprogramCyclicParCmd, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ReadCallSubprogramCyclicFB']


class MC_ReadCallSubprogramCyclicFB(RobotLibraryBaseEnableFB):
    """Reads cyclic data of called subprogram"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: ReadCallSubprogramCyclicParCmd = ReadCallSubprogramCyclicParCmd()
        # VAR_OUTPUT
        # command outputs
        self.OutCmd: ReadCallSubprogramCyclicOutCmd = ReadCallSubprogramCyclicOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ReadCallSubprogramCyclicParCmd = ReadCallSubprogramCyclicParCmd()

    def __call__(self, *, ParCmd: ReadCallSubprogramCyclicParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ReadCallSubprogramCyclic

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 0 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ReadCallSubprogramCyclicParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ReadCallSubprogramCyclicParCmd)), DataLen=0) != RobotLibraryConstants.OK

        # check parameter valid ?
        self._parameterValid = self.CheckParameterValid(AxesGroup=AxesGroup)

        if self._parameterChanged and self._parameterValid or self._parameterUpdateInternal:
            # Create log entry for parameter changed event
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='NotifyParameterChanged Event {1}', Para1='')

            # reset internal flag for send parameter update
            self._parameterUpdateInternal = False
            # Set busy flag
            self.Busy = True
            # reset enable flag
            self.Enabled = False
            # update internal copy of parameters
            copy_into(self._parCmd, self.ParCmd)
            # Create logging
            self.CreateCommandParameterLog(AxesGroup=AxesGroup)
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False

        CheckParameterValid = True
        return CheckParameterValid

    def CreateCommandParameterLog(self, *, AxesGroup: _T.AxesGroup) -> None:  # INTERNAL
        pass

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ReadCallSubprogramCyclicFB'

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

        super().OnExecRun(AxesGroup=AxesGroup)

        match self._stepCmd:

            case 0:
                if self._enable_R.Q and (not self.Error):
                    # reset the rising edge
                    self._enable_R()

                    # Check function is supported and parameter are valid ?
                    if self.CheckFunctionSupported(AxesGroup=AxesGroup) & self.CheckParameterValid(AxesGroup=AxesGroup):
                        # Reset all internal flags
                        self.Reset()
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadCallSubprogramCyclicOutCmd)), Value=0, DataLen=26)
                        # apply command parameter
                        copy_into(self._parCmd, self.ParCmd)
                        # Create logging
                        self.CreateCommandParameterLog(AxesGroup=AxesGroup)
                        # set timeout
                        SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                        # inc step counter
                        self._stepCmd = self._stepCmd + 1

            case 1:
                if AxesGroup.CyclicOptional.RobToPlc.SubProgramData.Active:
                    # busy
                    self.Busy = False
                    # reset busy flag
                    self.Enabled = True
                    # Reset command outputs
                    SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadCallSubprogramCyclicOutCmd)), Value=0, DataLen=26)
                    # update command outputs
                    copy_into(self.OutCmd.Data, AxesGroup.CyclicOptional.RobToPlc.SubProgramData.Data)

                if self._enable_F.Q:
                    # reset the falling edge
                    self._enable_F()
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1

            case 2:
                if not self.Enable:
                    self.Reset()
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # Reset FB
        if self._enable_R.Q or self._enable_F.Q:
            self.Reset()
        return OnExecRun

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        # Reset command outputs
        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadCallSubprogramCyclicOutCmd)), Value=0, DataLen=26)
        return Reset
