"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteToolDataSendData
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
from RobotLibrary.Structures.Data.Tool.ToolData import ToolData as ToolDataStruct


class WriteToolDataSendData(CmdHeader):
    """Structure for received data from WriteToolData command."""

    Reserve      : BYTE
    """Reserve"""
    
    ToolData     : ToolDataStruct
    """Tool data"""

    ToolNo       : USINT
    """
     Tool index\n
     •      0: Flange (default) Not possible to change
     • 1..254: Tool Frame
    """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.ToolData = ToolDataStruct()
        self.ToolNo   = USINT(0)