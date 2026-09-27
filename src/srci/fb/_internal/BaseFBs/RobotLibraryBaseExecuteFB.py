# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      RobotLibraryBaseExecuteFB
#  Author:      Thorsten Brach
#  Date:        2024-08-11
#
#  Description:
#
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

"""RobotLibraryBaseExecuteFB

ST-Source: POUs/_internal/BaseFBs/RobotLibraryBaseExecuteFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import srci.types as _T
from srci.fb._internal.BaseFBs.RobotLibraryBaseFB import RobotLibraryBaseFB
from srci.iec.rt import trunc_str
from srci.iec.standard import F_TRIG, R_TRIG
from srci.types import CmdMessageState, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['RobotLibraryBaseExecuteFB']


class RobotLibraryBaseExecuteFB(RobotLibraryBaseFB):

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Start of the command at the rising edge
        self.Execute: bool = False
        # VAR_OUTPUT
        # The command has been completed successfully
        self.Done: bool = False
        # FB is being processed
        self.Busy: bool = False
        # VAR
        # Rising edge for execute
        # {attribute 'hide'}
        self._execute_R: R_TRIG = R_TRIG()
        # Falling edge for execute
        # {attribute 'hide'}
        self._execute_F: F_TRIG = F_TRIG()
        self._executeIn: bool = False
        self._executeHold: bool = False

    def __call__(self, *, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        # ST-FIX F50: a falling edge of Execute must not cancel the command (spec 5.5.x "Output
        # status"): Execute is held internally while Busy; Done/Error/CommandAborted of a command
        # whose Execute is already FALSE are shown for one cycle, then the block resets
        self._executeIn = self.Execute
        self.Execute = self.Execute or self._executeHold
        super().__call__(AxesGroup=self.AxesGroup)
        self._executeHold = self.Busy
        self.Execute = self._executeIn

    def OnCall(self, *, AxesGroup: _T.AxesGroup) -> None:  # PROTECTED
        # internal return value
        _retVal: int = 0

        super().OnCall(AxesGroup=AxesGroup)

        # building rising and falling edges
        self._execute_R(CLK=self.Execute)
        self._execute_F(CLK=self.Execute)

        # Check command execution is allowed ?
        # is part of init sequence
        # is part of init sequence
        # is part of init sequence
        if (((self.Execute and (not AxesGroup.State.CMDsEnabled)) and self.MyType != 'MC_ExchangeConfigurationFB') and self.MyType != 'MC_ReadMessagesFB') and self.MyType != 'MC_ReadRobotDataFB':
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_COMMANDS_NOT_ENABLED, Overwrite=True)
            self.Error = True
            self.Busy = False

        # On execution started
        if self._execute_R.Q:
            self.OnExecStart(AxesGroup=AxesGroup)

        # On execution cancel
        if self.Busy and self._execute_F.Q:
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
        if self.Error and self._execute_F.Q:
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

        OnExecCancel = self.Reset()
        return OnExecCancel

    def OnExecErrorClear(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecErrorClear: int = 0

        OnExecErrorClear = self.Reset()
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
            # Create log entry
            self.CreateLogMessage(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid input Priority: higher than VERY_HIGH')
            self.Error = True
        elif self.Priority > PriorityLevel.LOW:
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PRIORITY_TOO_LOW, Overwrite=True)
            # Create log entry
            self.CreateLogMessage(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid input Priority: lower than LOW')
            self.Error = True
        return OnExecStart

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
                self.Done = True
                self.Busy = False
            # Aborted before completion
            case CmdMessageState.ABORTED:
                self.Busy = False
            # Encountered an error during execution
            case CmdMessageState.ERROR:
                self.Error = True
                self.Busy = False

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        return Reset
