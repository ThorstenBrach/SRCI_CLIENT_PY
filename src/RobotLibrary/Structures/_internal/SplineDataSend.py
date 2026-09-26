"""
 ------------------------------------------------------------------------- 
  SRCI Robot Library                                                
 ------------------------------------------------------------------------- 
                                                                           
  Object:      SplineDataSend                                       
  Author:      Thorsten Brach                                                
  Date:        2025-12-13

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

# Import iec data types
from RobotLibrary.IEC_Types import USINT, UINT, IEC_Struct 
from RobotLibrary.Structures.Cartesian.RobotCartesianPosition import RobotCartesianPosition


class SplineDataSend(IEC_Struct):
    _pack_ = 1
    
    Position: RobotCartesianPosition 
    """Absolute target coordinates in the selected coordinate system (see ToolNo and FrameNo)."""

    VelocityRate: UINT
    """
    TCP velocity in % of nominal velocity.\n
    •  <0% : Use default velocity (default)\n
    •   0% : Use internal minimal velocity\n
    • 100% : Use maximal reference velocity\n
    • See chapter 5.5.7 Robot dynamics\n
    """

    AccelerationRate: UINT 
    """
    Acceleration for movement in % of nominal acceleration.\n
    •  <0% : Use default acceleration (default)\n
    •   0% : Use internal minimal acceleration\n
    • 100% : Use maximal reference acceleration\n
    • See chapter 5.5.7 Robot dynamics\n
    """

    DecelerationRate: UINT
    """
    Deceleration for movement in % of nominal deceleration.\n
    •  <0% : Use default deceleration (default)\n
    •   0% : Use internal minimal deceleration\n
    • 100% : Use maximal reference deceleration\n
    • See chapter 5.5.7 Robot dynamics\n
    """

    JerkRate: UINT
    """
    Jerk of the movement in % of nominal jerk.\n
    •  <0% : Use default jerk (default)\n
    •   0% : Use internal minimal jerk\n
    • 100% : Use maximal reference jerk\n
    • See chapter 5.5.7 Robot dynamics\n
    """

    ToolNo: USINT
    """
    Index of tool\n
    0: Flange (default)\n
    1..254: Tool frames\n
    """

    FrameNo: USINT
    """
    Index of frame\n
    0: WCS (default)\n
    1..254: User frames\n
    """

    MoveTime: UINT
    """
    [ms] Parameter is used if it is greater than 0 (default):\n
    Parameter defines the time for the movement to reach the target position\n
    Velocity input can be ignored\n
    Acceleration, Deceleration and jerk will be ignored\n
    Define two consecutive points with identical positions and specified Time to realize waiting time on spline.\n
    Error is sent by the RC, if the time cannot be kept.\n
    """
    