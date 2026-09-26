"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MoveDirectAbsoluteRecvData
Author:      Thorsten Brach
Date:        2026-01-05

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

from RobotLibrary.IEC_Types import USINT, SINT, INT, UINT, REAL
from RobotLibrary.Structures.Common.RspHeader import RspHeader



class MoveDirectAbsoluteRecvData(RspHeader):
    """Structure for received data from MoveDirectAbsolute command."""
    
    InvocationCounter : USINT
    """
    Relates to ListenerID >0
    Number of successful trigger-based command invocations - For more information refer TO chapter 5.5.12.4
    """

    Reserve           : SINT
    """Reserve"""

    OriginID          : INT
    """
    Unique system-generated ID of the "Action" when the function is triggered.
     • >0: The "Action" is started by the trigger funcrion with identical FollowID.
     • <0: The "Action" is stopped by the trigger function with identical FollowID.
    For more information see chapter 5.5.12.4 EmitterID, ListenerID, FollowID and OriginID
    """

    Progress          : UINT
    """
    Percentage of already traversed distance of current job.
    If not supported : • -1
    """

    RemainingDistance  : REAL
    """
    Distance-to-go of the current job.
     • -1: No valid value because move command is not yet active (valid values are pending) or not supported by RC
     • >0: Actual distance between current and target position
     •  0: Target position reached
    """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.InvocationCounter = USINT(0)
        self.Reserve = SINT(0)
        self.OriginID = INT(0)
        self.Progress = UINT(0)
        self.RemainingDistance = REAL(0.0)