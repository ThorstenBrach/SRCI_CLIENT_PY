"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteLoadDataParCmd
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
from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Structures.Data.Load.LoadData import LoadData

class WriteLoadDataParCmd(IEC_Struct):
    
    LoadNo : int
    """
    Specifies the desired target values that shall be written\n
    Load index\n
     •      0: (default) - Not possible to write\n
     • 1..254: Load data
    """
    LoadData : LoadData
    """Load data (see chapter 5.5.6.4)"""
