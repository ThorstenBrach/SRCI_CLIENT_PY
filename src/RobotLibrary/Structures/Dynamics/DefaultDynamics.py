"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      DefaultDynamics
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
    
class DefaultDynamics(IEC_Struct):
    Timestamp: IEC_TIMESTAMP
    """Timestamp"""

    VelocityRate: REAL
    """
    Maximum velocity for the axes.
    Range [%]:
    •  <0% : Use default velocity given by the user
    •   0% : Use internal minimal velocity
    • 100% : Use the entire reference velocity, given by the user
    """

    AccelerationRate: REAL
    """
    Maximum acceleration.
    Range [%]:
    •  <0% : Use default acceleration given by the user
    •   0% : Use internal minimal acceleration
    • 100% : Use the entire reference acceleration, given by the user
    """

    DecelerationRate: REAL
    """
    Maximum deceleration.
    Range [%]:
    •  <0% : Use default deceleration given by the user
    •   0% : Use internal minimal deceleration
    • 100% : Use the entire reference deceleration, given by the user
    """

    JerkRate: REAL
    """
    Maximum jerk.
    Range [%]:
    •  <0% : Use default jerk given by the user
    •   0% : Use internal minimal jerk
    • 100% : Use the entire reference jerk, given by the user
      (Trapezoidal if possible)
    """