"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadFrameDataRecvData
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

from RobotLibrary.IEC_Types import BYTE, USINT, BOOL
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.Data.Frame.FrameData import FrameData as FrameDataStruct


class ReadFrameDataRecvData(RspHeader):
    """Structure for received data from ReadFrameData command."""
    
    Reserve       : BYTE
    """Reserve"""

    FrameNoReturn : USINT
    """Frame index"""
    
    FrameData     : FrameDataStruct
    """Frame data (see chapter 5.5.6.2)"""

    DataChanged   : BOOL
    """The status bit "DataChanged" represents the modification state"""


    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.Reserve       = BYTE(0)
        self.FrameNoReturn = USINT(0)
        self.FrameData     = FrameDataStruct()
        self.DataChanged   = BOOL(False)