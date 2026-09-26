"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadWorkAreaRecvData
Author:      Thorsten Brach
Date:        2026-01-24

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

from RobotLibrary.IEC_Types import BYTE, USINT, BOOL
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.Data.WorkArea.RobotWorkAreaData import RobotWorkAreaData


class ReadWorkAreaRecvData(RspHeader):
    """Structure for received data from ReadWorkArea command."""
    
    Reserve          : BYTE
    """Reserve"""
    
    WorkAreaNoReturn : USINT    
    """Index of the robot work area"""    
    
    WorkAreaData     : RobotWorkAreaData
    """Data specific to the work area requested by Index."""
    
    DataChanged      : BOOL
    """The status bit "DataChanged" represents the modification state"""

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.Reserve          = BYTE(0)
        self.WorkAreaNoReturn = USINT(0)
        self.WorkAreaData     = RobotWorkAreaData()
        self.DataChanged      = BOOL(False)