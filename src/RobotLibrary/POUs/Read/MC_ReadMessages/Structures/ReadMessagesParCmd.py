"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadMessagesParCmd
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
from RobotLibrary.IEC_Types import  IEC_Struct
from RobotLibrary.Enumerations.Level.MessageLevel import MessageLevel

class ReadMessagesParCmd(IEC_Struct):
    """Structure for parameter command of ReadMessages function block."""
    
    MsgID        : int
    """ID for function specific acknowledgement mechanism"""
    
    MessageLevel : MessageLevel
    """Defines up to which level of severity messages will be transmitted to the PLC's message buffer"""