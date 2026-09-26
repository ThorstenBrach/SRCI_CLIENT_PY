"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteRobotSwLimitsRecvData
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

from ctypes.wintypes import BOOL
from RobotLibrary.Structures.Common.RspHeader import RspHeader


class WriteRobotSwLimitsRecvData(RspHeader):
    """Structure for received data from WriteRobotSwLimits command."""
    
    RestartRequested : BOOL
    """TRUE, when Software limits were overwritten but not activated on RC until a restart of the RC"""


    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.RestartRequested = BOOL(0)
