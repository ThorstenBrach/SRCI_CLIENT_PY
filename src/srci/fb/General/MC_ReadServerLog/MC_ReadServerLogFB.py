# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_ReadServerLogFB
#  Author:      Thorsten Brach
#  Date:        2026-10-23
#
#  Description:
#    Read a server log of the RC line by line into LogFile
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""Read a server log of the RC line by line into LogFile

ST-Source: POUs/General/MC_ReadServerLog/MC_ReadServerLogFB.st
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
from srci.iec.conv import BOOL_TO_STRING, BYTE_TO_STRING, DINT_TO_STRING, DINT_TO_UDINT, INT_TO_STRING, INT_TO_UINT, UDINT_TO_REAL, UDINT_TO_STRING, UINT_TO_STRING, USINT_TO_DINT, USINT_TO_STRING
from srci.iec.rt import ADR, ADR_ELEM, LIMIT, LOWER_BOUND, MIN, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, UPPER_BOUND, bit, copy_into, copy_value, st_for_end, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, ReadServerLogOutCmd, ReadServerLogParCmd, ReadServerLogRecvData, ReadServerLogSendData, RobotLibraryConstants, RobotLibraryErrorIdEnum, RobotLibraryParameter, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ReadServerLogFB']


class MC_ReadServerLogFB(RobotLibraryBaseExecuteFB):
    """Read a server log of the RC line by line into LogFile"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: ReadServerLogParCmd = ReadServerLogParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # command outputs
        self.OutCmd: ReadServerLogOutCmd = ReadServerLogOutCmd()
        # VAR_IN_OUT
        # Requested log file: one log line per element
        self.LogFile: list[str] = None
        # VAR
        # internal copy of command parameter
        self._parCmd: ReadServerLogParCmd = ReadServerLogParCmd()
        # command data to send
        self._command: ReadServerLogSendData = ReadServerLogSendData()
        # response data received
        self._response: ReadServerLogRecvData = ReadServerLogRecvData()
        # a part of the log was received and must be stored in LogFile (StoreLogContent)
        self._contentReceived: bool = False
        # the response to the current Offset was handled
        self._offsetHandled: bool = False
        # new rising edge of Execute during the transfer: start again after the end of this one
        self._restart: bool = False
        # index of the element of LogFile for the current log line
        self._line: int = 0
        # number of elements of LogFile used by this transfer
        self._lines: int = 0
        # a log line is open (parts received, end of line not yet)
        self._lineOpen: bool = False
        # characters of the current log line
        self._lineLen: int = 0
        # characters copied from the received part
        self._copyLen: int = 0

    def __call__(self, *, ParCmd: ReadServerLogParCmd | None = None, LogFile: list[str] | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ParCmd is not None:
            copy_into(self.ParCmd, ParCmd)
        if LogFile is not None:
            self.LogFile = LogFile
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

        # store the received part of the log (LogFile is only reachable in the call of the block)
        self.StoreLogContent(AxesGroup=self.AxesGroup, LogFile=self.LogFile)

    def CheckAddParameter(self, *, PayloadPtr: int = 0) -> bool:  # INTERNAL
        CheckAddParameter: bool = False
        # Payload as byte array
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 27)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 27)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 27 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 27, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(ReadServerLogSendData)), DataLen=27)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 27 - PayloadPtr, 27)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 27, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 27, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        # ReadServerLog is a mandatory function of the profile Core (spec table 6-119): the RC
        # reports no bit for it in RCSupportedFunctions
        CheckFunctionSupported = True
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # The parameters of the transfer are taken with the rising edge of Execute; during the transfer
        # only the block itself sends updates (next part of the log: Offset, end: Enable FALSE)
        if self._stepCmd == 0:
            return CheckParameterChanged

        if self._parameterUpdateInternal:
            # reset internal flag for send parameter update
            self._parameterUpdateInternal = False
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

        # Check ParCmd.ExportMode: only 0 (output LogFile), the export to a file is optional (table 6-119)
        if self.ParCmd.ExportMode != 0:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_EXPORTMODE_NOT_EXIST, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExportMode = {1}', Para1=USINT_TO_STRING(self.ParCmd.ExportMode))
            return CheckParameterValid

        # Check ParCmd.StartLine: the first line is 1 (log header)
        if self.ParCmd.StartLine == 0:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.StartLine = {1}', Para1=UDINT_TO_STRING(self.ParCmd.StartLine))
            return CheckParameterValid

        # Check ParCmd.ServerLogID: -1 (latest), 0 (oldest) or an ID
        if self.ParCmd.ServerLogID < -1:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ServerLogID = {1}', Para1=INT_TO_STRING(self.ParCmd.ServerLogID))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # internal index for loops
        _idx: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.ReadServerLog
        # spec table 6-121: parallel only (default of ExecMode, FB_init)
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.Reserve = 0
        # -1 (latest) -> 16#FFFF
        self._command.ServerLogID = INT_TO_UINT(self._parCmd.ServerLogID)
        self._command.StartLine = self._parCmd.StartLine
        for _idx in range(0, 10):
            self._command.ContextFilter[_idx] = self._parCmd.ContextFilter[_idx]
        else:
            _idx = st_for_end(0, 9)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
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
            # add command.ServerLogID
            CreateCommandPayload.AddUint(Value=self._command.ServerLogID)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.StartLine
            CreateCommandPayload.AddUdint(Value=self._command.StartLine)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset
            CreateCommandPayload.AddUdint(Value=self._command.Offset)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        for _idx in range(0, 10):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.ContextFilter[x]
                CreateCommandPayload.AddUsint(Value=self._command.ContextFilter[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

        # Create logging
        self.CreateCommandPayloadLog(AxesGroup=AxesGroup, ParameterCnt=_parameterCnt)
        return CreateCommandPayload

    def CreateCommandPayloadLog(self, *, AxesGroup: _T.AxesGroup, ParameterCnt: int = 0) -> None:  # INTERNAL
        # internal index for loops
        _idx: int = 0

        # Create log entry for Parameter start
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Create command payload with {1} parameter(s) :', Para1=DINT_TO_STRING(ParameterCnt))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Command.Enable
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Enable = {1}', Para1=BOOL_TO_STRING(self._command.Enable))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Command.Reserve
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve = {1}', Para1=BYTE_TO_STRING(self._command.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Command.ServerLogID
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ServerLogID = {1}', Para1=UINT_TO_STRING(self._command.ServerLogID))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Command.StartLine
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.StartLine = {1}', Para1=UDINT_TO_STRING(self._command.StartLine))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Command.Offset
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset = {1}', Para1=UDINT_TO_STRING(self._command.Offset))

        for _idx in range(0, 10):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.ContextFilter
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ContextFilter[{2}] = {1}', Para1=USINT_TO_STRING(self._command.ContextFilter[_idx]), Para2=DINT_TO_STRING(_idx))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ReadServerLogFB'

        # spec 6.2.6: processed with low priority because of its processing time
        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.LOW
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadServerLogOutCmd)), Value=0, DataLen=21)
        # the counters of the log come with every part (StoreLogContent), the received lines are counted there

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecRun: int = 0

        # call base implementation
        super().OnExecRun(AxesGroup=AxesGroup)

        match self._stepCmd:

            case 0:
                if (self._execute_R.Q or self._restart) and (not self.Error):
                    self._restart = False
                    # Check function is supported and parameter are valid ?
                    if self.CheckFunctionSupported(AxesGroup=AxesGroup) & self.CheckParameterValid(AxesGroup=AxesGroup):
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadServerLogOutCmd)), Value=0, DataLen=21)
                        # apply command parameter
                        copy_into(self._parCmd, self.ParCmd)
                        # first element of LogFile, no open line
                        self._line = 0
                        self._lines = 0
                        self._lineOpen = False
                        self._lineLen = 0
                        self._contentReceived = False
                        self._offsetHandled = False
                        # transfer on, first request
                        self._command.Enable = True
                        self._command.Offset = 1
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
                # command again. SRCI SDK 1.1 keeps the read position of a running command, so the transfer
                # ends first (Enable FALSE) and the command is added again (new ACR entry).
                if self._executeRestart_R.Q and (not self._restart):
                    self._restart = True
                    self._command.Enable = False
                    self._parameterUpdateInternal = True

                # Wait for responce received
                if self._responseReceived:
                    # reset response received flag
                    self._responseReceived = False

                    match self._response.State:
                        case CmdMessageState.DONE:
                            if self._restart:
                                # the old transfer ended: start again (step 00)
                                self.Reset()
                                self._restart = True
                            else:
                                self.OnUpdateStateFlags(State=self._response.State)
                                # set timeout
                                SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                                # inc step counter
                                self._stepCmd = self._stepCmd + 1

                        case CmdMessageState.ABORTED | CmdMessageState.ERROR:
                            self._restart = False
                            self.OnUpdateStateFlags(State=self._response.State)
                            # set timeout
                            SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                            # inc step counter
                            self._stepCmd = self._stepCmd + 1
                        case _:
                            self.OnUpdateStateFlags(State=self._response.State)
                            # a part of the log for the current request ? (responses to older requests are ignored)
                            if ((self._command.Enable and (not self._restart)) and (not self._offsetHandled)) and self._response.Offset == self._command.Offset:
                                self._offsetHandled = True
                                self._contentReceived = True

            case 2:
                if not self.Execute:
                    self.Reset()
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # Reset FB
        if not self.Execute and (not self._restart):
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
                self.CommandBuffered = True
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
        # Byte 13: line flags
        _flags: int = 0

        # call base implementation to parse the header from payload buffer
        ResponseData.PayloadPtr = super().ParseResponsePayload(ResponseData=ResponseData, Timestamp=Timestamp)

        # missing (trailing zero) bytes of the payload are 0, no values of the previous response
        SysDepMemSet(pDest=ADR(self, '_response', _iec.StructType(ReadServerLogRecvData)), Value=0, DataLen=205)

        # copy parsed header to response
        self._response.ParSeq = self._rspHeader.ParSeq
        self._response.State = self._rspHeader.State
        self._response.AlarmMessageSeverity = self._rspHeader.AlarmMessageSeverity
        self._response.AlarmMessageCode = self._rspHeader.AlarmMessageCode

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.AvailableLogLines
            self._response.AvailableLogLines = ResponseData.GetUdint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.AvailableFilteredLogLines
            self._response.AvailableFilteredLogLines = ResponseData.GetUdint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LogContentLength
            self._response.LogContentLength = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.IsStartOfLine / IsEndOfLine / EndOfLogReached
            _flags = ResponseData.GetByte()
            self._response.IsStartOfLine = bit(_flags, 0)
            self._response.IsEndOfLine = bit(_flags, 1)
            self._response.EndOfLogReached = bit(_flags, 2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LogLine
            self._response.LogLine = ResponseData.GetUdint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Offset
            self._response.Offset = ResponseData.GetUdint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining and self._response.LogContentLength > 0:
            # Get Response.LogContent (LogContentLength characters)
            self._response.LogContent = trunc_str(ResponseData.GetString(Size=MIN(USINT_TO_DINT(self._response.LogContentLength), RobotLibraryConstants.SERVER_LOG_CONTENT_MAX)), 179)
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
        # Create log entry for AvailableLogLines
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.AvailableLogLines = {1}', Para1=UDINT_TO_STRING(self._response.AvailableLogLines))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AvailableFilteredLogLines
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.AvailableFilteredLogLines = {1}', Para1=UDINT_TO_STRING(self._response.AvailableFilteredLogLines))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LogContentLength
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LogContentLength = {1}', Para1=USINT_TO_STRING(self._response.LogContentLength))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for IsStartOfLine
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.IsStartOfLine = {1}', Para1=BOOL_TO_STRING(self._response.IsStartOfLine))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LogLine
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LogLine = {1}', Para1=UDINT_TO_STRING(self._response.LogLine))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Offset = {1}', Para1=UDINT_TO_STRING(self._response.Offset))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LogContent
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LogContent = {1}', Para1=self._response.LogContent)

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False
        self._restart = False
        self._contentReceived = False
        self._offsetHandled = False
        self._command.Enable = False
        return Reset

    def StoreLogContent(self, *, AxesGroup: _T.AxesGroup, LogFile: list[str]) -> None:  # PRIVATE
        # LogFile is full
        Full: bool = False

        if not self._contentReceived:
            return
        self._contentReceived = False

        self.OutCmd.AvailableLogLines = self._response.AvailableLogLines
        self.OutCmd.AvailableFilteredLogLines = self._response.AvailableFilteredLogLines

        # a part of a log line ? (a response without log line: the RC had not read the log yet)
        if self._response.LogLine > 0 and (self._response.LogContentLength > 0 or self._response.IsEndOfLine):
            # a new line starts in the next element of LogFile
            if self._response.IsStartOfLine or not self._lineOpen:
                self._line = LOWER_BOUND(LogFile) + self._lines
                self._lines = self._lines + 1
                SysDepMemSet(pDest=ADR_ELEM(LogFile, self._line, _iec.StringType(1023)), Value=0, DataLen=1024)
                self._lineLen = 0
                self._lineOpen = True

            # append the part (a line longer than LOG_LINE_LEN is cut)
            self._copyLen = MIN(USINT_TO_DINT(self._response.LogContentLength), RobotLibraryParameter.LOG_LINE_LEN - self._lineLen)
            if self._copyLen > 0:
                SysDepMemCpy(pDest=ADR_ELEM(LogFile, self._line, _iec.StringType(1023)) + self._lineLen, pSrc=ADR(self._response, 'LogContent', _iec.StringType(179)), DataLen=DINT_TO_UDINT(self._copyLen))
                self._lineLen = self._lineLen + self._copyLen
            elif self._response.LogContentLength > 0:
                self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.WARNING, MessageCode=0, MessageText='Log line {1} longer than LOG_LINE_LEN, cut', Para1=UDINT_TO_STRING(self._response.LogLine))

            if self._response.IsEndOfLine:
                self._lineOpen = False
                self.OutCmd.ReceivedLogLines = wrap(self.OutCmd.ReceivedLogLines + 1, 'UDINT')
                self.OutCmd.LogLine = self._response.LogLine
                if self._response.AvailableFilteredLogLines > 0:
                    self.OutCmd.Progress = MIN(100.0, UDINT_TO_REAL(self.OutCmd.ReceivedLogLines) * 100.0 / UDINT_TO_REAL(self._response.AvailableFilteredLogLines))

        self.OutCmd.EndOfLogReached = self._response.EndOfLogReached
        # no element of LogFile left for another line
        Full = (not self._lineOpen) & (LOWER_BOUND(LogFile) + self._lines > UPPER_BOUND(LogFile))

        if self._response.EndOfLogReached or Full:
            # end of the transfer: Enable FALSE, the RC answers with DONE
            self._command.Enable = False
        else:
            # next part of the log
            self._command.Offset = wrap(self._command.Offset + 1, 'UDINT')
            self._offsetHandled = False
        self._parameterUpdateInternal = True
