"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      FrameCalculationMode
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

class FrameCalculationMode(SINTEnum):
    THREE_POINT_METHOD = 0
    """
    0: Three-Point-method (default)
    """

    FOUR_POINT_METHOD = 1
    """
    1: Four-Point-method
    """

    ONE_POINT_METHOD = 2
    """
    2: One-Point-method
    """
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    