"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReturnToPrimaryOutCmd
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

from RobotLibrary.IEC_Types import IEC_Struct

class ReturnToPrimaryOutCmd(IEC_Struct):

    RemainingDistance  : float
    """
    Distance-to-go of the current job.
     • -1: No valid value because move command is not yet active (valid values are pending) or not supported by RC
     • >0: Actual distance between current and target position
     •  0: Target position reached
     """

    Progress           : float
    """
    Percentage of already traversed distance of current job.
     If not supported : • -1
    """

    PrimaryPosToolNo   : int
    """
    Tool index of target position of ReturnToPrimary
     • 0: Flange
     • 1..254: Tool frames
    """

    PrimaryPosFrameNo  : int
    """
    Frame index of target position of ReturnToPrimary
     • 0: WCS
     • 1..254: User frames
    """


    def __init__(self):
        self.RemainingDistance  = float(0)
        self.Progress           = float(0)
        self.PrimaryPosToolNo   = int(0)
        self.PrimaryPosFrameNo  = int(0)