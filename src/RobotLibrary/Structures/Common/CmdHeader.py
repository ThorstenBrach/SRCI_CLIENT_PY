"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      CmdHeader
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

from RobotLibrary.IEC_Types import BYTE, IEC_Struct
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
    
class CmdHeader(IEC_Struct):
  
    CmdTyp          : CmdType
    """
    Type of command
    """
    
    ExecMode        : ExecutionMode
    """ 
    Specifies target buffer and processing behavior
    """
    
    ParSeq          : BYTE
    """
    Parameter Sequence, used to identify sets of CMD parameter
    """
    
    Priority        : PriorityLevel  
    """
    Priority of this command
    """    
    
    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:
        
        bytes = bytearray()
        
        # header
        bytes.extend(self.CmdTyp.GetBytes(order))
        bytes.extend(self.ExecMode.GetBytes(order))
        bytes.extend(self.ParSeq.GetBytes(order))
        bytes.extend(self.Priority.GetBytes(order))
        
        return bytes