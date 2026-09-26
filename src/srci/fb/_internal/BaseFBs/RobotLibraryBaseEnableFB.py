"""RobotLibraryBaseEnableFB

ST-Source: POUs/_internal/BaseFBs/RobotLibraryBaseEnableFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import srci.types as _T
from srci.fb._internal.BaseFBs.RobotLibraryBaseFB import RobotLibraryBaseFB
from srci.functions.Common import CheckTimeout, SetTimeout
from srci.iec.rt import trunc_str
from srci.iec.standard import F_TRIG, R_TRIG
from srci.types import CmdMessageState, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['RobotLibraryBaseEnableFB']


class RobotLibraryBaseEnableFB(RobotLibraryBaseFB):

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Set TRUE to activate / Set False to deactivate
        self.Enable: bool = False
        # VAR_OUTPUT
        # FB is being processed
        self.Busy: bool = False
        # TRUE while function is active
        self.Enabled: bool = False
        # VAR
        # Rising edge for enable
        # {attribute 'hide'}
        self._enable_R: R_TRIG = R_TRIG()
        # Falling edge for enable
        # {attribute 'hide'}
        self._enable_F: F_TRIG = F_TRIG()

    def __call__(self, *, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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

    def OnCall(self, *, AxesGroup: _T.AxesGroup) -> None:  # PROTECTED
        # internal return value
        _retVal: int = 0

        super().OnCall(AxesGroup=AxesGroup)

        # building rising and falling edges
        self._enable_R(CLK=self.Enable)
        self._enable_F(CLK=self.Enable)

        # Check command execution is allowed ?
        # is part of init sequence
        # is part of init sequence
        # is part of init sequence
        if ((((self.Enable and (not AxesGroup.State.Initialized)) and (not AxesGroup.State.Synchronized)) and self.MyType != 'MC_ExchangeConfigurationFB') and self.MyType != 'MC_ReadMessagesFB') and self.MyType != 'MC_ReadRobotDataFB':
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_COMMANDS_NOT_ENABLED, Overwrite=True)
            self.Error = True
            self.Busy = False

        # On execution started
        if self._enable_R.Q:
            # ST-FIX F23: a new enable ends a pending cancel / error clear of the previous enable
            self._cancel = False
            self._stepCancel = 0
            self._clearError = False
            self._stepClearError = 0
            self.OnExecStart(AxesGroup=AxesGroup)

        # On execution cancel
        if self.Busy and self._enable_F.Q:
            # set cancel flag
            self._cancel = True

        if self._cancel:
            # call Cancel
            _retVal = self.OnExecCancel(AxesGroup=AxesGroup)

            # done or error ?
            if _retVal != RobotLibraryConstants.RUNNING:
                # reset cancel flag
                self._cancel = False

        # On execution error clear
        if self.Error and self._enable_F.Q:
            # set ClearError flag
            self._clearError = True

        if self._clearError:
            _retVal = self.OnExecErrorClear(AxesGroup=AxesGroup)

            # done or error ?
            if _retVal != RobotLibraryConstants.RUNNING:
                # reset ClearError flag
                self._clearError = False

    def OnExecCancel(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecCancel: int = 0
        # internal return value
        _retVal: int = 0

        OnExecCancel = self.Reset()

        # Create log entry
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Execution of {1} cancled ', Para1=self.MyType)

        # try to remove cmd
        _retVal = AxesGroup.Acyclic.ActiveCommandRegister.RemoveCmd(UniqueID=self._uniqueID)

        if _retVal == RobotLibraryConstants.OK:
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} successfully removed from ACR', Para1=self.MyType)
        else:
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} was not removed from ACR because execution was already in progress', Para1=self.MyType)
        return OnExecCancel

    def OnExecErrorClear(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecErrorClear: int = 0

        OnExecErrorClear = RobotLibraryConstants.RUNNING

        match self._stepClearError:

            case 0:
                self.Reset()
                # trigger parameter update to disable FB
                self._parameterUpdateInternal = True
                # call Check Parameter changed method to trigger the parameter update to deactivate jogging mode
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
            self._stepClearError = 0
        return OnExecErrorClear

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecRun: int = 0
        pass
        return OnExecRun

    def OnExecStart(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecStart: int = 0

        # ST-FIX F71: Priority (1 = very high ... 4 = low, table 7-1)
        if self.Priority < PriorityLevel.VERY_HIGH:
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PRIORITY_TOO_HIGH, Overwrite=True)
            self.Error = True
        elif self.Priority > PriorityLevel.LOW:
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PRIORITY_TOO_LOW, Overwrite=True)
            self.Error = True
        return OnExecStart

    def OnUpdateStateFlags(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        match State:

            # No operation or process is active
            case CmdMessageState.EMPTY:
                pass
            # Created but not yet started
            case CmdMessageState.CREATED:
                pass
            # Buffered and awaiting execution
            case CmdMessageState.BUFFERED:
                pass
            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER:
                pass
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
                self.Busy = False

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Busy = False
        self.Enabled = False
        return Reset
