"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReferenceDynamics
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
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP
    
class ReferenceDynamics(IEC_Struct):
    
    
    Timestamp: IEC_TIMESTAMP
    """Timestamp"""

    VelocityReference: REAL
    """
    Path velocity [mm/s] (tangent) at 100%
    • <0: (default) - Do not change values
    • ≥0: Change values according to input value
    """

    AccelerationReference: REAL
    """
    Path acceleration [mm/s2] at 100%
    • <0: (default) - Do not change values
    • ≥0: Change values according to input value
    """

    DecelerationReference: REAL
    """
    Path deceleration [mm/s2] at 100%
    • <0: (default) - Do not change values
    • ≥0: Change values according to input value
    """

    JerkReference: REAL
    """
    Jerk [mm/s3] at 100%
    • <0: (default) - Do not change values
    • ≥0: Change values according to input value
    """