"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteRobotSwLimitsSendData
Author:      Thorsten Brach
Date:        2026-01-22

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

from RobotLibrary.IEC_Types import BOOL
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader
from RobotLibrary.Structures.Miscellaneous.SWLimits import SWLimits 


class WriteRobotSwLimitsSendData(CmdHeader):
    """Structure for received data from WriteRobotSwLimits command."""
    
    LimitValues            : SWLimits
    """Limits for joints and external axes according to Table 6-180."""

    ResetToFactoryDefaults : BOOL
    """Reset limits to RC specific factory settings"""

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.LimitValues = SWLimits()
        self.ResetToFactoryDefaults = BOOL(0)