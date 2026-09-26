"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupMessageLogFB
Author:      Thorsten Brach
Date:        2026-01-02

Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
from RobotLibrary.IEC_Types import  UINT, STRING, ARRAY 
from RobotLibrary.IEC_Standard import LIMIT, StrReplace
from RobotLibrary.Structures.Miscellaneous.AlarmMessage import AlarmMessage
from RobotLibrary.Interfaces.IMessageLogger import IMessageLogger
from RobotLibrary.Enumerations.Level.LogLevel import LogLevel as LogLevelEnum
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Parameter import SYSTEM_LOG_MAX, MESSAGE_LOG_MAX, MESSAGE_TEXT_LEN

class AxesGroupMessageLogFB(IMessageLogger):
    """
    Python IEC Function Block: AxesGroupMessageLogFB
    Implements a message and system log buffer for axes group.
    """

    #region VAR_INPUT
    LogLevel         : LogLevelEnum = LogLevelEnum.INFO
    """Logging level"""
    ExternalLogger   : IMessageLogger = None #type: ignore
    """Interface to an external logger"""
    #endregion
    
    #region VAR_OUTPUT
    SystemLogEntries : int = 0
    """ Amount of system log entries"""
    
    MessagesEntries  : int = 0
    """ Amount of message log entries"""

    SystemLogs       : ARRAY[STRING] = ARRAY(0, SYSTEM_LOG_MAX,  STRING(MESSAGE_TEXT_LEN))
    """ System log"""

    Messages         : ARRAY[AlarmMessage] = ARRAY(0, MESSAGE_LOG_MAX, AlarmMessage)  
    """ Message Log"""
    #endregion

    # ============================================================================
    # AddMessageLog
    # ============================================================================                
    def AddMessageLog(self, MessageLog: AlarmMessage):
        
         # internal index
        _idx = int(0)
         # internal index to delete
        _idxFound = int(-1)
         # lowest Severity
        _lowestSeverity = Severity.FATAL_ERROR
        
        # Check entry must be added?
        if ((self.LogLevel <= MessageLog.Severity   ) and 
            (self.LogLevel > LogLevelEnum.DEACTIVATE)):        
            # Check message buffer is full?
            if int(self.MessagesEntries) >= MESSAGE_LOG_MAX:
                # find lowest Severity
                _lowestSeverity = Severity.FATAL_ERROR
                for _idx in range(1, MESSAGE_LOG_MAX + 1):
                    _lowestSeverity = min(self.Messages[_idx].Severity, _lowestSeverity)

                # search for the oldest message with a lower Severity
                for _idx in range(MESSAGE_LOG_MAX, 0, -1):
                    if ((self.Messages[_idx].Severity < MessageLog.Severity) and 
                        (self.Messages[_idx].Severity <= _lowestSeverity   )):
                        _idxFound = _idx
                        break

                # check message must be deleted?
                if _idxFound > 0:
                    # shift all messages starting from the found index one position forwards
                    for _idx in range(_idxFound, MESSAGE_LOG_MAX):
                        self.Messages[_idx] = self.Messages[_idx + 1]

            
            # shift all messages one position backwards (make space at index 0)
            for _idx in range(MESSAGE_LOG_MAX, 0, -1):
                self.Messages[_idx] = self.Messages[_idx - 1]

            # Add new message at position 0
            self.Messages[0].Timestamp   = MessageLog.Timestamp
            self.Messages[0].MessageType = MessageLog.MessageType
            self.Messages[0].Severity    = MessageLog.Severity
            self.Messages[0].MessageText = MessageLog.MessageText
            self.Messages[0].MessageCode = MessageLog.MessageCode

            # inc message counter
            self.MessagesEntries = min(self.MessagesEntries + 1, MESSAGE_LOG_MAX)

    # ============================================================================
    # AddMessageLogByParameter
    # ============================================================================                
    def AddMessageLogByParameter(self, Timestamp, MessageType, Severity, MessageCode, MessageText):
        
        # create temporary AlarmMessage
        _message = AlarmMessage()
        
        _message.Timestamp   = Timestamp
        _message.MessageType = MessageType
        _message.MessageCode = MessageCode
        _message.MessageText = MessageText
        _message.Severity    = Severity

        # Add message to message buffer       
        self.AddMessageLog(_message)        

    # ============================================================================
    # AddSystemLog
    # ============================================================================                
    def AddSystemLog(self, SystemLog):
        
        # shift all messages one position backwards (make space at index 0)
        for _idx in range(SYSTEM_LOG_MAX, 0, -1):
            self.SystemLogs[_idx] = self.SystemLogs[_idx - 1]
            
        SystemLog = StrReplace(SystemLog, "\r", "") 
        SystemLog = StrReplace(SystemLog, "\n", "")
            
        self.SystemLogs[0] = SystemLog
        # inc system log counter
        self.SystemLogEntries = LIMIT(0, (self.SystemLogEntries + 1), (SYSTEM_LOG_MAX))

    # ============================================================================
    # CheckMessageCodePresent
    # ============================================================================                
    def CheckMessageCodePresent(self, MessageCode):
        result = False
        for i in range(0, MESSAGE_LOG_MAX + 1):
            if self.Messages[i].MessageCode == MessageCode:
                result = True
                
        return result
    # ============================================================================
    # DeleteMessages
    # ============================================================================                
    def DeleteMessages(self):
        # delete all messages by re-initializing the array        
        self.Messages = ARRAY(0, MESSAGE_LOG_MAX, AlarmMessage)
        # set message entries to 0
        self.MessagesEntries = 0

    # ============================================================================
    # DeleteSystemLogs
    # ============================================================================                
    def DeleteSystemLogs(self):
        # delete all system logs by re-initializing the array        
        self.SystemLogs = ARRAY(0, SYSTEM_LOG_MAX, STRING(MESSAGE_TEXT_LEN))
        # set system log entries to 0
        self.SystemLogEntries = 0