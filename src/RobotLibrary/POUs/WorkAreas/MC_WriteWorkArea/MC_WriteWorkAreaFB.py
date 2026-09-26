"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_WriteWorkAreaFB
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

from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseExecuteFB import RobotLibraryBaseExecuteFB
from .Structures.WriteWorkAreaParCmd import WriteWorkAreaParCmd
from .Structures.WriteWorkAreaOutCmd import WriteWorkAreaOutCmd

class MC_WriteWorkAreaFB(RobotLibraryBaseExecuteFB):
    """Function block to write work area data to the robot controller."""
    
    ParCmd : WriteWorkAreaParCmd # ToDo
    OutCmd : WriteWorkAreaOutCmd