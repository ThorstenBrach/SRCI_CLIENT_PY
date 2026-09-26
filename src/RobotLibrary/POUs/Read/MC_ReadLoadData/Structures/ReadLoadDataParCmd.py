"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadLoadDataParCmd
Author:      Thorsten Brach
Date:        2026-01-11

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

class ReadLoadDataParCmd(IEC_Struct):
    
    """
    Load index\n
    • -1: Currently used load on RC\n
    •  0: Not possible to read\n
    •  1 (default)..254: Load data\n
    """
    LoadNo : int