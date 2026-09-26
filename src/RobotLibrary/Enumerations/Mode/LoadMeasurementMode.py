"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      LoadMeasurementMode
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

class LoadMeasurementMode(USINTEnum):
    ONE_POSITION = 0
    """
    0: One Position (default)\n
    Use one defined position and optional axes ranges
    """

    CONFIGURATION_ANGLE = 1
    """
    1: Configuration Angle\n
    Use one defined position and optional axes ranges
    """

    AREA = 2
    """
    2: Area\n
    Use a defined area for the measurement
    """

    TWO_POSITIONS = 3
    """
    3: Two Positions\n
    Use defined positions for the measurement
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    