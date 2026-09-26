"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MeasuringInputResult
Author:      Thorsten Brach
Date:        2025-12-20

Description:

Copyright:
    (C) 2025 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from RobotLibrary.IEC_Types import USINT, IEC_Struct
from RobotLibrary.Structures.Cartesian.RobotCartesianPosition import RobotCartesianPosition
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointPosition

class MeasuringInputResult(IEC_Struct):
    
    MeasuredCartesianPosition: RobotCartesianPosition
    """
    Measured robot position value at the rising edge of the digital input
    in selected coordinate systems (see input parameters ToolNo and FrameNo).
    """

    ToolNo: USINT
    """
    Index of tool of returned position
    • 0: Flange
    • 1..254: Tool frames
    """

    FrameNo: USINT
    """
    Index of frame of returned position
    • 0: WCS
    • 1..254: User frames
    """

    MeasuredJointPosition: RobotJointPosition
    """
    Measured robot position value at the rising edge of the digital input
    in Joint position.
    """