"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      UnitLimitAxis
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

class UnitLimitAxis(USINTEnum):

    PERCENTAGE = 0
    """
    Percentage (%) (default)
    """

    NEWTONMETER = 1
    """
    Newton meter (Nm)
    """

    MILLIAMPERE = 2
    """
    Milliampere (mA)
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)        