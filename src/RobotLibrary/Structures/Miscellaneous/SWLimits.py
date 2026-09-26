"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SWLimits
Author:      Thorsten Brach
Date:        2025-12-18

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
from RobotLibrary.IEC_Types import REAL, IEC_Struct
from ..DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP

class SWLimits(IEC_Struct):
    Timestamp: IEC_TIMESTAMP
    """Timestamp"""

    J1LowerLimit: REAL
    """Negative software limit for Joint J1 [mm/°]"""

    J1UpperLimit: REAL
    """Positive software limit for Joint J1 [mm/°]"""

    J2LowerLimit: REAL
    """Negative software limit for Joint J2 [mm/°]"""

    J2UpperLimit: REAL
    """Positive software limit for Joint J2 [mm/°]"""

    J3LowerLimit: REAL
    """Negative software limit for Joint J3 [mm/°]"""

    J3UpperLimit: REAL
    """Positive software limit for Joint J3 [mm/°]"""

    J4LowerLimit: REAL
    """Negative software limit for Joint J4 [mm/°]"""

    J4UpperLimit: REAL
    """Positive software limit for Joint J4 [mm/°]"""

    J5LowerLimit: REAL
    """Negative software limit for Joint J5 [mm/°]"""

    J5UpperLimit: REAL
    """Positive software limit for Joint J5 [mm/°]"""

    J6LowerLimit: REAL
    """Negative software limit for Joint J6 [mm/°]"""

    J6UpperLimit: REAL
    """Positive software limit for Joint J6 [mm/°]"""

    E1LowerLimit: REAL
    """Negative software limit for axis E1 [mm/°]"""

    E1UpperLimit: REAL
    """Positive software limit for axis E1 [mm/°]"""

    E2LowerLimit: REAL
    """Negative software limit for axis E2 [mm/°]"""

    E2UpperLimit: REAL
    """Positive software limit for axis E2 [mm/°]"""

    E3LowerLimit: REAL
    """Negative software limit for axis E3 [mm/°]"""

    E3UpperLimit: REAL
    """Positive software limit for axis E3 [mm/°]"""

    E4LowerLimit: REAL
    """Negative software limit for axis E4 [mm/°]"""

    E4UpperLimit: REAL
    """Positive software limit for axis E4 [mm/°]"""

    E5LowerLimit: REAL
    """Negative software limit for axis E5 [mm/°]"""

    E5UpperLimit: REAL
    """Positive software limit for axis E5 [mm/°]"""

    E6LowerLimit: REAL
    """Negative software limit for axis E6 [mm/°]"""

    E6UpperLimit: REAL
    """Positive software limit for axis E6 [mm/°]"""