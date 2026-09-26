"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadToolDataRecvData
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

from RobotLibrary.IEC_Types import BYTE, USINT, BOOL
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.Data.Tool.ToolData import ToolData as ToolDataStruct


class ReadToolDataRecvData(RspHeader):
    """Structure for received data from ReadToolData command."""
    
    
    Reserve      : BYTE
    """Reserve"""
    
    ToolNoReturn : USINT
    """Tool index"""
    
    ToolData     : ToolDataStruct
    """Tool data"""

    DataChanged   : BOOL
    """The status bit "DataChanged" represents the modification state"""


    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.Reserve      = BYTE(0)
        self.ToolNoReturn = USINT(0)
        self.ToolData     = ToolDataStruct()
        self.DataChanged  = BOOL(False)