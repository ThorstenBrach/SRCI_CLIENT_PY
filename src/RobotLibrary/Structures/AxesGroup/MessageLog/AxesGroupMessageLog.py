"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupMessageLog
Author:      Thorsten Brach
Date:        2025-12-20

Description:

Copyright:
    (C) 2025 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from RobotLibrary.IEC_Types import UINT ,ARRAY, STRING, IEC_Struct 
from RobotLibrary.Parameter import SYSTEM_LOG_MAX, MESSAGE_LOG_MAX, MESSAGE_TEXT_LEN
from RobotLibrary.Enumerations.Level.LogLevel import LogLevel
from RobotLibrary.Structures.Miscellaneous.AlarmMessage import AlarmMessage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from RobotLibrary.Interfaces.IMessageLogger import IMessageLogger

class AxesGroupMessageLog(IEC_Struct):
  
    SystemLogEntries : UINT = UINT(SYSTEM_LOG_MAX)
    """ Amount of system log entries"""

    MessagesEntries  : UINT = UINT(MESSAGE_LOG_MAX)
    """ Amount of message log entries"""

    LogLevel         : LogLevel
    """ Logging level"""

    SystemLog        : ARRAY[STRING] = ARRAY(0, SYSTEM_LOG_MAX, STRING(MESSAGE_TEXT_LEN))
    """ System log"""

    Messages         : ARRAY[AlarmMessage] = ARRAY(0, MESSAGE_LOG_MAX, AlarmMessage)
    """ Message Log"""

    ExternalLogger   : 'IMessageLogger'
    """ Interface to an external logger"""
