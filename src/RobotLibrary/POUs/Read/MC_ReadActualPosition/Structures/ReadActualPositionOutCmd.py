"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadActualPositionOutCmd
Author:      Thorsten Brach
Date:        2026-01-25

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

from typing import Any
from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Structures.Cartesian.RobotCartesianPosition import RobotCartesianPosition
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointPosition 

class ReadActualPositionOutCmd(IEC_Struct):

    """
    Docstring for ReadActualPositionOutCmd
    """
    
    InvocationCounter       : int
    """
    Relates to ListenerID >0 
    Number of successful trigger -based command invocations
    For more information refer to chapter 5.5.12.4.
    """
    
    OriginID                : int
    """
    Unique system-generated ID of the "Action" when the function is triggered.
    • >0: The "Action" is started by the trigger funcrion with identical FollowID.
    • <0: The "Action" is stopped by the trigger function with identical FollowID.
    For more information see chapter 5.5.12.4 EmitterID, ListenerID, FollowID and OriginID
    """

    ToolNoReturn            : int
    """Index of tool of returned position
     •     -1: Currently used tool on RC
     •      0: Flange (default)
     • 1..254: Tool frames
    """

    FrameNoReturn           : int
    """
    Index of frame of returned position
     •     -1: Currently used frame on RC
     •      0: WCS (default)
     • 1..254: User frames
    """

    ActualCartesianPosition : RobotCartesianPosition
    """Absolute coordinates in the active coordinate system"""

    ActualJointPosition     : RobotJointPosition
    """Absolute position of the robot in Joint position."""



    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        
        self.InvocationCounter = 0
        self.OriginID = 0
        self.ToolNoReturn = 0
        self.FrameNoReturn = 0
        self.ActualCartesianPosition = RobotCartesianPosition()
        self.ActualJointPosition = RobotJointPosition()

