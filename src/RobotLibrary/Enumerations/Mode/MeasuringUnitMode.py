"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MeasuringUnitMode
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

class MeasuringUnitMode(USINTEnum):
    VECTOR_LENGTH = 0  
    """
    0: VectorLength (default)\n
    Defines the distance in millimeter between two points in cartesian space
    """
    SEGMENT_LENGTH = 1
    """
    1: SegmentLength\n
    Defines the distance in mm covered between the two points in cartesian space
    """
    TIME_DURATION = 2
    """
    2: Time\n
    Defines the duration in milliseconds between the start and end point
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    