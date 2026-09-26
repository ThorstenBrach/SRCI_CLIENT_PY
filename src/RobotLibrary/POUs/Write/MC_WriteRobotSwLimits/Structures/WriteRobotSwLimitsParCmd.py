"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteRobotSwLimitsParCmd
Author:      Thorsten Brach
Date:        2026-01-16
Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Structures.Miscellaneous.SWLimits import SWLimits

class WriteRobotSwLimitsParCmd(IEC_Struct):

    LimitValues : SWLimits
    """DLimits for joints and external axes according to Table 6-173."""

    ResetToFactoryDefaults : bool
    """Reset limits to RC specific factory settings"""

