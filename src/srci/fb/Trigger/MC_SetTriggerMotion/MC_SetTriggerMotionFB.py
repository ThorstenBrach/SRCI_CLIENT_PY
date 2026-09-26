"""Trigger an action based on a motion related parameter (e.g. progress of trajectory)

ST-Source: POUs/Trigger/MC_SetTriggerMotion/MC_SetTriggerMotionFB.st
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
from srci.functions.Convert.TO_STRING.PROCESSING_MODE_TO_STRING import PROCESSING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.TRIGGER_CONDITION_TO_STRING import TRIGGER_CONDITION_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import DINT_TO_STRING, INT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, ProcessingMode, ProcessingModeEnum, RobotLibraryConstants, RobotLibraryErrorIdEnum, SetTriggerMotionOutCmd, SetTriggerMotionParCmd, SetTriggerMotionRecvData, SetTriggerMotionSendData, Severity, SystemTime, TriggerCondition

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_SetTriggerMotionFB']


class MC_SetTriggerMotionFB(RobotLibraryBaseExecuteFB):
    """Trigger an action based on a motion related parameter (e.g. progress of trajectory)"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Processing mode
        self.ProcessingMode: ProcessingMode = ProcessingMode.BUFFERED
        # command parameter
        self.ParCmd: SetTriggerMotionParCmd = SetTriggerMotionParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # TRUE, when the monitoring of the input parameter values is active.
        self.MonitoringActive: bool = False
        # command results
        self.OutCmd: SetTriggerMotionOutCmd = SetTriggerMotionOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: SetTriggerMotionParCmd = SetTriggerMotionParCmd()
        # command data to send
        self._command: SetTriggerMotionSendData = SetTriggerMotionSendData()
        # response data received
        self._response: SetTriggerMotionRecvData = SetTriggerMotionRecvData()

    def __call__(self, *, ProcessingMode: ProcessingMode | None = None, ParCmd: SetTriggerMotionParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ProcessingMode is not None:
            self.ProcessingMode = ProcessingMode(ProcessingMode)
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 20)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 20)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 20 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 20, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(SetTriggerMotionSendData)), DataLen=20)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 20 - PayloadPtr, 20)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 20, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 20, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.SetTriggerMotion

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 15 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(SetTriggerMotionParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(SetTriggerMotionParCmd)), DataLen=15) != RobotLibraryConstants.OK

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

        # Check ParCmd.ProcessingMode defined ?
        if self.ProcessingMode < ProcessingMode.BUFFERED and self.ProcessingMode > ProcessingMode.TRIGGER_MULTIPLE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check ProcessingMode valid ?
        if (self.ProcessingMode != ProcessingMode.DEACTIVATE and self.ProcessingMode != ProcessingMode.TRIGGER_ONCE) and self.ProcessingMode != ProcessingMode.TRIGGER_MULTIPLE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check ParCmd.TriggerMode_1 valid ?
        if ((((((((self.ParCmd.TriggerMode_1 != TriggerCondition.TARGET_POSITION_DISTANCE_PERCENT and self.ParCmd.TriggerMode_1 != TriggerCondition.START_POSITION_DISTANCE_PERCENT) and self.ParCmd.TriggerMode_1 != TriggerCondition.TARGET_POSITION_DISTANCE_ABSOLUTE) and self.ParCmd.TriggerMode_1 != TriggerCondition.START_POSITION_DISTANCE_ABSOLUTE) and self.ParCmd.TriggerMode_1 != TriggerCondition.TARGET_POSITION_TCP_VELOCITY_PERCENT) and self.ParCmd.TriggerMode_1 != TriggerCondition.START_POSITION_TCP_VELOCITY_PERCENT) and self.ParCmd.TriggerMode_1 != TriggerCondition.TARGET_POSITION_TCP_VELOCITY_ABSOLUTE) and self.ParCmd.TriggerMode_1 != TriggerCondition.START_POSITION_TCP_VELOCIT_ABSOLUTE) and self.ParCmd.TriggerMode_1 != TriggerCondition.TARGET_POSITION_TIME_MS) and self.ParCmd.TriggerMode_1 != TriggerCondition.START_POSITION_TIME_MS:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TriggerMode_1 = {1}', Para1=TRIGGER_CONDITION_TO_STRING(Value=self.ParCmd.TriggerMode_1))
            return CheckParameterValid

        # Check ParCmd.TriggerParameter_1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.TriggerParameter_1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TriggerParameter_1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.TriggerParameter_1))
            return CheckParameterValid

        # Check ParCmd.TriggerMode_2 valid ?
        if ((((((((self.ParCmd.TriggerMode_2 != TriggerCondition.TARGET_POSITION_DISTANCE_PERCENT and self.ParCmd.TriggerMode_2 != TriggerCondition.START_POSITION_DISTANCE_PERCENT) and self.ParCmd.TriggerMode_2 != TriggerCondition.TARGET_POSITION_DISTANCE_ABSOLUTE) and self.ParCmd.TriggerMode_2 != TriggerCondition.START_POSITION_DISTANCE_ABSOLUTE) and self.ParCmd.TriggerMode_2 != TriggerCondition.TARGET_POSITION_TCP_VELOCITY_PERCENT) and self.ParCmd.TriggerMode_2 != TriggerCondition.START_POSITION_TCP_VELOCITY_PERCENT) and self.ParCmd.TriggerMode_2 != TriggerCondition.TARGET_POSITION_TCP_VELOCITY_ABSOLUTE) and self.ParCmd.TriggerMode_2 != TriggerCondition.START_POSITION_TCP_VELOCIT_ABSOLUTE) and self.ParCmd.TriggerMode_2 != TriggerCondition.TARGET_POSITION_TIME_MS) and self.ParCmd.TriggerMode_2 != TriggerCondition.START_POSITION_TIME_MS:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TriggerMode_2 = {1}', Para1=TRIGGER_CONDITION_TO_STRING(Value=self.ParCmd.TriggerMode_2))
            return CheckParameterValid

        # Check ParCmd.TriggerParameter_2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.TriggerParameter_2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TriggerParameter_2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.TriggerParameter_2))
            return CheckParameterValid

        # Check ParCmd.ListenerID valid ?
        if self.ParCmd.ListenerID < 0 or self.ParCmd.ListenerID > 127:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ListenerID = {1}', Para1=SINT_TO_STRING(self.ParCmd.ListenerID))
            return CheckParameterValid

        for _idx in range(0, 4):
            # Check ParCmd.EmitterID[x] valid ?
            if self.ParCmd.EmitterID[_idx] < -127 or self.ParCmd.EmitterID[_idx] > 127:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EmitterID[{2}] = {1}', Para1=SINT_TO_STRING(self.ParCmd.EmitterID[_idx]), Para2=DINT_TO_STRING(_idx))
                return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # internal index for loops
        _idx: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.SetTriggerMotion
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.EmitterID[0] = self._parCmd.EmitterID[0]
        self._command.EmitterID[1] = self._parCmd.EmitterID[1]
        self._command.EmitterID[2] = self._parCmd.EmitterID[2]
        self._command.EmitterID[3] = self._parCmd.EmitterID[3]
        self._command.ListenerID = self._parCmd.ListenerID
        self._command.TriggerMode_1 = self._parCmd.TriggerMode_1
        self._command.TriggerMode_2 = self._parCmd.TriggerMode_2
        self._command.TriggerParameter_1 = self._parCmd.TriggerParameter_1
        self._command.TriggerParameter_2 = self._parCmd.TriggerParameter_2

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.EmitterID[x]
                CreateCommandPayload.AddSint(Value=self._command.EmitterID[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ListenerID
            CreateCommandPayload.AddSint(Value=self._command.ListenerID)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TriggerMode_1
            CreateCommandPayload.AddSint(Value=self._command.TriggerMode_1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TriggerMode_2
            CreateCommandPayload.AddSint(Value=self._command.TriggerMode_2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TriggerParameter_1
            CreateCommandPayload.AddReal(Value=self._command.TriggerParameter_1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TriggerParameter_2
            CreateCommandPayload.AddReal(Value=self._command.TriggerParameter_2)
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

        # Create log entry for EmitterID[x]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.EmitterID
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EmitterID[{2}] = {1}', Para1=SINT_TO_STRING(self._command.EmitterID[_idx]), Para2=DINT_TO_STRING(_idx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TriggerMode_1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TriggerMode_1 = {1}', Para1=TRIGGER_CONDITION_TO_STRING(Value=TriggerCondition(self._command.TriggerMode_1)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TriggerMode_2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TriggerMode_2 = {1}', Para1=TRIGGER_CONDITION_TO_STRING(Value=TriggerCondition(self._command.TriggerMode_2)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TriggerParameter_1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TriggerParameter_1 = {1}', Para1=REAL_TO_STRING(self._command.TriggerParameter_1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TriggerParameter_2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TriggerParameter_2 = {1}', Para1=REAL_TO_STRING(self._command.TriggerParameter_2))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_SetTriggerMotionFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        self.ProcessingMode = ProcessingMode.TRIGGER_ONCE
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(SetTriggerMotionOutCmd)), Value=0, DataLen=7)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.OriginID = self._response.OriginID
            self.OutCmd.InvocationCounter = self._response.InvocationCounter

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(SetTriggerMotionOutCmd)), Value=0, DataLen=7)
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
        self.MonitoringActive = False

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
                self.MonitoringActive = True
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

        # call base implementation to parse the header from payload buffer
        ResponseData.PayloadPtr = super().ParseResponsePayload(ResponseData=ResponseData, Timestamp=Timestamp)

        # copy parsed header to response
        self._response.ParSeq = self._rspHeader.ParSeq
        self._response.State = self._rspHeader.State
        self._response.AlarmMessageSeverity = self._rspHeader.AlarmMessageSeverity
        self._response.AlarmMessageCode = self._rspHeader.AlarmMessageCode

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.InvocationCounter
            self._response.InvocationCounter = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Reserve
            self._response.Reserve = ResponseData.GetSint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.OriginID
            self._response.OriginID = ResponseData.GetInt()
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
        # Create log entry for InvocationCounter
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.InvocationCounter = {1}', Para1=USINT_TO_STRING(self._response.InvocationCounter))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Reserve = {1}', Para1=SINT_TO_STRING(self._response.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for OriginID
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.OriginID = {1}', Para1=INT_TO_STRING(self._response.OriginID))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.MonitoringActive = False
        self.CommandBuffered = False
        return Reset
