"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      GroupResetSendData
Author:      Thorsten Brach
Date:        2026-01-23

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

from RobotLibrary.IEC_Types import BOOL
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader
from RobotLibrary.Enumerations import StepMode

class GroupResetSendData(CmdHeader):
  
    Enable: BOOL
    """Set TRUE to change RA power state to "Enabled\""""

    HoldToRun: BOOL
    """The robot will move while HoldToRun is set TRUE"""

    StepMode: StepMode
    """
    While activated the RI state switches to interrupted when a buffered command
    returns Done TRUE.
    At least one of the optional modes must be supported.
    """

    ManualStep: BOOL
    """
    Relates to StepMode 1 (Blending) and 2 (Exact stop).
    Start the next buffered command with the rising edge
    in T1 External or T2 External.
    """
    
    
    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:

        bytes = bytearray()

        # header
        bytes.extend(super().GetBytes(order))

        # command data
        bytes.extend(self.Enable.GetBytes(order))
        bytes.extend(self.HoldToRun.GetBytes(order))
        bytes.extend(self.StepMode.GetBytes(order))
        bytes.extend(self.ManualStep.GetBytes(order))

        return bytes
