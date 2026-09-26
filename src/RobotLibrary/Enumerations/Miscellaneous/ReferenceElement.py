"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReferenceElement
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

from RobotLibrary.IEC_Types import USINT, USINTEnum

class ReferenceElement(USINTEnum):

    NOT_USED = 0
    """
    0 (default): Not used
    """

    X_AXIS = 1
    """
    1: X-Axis
    """

    Y_AXIS = 2
    """
    2: Y-Axis
    """

    Z_AXIS = 3
    """
    3: Z-Axis
    """

    XY_PLANE = 4
    """
    4: XY-Plane
    """

    XZ_PLANE = 5
    """
    5: XZ-Plane
    """

    YZ_PLANE = 6
    """
    6: YZ-Plane
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)