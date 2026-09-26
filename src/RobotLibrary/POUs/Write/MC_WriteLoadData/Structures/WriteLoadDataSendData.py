"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteLoadDataSendData
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

from RobotLibrary.IEC_Types import USINT
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader
from RobotLibrary.Structures.Data.Load.LoadData import LoadData as LoadDataStruct


class WriteLoadDataSendData(CmdHeader):
    """Structure for received data from WriteLoadData command."""
    
    LoadData     : LoadDataStruct
    """Load data"""

    LoadNo       : USINT
    """
     Load index\n
     •      0: (default) - Not possible to write\n
     • 1..254: Load data\n
    """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.LoadData = LoadDataStruct()
        self.LoadNo   = USINT(0)