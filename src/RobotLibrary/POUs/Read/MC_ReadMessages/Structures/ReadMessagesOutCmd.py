"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadMessagesOutCmd
Author:      Thorsten Brach
Date:        2026-01-10

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

from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.Type.MessageType import MessageType
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP

class ReadMessagesOutCmd(IEC_Struct):
    """Structure for output command of ReadMessages function block."""

    MsgId                  : int
    """ID for function specific acknowledgement mechanism"""
    
    NumberOfActiveErrors   : int
    """Number of pending errors on RC"""
    
    NumberOfActiveWarnings : int
    """Number if pending warnings in RC"""
    
    Timestamp              : IEC_TIMESTAMP
    """Timestamp"""
    
    MsgType                : MessageType
    """Message Type"""
    
    Severity               : Severity
    """Severity of returned message according to .Table 5-47."""
    
    ErrorCode              : int
    """ErrorCode"""

    Text                   : str
    """Text"""