"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadFrameDataSendData
Author:      Thorsten Brach
Date:        2026-01-05

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


class ReadFrameDataSendData(CmdHeader):
    """Structure for received data from ReadFrameData command."""
    
    FrameNo       : USINT
    """
     Frame index\n
     • -1: Currently used frame on RC\n
     • 0: WCS\n
     • 1 (default)..254: UCS (User frames)\n
    """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.FrameNo = USINT(0)