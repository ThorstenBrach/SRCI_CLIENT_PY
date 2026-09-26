"""Activate/Deactivate functionality to avoid singularities

ST-Source: POUs/Additional/MC_AvoidSingularity/MC_AvoidSingularityFB.st
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
from srci.functions.Convert.TO_STRING.SINGULARITY_AVOIDANCE_MODE_TO_STRING import SINGULARITY_AVOIDANCE_MODE_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, DINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import AvoidSingularityOutCmd, AvoidSingularityParCmd, AvoidSingularityRecvData, AvoidSingularitySendData, CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SingularityAvoidanceMode, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_AvoidSingularityFB']


class MC_AvoidSingularityFB(RobotLibraryBaseEnableFB):
    """Activate/Deactivate functionality to avoid singularities"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: AvoidSingularityParCmd = AvoidSingularityParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # Receiving of input parameter values has been acknowledged by RC
        self.ParameterAccepted: bool = False
        # command results
        self.OutCmd: AvoidSingularityOutCmd = AvoidSingularityOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: AvoidSingularityParCmd = AvoidSingularityParCmd()
        # command data to send
        self._command: AvoidSingularitySendData = AvoidSingularitySendData()
        # response data received
        self._response: AvoidSingularityRecvData = AvoidSingularityRecvData()

    def __call__(self, *, ParCmd: AvoidSingularityParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 7, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(AvoidSingularitySendData)), DataLen=7)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 7 - PayloadPtr, 7)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 7, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 7, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.AvoidSingularity

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
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(AvoidSingularityParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(AvoidSingularityParCmd)), DataLen=1) != RobotLibraryConstants.OK

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

        # Check ParCmd.Mode valid ?
        if (self.ParCmd.Mode != SingularityAvoidanceMode.NO_CHANGE and self.ParCmd.Mode != SingularityAvoidanceMode.LOCK_J4) and self.ParCmd.Mode != SingularityAvoidanceMode.TOOL_ORIENTATION:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Mode = {1}', Para1=SINGULARITY_AVOIDANCE_MODE_TO_STRING(Value=self.ParCmd.Mode))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.AvoidSingularity
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.Enable = self.Enable
        self._command.Mode = self._parCmd.Mode

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
            # add command.Mode
            CreateCommandPayload.AddByte(Value=self._command.Mode)
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
        # Create log entry for Enable
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Enable = {1}', Para1=BOOL_TO_STRING(self._command.Enable))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Mode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Mode = {1}', Para1=SINGULARITY_AVOIDANCE_MODE_TO_STRING(Value=self._command.Mode))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_AvoidSingularityFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(AvoidSingularityOutCmd)), Value=0, DataLen=0)
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

        # Update enable flag
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

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Enabled
            self._response.Enabled = ResponseData.GetBool()
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

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Busy = False
        self.CommandBuffered = False
        return Reset
