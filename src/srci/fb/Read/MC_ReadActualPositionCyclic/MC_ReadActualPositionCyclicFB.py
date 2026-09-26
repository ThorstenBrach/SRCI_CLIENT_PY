"""Read the actual position cyclically

ST-Source: POUs/Read/MC_ReadActualPositionCyclic/MC_ReadActualPositionCyclicFB.st
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
from srci.iec.conv import BOOL_TO_STRING, INT_TO_STRING
from srci.iec.rt import ADR, SysDepMemCmp, SysDepMemSet, copy_into, trunc_str
from srci.types import ExecutionMode, MessageType, PriorityLevel, ReadActualPositionCyclicOutCmd, ReadActualPositionCyclicParCmd, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ReadActualPositionCyclicFB']


class MC_ReadActualPositionCyclicFB(RobotLibraryBaseEnableFB):
    """Read the actual position cyclically"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: ReadActualPositionCyclicParCmd = ReadActualPositionCyclicParCmd()
        # VAR_OUTPUT
        # command outputs
        self.OutCmd: ReadActualPositionCyclicOutCmd = ReadActualPositionCyclicOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ReadActualPositionCyclicParCmd = ReadActualPositionCyclicParCmd()

    def __call__(self, *, ParCmd: ReadActualPositionCyclicParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ReadActualPositionCyclic

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 8 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ReadActualPositionCyclicParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ReadActualPositionCyclicParCmd)), DataLen=8) != RobotLibraryConstants.OK

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
            # update tool number
            AxesGroup.Cyclic.PlcToRob.ToolNo = self._parCmd.ToolNo
            # update frame number
            AxesGroup.Cyclic.PlcToRob.FrameNo = self._parCmd.FrameNo
            # Create logging
            self.CreateCommandParameterLog(AxesGroup=AxesGroup)
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False

        CheckParameterValid = True

        # Check ParCmd.ReadCartesianPosition valid ?
        if self.ParCmd.ReadCartesianPosition and (not AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ReadCartesianPosition = {1} but CyclicOptional.RobToPlc.CartesianPosition = FALSE', Para1=BOOL_TO_STRING(self.ParCmd.ReadCartesianPosition))
            return CheckParameterValid

        # Check ParCmd.ReadCartesianPositionExt valid ?
        if self.ParCmd.ReadCartesianPositionExt and (not AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ReadCartesianPositionExt = {1} but CyclicOptional.RobToPlc.CartesianPositionExt = FALSE', Para1=BOOL_TO_STRING(self.ParCmd.ReadCartesianPositionExt))
            return CheckParameterValid

        # Check ParCmd.ToolNo valid ?
        if ((self.ParCmd.ToolNo < -1 or self.ParCmd.ToolNo > 254) or self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex) or self.ParCmd.ToolNo > AxesGroup.State.UnifiedToolIndex:
            # Parameter not valid
            CheckParameterValid = False

            # Check ToolNo available on RC ?
            if self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TOOLNO_UNAVAILABLE, Overwrite=True)
            else:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TOOLNO_RANGE, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ToolNo = {1}', Para1=INT_TO_STRING(self.ParCmd.ToolNo))
            return CheckParameterValid

        # Check ParCmd.FrameNo valid ?
        if ((self.ParCmd.FrameNo < -1 or self.ParCmd.FrameNo > 254) or self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex) or self.ParCmd.FrameNo > AxesGroup.State.UnifiedFrameIndex:
            # Parameter not valid
            CheckParameterValid = False

            # Check FrameNo available on RC ?
            if self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_FRAMENO_UNAVAILABLE, Overwrite=True)
            else:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_FRAMENO_RANGE, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.FrameNo = {1}', Para1=INT_TO_STRING(self.ParCmd.FrameNo))
            return CheckParameterValid

        # Check ParCmd.ReadJointPosition valid ?
        if self.ParCmd.ReadJointPosition and (not AxesGroup.CyclicOptional.RobToPlc.JointPosition.Active):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ReadJointPosition = {1} but CyclicOptional.RobToPlc.JointPosition = FALSE', Para1=BOOL_TO_STRING(self.ParCmd.ReadJointPosition))
            return CheckParameterValid

        # Check ParCmd.ReadJointPositionExt valid ?
        if self.ParCmd.ReadJointPositionExt and (not AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.Active):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ReadJointPositionExt = {1} but CyclicOptional.RobToPlc.JointPositionExt = FALSE', Para1=BOOL_TO_STRING(self.ParCmd.ReadJointPositionExt))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandParameterLog(self, *, AxesGroup: _T.AxesGroup) -> None:  # INTERNAL
        # Create log entry for Parameter start
        self.CreateLogMessage(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Update position with the following parameter(s) :')

        # Create log entry for _parCmd.ReadCartesianPosition
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='_parCmd.ReadCartesianPosition = {1}', Para1=BOOL_TO_STRING(self._parCmd.ReadCartesianPosition))

        # Create log entry for _parCmd.ReadCartesianPositionExt
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='_parCmd.ReadCartesianPositionExt = {1}', Para1=BOOL_TO_STRING(self._parCmd.ReadCartesianPositionExt))

        # Create log entry for _parCmd.ToolNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='_parCmd.ToolNo = {1}', Para1=INT_TO_STRING(self._parCmd.ToolNo))

        # Create log entry for _parCmd.FrameNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='_parCmd.FrameNo = {1}', Para1=INT_TO_STRING(self._parCmd.FrameNo))

        # Create log entry for _parCmd.ReadJointPosition
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='_parCmd.ReadJointPosition = {1}', Para1=BOOL_TO_STRING(self._parCmd.ReadJointPosition))

        # Create log entry for _parCmd.ReadJointPositionExt
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='_parCmd.ReadJointPositionExt = {1}', Para1=BOOL_TO_STRING(self._parCmd.ReadJointPositionExt))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ReadActualPositionCyclicFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnCall(self, *, AxesGroup: _T.AxesGroup) -> None:  # PROTECTED
        # internal return value
        _retVal: int = 0

        super().OnCall(AxesGroup=AxesGroup)

        # update status flags
        AxesGroup.State.ReadingCartesianPosition = self.Enabled and self._parCmd.ReadCartesianPosition
        AxesGroup.State.ReadingCartesianPositionExt = self.Enabled and self._parCmd.ReadCartesianPositionExt
        AxesGroup.State.ReadingJointPosition = self.Enabled and self._parCmd.ReadJointPosition
        AxesGroup.State.ReadingJointPositionExt = self.Enabled and self._parCmd.ReadJointPositionExt

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadActualPositionCyclicOutCmd)), Value=0, DataLen=226)
                        # apply command parameter
                        copy_into(self._parCmd, self.ParCmd)
                        # set parameter
                        AxesGroup.Cyclic.PlcToRob.ToolNo = self._parCmd.ToolNo
                        AxesGroup.Cyclic.PlcToRob.FrameNo = self._parCmd.FrameNo
                        # Create logging
                        self.CreateCommandParameterLog(AxesGroup=AxesGroup)
                        # set timeout
                        SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                        # inc step counter
                        self._stepCmd = self._stepCmd + 1

            case 1:
                if AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CoordinateSystem.FrameNo == self._parCmd.FrameNo and AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CoordinateSystem.ToolNo == self._parCmd.ToolNo or self._parCmd.ReadCartesianPosition == False:
                    # busy
                    self.Busy = False
                    # reset busy flag
                    self.Enabled = True
                    # Reset command outputs
                    SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadActualPositionCyclicOutCmd)), Value=0, DataLen=226)
                    # set ToolNo and FrameNo
                    self.OutCmd.CurrentCoordinateSystem.FrameNo = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CurrentCoordinateSystem.FrameNo  # ST-FIX F59
                    self.OutCmd.CoordinateSystem.FrameNo = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CoordinateSystem.FrameNo
                    self.OutCmd.CurrentCoordinateSystem.ToolNo = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CurrentCoordinateSystem.ToolNo  # ST-FIX F59
                    self.OutCmd.CoordinateSystem.ToolNo = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CoordinateSystem.ToolNo

                    # Set cartesian position
                    if self._parCmd.ReadCartesianPosition:
                        self.OutCmd.ReadingCartesianPosition = True
                        self.OutCmd.CartesianPositionShort.X = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.X
                        self.OutCmd.CartesianPosition.X = self.OutCmd.CartesianPositionShort.X
                        self.OutCmd.CartesianPositionShort.Y = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Y
                        self.OutCmd.CartesianPosition.Y = self.OutCmd.CartesianPositionShort.Y
                        self.OutCmd.CartesianPositionShort.Z = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Z
                        self.OutCmd.CartesianPosition.Z = self.OutCmd.CartesianPositionShort.Z
                        self.OutCmd.CartesianPositionShort.Rx = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Rx
                        self.OutCmd.CartesianPosition.Rx = self.OutCmd.CartesianPositionShort.Rx
                        self.OutCmd.CartesianPositionShort.Ry = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Ry
                        self.OutCmd.CartesianPosition.Ry = self.OutCmd.CartesianPositionShort.Ry
                        self.OutCmd.CartesianPositionShort.Rz = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Rz
                        self.OutCmd.CartesianPosition.Rz = self.OutCmd.CartesianPositionShort.Rz
                        copy_into(self.OutCmd.CartesianPositionShort.Config, AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Config)
                        copy_into(self.OutCmd.CartesianPosition.Config, self.OutCmd.CartesianPositionShort.Config)
                        copy_into(self.OutCmd.CartesianPositionShort.TurnNumber, AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber)
                        copy_into(self.OutCmd.CartesianPosition.TurnNumber, self.OutCmd.CartesianPositionShort.TurnNumber)
                        self.OutCmd.CartesianPositionShort.E1 = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.E1
                        self.OutCmd.CartesianPosition.E1 = self.OutCmd.CartesianPositionShort.E1

                    # Set extended cartesian position
                    if self._parCmd.ReadCartesianPositionExt:
                        self.OutCmd.ReadingCartesianPositionExt = True
                        self.OutCmd.CartesianPositionExt.E2 = AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E2
                        self.OutCmd.CartesianPosition.E2 = self.OutCmd.CartesianPositionExt.E2
                        self.OutCmd.CartesianPositionExt.E3 = AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E3
                        self.OutCmd.CartesianPosition.E3 = self.OutCmd.CartesianPositionExt.E3
                        self.OutCmd.CartesianPositionExt.E4 = AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E4
                        self.OutCmd.CartesianPosition.E4 = self.OutCmd.CartesianPositionExt.E4
                        self.OutCmd.CartesianPositionExt.E5 = AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E5
                        self.OutCmd.CartesianPosition.E5 = self.OutCmd.CartesianPositionExt.E5
                        self.OutCmd.CartesianPositionExt.E6 = AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E6
                        self.OutCmd.CartesianPosition.E6 = self.OutCmd.CartesianPositionExt.E6

                    # Set joint position
                    if self._parCmd.ReadJointPosition:
                        self.OutCmd.ReadingJointPosition = True
                        self.OutCmd.JointPositionShort.J1 = AxesGroup.CyclicOptional.RobToPlc.JointPosition.J1
                        self.OutCmd.JointPosition.J1 = self.OutCmd.JointPositionShort.J1
                        self.OutCmd.JointPositionShort.J2 = AxesGroup.CyclicOptional.RobToPlc.JointPosition.J2
                        self.OutCmd.JointPosition.J2 = self.OutCmd.JointPositionShort.J2
                        self.OutCmd.JointPositionShort.J3 = AxesGroup.CyclicOptional.RobToPlc.JointPosition.J3
                        self.OutCmd.JointPosition.J3 = self.OutCmd.JointPositionShort.J3
                        self.OutCmd.JointPositionShort.J4 = AxesGroup.CyclicOptional.RobToPlc.JointPosition.J4
                        self.OutCmd.JointPosition.J4 = self.OutCmd.JointPositionShort.J4
                        self.OutCmd.JointPositionShort.J5 = AxesGroup.CyclicOptional.RobToPlc.JointPosition.J5
                        self.OutCmd.JointPosition.J5 = self.OutCmd.JointPositionShort.J5
                        self.OutCmd.JointPositionShort.J6 = AxesGroup.CyclicOptional.RobToPlc.JointPosition.J6
                        self.OutCmd.JointPosition.J6 = self.OutCmd.JointPositionShort.J6

                    # Set extended joint position
                    if self._parCmd.ReadJointPositionExt:
                        self.OutCmd.ReadingCartesianPositionExt = True
                        self.OutCmd.JointPositionExt.E2 = AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E2
                        self.OutCmd.JointPosition.E2 = self.OutCmd.JointPositionExt.E2
                        self.OutCmd.JointPositionExt.E3 = AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E3
                        self.OutCmd.JointPosition.E3 = self.OutCmd.JointPositionExt.E3
                        self.OutCmd.JointPositionExt.E4 = AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E4
                        self.OutCmd.JointPosition.E4 = self.OutCmd.JointPositionExt.E4
                        self.OutCmd.JointPositionExt.E5 = AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E5
                        self.OutCmd.JointPosition.E5 = self.OutCmd.JointPositionExt.E5
                        self.OutCmd.JointPositionExt.E6 = AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E6
                        self.OutCmd.JointPosition.E6 = self.OutCmd.JointPositionExt.E6

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
        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadActualPositionCyclicOutCmd)), Value=0, DataLen=226)
        return Reset
