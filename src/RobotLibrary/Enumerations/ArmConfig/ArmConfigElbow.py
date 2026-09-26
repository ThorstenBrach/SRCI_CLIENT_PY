"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ArmConfigElbow
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
from RobotLibrary.IEC_Types import INT, INTEnum

class ArmConfigElbow(INTEnum): 

    """
    Defines how the elbow configuration of the robot arm is handled
    during a movement.
    """
    
    USE_CONFIG = 0
    """
    Use configuration defined in the target position.
    """

    SAME = 1
    """
    Do not change configuration with this movement. (default)
    """

    FREE = 2
    """
    Configuration in position is not used; the robot may freely change configuration.
    """

    DOWN = 3
    """
    Set elbow configuration in position to Down.
    """

    UP = 4
    """
    Set elbow configuration in position to Up.
    """
    
    # Set enum size for ctypes evaluation
    setattr(INTEnum, 'ctypes_type', INT)