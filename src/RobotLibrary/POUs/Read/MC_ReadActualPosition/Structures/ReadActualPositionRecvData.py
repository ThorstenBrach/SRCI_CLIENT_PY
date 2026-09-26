"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadActualPositionRecvData
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

from RobotLibrary.IEC_Types import USINT, SINT, INT
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.Joint.RobotJointPosition  import RobotJointPosition
from RobotLibrary.Structures.Cartesian.RobotCartesianPosition import RobotCartesianPosition


class ReadActualPositionRecvData(RspHeader):
    """Structure for received data from ReadActualPosition command."""
    
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

    ToolNoReturn            : USINT
    """
    Index of tool of returned position
     •     -1: Currently used tool on RC
     •      0: Flange (default)
     • 1..254: Tool frames
    """

    FrameNoReturn           : USINT
    """
    Index of frame of returned position
     •     -1: Currently used frame on RC
     •      0: WCS (default)
     • 1..254: User frames
     """
    
    ActualCartesianPosition : RobotCartesianPosition
    """ Absolute coordinates in the active coordinate system"""
    
    ActualJointPosition     : RobotJointPosition
    """Absolute position of the robot in Joint position."""



    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.InvocationCounter = USINT(0)
        self.Reserve = SINT(0)
        self.OriginID = INT(0)
        self.ToolNoReturn = INT(0)
        self.FrameNoReturn = INT(0)
        self.ActualCartesianPosition = RobotCartesianPosition()
        self.ActualJointPosition = RobotJointPosition()

