"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      LogParameter
Author:      Thorsten Brach
Date:        2025-12-18

Description:

Copyright:
    (C) 2025 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from RobotLibrary.IEC_Types import IEC_Struct 
from RobotLibrary.Enumerations.Level.LogLevel import LogLevel

    
class LogParameter(IEC_Struct):
  
    CreateCmd : LogLevel
    """
    Log level setting for creating commands 
    """

    UpdateCmd : LogLevel
    """
    Log level setting for updating commands
    """
    
    GenSeq    : LogLevel
    """
    Log level setting for generating sequence
    """

    DecSeq    : LogLevel
    """
    Log level for ??? sequence
    """