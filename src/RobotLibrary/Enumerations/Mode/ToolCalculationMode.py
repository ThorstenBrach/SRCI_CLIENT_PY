"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ToolCalculationMode
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

class ToolCalculationMode(SINTEnum):
    TWO_POINT_Z_METHOD = 0
    """
    0: Two Point + Z-Method (default)
    """

    THREE_POINT_METHOD = 1
    """
    1: Three-Point-Method
    """

    FOUR_POINT_METHOD = 2
    """
    2: Four-Point-Method
    """

    FIVE_POINT_METHOD = 3
    """
    3: Five-Point-Method
    """

    SIX_POINT_METHOD = 4
    """
    4: Six-Point-Method
    """

    ABC_WORLD_METHOD = 5
    """
    5: ABC-World-Method
    """

    ABC_TWO_POINT_METHOD = 6
    """
    6: ABC-Two-Point-Method
    """
    
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    