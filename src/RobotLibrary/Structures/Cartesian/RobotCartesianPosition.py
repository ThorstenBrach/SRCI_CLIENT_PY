"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotCartesianPosition
Author:      Thorsten Brach
Date:        2025-12-18

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

from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Structures.Miscellaneous.ArmConfigParameter import ArmConfigParameter
from RobotLibrary.Structures.Miscellaneous.TurnNumber import TurnNumber

class RobotCartesianPositionBase(IEC_Struct):
    """
    TCP Cartesian position and orientation.
    """
    
    X: float
    """
    TCP Position on the X-Axis
    """
    
    Y: float
    """ 
    TCP Position on the Y-Axis
    """
    
    Z: float
    """
    TCP Position on the Z-Axis
    """
    
    Rx: float
    """
    Rotation around the X-Axis (RX)
    """
    
    Ry: float
    """
    Rotation around the Y-Axis (RY)
    """
    
    Rz: float
    """
    Rotation around the Z-Axis (RZ)
    """
    
    
    
class RobotCartesianPositionShort(RobotCartesianPositionBase):
  
    Config     : ArmConfigParameter
    """
    Configuration data of the robot (Config)
    """
  
    TurnNumber : TurnNumber
    """ 
    Turn number of the axes (TurnNumber)
    """
 
    E1 : float
    """
    Position of first external axis
    """


class RobotCartesianPosition(RobotCartesianPositionShort):
    E2         : float
    """
    Position of second external axis
    """

    E3         : float
    """
    Position of third external axis
    """
    
    E4         : float
    """
    Position of fourth external axis
    """
    
    E5         : float
    """
    Position of fifth external axis
    """
    
    E6         : float
    """
    Position of sixth external axis
    """
    
class RobotCartesianPositionExt(IEC_Struct):
    E2         : float
    """
    Position of second external axis
    """

    E3         : float
    """
    Position of third external axis
    """
    
    E4         : float
    """
    Position of fourth external axis
    """
    
    E5         : float
    """
    Position of fifth external axis
    """
    
    E6         : float
    """
    Position of sixth external axis
    """