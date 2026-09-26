"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadRobotSwLimitsRecvData
Author:      Thorsten Brach
Date:        2026-01-21

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
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.Miscellaneous.SWLimits import SWLimits


class ReadRobotSwLimitsRecvData(RspHeader):
    """Structure for received data from ReadRobotSwLimits command."""
    
    LimitValues : SWLimits
    """Limits for joints and external axes according to Table 6-173."""
    DataChanged : BOOL
    """The status bit "DataChanged" represents the modification state"""


    #------------------------------------------------------------
    # Constructor + Initialization
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.LimitValues      = SWLimits()
        self.DataChanged      = BOOL(False)