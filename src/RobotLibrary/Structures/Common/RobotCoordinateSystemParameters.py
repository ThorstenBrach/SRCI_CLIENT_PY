"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotCoordinateSystemParameters
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

from RobotLibrary.IEC_Types import USINT, IEC_Struct

    
class RobotCoordinateSystemParameters(IEC_Struct):
  
    ToolNo : USINT
    """
    Index of target tool
    • 0: Flange (default)
    • 1..254: Tool frames
    """
    
    FrameNo : USINT
    """
    Index of target frame
    • 0: WCS (default)
    • 1..254: User frames
    """