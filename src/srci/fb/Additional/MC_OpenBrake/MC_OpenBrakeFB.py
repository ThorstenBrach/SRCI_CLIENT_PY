"""Release robot arm's brakes (Enable block, ST-FIX F42)

ST-Source: POUs/Additional/MC_OpenBrake/MC_OpenBrakeFB.st
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
from srci.fb._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from srci.fb._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from srci.functions.Common import CheckTimeout, SetTimeout
from srci.functions.Convert.TO_STRING.BYTE_TO_STRING_BIN import BYTE_TO_STRING_BIN
from srci.iec.conv import BOOL_TO_STRING, DINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, bit, copy_into, copy_value, set_bit, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, MessageType, OpenBrakeOutCmd, OpenBrakeParCmd, OpenBrakeRecvData, OpenBrakeSendData, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_OpenBrakeFB']


class MC_OpenBrakeFB(RobotLibraryBaseEnableFB):
    """Release robot arm's brakes (Enable block, ST-FIX F42)"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: OpenBrakeParCmd = OpenBrakeParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # Receiving of input parameter values has been acknowledged by RC
        self.ParameterAccepted: bool = False
        # command results
        self.OutCmd: OpenBrakeOutCmd = OpenBrakeOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: OpenBrakeParCmd = OpenBrakeParCmd()
        # command data to send
        self._command: OpenBrakeSendData = OpenBrakeSendData()
        # response data received
        self._response: OpenBrakeRecvData = OpenBrakeRecvData()

    def __call__(self, *, ParCmd: OpenBrakeParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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

    def CheckAddParameter(self, *, PayloadPtr: int = 0) -> bool:  # INTERNAL
        CheckAddParameter: bool = False
        # Payload as byte array
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 7)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 7)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 7 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 7, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(OpenBrakeSendData)), DataLen=7)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 7 - PayloadPtr, 7)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 7, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 7, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.OpenBrake

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 16 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(OpenBrakeParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(OpenBrakeParCmd)), DataLen=16) != RobotLibraryConstants.OK

        # check parameter valid ?
        self._parameterValid = self.CheckParameterValid(AxesGroup=AxesGroup)

        if self._parameterChanged and self._parameterValid or self._parameterUpdateInternal:
            # Create log entry for parameter changed event
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='NotifyParameterChanged Event {1}', Para1='')

            # reset internal flag for send parameter update
            self._parameterUpdateInternal = False
            # update internal copy of parameters
            copy_into(self._parCmd, self.ParCmd)
            # inc parameter sequence
            self._command.ParSeq = wrap(self._command.ParSeq + 1, 'BYTE')
            # update command data
            self.CommandData = self.CreateCommandPayload(AxesGroup=AxesGroup)  # ( Access via reference to rCommandFB in ACR )
            # notify active command register
            AxesGroup.Acyclic.ActiveCommandRegister.NotifyParameterChanged = self._uniqueID
            # Reset parameter accepted flag
            self.ParameterAccepted = False
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False

        CheckParameterValid = True

        # Check ParCmd.ParCmd.RobotAxesBrakeRelease.AxisJ1 valid ?
        if self.ParCmd.RobotAxesBrakeRelease.AxisJ1 and (not AxesGroup.State.RobotData.AxisJointUsed.J1):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.RobotAxesBrakeRelease.AxisJ1 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.RobotAxesBrakeRelease.AxisJ1))
            return CheckParameterValid

        # Check ParCmd.ParCmd.RobotAxesBrakeRelease.AxisJ2 valid ?
        if self.ParCmd.RobotAxesBrakeRelease.AxisJ2 and (not AxesGroup.State.RobotData.AxisJointUsed.J2):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.RobotAxesBrakeRelease.AxisJ2 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.RobotAxesBrakeRelease.AxisJ2))
            return CheckParameterValid

        # Check ParCmd.ParCmd.RobotAxesBrakeRelease.AxisJ3 valid ?
        if self.ParCmd.RobotAxesBrakeRelease.AxisJ3 and (not AxesGroup.State.RobotData.AxisJointUsed.J3):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.RobotAxesBrakeRelease.AxisJ3 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.RobotAxesBrakeRelease.AxisJ3))
            return CheckParameterValid

        # Check ParCmd.ParCmd.RobotAxesBrakeRelease.AxisJ4 valid ?
        if self.ParCmd.RobotAxesBrakeRelease.AxisJ4 and (not AxesGroup.State.RobotData.AxisJointUsed.J4):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.RobotAxesBrakeRelease.AxisJ4 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.RobotAxesBrakeRelease.AxisJ4))
            return CheckParameterValid

        # Check ParCmd.ParCmd.RobotAxesBrakeRelease.AxisJ5 valid ?
        if self.ParCmd.RobotAxesBrakeRelease.AxisJ5 and (not AxesGroup.State.RobotData.AxisJointUsed.J5):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.RobotAxesBrakeRelease.AxisJ5 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.RobotAxesBrakeRelease.AxisJ5))
            return CheckParameterValid

        # Check ParCmd.ParCmd.RobotAxesBrakeRelease.AxisJ6 valid ?
        if self.ParCmd.RobotAxesBrakeRelease.AxisJ6 and (not AxesGroup.State.RobotData.AxisJointUsed.J6):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.RobotAxesBrakeRelease.AxisJ6 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.RobotAxesBrakeRelease.AxisJ6))
            return CheckParameterValid

        # Check ParCmd.ParCmd.ExternalAxesBrakeRelease.AxisE1 valid ?
        if self.ParCmd.ExternalAxesBrakeRelease.AxisE1 and (not AxesGroup.State.RobotData.AxisExternalUsed.E1):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExternalAxesBrakeRelease.AxisE1 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ExternalAxesBrakeRelease.AxisE1))
            return CheckParameterValid

        # Check ParCmd.ParCmd.ExternalAxesBrakeRelease.AxisE2 valid ?
        if self.ParCmd.ExternalAxesBrakeRelease.AxisE2 and (not AxesGroup.State.RobotData.AxisExternalUsed.E2):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExternalAxesBrakeRelease.AxisE2 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ExternalAxesBrakeRelease.AxisE2))
            return CheckParameterValid

        # Check ParCmd.ParCmd.ExternalAxesBrakeRelease.AxisE3 valid ?
        if self.ParCmd.ExternalAxesBrakeRelease.AxisE3 and (not AxesGroup.State.RobotData.AxisExternalUsed.E3):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExternalAxesBrakeRelease.AxisE3 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ExternalAxesBrakeRelease.AxisE3))
            return CheckParameterValid

        # Check ParCmd.ParCmd.ExternalAxesBrakeRelease.AxisE4 valid ?
        if self.ParCmd.ExternalAxesBrakeRelease.AxisE4 and (not AxesGroup.State.RobotData.AxisExternalUsed.E4):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExternalAxesBrakeRelease.AxisE4 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ExternalAxesBrakeRelease.AxisE4))
            return CheckParameterValid

        # Check ParCmd.ParCmd.ExternalAxesBrakeRelease.AxisE5 valid ?
        if self.ParCmd.ExternalAxesBrakeRelease.AxisE5 and (not AxesGroup.State.RobotData.AxisExternalUsed.E5):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExternalAxesBrakeRelease.AxisE5 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ExternalAxesBrakeRelease.AxisE5))
            return CheckParameterValid

        # Check ParCmd.ParCmd.ExternalAxesBrakeRelease.AxisE6 valid ?
        if self.ParCmd.ExternalAxesBrakeRelease.AxisE6 and (not AxesGroup.State.RobotData.AxisExternalUsed.E6):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExternalAxesBrakeRelease.AxisE6 = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ExternalAxesBrakeRelease.AxisE6))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.OpenBrake
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.RobotAxesBrakeRelease = set_bit(self._command.RobotAxesBrakeRelease, 0, self._parCmd.RobotAxesBrakeRelease.Bit00)
        self._command.RobotAxesBrakeRelease = set_bit(self._command.RobotAxesBrakeRelease, 1, self._parCmd.RobotAxesBrakeRelease.AxisJ1)
        self._command.RobotAxesBrakeRelease = set_bit(self._command.RobotAxesBrakeRelease, 2, self._parCmd.RobotAxesBrakeRelease.AxisJ2)
        self._command.RobotAxesBrakeRelease = set_bit(self._command.RobotAxesBrakeRelease, 3, self._parCmd.RobotAxesBrakeRelease.AxisJ3)
        self._command.RobotAxesBrakeRelease = set_bit(self._command.RobotAxesBrakeRelease, 4, self._parCmd.RobotAxesBrakeRelease.AxisJ4)
        self._command.RobotAxesBrakeRelease = set_bit(self._command.RobotAxesBrakeRelease, 5, self._parCmd.RobotAxesBrakeRelease.AxisJ5)
        self._command.RobotAxesBrakeRelease = set_bit(self._command.RobotAxesBrakeRelease, 6, self._parCmd.RobotAxesBrakeRelease.AxisJ6)
        self._command.RobotAxesBrakeRelease = set_bit(self._command.RobotAxesBrakeRelease, 7, self._parCmd.RobotAxesBrakeRelease.Bit07)
        self._command.ExternalAxesBrakeRelease = set_bit(self._command.ExternalAxesBrakeRelease, 0, self._parCmd.ExternalAxesBrakeRelease.Bit00)
        self._command.ExternalAxesBrakeRelease = set_bit(self._command.ExternalAxesBrakeRelease, 1, self._parCmd.ExternalAxesBrakeRelease.AxisE1)
        self._command.ExternalAxesBrakeRelease = set_bit(self._command.ExternalAxesBrakeRelease, 2, self._parCmd.ExternalAxesBrakeRelease.AxisE2)
        self._command.ExternalAxesBrakeRelease = set_bit(self._command.ExternalAxesBrakeRelease, 3, self._parCmd.ExternalAxesBrakeRelease.AxisE3)
        self._command.ExternalAxesBrakeRelease = set_bit(self._command.ExternalAxesBrakeRelease, 4, self._parCmd.ExternalAxesBrakeRelease.AxisE4)
        self._command.ExternalAxesBrakeRelease = set_bit(self._command.ExternalAxesBrakeRelease, 5, self._parCmd.ExternalAxesBrakeRelease.AxisE5)
        self._command.ExternalAxesBrakeRelease = set_bit(self._command.ExternalAxesBrakeRelease, 6, self._parCmd.ExternalAxesBrakeRelease.AxisE6)
        self._command.ExternalAxesBrakeRelease = set_bit(self._command.ExternalAxesBrakeRelease, 7, self._parCmd.ExternalAxesBrakeRelease.Bit07)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)
        # ST-FIX F42: byte 4 Enable (spec table of OpenBrake)
        CreateCommandPayload.AddBool(Value=self.Enable)
        _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.RobotAxesBrakeRelease
            CreateCommandPayload.AddByte(Value=self._command.RobotAxesBrakeRelease)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ExternalAxesBrakeRelease
            CreateCommandPayload.AddByte(Value=self._command.ExternalAxesBrakeRelease)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Create logging
        self.CreateCommandPayloadLog(AxesGroup=AxesGroup, ParameterCnt=_parameterCnt)
        return CreateCommandPayload

    def CreateCommandPayloadLog(self, *, AxesGroup: _T.AxesGroup, ParameterCnt: int = 0) -> None:  # INTERNAL
        # Create log entry for Parameter start
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Create command payload with {1} parameter(s) :', Para1=DINT_TO_STRING(ParameterCnt))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for RobotAxesBrakeRelease
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.RobotAxesBrakeRelease = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.RobotAxesBrakeRelease))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ExternalAxesBrakeRelease
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ExternalAxesBrakeRelease = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.ExternalAxesBrakeRelease))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_OpenBrakeFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(OpenBrakeOutCmd)), Value=0, DataLen=17)

        # ST-FIX F42
        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.Enabled = bit(self._response.Enabled, 0)
            self.OutCmd.RobotAxesBrakeReleased.Bit00 = bit(self._response.RobotAxesBrakeReleased, 0)
            self.OutCmd.RobotAxesBrakeReleased.AxisJ1 = bit(self._response.RobotAxesBrakeReleased, 1)
            self.OutCmd.RobotAxesBrakeReleased.AxisJ2 = bit(self._response.RobotAxesBrakeReleased, 2)
            self.OutCmd.RobotAxesBrakeReleased.AxisJ3 = bit(self._response.RobotAxesBrakeReleased, 3)
            self.OutCmd.RobotAxesBrakeReleased.AxisJ4 = bit(self._response.RobotAxesBrakeReleased, 4)
            self.OutCmd.RobotAxesBrakeReleased.AxisJ5 = bit(self._response.RobotAxesBrakeReleased, 5)
            self.OutCmd.RobotAxesBrakeReleased.AxisJ6 = bit(self._response.RobotAxesBrakeReleased, 6)
            self.OutCmd.RobotAxesBrakeReleased.Bit07 = bit(self._response.RobotAxesBrakeReleased, 7)
            self.OutCmd.ExternalAxesBrakeReleased.Bit00 = bit(self._response.ExternalAxesBrakeReleased, 0)
            self.OutCmd.ExternalAxesBrakeReleased.AxisE1 = bit(self._response.ExternalAxesBrakeReleased, 1)
            self.OutCmd.ExternalAxesBrakeReleased.AxisE2 = bit(self._response.ExternalAxesBrakeReleased, 2)
            self.OutCmd.ExternalAxesBrakeReleased.AxisE3 = bit(self._response.ExternalAxesBrakeReleased, 3)
            self.OutCmd.ExternalAxesBrakeReleased.AxisE4 = bit(self._response.ExternalAxesBrakeReleased, 4)
            self.OutCmd.ExternalAxesBrakeReleased.AxisE5 = bit(self._response.ExternalAxesBrakeReleased, 5)
            self.OutCmd.ExternalAxesBrakeReleased.AxisE6 = bit(self._response.ExternalAxesBrakeReleased, 6)
            self.OutCmd.ExternalAxesBrakeReleased.Bit07 = bit(self._response.ExternalAxesBrakeReleased, 7)

        # ST-FIX F42: output Enabled of the enable block
        self.Enabled = self.OutCmd.Enabled

    def OnExecCancel(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecCancel: int = 0
        # internal return value
        _retVal: int = 0

        OnExecCancel = RobotLibraryConstants.RUNNING

        match self._stepCancel:

            case 0:
                self.Busy = True

                # Create log entry
                self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Execution of {1} cancelled', Para1=self.MyType)

                # try to remove cmd
                _retVal = AxesGroup.Acyclic.ActiveCommandRegister.RemoveCmd(UniqueID=self._uniqueID)

                # check result of removement
                if _retVal == RobotLibraryConstants.OK:
                    # Reset step counter
                    self._stepCancel = 0
                    # finished okay
                    OnExecCancel = RobotLibraryConstants.OK

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} successfully removed from ACR', Para1=self.MyType)
                else:
                    # set timeout
                    SetTimeout(PT=self._timeoutCancel, rTimer=self._timerCancel)
                    # inc step counter
                    self._stepCancel = self._stepCancel + 1

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} was not removed from ACR because execution was already in progress', Para1=self.MyType)

            case 1:
                OnExecCancel = self.OnExecErrorClear(AxesGroup=AxesGroup)

                if OnExecCancel == RobotLibraryConstants.OK:
                    # Reset busy flag
                    self.Busy = False
                    # Reset step counter
                    self._stepCancel = 0
                    # finished okay
                    OnExecCancel = RobotLibraryConstants.OK
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # reset step counter
        if OnExecCancel != RobotLibraryConstants.RUNNING:
            # Reset FB variables
            self.Reset()
            # Reset step counter
            self._stepCancel = 0
        return OnExecCancel

    def OnExecErrorClear(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecErrorClear: int = 0

        OnExecErrorClear = RobotLibraryConstants.RUNNING

        match self._stepClearError:

            case 0:
                self.Busy = True
                # trigger parameter update to disable FB
                self._parameterUpdateInternal = True
                # call Check Parameter changed method to trigger the parameter update to disable the function
                self.CheckParameterChanged(AxesGroup=AxesGroup)
                # set timeout
                SetTimeout(PT=self._timeoutClearError, rTimer=self._timerClearError)
                # inc step counter
                self._stepClearError = self._stepClearError + 1

            case 1:
                if self._responseReceived:
                    # reset response received flag
                    self._responseReceived = False
                    # reset step counter
                    self._stepClearError = 0
                    # finished
                    OnExecErrorClear = RobotLibraryConstants.OK
                else:
                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerClearError) == RobotLibraryConstants.OK:
                        OnExecErrorClear = RobotLibraryConstants.HAS_ERROR
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # reset step counter
        if OnExecErrorClear != RobotLibraryConstants.RUNNING:
            # Reset
            self.Reset()
            # reset step counter
            self._stepClearError = 0
        return OnExecErrorClear

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecRun: int = 0

        # call base implementation
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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(OpenBrakeOutCmd)), Value=0, DataLen=17)
                        # apply command parameter
                        copy_into(self._parCmd, self.ParCmd)
                        # init parameter sequence
                        self._command.ParSeq = 1
                        # create command data
                        self.CommandData = self.CreateCommandPayload(AxesGroup=AxesGroup)
                        # Add command to active command register
                        self._uniqueID = AxesGroup.Acyclic.ActiveCommandRegister.AddCmd(pCommandFB=self)
                        # set timeout
                        SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                        # inc step counter
                        self._stepCmd = self._stepCmd + 1

            case 1:
                if self._responseReceived:
                    # reset response received flag
                    self._responseReceived = False
                    # update state flags
                    self.OnUpdateStateFlags(State=self._response.State)
                    # update state flags
                    self.OnApplyOutCmd(State=self._response.State)

                # do not abort directly, so that the ParSeq update can be send
                if self._enable_F.Q:
                    # Set Busy flag
                    self.Busy = True
                    # trigger parameter update to disable FB
                    self._parameterUpdateInternal = True
                    # reset the falling edge
                    self._enable_F()
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1

            # Wait for response received or timeout or not Initialized
            case 2:
                if self._responseReceived | (CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK) or (not AxesGroup.State.Initialized and (not AxesGroup.State.Synchronized)):
                    self.Reset()
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # Reset FB
        if self._enable_R.Q or self._enable_F.Q:
            self.Reset()
        return OnExecRun

    def OnUpdateStateFlags(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        # Reset State flags

        # Update Enable flag
        # Enabled: see OnApplyOutCmd (ST-FIX F42)
        match State:

            # No operation or process is active
            case CmdMessageState.EMPTY:
                pass
            # Created but not yet started
            case CmdMessageState.CREATED:
                pass
            # Buffered and awaiting execution
            case CmdMessageState.BUFFERED:
                self.CommandBuffered = True
                self.ParameterAccepted = True
            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER:
                self.CommandBuffered = True
                self.ParameterAccepted = True
            # Currently active and in progress
            case CmdMessageState.ACTIVE:
                pass
            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                pass
            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass
            # Successfully completed
            case CmdMessageState.DONE:
                self.Busy = False
            # Aborted before completion
            case CmdMessageState.ABORTED:
                self.Busy = False
            # Encountered an error during execution
            case CmdMessageState.ERROR:
                self.Error = True
                self.Busy = False

    def ParseResponsePayload(self, *, ResponseData: RobotLibraryResponseDataFB | None = None, Timestamp: SystemTime | None = None) -> int:  # INTERNAL
        if ResponseData is None:
            ResponseData = RobotLibraryResponseDataFB()
        else:
            ResponseData = copy_value(ResponseData)  # VAR_INPUT is a copy in ST
        if Timestamp is None:
            Timestamp = SystemTime()
        ParseResponsePayload: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # call base implementation to parse the header from payload buffer
        ResponseData.PayloadPtr = super().ParseResponsePayload(ResponseData=ResponseData, Timestamp=Timestamp)

        # copy parsed header to response
        self._response.ParSeq = self._rspHeader.ParSeq
        self._response.State = self._rspHeader.State
        self._response.AlarmMessageSeverity = self._rspHeader.AlarmMessageSeverity
        self._response.AlarmMessageCode = self._rspHeader.AlarmMessageCode

        # ST-FIX F42: byte 4 Enabled
        if ResponseData.IsPayloadRemaining:
            self._response.Enabled = ResponseData.GetByte()
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get RobotAxesStatus
            self._response.RobotAxesBrakeReleased = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get ExternalAxesStatus
            self._response.ExternalAxesBrakeReleased = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Create logging
        self.ParseResponsePayloadLog(ResponseData=ResponseData, Timestamp=Timestamp, ParameterCnt=_parameterCnt)
        return ParseResponsePayload

    def ParseResponsePayloadLog(self, *, ResponseData: RobotLibraryResponseDataFB | None = None, Timestamp: SystemTime | None = None, ParameterCnt: int = 0) -> None:  # INTERNAL
        if ResponseData is None:
            ResponseData = RobotLibraryResponseDataFB()
        if Timestamp is None:
            Timestamp = SystemTime()
        # Create log entry for Parameter start
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} parameter(s) to parse from the response data:', Para1=DINT_TO_STRING(ParameterCnt))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for RobotAxesBrakeReleased
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.RobotAxesBrakeReleased = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._response.RobotAxesBrakeReleased))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ExternalAxesBrakeReleased
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ExternalAxesBrakeReleased = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._response.ExternalAxesBrakeReleased))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Busy = False
        self.CommandBuffered = False
        self.ParameterAccepted = False
        return Reset
