"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ForceStatus
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

from RobotLibrary.IEC_Types import BOOL, IEC_Struct

class ForceStatus(IEC_Struct):
    ForceControlEnabled: BOOL
    """TRUE, while a "ForceControl" function is enabled"""

    ForceLimitEnabled: BOOL
    """TRUE, while a "ForceLimit" function is enabled"""

    ApplyingForce: BOOL
    """TRUE, while robot is adjusting its movement to apply specified force"""

    MaxDeviationReached: BOOL
    """TRUE, while maximum deviation according to input parameter "MaxDeviation" is reached"""

    SpecifiedForceTorqueReached: BOOL
    """TRUE, while currently applied force/torque is identical to specified force/torque"""

    SpecifiedForceLimitReached: BOOL
    """TRUE, while currently detected force is identical to specified force limit"""

    Bit06: BOOL
    """Bit 06 Reserve"""

    Bit07: BOOL
    """Bit 07 Reserve"""