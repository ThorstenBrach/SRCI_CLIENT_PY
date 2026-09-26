"""AxesGroupMessageLogFB

ST-Source: POUs/_internal/LogFBs/AxesGroupMessageLogFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
import srci.types as _T
from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import DINT_TO_UINT
from srci.iec.fb import FunctionBlock
from srci.iec.rt import ADR, ADR_ELEM, LIMIT, MIN, SysDepMemCpy, SysDepMemSet, copy_into, st_for_end, type_size
from srci.types import AlarmMessage, LogLevelEnum, MessageType, RobotLibraryParameter, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger

__all__ = ['AxesGroupMessageLogFB']


class AxesGroupMessageLogFB(FunctionBlock):

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Logging level
        self.LogLevel: Severity = Severity.DEACTIVATE
        # Interface to an external logger
        self.ExternalLogger: IMessageLogger = None
        # VAR_OUTPUT
        # Amount of system log entries
        self.SystemLogEntries: int = 0
        # Amount of message log entries
        self.MessagesEntries: int = 0
        # System log
        self.SystemLogs: list[str] = [''] * _iec.array_len(0, _iec.Param('SYSTEM_LOG_MAX'))
        # Message Log
        self.Messages: list[AlarmMessage] = [AlarmMessage() for _ in range(_iec.array_len(0, _iec.Param('MESSAGE_LOG_MAX')))]

    def __call__(self, *, LogLevel: Severity | None = None, ExternalLogger: IMessageLogger | None = None) -> None:
        if LogLevel is not None:
            self.LogLevel = Severity(LogLevel)
        if ExternalLogger is not None:
            self.ExternalLogger = ExternalLogger
        self.__body()

    def __body(self) -> None:
        pass

    def AddMessageLog(self, *, MessageLog: AlarmMessage | None = None) -> None:  # PUBLIC
        if MessageLog is None:
            MessageLog = AlarmMessage()
        # internal index
        _idx: int = 0
        # internal index to delete
        _idxFound: int = 0
        # lowest Severity
        _lowestSeverity: Severity = Severity.FATAL_ERROR
        # temporary buffer ( must be one element less than the message log !!! )
        _tmpBuffer: list[AlarmMessage] = [AlarmMessage() for _ in range(_iec.array_len(0, _iec.Param('MESSAGE_LOG_MAX', -1)))]

        # Check entry must be added ?
        if self.LogLevel <= MessageLog.Severity and self.LogLevel > Severity.DEACTIVATE:
            # Check message buffer is full ?
            if self.MessagesEntries >= RobotLibraryParameter.MESSAGE_LOG_MAX:
                # find lowest Severity
                for _idx in range(1, RobotLibraryParameter.MESSAGE_LOG_MAX + 1):
                    # check entry has a lower severity ?
                    _lowestSeverity = MIN(self.Messages[_idx].Severity, _lowestSeverity)
                else:
                    _idx = st_for_end(1, RobotLibraryParameter.MESSAGE_LOG_MAX)

                # search for the oldes message with a lower Severity
                for _idx in range(RobotLibraryParameter.MESSAGE_LOG_MAX, 0, -1):
                    # message found ?
                    if self.Messages[_idx].Severity < MessageLog.Severity and self.Messages[_idx].Severity <= _lowestSeverity:
                        # save index to delete
                        _idxFound = _idx
                        break
                else:
                    _idx = st_for_end(RobotLibraryParameter.MESSAGE_LOG_MAX, 1, -1)

                # check message must be deleted ?
                if _idxFound > 0:
                    # shift all messages starting from the found index one position forwards
                    for _idx in range(_idxFound, RobotLibraryParameter.MESSAGE_LOG_MAX - 1 + 1):
                        copy_into(self.Messages[_idx], self.Messages[_idx + 1])

            # shift all messages one position backwards
            # shift messages log entries
            SysDepMemCpy(pDest=ADR_ELEM(_tmpBuffer, 0, _iec.StructType(AlarmMessage)), pSrc=ADR_ELEM(self.Messages, 0, _iec.StructType(AlarmMessage)), DataLen=type_size(_iec.ArrayType(0, _iec.Param('MESSAGE_LOG_MAX', -1), _iec.StructType(AlarmMessage))))
            SysDepMemCpy(pDest=ADR_ELEM(self.Messages, 1, _iec.StructType(AlarmMessage)), pSrc=ADR_ELEM(_tmpBuffer, 0, _iec.StructType(AlarmMessage)), DataLen=type_size(_iec.ArrayType(0, _iec.Param('MESSAGE_LOG_MAX', -1), _iec.StructType(AlarmMessage))))

            # Add new message
            copy_into(self.Messages[0].Timestamp, MessageLog.Timestamp)
            self.Messages[0].MessageType = MessageLog.MessageType
            self.Messages[0].Severity = MessageLog.Severity
            self.Messages[0].MessageText = MessageLog.MessageText
            self.Messages[0].MessageCode = MessageLog.MessageCode
            self.Messages[0].AcrID = MessageLog.AcrID  # ST-FIX F74
            self.Messages[0].CmdType = MessageLog.CmdType  # ST-FIX F74

            # inc message counter
            self.MessagesEntries = DINT_TO_UINT(LIMIT(0, self.MessagesEntries + 1, RobotLibraryParameter.MESSAGE_LOG_MAX))

    def AddMessageLogByParameter(self, *, Timestamp: SystemTime | None = None, MessageType: _T.MessageType = MessageType.RI, Severity: _T.Severity = Severity.DEACTIVATE, MessageCode: int = 0, MessageText: str = '') -> None:  # PUBLIC
        if Timestamp is None:
            Timestamp = SystemTime()
        # temporary message
        _message: AlarmMessage = AlarmMessage()

        copy_into(_message.Timestamp, Timestamp)
        _message.MessageType = MessageType
        _message.MessageCode = MessageCode
        _message.MessageText = MessageText
        _message.Severity = Severity

        # Add message to message buffer
        self.AddMessageLog(MessageLog=_message)

    def AddSystemLog(self, *, SystemLog: str = '') -> None:  # PUBLIC
        # internal index
        _idx: int = 0
        # internal log message
        _message: AlarmMessage = AlarmMessage()
        # temporary buffer ( must be one element less than the system log !!! )
        _tmpBuffer: list[str] = [''] * _iec.array_len(0, _iec.Param('SYSTEM_LOG_MAX', -1))

        # shift system log entries
        SysDepMemCpy(pDest=ADR_ELEM(_tmpBuffer, 0, _iec.StringType(255)), pSrc=ADR_ELEM(self.SystemLogs, 0, _iec.StringType(255)), DataLen=type_size(_iec.ArrayType(0, _iec.Param('SYSTEM_LOG_MAX', -1), _iec.StringType(255))))
        SysDepMemCpy(pDest=ADR_ELEM(self.SystemLogs, 1, _iec.StringType(255)), pSrc=ADR_ELEM(_tmpBuffer, 0, _iec.StringType(255)), DataLen=type_size(_iec.ArrayType(0, _iec.Param('SYSTEM_LOG_MAX', -1), _iec.StringType(255))))

        # Delete CR from system log message
        SystemLog = StrReplace(Str=SystemLog, SubStr1='\r', SubStr2='')
        # Delete LF from system log message
        SystemLog = StrReplace(Str=SystemLog, SubStr1='\n', SubStr2='')

        # Add System log to buffer
        self.SystemLogs[0] = SystemLog

        # inc SystemLog counter
        self.SystemLogEntries = DINT_TO_UINT(LIMIT(0, self.SystemLogEntries + 1, RobotLibraryParameter.SYSTEM_LOG_MAX))

    def CheckMessageCodePresent(self, *, MessageCode: int = 0) -> bool:
        CheckMessageCodePresent: bool = False
        # internal index for loops
        _idx: int = 0

        for _idx in range(0, RobotLibraryParameter.MESSAGE_LOG_MAX + 1):
            if self.Messages[_idx].MessageCode == MessageCode:
                CheckMessageCodePresent = True
                return CheckMessageCodePresent
        return CheckMessageCodePresent

    def DeleteMessages(self) -> None:  # PUBLIC
        # reset messages
        SysDepMemSet(pDest=ADR(self, 'Messages', _iec.ArrayType(0, _iec.Param('MESSAGE_LOG_MAX'), _iec.StructType(AlarmMessage))), Value=0, DataLen=type_size(_iec.ArrayType(0, _iec.Param('MESSAGE_LOG_MAX'), _iec.StructType(AlarmMessage))))
        # reset message counter
        self.MessagesEntries = 0

    def DeleteSystemLogs(self) -> None:
        # reset SystemLogs
        SysDepMemSet(pDest=ADR(self, 'SystemLogs', _iec.ArrayType(0, _iec.Param('SYSTEM_LOG_MAX'), _iec.StringType(255))), Value=0, DataLen=type_size(_iec.ArrayType(0, _iec.Param('SYSTEM_LOG_MAX'), _iec.StringType(255))))
        # reset SystemLogs counter
        self.SystemLogEntries = 0
