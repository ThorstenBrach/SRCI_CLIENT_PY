"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      LimitMode
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

class LimitMode(USINTEnum):
    NO_LIMIT_DEFINED = 0
    """
    0: No limit defined (default)\n
    The robot can be moved in the direction set with the input parameter \"CompliantAxes\"\n
    in a compliant manner by applying an external force on it.\n
    By reaching the mechanical or software limits, the robot stops.
    """

    LIMIT_DEFINED = 1
    """
    1: Limit defined\n
    The robot can be moved along the defined vector in a compliant manner by applying an external force on it.\n
    By reaching the vector limit defined by the input parameter \"VectorData\", the robot stops.
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    