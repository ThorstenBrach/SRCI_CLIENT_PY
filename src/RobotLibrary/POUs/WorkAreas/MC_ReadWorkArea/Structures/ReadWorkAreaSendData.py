"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadWorkAreaSendData
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

from RobotLibrary.IEC_Types import USINT
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader


class ReadWorkAreaSendData(CmdHeader):
    """Structure for received data from ReadWorkArea command."""
    
    WorkAreaNo : USINT
    """
    Index of the robot work area
     • 0 (default)..254
    """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.WorkAreaNo = USINT(0)