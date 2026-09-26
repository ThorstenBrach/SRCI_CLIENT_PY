"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TriggerModeLimit
Author:      Thorsten Brach
Date:        2025-12-14

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

from RobotLibrary.IEC_Types import SINT, SINTEnum

class TriggerModeLimit(SINTEnum):
    INVALID = 0
    """
    0: Invalid (default)
    """

    JOINT_CURRENT = 1
    """
    1: Joint current in mA
    """

    FORCE = 2
    """
    2: Force in Nm
    """

    FOLLOWING_ERROR = 3
    """
    3: Following error\nThe distance of the robot position from the path that was calculated
    """

    TEMPERATURE = 4
    """
    4: Temperature in °C
    """
    
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    