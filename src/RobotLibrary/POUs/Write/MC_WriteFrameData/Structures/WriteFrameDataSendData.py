"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteFrameDataSendData
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

from RobotLibrary.IEC_Types import BYTE, USINT
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader
from RobotLibrary.Structures.Data.Frame.FrameData import FrameData as FrameDataStruct


class WriteFrameDataSendData(CmdHeader):
    """Structure for received data from WriteFrameData command."""
    
    Reserve       : BYTE
    """Reserve"""
    
    FrameData     : FrameDataStruct
    """Frame data (see chapter 5.5.6.2)"""

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
        self.Reservev = BYTE(0)
        self.FrameData = FrameDataStruct()
        self.FrameNo   = USINT(0)