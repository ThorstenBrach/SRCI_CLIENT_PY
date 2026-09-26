"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MeasuringIoMode
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

class MeasuringIoMode(USINTEnum):
    MEASUREMENT_AT_NEXT_RISING_EDGE = 0
    """
    Measurement at next rising edge\n
    Output "MeasuredPosition_1" used
    """

    MEASUREMENT_AT_NEXT_FALLING_EDGE = 1
    """
    Measurement at next falling edge\n
    Output "MeasuredPosition_1" used
    """

    MEASUREMENT_AT_NEXT_EDGE = 2
    """
    Measurement at next edges, regardless of rising or falling edges\n
    First position stored in output "MeasuredPosition_1"\n
    Second position stored in output "MeasuredPosition_2"
    """

    MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_RISING = 3
    """
    Measurement at two edges, beginning with the rising edge\n
    Rising edge = "MeasuredPosition_1"\n
    Falling edge = "MeasuredPosition_2"
    """

    MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_FALLING = 4
    """
    Measurement at two edges, beginning with the falling edge\n
    Falling edge = "MeasuredPosition_1"\n
    Rising edge = "MeasuredPosition_2"
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)