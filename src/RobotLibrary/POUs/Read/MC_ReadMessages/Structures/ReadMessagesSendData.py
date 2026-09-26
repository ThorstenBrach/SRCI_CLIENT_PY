"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadMessagesSendData
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
from RobotLibrary.IEC_Types import BOOL, USINT
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader


class ReadMessagesSendData(CmdHeader):
    
    MsgID        : USINT
    """ID for function specific acknowledgement mechanism"""

    Enable       : BOOL
    """TRUE when function is returning messages from RC"""

    MessageLevel : USINT
    """Defines up to which level of severity messages will be transmitted to the PLC’s message buffer"""


    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:

        bytes = bytearray()
        
        # header
        bytes.extend(super().GetBytes(order))
        # command data
        bytes.extend(self.MsgID.GetBytes(order))
        bytes.extend(self.Enable.GetBytes(order))
        bytes.extend(self.MessageLevel.GetBytes(order))

        return bytes