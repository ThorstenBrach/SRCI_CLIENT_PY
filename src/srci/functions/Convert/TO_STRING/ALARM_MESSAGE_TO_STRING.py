"""ALARM_MESSAGE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/ALARM_MESSAGE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.Convert.TO_STRING.MESSAGE_TYPE_TO_STRING import MESSAGE_TYPE_TO_STRING
from srci.functions.Convert.TO_STRING.SEVERITY_TO_STRING import SEVERITY_TO_STRING
from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import DATE_TO_STRING, DWORD_TO_STRING, TOD_TO_STRING
from srci.iec.rt import CONCAT
from srci.types import AlarmMessage

__all__ = ['ALARM_MESSAGE_TO_STRING']


def ALARM_MESSAGE_TO_STRING(*, Message: AlarmMessage | None = None) -> str:
    if Message is None:
        Message = AlarmMessage()
    ALARM_MESSAGE_TO_STRING: str = ''
    # Carrage return and line feed
    CRLF: str = '\r\n'

    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, DATE_TO_STRING(Message.Timestamp.SystemDate))
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, '-')
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, TOD_TO_STRING(Message.Timestamp.SystemTime))
    ALARM_MESSAGE_TO_STRING = StrReplace(Str=ALARM_MESSAGE_TO_STRING, SubStr1='TOD#', SubStr2='')
    ALARM_MESSAGE_TO_STRING = StrReplace(Str=ALARM_MESSAGE_TO_STRING, SubStr1='D#', SubStr2='')
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, ':')
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, MESSAGE_TYPE_TO_STRING(Value=Message.MessageType, AlignString=True))
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, ':')
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, SEVERITY_TO_STRING(Value=Message.Severity, AlignString=True))
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, ':')
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, DWORD_TO_STRING(Message.MessageCode))
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, ':')
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, Message.MessageText)
    ALARM_MESSAGE_TO_STRING = CONCAT(ALARM_MESSAGE_TO_STRING, CRLF)
    return ALARM_MESSAGE_TO_STRING
