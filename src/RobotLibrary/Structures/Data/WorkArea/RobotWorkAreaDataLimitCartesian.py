"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotWorkAreaDataLimitCartesian
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

    
class RobotWorkAreaDataLimitCartesian(IEC_Struct):
    LowerLimit: REAL 
    """
    Relates to AreaType Box, Cylinder and Sphere.
    Distance in negative Direction - Default 0
    """

    UpperLimit: REAL 
    """
    Relates to AreaType Box, Cylinder and Sphere.
    Distance in positive Direction - Default 0
    """