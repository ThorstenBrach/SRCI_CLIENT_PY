"""Read error codes of pending errors and move them into user data block \"RobotData\"

ST-Source: POUs/Read/MC_ReadMessages/MC_ReadMessagesFB.st
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
from srci.functions.Convert.DT import IEC_TIMESTAMP_TO_SYSTEMTIME
from srci.functions.Convert.TO_STRING.IEC_DATE_TO_STRING import IEC_DATE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_TIME_TO_STRING import IEC_TIME_TO_STRING
from srci.functions.Convert.TO_STRING.MESSAGE_LEVEL_TO_STRING import MESSAGE_LEVEL_TO_STRING
from srci.functions.Convert.TO_STRING.SEVERITY_TO_STRING import SEVERITY_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, DINT_TO_STRING, DWORD_TO_STRING, INT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, MessageLevel, MessageType, PriorityLevel, ReadMessagesOutCmd, ReadMessagesParCmd, ReadMessagesRecvData, ReadMessagesSendData, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ReadMessagesFB']


class MC_ReadMessagesFB(RobotLibraryBaseEnableFB):
    """Read error codes of pending errors and move them into user data block \"RobotData\""""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: ReadMessagesParCmd = ReadMessagesParCmd()
        # VAR_OUTPUT
        # TRUE, while the following outputs return valid values:
        # • Values
        self.Valid: bool = False
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # command outputs
        self.OutCmd: ReadMessagesOutCmd = ReadMessagesOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ReadMessagesParCmd = ReadMessagesParCmd()
        # command data to send
        self._command: ReadMessagesSendData = ReadMessagesSendData()
        # response data received
        self._response: ReadMessagesRecvData = ReadMessagesRecvData()

    def __call__(self, *, ParCmd: ReadMessagesParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 8)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 8)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 8 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 8, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(ReadMessagesSendData)), DataLen=8)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 8 - PayloadPtr, 8)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 8, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 8, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = True  # Function is mandatory
        return CheckFunctionSupported

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ReadMessages

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 2 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ReadMessagesParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ReadMessagesParCmd)), DataLen=2) != RobotLibraryConstants.OK

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
            # Reset Valid output of the FB
            self.Valid = False
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False
        # internal index for loops
        _idx: int = 0

        CheckParameterValid = True

        # Check ParCmd.MsgID valid ?
        if self.ParCmd.MsgID < 0 or self.ParCmd.MsgID > 255:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.MsgID = {1}', Para1=INT_TO_STRING(self.ParCmd.MsgID))
            return CheckParameterValid

        # Check ParCmd.MessageLevel valid ?
        if ((self.ParCmd.MessageLevel != MessageLevel.DEBUG and self.ParCmd.MessageLevel != MessageLevel.INFO) and self.ParCmd.MessageLevel != MessageLevel.WARNING) and self.ParCmd.MessageLevel != MessageLevel.ERROR:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.MessageLevel = {1}', Para1=MESSAGE_LEVEL_TO_STRING(Value=self.ParCmd.MessageLevel))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.ReadMessages
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.MsgID = self._parCmd.MsgID
        self._command.Enable = self.Enable
        self._command.MessageLevel = self._parCmd.MessageLevel

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.MsgID
            CreateCommandPayload.AddUsint(Value=self._command.MsgID)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Enable
            CreateCommandPayload.AddBool(Value=self._command.Enable)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.MessageLevel
            CreateCommandPayload.AddUsint(Value=self._command.MessageLevel)
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
        # Create log entry for MsgID
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.MsgID = {1}', Para1=USINT_TO_STRING(self._command.MsgID))

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
        # Create log entry for MessageLevel
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.MessageLevel = {1}', Para1=USINT_TO_STRING(self._command.MessageLevel))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ReadMessagesFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadMessagesOutCmd)), Value=0, DataLen=271)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.MsgId = self._response.MsgId
            self.OutCmd.NumberOfActiveErrors = self._response.NumberOfActiveErrors
            self.OutCmd.NumberOfActiveWarnings = self._response.NumberOfActiveWarnings
            copy_into(self.OutCmd.Timestamp, self._response.Timestamp)
            self.OutCmd.MsgType = MessageType(self._response.MsgType)
            self.OutCmd.Severity = Severity(self._response.Severity)
            self.OutCmd.ErrorCode = self._response.ErrorCode
            self.OutCmd.Text = self._response.Text

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
        # internal index for loops
        _idx: int = 0

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadMessagesOutCmd)), Value=0, DataLen=271)
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

                    if self.Valid:
                        # Add message to message buffer
                        AxesGroup.MessageLog.AddMessageLogByParameter(Timestamp=IEC_TIMESTAMP_TO_SYSTEMTIME(Value=self.OutCmd.Timestamp), MessageType=self.OutCmd.MsgType, MessageCode=self.OutCmd.ErrorCode, MessageText=self.OutCmd.Text, Severity=self.OutCmd.Severity)

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
        self.Valid = False

        # Update results
        self.Enabled = self._response.Enabled

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
                self.Valid = True
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

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.MsgID
            self._response.MsgId = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Enabled
            self._response.Enabled = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.NumberOfActiveErrors
            self._response.NumberOfActiveErrors = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.NumberOfActiveWarnings
            self._response.NumberOfActiveWarnings = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Timestamp.IEC_DATE
            self._response.Timestamp.IEC_DATE = ResponseData.GetIecDate()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Timestamp.IEC_TIME
            self._response.Timestamp.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.MsgType
            self._response.MsgType = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Severity
            self._response.Severity = ResponseData.GetSint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ErrorCode
            self._response.ErrorCode = ResponseData.GetDword()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get _response.RCManufacturer
            ResponseData.GetDataBlock(pData=ADR(self._response, 'Text', _iec.StringType(255)), Size=151, IsString=True)  # ST-FIX F32: 150 chars + terminator
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
        # Create log entry for Enabled
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Enabled = {1}', Para1=BOOL_TO_STRING(self._response.Enabled))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for MsgID
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.MsgID = {1}', Para1=USINT_TO_STRING(self._response.MsgId))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for NumberOfActiveErrors
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.NumberOfActiveErrors = {1}', Para1=USINT_TO_STRING(self._response.NumberOfActiveErrors))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for NumberOfActiveWarnings
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.NumberOfActiveWarnings = {1}', Para1=USINT_TO_STRING(self._response.NumberOfActiveWarnings))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Timestamp.IEC_DATE
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Timestamp.IEC_DATE = {1}', Para1=IEC_DATE_TO_STRING(Value=self._response.Timestamp.IEC_DATE))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Timestamp.IEC_TIME
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Timestamp.IEC_TIME = {1}', Para1=IEC_TIME_TO_STRING(Value=self._response.Timestamp.IEC_TIME))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for MsgType
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.MsgType = {1}', Para1=USINT_TO_STRING(self._response.MsgType))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Severity
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Severity = {1}', Para1=SEVERITY_TO_STRING(Value=Severity(self._response.Severity), AlignString=False))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ErrorCode
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ErrorCode = {1}', Para1=DWORD_TO_STRING(self._response.ErrorCode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Text
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Text = {1}', Para1=self._response.Text)

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Busy = False
        self.Valid = False
        self.CommandBuffered = False
        return Reset
