"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadMessagesRecvData
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

from RobotLibrary.IEC_Types import BOOL, USINT, SINT, DWORD, STRING
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP


class ReadMessagesRecvData(RspHeader):
    """Structure for received data of ReadMessages function block."""
    

    Enabled                : BOOL
    """Set TRUE to read messages from RC."""

    MsgId                  : USINT
    """ID for function specific acknowledgement mechanism"""

    NumberOfActiveErrors   : USINT
    """Number of pending errors on RC"""
    
    NumberOfActiveWarnings : USINT
    """Number if pending warnings in RC"""
    
    Timestamp              : IEC_TIMESTAMP
    """Timestamp"""
    
    MsgType                : USINT
    """Message Type"""
    
    Severity               : SINT
    """Severity of returned message according to .Table 5-47."""
    
    ErrorCode              : DWORD
    """ErrorCode"""
    
    Text                   : STRING = STRING(255)   
    """Text"""



    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:

        bytes = bytearray()
        
        # header
        bytes.extend(super().GetBytes(order))
        # command data
        bytes.extend(self.Enabled.GetBytes(order))
        bytes.extend(self.MsgId.GetBytes(order))
        bytes.extend(self.NumberOfActiveErrors.GetBytes(order))
        bytes.extend(self.NumberOfActiveWarnings.GetBytes(order))
        bytes.extend(self.Timestamp.GetBytes(order))    
        bytes.extend(self.MsgType.GetBytes(order))
        bytes.extend(self.Severity.GetBytes(order))
        bytes.extend(self.ErrorCode.GetBytes(order))
        bytes.extend(self.Text.GetBytes(order))

        return bytes