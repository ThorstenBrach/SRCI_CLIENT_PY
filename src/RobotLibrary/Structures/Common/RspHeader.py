"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RspHeader
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

from RobotLibrary.IEC_Types import USINT, UINT, IEC_Struct

from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity

    
class RspHeader(IEC_Struct):
  
    ParSeq : USINT
    """
    Parameter Sequence, used to identify sets of CMD parameter
    """
    
    State : CmdMessageState
    """
    Actual state of the command
    """

    AlarmMessageSeverity : Severity
    """
    Severity of returned message
    """

    AlarmMessageCode : UINT
    """ Message code for error/warning/info identification reported during execution of command according to
    • Error:
    • Warning
    • Info
    """
    
    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:
        
        bytes = bytearray()
        
        # header
        bytes.extend(self.ParSeq.GetBytes(order))
        bytes.extend(self.State.GetBytes(order))
        bytes.extend(self.AlarmMessageSeverity.GetBytes(order))
        bytes.extend(self.AlarmMessageCode.GetBytes(order))
        
        return bytes
