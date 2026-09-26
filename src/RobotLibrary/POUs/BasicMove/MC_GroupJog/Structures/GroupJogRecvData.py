"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      GroupJogRecvData
Author:      Thorsten Brach
Date:        2026-01-24

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

from RobotLibrary.IEC_Types import BYTE
from RobotLibrary.Structures.Common.RspHeader import RspHeader

    
class GroupJogRecvData(RspHeader):

    Status : BYTE
    """Status"""

    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:
        
        bytes = bytearray()
        
        # header
        bytes.extend(super().GetBytes(order))
        # response data
        bytes.extend(self.Status.GetBytes(order))
        
        return bytes