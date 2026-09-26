"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ChangeSpeedOverrideSendData
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

from RobotLibrary.IEC_Types import UINT
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader

class ChangeSpeedOverrideSendData(CmdHeader):
  
    Override  : UINT
    """
    Set value for override
     • 0% No movement of the robot
     • 10% default
     • ≤100%: use input parameter value
    """



    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:

        bytes = bytearray()

        # header
        bytes.extend(super().GetBytes(order))

        # command data
        bytes.extend(self.Override.GetBytes(order = order))
        return bytes
