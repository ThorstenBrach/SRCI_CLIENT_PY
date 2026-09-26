# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_ReadWorkAreaFB
#  Author:      Thorsten Brach
#  Date:        2024-06-01
#
#  Description:
#    Read configuration of defined work areas
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

"""Read configuration of defined work areas

ST-Source: POUs/WorkAreas/MC_ReadWorkArea/MC_ReadWorkAreaFB.st
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
from srci.functions.Convert.TO_STRING.DEFINITION_MODE_TO_STRING import DEFINITION_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_DATE_TO_STRING import IEC_DATE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_TIME_TO_STRING import IEC_TIME_TO_STRING
from srci.functions.Convert.TO_STRING.WORK_AREA_REACTION_MODE_TO_STRING import WORK_AREA_REACTION_MODE_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, BYTE_TO_STRING, DINT_TO_STRING, REAL_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import AreaType, CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, ReadWorkAreaOutCmd, ReadWorkAreaParCmd, ReadWorkAreaRecvData, ReadWorkAreaSendData, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime, WorkAreaReactionMode

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ReadWorkAreaFB']


class MC_ReadWorkAreaFB(RobotLibraryBaseExecuteFB):
    """Read configuration of defined work areas"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: ReadWorkAreaParCmd = ReadWorkAreaParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # command outputs
        self.OutCmd: ReadWorkAreaOutCmd = ReadWorkAreaOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ReadWorkAreaParCmd = ReadWorkAreaParCmd()
        # command data to send
        self._command: ReadWorkAreaSendData = ReadWorkAreaSendData()
        # response data received
        self._response: ReadWorkAreaRecvData = ReadWorkAreaRecvData()
        # VAR_INPUT
        self.UpdateSystemData: bool = True  #  ST-FIX F16: FALSE for the internal instances of MC_RobotTaskFB (synchronisation)

    def __call__(self, *, ParCmd: ReadWorkAreaParCmd | None = None, UpdateSystemData: bool | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ParCmd is not None:
            copy_into(self.ParCmd, ParCmd)
        if UpdateSystemData is not None:
            self.UpdateSystemData = UpdateSystemData
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
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 6, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(ReadWorkAreaSendData)), DataLen=6)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 6 - PayloadPtr, 6)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 6, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 6, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ReadWorkArea

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
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ReadWorkAreaParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ReadWorkAreaParCmd)), DataLen=1) != RobotLibraryConstants.OK

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

        # Check ParCmd.WorkAreaNo valid ?
        if ((self.ParCmd.WorkAreaNo < 0 or self.ParCmd.WorkAreaNo > 254) or self.ParCmd.WorkAreaNo > AxesGroup.State.ConfigurationData.HighestWorkAreaIndex) or self.ParCmd.WorkAreaNo > AxesGroup.State.UnifiedWorkAreaIndex:
            # Parameter not valid
            CheckParameterValid = False

            # Check LoadNo available on RC ?
            if self.ParCmd.WorkAreaNo > AxesGroup.State.ConfigurationData.HighestWorkAreaIndex:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_WORKAREANO_UNAVAILABLE, Overwrite=True)
            else:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_WORKAREANO_RANGE, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.WorkAreaNo))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.ReadWorkArea
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.WorkAreaNo = self._parCmd.WorkAreaNo

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaNo
            CreateCommandPayload.AddUsint(Value=self._command.WorkAreaNo)
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
        # Create log entry for WorkAreaNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaNo = {1}', Para1=USINT_TO_STRING(self._command.WorkAreaNo))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ReadWorkAreaFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadWorkAreaOutCmd)), Value=0, DataLen=149)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            copy_into(self.OutCmd.WorkAreaData, self._response.WorkAreaData)
            self.OutCmd.WorkAreaNoReturn = self._response.WorkAreaNoReturn

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ReadWorkAreaOutCmd)), Value=0, DataLen=149)
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
                        # Update the WorAreas in user defined system datas
                        # ST-FIX F16
                        if self.UpdateSystemData and self._response.State == CmdMessageState.DONE:
                            AxesGroup.SystemData.UpdateWorAreas(Caller=self, SystemTime=AxesGroup.State.SystemTime, WorkAreaNo=self.OutCmd.WorkAreaNoReturn, WorkAreaData=self.OutCmd.WorkAreaData)
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
            # Get Response.WorkAreaNoReturn
            self._response.WorkAreaNoReturn = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Reserve
            self._response.Reserve = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.Timestamp.IEC_DATE
            self._response.WorkAreaData.Timestamp.IEC_DATE = ResponseData.GetIecDate()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.Timestamp.IEC_TIME
            self._response.WorkAreaData.Timestamp.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.AreaType
            self._response.WorkAreaData.AreaType = AreaType(ResponseData.GetUsint())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.AreaMode
            self._response.WorkAreaData.AreaMode = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.ReactionMode
            self._response.WorkAreaData.ReactionMode = WorkAreaReactionMode(ResponseData.GetUsint())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.ActiveModification
            self._response.WorkAreaData.ActiveModification = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # ST-FIX F33: WorkAreaData.DefinitionMode removed
        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.FrameNo
            self._response.WorkAreaData.FrameNo = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.ZeroPointX
            self._response.WorkAreaData.ZeroPointX = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.ZeroPointY
            self._response.WorkAreaData.ZeroPointY = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.ZeroPointZ
            self._response.WorkAreaData.ZeroPointZ = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.X.LowerLimit
            self._response.WorkAreaData.X.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.X.UpperLimit
            self._response.WorkAreaData.X.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.Y.LowerLimit
            self._response.WorkAreaData.Y.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.Y.UpperLimit
            self._response.WorkAreaData.Y.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.Z.LowerLimit
            self._response.WorkAreaData.Z.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.Z.UpperLimit
            self._response.WorkAreaData.Z.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.Radiust
            self._response.WorkAreaData.Radius = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J1Limit.LowerLimit
            self._response.WorkAreaData.J1Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J2Limit.LowerLimit
            self._response.WorkAreaData.J2Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J3Limit.LowerLimit
            self._response.WorkAreaData.J3Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J4Limit.LowerLimit
            self._response.WorkAreaData.J4Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J5Limit.LowerLimit
            self._response.WorkAreaData.J5Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J6Limit.LowerLimit
            self._response.WorkAreaData.J6Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E1Limit.LowerLimit
            self._response.WorkAreaData.E1Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J1Limit.UpperLimit
            self._response.WorkAreaData.J1Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J2Limit.UpperLimit
            self._response.WorkAreaData.J2Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J3Limit.UpperLimit
            self._response.WorkAreaData.J3Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J4Limit.UpperLimit
            self._response.WorkAreaData.J4Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J5Limit.UpperLimit
            self._response.WorkAreaData.J5Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.J6Limit.UpperLimit
            self._response.WorkAreaData.J6Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E1Limit.UpperLimit
            self._response.WorkAreaData.E1Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E2Limit.LowerLimit
            self._response.WorkAreaData.E2Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E3Limit.LowerLimit
            self._response.WorkAreaData.E3Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E4Limit.LowerLimit
            self._response.WorkAreaData.E4Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E5Limit.LowerLimit
            self._response.WorkAreaData.E5Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E6Limit.LowerLimit
            self._response.WorkAreaData.E6Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E2Limit.UpperLimit
            self._response.WorkAreaData.E2Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E3Limit.UpperLimit
            self._response.WorkAreaData.E3Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E4Limit.UpperLimit
            self._response.WorkAreaData.E4Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E5Limit.UpperLimit
            self._response.WorkAreaData.E5Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.WorkAreaData.E6Limit.UpperLimit
            self._response.WorkAreaData.E6Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.DataChanged
            self._response.DataChanged = ResponseData.GetBool()
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
        # Create log entry for WorkAreaNoReturn
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaNoReturn = {1}', Para1=USINT_TO_STRING(self._response.WorkAreaNoReturn))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Reserve = {1}', Para1=BYTE_TO_STRING(self._response.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Timestamp.IEC_DATE
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.Timestamp.IEC_DATE = {1}', Para1=IEC_DATE_TO_STRING(Value=self._response.WorkAreaData.Timestamp.IEC_DATE))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Timestamp.IEC_TIME
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.Timestamp.IEC_TIME = {1}', Para1=IEC_TIME_TO_STRING(Value=self._response.WorkAreaData.Timestamp.IEC_TIME))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.AreaType
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.AreaType = {1}', Para1=USINT_TO_STRING(self._response.WorkAreaData.AreaType))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.AreaMode
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.AreaMode = {1}', Para1=BOOL_TO_STRING(self._response.WorkAreaData.AreaMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ReactionMode
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.ReactionMode = {1}', Para1=WORK_AREA_REACTION_MODE_TO_STRING(Value=self._response.WorkAreaData.ReactionMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ActiveModification
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.ActiveModification = {1}', Para1=BOOL_TO_STRING(self._response.WorkAreaData.ActiveModification))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.DefinitionMode
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.DefinitionMode = {1}', Para1=DEFINITION_MODE_TO_STRING(Value=self._response.WorkAreaData.DefinitionMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.FrameNo
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.FrameNo = {1}', Para1=USINT_TO_STRING(self._response.WorkAreaData.FrameNo))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ZeroPointX
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.ZeroPointX = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.ZeroPointX))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ZeroPointY
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.ZeroPointY = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.ZeroPointY))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ZeroPointZ
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.ZeroPointZ = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.ZeroPointZ))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.X.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.X.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.X.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.X.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.X.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.X.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Y.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.Y.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.Y.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Y.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.Y.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.Y.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Z.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.Z.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.Z.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Z.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.Z.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.Z.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Radius
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.Radius = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.Radius))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J1Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J1Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J1Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J2Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J2Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J2Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J3Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J3Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J3Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J4Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J4Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J4Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J5Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J5Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J5Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J6Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J6Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J6Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E1Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E1Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E1Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J1Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J1Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J1Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J2Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J2Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J2Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J3Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J3Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J3Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J4Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J4Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J4Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J5Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J5Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J5Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J6Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.J6Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.J6Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E1Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E1Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E1Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E2Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E2Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E2Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E3Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E3Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E3Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E4Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E4Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E4Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E5Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E5Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E5Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E6Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E6Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E6Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E2Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E2Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E2Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E3Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E3Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E3Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E4Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E4Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E4Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E5Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E5Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E5Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E6Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.WorkAreaData.E6Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._response.WorkAreaData.E6Limit.UpperLimit))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False
        return Reset
