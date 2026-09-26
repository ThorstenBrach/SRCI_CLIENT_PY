"""Read DH (Denavit–Hartenberg) parameters of robot

ST-Source: POUs/Read/MC_ReadDHParameter/MC_ReadDHParameterFB.st
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
from srci.iec.conv import BOOL_TO_STRING, DINT_TO_STRING, REAL_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, st_for_end, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, ReadDHParameterOutCmd, ReadDHParameterParCmd, ReadDHParameterRecvData, ReadDHParameterSendData, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ReadDHParameterFB']


class MC_ReadDHParameterFB(RobotLibraryBaseExecuteFB):
    """Read DH (Denavit–Hartenberg) parameters of robot"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: ReadDHParameterParCmd = ReadDHParameterParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # command outputs
        self.OutCmd: ReadDHParameterOutCmd = ReadDHParameterOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ReadDHParameterParCmd = ReadDHParameterParCmd()
        # command data to send
        self._command: ReadDHParameterSendData = ReadDHParameterSendData()
        # response data received
        self._response: ReadDHParameterRecvData = ReadDHParameterRecvData()
        self._directionBits: int = 0

    def __call__(self, *, ParCmd: ReadDHParameterParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 6)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 6)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 6 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 6, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(ReadDHParameterSendData)), DataLen=6)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 6 - PayloadPtr, 6)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 6, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 6, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ReadDHParameter

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 1 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ReadDHParameterParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ReadDHParameterParCmd)), DataLen=1) != RobotLibraryConstants.OK

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
        # internal index for loops
        _idx: int = 0

        CheckParameterValid = True

        # Check ParCmd.ModifiedConvention valid ?
        if self.ParCmd.ModifiedConvention != False and self.ParCmd.ModifiedConvention != True:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ModifiedConvention = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ModifiedConvention))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.ReadDHParameter
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.ModifiedConvention = self._parCmd.ModifiedConvention

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ModifiedConvention
            CreateCommandPayload.AddBool(Value=self._command.ModifiedConvention)
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
        # Create log entry for ModifiedConvention
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ModifiedConvention = {1}', Para1=BOOL_TO_STRING(self._command.ModifiedConvention))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ReadDHParameterFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadDHParameterOutCmd)), Value=0, DataLen=147)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            copy_into(self.OutCmd.DHParameter, self._response.DHParameter)

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadDHParameterOutCmd)), Value=0, DataLen=147)
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

    def ParseResponsePayload(self, *, ResponseData: RobotLibraryResponseDataFB | None = None, Timestamp: SystemTime | None = None) -> int:  # INTERNAL
        if ResponseData is None:
            ResponseData = RobotLibraryResponseDataFB()
        else:
            ResponseData = copy_value(ResponseData)  # VAR_INPUT is a copy in ST
        if Timestamp is None:
            Timestamp = SystemTime()
        ParseResponsePayload: int = 0
        # internal index for loops
        _idx: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # call base implementation to parse the header from payload buffer
        ResponseData.PayloadPtr = super().ParseResponsePayload(ResponseData=ResponseData, Timestamp=Timestamp)

        # copy parsed header to response
        self._response.ParSeq = self._rspHeader.ParSeq
        self._response.State = self._rspHeader.State
        self._response.AlarmMessageSeverity = self._rspHeader.AlarmMessageSeverity
        self._response.AlarmMessageCode = self._rspHeader.AlarmMessageCode

        for _idx in range(0, 7):
            # Check payload remaining ?
            if ResponseData.IsPayloadRemaining:
                # Get Response.DHParameter.Alpha
                self._response.DHParameter.Alpha[_idx] = ResponseData.GetReal()
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 6)

        for _idx in range(0, 7):
            # Check payload remaining ?
            if ResponseData.IsPayloadRemaining:
                # Get Response.DHParameter.A
                self._response.DHParameter.A[_idx] = ResponseData.GetReal()
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 6)

        for _idx in range(0, 7):
            # Check payload remaining ?
            if ResponseData.IsPayloadRemaining:
                # Get Response.DHParameter.D
                self._response.DHParameter.D[_idx] = ResponseData.GetReal()
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 6)

        for _idx in range(0, 7):
            # Check payload remaining ?
            if ResponseData.IsPayloadRemaining:
                # Get Response.DHParameter.Theta
                self._response.DHParameter.Theta[_idx] = ResponseData.GetReal()
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 6)

        for _idx in range(0, 7):
            # Check payload remaining ?
            if ResponseData.IsPayloadRemaining:
                # Get Response.DHParameter.JointZeroPosition
                self._response.DHParameter.JointZeroPosition[_idx] = ResponseData.GetReal()
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 6)

        # ST-FIX F33: PositiveJointDirection[0..6] are the bits 0..6 of one byte (spec table)
        if ResponseData.IsPayloadRemaining:
            self._directionBits = ResponseData.GetByte()
            for _idx in range(0, 7):
                self._response.DHParameter.PositiveJointDirection[_idx] = self._directionBits >> _idx & 1 == 1
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

        # Create log entry for DHParameter.Alpha[{x}]
        for _idx in range(0, 7):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # create log entry for Response.DHParameter.Aplpha
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DHParameter.Alpha[{2}] = {1}', Para1=REAL_TO_STRING(self._response.DHParameter.Alpha[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 6)

        # Create log entry for DHParameter.A[{x}]
        for _idx in range(0, 7):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # create log entry for Response.DHParameter.A
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DHParameter.A[{2}] = {1}', Para1=REAL_TO_STRING(self._response.DHParameter.A[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 6)

        # Create log entry for DHParameter.D[{x}]
        for _idx in range(0, 7):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # create log entry for Response.DHParameter.D
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DHParameter.D[{2}] = {1}', Para1=REAL_TO_STRING(self._response.DHParameter.D[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 6)

        # Create log entry for DHParameter.Theta[{x}]
        for _idx in range(0, 7):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # create log entry for Response.DHParameter.Theta
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DHParameter.Theta[{2}] = {1}', Para1=REAL_TO_STRING(self._response.DHParameter.Theta[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 6)

        # Create log entry for DHParameter.JointZeroPosition[{x}]
        for _idx in range(0, 7):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # create log entry for Response.DHParameter.JointZeroPosition
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DHParameter.JointZeroPosition[{2}] = {1}', Para1=REAL_TO_STRING(self._response.DHParameter.JointZeroPosition[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 6)

        # Create log entry for DHParameter.PositiveJointDirection[{x}]
        for _idx in range(0, 7):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # create log entry for Response.DHParameter.PositiveJointDircetion
            self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DHParameter.PositiveJointDirection[{2}] = {1}', Para1=BOOL_TO_STRING(self._response.DHParameter.PositiveJointDirection[_idx]), Para2=DINT_TO_STRING(_idx))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False
        return Reset
