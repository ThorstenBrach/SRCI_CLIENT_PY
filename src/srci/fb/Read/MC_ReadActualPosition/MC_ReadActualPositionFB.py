"""Read the actual position – TCP: X…RZ + config/Turn, … Joint: (J1…E6)

ST-Source: POUs/Read/MC_ReadActualPosition/MC_ReadActualPositionFB.st
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
from srci.functions.Convert.TO_STRING.PROCESSING_MODE_TO_STRING import PROCESSING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.SEQUENCE_FLAG_TO_STRING import SEQUENCE_FLAG_TO_STRING
from srci.iec.conv import BYTE_TO_STRING, DINT_TO_STRING, INT_TO_STRING, INT_TO_USINT, REAL_TO_STRING, SINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, ProcessingMode, ProcessingModeEnum, ReadActualPositionOutCmd, ReadActualPositionParCmd, ReadActualPositionRecvData, ReadActualPositionSendData, RobotLibraryConstants, RobotLibraryErrorIdEnum, SequenceFlag, SequenceFlagEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ReadActualPositionFB']


class MC_ReadActualPositionFB(RobotLibraryBaseExecuteFB):
    """Read the actual position – TCP: X…RZ + config/Turn, … Joint: (J1…E6)"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Processing mode - For more information see chapter 5.6.4.5.
        self.ProcessingMode: ProcessingMode = ProcessingMode.BUFFERED
        # Defines the target sequence in which the command will be executed
        self.SequenceFlag: SequenceFlag = SequenceFlag.NO_SEQUENCE
        # command parameter
        self.ParCmd: ReadActualPositionParCmd = ReadActualPositionParCmd()
        # VAR_OUTPUT
        # TRUE, while the following outputs return valid values
        # • ActualCartesianPosition
        # • ToolNoReturn
        # • FrameNoReturn
        # • ActualJointPosition
        self.Valid: bool = False
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # The command was aborted by another command.
        self.CommandAborted: bool = False
        # TRUE, while command is interrupted during execution and can be continued.
        self.CommandInterrupted: bool = False
        # Receiving of input parameter values has been acknowledged by RC
        self.ParameterAccepted: bool = False
        # command outputs
        self.OutCmd: ReadActualPositionOutCmd = ReadActualPositionOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ReadActualPositionParCmd = ReadActualPositionParCmd()
        # command data to send
        self._command: ReadActualPositionSendData = ReadActualPositionSendData()
        # response data received
        self._response: ReadActualPositionRecvData = ReadActualPositionRecvData()

    def __call__(self, *, ProcessingMode: ProcessingMode | None = None, SequenceFlag: SequenceFlag | None = None, ParCmd: ReadActualPositionParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ProcessingMode is not None:
            self.ProcessingMode = ProcessingMode(ProcessingMode)
        if SequenceFlag is not None:
            self.SequenceFlag = SequenceFlag(SequenceFlag)
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 13)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 13)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 13 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 13, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(ReadActualPositionSendData)), DataLen=13)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 13 - PayloadPtr, 13)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 13, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 13, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ReadActualPosition

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 5 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ReadActualPositionParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ReadActualPositionParCmd)), DataLen=5) != RobotLibraryConstants.OK

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
            # Reset parameter accepted flag
            self.ParameterAccepted = False
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
        if ((((((self.ProcessingMode != ProcessingMode.BUFFERED and self.ProcessingMode != ProcessingMode.ABORTING) and self.ProcessingMode != ProcessingMode.PARALLEL) and self.ProcessingMode != ProcessingMode.CONTINUOUS) and self.ProcessingMode != ProcessingMode.DEACTIVATE) and self.ProcessingMode != ProcessingMode.TRIGGER_ONCE) and self.ProcessingMode != ProcessingMode.TRIGGER_CONTINUOUS) and self.ProcessingMode != ProcessingMode.TRIGGER_MULTIPLE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check SequenceFlag valid ?
        if (self.SequenceFlag != SequenceFlag.NO_SEQUENCE and self.SequenceFlag != SequenceFlag.PRIMARY_SEQUENCE) and self.SequenceFlag != SequenceFlag.SECONDARY_SEQUENCE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter SequenceFlag = {1}', Para1=SEQUENCE_FLAG_TO_STRING(Value=self.SequenceFlag))
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

        # Check ParCmd.ListenerID valid ?
        if self.ParCmd.ListenerID < 0 or self.ParCmd.ListenerID > 127:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ListenerID = {1}', Para1=SINT_TO_STRING(self.ParCmd.ListenerID))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # internal index for loops
        _idx: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.ReadActualPosition
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.EmitterID[0] = 0
        self._command.EmitterID[1] = 0
        self._command.EmitterID[2] = 0
        self._command.EmitterID[3] = 0
        self._command.Reserve = 0
        self._command.ListenerID = self._parCmd.ListenerID
        self._command.ToolNo = INT_TO_USINT(self._parCmd.ToolNo)
        self._command.FrameNo = INT_TO_USINT(self._parCmd.FrameNo)

        if self._parCmd.ToolNo == -1:
            self._command.ToolNo = 255  # -1 is mapped to 255, see specification

        if self._parCmd.FrameNo == -1:
            self._command.FrameNo = 255  # -1 is mapped to 255, see specification

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
            # add command.Reserve
            CreateCommandPayload.AddByte(Value=self._command.Reserve)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Index[0]
            CreateCommandPayload.AddUsint(Value=self._command.ToolNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Index[1]
            CreateCommandPayload.AddUsint(Value=self._command.FrameNo)
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
        # Create log entry for ListenerID
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ListenerID = {1}', Para1=SINT_TO_STRING(self._command.ListenerID))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve = {1}', Para1=BYTE_TO_STRING(self._command.Reserve))

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

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ReadActualPositionFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        self.ProcessingMode = ProcessingMode.PARALLEL
        self.SequenceFlag = SequenceFlag.NO_SEQUENCE
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadActualPositionOutCmd)), Value=0, DataLen=116)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.OriginID = self._response.OriginID
            self.OutCmd.InvocationCounter = self._response.InvocationCounter
            self.OutCmd.ToolNoReturn = self._response.ToolNoReturn
            self.OutCmd.FrameNoReturn = self._response.FrameNoReturn
            copy_into(self.OutCmd.ActualCartesianPosition, self._response.ActualCartesianPosition)
            copy_into(self.OutCmd.ActualJointPosition, self._response.ActualJointPosition)

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadActualPositionOutCmd)), Value=0, DataLen=116)
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
                    # Apply Command Outputs
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

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolNoReturn
            self._response.ToolNoReturn = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.FrameNoReturn
            self._response.FrameNoReturn = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.X
            self._response.ActualCartesianPosition.X = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.Y
            self._response.ActualCartesianPosition.Y = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.Z
            self._response.ActualCartesianPosition.Z = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.Rx
            self._response.ActualCartesianPosition.Rx = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.Ry
            self._response.ActualCartesianPosition.Ry = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.Rz
            self._response.ActualCartesianPosition.Rz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.Config
            copy_into(self._response.ActualCartesianPosition.Config, ResponseData.GetArmConfig())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.TurnNumber
            copy_into(self._response.ActualCartesianPosition.TurnNumber, ResponseData.GetTurnNumbers())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.E1
            self._response.ActualCartesianPosition.E1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.J1
            self._response.ActualJointPosition.J1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.J2
            self._response.ActualJointPosition.J2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.J3
            self._response.ActualJointPosition.J3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.J4
            self._response.ActualJointPosition.J4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.J5
            self._response.ActualJointPosition.J5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.J6
            self._response.ActualJointPosition.J6 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.E2
            self._response.ActualCartesianPosition.E2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.E3
            self._response.ActualCartesianPosition.E3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.E4
            self._response.ActualCartesianPosition.E4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.E5
            self._response.ActualCartesianPosition.E5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualCartesianPosition.E6
            self._response.ActualCartesianPosition.E6 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.E1
            self._response.ActualJointPosition.E1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.E2
            self._response.ActualJointPosition.E2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.E3
            self._response.ActualJointPosition.E3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.E4
            self._response.ActualJointPosition.E4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.E5
            self._response.ActualJointPosition.E5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ActualJointPosition.E6
            self._response.ActualJointPosition.E6 = ResponseData.GetReal()
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

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolNoReturn
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolNoReturn = {1}', Para1=INT_TO_STRING(self._response.ToolNoReturn))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for FrameNoReturn
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.FrameNoReturn = {1}', Para1=INT_TO_STRING(self._response.FrameNoReturn))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.X
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.X = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.Y
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.Y = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.Z
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.Z = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.Rx
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.Rx = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.Ry
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.Ry = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.Rz
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.Rz = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.Config
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.Config = {1}', Para1=ARM_CONFIG_TO_STRING(Value=self._response.ActualCartesianPosition.Config))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.TurnNumber.J1Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.TurnNumber.J1Turns = {1}', Para1=SINT_TO_STRING(self._response.ActualCartesianPosition.TurnNumber.J1Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.TurnNumber.J2Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.TurnNumber.J2Turns = {1}', Para1=SINT_TO_STRING(self._response.ActualCartesianPosition.TurnNumber.J2Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.TurnNumber.J3Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.TurnNumber.J3Turns = {1}', Para1=SINT_TO_STRING(self._response.ActualCartesianPosition.TurnNumber.J3Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.TurnNumber.J4Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.TurnNumber.J4Turns = {1}', Para1=SINT_TO_STRING(self._response.ActualCartesianPosition.TurnNumber.J4Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.TurnNumber.J5Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.TurnNumber.J5Turns = {1}', Para1=SINT_TO_STRING(self._response.ActualCartesianPosition.TurnNumber.J5Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.TurnNumber.J6Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.TurnNumber.J6Turns = {1}', Para1=SINT_TO_STRING(self._response.ActualCartesianPosition.TurnNumber.J6Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.TurnNumber.E1Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.TurnNumber.E1Turns = {1}', Para1=SINT_TO_STRING(self._response.ActualCartesianPosition.TurnNumber.E1Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.E1
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.E1 = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.J1
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.J1 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.J1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.J2
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.J2 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.J2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.J3
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.J3 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.J3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.J4
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.J4 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.J4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.J5
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.J5 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.J5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.J6
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.J6 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.J6))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.E1
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.E1 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.E2
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.E2 = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.E3
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.E3 = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.E4
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.E4 = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.E5
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.E5 = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualCartesianPosition.E6
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualCartesianPosition.E6 = {1}', Para1=REAL_TO_STRING(self._response.ActualCartesianPosition.E6))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.E2
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.E2 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.E3
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.E3 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.E4
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.E4 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.E5
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.E5 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActualJointPosition.E6
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ActualJointPosition.E6 = {1}', Para1=REAL_TO_STRING(self._response.ActualJointPosition.E6))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.Valid = False
        self.ParameterAccepted = False
        self.CommandBuffered = False
        self.CommandAborted = False
        self.CommandInterrupted = False
        return Reset
