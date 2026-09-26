"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReturnToPrimaryParCmd
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
from RobotLibrary.Enumerations.Mode.ReturnMode import ReturnMode
from RobotLibrary.Enumerations.Mode.TrajectoryMode import TrajectoryMode


class ReturnToPrimaryParCmd(IEC_Struct):
    

    ReturnMode         : ReturnMode
    """
    Defines target position when function is executed:
     • 0: Interrupt position (default) - Returns to position active,  when interrupt was executed
     • 1: End position                 - Returns to target position of interrupted segment
     """

    VelocityRate       : float
    """
    TCP velocity in % of nominal velocity
     •  <0%: (default) - Use default velocity
     •   0%:           - Use internal minimal velocity
     • 100%:           - Use maximal reference velocity
    See chapter 5.5.7 Robot dynamics
    """
    AccelerationRate   : float
    """
    Acceleration for movement in % of nominal acceleration
     •  <0%: (default) - Use default acceleration
     •   0%:           - Use internal minimal acceleration
     • 100%:           - Use maximal reference acceleration
    See chapter 5.5.7 Robot dynamics
    """

    DecelerationRate   : float
    """
    Deceleration for movement in % of nominal deceleration
     •  <0%: (default) - Use default deceleration 
     •   0%:           - Use internal minimal deceleration
     • 100%:           - Use maximal reference deceleration
    See chapter 5.5.7 Robot dynamics
    """
    JerkRate           : float
    """
    Jerk of the movement in % of nominal jerk
     •  <0%: (default) - Use default jerk
     •   0%:           - Use internal minimal jerk
     • 100%:           - Use maximal reference jerk
    See chapter 5.5.7 Robot dynamics
    """
    ToolNo             : int
    """Index of tool
     •      0: Flange (default)
     • 1..254: Tool frames
    """
    FrameNo            : int
    """Index of frame
     •      0: WCS (default)
     • 1..254: User frames
    """

    DistanceLimit      : float
    """Parameter is used if it is greater than 0 (default):
    Maximum allowed distance between current position and target position according to ReturnMode.
    If calculated distance is beyond specified Limit, RC returns an error
    """

    TrajectoryMode     : TrajectoryMode
    """Defines type of command movement. One of the optional modes must be supported
    """

    MoveTime           : int
    """Parameter is used if it is greater than 0 (default)
    • Velocity input is ignored
    • Parameter defines the time for the movement to reach the target position
    Error is sent by the RC if the time cannot be kept
    """

    AllowDifferences   : bool
    """
    Set TRUE to deactivate comparison of
     • ToolData and FrameData
     • ToolNo and PrimaryPosToolNo
     • FrameNo and PrimaryPosFrameNo
     """
