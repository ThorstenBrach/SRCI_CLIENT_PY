"""Capture trigger Position, measuring input

ST-Source: POUs/Additional/MC_MeasuringInput/MC_MeasuringInputFB.st
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
from srci.functions.Convert.TO_STRING.ARM_CONFIG_TO_STRING import ARM_CONFIG_TO_STRING
from srci.functions.Convert.TO_STRING.MEASURING_IO_MODE_TO_STRING import MEASURING_IO_MODE_TO_STRING
from srci.iec.conv import DINT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, UINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, st_for_end, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, MeasuringInputOutCmd, MeasuringInputParCmd, MeasuringInputRecvData, MeasuringInputSendData, MeasuringIoMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_MeasuringInputFB']


class MC_MeasuringInputFB(RobotLibraryBaseExecuteFB):
    """Capture trigger Position, measuring input"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: MeasuringInputParCmd = MeasuringInputParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # Command output
        self.OutCmd: MeasuringInputOutCmd = MeasuringInputOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: MeasuringInputParCmd = MeasuringInputParCmd()
        # command data to send
        self._command: MeasuringInputSendData = MeasuringInputSendData()
        # response data received
        self._response: MeasuringInputRecvData = MeasuringInputRecvData()
        # VAR_OUTPUT
        self.CommandAborted: bool = False

    def __call__(self, *, ParCmd: MeasuringInputParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ParCmd is not None:
            copy_into(self.ParCmd, ParCmd)
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 8)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 8)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 8 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 8, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(MeasuringInputSendData)), DataLen=8)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 8 - PayloadPtr, 8)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 8, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 8, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.MeasuringInput

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 3 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(MeasuringInputParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(MeasuringInputParCmd)), DataLen=3) != RobotLibraryConstants.OK

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

        # Check ParCmd.MeasuringMode valid ?
        if (((self.ParCmd.MeasuringMode != MeasuringIoMode.MEASUREMENT_AT_NEXT_RISING_EDGE and self.ParCmd.MeasuringMode != MeasuringIoMode.MEASUREMENT_AT_NEXT_FALLING_EDGE) and self.ParCmd.MeasuringMode != MeasuringIoMode.MEASUREMENT_AT_NEXT_EDGE) and self.ParCmd.MeasuringMode != MeasuringIoMode.MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_RISING) and self.ParCmd.MeasuringMode != MeasuringIoMode.MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_FALLING:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.MeasuringMode = {1}', Para1=MEASURING_IO_MODE_TO_STRING(Value=self.ParCmd.MeasuringMode))
            return CheckParameterValid

        # Check ParCmd.Index valid ?
        if self.ParCmd.Index < 0 or self.ParCmd.Index > 255:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Index = {1}', Para1=USINT_TO_STRING(self.ParCmd.Index))
            return CheckParameterValid

        # Check ParCmd.BitNumber valid ?
        if self.ParCmd.BitNumber < 0 or self.ParCmd.BitNumber > 255:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.BitNumber = {1}', Para1=USINT_TO_STRING(self.ParCmd.BitNumber))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.MeasuringInput
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority

        self._command.MeasuringMode = self.ParCmd.MeasuringMode
        self._command.Index = self.ParCmd.Index
        self._command.BitNumber = self.ParCmd.BitNumber

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.MeasuringMode
            CreateCommandPayload.AddUsint(Value=self._command.MeasuringMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Index
            CreateCommandPayload.AddUsint(Value=self._command.Index)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.BitNumber
            CreateCommandPayload.AddUsint(Value=self._command.BitNumber)
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
        # Create log entry for MeasuringMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.MeasuringMode = {1}', Para1=USINT_TO_STRING(self._command.MeasuringMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Index
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Index = {1}', Para1=USINT_TO_STRING(self._command.Index))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for BitNumber
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.BitNumber = {1}', Para1=USINT_TO_STRING(self._command.BitNumber))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_MeasuringInputFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(MeasuringInputOutCmd)), Value=0, DataLen=224)

        if State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.MeasuringID = self._response.MeasuringID
            copy_into(self.OutCmd.Measurings, self._response.Measurings)

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(MeasuringInputOutCmd)), Value=0, DataLen=224)
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
                pass
            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                pass
            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass
            # Successfully completed
            case CmdMessageState.DONE:
                self.Done = True
                self.Busy = False
            # Aborted before completion
            case CmdMessageState.ABORTED:
                self.Busy = False
            # Encountered an error during execution
            case CmdMessageState.ERROR:
                self.Error = True
                self.Busy = False

        # ST-FIX F45: output CommandAborted
        self.CommandAborted = State == CmdMessageState.ABORTED

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
            # Get Response.MeasuringID
            self._response.MeasuringID = ResponseData.GetUint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].ToolNo
            self._response.Measurings[1].ToolNo = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].FrameNo
            self._response.Measurings[1].FrameNo = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].ToolNo
            self._response.Measurings[2].ToolNo = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].FrameNo
            self._response.Measurings[2].FrameNo = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.X
            self._response.Measurings[1].MeasuredCartesianPosition.X = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.Y
            self._response.Measurings[1].MeasuredCartesianPosition.Y = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.Z
            self._response.Measurings[1].MeasuredCartesianPosition.Z = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.Rx
            self._response.Measurings[1].MeasuredCartesianPosition.Rx = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.Ry
            self._response.Measurings[1].MeasuredCartesianPosition.Ry = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.Rz
            self._response.Measurings[1].MeasuredCartesianPosition.Rz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.Config
            copy_into(self._response.Measurings[1].MeasuredCartesianPosition.Config, ResponseData.GetArmConfig())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.TurnNumber
            copy_into(self._response.Measurings[1].MeasuredCartesianPosition.TurnNumber, ResponseData.GetTurnNumbers())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.E1
            self._response.Measurings[1].MeasuredCartesianPosition.E1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.J1
            self._response.Measurings[1].MeasuredJointPosition.J1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.J2
            self._response.Measurings[1].MeasuredJointPosition.J2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.J3
            self._response.Measurings[1].MeasuredJointPosition.J3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.J4
            self._response.Measurings[1].MeasuredJointPosition.J4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.J5
            self._response.Measurings[1].MeasuredJointPosition.J5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.J6
            self._response.Measurings[1].MeasuredJointPosition.J6 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.E1
            self._response.Measurings[1].MeasuredJointPosition.E1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.X
            self._response.Measurings[2].MeasuredCartesianPosition.X = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.Y
            self._response.Measurings[2].MeasuredCartesianPosition.Y = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.Z
            self._response.Measurings[2].MeasuredCartesianPosition.Z = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.Rx
            self._response.Measurings[2].MeasuredCartesianPosition.Rx = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.Ry
            self._response.Measurings[2].MeasuredCartesianPosition.Ry = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.Rz
            self._response.Measurings[2].MeasuredCartesianPosition.Rz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.Config
            copy_into(self._response.Measurings[2].MeasuredCartesianPosition.Config, ResponseData.GetArmConfig())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.TurnNumber
            copy_into(self._response.Measurings[2].MeasuredCartesianPosition.TurnNumber, ResponseData.GetTurnNumbers())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.E1
            self._response.Measurings[2].MeasuredCartesianPosition.E1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.J1
            self._response.Measurings[2].MeasuredJointPosition.J1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.J2
            self._response.Measurings[2].MeasuredJointPosition.J2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.J3
            self._response.Measurings[2].MeasuredJointPosition.J3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.J4
            self._response.Measurings[2].MeasuredJointPosition.J4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.J5
            self._response.Measurings[2].MeasuredJointPosition.J5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.J6
            self._response.Measurings[2].MeasuredJointPosition.J6 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.E1
            self._response.Measurings[2].MeasuredJointPosition.E1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.E2
            self._response.Measurings[1].MeasuredCartesianPosition.E2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.E3
            self._response.Measurings[1].MeasuredCartesianPosition.E3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.E4
            self._response.Measurings[1].MeasuredCartesianPosition.E4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.E5
            self._response.Measurings[1].MeasuredCartesianPosition.E5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredCartesianPosition.E6
            self._response.Measurings[1].MeasuredCartesianPosition.E6 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.E2
            self._response.Measurings[1].MeasuredJointPosition.E2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.E3
            self._response.Measurings[1].MeasuredJointPosition.E3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.E4
            self._response.Measurings[1].MeasuredJointPosition.E4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.E5
            self._response.Measurings[1].MeasuredJointPosition.E5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[1].MeasuredJointPosition.E6
            self._response.Measurings[1].MeasuredJointPosition.E6 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.E2
            self._response.Measurings[2].MeasuredCartesianPosition.E2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.E3
            self._response.Measurings[2].MeasuredCartesianPosition.E3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.E4
            self._response.Measurings[2].MeasuredCartesianPosition.E4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.E5
            self._response.Measurings[2].MeasuredCartesianPosition.E5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredCartesianPosition.E6
            self._response.Measurings[2].MeasuredCartesianPosition.E6 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.E2
            self._response.Measurings[2].MeasuredJointPosition.E2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.E3
            self._response.Measurings[2].MeasuredJointPosition.E3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.E4
            self._response.Measurings[2].MeasuredJointPosition.E4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.E5
            self._response.Measurings[2].MeasuredJointPosition.E5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Measurings[2].MeasuredJointPosition.E6
            self._response.Measurings[2].MeasuredJointPosition.E6 = ResponseData.GetReal()
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
        # internal index for loops
        _idx: int = 0

        # Create log entry for Parameter start
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} parameter(s) to parse from the response data:', Para1=DINT_TO_STRING(ParameterCnt))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for MeasuringID
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.MeasuringID = {1}', Para1=UINT_TO_STRING(self._response.MeasuringID))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for MeasuringID
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.MeasuringID = {1}', Para1=UINT_TO_STRING(self._response.MeasuringID))

        # Create log entry for Measurings[x]
        for _idx in range(1, 3):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].ToolNo
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].ToolNo = {1}', Para1=USINT_TO_STRING(self._response.Measurings[_idx].ToolNo), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].FrameNo
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].FrameNo = {1}', Para1=USINT_TO_STRING(self._response.Measurings[_idx].FrameNo), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(1, 2)

        # Create log entry for Measurings[x]
        for _idx in range(1, 3):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.X
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.X = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.X), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.Y
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.Y = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.Y), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.Z
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.Z = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.Z), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.Rx
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.Rx = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.Rx), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.Ry
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.Ry = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.Ry), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.Rz
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.Rz = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.Rz), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.Config
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.Config = {1}', Para1=ARM_CONFIG_TO_STRING(Value=self._response.Measurings[_idx].MeasuredCartesianPosition.Config), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.TurnNumber.J1Turns
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.TurnNumber.J1Turns = {1}', Para1=SINT_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.TurnNumber.J1Turns), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.TurnNumber.J2Turns
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.TurnNumber.J2Turns = {1}', Para1=SINT_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.TurnNumber.J2Turns), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.TurnNumber.J3Turns
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.TurnNumber.J3Turns = {1}', Para1=SINT_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.TurnNumber.J3Turns), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.TurnNumber.J4Turns
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.TurnNumber.J4Turns = {1}', Para1=SINT_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.TurnNumber.J4Turns), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.TurnNumber.J5Turns
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.TurnNumber.J5Turns = {1}', Para1=SINT_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.TurnNumber.J5Turns), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.TurnNumber.J6Turns
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.TurnNumber.J6Turns = {1}', Para1=SINT_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.TurnNumber.J6Turns), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.TurnNumber.E1Turns
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.TurnNumber.E1Turns = {1}', Para1=SINT_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.TurnNumber.E1Turns), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.E1
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.E1 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.E1), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.J1
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.J1 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.J1), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.J2
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.J2 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.J2), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.J3
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.J3 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.J3), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.J4
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.J4 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.J4), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.J5
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.J5 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.J5), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.J6
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.J6 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.J6), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.E1
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.E1 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.E1), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(1, 2)

        # Create log entry for Measurings[x]
        for _idx in range(1, 3):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.E2
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.E2 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.E2), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.E3
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.E3 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.E3), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.E4
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.E4 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.E4), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.E5
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.E5 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.E5), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredCartesianPosition.E6
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredCartesianPosition.E6 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredCartesianPosition.E6), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.E2
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.E2 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.E2), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.E3
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.E3 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.E3), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.E4
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.E4 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.E4), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.E5
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.E5 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.E5), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Measurings[x].MeasuredJointPosition.E6
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Measurings[{2}].MeasuredJointPosition.E6 = {1}', Para1=REAL_TO_STRING(self._response.Measurings[_idx].MeasuredJointPosition.E6), Para2=DINT_TO_STRING(_idx))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False

        # ST-FIX F45
        self.CommandAborted = False
        return Reset
