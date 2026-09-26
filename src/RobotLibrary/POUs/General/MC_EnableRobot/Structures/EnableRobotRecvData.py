"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      EnableRobotRecvData
Author:      Thorsten Brach
Date:        2025-12-22

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

from RobotLibrary.IEC_Types import BOOL
from RobotLibrary.Structures.Common.RspHeader import RspHeader

    
class EnableRobotRecvData(RspHeader):
  
    Enabled : BOOL
    """ 
    TRUE when robot is set to RA power state "Enabled".
    """

    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:
        
        bytes = bytearray()
        
        # header
        bytes.extend(super().GetBytes(order))
        # response data
        bytes.extend(self.Enabled.GetBytes(order))
        
        return bytes