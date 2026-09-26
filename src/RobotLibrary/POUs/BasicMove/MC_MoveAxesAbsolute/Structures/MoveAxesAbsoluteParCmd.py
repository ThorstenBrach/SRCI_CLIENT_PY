"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MoveAxesAbsoluteParCmd
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

from typing import Any
from RobotLibrary.IEC_Types import IEC_Struct, ARRAY
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointPosition
from RobotLibrary.Enumerations.Mode.BlendingMode import BlendingMode as BlendingModeEnum
from RobotLibrary.Structures.Miscellaneous.ArmConfigParameter import ArmConfigParameter

class MoveAxesAbsoluteParCmd(IEC_Struct):

    JointPosition      : RobotJointPosition
    """Absolute end position of the robot in Joint position."""

    VelocityRate       : float
    """
    Axes velocity in % of nominal velocity.
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
    """
    Index of tool
     •      0: Flange (default)
     • 1..254: Tool frames
    """

    BlendingMode       : BlendingModeEnum
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the next command. 
    The user can choose a transition type between exact stop and different blend possibilities
    """
    
    BlendingParameter  : ARRAY[float] = ARRAY(0, 1, float)
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""

    MoveTime           : int
    """Parameter is used if it is greater than 0 (default)
    • Velocity input is ignored
    • Parameter defines the time for the movement to reach the target position
    • Error is sent by the RC if the time cannot be kept
    """

    ConfigMode         : ArmConfigParameter
    """Defines the usage of the config byte inside the position according to Table 6-238"""

    Manipulation       : bool
    """
    Set TRUE to allow manipulation of this move command through superimposing functions.
    For more information see chapter 5.5.9.5
    """

    EmitterID          : ARRAY [int] = ARRAY(0, 3, int)
    """
    ID of Action that will be executed when this command is active
     • >0: Start Action - Start executing the Action function with the identical ListenerID.
     • <0: Stop Action  -  Stop executing the Action function with the identical ListenerID.
     • 0: No trigger (default)-  If no EmitterID is defined, the function will not trigger any Action during its execution
    For more information see section Triggers of this chapter or chapter 5.5.12.4.
    """
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.JointPosition = RobotJointPosition()
        self.VelocityRate = float(0)
        self.AccelerationRate = float(0)
        self.DecelerationRate = float(0)
        self.JerkRate = float(0)
        self.ToolNo = int(0)
        self.BlendingMode = BlendingModeEnum.EXACT_STOP
        self.MoveTime = int(0)
        self.ConfigMode = ArmConfigParameter()
        self.Manipulation = bool(False)
        self.EmitterID = ARRAY(0, 3, int)