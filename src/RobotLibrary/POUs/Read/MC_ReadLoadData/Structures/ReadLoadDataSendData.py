"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadLoadDataSendData
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


class ReadLoadDataSendData(CmdHeader):
    """Structure for received data from ReadLoadData command."""
    
    LoadNo       : USINT
    """
    Load index\n
     • -1: Currently used load on RC\n
     •  0: Not possible to read\n
     •  1 (default)..254: Load data\n
    """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.LoadNo = USINT(0)