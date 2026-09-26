"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadLoadDataRecvData
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

from RobotLibrary.IEC_Types import BYTE, USINT, BOOL
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.Data.Load.LoadData import LoadData as LoadDataStruct


class ReadLoadDataRecvData(RspHeader):
    """Structure for received data from ReadLoadData command."""
    
    LoadNoReturn : USINT
    """Load index"""
    
    LoadData     : LoadDataStruct
    """Load data (see chapter 5.5.6.2)"""

    DataChanged   : BOOL
    """The status bit "DataChanged" represents the modification state"""


    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.LoadNoReturn = USINT(0)
        self.LoadData     = LoadDataStruct()
        self.DataChanged   = BOOL(False)