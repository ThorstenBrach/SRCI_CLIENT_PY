"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      StepMode
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

from RobotLibrary.IEC_Types import USINT, USINTEnum

class StepMode(USINTEnum):
    DEACTIVATE = 0
    """
    StepMode is deactivated
    """

    BLENDING = 1
    """
    Blending\n
    • The robot moves on the blended trajectory\n
    • The movement is interrupted when the active segment changes
    """

    EXACT_STOP = 2
    """
    Exact stop\n
    • The robot moves to the defined target positions without blending\n
    • The movement is interrupted when the defined target position is reached
    """
