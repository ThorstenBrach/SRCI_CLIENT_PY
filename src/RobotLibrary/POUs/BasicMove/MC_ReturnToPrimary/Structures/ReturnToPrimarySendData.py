"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReturnToPrimarySendData
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

from RobotLibrary.IEC_Types import USINT, UINT, REAL, BOOL
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader


class ReturnToPrimarySendData(CmdHeader):
    """Structure for received data from ReturnToPrimary command."""
    
    VelocityRate       : UINT
    """
    TCP velocity in % of nominal velocity
     •  <0%: (default) - Use default velocity
     •   0%:           - Use internal minimal velocity
     • 100%:           - Use maximal reference velocity
    See chapter 5.5.7 Robot dynamics
    """
    
    AccelerationRate   : UINT
    """
    Acceleration for movement in % of nominal acceleration
     •  <0%: (default) - Use default acceleration
     •   0%:           - Use internal minimal acceleration
     • 100%:           - Use maximal reference acceleration
    See chapter 5.5.7 Robot dynamics
    """
    
    DecelerationRate   : UINT
    """
    Deceleration for movement in % of nominal deceleration
     •  <0%: (default) - Use default deceleration 
     •   0%:           - Use internal minimal deceleration
     • 100%:           - Use maximal reference deceleration
    See chapter 5.5.7 Robot dynamics
    """
    
    JerkRate           : UINT
    """
    Jerk of the movement in % of nominal jerk
     •  <0%: (default) - Use default jerk
     •   0%:           - Use internal minimal jerk
     • 100%:           - Use maximal reference jerk
    See chapter 5.5.7 Robot dynamics
    """
    
    DistanceLimit      : REAL
    """
    Parameter is used if it is greater than 0 (default):
    Maximum allowed distance between current position and target position according to ReturnMode.
    If calculated distance is beyond specified Limit, RC returns an error
    """
    
    ToolNo             : USINT
    """
    Index of tool
    •      0: Flange (default)
    • 1..254: Tool frames
    """

    FrameNo            : USINT
    """
    Index of frame
      •      0: WCS (default)
     • 1..254: User frames
    """
    
    MoveTime           : UINT
    """
    Parameter is used if it is greater than 0 (default)
    • Velocity input is ignored
    • Parameter defines the time for the movement to reach the target position
    Error is sent by the RC if the time cannot be kept
    """
    
    ReturnMode         : BOOL
    """
    Defines target position when function is executed:
    • 0: Interrupt position (default) - Returns to position active,  when interrupt was executed
    • 1: End position                 - Returns to target position of interrupted segment
    """
    
    TrajectoryMode     : BOOL
    """
    Defines type of command movement. One of the optional modes must be supported
    """

    Enable : BOOL
    """Enables the command execution"""

    AllowDifferences : BOOL
    """Allows small differences between current position and target position"""

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.VelocityRate = UINT(0)
        self.AccelerationRate = UINT(0)
        self.DecelerationRate = UINT(0)
        self.JerkRate = UINT(0)
        self.DistanceLimit = REAL(0)
        self.ToolNo = USINT(0)
        self.FrameNo = USINT(0)
        self.MoveTime = UINT(0)
        self.ReturnMode = BOOL(False)
        self.TrajectoryMode = BOOL(False)
        self.Enable = BOOL(False)
        self.AllowDifferences = BOOL(False)