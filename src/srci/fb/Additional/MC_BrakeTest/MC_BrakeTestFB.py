# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_BrakeTestFB
#  Author:      Thorsten Brach
#  Date:        2024-06-01
#
#  Description:
#    Activate robot cycle brake test and give feedback to PLC
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

"""Activate robot cycle brake test and give feedback to PLC

ST-Source: POUs/Additional/MC_BrakeTest/MC_BrakeTestFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
import srci.types as _T
from srci.fb._internal.BaseFBs.RobotLibraryBaseExecuteFB import RobotLibraryBaseExecuteFB
from srci.fb._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from srci.fb._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from srci.functions.Common import SetTimeout
from srci.functions.Convert.TO_STRING.ABORTING_MODE_TO_STRING import ABORTING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.BYTE_TO_STRING_BIN import BYTE_TO_STRING_BIN
from srci.functions.Convert.TO_STRING.EXTERNAL_AXES_FLAGS_TO_STRING import EXTERNAL_AXES_FLAGS_TO_STRING
from srci.functions.Convert.TO_STRING.ROBOT_AXES_FLAGS_TO_STRING import ROBOT_AXES_FLAGS_TO_STRING
from srci.functions.Convert.TO_STRING.SEQUENCE_FLAG_TO_STRING import SEQUENCE_FLAG_TO_STRING
from srci.iec.conv import DINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, bit, copy_into, copy_value, set_bit, trunc_str, wrap
from srci.types import AbortingMode, AbortingModeEnum, BrakeTestOutCmd, BrakeTestParCmd, BrakeTestRecvData, BrakeTestSendData, CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, SequenceFlag, SequenceFlagEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_BrakeTestFB']


class MC_BrakeTestFB(RobotLibraryBaseExecuteFB):
    """Activate robot cycle brake test and give feedback to PLC"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: BrakeTestParCmd = BrakeTestParCmd()
        # Parameter which determines the behavior towards the previously sent and still active or buffered commands.
        self.AbortingMode: AbortingMode = AbortingMode.BUFFER
        # Defines the target sequence in which the command will be executed
        self.SequenceFlag: SequenceFlag = SequenceFlag.NO_SEQUENCE
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # During the realization of the brake test, the command controls the motion of the respective axis group.
        # TRUE: The brake test is being realized
        # FALSE: The brake test is not realized
        self.Active: bool = False
        # The command was aborted by another command.
        self.CommandAborted: bool = False
        # TRUE, while command is interrupted during execution and can be continued
        self.CommandInterrupted: bool = False
        # Command output
        self.OutCmd: BrakeTestOutCmd = BrakeTestOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: BrakeTestParCmd = BrakeTestParCmd()
        # command data to send
        self._command: BrakeTestSendData = BrakeTestSendData()
        # response data received
        self._response: BrakeTestRecvData = BrakeTestRecvData()

    def __call__(self, *, ParCmd: BrakeTestParCmd | None = None, AbortingMode: AbortingMode | None = None, SequenceFlag: SequenceFlag | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ParCmd is not None:
            copy_into(self.ParCmd, ParCmd)
        if AbortingMode is not None:
            self.AbortingMode = AbortingMode(AbortingMode)
        if SequenceFlag is not None:
            self.SequenceFlag = SequenceFlag(SequenceFlag)
        if Execute is not None:
            self.Execute = Execute
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
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 7, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(BrakeTestSendData)), DataLen=7)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 7 - PayloadPtr, 7)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 7, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 7, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.BrakeTest

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
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(BrakeTestParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(BrakeTestParCmd)), DataLen=16) != RobotLibraryConstants.OK

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
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False

        CheckParameterValid = True

        # Check ParCmd.SequenceFlag valid ?
        if self.SequenceFlag != SequenceFlag.PRIMARY_SEQUENCE and self.SequenceFlag != SequenceFlag.SECONDARY_SEQUENCE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SEQFLAG_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter SequenceFlag = {1}', Para1=SEQUENCE_FLAG_TO_STRING(Value=self.SequenceFlag))
            return CheckParameterValid

        # Check AbortingMode valid ?
        if self.AbortingMode != AbortingMode.BUFFER and self.AbortingMode != AbortingMode.ABORT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_ABORTINGMODE_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter AbortingMode = {1}', Para1=ABORTING_MODE_TO_STRING(Value=self.AbortingMode))
            return CheckParameterValid

        # Check RobotAxesActive valid ?
        if ((((self.ParCmd.RobotAxesActive.AxisJ1 and (not AxesGroup.State.RobotData.AxisJointUsed.J1) or (self.ParCmd.RobotAxesActive.AxisJ2 and (not AxesGroup.State.RobotData.AxisJointUsed.J2))) or (self.ParCmd.RobotAxesActive.AxisJ3 and (not AxesGroup.State.RobotData.AxisJointUsed.J3))) or (self.ParCmd.RobotAxesActive.AxisJ4 and (not AxesGroup.State.RobotData.AxisJointUsed.J4))) or (self.ParCmd.RobotAxesActive.AxisJ5 and (not AxesGroup.State.RobotData.AxisJointUsed.J5))) or (self.ParCmd.RobotAxesActive.AxisJ6 and (not AxesGroup.State.RobotData.AxisJointUsed.J6)):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.RobotAxesActive = {1}', Para1=ROBOT_AXES_FLAGS_TO_STRING(Value=self.ParCmd.RobotAxesActive))
            return CheckParameterValid

        # Check ExternalAxesActive valid ?
        if ((((self.ParCmd.ExternalAxesActive.AxisE1 and (not AxesGroup.State.RobotData.AxisExternalUsed.E1) or (self.ParCmd.ExternalAxesActive.AxisE2 and (not AxesGroup.State.RobotData.AxisExternalUsed.E2))) or (self.ParCmd.ExternalAxesActive.AxisE3 and (not AxesGroup.State.RobotData.AxisExternalUsed.E3))) or (self.ParCmd.ExternalAxesActive.AxisE4 and (not AxesGroup.State.RobotData.AxisExternalUsed.E4))) or (self.ParCmd.ExternalAxesActive.AxisE5 and (not AxesGroup.State.RobotData.AxisExternalUsed.E5))) or (self.ParCmd.ExternalAxesActive.AxisE6 and (not AxesGroup.State.RobotData.AxisExternalUsed.E6)):
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExternalAxesActive = {1}', Para1=EXTERNAL_AXES_FLAGS_TO_STRING(Value=self.ParCmd.ExternalAxesActive))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.BrakeTest
        # ST-FIX F51: ExecutionMode from AbortingMode and SequenceFlag (spec table 5-77)
        if self.SequenceFlag == SequenceFlag.SECONDARY_SEQUENCE:
            if self.AbortingMode == AbortingMode.ABORT:
                self._command.ExecMode = ExecutionMode.SEQUENCE_ABORT_OTHERS_SECONDARY
            else:
                self._command.ExecMode = ExecutionMode.SEQUENCE_SECONDARY
        else:
            if self.AbortingMode == AbortingMode.ABORT:
                self._command.ExecMode = ExecutionMode.SEQUENCE_ABORT_OTHERS_PRIMARY
            else:
                self._command.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.RobotAxesActive = set_bit(self._command.RobotAxesActive, 0, self._parCmd.RobotAxesActive.Bit00)
        self._command.RobotAxesActive = set_bit(self._command.RobotAxesActive, 1, self._parCmd.RobotAxesActive.AxisJ1)
        self._command.RobotAxesActive = set_bit(self._command.RobotAxesActive, 2, self._parCmd.RobotAxesActive.AxisJ2)
        self._command.RobotAxesActive = set_bit(self._command.RobotAxesActive, 3, self._parCmd.RobotAxesActive.AxisJ3)
        self._command.RobotAxesActive = set_bit(self._command.RobotAxesActive, 4, self._parCmd.RobotAxesActive.AxisJ4)
        self._command.RobotAxesActive = set_bit(self._command.RobotAxesActive, 5, self._parCmd.RobotAxesActive.AxisJ5)
        self._command.RobotAxesActive = set_bit(self._command.RobotAxesActive, 6, self._parCmd.RobotAxesActive.AxisJ6)
        self._command.RobotAxesActive = set_bit(self._command.RobotAxesActive, 7, self._parCmd.RobotAxesActive.Bit07)
        self._command.ExternalAxesActive = set_bit(self._command.ExternalAxesActive, 0, self._parCmd.ExternalAxesActive.Bit00)
        self._command.ExternalAxesActive = set_bit(self._command.ExternalAxesActive, 1, self._parCmd.ExternalAxesActive.AxisE1)
        self._command.ExternalAxesActive = set_bit(self._command.ExternalAxesActive, 2, self._parCmd.ExternalAxesActive.AxisE2)
        self._command.ExternalAxesActive = set_bit(self._command.ExternalAxesActive, 3, self._parCmd.ExternalAxesActive.AxisE3)
        self._command.ExternalAxesActive = set_bit(self._command.ExternalAxesActive, 4, self._parCmd.ExternalAxesActive.AxisE4)
        self._command.ExternalAxesActive = set_bit(self._command.ExternalAxesActive, 5, self._parCmd.ExternalAxesActive.AxisE5)
        self._command.ExternalAxesActive = set_bit(self._command.ExternalAxesActive, 6, self._parCmd.ExternalAxesActive.AxisE6)
        self._command.ExternalAxesActive = set_bit(self._command.ExternalAxesActive, 7, self._parCmd.ExternalAxesActive.Bit07)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EmitterID[0]
            CreateCommandPayload.AddByte(Value=self._command.RobotAxesActive)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EmitterID[1]
            CreateCommandPayload.AddByte(Value=self._command.ExternalAxesActive)
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
        # Create log entry for RobotAxesActive
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.RobotAxesActive = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.RobotAxesActive))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ExternalAxesActive
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ExternalAxesActive = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.ExternalAxesActive))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_BrakeTestFB'

        self.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
        self.Priority = PriorityLevel.NORMAL
        self.SequenceFlag = SequenceFlag.PRIMARY_SEQUENCE
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(BrakeTestOutCmd)), Value=0, DataLen=32)

        if State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.RobotAxesStatus.Bit00 = bit(self._response.RobotAxesStatus, 0)
            self.OutCmd.RobotAxesStatus.AxisJ1 = bit(self._response.RobotAxesStatus, 1)
            self.OutCmd.RobotAxesStatus.AxisJ2 = bit(self._response.RobotAxesStatus, 2)
            self.OutCmd.RobotAxesStatus.AxisJ3 = bit(self._response.RobotAxesStatus, 3)
            self.OutCmd.RobotAxesStatus.AxisJ4 = bit(self._response.RobotAxesStatus, 4)
            self.OutCmd.RobotAxesStatus.AxisJ5 = bit(self._response.RobotAxesStatus, 5)
            self.OutCmd.RobotAxesStatus.AxisJ6 = bit(self._response.RobotAxesStatus, 6)
            self.OutCmd.RobotAxesStatus.Bit07 = bit(self._response.RobotAxesStatus, 7)

            self.OutCmd.RobotAxesWarning.Bit00 = bit(self._response.RobotAxesWarning, 0)
            self.OutCmd.RobotAxesWarning.AxisJ1 = bit(self._response.RobotAxesWarning, 1)
            self.OutCmd.RobotAxesWarning.AxisJ2 = bit(self._response.RobotAxesWarning, 2)
            self.OutCmd.RobotAxesWarning.AxisJ3 = bit(self._response.RobotAxesWarning, 3)
            self.OutCmd.RobotAxesWarning.AxisJ4 = bit(self._response.RobotAxesWarning, 4)
            self.OutCmd.RobotAxesWarning.AxisJ5 = bit(self._response.RobotAxesWarning, 5)
            self.OutCmd.RobotAxesWarning.AxisJ6 = bit(self._response.RobotAxesWarning, 6)
            self.OutCmd.RobotAxesWarning.Bit07 = bit(self._response.RobotAxesWarning, 7)

            self.OutCmd.ExternalAxesStatus.Bit00 = bit(self._response.ExternalAxesStatus, 0)
            self.OutCmd.ExternalAxesStatus.AxisE1 = bit(self._response.ExternalAxesStatus, 1)
            self.OutCmd.ExternalAxesStatus.AxisE2 = bit(self._response.ExternalAxesStatus, 2)
            self.OutCmd.ExternalAxesStatus.AxisE3 = bit(self._response.ExternalAxesStatus, 3)
            self.OutCmd.ExternalAxesStatus.AxisE4 = bit(self._response.ExternalAxesStatus, 4)
            self.OutCmd.ExternalAxesStatus.AxisE5 = bit(self._response.ExternalAxesStatus, 5)
            self.OutCmd.ExternalAxesStatus.AxisE6 = bit(self._response.ExternalAxesStatus, 6)
            self.OutCmd.ExternalAxesStatus.Bit07 = bit(self._response.ExternalAxesStatus, 7)

            self.OutCmd.ExternalAxesWarning.Bit00 = bit(self._response.ExternalAxesWarning, 0)
            self.OutCmd.ExternalAxesWarning.AxisE1 = bit(self._response.ExternalAxesWarning, 1)
            self.OutCmd.ExternalAxesWarning.AxisE2 = bit(self._response.ExternalAxesWarning, 2)
            self.OutCmd.ExternalAxesWarning.AxisE3 = bit(self._response.ExternalAxesWarning, 3)
            self.OutCmd.ExternalAxesWarning.AxisE4 = bit(self._response.ExternalAxesWarning, 4)
            self.OutCmd.ExternalAxesWarning.AxisE5 = bit(self._response.ExternalAxesWarning, 5)
            self.OutCmd.ExternalAxesWarning.AxisE6 = bit(self._response.ExternalAxesWarning, 6)
            self.OutCmd.ExternalAxesWarning.Bit07 = bit(self._response.ExternalAxesWarning, 7)

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecRun: int = 0

        # call base implementation
        super().OnExecRun(AxesGroup=AxesGroup)

        match self._stepCmd:

            case 0:
                if self._execute_R.Q and (not self.Error):
                    # Check function is supported and parameter are valid ?
                    if self.CheckFunctionSupported(AxesGroup=AxesGroup) & self.CheckParameterValid(AxesGroup=AxesGroup):
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(BrakeTestOutCmd)), Value=0, DataLen=32)
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

                    # Done, Aborted or Error ?
                    if self._response.State >= CmdMessageState.DONE:
                        # set timeout
                        SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                        # inc step counter
                        self._stepCmd = self._stepCmd + 1

            case 2:
                if not self.Execute:
                    self.Reset()
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # Reset FB
        if not self.Execute:
            self.Reset()
        return OnExecRun

    def OnUpdateStateFlags(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        # Reset State flags
        self.Active = False
        self.CommandAborted = False
        self.CommandInterrupted = False
        self.Done = False

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
            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER:
                self.CommandBuffered = True
            # Currently active and in progress
            case CmdMessageState.ACTIVE:
                self.Active = True
            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                self.CommandInterrupted = True
            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass
            # Successfully completed
            case CmdMessageState.DONE:
                self.Done = True
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
            # Get RobotAxesStatus
            self._response.RobotAxesStatus = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get ExternalAxesStatus
            self._response.ExternalAxesStatus = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get RobotAxesWarning
            self._response.RobotAxesWarning = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get ExternalAxesWarning
            self._response.ExternalAxesWarning = ResponseData.GetByte()
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
        # Create log entry for RobotAxesStatus
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.RobotAxesStatus = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._response.RobotAxesStatus))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ExternalAxesStatus
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ExternalAxesStatus = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._response.ExternalAxesStatus))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for RobotAxesWarning
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.RobotAxesWarning = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._response.RobotAxesWarning))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ExternalAxesWarning
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ExternalAxesWarning = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._response.ExternalAxesWarning))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.Active = False
        self.CommandBuffered = False
        self.CommandAborted = False
        self.CommandInterrupted = False
        return Reset
