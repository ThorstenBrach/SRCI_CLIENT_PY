"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotWorkAreaDataLimitJoint
Author:      Thorsten Brach
Date:        2025-12-20

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

from RobotLibrary.IEC_Types import REAL,IEC_Struct

    
class RobotWorkAreaDataLimitJoint(IEC_Struct):
    LowerLimit: REAL
    """
    Relates to AreaType Axes.
    Negative work area limit for Joint
    • 0 (default) : No work area restriction of joint if lower and upper limit are set to 0
    • 16#FFFF_FFFF: No lower work area restrictions for Joint
    """

    UpperLimit: REAL
    """
    Relates to AreaType Axes.
    Positive work area limit for Joint
    • 0 (default) : No work area restriction of joint if lower and upper limit are set to 0
    • 16#FFFF_FFFF: No lower work area restrictions for Joint
    """