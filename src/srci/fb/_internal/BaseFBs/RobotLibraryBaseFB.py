"""RobotLibraryBaseFB

ST-Source: POUs/_internal/BaseFBs/RobotLibraryBaseFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import srci.types as _T
from srci.fb._internal.BaseFBs.RobotLibraryLogFB import RobotLibraryLogFB
from srci.fb._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from srci.fb._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from srci.functions.Common import CheckTimeout
from srci.functions.Convert.TO_STRING.MESSAGE_CODE_TO_STRING import MESSAGE_CODE_TO_STRING
from srci.functions.Convert.TO_STRING.WORD_TO_STRING_HEX import WORD_TO_STRING_HEX
from srci.iec.rt import CONCAT, copy_into, copy_value, trunc_str
from srci.iec.standard import R_TRIG, TON
from srci.types import AxesGroupAcyclicAcrEntryRspBuffer, CmdHeader, CmdMessageState, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, RobotLibraryInfoIdEnum, RobotLibraryWarningIdEnum, RspHeader, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['RobotLibraryBaseFB']


class RobotLibraryBaseFB(RobotLibraryLogFB):

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # User defined command name
        self.Name: str = ''
        # Execution Mode
        self.ExecMode: ExecutionMode = ExecutionMode.SEQUENCE_PRIMARY
        # Priority
        self.Priority: PriorityLevel = PriorityLevel.VERY_HIGH
        # VAR_OUTPUT
        # Command data
        self.CommandData: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # response data
        self.ResponseData: RobotLibraryResponseDataFB = RobotLibraryResponseDataFB()
        # An error occurred during the execution of the command
        self.Error: bool = False
        # ErrorID reported by RC for error identification according to Table 7-1
        self.ErrorID: int = 0
        self.ErrorIdEnum: RobotLibraryErrorIdEnum = RobotLibraryErrorIdEnum.NO_ERROR
        self.ErrorAddTxt: str = ''
        # WarningID for warning identification reported during execution of command according to Table 7-3
        self.WarningID: int = 0
        self.WarningIdEnum: RobotLibraryWarningIdEnum = RobotLibraryWarningIdEnum.NO_WARNING
        # InfoID for info identification reported during execution of command according to Table 7-5
        self.InfoID: int = 0
        self.InfoIdEnum: RobotLibraryInfoIdEnum = RobotLibraryInfoIdEnum.NO_INFO
        # VAR_IN_OUT
        # Robot assignment of function
        self.AxesGroup: AxesGroup = None
        # VAR
        # Rising edge for error
        # {attribute 'hide'}
        self._error_R: R_TRIG = R_TRIG()
        # Rising edge for warning
        # {attribute 'hide'}
        self._warning_R: R_TRIG = R_TRIG()
        # Rising edge for information
        # {attribute 'hide'}
        self._info_R: R_TRIG = R_TRIG()
        # clear error active
        self._clearError: bool = False
        # cancel active
        self._cancel: bool = False
        # unique ID
        self._uniqueID: int = 0
        # flag for response received
        self._responseReceived: bool = False
        # internal step counter
        self._stepCmd: int = 0
        # internal timer
        # {attribute 'hide'}
        self._timerCmd: TON = TON()
        # internal timeout
        # {attribute 'hide'}
        self._timeoutCmd: int = 5000
        # internal step counter for ClearError
        self._stepClearError: int = 0
        # internal timer for ClearError
        # {attribute 'hide'}
        self._timerClearError: TON = TON()
        # internal timeout for ClearError
        # {attribute 'hide'}
        self._timeoutClearError: int = 5000
        # internal step counter for Cancel
        self._stepCancel: int = 0
        # internal timer for Cancel
        # {attribute 'hide'}
        self._timerCancel: TON = TON()
        # internal timeout for Cancel
        # {attribute 'hide'}
        self._timeoutCancel: int = 5000
        # internal command header
        self._cmdHeader: CmdHeader = CmdHeader()
        # internal response header
        self._rspHeader: RspHeader = RspHeader()
        # internal flag for send a parameter update
        self._parameterUpdateInternal: bool = False
        # internal flag for parameter has changed
        self._parameterChanged: bool = False
        # internal flag for parameter are valid
        self._parameterValid: bool = False

    def __call__(self, *, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        self.OnCall(AxesGroup=self.AxesGroup)
        self.OnExecRun(AxesGroup=self.AxesGroup)
        # ST-FIX F53: no response of the RC within _timeoutCmd after the command was added
        # -> error (before: _timerCmd was started but never evaluated, the FB stayed Busy)
        if (self._uniqueID != 0 and self._rspHeader.State == CmdMessageState.EMPTY) and (not self.Error):
            if CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK:
                self.AxesGroup.Acyclic.ActiveCommandRegister.RemoveCmd(UniqueID=self._uniqueID)
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=True)
                self.OnUpdateStateFlags(State=CmdMessageState.ERROR)
        self.CheckParameterChanged(AxesGroup=self.AxesGroup)

        if self.AxesGroup.State.OnlineChange_R.Q:
            self.OnOnlineChange(AxesGroup=self.AxesGroup)

    def CallBack(self, *, RspData: AxesGroupAcyclicAcrEntryRspBuffer | None = None, Timestamp: SystemTime | None = None) -> int:  # PUBLIC
        if RspData is None:
            RspData = AxesGroupAcyclicAcrEntryRspBuffer()
        if Timestamp is None:
            Timestamp = SystemTime()
        CallBack: int = 0

        # Create log entry
        self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Callback reveiced in FB {1} <{2}>', Para1=self.MyType, Para2=self.Name)

        self.ResponseData.Reset()
        copy_into(self.ResponseData.Payload, RspData.Payload)
        self.ResponseData.PayloadLen = RspData.PayloadLen
        self.ParseResponsePayload(ResponseData=self.ResponseData, Timestamp=Timestamp)

        # set flag for response received
        self._responseReceived = True
        return CallBack

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        self.Error = True
        self.ErrorID = RobotLibraryErrorIdEnum.ERR_FUNCTION_NOT_SUPPORTED
        self.ErrorAddTxt = trunc_str(CONCAT(self._myType, ' '), 40)
        self.ErrorAddTxt = trunc_str(CONCAT(self.ErrorAddTxt, self.Name), 40)

        # Create log entry
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Execution canceled, because function <{1}> is not supported by the robot controller', Para1=self._myType)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        if CheckParameterChanged:
            AxesGroup.Acyclic.ActiveCommandRegister.NotifyParameterChanged = self._uniqueID
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False

        CheckParameterValid = True
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()

        # Reset all variables
        CreateCommandPayload.Reset()
        # Add CmdType
        CreateCommandPayload.AddUint(Value=self._cmdHeader.CmdTyp)
        # Add Reserve_ExecMode
        CreateCommandPayload.AddHalfBytes(HalfByteHi=0, HalfByteLo=self._cmdHeader.ExecMode)
        # Add ParSeq_Priority
        CreateCommandPayload.AddHalfBytes(HalfByteHi=self._cmdHeader.ParSeq, HalfByteLo=self._cmdHeader.Priority)
        return CreateCommandPayload

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        pass

    def OnCall(self, *, AxesGroup: _T.AxesGroup) -> None:  # PROTECTED
        # map numeric value to enum, so that the corresponding message text is directly shown by the tooltip
        self.ErrorIdEnum = RobotLibraryErrorIdEnum(self.ErrorID)
        self.WarningIdEnum = RobotLibraryWarningIdEnum(self.WarningID)
        self.InfoIdEnum = RobotLibraryInfoIdEnum(self.InfoID)

        self.Error = self.ErrorID != RobotLibraryConstants.OK

        self.InternalLogger = AxesGroup.MessageLog
        self.ExternalLogger = AxesGroup.MessageLog.ExternalLogger
        self.LogLevel = AxesGroup.MessageLog.LogLevel

        # building rising edges for error, warning, info number detected
        self._error_R(CLK=self.ErrorID != RobotLibraryConstants.OK)
        self._warning_R(CLK=self.WarningID != RobotLibraryConstants.OK)
        self._info_R(CLK=self.InfoID != RobotLibraryConstants.OK)

        # Log Command events to message log
        if self.LogLevel < self._rspHeader.AlarmMessageSeverity and ((self._error_R.Q or self._warning_R.Q) or self._info_R.Q):
            # Add command message to message buffer
            AxesGroup.MessageLog.AddMessageLogByParameter(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, MessageCode=self._rspHeader.AlarmMessageCode, MessageText=CONCAT(self.MyType, CONCAT(' : ', MESSAGE_CODE_TO_STRING(MessageCode=self._rspHeader.AlarmMessageCode))), Severity=self._rspHeader.AlarmMessageSeverity)

        if self._error_R.Q:
            # Create log entry
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Error with ID: 16#{1} in FB {2} received ', Para1=WORD_TO_STRING_HEX(Value=self.ErrorID), Para2=self.MyType)

        if self._warning_R.Q:
            # Create log entry
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Warning with ID: 16#{1} in FB {2} received ', Para1=WORD_TO_STRING_HEX(Value=self.WarningID), Para2=self.MyType)

        if self._info_R.Q:
            # Create log entry
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Info with ID: 16#{1} in FB {2} received ', Para1=WORD_TO_STRING_HEX(Value=self.InfoID), Para2=self.MyType)

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecRun: int = 0
        pass
        return OnExecRun

    def OnOnlineChange(self, *, AxesGroup: _T.AxesGroup) -> int:
        OnOnlineChange: int = 0

        # update pointer to command FB
        AxesGroup.Acyclic.ActiveCommandRegister.OnOnlineChange(UniqueID=self._uniqueID, pCommandFB=self)
        return OnOnlineChange

    def OnUpdateStateFlags(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        pass

    def ParseResponsePayload(self, *, ResponseData: RobotLibraryResponseDataFB | None = None, Timestamp: SystemTime | None = None) -> int:  # INTERNAL
        if ResponseData is None:
            ResponseData = RobotLibraryResponseDataFB()
        else:
            ResponseData = copy_value(ResponseData)  # VAR_INPUT is a copy in ST
        if Timestamp is None:
            Timestamp = SystemTime()
        ParseResponsePayload: int = 0

        # reset message IDs
        self.InfoID = 0
        self.WarningID = 0
        self.ErrorID = 0

        # get State
        self._rspHeader.State = CmdMessageState(ResponseData.GetHalfeByte1(IncPayloadPtr=False))
        # get ParSeq
        self._rspHeader.ParSeq = ResponseData.GetHalfeByte2(IncPayloadPtr=True)
        # get AlarmMessageSeverity
        self._rspHeader.AlarmMessageSeverity = Severity(ResponseData.GetSint())
        # get AlarmMessageCode
        self._rspHeader.AlarmMessageCode = ResponseData.GetUint()

        # Update InfoID / WarningID / ErrorID
        match self._rspHeader.AlarmMessageSeverity:

            # Informative message
            case Severity.INFO:
                self.SetInfo(InfoID=self._rspHeader.AlarmMessageCode, Overwrite=True)
            # Warning message
            case Severity.WARNING:
                self.SetWarning(WarningID=self._rspHeader.AlarmMessageCode, Overwrite=True)
            # Error message
            case Severity.ERROR:
                self.SetError(ErrorID=self._rspHeader.AlarmMessageCode, Overwrite=True)
            # Fataö error message
            case Severity.FATAL_ERROR:
                self.SetError(ErrorID=self._rspHeader.AlarmMessageCode, Overwrite=True)

        ParseResponsePayload = ResponseData.PayloadPtr
        return ParseResponsePayload

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        self._parameterUpdateInternal = False
        self._responseReceived = False

        self._uniqueID = 0
        self._rspHeader.State = CmdMessageState.EMPTY  # ST-FIX F53: no response yet
        self._stepCmd = 0
        self.Error = False
        self.ErrorID = 0
        self.WarningID = 0
        self.InfoID = 0

        Reset = RobotLibraryConstants.OK
        return Reset

    def SetError(self, *, ErrorID: int = 0, Overwrite: bool = False) -> None:  # PUBLIC
        if not self.HasError or Overwrite:
            self.ErrorID = ErrorID

    def SetInfo(self, *, InfoID: int = 0, Overwrite: bool = False) -> None:  # PUBLIC
        if not self.HasInfo or Overwrite:
            self.InfoID = InfoID

    def SetWarning(self, *, WarningID: int = 0, Overwrite: bool = False) -> None:  # PUBLIC
        if not self.HasWarning or Overwrite:
            self.WarningID = WarningID

    def _get_HasError(self) -> bool:
        HasError: bool = False

        HasError = self.ErrorID != RobotLibraryErrorIdEnum.NO_ERROR
        return HasError

    HasError = property(_get_HasError, None)  # PUBLIC

    def _get_HasInfo(self) -> bool:
        HasInfo: bool = False

        HasInfo = self.InfoID != RobotLibraryInfoIdEnum.NO_INFO
        return HasInfo

    HasInfo = property(_get_HasInfo, None)  # PUBLIC

    def _get_HasWarning(self) -> bool:
        HasWarning: bool = False

        HasWarning = self.WarningID != RobotLibraryWarningIdEnum.NO_WARNING
        return HasWarning

    HasWarning = property(_get_HasWarning, None)  # PUBLIC
