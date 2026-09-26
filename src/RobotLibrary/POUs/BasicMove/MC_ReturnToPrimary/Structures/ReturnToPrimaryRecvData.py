"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReturnToPrimaryRecvData
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

from RobotLibrary.IEC_Types import USINT, UINT, REAL
from RobotLibrary.Structures.Common.RspHeader import RspHeader


class ReturnToPrimaryRecvData(RspHeader):
    """Structure for received data from ReturnToPrimary command."""
    
    Progress           : UINT
    """"
    Percentage of already traversed distance of current job.
    If not supported : • -1
    """

    RemainingDistance  : REAL
    """"
    Distance-to-go of the current job.
    • -1: No valid value because move command is not yet active (valid values are pending) or not supported by RC
    • >0: Actual distance between current and target position
    •  0: Target position reached
    """
    PrimaryPosToolNo   : USINT
    """
    Tool index of target position of ReturnToPrimary
     • 0: Flange
     • 1..254: Tool frames
     """

    PrimaryPosFrameNo  : USINT
    """
    Frame index of target position of ReturnToPrimary
     • 0: WCS
     • 1..254: User frames
     """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.Progress  = UINT(0)
        self.RemainingDistance  = REAL(0)
        self.PrimaryPosToolNo   = USINT(0)  
        self.PrimaryPosFrameNo  = USINT(0)
