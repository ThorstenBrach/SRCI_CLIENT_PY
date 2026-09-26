"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MoveAxesAbsoluteDataSendData
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

from RobotLibrary.IEC_Types import USINT , SINT, UINT, REAL, ARRAY, BOOL, BYTE
from RobotLibrary.Enumerations.Mode.BlendingMode import BlendingMode as BlendingModeEnum
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointPosition

class MoveAxesAbsoluteSendData(CmdHeader):
    """Structure for received data from MoveAxesAbsolute command."""
    
    EmitterID          : ARRAY[SINT] = ARRAY(0, 4, SINT) 
    """
    ID of Action that will be executed when this command is active
     • >0: Start Action - Start executing the Action function with the identical ListenerID.
     • <0: Stop Action  -  Stop executing the Action function with the identical ListenerID.
     • 0: No trigger (default)-  If no EmitterID is defined, the function will not trigger any Action during its execution
    For more information see section Triggers of this chapter or chapter 5.5.12.4.
    """

    ListenerID         : SINT
    """
    ID of the trigger function that may be triggered:
     • 0: Immediately (default). - Start executing THIS function immediately.
     • >0: Triggero Start executing when the trigger function with the identical EmitterID is called.
    For more information see chapter 5.5.12.4.
    """

    Reserve            : SINT
    """Reserve"""

    VelocityRate       : UINT
    """
    Axes velocity in % of nominal velocity.
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

    ToolNo             : USINT
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

    BlendingParameter  : ARRAY[REAL] = ARRAY(0, 1, REAL) 
    """
    Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius
    """

    JointPosition      : RobotJointPosition
    """
    Absolute end position of the robot in Joint position.
    """

    Manipulation       : BOOL
    """
    Set TRUE to allow manipulation of this move command through superimposing functions.
    For more information see chapter 5.5.9.5
    """

    Reserve2           : BYTE
    """Reserve"""

    MoveTime           : UINT
    """
    Parameter is used if it is greater than 0 (default)
    • Velocity input is ignored
    • Parameter defines the time for the movement to reach the target position
    Error is sent by the RC if the time cannot be kept
    """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        
        super().__init__()
        self.EmitterID = ARRAY(0, 3, SINT)
        self.ListenerID = SINT(0)
        self.Reserve = SINT(0)
        self.VelocityRate = UINT(0)
        self.AccelerationRate = UINT(0)
        self.DecelerationRate = UINT(0)
        self.JerkRate = UINT(0)
        self.ToolNo = USINT(0)
        self.BlendingMode = BlendingModeEnum.EXACT_STOP
        self.BlendingParameter = ARRAY(0, 1, REAL)
        self.JointPosition = RobotJointPosition()
        self.Manipulation = BOOL(False)
        self.Reserve2 = BYTE(0)
        self.MoveTime = UINT(0)
