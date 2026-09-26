"""Bridge from the PLC library logging to Python logging."""

from __future__ import annotations

import logging

import pytest

from srci.fb._internal.BaseFBs.RobotLibraryLogFB import RobotLibraryLogFB
from srci.logging_bridge import PythonLogger, forward_rc_messages, python_level
from srci.types import AlarmMessage, AxesGroup, MessageType, Severity, SystemTime


def test_levels() -> None:
    assert python_level(Severity.DEBUG) == logging.DEBUG
    assert python_level(Severity.FATAL_ERROR) == logging.CRITICAL
    assert python_level(99) == logging.INFO


def test_system_log_of_a_function_block(caplog: pytest.LogCaptureFixture) -> None:
    fb = RobotLibraryLogFB()
    fb.MyType = "TestFB"
    fb.ExternalLogger = PythonLogger()
    fb.LogLevel = Severity.DEBUG
    with caplog.at_level(logging.DEBUG, logger="srci.plc"):
        fb.CreateLogMessagePara2(
            Timestamp=SystemTime(),
            MessageType=MessageType.CMD,
            Severity=Severity.WARNING,
            MessageCode=7,
            MessageText="value {1} of {2}",
            Para1="3",
            Para2="x",
        )
        fb.LogLevel = Severity.ERROR  # filtered in ST before the text is created
        fb.CreateLogMessage(
            Timestamp=SystemTime(),
            MessageType=MessageType.CMD,
            Severity=Severity.INFO,
            MessageCode=0,
            MessageText="no",
        )
    assert len(caplog.records) == 1
    rec = caplog.records[0]
    assert rec.levelno == logging.WARNING and rec.name == "srci.plc"
    assert "TestFB" in rec.getMessage() and rec.getMessage().endswith("value 3 of x")


def test_rc_messages_are_forwarded(caplog: pytest.LogCaptureFixture) -> None:
    ag = AxesGroup()
    ag.MessageLog.LogLevel = Severity.INFO
    forward_rc_messages(ag, PythonLogger())
    with caplog.at_level(logging.INFO, logger="srci.rc"):
        ag.MessageLog.AddMessageLogByParameter(
            Timestamp=SystemTime(),
            MessageType=MessageType.RC,
            Severity=Severity.ERROR,
            MessageCode=0x6C02,
            MessageText="motion error",
        )
    assert ag.MessageLog.MessagesEntries == 1
    assert ag.MessageLog.Messages[0].MessageText == "motion error"
    assert caplog.records[0].levelno == logging.ERROR and "motion error" in caplog.records[0].getMessage()
    PythonLogger().AddMessageLog(MessageLog=None)
    PythonLogger().AddMessageLog(MessageLog=AlarmMessage())
