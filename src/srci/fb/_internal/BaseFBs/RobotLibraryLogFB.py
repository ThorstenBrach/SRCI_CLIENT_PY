"""RobotLibraryLogFB

ST-Source: POUs/_internal/BaseFBs/RobotLibraryLogFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import srci.types as _T
from srci.functions.Convert.TO_STRING.ALARM_MESSAGE_TO_STRING import ALARM_MESSAGE_TO_STRING
from srci.functions.String.StrPadRight import StrPadRight
from srci.functions.String.StrReplace import StrReplace
from srci.iec.fb import FunctionBlock
from srci.iec.rt import CONCAT, LEN, MAX, copy_into
from srci.types import AlarmMessage, LogLevelEnum, MessageType, RobotLibraryDefines, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger

__all__ = ['RobotLibraryLogFB']


class RobotLibraryLogFB(FunctionBlock):

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Interface to an internal logger
        self.InternalLogger: IMessageLogger = None
        # Interface to an external logger
        self.ExternalLogger: IMessageLogger = None
        # Logging level
        self.LogLevel: Severity = Severity.INFO
        # VAR
        # Type of the function block
        self._myType: str = ''

    def __call__(self, *, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if InternalLogger is not None:
            self.InternalLogger = InternalLogger
        if ExternalLogger is not None:
            self.ExternalLogger = ExternalLogger
        if LogLevel is not None:
            self.LogLevel = Severity(LogLevel)
        self.__body()

    def __body(self) -> None:
        pass

    def CreateLogMessage(self, *, Timestamp: SystemTime | None = None, MessageType: _T.MessageType = MessageType.RI, Severity: _T.Severity = Severity.DEACTIVATE, MessageCode: int = 0, MessageText: str = '') -> str:
        if Timestamp is None:
            Timestamp = SystemTime()
        CreateLogMessage: str = ''
        # internal log message
        _message: AlarmMessage = AlarmMessage()
        # internal string
        _tmpString: str = ''

        if self.LogLevel <= Severity:
            copy_into(_message.Timestamp, Timestamp)
            _message.MessageType = MessageType
            _message.Severity = Severity
            _message.MessageCode = MessageCode
            _message.MessageText = StrPadRight(Str=self.MyType, SubStr=' ', Length=RobotLibraryDefines.MaxTypeNameLength)
            _message.MessageText = CONCAT(_message.MessageText, ': ')
            _message.MessageText = CONCAT(_message.MessageText, MessageText)

            # return log message
            CreateLogMessage = ALARM_MESSAGE_TO_STRING(Message=_message)

            # Check internal logger valid ?
            if self.InternalLogger is not None:
                self.InternalLogger.AddSystemLog(SystemLog=ALARM_MESSAGE_TO_STRING(Message=_message))

            # Check external logger valid ?
            if self.ExternalLogger is not None:
                self.ExternalLogger.AddSystemLog(SystemLog=ALARM_MESSAGE_TO_STRING(Message=_message))
        return CreateLogMessage

    def CreateLogMessagePara1(self, *, Timestamp: SystemTime | None = None, MessageType: _T.MessageType = MessageType.RI, Severity: _T.Severity = Severity.DEACTIVATE, MessageCode: int = 0, MessageText: str = '', Para1: str = '') -> str:
        if Timestamp is None:
            Timestamp = SystemTime()
        CreateLogMessagePara1: str = ''
        # internal log message
        _logMessage: AlarmMessage = AlarmMessage()

        if self.LogLevel <= Severity:
            MessageText = StrReplace(Str=MessageText, SubStr1='{1}', SubStr2=Para1)

            CreateLogMessagePara1 = self.CreateLogMessage(Timestamp=Timestamp, MessageType=MessageType, Severity=Severity, MessageCode=MessageCode, MessageText=MessageText)
        return CreateLogMessagePara1

    def CreateLogMessagePara2(self, *, Timestamp: SystemTime | None = None, MessageType: _T.MessageType = MessageType.RI, Severity: _T.Severity = Severity.DEACTIVATE, MessageCode: int = 0, MessageText: str = '', Para1: str = '', Para2: str = '') -> str:
        if Timestamp is None:
            Timestamp = SystemTime()
        CreateLogMessagePara2: str = ''
        # internal log message
        _logMessage: AlarmMessage = AlarmMessage()

        if self.LogLevel <= Severity:
            MessageText = StrReplace(Str=MessageText, SubStr1='{2}', SubStr2=Para2)

            CreateLogMessagePara2 = self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType, Severity=Severity, MessageCode=MessageCode, MessageText=MessageText, Para1=Para1)
        return CreateLogMessagePara2

    def CreateLogMessagePara3(self, *, Timestamp: SystemTime | None = None, MessageType: _T.MessageType = MessageType.RI, Severity: _T.Severity = Severity.DEACTIVATE, MessageCode: int = 0, MessageText: str = '', Para1: str = '', Para2: str = '', Para3: str = '') -> str:
        if Timestamp is None:
            Timestamp = SystemTime()
        CreateLogMessagePara3: str = ''
        # internal log message
        _logMessage: AlarmMessage = AlarmMessage()

        if self.LogLevel <= Severity:
            MessageText = StrReplace(Str=MessageText, SubStr1='{3}', SubStr2=Para3)

            CreateLogMessagePara3 = self.CreateLogMessagePara2(Timestamp=Timestamp, MessageType=MessageType, Severity=Severity, MessageCode=MessageCode, MessageText=MessageText, Para1=Para1, Para2=Para2)
        return CreateLogMessagePara3

    def CreateLogMessagePara4(self, *, Timestamp: SystemTime | None = None, MessageType: _T.MessageType = MessageType.RI, Severity: _T.Severity = Severity.DEACTIVATE, MessageCode: int = 0, MessageText: str = '', Para1: str = '', Para2: str = '', Para3: str = '', Para4: str = '') -> str:
        if Timestamp is None:
            Timestamp = SystemTime()
        CreateLogMessagePara4: str = ''
        # internal log message
        _logMessage: AlarmMessage = AlarmMessage()

        if self.LogLevel <= Severity:
            MessageText = StrReplace(Str=MessageText, SubStr1='{4}', SubStr2=Para4)

            CreateLogMessagePara4 = self.CreateLogMessagePara3(Timestamp=Timestamp, MessageType=MessageType, Severity=Severity, MessageCode=MessageCode, MessageText=MessageText, Para1=Para1, Para2=Para2, Para3=Para3)
        return CreateLogMessagePara4

    def CreateLogMessagePara5(self, *, Timestamp: SystemTime | None = None, MessageType: _T.MessageType = MessageType.RI, Severity: _T.Severity = Severity.DEACTIVATE, MessageCode: int = 0, MessageText: str = '', Para1: str = '', Para2: str = '', Para3: str = '', Para4: str = '', Para5: str = '') -> str:
        if Timestamp is None:
            Timestamp = SystemTime()
        CreateLogMessagePara5: str = ''
        # internal log message
        _logMessage: AlarmMessage = AlarmMessage()

        if self.LogLevel <= Severity:
            MessageText = StrReplace(Str=MessageText, SubStr1='{5}', SubStr2=Para5)

            CreateLogMessagePara5 = self.CreateLogMessagePara4(Timestamp=Timestamp, MessageType=MessageType, Severity=Severity, MessageCode=MessageCode, MessageText=MessageText, Para1=Para1, Para2=Para2, Para3=Para3, Para4=Para4)
        return CreateLogMessagePara5

    def CreateLogMessagePara6(self, *, Timestamp: SystemTime | None = None, MessageType: _T.MessageType = MessageType.RI, Severity: _T.Severity = Severity.DEACTIVATE, MessageCode: int = 0, MessageText: str = '', Para1: str = '', Para2: str = '', Para3: str = '', Para4: str = '', Para5: str = '', Para6: str = '') -> str:
        if Timestamp is None:
            Timestamp = SystemTime()
        CreateLogMessagePara6: str = ''
        # internal log message
        _logMessage: AlarmMessage = AlarmMessage()

        if self.LogLevel <= Severity:
            MessageText = StrReplace(Str=MessageText, SubStr1='{6}', SubStr2=Para6)

            CreateLogMessagePara6 = self.CreateLogMessagePara5(Timestamp=Timestamp, MessageType=MessageType, Severity=Severity, MessageCode=MessageCode, MessageText=MessageText, Para1=Para1, Para2=Para2, Para3=Para3, Para4=Para4, Para5=Para5)
        return CreateLogMessagePara6

    def _get_MyType(self) -> str:
        MyType: str = ''

        MyType = self._myType
        return MyType

    def _set_MyType(self, MyType: str) -> None:
        self._myType = MyType

        # set the max type name length
        RobotLibraryDefines.MaxTypeNameLength = MAX(LEN(self._myType), RobotLibraryDefines.MaxTypeNameLength)

    MyType = property(_get_MyType, _set_MyType)  # PROTECTED
