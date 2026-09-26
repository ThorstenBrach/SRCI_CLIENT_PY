"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibraryLogFB
Author:      Thorsten Brach
Date:        2025-12-26

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

from RobotLibrary.IEC_Types import IEC_POU, STRING, DWORD, IEC_String
from typing import Optional, Union
from RobotLibrary.IEC_Standard import CONCAT
from RobotLibrary.Interfaces.IMessageLogger import IMessageLogger
from RobotLibrary.Enumerations.Type.MessageType import MessageType
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Structures.Miscellaneous.AlarmMessage import AlarmMessage
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Parameter import MESSAGE_TEXT_LEN


# Global configuration for maximum type name length
class _RobotLibraryDefines:
    MaxTypeNameLength: int = 0

RobotLibraryDefines = _RobotLibraryDefines()


class RobotLibraryLogFB(IEC_POU):
    #VAR_INPUT
    InternalLogger : IMessageLogger = None #type: ignore  # Optional, default None
    ExternalLogger : IMessageLogger = None #type: ignore  # Optional, default None
    LogLevel       : Severity = Severity.INFO

    #VAR
    _myType = STRING(80)


    @property
    def MyType(self):
        return self._myType

    @MyType.setter
    def MyType(self, value) -> None:
        self._myType = value
        # Set the max type name length
        type_str = str(value)
        RobotLibraryDefines.MaxTypeNameLength = max(len(type_str), RobotLibraryDefines.MaxTypeNameLength)
    
    
    # --------------------------------------------------------
    # CreateLogMessage - with optional parameters (Python overloading)
    # --------------------------------------------------------
    def CreateLogMessage(
        self,
        Timestamp: SystemTime,
        MessageType: MessageType,
        Severity: Severity,
        MessageCode: Union[int, DWORD],
        MessageText: str,
        Para1: Optional[Union[str, IEC_String, STRING]] = None,
        Para2: Optional[Union[str, IEC_String, STRING]] = None,
        Para3: Optional[Union[str, IEC_String, STRING]] = None,
        Para4: Optional[Union[str, IEC_String, STRING]] = None,
        Para5: Optional[Union[str, IEC_String, STRING]] = None,
        Para6: Optional[Union[str, IEC_String, STRING]] = None
    ) -> IEC_String:
        
        """
        Create log message with optional parameter placeholders.
        
        Args:
            Timestamp: Message timestamp
            MessageType: Type of message
            Severity: Message severity level
            MessageCode: Message code
            MessageText: Message text with optional placeholders {1} to {6}
            Para1-Para6: Optional parameters to replace placeholders
            
        Returns:
            Formatted log message as IEC_String
        """
        result = IEC_String(MESSAGE_TEXT_LEN)
        
        if int(self.LogLevel) <= int(Severity):
            # Helper to coerce STRING/IEC_String/str to plain str
            def _to_str(p: Optional[Union[str, IEC_String, STRING]]) -> Optional[str]:
                if p is None:
                    return None
                try:
                    # IEC_String and STRING descriptor instances should stringify cleanly
                    return str(p)
                except Exception:
                    return None
            # Replace placeholders with parameters           
            p1 = _to_str(Para1)
            p2 = _to_str(Para2)
            p3 = _to_str(Para3)
            p4 = _to_str(Para4)
            p5 = _to_str(Para5)
            p6 = _to_str(Para6)
            
            if p1 is not None:
                MessageText = MessageText.replace('{1}', p1)
            if p2 is not None:
                MessageText = MessageText.replace('{2}', p2)
            if p3 is not None:
                MessageText = MessageText.replace('{3}', p3)
            if p4 is not None:
                MessageText = MessageText.replace('{4}', p4)
            if p5 is not None:
                MessageText = MessageText.replace('{5}', p5)
            if p6 is not None:
                MessageText = MessageText.replace('{6}', p6)
            
            # Create internal log message
            _message = AlarmMessage()
            _message.Timestamp = Timestamp
            _message.MessageType = MessageType
            _message.Severity = Severity
            # Accept int or DWORD for MessageCode
            try:
                _message.MessageCode = MessageCode if isinstance(MessageCode, DWORD) else DWORD(int(MessageCode))
            except Exception:
                # Fallback to zero if conversion fails
                _message.MessageCode = DWORD(0)
            
            # Build message text with type prefix
            padded_type = str(self._myType).ljust(RobotLibraryDefines.MaxTypeNameLength)
            _message.MessageText = CONCAT(padded_type, ': ')
            _message.MessageText = CONCAT(str(_message.MessageText), MessageText)
            
            # Convert to string
            result = IEC_String(MESSAGE_TEXT_LEN)
            result.set(str(_message))
            
            # Check internal logger valid
            if self.InternalLogger is not None:
                self.InternalLogger.AddSystemLog(SystemLog=result)
            
            # Check external logger valid
            if self.ExternalLogger is not None:
                self.ExternalLogger.AddSystemLog(SystemLog=result)
        
        return result    