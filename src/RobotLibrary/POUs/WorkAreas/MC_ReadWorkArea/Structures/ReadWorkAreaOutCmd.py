"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadWorkAreaOutCmd
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
from RobotLibrary.Structures.Data.WorkArea.RobotWorkAreaData import RobotWorkAreaData

class ReadWorkAreaOutCmd(IEC_Struct):
    
    WorkAreaNoReturn       : int
    """Index of the robot work area"""
    WorkAreaData           : RobotWorkAreaData
    """Data specific to the work area requested by Index."""
