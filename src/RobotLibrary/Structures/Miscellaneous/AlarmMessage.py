"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AlarmMessage
Author:      Thorsten Brach
Date:        2025-12-18

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
from RobotLibrary.IEC_Types import DWORD,  STRING, IEC_Struct
from RobotLibrary.Enumerations.Type.MessageType import MessageType as MessageTypeEnum
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity as SeverityEnum
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Parameter import MESSAGE_TEXT_LEN


class AlarmMessage(IEC_Struct):

   
    Timestamp: SystemTime
    """Timestamp"""

    MessageType: MessageTypeEnum
    """Type of message according to Table 5-46"""

    Severity: SeverityEnum
    """Severity of message according to Table 5-47: Debug, Info, Warning, Error, Fatal error"""

    MessageCode: DWORD
    """Code of messages"""

    MessageText : STRING  = STRING(MESSAGE_TEXT_LEN)    
    
    """Static text of message (length: RobotLibraryParameter.MESSAGE_TEXT_LEN)"""
    
    
    def __str__(self) -> str:
        """Convert AlarmMessage to formatted string"""
        return f"{self.Timestamp} | {self.MessageType.toString()} | {self.Severity.toString()} | {self.MessageCode.value} | {self.MessageText}"