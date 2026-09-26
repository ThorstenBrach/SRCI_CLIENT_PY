"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      OrientationMode
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

class OrientationMode(SINT):
    LINEAR_INTERPOLATED = 1
    """
    Change orientation continuously in a linear way
    """

    JOINT_INTERPOLATED = 2
    """
    Change orientation continuously in a joint interpolated way of wrist joints
    """

    FIX = 3
    """
    No change of orientation during movement
    """

    PATH = 4
    """
    No change of orientation in relation to trajectory
    """
    
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    