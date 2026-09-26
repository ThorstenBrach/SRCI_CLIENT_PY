"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      PathChoice
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

from RobotLibrary.IEC_Types import BYTE, BYTEEnum

class PathChoice(BYTEEnum):

    CLOCKWISE = 0
    """
    Clockwise movement of the circular path
    """

    COUNTERCLOCKWISE = 1
    """
    Counterclockwise movement of the circular path
    """
    # Set enum size for ctypes evaluation
    setattr(BYTEEnum, 'ctypes_type', BYTE)        