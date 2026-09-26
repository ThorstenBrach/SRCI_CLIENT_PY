"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadToolDataSendData
Author:      Thorsten Brach
Date:        2026-01-20

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


class ReadToolDataSendData(CmdHeader):
    """Structure for received data from ReadToolData command."""
    
    ToolNo       : USINT
    """
    Tool index\n
     • -1: Currently used tool on RC\n
     •  0: Flange -  Not possible to change\n
     • 1 (default)..254: Tool Frame\n
    """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.ToolNo = USINT(0)