"""Jog robot manually

ST-Source: POUs/BasicMove/MC_GroupJog/MC_GroupJogFB.st
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
from srci.functions.Convert.TO_STRING.JOG_CONTROL_TO_STRING import JOG_CONTROL_TO_STRING
from srci.functions.Convert.TO_STRING.JOG_MODE_TO_STRING import JOG_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, BYTE_TO_STRING, DINT_TO_STRING, REAL_TO_STRING, UINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, bit, copy_into, copy_value, set_bit, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, GroupJogOutCmd, GroupJogParCmd, GroupJogRecvData, GroupJogSendData, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_GroupJogFB']


class MC_GroupJogFB(RobotLibraryBaseEnableFB):
    """Jog robot manually"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: GroupJogParCmd = GroupJogParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # The active movement was aborted by another command
        self.CommandAborted: bool = False
        # Receiving of input parameter values has been acknowledged by RC
        self.ParameterAccepted: bool = False
        # The command takes control of the motion of the according axis group.
        self.Active: bool = False
        # Command output
        self.OutCmd: GroupJogOutCmd = GroupJogOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: GroupJogParCmd = GroupJogParCmd()
        # command data to send
        self._command: GroupJogSendData = GroupJogSendData()
        # response data received
        self._response: GroupJogRecvData = GroupJogRecvData()

    def __call__(self, *, ParCmd: GroupJogParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 24)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 24)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 24 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 24, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(GroupJogSendData)), DataLen=24)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 24 - PayloadPtr, 24)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 24, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 24, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.GroupJog

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if (37 == 0 or self._stepCmd == 0) and (not self._parameterUpdateInternal):
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(GroupJogParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(GroupJogParCmd)), DataLen=37) != RobotLibraryConstants.OK

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

        # Check ParCmd.Override valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.Override) == False or self.ParCmd.Override < 0) or self.ParCmd.Override > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            # ST-FIX F70
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_OVERRIDE_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Override = {1}', Para1=VALID_REAL_TO_STRING(Value=float(self.ParCmd.Override)))
            return CheckParameterValid

        # Check ParCmd.Control valid ?
        if ((((self.ParCmd.Control.X_J1_Neg and self.ParCmd.Control.X_J1_Pos or (self.ParCmd.Control.Y_J2_Neg and self.ParCmd.Control.Y_J2_Pos)) or (self.ParCmd.Control.Z_J3_Neg and self.ParCmd.Control.Z_J3_Pos)) or (self.ParCmd.Control.Rx_J4_Neg and self.ParCmd.Control.Rx_J4_Pos)) or (self.ParCmd.Control.Ry_J5_Neg and self.ParCmd.Control.Ry_J5_Pos)) or (self.ParCmd.Control.Rz_J6_Neg and self.ParCmd.Control.Rz_J6_Pos):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Control = {1}', Para1=JOG_CONTROL_TO_STRING(Value=self.ParCmd.Control))
            return CheckParameterValid

        # Check ParCmd.ToolNo valid ?
        if ((self.ParCmd.ToolNo < 0 or self.ParCmd.ToolNo > 254) or self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex) or self.ParCmd.ToolNo > AxesGroup.State.UnifiedToolIndex:
            # Parameter not valid
            CheckParameterValid = False

            # Check ToolNo available on RC ?
            if self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TOOLNO_UNAVAILABLE, Overwrite=True)
            else:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TOOLNO_RANGE, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ToolNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.ToolNo))
            return CheckParameterValid

        # Check ParCmd.FrameNo valid ?
        if ((self.ParCmd.FrameNo < 0 or self.ParCmd.FrameNo > 254) or self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex) or self.ParCmd.FrameNo > AxesGroup.State.UnifiedFrameIndex:
            # Parameter not valid
            CheckParameterValid = False

            # Check FrameNo available on RC ?
            if self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_FRAMENO_UNAVAILABLE, Overwrite=True)
            else:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_FRAMENO_RANGE, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.FrameNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.FrameNo))
            return CheckParameterValid

        # Check ParCmd.IncrementalTranslation valid ?
        if SysDepIsValidReal(Value=self.ParCmd.IncrementalTranslation) == False or self.ParCmd.IncrementalTranslation < 0:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.IncrementalTranslation = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.IncrementalTranslation))
            return CheckParameterValid

        # Check ParCmd.IncrementalRotation valid ?
        if SysDepIsValidReal(Value=self.ParCmd.IncrementalRotation) == False or self.ParCmd.IncrementalRotation < 0:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.IncrementalRotation = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.IncrementalRotation))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.GroupJog
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority

        self._command.Enable = self.Enable
        self._command.Reserve = 0
        self._command.ToolNo = self._parCmd.ToolNo
        self._command.FrameNo = self._parCmd.FrameNo
        self._command.Mode = self._parCmd.Mode
        self._command.Reserve2 = 0
        self._command.IncrementalTranslation = self._parCmd.IncrementalTranslation
        self._command.IncrementalRotation = self._parCmd.IncrementalRotation
        self._command.Override = wrap(self._parCmd.Override * 100, 'UINT')
        self._command.JogControl[0] = set_bit(self._command.JogControl[0], 0, self._parCmd.Control.X_J1_Pos)
        self._command.JogControl[0] = set_bit(self._command.JogControl[0], 1, self._parCmd.Control.Y_J2_Pos)
        self._command.JogControl[0] = set_bit(self._command.JogControl[0], 2, self._parCmd.Control.Z_J3_Pos)
        self._command.JogControl[0] = set_bit(self._command.JogControl[0], 3, self._parCmd.Control.Rx_J4_Pos)
        self._command.JogControl[0] = set_bit(self._command.JogControl[0], 4, self._parCmd.Control.Ry_J5_Pos)
        self._command.JogControl[0] = set_bit(self._command.JogControl[0], 5, self._parCmd.Control.Rz_J6_Pos)
        self._command.JogControl[0] = set_bit(self._command.JogControl[0], 6, self._parCmd.Control.X_J1_Neg)
        self._command.JogControl[0] = set_bit(self._command.JogControl[0], 7, self._parCmd.Control.Y_J2_Neg)
        self._command.JogControl[1] = set_bit(self._command.JogControl[1], 0, self._parCmd.Control.Z_J3_Neg)
        self._command.JogControl[1] = set_bit(self._command.JogControl[1], 1, self._parCmd.Control.Rx_J4_Neg)
        self._command.JogControl[1] = set_bit(self._command.JogControl[1], 2, self._parCmd.Control.Ry_J5_Neg)
        self._command.JogControl[1] = set_bit(self._command.JogControl[1], 3, self._parCmd.Control.Rz_J6_Neg)
        self._command.JogControl[1] = set_bit(self._command.JogControl[1], 4, self._parCmd.Control.E1_Pos)
        self._command.JogControl[1] = set_bit(self._command.JogControl[1], 5, self._parCmd.Control.E2_Pos)
        self._command.JogControl[1] = set_bit(self._command.JogControl[1], 6, self._parCmd.Control.E3_Pos)
        self._command.JogControl[1] = set_bit(self._command.JogControl[1], 7, self._parCmd.Control.E4_Pos)
        self._command.JogControl[2] = set_bit(self._command.JogControl[2], 0, self._parCmd.Control.E5_Pos)
        self._command.JogControl[2] = set_bit(self._command.JogControl[2], 1, self._parCmd.Control.E6_Pos)
        self._command.JogControl[2] = set_bit(self._command.JogControl[2], 2, self._parCmd.Control.E1_Neg)
        self._command.JogControl[2] = set_bit(self._command.JogControl[2], 3, self._parCmd.Control.E2_Neg)
        self._command.JogControl[2] = set_bit(self._command.JogControl[2], 4, self._parCmd.Control.E3_Neg)
        self._command.JogControl[2] = set_bit(self._command.JogControl[2], 5, self._parCmd.Control.E4_Neg)
        self._command.JogControl[2] = set_bit(self._command.JogControl[2], 6, self._parCmd.Control.E5_Neg)
        self._command.JogControl[2] = set_bit(self._command.JogControl[2], 7, self._parCmd.Control.E6_Neg)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        # send always
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr) or True:
            # add command.Enable
            CreateCommandPayload.AddBool(Value=self._command.Enable)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Reserve
            CreateCommandPayload.AddByte(Value=self._command.Reserve)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ToolNo
            CreateCommandPayload.AddUsint(Value=self._command.ToolNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.FrameNo
            CreateCommandPayload.AddUsint(Value=self._command.FrameNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Mode
            CreateCommandPayload.AddUsint(Value=self._command.Mode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Reserve
            CreateCommandPayload.AddByte(Value=self._command.Reserve2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.IncrementalTranslation
            CreateCommandPayload.AddReal(Value=self._command.IncrementalTranslation)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.IncrementalRotation
            CreateCommandPayload.AddReal(Value=self._command.IncrementalRotation)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Override
            CreateCommandPayload.AddUint(Value=self._command.Override)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.JogControl[0]
            CreateCommandPayload.AddByte(Value=self._command.JogControl[0])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.JogControl[1]
            CreateCommandPayload.AddByte(Value=self._command.JogControl[1])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.JogControl[2]
            CreateCommandPayload.AddByte(Value=self._command.JogControl[2])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Create log entry for Parameter start
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
        # Create log entry for Enable
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Enable = {1}', Para1=BOOL_TO_STRING(self._command.Enable))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ToolNo = {1}', Para1=USINT_TO_STRING(self._command.ToolNo))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for FrameNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.FrameNo = {1}', Para1=USINT_TO_STRING(self._command.FrameNo))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for JogMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.JogMode = {1}', Para1=JOG_MODE_TO_STRING(Value=self._command.Mode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for IncrementalTranslation
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.IncrementalTranslation = {1}', Para1=REAL_TO_STRING(self._command.IncrementalTranslation))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for IncrementalRotation
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.IncrementalRotation = {1}', Para1=REAL_TO_STRING(self._command.IncrementalRotation))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Override
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Override = {1}', Para1=UINT_TO_STRING(self._command.Override))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for JogControl[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.JogControl[0] = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.JogControl[0]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for JogControl[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.JogControl[1] = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.JogControl[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for JogControl[2]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.JogControl[2] = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.JogControl[2]))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_GroupJogFB'

        self.ExecMode = ExecutionMode.SEQUENCE_SECONDARY
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(GroupJogOutCmd)), Value=0, DataLen=2)

        if State == CmdMessageState.ACTIVE:
            # Update results
            self.OutCmd.DistanceReached = bit(self._response.Status, 1)
            self.OutCmd.MotionActive = bit(self._response.Status, 2)

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(GroupJogOutCmd)), Value=0, DataLen=2)
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
                    # reset busy flag
                    self.Enabled = False  # {warning 'ToDo: doit for all others the same'}
                    # trigger parameter update to disable FB
                    self._parameterUpdateInternal = True
                    # reset the falling edge
                    self._enable_F()
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1

            case 2:
                if (self._response.State == CmdMessageState.DONE or self._response.State == CmdMessageState.ERROR) | (CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK) or (not AxesGroup.State.Initialized and (not AxesGroup.State.Synchronized)):
                    self.Reset()
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        return OnExecRun

        # Reset FB
        if self._enable_R.Q or self._enable_F.Q:
            self.Reset()
        return OnExecRun

    def OnUpdateStateFlags(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        # Reset State flags
        self.Active = False
        self.CommandAborted = False

        # Update Enable flag
        self.Enabled = bit(self._response.Status, 0)

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
                self.Active = True
                self.Busy = False
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
                self.CommandAborted = True
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

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Status
            self._response.Status = ResponseData.GetByte()
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
        # Create log entry for Status
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Status = {1}', Para1=BYTE_TO_STRING(self._response.Status))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        super().Reset()

        self.Busy = False
        self.CommandBuffered = False
        self.ParameterAccepted = False
        return Reset
