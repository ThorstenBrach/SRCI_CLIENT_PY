"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      BlendingMode
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

class BlendingMode(USINTEnum):

    EXACT_STOP = 0
    """
    Appended, buffered, no blending
    """

    DEFINED_VELOCITY = 2
    """
    Start blending when the defined velocity is reached
    """

    CORNER_DISTANCE = 3
    """
    Define blending sphere with radius
    """

    MAX_CORNER_DEVIATION = 4
    """
    Define blending with deviation
    """

    CORNER_DISTANCE_2R = 10
    """
    Define blending sphere with 2 radiuses
    """

    RAMP_OVERLAP = 11
    """
    Define blending with percentage of overlapping of deceleration and acceleration ramp
    """

    CORNER_DISTANCE_1R = 12
    """
    Define blending sphere with starting radius
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)        