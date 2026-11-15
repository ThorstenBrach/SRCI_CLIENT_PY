# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.logging_bridge
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Bridge from the logging of the PLC library to Python :mod:`logging`.
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""Bridge from the logging of the PLC library to Python :mod:`logging`.

Every function block of the library writes its log entries (``CreateLogMessage*``)
into the system log ring buffer of the axes group (``AxesGroup.MessageLog.SystemLogs``,
output ``SystemLog`` of ``MC_RobotTaskFB``) and to an optional *external logger*
(interface ``IMessageLogger``). :class:`PythonLogger` is such an external logger::

    import logging
    from srci.logging_bridge import PythonLogger
    from srci.types import Severity

    logging.basicConfig(level=logging.DEBUG)
    robot_task(..., ExternalLogger=PythonLogger(), LogLevel=Severity.DEBUG)

Loggers: ``srci.plc`` (system log of all FBs, the level follows the ST severity) and
``srci.rc`` (alarm messages of the robot controller, see :func:`forward_rc_messages`).
The ST ``LogLevel`` filters before the text is created - keep it at ``INFO`` in
production, ``DEBUG`` logs every telegram and costs cycle time.
"""

from __future__ import annotations

import logging
from typing import Any

from srci.functions.Convert.TO_STRING.ALARM_MESSAGE_TO_STRING import ALARM_MESSAGE_TO_STRING
from srci.types import AlarmMessage, Severity

__all__ = ["PythonLogger", "forward_rc_messages", "python_level"]

_LEVELS = {
    Severity.DEBUG: logging.DEBUG,
    Severity.INFO: logging.INFO,
    Severity.WARNING: logging.WARNING,
    Severity.ERROR: logging.ERROR,
    Severity.FATAL_ERROR: logging.CRITICAL,
}
# SEVERITY_TO_STRING(AlignString := TRUE) as it appears in the system log text
_TOKENS = [(f":{s.name.ljust(11)}:", level) for s, level in _LEVELS.items()]


def python_level(severity: int) -> int:
    """Python logging level of an ST ``Severity``."""
    try:
        return _LEVELS[Severity(severity)]
    except (KeyError, ValueError):
        return logging.INFO


class PythonLogger:
    """``IMessageLogger`` implementation that writes to Python loggers."""

    def __init__(self, plc: logging.Logger | None = None, rc: logging.Logger | None = None) -> None:
        self.plc = plc or logging.getLogger("srci.plc")
        self.rc = rc or logging.getLogger("srci.rc")

    def AddSystemLog(self, *, SystemLog: str = "") -> None:
        text = SystemLog.rstrip("\r\n")
        level = logging.INFO
        for token, lvl in _TOKENS:
            if token in text:
                level = lvl
                break
        if self.plc.isEnabledFor(level):
            self.plc.log(level, "%s", text)

    def AddMessageLog(self, *, MessageLog: AlarmMessage | None = None) -> None:
        if MessageLog is None:
            return
        level = python_level(MessageLog.Severity)
        if self.rc.isEnabledFor(level):
            self.rc.log(level, "%s", ALARM_MESSAGE_TO_STRING(Message=MessageLog).rstrip("\r\n"))


def forward_rc_messages(axes_group: Any, logger: PythonLogger) -> None:
    """Also write the alarm messages of the RC (``MessageLog.AddMessageLog``) to ``logger``.

    The PLC library keeps them only in the ring buffer ``AxesGroup.MessageLog.Messages``.
    """
    message_log = axes_group.MessageLog
    original = message_log.AddMessageLog

    def add_message_log(*, MessageLog: AlarmMessage | None = None) -> None:
        original(MessageLog=MessageLog)
        logger.AddMessageLog(MessageLog=MessageLog)

    message_log.AddMessageLog = add_message_log
