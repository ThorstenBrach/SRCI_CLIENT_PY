"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      CollisionReactionMode
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

class CollisionReactionMode(USINTEnum):
    STANDING_STILL = 0
    """
    Standing still
    """

    REVERSED_MOVEMENT = 1
    """
    Reversed movement
    """
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    