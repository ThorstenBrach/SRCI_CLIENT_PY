"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      PriorityLevel
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

from RobotLibrary.IEC_Types import BYTE, BYTEEnum

class PriorityLevel(BYTEEnum):

    VERY_HIGH = 1
    """
    Priority level is very high
    """

    HIGH = 2
    """
    Priority level is high
    """

    NORMAL = 3
    """
    Priority level is normal
    """

    LOW = 4
    """
    Priority level is low
    """
    
    # Set enum size for ctypes evaluation
    setattr(BYTEEnum, 'ctypes_type', BYTE)    